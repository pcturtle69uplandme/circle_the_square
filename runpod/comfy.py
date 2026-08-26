"""Drive a ComfyUI server - local or on a RunPod pod - over its HTTP API.

    # point at a pod (proxy URL is built from the pod id)
    set COMFY_POD=abc123xyz
    # ...or at anything else
    set COMFY_SERVER=http://127.0.0.1:8188

    python comfy.py ping                          # is it up, what's queued
    python comfy.py run prompt.json -o outputs/   # submit, poll, download
    python comfy.py submit prompt.json            # -> prompt_id, returns at once
    python comfy.py wait <PROMPT_ID> -o outputs/  # poll an in-flight job
    python comfy.py cancel                        # clear the queue

Why submit-then-poll rather than one blocking call: RunPod's HTTPS proxy sits
behind Cloudflare with a hard 100-second cap, and closes the connection with a
524 after that. Our clips take 3-10 MINUTES. ComfyUI's /prompt returns a
prompt_id immediately and does the work on its own queue, so every individual
request here stays well inside the cap. Never add a "render and wait" endpoint.

Large outputs are the other proxy hazard - a big mp4 can itself run past 100s.
--via-ssh fetches results with scp over the direct SSH endpoint instead, which
has no timeout. Use it for anything over ~50MB.
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

POLL_SECONDS = 5
REQUEST_TIMEOUT = 60  # comfortably under the proxy's 100s


def server_url():
    """COMFY_SERVER wins; otherwise build the proxy URL from COMFY_POD."""
    explicit = os.environ.get("COMFY_SERVER")
    if explicit:
        return explicit.rstrip("/")
    pod = os.environ.get("COMFY_POD")
    if pod:
        return f"https://{pod}-8188.proxy.runpod.net"
    return "http://127.0.0.1:8188"


def api(path, body=None, timeout=REQUEST_TIMEOUT, raw=False):
    url = f"{server_url()}{path}"
    data = json.dumps(body).encode() if body is not None else None
    headers = {"Content-Type": "application/json"} if data else {}
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            payload = r.read()
            return payload if raw else (json.loads(payload) if payload else {})
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")[:800]
        if exc.code == 524:
            sys.exit("error: 524 from the RunPod proxy - the request ran past Cloudflare's\n"
                     "  100-second cap. This script should never block that long; if you see\n"
                     "  this, something is calling a synchronous endpoint.")
        sys.exit(f"error: HTTP {exc.code} from ComfyUI at {url}\n  {detail}")
    except OSError as exc:
        sys.exit(f"error: cannot reach ComfyUI at {url}\n  {exc}\n"
                 "  pod still PROVISIONING? ComfyUI not started? wrong COMFY_POD?")


# ---------------------------------------------------------------- commands

def cmd_ping(args):
    stats = api("/system_stats")
    queue = api("/queue")
    devices = stats.get("devices") or []
    for d in devices:
        free = d.get("vram_free", 0) / 1e9
        total = d.get("vram_total", 0) / 1e9
        print(f"{d.get('name','gpu')}: {free:.1f}GB free / {total:.1f}GB")
    print(f"server: {server_url()}")
    print(f"queue: {len(queue.get('queue_running', []))} running, "
          f"{len(queue.get('queue_pending', []))} pending")


def cmd_submit(args):
    with open(args.prompt_json) as f:
        prompt = json.load(f)
    res = api("/prompt", {"prompt": prompt})
    pid = res.get("prompt_id")
    if not pid:
        sys.exit(f"error: no prompt_id in response: {json.dumps(res)[:400]}")
    if res.get("node_errors"):
        print(f"warning: node_errors reported: {json.dumps(res['node_errors'])[:400]}",
              file=sys.stderr)
    print(pid)
    return pid


def _outputs_for(prompt_id):
    """Return the list of output file descriptors once the job is in /history."""
    hist = api(f"/history/{prompt_id}")
    entry = hist.get(prompt_id)
    if not entry:
        return None
    status = entry.get("status", {})
    if status.get("status_str") == "error" or status.get("completed") is False:
        msgs = json.dumps(status.get("messages", []))[:800]
        sys.exit(f"error: ComfyUI reported failure for {prompt_id}\n  {msgs}")
    files = []
    for node_id, out in (entry.get("outputs") or {}).items():
        for kind in ("images", "gifs", "videos", "audio", "files"):
            for f in out.get(kind, []) or []:
                if f.get("filename"):
                    files.append(f)
    return files


def cmd_wait(args):
    pid = args.prompt_id
    started = time.time()
    last_note = 0
    while True:
        files = _outputs_for(pid)
        if files is not None:
            break
        elapsed = time.time() - started
        if args.timeout and elapsed > args.timeout:
            sys.exit(f"error: {pid} still not finished after {elapsed / 60:.1f} min - giving up "
                     "(the job may still be running on the pod).")
        if elapsed - last_note >= 60:
            q = api("/queue")
            print(f"  [{elapsed / 60:>5.1f} min] running={len(q.get('queue_running', []))} "
                  f"pending={len(q.get('queue_pending', []))}", file=sys.stderr)
            last_note = elapsed
        time.sleep(POLL_SECONDS)

    print(f"done in {(time.time() - started) / 60:.1f} min, {len(files)} output(s)",
          file=sys.stderr)
    if not args.out:
        for f in files:
            print(f"{f.get('subfolder','')}/{f['filename']}".lstrip("/"))
        return
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    for f in files:
        _download(f, outdir, args.via_ssh)


def _download(fdesc, outdir, via_ssh):
    name = fdesc["filename"]
    sub = fdesc.get("subfolder", "")
    ftype = fdesc.get("type", "output")
    dest = outdir / name
    if via_ssh:
        remote = f"/workspace/ComfyUI/{ftype}/{sub}/{name}".replace("//", "/")
        cmd = ["scp", "-P", str(via_ssh[1]), "-o", "StrictHostKeyChecking=no",
               f"{via_ssh[2]}@{via_ssh[0]}:{remote}", str(dest)]
        print(f"  scp {name}", file=sys.stderr)
        if subprocess.run(cmd).returncode != 0:
            sys.exit(f"error: scp failed for {remote}")
        return
    qs = urllib.parse.urlencode({"filename": name, "subfolder": sub, "type": ftype})
    print(f"  GET {name}", file=sys.stderr)
    blob = api(f"/view?{qs}", raw=True, timeout=300)
    dest.write_bytes(blob)
    print(f"  -> {dest} ({len(blob) / 1e6:.1f} MB)", file=sys.stderr)


def cmd_run(args):
    args.prompt_id = cmd_submit(args)
    cmd_wait(args)


def cmd_cancel(args):
    api("/queue", {"clear": True})
    api("/interrupt", {})
    print("queue cleared and current job interrupted.")


def _ssh_target(value):
    """--via-ssh host:port:user"""
    if not value:
        return None
    parts = value.split(":")
    if len(parts) == 2:
        parts.append("root")
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("expected host:port or host:port:user")
    return (parts[0], parts[1], parts[2])


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("ping", help="server up? vram? queue?").set_defaults(fn=cmd_ping)
    sub.add_parser("cancel", help="clear queue, interrupt current").set_defaults(fn=cmd_cancel)

    def add_fetch_opts(p):
        p.add_argument("-o", "--out", help="directory to download outputs into")
        p.add_argument("--via-ssh", type=_ssh_target, metavar="HOST:PORT[:USER]",
                       help="fetch with scp instead of the HTTP proxy (use for big files)")
        p.add_argument("--timeout", type=float, default=3600,
                       help="seconds to keep polling (default 3600)")

    p = sub.add_parser("submit", help="queue a job, print prompt_id, exit")
    p.add_argument("prompt_json", help="API-format JSON (see graph_to_prompt.py)")
    p.set_defaults(fn=cmd_submit)

    p = sub.add_parser("wait", help="poll an existing job and fetch its outputs")
    p.add_argument("prompt_id")
    add_fetch_opts(p)
    p.set_defaults(fn=cmd_wait)

    p = sub.add_parser("run", help="submit + wait + download")
    p.add_argument("prompt_json")
    add_fetch_opts(p)
    p.set_defaults(fn=cmd_run)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
