#!/usr/bin/env bash
# Lean pod bootstrap: MiniMax-H3 ONLY. No ComfyUI, no Wan, no MuseTalk, no TTS.
#
#   scp this up, then:  setsid nohup bash /workspace/setup_pod_minimax.sh \
#                         > /workspace/setup.log 2>&1 < /dev/null & disown
#
# ---------------------------------------------------------------------------
# WHY THIS EXISTS
#
# MiniMax-H3 generates video AND native synced audio from one model, so it
# replaces the whole Wan-silent -> Qwen3-TTS -> MuseTalk lip-sync chain for
# dialogue shots. Dropping to a single model removes ~60GB of weights, ComfyUI,
# three custom nodes, mmcv, and every environment fight from the 2026-08-26
# sessions.
#
# The known cost: MiniMax-H3 cannot do WIDE shots - faces resolve to a
# featureless blob at 864x480 in full-room framing. HANDOVER.md calls that "a
# pixel-count problem, not a quantization one", so the only lever is rendering
# larger, which is why 48GB was worth insisting on. UNTESTED as of this script.
#
# WHY sd-cli IS BUILT, NOT DOWNLOADED
#
# stable-diffusion.cpp publishes a prebuilt *Windows* CUDA binary (what the main
# PC uses) but NO Linux CUDA build - Linux releases are CPU/Vulkan/ROCm only. So
# it gets compiled here. nvcc IS present at /usr/local/cuda/bin, it is just not
# on PATH by default.
#
# LAYOUT: small files on the container disk, big files on the volume.
# Measured on this pod (A40, ca-mtl-1), 300 small files:
#     container disk :    16 ms
#     network volume : 3,957 ms      (~250x slower - and the US-KS-2 volume was
#                                     147,884 ms, so this varies wildly by DC)
# ---------------------------------------------------------------------------

set -euo pipefail

WS=/workspace
BUILD=/opt/sd.cpp            # container disk: thousands of small object files
RUN=$WS/minimax              # volume: binary, weights, refs, output
MODELS=$RUN/models
CUDA_ARCH=${CUDA_ARCH:-86}   # A40/A6000/3090 = 86. 4090 = 89. Blackwell = 120.

export PATH=/usr/local/cuda/bin:$PATH

log() { echo -e "\n=== $* ==="; }
have() { [ -e "$1" ]; }

# ---------------------------------------------------------------- sanity
log "environment"
nvidia-smi --query-gpu=name,memory.total,compute_cap --format=csv,noheader
nvcc --version | tail -1
mountpoint -q $WS || { echo "!! $WS is not a mount - weights would not persist"; exit 1; }
mkdir -p "$MODELS" "$RUN/refs" "$RUN/output" "$RUN/bin"

# ---------------------------------------------------------------- weights first
# Deliberately BEFORE the build: this is the long pole and the part that must
# not be gated behind a compiler problem. Last session a dependency build we
# didn't even need stranded the whole download.
log "weights -> $MODELS (~40GB, large sequential files)"
pip install -q --break-system-packages "huggingface_hub[cli]" 2>/dev/null \
  || pip install -q "huggingface_hub[cli]"
HF_CLI=$(command -v hf || command -v huggingface-cli)

get() {  # get <repo> <remote_path> <local_dir>
  local target="$3/$(basename "$2")"
  if have "$target"; then echo "  have $(basename "$2")"; return; fi
  mkdir -p "$3"
  echo "  fetching $(basename "$2")"
  "$HF_CLI" download "$1" "$2" --local-dir "$3"
  [ -f "$target" ] || find "$3" -name "$(basename "$2")" -exec mv {} "$3/" \; 2>/dev/null || true
}

# Ref2VA only. fl2va is text-only and gen_clip.py is hardcoded to Ref2VA; turbo
# is skipped because its audio is verified broken (Whisper: empty/wrong) and this
# pipeline is now carrying ALL the dialogue.
get unsloth/MiniMax-H3-GGUF minimax_h3_ref2va_pruned-Q4_K.gguf        "$MODELS"
get unsloth/MiniMax-H3-GGUF qwen3vl_32b_minimax_h3-Q4_K_M.gguf        "$MODELS"
get unsloth/MiniMax-H3-GGUF vae/minimax_h3_video_vae_fp16.safetensors "$MODELS/vae"
get unsloth/MiniMax-H3-GGUF vae/minimax_h3_audio_vae_fp32.safetensors "$MODELS/vae"

echo "weights on volume: $(du -sh $MODELS | cut -f1)"

# ---------------------------------------------------------------- build sd-cli
log "stable-diffusion.cpp -> $BUILD (container disk), CUDA arch $CUDA_ARCH"
if ! have $BUILD; then
  git clone --recursive https://github.com/leejet/stable-diffusion.cpp $BUILD
fi
cd $BUILD
# The CUDA flag was renamed; try the current name, fall back to the old one.
cmake -B build -DCMAKE_BUILD_TYPE=Release \
      -DSD_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=$CUDA_ARCH 2>/dev/null \
  || cmake -B build -DCMAKE_BUILD_TYPE=Release \
      -DSD_CUBLAS=ON -DCMAKE_CUDA_ARCHITECTURES=$CUDA_ARCH
# NOT $(nproc). nproc reports the HOST - 96 on this pod - while the cgroup quota
# is 7.65 CPUs. `make -j96` on 7.65 CPUs drove load average to 37 and thrashed.
# Read the real quota instead; this is the same trap documented in
# RUNPOD_CLOUD_RENDERING.md §7 for worker counts and batch sizes.
JOBS=$(awk '{ if ($1 == "max") print 4; else { n = int($1/$2); print (n < 1 ? 1 : n) } }' \
        /sys/fs/cgroup/cpu.max 2>/dev/null || echo 4)
echo "building with -j$JOBS (nproc claims $(nproc), cgroup allows $JOBS)"
cmake --build build --config Release -j"$JOBS"

BIN=$(find $BUILD/build -maxdepth 3 -type f -name 'sd*' -perm -u+x ! -name '*.o' | head -1)
[ -n "$BIN" ] || { echo "!! built, but no sd binary found under $BUILD/build"; exit 1; }
cp "$BIN" "$RUN/bin/sd-cli"
chmod +x "$RUN/bin/sd-cli"
echo "binary: $RUN/bin/sd-cli"
"$RUN/bin/sd-cli" --help 2>&1 | head -3 || true

# ---------------------------------------------------------------- done
log "done"
echo "layout:"
echo "  binary : $RUN/bin/sd-cli"
echo "  models : $MODELS  ($(du -sh $MODELS | cut -f1))"
echo "  refs   : $RUN/refs     <- scp reference images here"
echo "  output : $RUN/output   <- clips land here"
echo
echo "volume total: $(du -sh $WS | cut -f1)   (df cannot show the quota - use du)"
echo
echo "Run clips DETACHED - an SSH drop otherwise kills the render while the pod bills:"
echo "  setsid nohup python3 $RUN/gen_clip.py --out F01_c1 --seed 101001 \\"
echo "    --refs jan.jpg office.png --prompt \"...\" \\"
echo "    > $RUN/output/F01_c1.log 2>&1 < /dev/null & disown"
echo
echo "REMEMBER to stop the pod when the batch finishes. Nothing will remind you."
