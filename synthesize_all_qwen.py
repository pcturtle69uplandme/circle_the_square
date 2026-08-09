import sys, os
from pathlib import Path
import torch
import soundfile as sf

# Add ComfyUI root and custom_nodes paths
comfy_root = Path(r"C:\ai\ComfyUI\ComfyUI")
comfy_node_dir = comfy_root / "custom_nodes" / "ComfyUI-QwenTTS"
sys.path.insert(0, str(comfy_root))
sys.path.insert(0, str(comfy_node_dir))
sys.path.insert(0, str(comfy_node_dir / "qwen_tts"))

# Import QwenTTS model loader
from AILab_QwenTTS import _load_qwen3_model, _ensure_qwen_package

_ensure_qwen_package()
Qwen3TTSModel = _load_qwen3_model()

if Qwen3TTSModel:
    model_dir = r"C:\ai\ComfyUI\ComfyUI\models\TTS\Qwen3-TTS\Qwen3-TTS-12Hz-1.7B-CustomVoice"
    out_dir = r"C:\kontitemp\ai\circle_the_square\audio-refs"
    
    print(f"Loading Qwen3-TTS CustomVoice model from {model_dir}...")
    model_wrapper = Qwen3TTSModel.from_pretrained(
        model_dir,
        dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="cuda" if torch.cuda.is_available() else "cpu"
    )
    print("Qwen3-TTS Model successfully loaded onto GPU!")

    tasks = [
        {
            'name': 'Christina Dross',
            'filename': 'christina_qwen_custom.wav',
            'speaker': 'Serena',
            'text': 'Well every two weeks on a Friday we do a breakfast meeting and offer some pastries loaded with as much sugar as humanly possible.'
        },
        {
            'name': 'Chris',
            'filename': 'chris_qwen_custom.wav',
            'speaker': 'Dylan',
            'text': 'You are dreaming Jan. Inception is the name of a film about dreams Jan.'
        },
        {
            'name': 'Rick',
            'filename': 'rick_qwen_custom.wav',
            'speaker': 'Uncle_Fu',
            'text': 'No relax, he will be out for a while. I think we need the police here.'
        }
    ]

    for t in tasks:
        filepath = os.path.join(out_dir, t['filename'])
        print(f"Synthesizing {t['name']} line: '{t['text']}'...")
        wavs, sr = model_wrapper.generate_custom_voice(text=t['text'], speaker=t['speaker'], language="english")
        sf.write(filepath, wavs[0], sr)
        print(f"Saved {t['name']} Qwen3-TTS Audio: {filepath} ({os.path.getsize(filepath)} bytes)")
