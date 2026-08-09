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
    # Use VoiceDesign model for exact text-instructed British female voice
    model_dir = r"C:\ai\ComfyUI\ComfyUI\models\TTS\Qwen3-TTS\Qwen3-TTS-12Hz-1.7B-VoiceDesign"
    out_dir = r"C:\kontitemp\ai\circle_the_square\audio-refs"
    
    print(f"Loading Qwen3-TTS VoiceDesign model from {model_dir}...")
    model_wrapper = Qwen3TTSModel.from_pretrained(
        model_dir,
        dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="cuda" if torch.cuda.is_available() else "cpu"
    )

    text_christina = "Well every two weeks on a Friday we do a breakfast meeting and offer some pastries loaded with as much sugar as humanly possible."
    instruct_christina = "A 38-year-old crisp British female corporate strategist with a low-to-mid alto voice. Speaks with a clear, measured, unhurried Received Pronunciation London accent, delivering sarcastic lines with level precision."
    
    print(f"Synthesizing Christina Dross VoiceDesign line: '{text_christina}'...")
    wavs_christina, sr = model_wrapper.generate_voice_design(text=text_christina, instruct=instruct_christina, language="english")
    
    out_christina = os.path.join(out_dir, "christina_qwen_custom.wav")
    sf.write(out_christina, wavs_christina[0], sr)
    print(f"Saved Christina Dross Qwen3-TTS GPU Audio: {out_christina} ({os.path.getsize(out_christina)} bytes)")
