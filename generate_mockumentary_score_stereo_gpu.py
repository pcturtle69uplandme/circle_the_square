import sys
import os
import torch
import scipy.io.wavfile
import numpy as np

print("=== Meta MusicGen Large STEREO (facebook/musicgen-stereo-large, 3.3B) — CALM CONTINUOUS Mockumentary Score ===")

try:
    from transformers import AutoProcessor, MusicgenForConditionalGeneration
    print("[1/4] Transformers & Audio Dependencies Loaded OK!")
except ImportError as e:
    print("[ERROR] Required libraries not found:", e)
    sys.exit(1)

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[2/4] Device: {device} ({torch.cuda.get_device_name(0) if device == 'cuda' else 'CPU fallback'})")

model_id = "facebook/musicgen-stereo-large"
local_dir = r"C:\ai\models\musicgen-stereo-large"
os.makedirs(local_dir, exist_ok=True)
dtype = torch.float16 if device == "cuda" else torch.float32

print(f"[3/5] Loading {model_id} (stereo 3.3B checkpoint, already cached locally)...")
processor = AutoProcessor.from_pretrained(model_id, cache_dir=local_dir)
model = MusicgenForConditionalGeneration.from_pretrained(model_id, cache_dir=local_dir, dtype=dtype).to(device)

sampling_rate = model.config.audio_encoder.sampling_rate

# ==========================================================================
# DIRECTOR'S NOTE — genre pivot away from the "action trailer parody" score.
#
# "Circle the Square" is a mockumentary (The Office / Parks & Rec lineage),
# not an action-thriller. Those shows never score with orchestral BRAAMs or
# taiko drums — the joke lives in the DIALOGUE and the characters' delusion,
# not in the music underlining it. A real mockumentary composer (Jay
# Ferguson on The Office, or the Parks & Rec team) reaches for small, warm,
# ACOUSTIC ensembles: fingerpicked guitar, ukulele, upright/pizzicato bass,
# glockenspiel/marimba for "cute" accents. Dynamics stay gentle and
# observational — even the "meltdown" beat should undercut itself rather
# than swell like a thriller, because the comedy is that everyone else in
# the room is underreacting to the chaos.
#
# CALM REVISION — the first acoustic pass was the right genre but too BUSY:
# strummed ukulele, comic muted-trumpet stabs, brushed snare, a movement
# that "builds". None of that leaves room for dialogue. Energy is now taken
# out on every axis: an explicit slow tempo (~72 BPM), a SPARSE arrangement
# with space between notes, no percussion at all, fingerpicking instead of
# strumming, guidance_scale 2.5 -> 2.0 and temperature 0.85 (both cut
# erratic flourishes), and a 0.62 peak ceiling so the bed already sits low
# under dialogue before the trailer mix touches it.
#
# CONTINUITY FIX — the earlier score audibly changed tune between the
# interview cutaways. That was structural, not a prompt problem: the script
# made four INDEPENDENT generate() calls with four DIFFERENT text prompts,
# so each movement was its own composition in its own key and tempo, merely
# crossfaded onto the last one. Two changes fix it:
#
#   1. ONE text prompt (CUE_PROMPT) for the entire cue. The per-movement
#      prompts are deliberately gone — differing prompts guarantee
#      differing tunes.
#   2. AUDIO CONTINUATION. Every segment after the first is generated with
#      the tail of the previous segment fed back in as an audio prompt, so
#      MusicGen continues the melody, key and tempo it already established
#      instead of starting a fresh idea. Joins get a short equal-power
#      crossfade only to hide the re-encode seam, not to disguise a change
#      of tune.
#
# The result is a single ~82s piece that develops but never restarts.
# ==========================================================================

