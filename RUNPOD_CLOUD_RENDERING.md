# ☁️ RunPod — renting a GPU for the video pipelines

> **Written**: 2026-08-26, from the laptop (Intel UHD, no NVIDIA GPU at all).
> **Status**: pod deployed, `setup_pod.sh` running, weights downloading. Nothing rendered yet.
> **Operational detail**: `runpod/README.md`. This doc is the *why* and the session record.
> **Read alongside**: `HANDOVER.md` §6 and §9, `minimax-h3-pipeline/README.md`, `wan22-pipeline/README.md`.

---

## 1. Why this exists

`HANDOVER.md` records three separate rejections that were all, underneath, **one
rejection — 16GB of VRAM**:

| What was rejected | Stated reason | Actual reason |
| :--- | :--- | :--- |
| Q5_0 / Q6_K / Q8_0 MiniMax quants (13.9–21.4GB) | "won't fit" | 16GB card |
| WAN 2.2 14B MoE, FLUX.2 klein | "unusably slow" | offload to RAM once weights exceed VRAM |
| F01 wide-shot faces = featureless blob at 864×480 | "pixel-count problem" | can't afford the resolution in VRAM |

On a 48GB card none of those are constraints. **That** is the reason to rent, not
convenience. Cloud *video APIs* (Veo/Flow, Runway, Kling) were considered and
rejected separately — they carry the same likeness/content filters that already
block photoreal Jan (see `HANDOVER.md` §2 and §6). Renting a bare GPU and running
our own open weights sidesteps filters entirely.

Second benefit, not the main one: the laptop has no NVIDIA GPU. A rented pod means
work is no longer pinned to being physically at the main PC.

---

## 2. GPU choice — pick for VRAM, not for the badge

RunPod on-demand pricing, 2026-08-26:

| GPU | VRAM | RAM | $/hr | verdict |
| :--- | ---: | ---: | ---: | :--- |
| A40 | 48GB | 50GB | 0.44 | cheapest 48GB |
| **RTX A6000** | **48GB** | **50GB** | **0.53** | **chosen** |
| RTX 4090 | 24GB | 31GB | 0.74 | **trap — see below** |
| RTX 5090 | 32GB | 60GB | 0.99 | |
| L40S | 48GB | 125GB | 0.99 | Ada, fast + roomy |
| H100 NVL | 94GB | 180GB | 3.19 | |
| A100 PCIe | 80GB | 117GB | 1.39 | overkill for 5B/GGUF |

**The RTX 4090 costs more than the A6000 and gives half the VRAM.** It is the
obvious-looking pick and the wrong one. 24GB does not hold a 21.4GB Q8_0 plus VAE,
latents and activations — which lands you straight back in the offload failure mode
that got local WAN 2.2 rejected in the first place. Its 31GB of system RAM is thin
too, given the 32B text encoder can run on CPU.

The A6000/A40 are Ampere and genuinely slower per step than a 4090 (no fp8 fast
path). **It does not matter.** Avoiding offload is worth far more than the
architecture gap. If speed later proves binding and everything fits in 48GB, L40S
is the Ada upgrade at $0.99/hr.

---

## 3. Cost

**Chosen config**: 1× RTX A6000, 30GB container disk, 200GB network volume =
**$0.55/hr** while running.

At 4 hrs/night × 30 nights = 120 GPU-hours, using the cached rate in
`../.usd_gbp_rate.json` (0.74075, dated 2026-08-11 — **refresh it**):

| Line | USD |
| :--- | ---: |
| GPU, 120 hrs × $0.53 | 63.60 |
| Container disk, 120 hrs × $0.004 | 0.48 |
| Network volume, 200GB × 730 hrs × $0.019 | 13.87 |
| **Total / month** | **$77.95 ≈ £57.74** |

≈ **£1.92 per night** — £1.58 GPU, £0.34 storage that ticks over whether used or not.

### The important caveat: 120 hours is far more than the work needs

At the measured **~3.4 min/clip** (MiniMax-H3 + EasyCache), 120 hours is ~2,100
clips. Scene 1 is on the order of 50. **The whole scene is roughly 3 GPU-hours.**

Budget for re-rolls, failed experiments and forgotten pods — *not* for throughput.
The realistic monthly spend is far below £57 unless pods get left running.

### Money traps

- **The volume bills 24/7**, pod running or not. $13.87/month is the floor.
- **If the account balance hits $0**, pods stop but the volume keeps accruing
  charges and can eventually be **deleted with no recovery**. Do not park 200GB of
  weights on a dry account.
