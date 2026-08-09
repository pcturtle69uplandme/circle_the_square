import sys
import os
import torch
import scipy.io.wavfile
import numpy as np

print("=== Meta MusicGen Large STEREO (facebook/musicgen-stereo-large, 3.3B) — GPU Epic Score ===")

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

print("[4/5] Model Loaded! Composing 4-movement upbeat action trailer score (~82s stereo)...")

# Movement 1 (~22s): Acts I - Driving energetic opening (S01-S03)
prompt1 = (
    "High-energy Hollywood action trailer opener, driving rhythmic pulse, punchy taiko drums, "
    "energetic staccato brass stabs, propulsive string ostinato, confident heroic momentum building, "
    "modern blockbuster trailer music, wide stereo image, pristine 32kHz studio master recording."
)

# Movement 2 (~22s): Acts II - Executive speech, upbeat but sharp (S04)
prompt2 = (
    "Upbeat action-packed Hollywood trailer soundtrack, punchy brass hits, fast energetic string runs, "
    "driving snare and taiko percussion, confident heroic swagger, corporate power-play energy, "
    "wide stereo image, pristine studio master recording."
)

# Movement 3 (~22s): Acts III - Whistleblower montage, fast and chaotic-fun (S05-S07)
prompt3 = (
    "Fast-paced action montage soundtrack, energetic non-repeating staccato violins, driving electric "
    "energy, punchy horn stabs, relentless rhythmic percussion, thrilling chase-scene momentum, "
    "upbeat heroic action energy, wide stereo image, pristine studio master recording."
)

# Movement 4 (~22s): Acts IV-V - Meltdown climax, BRAAM stings, triumphant title stinger (S08-S09 + title card)
prompt4 = (
    "Epic Hollywood blockbuster climax action soundtrack, heavy cinematic BRAAM low-frequency impact "
    "hits, explosive taiko drum rolls, soaring triumphant French horn and brass crescendo, fast "
    "energetic staccato strings, upbeat heroic action movie finale resolving into a big triumphant "
    "final impact sting, wide stereo image, pristine studio master recording."
)

print("[5/5] Neural-synthesizing 4 stereo studio music movements (max 22s each — safely inside MusicGen's coherent generation window)...")

def synth(prompt, seconds, label):
    tokens = int(seconds * 50)
    print(f"  -> {label}: {seconds}s ({tokens} tokens)")
    inputs = processor(text=[prompt], padding=True, return_tensors="pt").to(device)
    with torch.inference_mode():
        audio = model.generate(**inputs, max_new_tokens=tokens, guidance_scale=3.0)
    arr = audio[0].to(torch.float32).cpu().numpy()
    peak = np.abs(arr).max()
    if peak > 0.98:
        arr = arr / peak * 0.95
        print(f"     [normalize] peak was {peak:.2f} -> rescaled to 0.95")
    return arr

a1 = synth(prompt1, 22, "Movement 1 (Driving Opener)")
a2 = synth(prompt2, 22, "Movement 2 (Confident Power-Play)")
a3 = synth(prompt3, 22, "Movement 3 (Chase Montage)")
a4 = synth(prompt4, 22, "Movement 4 (Climax/Title)")

sampling_rate = model.config.audio_encoder.sampling_rate

def crossfade(a, b, seconds=2.0):
    # a, b: (channels, samples)
    n = int(sampling_rate * seconds)
    ramp = np.linspace(0, 1, n)
    a_end, a_body = a[:, -n:], a[:, :-n]
    b_start, b_body = b[:, :n], b[:, n:]
    overlap = a_end * (1 - ramp) + b_start * ramp
    return np.concatenate([a_body, overlap, b_body], axis=1)

merged = crossfade(a1, a2, 2.0)
merged = crossfade(merged, a3, 2.0)
merged = crossfade(merged, a4, 2.0)

# Final safety clamp — belt-and-braces against any residual overshoot/clicks
peak = np.abs(merged).max()
if peak > 0.98:
    merged = merged / peak * 0.95
    print(f"[final normalize] peak was {peak:.2f} -> rescaled to 0.95")
merged = np.clip(merged, -0.99, 0.99)

nan_count = np.isnan(merged).sum()
if nan_count:
    print(f"[WARNING] {nan_count} NaN samples found — zeroing them out")
    merged = np.nan_to_num(merged)

out_dir = r"C:\ai\Circle the Square\audio-refs"
os.makedirs(out_dir, exist_ok=True)
out_wav = os.path.join(out_dir, "musicgen_large_neural_score.wav")

# scipy expects (samples, channels) for stereo; write as 32-bit float (widely compatible)
scipy.io.wavfile.write(out_wav, rate=sampling_rate, data=merged.T.astype(np.float32))
print(f"\n[MASTER SUCCESS] Meta MusicGen Large STEREO (3.3B) Upbeat Action Score Generated!")
print(f"Output File: {out_wav} ({merged.shape[1]/sampling_rate:.1f}s, {merged.shape[0]} channels, peak {np.abs(merged).max():.2f})")
