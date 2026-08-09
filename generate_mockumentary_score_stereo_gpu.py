import sys
import os
import torch
import scipy.io.wavfile
import numpy as np

print("=== Meta MusicGen Large STEREO (facebook/musicgen-stereo-large, 3.3B) — Mockumentary Score ===")

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

# ==========================================================================
# DIRECTOR'S NOTE — genre pivot away from the "action trailer parody" score.
#
# "Circle the Square" is a mockumentary (The Office / Parks & Rec lineage),
# not an action-thriller. Those shows never score with orchestral BRAAMs or
# taiko drums — the joke lives in the DIALOGUE and the characters' delusion,
# not in the music underlining it. A real mockumentary composer (Jay
# Ferguson on The Office, or the Parks & Rec team) reaches for small, warm,
# ACOUSTIC ensembles: fingerpicked guitar, ukulele, upright/pizzicato bass,
# glockenspiel/marimba for "cute" accents, maybe a muted trumpet for
# pompous-executive comic timing. Dynamics stay gentle and observational —
# even the "meltdown" beat should undercut itself rather than swell like a
# thriller, because the comedy is that everyone else in the room is
# underreacting to the chaos.
# ==========================================================================

print("[4/5] Model Loaded! Composing 4-movement acoustic mockumentary score (~82s stereo)...")

# Movement 1 (~22s): Establishing shots — warm, slightly whimsical, ordinary-day-at-the-office
prompt1 = (
    "Warm quirky acoustic sitcom theme, gentle fingerpicked acoustic guitar melody, light marimba "
    "accents, soft upright bass, understated observational documentary feel, real organic "
    "instruments only, no synths, no orchestra, intimate close-mic studio recording, "
    "The Office mockumentary theme style."
)

# Movement 2 (~22s): The executive's self-important speech — playful, mock-pompous
prompt2 = (
    "Playful mock-pompous comedic theme, cheerful ukulele strumming, muted trumpet comic accents, "
    "light pizzicato strings, a self-important corporate executive strutting, gentle comedic timing, "
    "real acoustic instruments only, warm intimate studio recording, sitcom mockumentary underscore."
)

# Movement 3 (~22s): Staff talking-head interview cutaways — quirky, curious, slightly deadpan
prompt3 = (
    "Quirky deadpan interview-cutaway theme, plucked ukulele and glockenspiel, light walking upright "
    "bass, curious and slightly awkward comedic pacing, gentle woodwind (clarinet) accents, "
    "real acoustic instruments only, warm intimate documentary studio recording."
)

# Movement 4 (~22s): The meltdown & title card — comedic anticlimax, not a thriller swell
prompt4 = (
    "Gentle comedic anticlimax theme, acoustic guitar strum building slightly then relaxing back down, "
    "soft marimba button ending, light brushed snare, warm and good-natured resolution, "
    "real acoustic instruments only, no bombast, no orchestral swell, intimate sitcom closing theme."
)

print("[5/5] Neural-synthesizing 4 acoustic studio movements (max 22s each)...")

def synth(prompt, seconds, label):
    tokens = int(seconds * 50)
    print(f"  -> {label}: {seconds}s ({tokens} tokens)")
    inputs = processor(text=[prompt], padding=True, return_tensors="pt").to(device)
    with torch.inference_mode():
        # Lower guidance scale than the action score — acoustic ensembles read more
        # natural with less aggressive prompt adherence pressure.
        audio = model.generate(**inputs, max_new_tokens=tokens, guidance_scale=2.5)
    arr = audio[0].to(torch.float32).cpu().numpy()
    peak = np.abs(arr).max()
    if peak > 0.9:
        arr = arr / peak * 0.85
        print(f"     [normalize] peak was {peak:.2f} -> rescaled to 0.85")
    return arr

a1 = synth(prompt1, 22, "Movement 1 (Establishing/Warm)")
a2 = synth(prompt2, 22, "Movement 2 (Mock-Pompous Speech)")
a3 = synth(prompt3, 22, "Movement 3 (Interview Cutaways)")
a4 = synth(prompt4, 22, "Movement 4 (Anticlimax/Title)")

sampling_rate = model.config.audio_encoder.sampling_rate

def crossfade(a, b, seconds=2.0):
    n = int(sampling_rate * seconds)
    ramp = np.linspace(0, 1, n)
    a_end, a_body = a[:, -n:], a[:, :-n]
    b_start, b_body = b[:, :n], b[:, n:]
    overlap = a_end * (1 - ramp) + b_start * ramp
    return np.concatenate([a_body, overlap, b_body], axis=1)

merged = crossfade(a1, a2, 2.0)
merged = crossfade(merged, a3, 2.0)
merged = crossfade(merged, a4, 2.0)

peak = np.abs(merged).max()
if peak > 0.9:
    merged = merged / peak * 0.85
    print(f"[final normalize] peak was {peak:.2f} -> rescaled to 0.85")
merged = np.clip(merged, -0.95, 0.95)

nan_count = np.isnan(merged).sum()
if nan_count:
    print(f"[WARNING] {nan_count} NaN samples found — zeroing them out")
    merged = np.nan_to_num(merged)

out_dir = r"C:\ai\Circle the Square\audio-refs"
os.makedirs(out_dir, exist_ok=True)
out_wav = os.path.join(out_dir, "musicgen_mockumentary_score.wav")

scipy.io.wavfile.write(out_wav, rate=sampling_rate, data=merged.T.astype(np.float32))
print(f"\n[MASTER SUCCESS] Meta MusicGen Large STEREO (3.3B) Mockumentary Score Generated!")
print(f"Output File: {out_wav} ({merged.shape[1]/sampling_rate:.1f}s, {merged.shape[0]} channels, peak {np.abs(merged).max():.2f})")
