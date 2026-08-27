# 🤖 Agent handover — rendering Circle the Square on a RunPod GPU

> **Audience**: any coding agent (Antigravity/`agy`, Gemini, Codex, another Claude session)
> picking this up cold, from any machine.
> **Last updated**: 2026-08-27, after a full day of testing on rented GPUs.
> **You do not need a local GPU.** The laptop this was set up from has Intel UHD graphics
> and no CUDA at all. Everything runs on a rented pod; your machine only sends commands.

Read this whole file before running anything. §5 and §6 are results paid for in GPU time —
re-running those experiments wastes money and tells you nothing new.

---

## 1. What the job is

*Circle the Square* is a British mockumentary comedy. 64 storyboard keyframes across 3
scenes need turning into video clips with dialogue. Scene 1 is 28 keyframes (F01–F26b) and
is the active work; `SCENE1_MINIMAX_TRACKER.md` is the shot-by-shot source of truth.

**The working model is MiniMax-H3.** It generates video *and* native synced audio in one
pass, from reference images plus a text prompt, via `sd-cli` (stable-diffusion.cpp).

### 🚫 Hard rule: never propose a silent video model

Any route needing a separate TTS and lip-sync stage is **out of scope**, by explicit user
instruction (2026-08-27). The user does not work with that tooling and will not maintain a
pipeline that depends on it.

This rules out **Wan 2.2** (sharper, better at wides, video-only) and the
Wan → Qwen3-TTS → MuseTalk chain in `wan22-pipeline/`, **even though that chain was
validated end-to-end**. It also rules out every RunPod template in the Hub video category —
WAN, HunyuanVideo, LTX 0.9.5, Stable Video Diffusion, FramePack are all silent.

Researched 2026-08-27: **LTX-2.x is the only other open-weight model doing single-pass
synchronised audio.** Seedance, Sora 2, Veo 3 and Kling are hosted-only, and hosted services
also hit the likeness filters that already blocked Google Flow for photoreal Jan
(`HANDOVER.md` §2). The field is MiniMax-H3 or LTX-2. There is no third option to find.

Acceptable levers when picture quality is short, in order:
1. Render at higher resolution (`--width`/`--height`) — **proven to work**, see §5.
2. Better quantisation / more sampling steps — **never yet tried**, see §7.
3. LTX-2.3, already downloaded — see §6.
4. **Change the shot.** Cut to a medium for the dialogue and hold the wide either side.
   A legitimate first-class answer, not a consolation. Suggest it.

---

## 2. Connecting

Pods run **Ubuntu 24.04**. The user's main PC is **Windows**. Nothing binary transfers —
no `.exe` files, no Windows paths, and `.sh` files must stay LF (`.gitattributes` pins this;
CRLF gives `bad interpreter: /bin/bash^M`).

### 2.1 Current pod

| | |
| :--- | :--- |
| Pod | `doubtful_harlequin_felidae` — `2fgh1e1dvyrwah` |
| GPU | **NVIDIA A100-SXM4-80GB** (sm_80), $1.59/hr |
| Data center | **US-KS-2** |
| Volume | `ksi7rp0d54`, 200GB, US-KS-2 |
| SSH | `ssh root@216.81.245.143 -p 15336 -i ~/.ssh/id_ed25519` |

⚠️ **IP and port change on every pod creation.** `runpod/pod.env` holds the last known
values; verify before trusting them.

### 2.2 The RunPod MCP server is connected — use it

Installed 2026-08-27 via `/plugin marketplace add runpod/runpod-plugins-official` then
`/plugin install runpod@runpod`, hosted OAuth mode (no API key on disk). If your session
doesn't have it, install it the same way and authenticate.

It gives `list-pods`, `get-pod`, `list-network-volumes`, `get-billing`, `get-capacity`,
`stop-pod`, `create-pod` and more. **Use it instead of asking the user to paste console
screenshots.** Two mistakes on 2026-08-27 came from reasoning about stale pasted state:
telling the user to terminate a pod they had already terminated, and asserting two network
volumes existed when there was one.

