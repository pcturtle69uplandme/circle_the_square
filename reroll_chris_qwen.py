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
    model_dir = r"C:\ai\ComfyUI\ComfyUI\models\TTS\Qwen3-TTS\Qwen3-TTS-12Hz-1.7B-VoiceDesign"
    out_dir = r"C:\ai\Circle the Square\audio-refs"
    
    print(f"Loading Qwen3-TTS VoiceDesign model from {model_dir}...")
    model_wrapper = Qwen3TTSModel.from_pretrained(
        model_dir,
        dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="cuda" if torch.cuda.is_available() else "cpu"
    )

    text_chris = "You are dreaming Jan. Inception is the name of a film about dreams Jan."
    instruct_chris = "gender: Male.\nage: 32 years old young adult male.\npitch: Conversational British baritone voice.\nspeed: Quick-witted, casual, sharp pacing.\nemotion: Sarcastic, deadpan, amused male speaker.\npersonality: Office smart-mouth and comic relief.\naccent: Dry South London Estuary British accent."
    
    print(f"Synthesizing Chris 32-Yr-Old Male VoiceDesign line: '{text_chris}'...")
    wavs_chris, sr = model_wrapper.generate_voice_design(text=text_chris, instruct=instruct_chris, language="english")
    
    out_chris = os.path.join(out_dir, "chris_qwen_custom.wav")
    sf.write(out_chris, wavs_chris[0], sr)
    print(f"Saved Chris 32-Yr-Old Qwen3-TTS GPU Audio: {out_chris} ({os.path.getsize(out_chris)} bytes)")
