# RunPod — renting a GPU instead of owning one

> **Decision record and session log**: `../RUNPOD_CLOUD_RENDERING.md` — why A6000 over
> 4090, what it costs, and the gotchas found the hard way.

Written 2026-08-26, while the local track was pinned to a 16GB card. The point of
this directory is to run the **existing** `minimax-h3-pipeline/` and `wan22-pipeline/`
work on rented hardware, driven from a laptop with no NVIDIA GPU at all.

Nothing here replaces those pipelines. It's transport.

---

## Why bother

`HANDOVER.md` §9 records three rejections that were all really the same rejection —
**16GB of VRAM**:

- Q5_0 / Q6_K / Q8_0 MiniMax quants (13.9–21.4GB) — didn't fit, never tried.
- WAN 2.2 14B MoE and FLUX.2 klein — "unusably slow" once weights offloaded to RAM.
- F01's wide-shot faces resolving to a blob at 864×480 — a **pixel-count** problem.
  Rendering wider/taller is the fix, and that costs VRAM.

On a 48GB card all three stop being constraints. That, not convenience, is the
reason to do this.

## Pick the GPU for VRAM, not for the badge

From RunPod's on-demand list (2026-08-26):

| GPU | VRAM | RAM | $/hr | note |
| :--- | ---: | ---: | ---: | :--- |
| A40 | 48GB | 50GB | 0.44 | cheapest 48GB |
| **RTX A6000** | **48GB** | **50GB** | **0.53** | **recommended** |
| RTX 4090 | 24GB | 31GB | 0.74 | faster per step, half the VRAM, more money |
| L40S | 48GB | 125GB | 0.99 | Ada, fast + roomy, if budget allows |
| A100 PCIe | 80GB | 117GB | 1.39 | overkill for 5B/GGUF work |

**The 4090 is the trap.** It costs *more* than the A6000 and gives *half* the VRAM,
and 24GB does not hold a 21.4GB Q8_0 plus VAE, latents and activations — you'd land
straight back in the offload failure mode that got local WAN 2.2 rejected. Its 31GB
of system RAM is also thin, given the 32B text encoder runs on CPU.

The A6000/A40 are Ampere and genuinely slower per step than a 4090. It does not
matter: avoiding offload is worth far more than the architecture gap.

## Cost — 4 hours a night, 30 nights (120 GPU-hours)

At the cached rate in `../../.usd_gbp_rate.json` (0.74075, dated 2026-08-11 — refresh it).
Includes 30GB container disk and a **200GB** network volume at $0.07/GB/month ($14).

| GPU | GPU cost | + disk + volume | **per month** |
| :--- | ---: | ---: | ---: |
| A40 | $52.80 | $14.48 | **$67.28 ≈ £49.84** |
| **RTX A6000** | $63.60 | $14.48 | **$78.08 ≈ £57.84** |
| RTX 4090 | $88.80 | $14.48 | **$103.28 ≈ £76.51** |
| L40S | $118.80 | $14.48 | **$133.28 ≈ £98.73** |
| A100 PCIe | $166.80 | $14.48 | **$181.28 ≈ £134.28** |

With a 100GB volume instead, knock $7/month (≈£5.19) off any row.

**But 120 hours is far more than the work needs.** At the measured ~3.4 min/clip
(MiniMax-H3 + EasyCache) that's ~2,100 clips; Scene 1 is on the order of 50. The
whole scene is roughly **3 hours of GPU time**, not a month of nights. Budget for
re-rolls and idle mistakes, not throughput.

## The volume is the thing that actually needs deciding

Weights inventory, from the pipeline READMEs:

| | GB |
| :--- | ---: |
| MiniMax-H3 denoisers + VAEs + encoder | ~50 |
| MiniMax turbo denoiser | 11.4 |
| Comfy-Org text encoder (safetensors) | 15.7 |
| Wan 2.2 TI2V-5B + VAE + umt5 | 17.4 |
| MuseTalk / yolo / venv / ComfyUI | ~5 |
| **total** | **~99** |

So **a 100GB volume is full on arrival**. Create it at **200GB**. Volumes can be
grown later but **never shrunk**, and they're **locked to one datacenter** — pick a
region that actually stocks the GPU you want, because you're stuck with it.

