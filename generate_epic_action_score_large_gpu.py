import sys
import os
import torch
import scipy.io.wavfile
import numpy as np

print("=== Meta MusicGen Large (facebook/musicgen-large, 3.3B) — GPU Epic Score ===")

try:
    from transformers import AutoProcessor, MusicgenForConditionalGeneration
    print("[1/4] Transformers & Audio Dependencies Loaded OK!")
except ImportError as e:
    print("[ERROR] Required libraries not found:", e)
    sys.exit(1)

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[2/4] Device: {device} ({torch.cuda.get_device_name(0) if device == 'cuda' else 'CPU fallback'})")

model_dir = r"C:\ai\models\musicgen-large"
dtype = torch.float16 if device == "cuda" else torch.float32

processor = AutoProcessor.from_pretrained(model_dir)
model = MusicgenForConditionalGeneration.from_pretrained(model_dir, torch_dtype=dtype).to(device)

print("[3/4] Model Loaded! Composing 3-movement epic action trailer score (~80s, matches 77.9s master cut)...")

# Movement 1 (~24s): Acts I - The Deceptive Calm (S01-S03, ominous drone architecture)
prompt1 = (
    "Ominous cinematic trailer intro, slow evolving orchestral drone, deep sub-bass hum, "
    "metallic ticking clock pulse, distant low brass swell building tension, dark atmospheric "
    "Hans Zimmer style corporate thriller score, pristine 32kHz studio master recording."
)

# Movement 2 (~40s): Acts II-III - Executive speech into whistleblower montage (S04-S07)
prompt2 = (
    "Escalating Hollywood trailer soundtrack, rising suspenseful strings, non-repeating staccato "
    "violin ostinato, pulsing low brass hits, heartbeat percussion accelerating, corporate conspiracy "
    "thriller tension building to a breaking point, dramatic evolving orchestral progression, "
    "pristine studio master recording."
)

# Movement 3 (~20s): Acts IV-V - Meltdown climax, BRAAM stings, title stinger (S08-S09 + title card)
prompt3 = (
    "Epic Hollywood blockbuster climax action soundtrack, heavy cinematic BRAAM low-frequency "
    "impact hits, explosive taiko drum rolls, soaring heroic French horn and brass crescendo, "
    "fast non-repeating staccato strings, dramatic action movie finale swell resolving into a "
    "final metallic impact sting, pristine studio master recording."
)

print("[4/4] Neural-synthesizing 3 studio music movements...")

def synth(prompt, seconds, label):
    tokens = int(seconds * 50)
    print(f"  -> {label}: {seconds}s ({tokens} tokens)")
    inputs = processor(text=[prompt], padding=True, return_tensors="pt").to(device)
    with torch.inference_mode():
        audio = model.generate(**inputs, max_new_tokens=tokens)
    return audio[0, 0].to(torch.float32).cpu().numpy()

a1 = synth(prompt1, 24, "Movement 1 (Calm/Ominous)")
a2 = synth(prompt2, 39, "Movement 2 (Rising Tension)")
a3 = synth(prompt3, 20, "Movement 3 (Climax/Title)")

sampling_rate = model.config.audio_encoder.sampling_rate

def crossfade(a, b, seconds=2.0):
    n = int(sampling_rate * seconds)
    ramp = np.linspace(0, 1, n)
    a_end, a_body = a[-n:], a[:-n]
    b_start, b_body = b[:n], b[n:]
    overlap = a_end * (1 - ramp) + b_start * ramp
    return np.concatenate([a_body, overlap, b_body])

merged = crossfade(a1, a2, 2.0)
merged = crossfade(merged, a3, 2.0)

out_dir = r"C:\ai\Circle the Square\audio-refs"
os.makedirs(out_dir, exist_ok=True)
out_wav = os.path.join(out_dir, "musicgen_large_neural_score.wav")

scipy.io.wavfile.write(out_wav, rate=sampling_rate, data=merged)
print(f"\n[MASTER SUCCESS] Meta MusicGen Large (3.3B) Epic Action Score Generated!")
print(f"Output File: {out_wav} ({len(merged)/sampling_rate:.1f}s)")
