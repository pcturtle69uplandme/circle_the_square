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
    "Upbeat cheerful corporate acoustic guitar, bright marimba melody, "
    "acoustic ukulele rhythm, cheerful British workplace comedy theme music, "
    "clean studio production, 120 bpm, joyful outro."
)

print("Generating 40-second studio-quality AI music track on CPU...")

inputs = processor(
    text=[prompt],
    padding=True,
    return_tensors="pt",
).to("cpu")

with torch.inference_mode():
    audio_values = model.generate(**inputs, max_new_tokens=2000)

sampling_rate = model.config.audio_encoder.sampling_rate
audio_data = audio_values[0, 0].cpu().numpy().astype(float)

out_dir = r"C:\ai\Circle the Square\audio-refs"
os.makedirs(out_dir, exist_ok=True)
out_wav = os.path.join(out_dir, "ai_musicgen_soundtrack.wav")

scipy.io.wavfile.write(out_wav, rate=sampling_rate, data=audio_data)
print(f"[SUCCESS] Generated 40s Meta MusicGen AI soundtrack ({len(audio_data)/sampling_rate:.1f}s) -> {out_wav}")
