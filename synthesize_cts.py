"""
Circle the Square — Qwen3-TTS Synthesis Script
Generates MP3 voice files for all 5 principal characters.
Uses CustomVoice presets where available, VoiceDesign for instruct-based voices.

Outputs to: C:\AI\Circle the Square\audio-refs\
Naming:  {character}_{index}.mp3  e.g. jan_01.mp3, christina_01.mp3
"""

import sys, os
from pathlib import Path
import torch
import soundfile as sf
import numpy as np

# Force UTF-8 stdout so Unicode prints work in Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ── ComfyUI paths ────────────────────────────────────────────────────────────
COMFY_ROOT   = Path(r"C:\ai\ComfyUI\ComfyUI")
COMFY_NODES  = COMFY_ROOT / "custom_nodes" / "ComfyUI-QwenTTS"
QwenTTS_DIR  = COMFY_NODES / "qwen_tts"

# Must chdir to ComfyUI root so 'comfy' package resolves
os.chdir(str(COMFY_ROOT))

for _p in [str(COMFY_ROOT), str(COMFY_NODES), str(QwenTTS_DIR)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from AILab_QwenTTS import _load_qwen3_model, _ensure_qwen_package

# ── Output ─────────────────────────────────────────────────────────────────────
OUT_DIR = Path(r"C:\AI\Circle the Square\audio-refs")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Helpers ───────────────────────────────────────────────────────────────────

def wav_to_mp3(wav_path: Path, mp3_path: Path, bitrate: str = "128k"):
    """Convert a WAV file to MP3 using pydub."""
    from pydub import AudioSegment
    audio = AudioSegment.from_wav(str(wav_path))
    audio.export(str(mp3_path), format="mp3", bitrate=bitrate)
    wav_size = wav_path.stat().st_size
    mp3_size = mp3_path.stat().st_size
    ratio = wav_size / mp3_size if mp3_size > 0 else 0
    print(f"  WAV: {wav_size/1024:.1f} KB -> MP3: {mp3_size/1024:.1f} KB  ({ratio:.1f}x smaller)")


def synthesize_customvoice(model_class, speaker: str, text: str, out_path: Path):
    """Load CustomVoice model, generate, save as WAV then MP3."""
    model_dir = COMFY_ROOT / "models" / "TTS" / "Qwen3-TTS" / "Qwen3-TTS-12Hz-1.7B-CustomVoice"
    print(f"  Loading CustomVoice model from {model_dir}...")
    model = model_class.from_pretrained(
        str(model_dir),
        dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="cuda" if torch.cuda.is_available() else "cpu",
    )
    print(f"  Synthesizing: '{text[:60]}...'")
    wavs, sr = model.generate_custom_voice(text=text, speaker=speaker, language="english")
    wav_path = out_path.with_suffix(".wav")
    sf.write(str(wav_path), wavs[0], sr)
    wav_to_mp3(wav_path, out_path)
    wav_path.unlink(missing_ok=True)  # clean up WAV
    # Free GPU
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def synthesize_voicedesign(model_class, instruct: str, text: str, out_path: Path):
    """Load VoiceDesign model, generate, save as WAV then MP3."""
    model_dir = COMFY_ROOT / "models" / "TTS" / "Qwen3-TTS" / "Qwen3-TTS-12Hz-1.7B-VoiceDesign"
    print(f"  Loading VoiceDesign model from {model_dir}...")
    model = model_class.from_pretrained(
        str(model_dir),
        dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="cuda" if torch.cuda.is_available() else "cpu",
    )
    print(f"  Synthesizing: '{text[:60]}...'")
    wavs, sr = model.generate_voice_design(text=text, instruct=instruct, language="english")
    wav_path = out_path.with_suffix(".wav")
    sf.write(str(wav_path), wavs[0], sr)
    wav_to_mp3(wav_path, out_path)
    wav_path.unlink(missing_ok=True)  # clean up WAV
    # Free GPU
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


# ── Character roster ─────────────────────────────────────────────────────────
# Preset speakers:  Aiden, Dylan, Eric, Ono_Anna, Ryan, Serena, Sohee, Uncle_Fu, Vivian
# CustomVoice (preset):  Jan=Ryan, Christina=Serena, Chris=Dylan, Rick=Uncle_Fu, Sharon=Vivian
# VoiceDesign (instruct):  Maureen=Maureen_voice, Priya=Priya_voice, Barbara=Barbara_voice, Dev=Dev_voice, Tomasz=Tomasz_voice

VOICES = [
    # ── Jan Peach (CEO, pompous tyrant) ──────────────────────────────────────
    {
        "character": "jan",
        "speaker": "Ryan",          # CustomVoice preset
        "instruct": None,
        "lines": [
            "Barely. Another day dealing with these morons at the office.",
            "I'm listening.",
            "This is exactly the kind of strategic thinking that separates the leaders from the followers.",
            "Great. Make it so.",
            "You never seen Star Trek Next Generation?",
            "Fine, just make it happen. No more interruptions.",
            "Jesus! Everyone thinks they know better than me! I am the one with the MBA from the University of —",
            "GET OUT NOW YOU STUPID COW! JUST GET THAT DAMN MEETING ORGANISED!",
            "BLOODY HELL SHARON. KNOCK ON THE DOOR WILL YOU!",
            "I really don't have time for this now Sharon...",
        ],
    },
    # ── Christina Dross (Comms Lead, dry strategist) ─────────────────────────
    {
        "character": "christina",
        "speaker": "Serena",         # CustomVoice preset
        "instruct": None,
        "lines": [
            "Morning Jan. Survive the weekend?",
            "I see. Well, I might be able to help...",
            "Well every two weeks on a Friday we do a breakfast meeting and offer some pastries loaded with as much sugar as humanly possible.",
            "Thought you would like it...",
            "Is this another one of your poorly rehearsed presentations?",
            "Made Up Place?",
            "Oh I see, the whiteboard. How terribly innovative.",
            "Jan, I have a rather more immediate concern...",
            "The police will probably want to take a statement.",
        ],
    },
    # ── Sharon Enfield (Staff, unbothered opportunist) ───────────────────────
    {
        "character": "sharon",
        "speaker": "Vivian",         # CustomVoice preset
        "instruct": None,
        "lines": [
            "Och, well I have needs too Jan that must be met.",
            "I hear Christina is doing breakfast meetings now.",
            "Jan, I was just wondering if you had a moment.",
            "Well, I'm not saying anything, but the blinds are quite dramatic tonight.",
            "Door locks itself when it wants to.",
        ],
    },
    # ── Chris (Staff, workplace smart-mouth) ─────────────────────────────────
    {
        "character": "chris",
        "speaker": "Dylan",          # CustomVoice preset
        "instruct": None,
        "lines": [
            "You are dreaming Jan. Inception is the name of a film about dreams Jan.",
            "Is that a whiteboard in your office? I can see it from here.",
            "Christina mentioned something about breakfast pastries. You know I can't resist.",
            "No, no, I just came to ask about the fire safety procedures. That's all.",
        ],
    },
    # ── Rick (Staff, blunt realist) ─────────────────────────────────────────
    {
        "character": "rick",
        "speaker": "Uncle_Fu",       # CustomVoice preset
        "instruct": None,
        "lines": [
            "No relax, he will be out for a while. I think we need the police here.",
            "The blinds slammed shut on their own. I saw it happen.",
            "Just doing my rounds. Everything is under control.",
        ],
    },
    # ── Maureen (Canteen, warm East Anglian) ────────────────────────────────
    {
        "character": "maureen",
        "speaker": None,
        "instruct": (
            "pitch: Medium, warm, slightly husky.\n"
            "speed: Steady, unhurried.\n"
            "emotion: Kind, maternal, no-nonsense.\n"
            "personality: Reliable, good-humoured caretaker.\n"
            "accent: East Anglian (Norfolk/Cambridge region)."
        ),
        "lines": [
            "Breakfast is served in the main hall at eight, dear. Don't be late.",
            "I've laid on an extra tray. Looks like it's going to be a busy one.",
        ],
    },
    # ── Gemma Ashcroft (Reception, professional) ─────────────────────────────
    {
        "character": "gemma",
        "speaker": None,
        "instruct": (
            "pitch: Clear, mid-range, pleasant.\n"
            "speed: Moderate, efficient.\n"
            "emotion: Polite, attentive.\n"
            "personality: Organised, welcoming.\n"
            "accent: Standard Southern English."
        ),
        "lines": [
            "Jan, there's a call for you on line two. Says it's urgent.",
            "The visitor from PRISM is waiting in reception.",
        ],
    },
    # ── Priya Raghavan (Staff) ───────────────────────────────────────────────
    {
        "character": "priya",
        "speaker": None,
        "instruct": (
            "pitch: Warm, melodic, mid-range.\n"
            "speed: Measured, thoughtful.\n"
            "emotion: Calm, observant.\n"
            "personality: Quietly confident, analytical.\n"
            "accent: Received Southern British with subtle Indian influence."
        ),
        "lines": [
            "I think there may have been some miscommunication about the agenda.",
            "The data from last quarter is in the shared drive if you need it.",
        ],
    },
    # ── Barbara Whitlock (Staff, older) ──────────────────────────────────────
    {
        "character": "barbara",
        "speaker": None,
        "instruct": (
            "pitch: Low, measured, dignified.\n"
            "speed: Slow, deliberate.\n"
            "emotion: Dry wit, unflappable.\n"
            "personality: Experienced, sardonic observer.\n"
            "accent: RP with faint Midlands undertone."
        ),
        "lines": [
            "I've seen a few reorganisations in my time, Jan. This one feels familiar.",
            "Would you like me to book the conference room for later?",
        ],
    },
    # ── Dev Osei (Staff) ──────────────────────────────────────────────────────
    {
        "character": "dev",
        "speaker": None,
        "instruct": (
            "pitch: Deep, resonant, confident baritone.\n"
            "speed: Even, deliberate.\n"
            "emotion: Composed, direct.\n"
            "personality: Steady, reliable.\n"
            "accent: British West African / RP blend."
        ),
        "lines": [
            "I've run the diagnostics. The server is stable for now.",
            "If you need the file transferred, I can handle that.",
        ],
    },
    # ── Tomasz Wojcik (Staff, taller) ───────────────────────────────────────
    {
        "character": "tomasz",
        "speaker": None,
        "instruct": (
            "pitch: Mid-range, slightly gruff.\n"
            "speed: Slow to measured.\n"
            "emotion: Practical, no fuss.\n"
            "personality: Straightforward, physically imposing.\n"
            "accent: East European English (Polish influence)."
        ),
        "lines": [
            "The delivery came. I put it in the store room.",
            "If you need a hand with anything heavy, just say.",
        ],
    },
]

# ── Main ──────────────────────────────────────────────────────────────────────
_ensure_qwen_package()
ModelClass = _load_qwen3_model()
if ModelClass is None:
    print("ERROR: Could not load Qwen3-TTS model. Check AILab_QwenTTS installation.")
    sys.exit(1)

total_files = 0
total_errors = 0
for voice in VOICES:
    character = voice["character"]
    speaker   = voice["speaker"]
    instruct  = voice["instruct"]
    lines     = voice["lines"]

    print(f"\n{'='*60}")
    print(f"Character: {character.upper()}")
    print(f"  Mode: {'CustomVoice (' + speaker + ')' if speaker else 'VoiceDesign'}")
    print(f"  Lines: {len(lines)}")

    for i, line in enumerate(lines, start=1):
        idx    = str(i).zfill(2)
        out_path = OUT_DIR / f"{character}_{idx}.mp3"

        if out_path.exists():
            size_kb = out_path.stat().st_size / 1024
            print(f"  [SKIP] {out_path.name} ({size_kb:.1f} KB, already exists)")
            total_files += 1
            continue

        print(f"\n  [{idx}/{len(lines)}] {out_path.name}")
        try:
            if speaker:
                synthesize_customvoice(ModelClass, speaker, line, out_path)
            else:
                synthesize_voicedesign(ModelClass, instruct, line, out_path)
            total_files += 1
            print(f"  ✓ {out_path.name} ({out_path.stat().st_size/1024:.1f} KB)")
        except Exception as e:
            import traceback
            total_errors += 1
            print(f"  ERROR: {e}")
            traceback.print_exc()
            # clean up partial file
            if out_path.exists():
                out_path.unlink(missing_ok=True)

print(f"\n{'='*60}")
print(f"Done. {total_files} MP3 files generated, {total_errors} errors.")
print(f"  Output: {OUT_DIR}")
