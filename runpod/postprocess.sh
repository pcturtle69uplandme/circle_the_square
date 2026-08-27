#!/usr/bin/env bash
# Post-processing pass for generated clips: face restoration + optional upscale.
#
#   bash postprocess.sh /workspace/minimax/output/F01_Q8_30step.mp4 [--fidelity 0.7] [--upscale 2]
#
# ---------------------------------------------------------------------------
# WHY THIS EXISTS
#
# Every clip judged so far has been RAW single-model output. People posting
# "movie quality" open-model video are running a pipeline: generate -> face
# restore -> upscale -> interpolate -> grade. We had only the first stage.
#
# Face restoration is the stage that matters most here. The complaint is soft
# faces in wide shots, where Jan occupies ~90x110 pixels. CodeFormer is built
# for exactly that: it hallucinates plausible facial detail from a degraded
# face crop. Plain upscaling cannot - it sharpens what exists, it does not
# invent eyes.
#
# ⚠️ THE RISK: identity drift. CodeFormer invents detail, and invented detail
# may not be JAN's. --fidelity controls the trade (0 = prettiest, 1 = most
# faithful to input). Default 0.7 leans faithful, because character consistency
# across 64 frames matters more than any single frame looking good. CHECK THE
# FACE AGAINST character-refs/ BEFORE adopting a setting.
#
# ⚠️ AUDIO: the whole reason MiniMax-H3 was chosen is its synced audio. This
# script extracts the original audio stream and remuxes it onto the processed
# video untouched - frames are rebuilt, audio is never re-generated. It also
# re-encodes rather than stream-copies on assembly, because stream-copy is what
# corrupted audio at splice boundaries previously.
# ---------------------------------------------------------------------------

set -euo pipefail

IN="${1:?usage: postprocess.sh <input.mp4> [--fidelity F] [--upscale N]}"
shift || true
FIDELITY=0.7
UPSCALE=1
while [ $# -gt 0 ]; do
  case "$1" in
    --fidelity) FIDELITY="$2"; shift 2 ;;
    --upscale)  UPSCALE="$2";  shift 2 ;;
    *) echo "unknown arg: $1"; exit 1 ;;
  esac
done

[ -f "$IN" ] || { echo "!! no such file: $IN"; exit 1; }
BASE=$(basename "$IN" .mp4)
OUTDIR=$(dirname "$IN")
OUT="$OUTDIR/${BASE}_post.mp4"
# Container disk: thousands of small PNGs would be brutally slow on the volume.
WORK=/opt/postwork/$BASE
CODEFORMER=/opt/CodeFormer

log() { echo -e "\n=== $* ==="; }

rm -rf "$WORK"; mkdir -p "$WORK/in" "$WORK/out"

# ---------------------------------------------------------------- probe
FPS=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate \
        -of default=nw=1:nk=1 "$IN" | awk -F/ '{ if ($2) print $1/$2; else print $1 }')
HAS_AUDIO=$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$IN" | head -1)
log "input: $IN  fps=$FPS  audio=${HAS_AUDIO:+yes}"

# ---------------------------------------------------------------- split
log "extracting frames -> $WORK/in (container disk)"
ffmpeg -v error -y -i "$IN" "$WORK/in/%06d.png"
echo "frames: $(ls "$WORK/in" | wc -l)"
if [ -n "$HAS_AUDIO" ]; then
  ffmpeg -v error -y -i "$IN" -vn -acodec copy "$WORK/audio.m4a" 2>/dev/null \
    || ffmpeg -v error -y -i "$IN" -vn "$WORK/audio.wav"
  echo "audio extracted (original stream, never regenerated)"
fi

# ---------------------------------------------------------------- CodeFormer
log "face restoration (CodeFormer, fidelity=$FIDELITY)"
if [ ! -d "$CODEFORMER" ]; then
  git clone --depth 1 https://github.com/sczhou/CodeFormer.git "$CODEFORMER"
  pip install --quiet -r "$CODEFORMER/requirements.txt" || true
  pip install --quiet basicsr facexlib || true
  (cd "$CODEFORMER" && python3 basicsr/setup.py develop >/dev/null 2>&1) || true
  (cd "$CODEFORMER" && python3 scripts/download_pretrained_models.py facelib >/dev/null 2>&1) || true
  (cd "$CODEFORMER" && python3 scripts/download_pretrained_models.py CodeFormer >/dev/null 2>&1) || true
fi

RESTORED="$WORK/in"
if (cd "$CODEFORMER" && python3 inference_codeformer.py \
      -w "$FIDELITY" --input_path "$WORK/in" --output_path "$WORK/cf" \
      --bg_upsampler none 2>&1 | tail -5); then
  # CodeFormer writes into a final_results/ subdirectory
  FOUND=$(find "$WORK/cf" -type d -name final_results | head -1)
  if [ -n "$FOUND" ] && [ "$(ls -A "$FOUND" 2>/dev/null | wc -l)" -gt 0 ]; then
    RESTORED="$FOUND"
    echo "restored frames: $(ls "$RESTORED" | wc -l)"
  else
    echo "!! CodeFormer produced no frames - continuing with originals"
  fi
else
  echo "!! CodeFormer failed - continuing with originals (not fatal)"
fi

# ---------------------------------------------------------------- reassemble
log "reassembling at ${FPS}fps"
VF=""
[ "$UPSCALE" != "1" ] && VF="-vf scale=iw*${UPSCALE}:ih*${UPSCALE}:flags=lanczos"

if [ -n "$HAS_AUDIO" ]; then
  AUD=$(ls "$WORK"/audio.* 2>/dev/null | head -1)
  # Re-encode, never stream-copy: -c copy corrupts audio at AAC splice points.
  ffmpeg -v error -y -framerate "$FPS" -i "$RESTORED/%06d.png" -i "$AUD" \
    $VF -c:v libx264 -crf 16 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest "$OUT"
else
  ffmpeg -v error -y -framerate "$FPS" -i "$RESTORED/%06d.png" \
    $VF -c:v libx264 -crf 16 -pix_fmt yuv420p "$OUT"
fi

log "done"
ls -la "$OUT"
ffprobe -v error -show_entries format=duration:stream=codec_type,width,height \
        -of default=nw=1 "$OUT"
echo
echo "Compare against the original before adopting: $IN"
echo "Check the FACE against character-refs/ - CodeFormer can drift identity."
