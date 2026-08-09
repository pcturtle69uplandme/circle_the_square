import sys
import torch
import scipy.io.wavfile
import numpy as np
import os

print("=== Meta MusicGen Medium (1.5B Parameter Studio Musician AI Model) ===")

try:
    from transformers import AutoProcessor, MusicgenForConditionalGeneration
    print("[1/4] Transformers & Audio Dependencies Loaded OK!")
except ImportError as e:
    print("[ERROR] Required libraries not found:", e)
    sys.exit(1)

device = "cpu"
print("[2/4] Loading Meta MusicGen Medium (facebook/musicgen-medium 1.5B Parameters)...")

processor = AutoProcessor.from_pretrained("facebook/musicgen-medium")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-medium").to(device)

print("[3/4] Model Loaded! Composing Non-Repeating Hollywood Cinematic Trailer Score...")

# Prompt engineered specifically for non-repeating evolving cinematic progression
prompt1 = (
    "A continuous evolving Hollywood action film score, non-repeating orchestral arrangement, "
    "low suspenseful cello pad, subtle metallic pulse, realistic studio instruments, "
    "cinematic atmosphere, Hans Zimmer style, pristine 32kHz production."
)

prompt2 = (
    "Hollywood blockbuster climax action soundtrack, soaring French horn melody, "
    "fast non-repeating staccato strings, explosive taiko drum rolls, heroic brass crescendo, "
    "dramatic cinematic finale, pristine studio master recording."
)

print("[4/4] Neural-synthesizing 2x 38-second studio music blocks...")

# Block 1 (38 seconds = 1900 tokens, well within 2048 context limit)
inputs1 = processor(text=[prompt1], padding=True, return_tensors="pt").to(device)
with torch.inference_mode():
    audio1 = model.generate(**inputs1, max_new_tokens=1900)

# Block 2 (38 seconds = 1900 tokens)
inputs2 = processor(text=[prompt2], padding=True, return_tensors="pt").to(device)
with torch.inference_mode():
    audio2 = model.generate(**inputs2, max_new_tokens=1900)

sampling_rate = model.config.audio_encoder.sampling_rate
a1 = audio1[0, 0].cpu().numpy().astype(float)
a2 = audio2[0, 0].cpu().numpy().astype(float)

# Seamless 2.0s crossfade between Block 1 and Block 2
fade_samples = int(sampling_rate * 2.0)
crossfade = np.linspace(0, 1, fade_samples)

a1_end = a1[:-fade_samples]
overlap = a1[-fade_samples:] * (1 - crossfade) + a2[:fade_samples] * crossfade
a2_start = a2[fade_samples:]

master_score = np.concatenate([a1_end, overlap, a2_start])

out_dir = r"C:\ai\Circle the Square\audio-refs"
os.makedirs(out_dir, exist_ok=True)
out_wav = os.path.join(out_dir, "studio_musician_ai_score.wav")

scipy.io.wavfile.write(out_wav, rate=sampling_rate, data=master_score)
print(f"\n[SUCCESS] Meta MusicGen Medium (1.5B) Studio Score Generated!")
print(f"Output File: {out_wav} ({len(master_score)/sampling_rate:.1f}s)")