### 2.3 SSH keys are injected at pod CREATION only

Register a key *after* deploying and the running pod has never seen it →
`Permission denied (publickey)`. Fix: enable the pod's **web terminal** and append it, or
restart the pod. Register in Account Settings so future pods get it automatically.

```bash
mkdir -p ~/.ssh && echo '<public key>' >> ~/.ssh/authorized_keys \
  && chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys
```

### 2.4 Layout

| Path | What | Survives pod stop? |
| :--- | :--- | :--- |
| `/workspace/minimax/` | MiniMax weights (33GB), refs, output, `sd-cli`, `gen_clip.py` | ✅ volume |
| `/workspace/ltx2/` | LTX-2.3 weights (~34GB with Gemma) | ✅ volume |
| `/opt/sd.cpp`, `/opt/venv` | build tree | ❌ **erased on stop** |

Only an explicit Stop or Terminate wipes the container disk. Closing a laptop or dropping
SSH does nothing to the pod — **including nothing to the billing.**

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

`setsid nohup … & disown`. A render started in a plain SSH session dies when that session
drops, and the pod keeps billing while the work is lost. Watch with `tail -f`.

### ⚠️ Always download results to the user

Every finished clip must be `scp`-ed to **`C:\kontitemp\AI\cloud-clips\`** and the reply must
quote the full path. The user reviews picture and audio himself; a file on the pod is
useless to him. Pull frame crops too when making any claim about quality.

Do **not** offer `\\HOST\c$\...` UNC paths — that is the admin share and fails without
elevation.

### References

`--refs` are **filenames inside `refs/`**, not paths. MiniMax-H3 uses natural language, so
the prompt must name them: *"Reference 1 shows Jan. Reference 2 shows the office."* Sources
are in the repo at `character-refs/_photoreal-archive/` and `location-refs/`.

Use `jan_office_location_sheet_fixed.png`, **not** the non-`_fixed` version.

### Flags

| Flag | Default | Notes |
| :--- | :--- | :--- |
| `--frames` | 56 | 2.33s @ 24fps. **Do not exceed ~56 at 720p — see §5** |
| `--width`/`--height` | 864/480 | 1280×736 for wides — see §5 |
| `--quant` | `Q4_K` | `Q8_0` (21.4GB) now affordable and **never tested** |
| `--vae-tiling` | off | ~20% slower; VAE decode is a memory *spike* |
| `--turbo` | off | **audio is broken — silent shots only** |

---

## 4. Known-broken. Do not rediscover.

- **`--turbo` audio is garbage.** Whisper transcribes it as empty or nonsense while the
  video looks fine. 4-step audio distillation failure. Silent shots only.
- **Naive concat corrupts audio.** Stream-copy mangles AAC splice boundaries. Re-encode.
- **Chained clips drift** (`chain_clips.py`) — compounding framing/zoom drift per chunk.
- **Dialogue pace is ~2.2–2.5 words/sec** — ~5–6 words per 56-frame clip, not ~11.
- **`--stream-layers` (32B encoder on GPU) is 13× slower** and OOMs. Leave placement alone.
- **H3-FaceRefine does not sharpen wide-shot faces** even when working correctly.

---

## 5. ✅ RESULT: 720p fixes the wide-shot blob. 124 frames breaks it.

Tested 2026-08-27 on an A40 48GB. Clips are in `C:\kontitemp\AI\cloud-clips\`.

| Config | Result | Time |
| :--- | :--- | ---: |
| 864×480, 56f, close-up | ✅ baseline, good | 179 s |
| **1280×736, 56f, wide** | ✅ **face resolves — the blob is fixed** | 408 s |
| 1280×736, 124f, wide | ❌ **degrades progressively** | 964 s |

**The wide-shot face problem is solved by resolution.** `HANDOVER.md` called it "a
pixel-count problem, not a quantization one" and that was correct. At 1280×736 Jan's face
has eyes, glasses and a readable expression at native pixel crop.

**Doubling the length does not work, and it is NOT a VRAM limit.** 124 frames fit fine
(41.7/46GB) and rendered — but the picture decays *through* the clip: frame 8 intact,
frame 60 smeared, frame 115 badly distorted with colour fringing and mangled hands.

⚠️ This corrects an assumption in `minimax-h3-pipeline/README.md`, which attributes the
96-frame failure to VRAM thrashing. **There is a separate quality ceiling that more VRAM
does not lift.** Chaining short segments is therefore *better* than one long pass, not
worse — drift between chunks is milder than decay within one.

### ❌ Still unsolved: the London skyline

The Shard reappears through the office windows in wides, **despite** using the `_fixed`
office plate and **despite** an explicit negative ("LOW-RISE CAMBRIDGE… NO London skyline,
NO skyscrapers, NO The Shard"). Negative prompting is not the lever. A wide exposes far
more glass than the close-ups the `_fixed` plate was validated against. Likely fixes: a
reference whose window content is unambiguous, an edit pass, or blocking shots so the glass
isn't behind the actors.

---

## 6. LTX-2.3 — downloaded, unproven

`runpod/get_ltx2.sh` fetches it. **It runs on the same `sd-cli`** — no ComfyUI, no new build.

```
ltx-2.3-22b-dev-Q8_0.gguf                          22.8 GB  --diffusion-model
gemma-3-12b-it-qat-UD-Q4_K_XL.gguf                  7.4 GB  --llm
ltx-2.3-22b-dev_embeddings_connectors.safetensors    2.3 GB  --embeddings-connectors
ltx-2.3-22b-dev_video_vae.safetensors                1.5 GB  --vae
ltx-2.3-22b-dev_audio_vae.safetensors                0.4 GB  --audio-vae
```

**LTX needs a separate LLM text encoder — Gemma-3-12B.** The GGUF repo does not ship one;
`embeddings_connectors` is a trained adapter, not the encoder. Architecturally this is
better than MiniMax: LTX freezes a stock swappable LLM (12B) where MiniMax bakes in a 32B.

Constraints: **width/height divisible by 32, frame count divisible by 8 plus 1** (so 121,
not 124). Use `dev`, not `distilled` — distilled is 8-step and MiniMax's equivalent turbo
build had broken audio.

### Three OOM failures on 48GB — all at VAE decode

Sampling always succeeded; the **video VAE** then asked for 30.4GB, then 14.3GB with
temporal tiling, then 24.3GB per tile. Each failure wasted ~7 minutes of good sampling
because sd-cli keeps no checkpoint between sampling and decode.

⚠️ **`--auto-fit` silently overrides `--backend` and `--params-backend`** — only a WARN:
`--auto-fit is enabled; ignoring --backend / --params-backend`. Two of those three attempts
were passing a flag that was being discarded. Auto-fit reasons about load-time fit, not
peak-decode fit, so on a roomy card it parks the text encoder on GPU where it holds 10GB
for the whole render despite finishing in seconds.

Explicit placement (drop `--auto-fit`):
`--backend "diffusion=CUDA0,te=CPU,vae=CUDA0"` — verified to put Gemma in RAM.

**Untested on 80GB.** That is the open question; the 24GB tile should now fit.

---

## 7. 🔴 The most important untried experiment

**Every setting used so far is a speed compromise inherited from a 16GB card, and none has
been revisited on rented hardware:**

- `Q4_K` denoiser — because `Q8_0` (21.4GB) didn't fit 16GB.
- 20 steps **with EasyCache skipping roughly half of them**.

The user judged output quality "not good enough" — but has only ever seen **preview
settings**. Before renting anything bigger or switching models, run:

```
--quant Q8_0, EasyCache off, ~30 steps, 1280×736, on the F01 wide
```

directly comparable to `F01_720p.mp4` which he has already watched. This is the single
cheapest experiment with the highest chance of changing the answer.

---

## 8. RunPod rules that will bite you

- **`nproc` and `free` lie** — they report the *host*. A pod showed 96 CPUs / 503GB RAM
  against a real quota of **7.65 CPUs** / 50GB. `make -j$(nproc)` drove load average to 37.
  Read `/sys/fs/cgroup/cpu.max` and `memory.max`.
- **`df` cannot see the volume quota** — it reports the shared cluster (hundreds of TB).
  Use `du -sh /workspace`.
- **`sd-cli` must be rebuilt per GPU architecture** — sm_80 (A100), sm_86 (A40/A6000/3090),
  sm_89 (4090/L40S), sm_120 (Blackwell). `setup_pod_minimax.sh` handles it; pass
  `CUDA_ARCH=`. It skips weights already on the volume, so a rebuild is ~15 min.
- **Network volumes are datacenter-locked forever** and bill 24/7. At measured **~100 MB/s**
  download, re-fetching all 60GB takes ~15 min ≈ $0.40 on an A100 — so a $14/month volume
  only pays off above ~35 pod-starts a month. **Going volume-free with a large container
  disk buys total freedom of GPU and datacenter**, which is worth more than the $14.
- **Avoid MIG slices.** `PRO 6000 MIG 24GB` at $0.59/hr is one compute *slice* — worse and
  dearer than a whole **A40 48GB at $0.44/hr**.
- **Pick for VRAM, not speed.** Every failure this project has hit was `cudaMalloc failed`,
  never "too slow". An RTX 5090 (32GB, $0.99) is a downgrade from an A40 (48GB, $0.44).
- **Small files on a network volume can be catastrophically slow** — 300 files took 37ms on
  container disk vs 147,884ms on a `us-ks-2` volume (but only 3,957ms on `ca-mtl-1`; it
  varies wildly). Build environments on the container disk; keep only large weights on the
  volume.
- **Set `HF_TOKEN`** — the downloads warn about rate limits without one.

### 💸 Stop the pod when the batch finishes

Nothing will remind you. Total spend 26–27 Aug was **$1.46** ($1.20 GPU, $0.19 storage) —
cheap because pods were stopped. Scene 1 is only ~3 GPU-hours at ~3.4 min/clip; budget for
re-rolls and idle mistakes, not throughput.

---

## 9. Rebuilding from scratch

```bash
scp -P <PORT> runpod/setup_pod_minimax.sh root@<IP>:/workspace/
ssh root@<IP> -p <PORT> \
  'setsid nohup bash -c "CUDA_ARCH=80 bash /workspace/setup_pod_minimax.sh" \
     > /workspace/setup.log 2>&1 < /dev/null & disown'
