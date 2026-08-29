"""
Quick WAV → MP3 converter for existing generated files.
"""
import os
from pathlib import Path
from pydub import AudioSegment

audio_dir = Path(r"C:\AI\Circle the Square\audio-refs")
wavs = sorted(audio_dir.glob("*.wav"))
print(f"Found {len(wavs)} WAV files to convert...")

for wav_path in wavs:
    mp3_path = wav_path.with_suffix(".mp3")
    if mp3_path.exists():
        print(f"  SKIP {wav_path.name} (MP3 exists)")
        continue
    try:
        print(f"  Converting {wav_path.name}...", end=" ", flush=True)
        audio = AudioSegment.from_wav(str(wav_path))
        audio.export(str(mp3_path), format="mp3", bitrate="128k")
        wav_kb = wav_path.stat().st_size / 1024
        mp3_kb = mp3_path.stat().st_size / 1024
        print(f"WAV={wav_kb:.0f}KB -> MP3={mp3_kb:.0f}KB ({wav_kb/mp3_kb:.1f}x)")
        wav_path.unlink()
    except Exception as e:
        print(f"ERROR: {e}")

print("Done!")
