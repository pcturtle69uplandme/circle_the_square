# 🤖 Agent handover — rendering Circle the Square on a RunPod GPU

> **Audience**: any coding agent (Antigravity/`agy`, Gemini, Codex, another Claude session)
> picking this up cold, from any machine.
> **Written**: 2026-08-27.
> **You do not need a local GPU.** The laptop this was set up from has Intel UHD graphics
> and no CUDA at all. Everything runs on a rented pod; your machine only sends commands.

Read this whole file before running anything. The constraints below are not style
preferences — each one is a bug someone already paid for.

---

## 1. What the job is

*Circle the Square* is a British mockumentary comedy. 64 storyboard keyframes across 3
scenes need turning into video clips with dialogue. Scene 1 is 28 keyframes (F01–F26b) and
is the active work; `SCENE1_MINIMAX_TRACKER.md` is the shot-by-shot source of truth.

**One model does everything: MiniMax-H3.** It generates video *and* native synced audio in
a single pass, driven by reference images plus a text prompt.

### 🚫 Hard rule: never propose a silent video model

Any route that needs a separate TTS and lip-sync stage is **out of scope**, by explicit user
instruction. This rules out Wan 2.2 (sharper, better at wides, but video-only) and the
Wan → Qwen3-TTS → MuseTalk chain, even though that chain was validated end-to-end and is
still described in `wan22-pipeline/`. The user does not work with TTS or lip-sync tooling and
will not maintain a pipeline that needs it.

If picture quality forces the issue, the acceptable levers are, in order:
1. Render at higher resolution (`--width`/`--height`).
2. A different **single** model that also emits audio (LTX-2 is a candidate — `sd-cli`
   supports it; untested).
3. **Change the shot.** Cut to a medium for the dialogue and hold the wide either side. This
   is a legitimate and often cheapest answer. Suggest it.

---

## 2. Connecting to the pod

The pod is Linux (Ubuntu 24.04). The user's main PC is Windows. **Nothing binary transfers
between them** — don't copy `.exe` files or Windows paths across.

### 2.1 Where the connection details live

**There is no permanent address.** RunPod assigns a fresh IP and TCP port every time a pod
is created, so anything written down goes stale. Get them fresh, in this order:

1. **`runpod/pod.env` in this repo** — last known values, with the date they were captured.
   Source it: `set -a; . runpod/pod.env; set +a`. **Verify before trusting it**; if
   `ssh` gives `Connection refused` or `container not found`, it's stale — go to 2 or 3.
2. **RunPod MCP server**, if the session has it — it can list pods and their status
   directly. Install: `/plugin marketplace add runpod/runpod-plugins-official` then
   `/plugin install runpod@runpod`. Choose **Hosted** mode at the prompt (OAuth, no API key
   written to disk).
