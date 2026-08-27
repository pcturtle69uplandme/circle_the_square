#!/usr/bin/env bash
# Fetch LTX-2.3 for the existing sd-cli. No new runtime needed.
#
#   setsid nohup bash /workspace/get_ltx2.sh > /workspace/ltx2.log 2>&1 < /dev/null & disown
#
# WHY LTX-2.3
# MiniMax-H3 hit two ceilings on 2026-08-27: wide-shot faces need 720p (fixed),
# but doubling clip length to 124 frames degraded the picture progressively -
# a QUALITY ceiling, not a VRAM one (it fit in 41.7/46GB). LTX-2 is the only
# open-weight alternative that also generates its own synced audio, which is a
# hard requirement here (see AGENT_HANDOVER.md - no TTS/lip-sync chains).
#
# It needs NO new runtime: sd-cli already carries LTX audio VAE loading, LTXAV
# embeddings connectors, LTX VAE encoder v2+, temporal tiling and LTX latent
# spatial upscale. Confirmed by inspecting the built binary.
#
# WHY dev, NOT distilled
# The distilled build is 8-step and fast, and there is a distilled GGUF set in
# the same repo. Not used first, deliberately: MiniMax-H3's equivalent "turbo"
# checkpoint produced verified-broken audio (Whisper transcribed it as empty or
# nonsense) while the video looked fine. Audio is the whole reason this model is
# a candidate, so start from the quality build and only try distilled once the
# audio is confirmed good.
#
# WHY Q8_0
# 22B at Q8_0 is ~23GB. Unlike MiniMax there is no separate 18GB text encoder -
# just small embeddings connectors - so this fits a 48GB card with plenty of
# room for latents. Drop to Q6_K or Q4_K_M if VRAM turns out tight.

set -euo pipefail

WS=/workspace
RUN=$WS/ltx2
MODELS=$RUN/models
REPO=unsloth/LTX-2.3-GGUF
QUANT=${QUANT:-Q8_0}

mkdir -p "$MODELS/vae" "$MODELS/text_encoders" "$RUN/refs" "$RUN/output"
HF_CLI=$(command -v hf || command -v huggingface-cli)
[ -n "$HF_CLI" ] || { echo "!! no huggingface CLI"; exit 1; }

get() {  # get <remote_path> <local_dir>
  local target="$2/$(basename "$1")"
  if [ -e "$target" ]; then echo "  have $(basename "$1")"; return; fi
  echo "  fetching $(basename "$1")"
  "$HF_CLI" download "$REPO" "$1" --local-dir "$2"
  [ -f "$target" ] || find "$2" -name "$(basename "$1")" -exec mv {} "$2/" \; 2>/dev/null || true
}

echo "=== LTX-2.3 dev $QUANT -> $MODELS ==="
get "ltx-2.3-22b-dev-$QUANT.gguf"                                   "$MODELS"
get "text_encoders/ltx-2.3-22b-dev_embeddings_connectors.safetensors" "$MODELS/text_encoders"
get "vae/ltx-2.3-22b-dev_video_vae.safetensors"                     "$MODELS/vae"
get "vae/ltx-2.3-22b-dev_audio_vae.safetensors"                     "$MODELS/vae"

echo
echo "=== done: $(du -sh $MODELS | cut -f1) ==="
find "$MODELS" -type f \( -name '*.gguf' -o -name '*.safetensors' \) -printf '%-62f %10s bytes\n'
echo
echo "volume total: $(du -sh $WS | cut -f1)"
echo
cat <<'EOF'
Run it (LTX constraints: width/height divisible by 32, frames divisible by 8 plus 1):

  cd /workspace/ltx2
  setsid nohup /workspace/minimax/bin/sd-cli -M vid_gen \
    --diffusion-model      models/ltx-2.3-22b-dev-Q8_0.gguf \
    --embeddings-connectors models/text_encoders/ltx-2.3-22b-dev_embeddings_connectors.safetensors \
    --vae                  models/vae/ltx-2.3-22b-dev_video_vae.safetensors \
    --audio-vae            models/vae/ltx-2.3-22b-dev_audio_vae.safetensors \
    --auto-fit --diffusion-fa \
    -p "..." -W 1280 -H 736 --video-frames 121 --fps 24 --seed 201002 \
    -o output/LTX_test.mp4 -v \
    > output/LTX_test.log 2>&1 < /dev/null & disown
EOF
