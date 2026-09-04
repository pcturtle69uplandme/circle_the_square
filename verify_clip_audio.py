"""Verify a generated clip actually SPEAKS its scripted lines, by transcribing it.

    python verify_clip_audio.py scene2-clips/c01_corridor_gossip.mp4
    python verify_clip_audio.py --all scene2-clips

Why this exists: a clip can have a perfectly healthy AAC stream and still say nothing
intelligible. Checking that the container has audio proves only that the model emitted
sound -- and MiniMax H3's dialogue is unreliable (SCENE1_MINIMAX_TRACKER row 1 records an
H3 take with "unusable audio"). Scene 1 validated its audio by Whisper transcription and
comparing against the scripted line; this restores that step for Scene 2.

Prints the transcript plus a word-overlap score against the expected dialogue pulled from
the clip definitions, so "the audio is nonsense" becomes a measurement rather than an
impression.
"""
import json
import os
import re
import subprocess
import sys

import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
BASE = os.path.dirname(os.path.abspath(__file__))


def expected_lines(slug):
    """Pull the quoted dialogue for a clip out of the JS definitions."""
    for rel in ('fal-tools/browser/scene2_clips.js', 'higgsfield-tools/browser/scene3_clips.js'):
        path = os.path.join(BASE, rel)
        if not os.path.exists(path):
            continue
        src = open(path, encoding='utf-8').read()
        i = src.find(f'  {slug}: {{')
        if i < 0:
            continue
        block = src[i:src.find('\n  },', i)]
        # Only the DIALOGUE segment holds spoken words. Taking every quoted string also
        # scooped up the TIMING and AUDIO stage directions, which are instructions to the
        # model and are never spoken aloud -- that scored a verbatim-correct take at 32%
        # and reported it as failing.
        out = []
        for seg in re.findall(r'DIALOGUE:(.*?)(?:AUDIO:|TIMING:|CRITICAL|$)', block, re.S):
            out += re.findall(r'"([^"]{4,})"', seg)
        return out
    return []


def transcribe(path):
    from faster_whisper import WhisperModel
    wav = os.path.join(BASE, '_audio_qa.wav')
    subprocess.run([FFMPEG, '-y', '-i', path, '-vn', '-ac', '1', '-ar', '16000', wav],
                   capture_output=True)
    model = WhisperModel('base.en', device='cpu', compute_type='int8')
    segments, _ = model.transcribe(wav, beam_size=5)
    text = ' '.join(s.text.strip() for s in segments).strip()
    try:
        os.remove(wav)
    except OSError:
        pass
    return text


def score(said, expected):
    """Fraction of the expected words that actually appear in the transcript."""
    norm = lambda s: set(re.findall(r"[a-z']+", s.lower()))
    want = norm(' '.join(expected))
    got = norm(said)
    if not want:
        return None
    return len(want & got) / len(want)


def check(path):
    slug = os.path.splitext(os.path.basename(path))[0]
    exp = expected_lines(slug)
    said = transcribe(path)

    print(f'\n=== {slug} ===')
    print(f'  heard   : {said[:300] or "(nothing intelligible)"}')
    if exp:
        print(f'  expected: {" / ".join(l[:70] for l in exp[:3])}')
        s = score(said, exp)
        verdict = 'PASS' if s >= 0.6 else ('PARTIAL' if s >= 0.3 else 'FAIL')
        print(f'  overlap : {s:.0%}  -> {verdict}')
        return {'slug': slug, 'heard': said, 'overlap': s, 'verdict': verdict}
    print('  (no scripted dialogue found for this slug)')
    return {'slug': slug, 'heard': said, 'overlap': None, 'verdict': 'NO-SCRIPT'}


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--all']
    targets = []
    for a in args:
        if os.path.isdir(a):
            targets += [os.path.join(a, f) for f in sorted(os.listdir(a)) if f.endswith('.mp4')]
        else:
            targets.append(a)
    if not targets:
        sys.exit('usage: verify_clip_audio.py <clip.mp4 | dir> [...]')

    results = [check(t) for t in targets]
    bad = [r for r in results if r['verdict'] in ('FAIL', 'PARTIAL')]
    print(f'\n{len(results) - len(bad)}/{len(results)} clip(s) spoke their lines')
    if bad:
        print('needs attention: ' + ', '.join(r['slug'] for r in bad))
