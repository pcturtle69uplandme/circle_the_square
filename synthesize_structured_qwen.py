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
    print("Qwen3-TTS VoiceDesign Model successfully loaded onto GPU!")

    characters = [
        {
            'name': 'Jan Peach (CEO)',
            'filename': 'jan_qwen_custom.wav',
            'instruct': 'pitch: High, sharp, strained tenor.\nspeed: Fast, erratic, anxious.\nemotion: Hysterical, pompous, angry.\npersonality: Arrogant, thin-skinned corporate tyrant.\naccent: British Received Pronunciation (RP).',
            'text': 'Great. Make it so. GET OUT NOW YOU STUPID COW! JUST GET THAT DAMN MEETING ORGANISED!'
        },
        {
            'name': 'Christina Dross (Comms Lead)',
            'filename': 'christina_qwen_custom.wav',
            'instruct': 'pitch: Low-to-mid, crisp, level alto.\nspeed: Measured, unhurried, steady.\nemotion: Cold, deadpan, calm.\npersonality: Dry, calculating corporate strategist.\naccent: Clear British London RP.',
            'text': 'Well every two weeks on a Friday we do a breakfast meeting and offer some pastries loaded with as much sugar as humanly possible.'
        },
        {
            'name': 'Sharon Enfield (Staff)',
            'filename': 'sharon_qwen_custom.wav',
            'instruct': 'pitch: Warm, confident, grounded adult female.\nspeed: Casual, relaxed.\nemotion: Unbothered, amused, transactional.\npersonality: Self-assured opportunist.\naccent: Scottish (West Coast / Edinburgh).',
            'text': 'Och, well I have needs too Jan that must be met.'
        },
        {
            'name': 'Chris (Staff)',
            'filename': 'chris_qwen_custom.wav',
            'instruct': 'pitch: Bright, conversational baritone.\nspeed: Quick-witted, rising punchlines.\nemotion: Sarcastic, amused.\npersonality: Designated workplace smart-mouth.\naccent: South London / Estuary.',
            'text': 'You are dreaming Jan. Inception is the name of a film about dreams Jan.'
        },
        {
            'name': 'Rick (Staff)',
            'filename': 'rick_qwen_custom.wav',
            'instruct': 'pitch: Deep, gravelly bass-baritone.\nspeed: Slow, deliberate monotone.\nemotion: Flat, unhurried.\npersonality: Blunt realist, unblinking Taser operator.\naccent: Flat Midlands / East Anglian.',
            'text': 'No relax, he will be out for a while. I think we need the police here.'
        }
    ]

    for c in characters:
        filepath = os.path.join(out_dir, c['filename'])
        print(f"\nSynthesizing {c['name']} using Qwen3-TTS VoiceDesign...")
        wavs, sr = model_wrapper.generate_voice_design(text=c['text'], instruct=c['instruct'], language="english")
        sf.write(filepath, wavs[0], sr)
        print(f"Saved {c['name']} Audio: {filepath} ({os.path.getsize(filepath)} bytes)")