# One prompt, used for the first segment and every continuation. Do not
# split this into per-section prompts again — that is what broke continuity.
CUE_PROMPT = (
    "Slow calm acoustic mockumentary underscore, around 72 BPM, one continuous gentle piece with a "
    "single recurring melody, softly fingerpicked nylon acoustic guitar, sparse ukulele plucks, "
    "quiet sustained upright bass, occasional soft marimba and glockenspiel notes, "
    "sparse arrangement with plenty of space between notes, soft low dynamics, unhurried, "
    "warm and wry and observational, no drums, no percussion, no synths, no orchestra, "
    "no build-up, no key change, real acoustic instruments only, "
    "warm intimate close-mic studio recording, quiet background bed that sits under dialogue"
)

# --- Generation parameters -------------------------------------------------
# MusicGen's audio decoder tops out at 1500 tokens (30s) per call, INCLUDING
# the tokens of any audio prompt. 8s prompt (400 tok) + 20s new (1000 tok)
# = 1400, which stays safely inside that ceiling.
FIRST_SEGMENT_SECONDS = 24
SEGMENT_SECONDS = 20
PROMPT_TAIL_SECONDS = 8
NUM_CONTINUATIONS = 3          # 24 + 3*20 = 84s raw, ~82.5s after joins
JOIN_CROSSFADE_SECONDS = 0.5   # just enough to hide the EnCodec re-encode seam

# 2.0 relaxes prompt-adherence pressure and a sub-1.0 temperature keeps the
# sampler from wandering into fills — both read as "calmer".
GUIDANCE_SCALE = 2.0
TEMPERATURE = 0.85
# The earlier score peaked at 0.85, loud for a bed playing under six dialogue
# streams. 0.62 is roughly -3 dB from that.
PEAK_CEILING = 0.62


def _to_numpy(audio_tensor):
    return audio_tensor[0].to(torch.float32).cpu().numpy()


def generate_opening(seconds):
    """First segment — text-conditioned only, establishes the tune."""
    tokens = int(seconds * 50)
    print(f"  -> Opening segment: {seconds}s ({tokens} tokens)")
    inputs = processor(text=[CUE_PROMPT], padding=True, return_tensors="pt").to(device)
    with torch.inference_mode():
        audio = model.generate(
            **inputs,
            max_new_tokens=tokens,
            guidance_scale=GUIDANCE_SCALE,
            do_sample=True,
            temperature=TEMPERATURE,
        )
    return _to_numpy(audio)


def generate_continuation(tail, seconds, index):
    """Continue the existing cue from `tail` (shape: channels x samples).

    Returns ONLY the newly generated audio — MusicGen hands back the audio
    prompt re-encoded at the head of the sequence, so that prefix is trimmed.
    """
    tokens = int(seconds * 50)
    print(f"  -> Continuation {index}: +{seconds}s ({tokens} tokens, {PROMPT_TAIL_SECONDS}s audio prompt)")

    def _build_inputs(prompt_audio):
        return processor(
            audio=prompt_audio,
            sampling_rate=sampling_rate,
            text=[CUE_PROMPT],
            padding=True,
            return_tensors="pt",
        ).to(device)

    try:
        inputs = _build_inputs(tail)
    except Exception as e:
        # Some processor versions want a mono conditioning signal even for the
        # stereo checkpoint. Downmix and retry before giving up on continuation.
        print(f"     [note] stereo audio prompt rejected ({e}); retrying with mono downmix")
        inputs = _build_inputs(tail.mean(axis=0))

    with torch.inference_mode():
        audio = model.generate(
            **inputs,
            max_new_tokens=tokens,
            guidance_scale=GUIDANCE_SCALE,
            do_sample=True,
            temperature=TEMPERATURE,
        )
    arr = _to_numpy(audio)

    # Drop the re-encoded prompt prefix if it came back with the continuation.
    # Guarded rather than assumed, so this holds if the behaviour differs.
    if arr.shape[1] > tail.shape[1] + int(0.5 * sampling_rate):
        arr = arr[:, tail.shape[1]:]
        print(f"     [trim] removed {PROMPT_TAIL_SECONDS}s re-encoded prompt prefix")
    return arr