```

Idempotent — weights on the volume are skipped. `sd-cli` is **compiled**, not downloaded:
stable-diffusion.cpp ships a Windows CUDA binary but no Linux CUDA build. `nvcc` is at
`/usr/local/cuda/bin`, just not on `PATH`. The image's Python is PEP 668
externally-managed, so the script builds a venv on the container disk with
`--system-site-packages` to inherit the image's torch.

Weights download **before** the build, deliberately — a compiler problem must not strand
60GB.

---

## 10. Where this was left

Pod is an A100 80GB, rebuilding after a GPU switch. Immediate queue:

1. **MiniMax at real quality settings** (§7) — the experiment that may make the model
   question moot.
2. **LTX-2.3 at 1280×736 on 80GB** (§6) — the VAE tile that OOM'd on 48GB should now fit.
3. Fix the **London skyline** in wides (§5).
4. Re-plan Scene 1's clip count against the corrected dialogue pace
   (`SCENE1_MINIMAX_TRACKER.md` QA Rule 2) — unaffected by hardware.

**Not yet recorded anywhere: the exact prompt strings used per clip.** The tracker logs
outcomes, not prompts, so `F01_v3`/`F02_v3` cannot be reproduced exactly. Log prompts per
clip going forward.

| File | For |
| :--- | :--- |
| `SCENE1_MINIMAX_TRACKER.md` | shot-by-shot status and QA rules — **the working doc** |
| `RUNPOD_CLOUD_RENDERING.md` | why cloud, GPU choice, costs, full gotcha list |
| `minimax-h3-pipeline/README.md` | model detail and settings rationale (see §5 caveat) |
| `HANDOVER.md` §9 | how the project got here, and what was already rejected |
| `runpod/README.md` | operational reference |