- **A pod left running overnight costs more than all of Scene 1.** Stop it when the
  batch finishes. Nothing will remind you.

---

## 4. The pod as provisioned

| | |
| :--- | :--- |
| Name | `managerial_blush_cat` |
| Pod ID | `juq9cu71lijpjq` |
| Template | `runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404` |
| GPU | NVIDIA RTX A6000, 49140 MiB, driver 570.211.01 |
| **Datacenter** | **US-KS-2 (Kansas)** |
| Container disk | 30GB at `/` |
| Network volume | 200GB at `/workspace` (MooseFS, `mfs#us-ks-2.runpod.net:9421`) |
| SSH (direct TCP) | `root@64.247.206.204 -p 43231` — supports SCP/SFTP |
| SSH (proxy) | `ssh.runpod.io` — **no SCP/SFTP** |
| HTTP exposed | **8888 only** (Jupyter). 8188 is *not* exposed. |

⚠️ **The IP, port and pod ID are ephemeral** — they change on every redeploy. The
**datacenter does not**: the network volume is welded to **US-KS-2** permanently.
Every future pod must be deployed there. If A6000 stock in Kansas thins out, that
is the hard ceiling, and the only escape is building a second volume elsewhere and
re-downloading ~99GB.

---

## 5. Connecting

### SSH keys are injected at pod CREATION

Generate or register a key *after* deploying and the running pod has never seen it:
`Permission denied (publickey)`. Hit this on the first attempt.

Two fixes — Account Settings → SSH Public Keys then restart the pod, or (faster, no
restart) enable the pod's **web terminal** and append it by hand:

```bash
mkdir -p ~/.ssh && echo '<your ssh-ed25519 public key>' >> ~/.ssh/authorized_keys \
  && chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys
```

Register it in Account Settings regardless, or every future pod repeats the dance.

### Use an SSH tunnel, not the HTTPS proxy

RunPod only publishes HTTP ports declared at **creation** time, and the default
template gives 8888, not 8188. Rather than recreating the pod, tunnel it — which is
the better transport anyway:

```bash
ssh -N -L 8188:localhost:8188 -i ~/.ssh/id_ed25519 -p 43231 root@64.247.206.204
```

Leave it running in its own terminal, then `COMFY_SERVER=http://127.0.0.1:8188`.

**Why the tunnel wins:** the proxy at `https://<POD_ID>-8188.proxy.runpod.net` sits
behind Cloudflare with a hard **100-second cap** — any request past it dies with a
`524`. Our clips take 3–10 minutes, and large mp4 downloads can exceed 100s on their
own. The tunnel has no cap and carries SCP. Use the **direct TCP** endpoint, not
`ssh.runpod.io`, which has no SCP support.

`comfy.py` still supports the proxy path via `COMFY_POD` if 8188 is ever exposed
properly — it submits and polls precisely so no single request goes long.

---

## 6. Setup — what runs on the pod

`runpod/setup_pod.sh`, uploaded by scp and run detached, logging to
`/workspace/setup.log`. **Idempotent** — safe to re-run on a fresh pod; it skips
whatever the volume already holds. Everything lands on `/workspace` so it survives
the pod's death.

Order is deliberate: **ComfyUI and all custom nodes install first**, so a broken
dependency chain fails in the first few minutes rather than after 99GB.

It carries every hard-won fix from `wan22-pipeline/comfyui-tools/README.md` —
`moviepy==1.0.3`, `setuptools==79.0.1`, `filelock` upgrade, `chumpy
--no-build-isolation`, the mmcv source-build fallback, and the ComfyUI-GGUF
`IMG_ARCH_LIST` patch to accept `"ltx2"`. **Do not "tidy up" those pins.**

### Weight inventory (~99GB, downloads once per volume, ever)

| File | GB | Source |
| :--- | ---: | :--- |
| `minimax_h3_ref2va_pruned-Q4_K.gguf` + `fl2va` + VAEs + encoder | ~50 | `unsloth/MiniMax-H3-GGUF` |
| `minimax_h3_ref2va_turbo_Q4_K_M.gguf` | 11.4 | `ChrisColeTech/minimax-h3-turbo-GGUF` (under `split/`, **not** repo root) |
| `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors` | 15.7 | `Comfy-Org/MiniMax-H3` |
| `wan2.2_ti2v_5B_fp16.safetensors` + VAE + `umt5-xxl-encoder-Q8_0.gguf` | 17.4 | Comfy-Org / `city96` |
| `face_yolov8m.pt`, venv, ComfyUI | ~5 | |

