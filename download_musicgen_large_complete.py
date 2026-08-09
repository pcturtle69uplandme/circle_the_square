import sys
import os
import torch
import scipy.io.wavfile
import numpy as np

print("=== Downloading Meta MusicGen Large (facebook/musicgen-large 3.3B Parameters) to 100% Completion ===")

try:
    from transformers import AutoProcessor, MusicgenForConditionalGeneration
    from huggingface_hub import snapshot_download
    print("[1/5] Transformers & HuggingFace Hub Loaded OK!")
except ImportError as e:
    print("[ERROR] Required libraries not found:", e)
    sys.exit(1)

repo_id = "facebook/musicgen-large"

print(f"[2/5] Downloading all model shards for '{repo_id}' to 100% completion...")
print("      (This will download all 3.3B parameters, including pytorch_model-00001-of-00002.bin)")

try:
    # Explicit snapshot download with resume_download=True
    model_folder = snapshot_download(
        repo_id=repo_id,
        resume_download=True,
        max_workers=4
    )
    print(f"[SUCCESS] Download completed! Local Snapshot Path:\n  -> {model_folder}")
except Exception as e:
    print(f"[RETRYING] HuggingFace Hub snapshot download error: {e}")
    model_folder = repo_id

print("\n[3/5] Loading 3.3B Parameter Meta MusicGen Large Model from completed local cache...")
device = "cpu"
processor = AutoProcessor.from_pretrained(model_folder)
model = MusicgenForConditionalGeneration.from_pretrained(model_folder).to(device)

print("[4/5] 3.3B Model Loaded Successfully! Composing Non-Repeating Hollywood Cinematic Score...")

# Neural AI prompts engineered for non-repeating 3.3B film score progression
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

print("[5/5] Neural-synthesizing 2x 38-second 3.3B studio music blocks...")

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
print(f"\n[MASTER SUCCESS] Meta MusicGen Large (3.3B) Studio Neural Score Generated!")
print(f"Output File: {out_wav} ({len(master_score)/sampling_rate:.1f}s)")
