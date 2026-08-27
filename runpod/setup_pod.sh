#!/usr/bin/env bash
# Bootstrap a RunPod pod for Circle the Square rendering.
#
#   scp this up, then on the pod:  bash /workspace/setup_pod.sh
#
# ---------------------------------------------------------------------------
# THE LAYOUT, AND WHY IT IS NOT ALL ON THE VOLUME
#
# Measured on this pod (RTX A6000, US-KS-2), writing 300 small files:
#
#     container disk (/)     :      37 ms
#     network volume (/wksp) : 147,884 ms      <-- ~4000x slower
#
# ...while a sequential 1GB write is 1.8 GB/s local vs 542 MB/s on the volume,
# which is perfectly fine. MooseFS is good at big files and catastrophic at
# small ones. A `python3 -m venv` (~700 files) took over 13 minutes on the
# volume before being killed; ComfyUI's full dependency tree is tens of
# thousands of files and would have taken HOURS.
#
# So:
#   CODE + PYTHON DEPS -> container disk. Fast, and rebuilt per pod (~minutes).
#   MODEL WEIGHTS      -> /workspace. Big sequential files, downloaded once ever.
#
# The venv lives on the container disk too. It cannot be skipped entirely: the
# image's python is PEP 668 "externally managed" and pip refuses to touch it. But
# it is created with --system-site-packages, so it inherits the image's working
# torch 2.8.0+cu128 instead of pulling 2.5GB of CUDA wheels.
# ---------------------------------------------------------------------------
#
# Idempotent. Re-run it on every fresh pod: the weights are skipped if the
# volume already has them, and only the (fast) code install repeats.
#
# Do not "tidy up" the odd-looking pins below; each one is a documented fix
# from wan22-pipeline/comfyui-tools/README.md.

set -euo pipefail

WS=/workspace
COMFY=/opt/ComfyUI          # container disk - wiped on pod stop, rebuilt cheaply
VENV=/opt/venv              # ditto. NOT on the volume - that took 13+ min there
MODELS=$WS/models           # network volume - the expensive, persistent part
OUTPUTS=$WS/outputs
PY=$VENV/bin/python
PIP="$VENV/bin/pip --quiet --disable-pip-version-check"

log() { echo -e "\n=== $* ==="; }
have() { [ -e "$1" ]; }

# ---------------------------------------------------------------- sanity
log "environment"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
python3 -c "import torch; print('torch', torch.__version__, 'cuda', torch.cuda.is_available())"
echo "cgroup RAM limit: $(( $(cat /sys/fs/cgroup/memory.max 2>/dev/null || echo 0) / 1024**3 )) GB"
echo "(ignore nproc/free - they report the HOST, not your slice)"

if ! mountpoint -q $WS 2>/dev/null; then
  echo "!! WARNING: $WS is not a mount point - weights would go to the container"
  echo "!! disk and be erased when the pod stops. Attach the network volume first."
  exit 1
fi
mkdir -p "$MODELS" "$OUTPUTS"

# ---------------------------------------------------------------- python
# The image's python is PEP 668 "externally managed", so pip refuses to install
# into it. A venv on the CONTAINER DISK is the fix - it takes seconds there, and
# --system-site-packages inherits the image's torch 2.8.0+cu128 rather than
# re-downloading 2.5GB of CUDA wheels.
log "venv -> $VENV (container disk, inherits system torch)"
have $VENV || python3 -m venv --system-site-packages $VENV
$PIP install --upgrade pip wheel
$PY -c "import torch; print('venv sees torch', torch.__version__, 'cuda', torch.cuda.is_available())"

# ---------------------------------------------------------------- comfyui
log "ComfyUI -> $COMFY (container disk)"
if ! have $COMFY; then
  git clone --depth 1 https://github.com/comfyanonymous/ComfyUI.git $COMFY
fi

# Point ComfyUI's heavy directories at the volume BEFORE installing, so nothing
# large ever lands on the container disk.
for d in models output; do
  target=$([ "$d" = models ] && echo "$MODELS" || echo "$OUTPUTS")
  if [ ! -L "$COMFY/$d" ]; then
    rm -rf "$COMFY/$d"
    ln -s "$target" "$COMFY/$d"
  fi