def equal_power_join(a, b, seconds=JOIN_CROSSFADE_SECONDS):
    """Butt two continuous segments together, hiding the seam."""
    n = int(sampling_rate * seconds)
    n = min(n, a.shape[1], b.shape[1])
    if n <= 0:
        return np.concatenate([a, b], axis=1)
    t = np.linspace(0.0, 1.0, n)
    fade_out, fade_in = np.cos(t * np.pi / 2), np.sin(t * np.pi / 2)
    overlap = a[:, -n:] * fade_out + b[:, :n] * fade_in
    return np.concatenate([a[:, :-n], overlap, b[:, n:]], axis=1)


print("[4/5] Model Loaded! Composing ONE continuous calm acoustic cue (~82s stereo)...")
print("[5/5] Neural-synthesizing via audio continuation (single tune throughout)...")

merged = generate_opening(FIRST_SEGMENT_SECONDS)

continuation_failed = False
for i in range(1, NUM_CONTINUATIONS + 1):
    tail_samples = int(PROMPT_TAIL_SECONDS * sampling_rate)
    tail = merged[:, -tail_samples:]
    try:
        nxt = generate_continuation(tail, SEGMENT_SECONDS, i)
    except Exception as e:
        # Fall back rather than abandon the run — the 3.3B model takes a long
        # time to load and generate, and a usable score beats no score.
        print(f"     [WARNING] continuation {i} failed ({e}); falling back to an")
        print("               independent segment on the same prompt (a tune change")
        print("               may be audible at this join)")
        continuation_failed = True
        nxt = generate_opening(SEGMENT_SECONDS)
    merged = equal_power_join(merged, nxt)

if continuation_failed:
    print("\n[NOTE] At least one segment could not be audio-continued. If the tune still")
    print("       shifts, check the installed transformers version supports passing")
    print("       audio= to the MusicGen processor for audio-prompted generation.")


def apply_edge_fades(sig, fade_in=2.0, fade_out=3.0):
    """Ease the cue in and out so it never announces itself."""
    n_in = min(int(sampling_rate * fade_in), sig.shape[1])
    n_out = min(int(sampling_rate * fade_out), sig.shape[1])
    sig[:, :n_in] *= np.linspace(0.0, 1.0, n_in)
    sig[:, -n_out:] *= np.linspace(1.0, 0.0, n_out)
    return sig


merged = apply_edge_fades(merged)

peak = np.abs(merged).max()
if peak > PEAK_CEILING:
    merged = merged / peak * PEAK_CEILING
    print(f"[final normalize] peak was {peak:.2f} -> rescaled to {PEAK_CEILING}")
merged = np.clip(merged, -0.95, 0.95)

nan_count = np.isnan(merged).sum()
if nan_count:
    print(f"[WARNING] {nan_count} NaN samples found — zeroing them out")
    merged = np.nan_to_num(merged)

# Resolve audio-refs next to this script so the same file works from any
# checkout location (C:\ai\Circle the Square on the main PC, or elsewhere)
# instead of relying on a hardcoded absolute path.
out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio-refs")
os.makedirs(out_dir, exist_ok=True)
# Written alongside the previous score, not over it — build_action_trailer_master.py
# picks this one first and falls back to the earlier ones if it is missing.
out_wav = os.path.join(out_dir, "musicgen_calm_mockumentary_score.wav")

scipy.io.wavfile.write(out_wav, rate=sampling_rate, data=merged.T.astype(np.float32))
print(f"\n[MASTER SUCCESS] Meta MusicGen Large STEREO (3.3B) CALM CONTINUOUS Mockumentary Score Generated!")
print(f"Output File: {out_wav} ({merged.shape[1]/sampling_rate:.1f}s, {merged.shape[0]} channels, peak {np.abs(merged).max():.2f})")
print("Next: run build_action_trailer_master.py to re-render the trailer with this score.")
