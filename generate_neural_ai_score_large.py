import sys
import torch
import scipy.io.wavfile
import numpy as np
import os

print("=== Running Meta MusicGen Neural AI Musician (facebook/musicgen-small) ===")

try:
    from transformers import AutoProcessor, MusicgenForConditionalGeneration
    print("[1/4] Transformers and Audio Dependencies Loaded OK!")
except ImportError as e:
    print("[ERROR] Required libraries not found:", e)
    sys.exit(1)

device = "cpu"
model_id = "facebook/musicgen-small"
print(f"[2/4] Loading Meta MusicGen Neural AI model ({model_id})...")

processor = AutoProcessor.from_pretrained(model_id)
model = MusicgenForConditionalGeneration.from_pretrained(model_id).to(device)

print("[3/4] Model Loaded! Composing Non-Repeating Hollywood Cinematic Score...")

# Neural AI prompts engineered for organic, non-repeating film score progression
prompt1 = (
    "A continuous evolving Hollywood action film trailer soundtrack, non-repeating orchestral score, "
    "low suspenseful cello texture, subtle brass swell, natural studio acoustics, "
    "Hans Zimmer style, pristine 32kHz master recording."
)

prompt2 = (
    "Epic Hollywood blockbuster climax action soundtrack part 2, heroic French horn lead motif, "
    "fast non-repeating staccato violins, explosive taiko drum rolls, dramatic brass crescendo, "
    "heroic orchestral finale, pristine studio master recording."
)

print("[4/4] Neural-synthesizing 2x 38-second studio music blocks...")

# Block 1 (38 seconds = 1900 tokens)
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
out_wav = os.path.join(out_dir, "musicgen_neural_score_master.wav")

scipy.io.wavfile.write(out_wav, rate=sampling_rate, data=master_score)
print(f"\n[SUCCESS] Meta MusicGen Neural AI Studio Score Generated!")
print(f"Output File: {out_wav} ({len(master_score)/sampling_rate:.1f}s)")
