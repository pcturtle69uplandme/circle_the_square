#!/usr/bin/env bash
# Bootstrap a RunPod pod for Circle the Square rendering.
#
#   ssh into the pod, then:
#     curl -sL <this file> -o setup_pod.sh && bash setup_pod.sh
#   or scp it up and run it.
#
# Everything lands on /workspace (the network volume) so it SURVIVES the pod.
# Run it again on a fresh pod and it skips whatever is already there - the
# expensive part (~95GB of weights) only downloads once, ever.
#
# Weight inventory and the reasons behind each file are in
#   minimax-h3-pipeline/README.md and wan22-pipeline/README.md
# Do not "tidy up" the odd-looking pins below; each one is a documented fix.

set -euo pipefail

WS=/workspace
COMFY=$WS/ComfyUI
MODELS=$WS/models
VENV=$WS/venv

log() { echo -e "\n=== $* ==="; }
have() { [ -e "$1" ]; }

# ---------------------------------------------------------------- sanity
log "environment"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
df -h $WS | tail -1
if ! mountpoint -q $WS 2>/dev/null; then
  echo "!! WARNING: $WS is not a mount point."
  echo "!! You are about to write ~95GB to the CONTAINER DISK, which is erased"
  echo "!! when the pod stops. Attach a network volume at /workspace first."
  read -rp "Continue anyway? [y/N] " a; [ "$a" = y ] || exit 1
fi

mkdir -p $WS $MODELS

# ---------------------------------------------------------------- python
log "python venv on the volume"
if ! have $VENV; then python3 -m venv $VENV; fi
# shellcheck disable=SC1091
source $VENV/bin/activate
pip install -q --upgrade pip wheel
pip install -q "huggingface_hub[cli]"

# ---------------------------------------------------------------- comfyui
log "ComfyUI"
if ! have $COMFY; then
  git clone https://github.com/comfyanonymous/ComfyUI.git $COMFY
fi
pip install -q -r $COMFY/requirements.txt

log "custom nodes"
cd $COMFY/custom_nodes
clone_node() {  # clone_node <url> <dirname>
  have "$2" || git clone "$1" "$2"
  [ -f "$2/requirements.txt" ] && pip install -q -r "$2/requirements.txt" || true
}
clone_node https://github.com/city96/ComfyUI-GGUF.git                ComfyUI-GGUF
clone_node https://github.com/Carasibana/ComfyUI-H3-FaceRefine.git   ComfyUI-H3-FaceRefine
clone_node https://github.com/AIFSH/ComfyUI-MuseTalk_FSH.git         ComfyUI-MuseTalk_FSH

# Documented pins. See wan22-pipeline/comfyui-tools/README.md for why each exists.
log "dependency pins (each one is a fix, not a preference)"
pip install -q "moviepy==1.0.3"      # MuseTalk_FSH uses moviepy.editor, gone in 2.x
pip install -q "setuptools==79.0.1"  # restores pkg_resources
pip install -q -U filelock           # ultralytics needs AsyncFileLock
pip install -q chumpy --no-build-isolation
pip install -q openai-whisper        # audio QA: verify dialogue actually rendered

# mmcv: on Windows this needed VS Build Tools, a CUDA Toolkit install and a
# source patch (/std:c++17 -> c++20). On Linux the prebuilt wheel normally just
# works. If it does not, build from source with CUDA_HOME set.
pip install -q mmcv==2.1.0 || {
  echo "!! prebuilt mmcv failed; building from source"
  CUDA_HOME=/usr/local/cuda pip install --no-build-isolation mmcv==2.1.0
}

# ComfyUI-GGUF's IMG_ARCH_LIST whitelist omits "ltx2", which is the architecture
# string the MiniMax turbo GGUF actually reports. Same patch as on Windows.
GGUF_LOADER=$COMFY/custom_nodes/ComfyUI-GGUF/loader.py
if [ -f "$GGUF_LOADER" ] && ! grep -q '"ltx2"' "$GGUF_LOADER"; then
  sed -i 's/IMG_ARCH_LIST = {/IMG_ARCH_LIST = {"ltx2", /' "$GGUF_LOADER"
  echo "patched IMG_ARCH_LIST to accept ltx2"
fi

# ---------------------------------------------------------------- weights
log "weights (~95GB, once per volume)"
# huggingface_hub renamed the CLI to `hf` in 0.34; `huggingface-cli` still works
# but warns. Prefer whichever exists so this survives either version.
HF_CLI=$(command -v hf || command -v huggingface-cli)
[ -n "$HF_CLI" ] || { echo "!! no huggingface CLI on PATH"; exit 1; }

hf() {  # hf <repo> <remote_path> <local_dir>
  local target="$3/$(basename "$2")"
  if have "$target"; then echo "  have $(basename "$2")"; return; fi
  mkdir -p "$3"
  echo "  fetching $(basename "$2")"
  "$HF_CLI" download "$1" "$2" --local-dir "$3"
  # flatten if the CLI preserved the remote subdirectory
  [ -f "$target" ] || find "$3" -name "$(basename "$2")" -exec mv {} "$3/" \; 2>/dev/null || true
}

M=$COMFY/models
# MiniMax-H3 - close-up dialogue shots (this one has working audio)
hf unsloth/MiniMax-H3-GGUF minimax_h3_ref2va_pruned-Q4_K.gguf        "$M/diffusion_models"
hf unsloth/MiniMax-H3-GGUF minimax_h3_fl2va_pruned-Q4_K.gguf         "$M/diffusion_models"
hf unsloth/MiniMax-H3-GGUF vae/minimax_h3_video_vae_fp16.safetensors "$M/vae"
hf unsloth/MiniMax-H3-GGUF vae/minimax_h3_audio_vae_fp32.safetensors "$M/vae"
# Turbo denoiser: note the real path is under split/, not the repo root.
# AUDIO IS BROKEN on this one - silent/no-dialogue shots only, --steps 4 --guidance 1.0.
hf ChrisColeTech/minimax-h3-turbo-GGUF \
   split/diffusion_models/minimax_h3_ref2va_turbo_Q4_K_M.gguf        "$M/diffusion_models"
# Text encoder: the 32B GGUF does NOT load via CLIPLoaderGGUF (no general.architecture
# metadata). Use this safetensors build with plain CLIPLoader, type: minimax.
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
log "launch script"
cat > $WS/start_comfy.sh <<'EOF'
#!/usr/bin/env bash
source /workspace/venv/bin/activate
cd /workspace/ComfyUI
exec python main.py --listen 0.0.0.0 --port 8188 --preview-method none
EOF
chmod +x $WS/start_comfy.sh

log "done"
echo "start ComfyUI:   bash /workspace/start_comfy.sh"
echo "then from your laptop:"
echo "  set COMFY_POD=<pod id>"
echo "  python runpod/comfy.py ping"
echo
echo "MuseTalk weights are NOT fetched here - they go in"
echo "  $COMFY/custom_nodes/ComfyUI-MuseTalk_FSH/models/<subfolder>/"
echo "exactly as that node's README lays out. See wan22-pipeline/comfyui-tools/README.md."
