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

    text_sharon = "Well I have needs too Jan that must be met, mind."
    instruct_sharon = "gender: Female.\nage: 34 years old adult female.\npitch: Warm, melodic adult female voice.\nspeed: Relaxed, musical pacing.\nemotion: Unbothered, confident, transactional female speaker.\npersonality: Self-assured opportunist.\naccent: Musical Welsh female accent with a gentle Cardiff lilt."
    
    print(f"Synthesizing Sharon Enfield Welsh VoiceDesign line: '{text_sharon}'...")
    wavs_sharon, sr = model_wrapper.generate_voice_design(text=text_sharon, instruct=instruct_sharon, language="english")
    
    out_sharon = os.path.join(out_dir, "sharon_qwen_custom.wav")
    sf.write(out_sharon, wavs_sharon[0], sr)
    print(f"Saved Sharon Enfield Welsh Qwen3-TTS GPU Audio: {out_sharon} ({os.path.getsize(out_sharon)} bytes)")