The volume bills **24/7**, whether or not a pod is running. And if the account
balance hits $0 the volume keeps accruing charges and can eventually be **deleted
with no recovery**. Don't park 200GB of weights on a dry account.

## Files here

| File | What |
| :--- | :--- |
| `setup_pod.sh` | One-shot pod bootstrap onto `/workspace`. Idempotent — the ~99GB downloads once per volume, ever. Carries every documented dependency pin and source patch. |
| `comfy.py` | Submit / poll / fetch against a ComfyUI server, local or on a pod. |
| `../../runpod_key.py` | API key in Windows Credential Manager (outside the repo, like `fal_key.py`). Only needed for the scripted path. |

## Two ways to manage pods — pick one

**RunPod's own MCP server (recommended).** Hosted, OAuth, no key on disk:

```
/plugin marketplace add runpod/runpod-plugins-official
/plugin install runpod@runpod
```

Claude can then create/start/stop/list pods and check spend directly. This is
strictly better than hand-rolling lifecycle scripts, which is why there is no
`rp.py` here.

**Or the console**, by hand. Either way, MCP does *not* drive ComfyUI — that's what
`comfy.py` is for, and it's the half that matters.

## Transport: use an SSH tunnel, not the HTTP proxy

RunPod only exposes the HTTP ports you asked for at **creation** time, and the
default template exposes 8888 (Jupyter), not 8188. Rather than recreating the pod
to add a port, tunnel it — and this is genuinely the better option anyway:

```bash
ssh -N -L 8188:localhost:8188 -i ~/.ssh/id_ed25519 -p <TCP_PORT> root@<POD_IP>
```

Leave that running in its own terminal, then `COMFY_SERVER=http://127.0.0.1:8188`.

The tunnel **removes the 100-second Cloudflare cap entirely** and streams large mp4s
without limit, so `--via-ssh` stops being necessary. Use the *direct TCP* SSH endpoint
(`root@<ip> -p <port>`), not `ssh.runpod.io` — the proxy endpoint carries no SCP/SFTP.

The `COMFY_POD` proxy path in `comfy.py` still works if you do expose 8188 at
creation; it's just the more constrained route.

## SSH keys are injected at pod creation

If you generate or register a key **after** deploying, the running pod has never seen
it and you get `Permission denied (publickey)`. Two fixes: add the key in Account
Settings and restart the pod, or — faster, no restart — enable the pod's **web
terminal** and append it by hand:

```bash
mkdir -p ~/.ssh && echo '<your ssh-ed25519 public key>' >> ~/.ssh/authorized_keys \
  && chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys
```

Register it in Account Settings too, or every future pod repeats the same dance.

## Running work

```bash
# on the pod, once per volume
bash setup_pod.sh
bash /workspace/start_comfy.sh

# on the laptop, in a second terminal: open the tunnel (see above), then
set COMFY_SERVER=http://127.0.0.1:8188
python runpod/comfy.py ping
python runpod/comfy.py run prompt.json -o outputs/
```

`prompt.json` is API-format — build it from a saved workflow with
`wan22-pipeline/comfyui-tools/graph_to_prompt.py`. That script hardcodes
`SERVER = "http://127.0.0.1:8188"` on line 8; make it read the environment so it
can introspect the pod's node set rather than a local one:

```python
SERVER = os.environ.get("COMFY_SERVER") or (
    f"https://{os.environ['COMFY_POD']}-8188.proxy.runpod.net"
    if os.environ.get("COMFY_POD") else "http://127.0.0.1:8188")
```

## Two gotchas that will bite

**The proxy has a hard 100-second cap.** `https://<POD_ID>-8188.proxy.runpod.net`
goes through Cloudflare, which kills any request past 100s with a `524`. Clips take
3–10 minutes. `comfy.py` therefore submits to `/prompt` (returns a `prompt_id`
instantly) and polls `/history/<id>` — every individual request stays short. Never
introduce a blocking render call. For large downloads, `--via-ssh` uses scp over the
direct SSH endpoint, which has no cap.

**Stopping a pod is not automatic and nobody will remind you.** A forgotten pod
overnight costs more than all of Scene 1. Stop it when the batch finishes.
