import sys
import torch
import scipy.io.wavfile
import os

try:
    from transformers import AutoProcessor, MusicgenForConditionalGeneration
    print("MusicGen import OK!")
except ImportError as e:
    print("Import error:", e)
    sys.exit(1)

print("Loading Meta MusicGen model (facebook/musicgen-small) on CPU...")
processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small").to("cpu")

prompt = (
    "High intensity Hollywood action movie trailer soundtrack, "
    "fast orchestral brass braam stings, driving taiko drum percussion, "
    "suspenseful cinematic strings, 135 bpm, epic action blockbuster pulse, "
    "clean studio production, powerful bass drop climax."
)

print("Generating 60-second epic AI action trailer soundtrack on CPU...")

# Generate 60 seconds of music (60 * 50 = 3000 tokens)
inputs = processor(
    text=[prompt],
    padding=True,
    return_tensors="pt",
).to("cpu")

with torch.inference_mode():
    audio_values = model.generate(**inputs, max_new_tokens=3000)

sampling_rate = model.config.audio_encoder.sampling_rate
audio_data = audio_values[0, 0].cpu().numpy().astype(float)

out_dir = r"C:\ai\Circle the Square\audio-refs"
os.makedirs(out_dir, exist_ok=True)
out_wav = os.path.join(out_dir, "action_musicgen_epic.wav")

scipy.io.wavfile.write(out_wav, rate=sampling_rate, data=audio_data)
print(f"[SUCCESS] Generated 60s Epic Action AI MusicGen soundtrack ({len(audio_data)/sampling_rate:.1f}s) -> {out_wav}")
