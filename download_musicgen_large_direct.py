import sys
import os
import torch
import scipy.io.wavfile
import numpy as np

print("=== Direct Download Meta MusicGen Large (facebook/musicgen-large 3.3B) ===")

try:
    from transformers import AutoProcessor, MusicgenForConditionalGeneration
    from huggingface_hub import snapshot_download
    print("[1/4] Transformers & HuggingFace Hub Loaded OK!")
except ImportError as e:
    print("[ERROR] Required libraries not found:", e)
    sys.exit(1)

model_dir = r"C:\ai\models\musicgen-large"
os.makedirs(model_dir, exist_ok=True)

print(f"[2/4] Downloading Meta MusicGen Large (3.3B) directly to local folder:\n  -> {model_dir}")

snapshot_download(
    repo_id="facebook/musicgen-large",
    local_dir=model_dir,
    local_dir_use_symlinks=False
)

print(f"\n[3/4] Successfully downloaded 3.3B model! Loading from {model_dir}...")
device = "cpu"
processor = AutoProcessor.from_pretrained(model_dir)
model = MusicgenForConditionalGeneration.from_pretrained(model_dir).to(device)

print("[4/4] 3.3B Model Loaded! Generating 2x 38s Non-Repeating Neural AI Score...")

prompt1 = (
    "A dramatic evolving Hollywood film trailer soundtrack, non-repeating orchestral score, "
    "low suspenseful cello texture, subtle brass swell, natural studio acoustics, "
    "Hans Zimmer style, pristine 32kHz master recording."
)

prompt2 = (
    "Epic Hollywood blockbuster climax action soundtrack part 2, heroic French horn lead motif, "
    "fast non-repeating staccato violins, explosive taiko drum rolls, dramatic brass crescendo, "
    "heroic orchestral finale, pristine studio master recording."
)

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
out_wav = os.path.join(out_dir, "musicgen_large_neural_score.wav")

scipy.io.wavfile.write(out_wav, rate=sampling_rate, data=master_score)
print(f"\n[MASTER SUCCESS] Meta MusicGen Large (3.3B) Neural AI Score Generated!")
print(f"Output File: {out_wav} ({len(master_score)/sampling_rate:.1f}s)")
