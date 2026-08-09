import sys
import torch
import scipy.io.wavfile
import numpy as np
import os

print("=== Downloading & Running Meta MusicGen Large (facebook/musicgen-large 3.3B Parameters) ===")

try:
    from transformers import AutoProcessor, MusicgenForConditionalGeneration
    print("[1/4] Transformers and Audio Dependencies Loaded OK!")
except ImportError as e:
    print("[ERROR] Required libraries not found:", e)
    sys.exit(1)

device = "cpu"
print(f"[2/4] Downloading Meta MusicGen Large model weights (facebook/musicgen-large)...")

processor = AutoProcessor.from_pretrained("facebook/musicgen-large")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-large").to(device)

print("[3/4] Model loaded successfully! Preparing Hollywood Action Blockbuster Prompt...")

prompt1 = (
    "Epic Hollywood blockbuster action trailer soundtrack part 1, "
    "massive thunderous orchestral brass braams, aggressive staccato string section, "
    "driving taiko drum percussion, heroic French horn motif, 135 bpm, studio master."
)

prompt2 = (
    "Epic Hollywood blockbuster action trailer soundtrack part 2 climax, "
    "fast orchestral string ostinato, explosive brass crescendo, timpani drum rolls, "
    "heroic orchestral climax, 135 bpm, pristine studio master production."
)

print("[4/4] Generating 2x 35s High-Fidelity Audio Blocks (within 2048 positional embedding limit)...")

# Block 1 (35 seconds = 1750 tokens)
inputs1 = processor(text=[prompt1], padding=True, return_tensors="pt").to(device)
with torch.inference_mode():
    audio1 = model.generate(**inputs1, max_new_tokens=1750)

# Block 2 (35 seconds = 1750 tokens)
inputs2 = processor(text=[prompt2], padding=True, return_tensors="pt").to(device)
with torch.inference_mode():
    audio2 = model.generate(**inputs2, max_new_tokens=1750)

sampling_rate = model.config.audio_encoder.sampling_rate
a1 = audio1[0, 0].cpu().numpy().astype(float)
a2 = audio2[0, 0].cpu().numpy().astype(float)

# Crossfade 2.0s transition between Block 1 and Block 2
fade_samples = int(sampling_rate * 2.0)
crossfade = np.linspace(0, 1, fade_samples)

a1_end = a1[:-fade_samples]
overlap = a1[-fade_samples:] * (1 - crossfade) + a2[:fade_samples] * crossfade
a2_start = a2[fade_samples:]

full_audio = np.concatenate([a1_end, overlap, a2_start])

out_dir = r"C:\ai\Circle the Square\audio-refs"
os.makedirs(out_dir, exist_ok=True)
out_wav = os.path.join(out_dir, "action_musicgen_large_master.wav")

scipy.io.wavfile.write(out_wav, rate=sampling_rate, data=full_audio)
print(f"\n[SUCCESS] Meta MusicGen Large 3.3B Master Action Soundtrack Generated!")
print(f"Output File: {out_wav} ({len(full_audio)/sampling_rate:.1f}s)")