3. **The console**, by hand: [console.runpod.io](https://console.runpod.io) → the pod →
   **Connect** → **"SSH over exposed TCP"**. Ask the user to paste that line.

Use the **direct TCP** endpoint (`root@<ip> -p <port>`). The `ssh.runpod.io` proxy endpoint
also exists but has **no SCP/SFTP**, so you cannot upload refs or scripts through it.

After connecting to a new pod, **update `runpod/pod.env` and commit it** so the next agent
starts from a working address. The pod is private infrastructure in a private repo; the IP
is ephemeral and not a secret. **Never commit the private key.**

### 2.2 You need an SSH key registered on the account

Connecting needs a private key whose public half RunPod knows about. If you are on a new
machine, you have neither.

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ""
cat ~/.ssh/id_ed25519.pub          # give this to the user
```

The user adds it at **console.runpod.io → Settings → SSH Public Keys**. Strip the trailing
email comment first — it isn't needed and needn't be on a rented box.

⚠️ **Registering a key does not fix an already-running pod.** RunPod injects account keys
at pod **creation** only, so an existing pod has never seen the new key and gives
`Permission denied (publickey)`. Two fixes: have the user enable the pod's **web terminal**
and append the key by hand, or restart the pod so it re-injects.

```bash
mkdir -p ~/.ssh && echo '<public key>' >> ~/.ssh/authorized_keys \
  && chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys
```

### Layout on the pod

| Path | What | Survives pod stop? |
| :--- | :--- | :--- |
| `/workspace/minimax/models/` | ~33GB of weights | ✅ network volume |
| `/workspace/minimax/refs/` | reference images you upload | ✅ |
| `/workspace/minimax/output/` | generated clips | ✅ |
| `/workspace/minimax/bin/sd-cli` | the renderer | ✅ |
| `/workspace/minimax/gen_clip.py` | the driver script | ✅ |
| `/opt/sd.cpp`, `/opt/venv` | build tree | ❌ **erased on stop** |

Only an explicit **Stop** or **Terminate** wipes the container disk. Closing a laptop or
dropping SSH does nothing to the pod — **including nothing to the billing.**

---

## 3. Running a clip

```bash
cd /workspace/minimax
setsid nohup python3 gen_clip.py \
    --out F02_c1 --seed 202101 \
    --refs jan_peach_identity_sheet.jpg jan_office_location_sheet_fixed.png \
    --prompt "Reference 1 shows Jan. Reference 2 shows the office. ..." \
    > output/F02_c1.log 2>&1 < /dev/null & disown
```

### ⚠️ Always launch detached

`setsid nohup … & disown`. A render started in a plain SSH session **dies when that session
drops** — and the pod keeps billing while the work is lost. Watch it with
`tail -f output/<name>.log`, never by holding the terminal open.

### How references work

`--refs` are **filenames inside `refs/`**, not paths. MiniMax-H3 uses natural language, not
positional tags, so the prompt must name them: *"Reference 1 shows Jan. Reference 2 shows the
office."* Source images live in the repo at `character-refs/_photoreal-archive/` and
`location-refs/` — upload with `scp -P <PORT>`.

Use `location-refs/jan_office_location_sheet_fixed.png`, **not** the non-`_fixed` version:
the original has the London skyline through the window, and this is Cambridge.

### Useful flags

| Flag | Default | Notes |
| :--- | :--- | :--- |
| `--frames` | 56 | 2.33s @ 24fps. 56 was the 16GB ceiling — **higher is untested on 48GB and worth testing** |
| `--width` / `--height` | 864 / 480 | the wide-shot fix lever |
| `--quant` | `Q4_K` | also `Q5_0`, `Q6_K`, `Q8_0`. Only `Q4_K` is downloaded by default |
| `--vae-tiling` | off | ~20% slower, but VAE decode is a memory *spike* — try this before declaring a resolution impossible |
| `--turbo` | off | **see the warning below** |

---

## 4. Things that are already known to be broken

Do not rediscover these.

- **`--turbo` audio is garbage.** Verified with Whisper: the standard model transcribes
  dialogue exactly; turbo transcribes as empty or unrelated nonsense on every chunk, despite
  fine-looking video and non-silent waveforms. It's a 4-step audio distillation failure.
  **Only use `--turbo` for shots with no speech at all.**
- **Wide shots produce featureless blob faces at 864×480.** `HANDOVER.md` is explicit that
  this is *"a pixel-count problem, not a quantization one"* — a bigger `--quant` will not fix
  it. Higher resolution is the lever. H3-FaceRefine was tried and did **not** sharpen the
  face even when working correctly; don't retry it.
- **Naive concat corrupts audio.** Stream-copy (`ffmpeg -c copy`) mangles audio at AAC splice
  boundaries and sounds like hard cuts. **Re-encode when concatenating.**
- **Chained clips drift.** `chain_clips.py` gets past the single-pass frame ceiling by seeding
  each chunk from the last frame of the previous one, but there is real compounding
  framing/zoom-in drift within each chunk. Prefer a longer single pass if VRAM now allows —
  that removes the problem rather than managing it.
- **Dialogue pace: ~2.2–2.5 words/sec.** Roughly 5–6 words per 56-frame clip, **not** the ~11
  originally assumed. Long lines must be split at natural clause breaks across several clips
  or they sound rushed. Scene 1's original 39-clip estimate undercounts.
- **Forcing the 32B text encoder onto the GPU (`--stream-layers`) is 13× slower** and OOMs
  anyway. Leave `--auto-fit` to place it.

---

## 5. RunPod rules that will bite you

- **`nproc` and `free` lie.** They report the *host*. This pod shows 96 CPUs and 503GB RAM;
  the real cgroup quota is **7.65 CPUs** and 50GB. `make -j$(nproc)` drove load average to 37.
  Read `/sys/fs/cgroup/cpu.max` and `/sys/fs/cgroup/memory.max` instead.
- **`df` cannot see your volume quota.** `df -h /workspace` reports the shared cluster
  (hundreds of TB) and says the same thing at 1GB used or 190GB. **Use `du -sh /workspace`.**
- **Network volumes are datacenter-locked forever**, and bill 24/7 whether a pod is attached
  or not. If the account balance reaches $0 the volume can eventually be **deleted with no
  recovery**.
- **Small files on the network volume can be catastrophically slow** — measured 300 small
  files at 37ms on the container disk vs 147,884ms on a `us-ks-2` volume (though only 3,957ms
  on `ca-mtl-1`; it varies wildly by datacenter). Build environments on the container disk,
  keep only large model files on the volume.
- **A stopped pod does not reserve its GPU.** If the datacenter is out of that card when you
  restart, you wait.
- **Pick GPUs for VRAM, and avoid MIG slices.** `PRO 6000 MIG 24GB` at $0.59/hr is one
  *compute slice* of a card — worse and dearer than a whole **A40 48GB at $0.44/hr**.
  Current pod is an A40.

### 💸 Stop the pod when the batch finishes

Nothing will remind you. A forgotten pod overnight costs more than all of Scene 1 — the whole
scene is only about 3 GPU-hours at ~3.4 min/clip. Budget for re-rolls and idle mistakes, not
throughput.

---

## 6. Rebuilding from scratch

If the pod is gone, `runpod/setup_pod_minimax.sh` rebuilds everything. It is **idempotent** —
weights already on the volume are skipped, so a fresh pod only repeats the (fast) build.

```bash
scp -P <PORT> runpod/setup_pod_minimax.sh root@<IP>:/workspace/
ssh root@<IP> -p <PORT> \
  'setsid nohup bash /workspace/setup_pod_minimax.sh > /workspace/setup.log 2>&1 < /dev/null & disown'
```

`sd-cli` is **compiled**, not downloaded: stable-diffusion.cpp ships a prebuilt *Windows*
CUDA binary but no Linux CUDA build. `nvcc` is present at `/usr/local/cuda/bin`, just not on
`PATH`. Set `CUDA_ARCH` for the card — 86 for A40/A6000/3090, 89 for 4090, 120 for Blackwell.

The image's Python is PEP 668 externally-managed, so pip needs a venv; the script builds one
on the container disk with `--system-site-packages` to inherit the image's working torch.

---

## 7. Where to look next

| File | For |
| :--- | :--- |
| `SCENE1_MINIMAX_TRACKER.md` | shot-by-shot status and QA rules — **the working doc** |
| `RUNPOD_CLOUD_RENDERING.md` | why cloud, GPU choice, costs, full gotcha list |
| `minimax-h3-pipeline/README.md` | model detail, settings rationale, hardware constraints |
| `HANDOVER.md` §9 | how the project got here, and what was already rejected |
| `featurette_storyboard_image_prompts.md` | all 64 keyframe prompts |
| `runpod/README.md` | operational reference for the pod |

**Open question as of this handover**: whether MiniMax-H3 at 1280×720 fixes the wide-shot
blob face. Nothing has been rendered on the pod yet. That test, and an A40-vs-4080 speed
baseline, are the immediate next steps.
