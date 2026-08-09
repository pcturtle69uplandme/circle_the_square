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
    
    print(f"Loading Qwen3-TTS CustomVoice model from {model_dir}...")
    model_wrapper = Qwen3TTSModel.from_pretrained(
        model_dir,
        dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="cuda" if torch.cuda.is_available() else "cpu"
    )
    print("Qwen3-TTS Model successfully loaded onto GPU!")

    # 1. Synthesize Jan Peach using preset 'Ryan'
    text_jan = "Great. Make it so. GET OUT NOW YOU STUPID COW! JUST GET THAT DAMN MEETING ORGANISED!"
    print(f"Synthesizing Jan line: '{text_jan}'...")
    wavs_jan, sr = model_wrapper.generate_custom_voice(text=text_jan, speaker="Ryan", language="english")
    
    out_jan = r"C:\kontitemp\ai\circle_the_square\audio-refs\jan_qwen_custom.wav"
    sf.write(out_jan, wavs_jan[0], sr)
    print(f"Saved Jan Qwen3-TTS Audio: {out_jan} ({os.path.getsize(out_jan)} bytes)")

    # 2. Synthesize Sharon Enfield using preset 'Vivian'
    text_sharon = "Och, well I have needs too Jan that must be met."
    print(f"Synthesizing Sharon line: '{text_sharon}'...")
    wavs_sharon, sr = model_wrapper.generate_custom_voice(text=text_sharon, speaker="Vivian", language="english")
    
    out_sharon = r"C:\kontitemp\ai\circle_the_square\audio-refs\sharon_qwen_custom.wav"
    sf.write(out_sharon, wavs_sharon[0], sr)
    print(f"Saved Sharon Qwen3-TTS Audio: {out_sharon} ({os.path.getsize(out_sharon)} bytes)")