done
echo "models -> $(readlink -f $COMFY/models)"
echo "output -> $(readlink -f $COMFY/output)"

$PIP install -r $COMFY/requirements.txt   # torch already satisfied via system-site-packages

log "custom nodes"
cd $COMFY/custom_nodes
clone_node() {  # clone_node <url> <dirname>
  have "$2" || git clone --depth 1 "$1" "$2"
  [ -f "$2/requirements.txt" ] && $PIP install -r "$2/requirements.txt" || true
}
clone_node https://github.com/city96/ComfyUI-GGUF.git                ComfyUI-GGUF
clone_node https://github.com/Carasibana/ComfyUI-H3-FaceRefine.git   ComfyUI-H3-FaceRefine
clone_node https://github.com/AIFSH/ComfyUI-MuseTalk_FSH.git         ComfyUI-MuseTalk_FSH

# ---------------------------------------------------------------- weights
log "weights -> $MODELS (~99GB, downloads once per volume, ever)"
HF_CLI=$(command -v $VENV/bin/hf || command -v $VENV/bin/huggingface-cli || command -v hf || command -v huggingface-cli)
[ -n "$HF_CLI" ] || { echo "!! no huggingface CLI on PATH"; exit 1; }
export HF_HUB_ENABLE_HF_TRANSFER=0

hf() {  # hf <repo> <remote_path> <local_dir>
  local target="$3/$(basename "$2")"
  if have "$target"; then echo "  have $(basename "$2")"; return; fi
  mkdir -p "$3"
  echo "  fetching $(basename "$2")"
  "$HF_CLI" download "$1" "$2" --local-dir "$3"
  [ -f "$target" ] || find "$3" -name "$(basename "$2")" -exec mv {} "$3/" \; 2>/dev/null || true
}

M=$MODELS
# MiniMax-H3 - close-up dialogue shots (this is the one with working audio)
hf unsloth/MiniMax-H3-GGUF minimax_h3_ref2va_pruned-Q4_K.gguf        "$M/diffusion_models"
hf unsloth/MiniMax-H3-GGUF minimax_h3_fl2va_pruned-Q4_K.gguf         "$M/diffusion_models"
hf unsloth/MiniMax-H3-GGUF vae/minimax_h3_video_vae_fp16.safetensors "$M/vae"
hf unsloth/MiniMax-H3-GGUF vae/minimax_h3_audio_vae_fp32.safetensors "$M/vae"
# Turbo denoiser: the real path is under split/, not the repo root.
# AUDIO IS BROKEN on this one - silent shots only, --steps 4 --guidance 1.0.
hf ChrisColeTech/minimax-h3-turbo-GGUF \
   split/diffusion_models/minimax_h3_ref2va_turbo_Q4_K_M.gguf        "$M/diffusion_models"
# Text encoder: the 32B GGUF does NOT load via CLIPLoaderGGUF (no
# general.architecture metadata). Use this safetensors build with plain
# CLIPLoader, type: minimax.
hf Comfy-Org/MiniMax-H3 \
   text_encoders/qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors        "$M/text_encoders"

# Wan 2.2 TI2V-5B - wide/establishing/silent shots. Needs --vae-tiling.
hf Comfy-Org/Wan_2.2_ComfyUI_Repackaged \
   split_files/diffusion_models/wan2.2_ti2v_5B_fp16.safetensors      "$M/diffusion_models"
hf Comfy-Org/Wan_2.2_ComfyUI_Repackaged \
   split_files/vae/wan2.2_vae.safetensors                            "$M/vae"
hf city96/umt5-xxl-encoder-gguf umt5-xxl-encoder-Q8_0.gguf           "$M/text_encoders"

# Face detection for H3-FaceRefine
hf Bingsu/adetailer face_yolov8m.pt                                  "$M/ultralytics/bbox"

# ---------------------------------------------------------------- launch
log "dependency pins (each one is a fix, not a preference)"
$PIP install "moviepy==1.0.3"      # MuseTalk_FSH uses moviepy.editor, gone in 2.x
$PIP install "setuptools==79.0.1"  # restores pkg_resources
$PIP install -U filelock           # ultralytics needs AsyncFileLock
$PIP install chumpy --no-build-isolation
$PIP install openai-whisper        # audio QA: verify dialogue actually rendered
$PIP install "huggingface_hub[cli]"

