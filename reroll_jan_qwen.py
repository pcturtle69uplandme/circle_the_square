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

from AILab_QwenTTS import _load_qwen3_model, _ensure_qwen_package

_ensure_qwen_package()
Qwen3TTSModel = _load_qwen3_model()

if Qwen3TTSModel:
    model_dir = r"C:\ai\ComfyUI\ComfyUI\models\TTS\Qwen3-TTS\Qwen3-TTS-12Hz-1.7B-CustomVoice"
    out_dir = r"C:\ai\Circle the Square\audio-refs"
    
    print(f"Loading Qwen3-TTS CustomVoice model from {model_dir}...")
    model_wrapper = Qwen3TTSModel.from_pretrained(
        model_dir,
        dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="cuda" if torch.cuda.is_available() else "cpu"
    )

    text_jan = "Great. Make it so. GET OUT NOW YOU STUPID COW! JUST GET THAT DAMN MEETING ORGANISED!"
    print(f"Synthesizing older Jan Peach line: '{text_jan}'...")
    wavs_jan, sr = model_wrapper.generate_custom_voice(text=text_jan, speaker="Uncle_Fu", language="english")
    
    out_jan = os.path.join(out_dir, "jan_qwen_custom.wav")
    sf.write(out_jan, wavs_jan[0], sr)
    print(f"Saved Older Jan Qwen3-TTS GPU Audio: {out_jan} ({os.path.getsize(out_jan)} bytes)")