**This is why the volume is 200GB, not the 100GB the console suggests.** Volumes can
be grown later but **never shrunk**.

**MuseTalk weights are not fetched by the script** — they go in
`custom_nodes/ComfyUI-MuseTalk_FSH/models/<subfolder>/` exactly as that node's README
lays out.

### Then

```bash
bash /workspace/start_comfy.sh          # on the pod
python runpod/comfy.py ping             # from the laptop, through the tunnel
python runpod/comfy.py run prompt.json -o outputs/
```

`prompt.json` is API-format — build it from a saved workflow with
`wan22-pipeline/comfyui-tools/graph_to_prompt.py`, whose hardcoded
`SERVER = "http://127.0.0.1:8188"` should be made to read `COMFY_SERVER` (patch in
`runpod/README.md`).

---

## 7. Gotchas found the hard way

- **`nproc` and `free` lie inside a pod.** They report the *host*: this pod shows 64
  vCPU and 503GB RAM, while the real cgroup limit is **~58GB** and the plan sells 8
  vCPU. **Never set worker counts or batch sizes from `nproc` on RunPod** — you will
  oversubscribe and thrash. Read `/sys/fs/cgroup/memory.max` instead.
- **`/workspace` is network storage (MooseFS), not local disk.** Thousands of small
  files — venv creation, pip installs, git clones — are noticeably slow. Large
  sequential weight downloads are fine. Don't mistake a slow pip step for a hang.
- **SSH keys are injected at pod creation only** (§5).
- **HTTP ports are fixed at pod creation only** (§5).
- **The Cloudflare 100-second cap** on the HTTPS proxy (§5).
- **The volume is datacenter-locked forever** (§4).
- **Balance → $0 can destroy the volume** (§3).
- Container disk (`/`) is **erased when the pod stops**. Only `/workspace` persists.

### Unverified — check early, cheaply

The text encoder is `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors`. **NVFP4 has no
native hardware support on Ampere (A6000).** It has none on Ada either, and it
worked on the 4080, so the same dequantise-on-load path should apply — but **load it
before queuing a long batch**, not after.

---

## 8. Managing pods

RunPod ships a first-party MCP server, which is the better route than hand-rolled
lifecycle scripts:

```
/plugin marketplace add runpod/runpod-plugins-official
/plugin install runpod@runpod
```

**Choose "Hosted" mode when the installer asks.** Local mode writes the API key in
plaintext into `~/.claude.json`; hosted mode uses OAuth and puts nothing on disk —
which is the whole point of the `fal_key.py` / `gemini_key.py` Credential Manager
convention. `runpod_key.py` (in `C:\kontitemp\AI\`, outside the repo, same pattern,
validates on paste via a free `GET /v2/pods`) exists only for scripting outside MCP.

MCP does **not** drive ComfyUI. That is `runpod/comfy.py`, and it's the half that
matters.

---

## 9. Files added this session

| File | In repo? | What |
| :--- | :--- | :--- |
| `RUNPOD_CLOUD_RENDERING.md` | ✅ | this doc |
| `runpod/README.md` | ✅ | operational reference |
| `runpod/setup_pod.sh` | ✅ | idempotent pod bootstrap |
| `runpod/comfy.py` | ✅ | submit / poll / fetch against ComfyUI |
| `C:\kontitemp\AI\runpod_key.py` | ❌ **not in git** | API key in Credential Manager — recreate per machine, like `fal_key.py` |

No `rp.py` — the RunPod MCP server covers pod lifecycle better.

---

## 10. Where this was left

1. Pod deployed, SSH working, `setup_pod.sh` running — **weights still downloading**.
2. **Nothing has been rendered yet.** The pipelines are unproven on this hardware.
3. First real test should be cheap: load the NVFP4 text encoder (§7), then a single
   Wan 2.2 silent wide clip end-to-end — the fastest honest check that ComfyUI, the
   tunnel and `comfy.py` all work together.
4. Only then attempt the thing that justified renting at all: **F01's wide shot at a
   resolution 16GB couldn't afford**, to see whether Jan's face stops being a blob.
   If it does, re-examine every "too slow / won't fit" rejection in `HANDOVER.md` §6
   and §9 — they were all measured against a constraint that no longer applies.
5. Scene 1 clip-count and pacing still need re-planning against the corrected
   dialogue rate (~2.2–2.5 words/sec), per `SCENE1_MINIMAX_TRACKER.md` QA Rule 2.
   That work is unaffected by the hardware change.