# On Windows this needed VS Build Tools, a CUDA Toolkit install and a source
# patch (/std:c++17 -> c++20). On Linux the prebuilt wheel normally just works.
#
# NON-FATAL BY DESIGN. mmcv is only needed by MuseTalk (lip-sync) and
# H3-FaceRefine - neither is on the critical path for a first render, and the
# source build needs nvcc, which this image may not carry. Letting it abort the
# script would strand the ~99GB weight download behind a dependency we don't
# need yet. Fix it later, on a pod that already has the weights.
# --no-build-isolation on the FIRST attempt too: with isolation pip builds in a
# clean env that lacks our pinned setuptools 79, and mmcv's setup.py dies on
# "No module named 'pkg_resources'" before it ever reaches the compiler.
$PIP install --no-build-isolation mmcv==2.1.0 || {
  echo "!! mmcv wheel/build failed; retrying with CUDA_HOME set"
  CUDA_HOME=${CUDA_HOME:-/usr/local/cuda} $PIP install --no-build-isolation mmcv==2.1.0 || {
    echo "!! mmcv NOT INSTALLED - MuseTalk lip-sync and H3-FaceRefine will not load."
    echo "!! Everything else (MiniMax-H3, Wan 2.2) is unaffected. Continuing."
  }
}

# ComfyUI-GGUF's IMG_ARCH_LIST whitelist omits "ltx2", which is what the MiniMax
# turbo GGUF actually reports. Same patch as on Windows.
GGUF_LOADER=$COMFY/custom_nodes/ComfyUI-GGUF/loader.py
if [ -f "$GGUF_LOADER" ] && ! grep -q '"ltx2"' "$GGUF_LOADER"; then
  sed -i 's/IMG_ARCH_LIST = {/IMG_ARCH_LIST = {"ltx2", /' "$GGUF_LOADER"
  echo "patched IMG_ARCH_LIST to accept ltx2"
fi

log "launch script"
# Detached BY DEFAULT, deliberately. Started from a plain SSH session, ComfyUI
# dies the moment the connection drops - close the laptop mid-render and the job
# is gone while the pod keeps billing. Making the safe form the default means
# nobody has to remember the nohup incantation.
cat > $WS/start_comfy.sh <<EOF
#!/usr/bin/env bash
COMFY=$COMFY
PY=$VENV/bin/python
LOG=$WS/comfy.log
EOF
cat >> $WS/start_comfy.sh <<'EOF'
# usage: start_comfy.sh [--fg]
cd "$COMFY" || exit 1
ARGS=(main.py --listen 0.0.0.0 --port 8188 --preview-method none)

if [ "${1:-}" = "--fg" ]; then
  exec "$PY" "${ARGS[@]}"          # foreground, for debugging only
fi

if pgrep -f "main.py --listen" > /dev/null; then
  echo "ComfyUI is already running (pid $(pgrep -f 'main.py --listen' | head -1))"
  echo "log: $LOG"
  exit 0
fi

setsid nohup "$PY" "${ARGS[@]}" >> "$LOG" 2>&1 < /dev/null &
disown
sleep 2
echo "ComfyUI started detached. It survives SSH dropping and the laptop closing."
echo "log:  tail -f $LOG"
echo "stop: pkill -f 'main.py --listen'"
EOF
chmod +x $WS/start_comfy.sh

log "done"
echo "volume used: $(du -sh $WS 2>/dev/null | cut -f1)  (df cannot show your quota - use du)"
echo
echo "start ComfyUI:   bash /workspace/start_comfy.sh   (detaches itself - safe to close the laptop)"
echo "then from your laptop, in a second terminal:"
echo "  ssh -N -L 8188:localhost:8188 -i ~/.ssh/id_ed25519 -p <PORT> root@<POD_IP>"
echo "  set COMFY_SERVER=http://127.0.0.1:8188"
echo "  python runpod/comfy.py ping"
echo
echo "MuseTalk weights are NOT fetched here - they go in"
echo "  $COMFY/custom_nodes/ComfyUI-MuseTalk_FSH/models/<subfolder>/"
echo "exactly as that node's README lays out."
echo
echo "REMEMBER to stop the pod when the batch finishes."
