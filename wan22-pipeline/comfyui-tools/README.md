# ComfyUI-based tools: H3-FaceRefine and TTS+lip-sync (2026-08-26)

Everything in this doc lives partly outside this git repo (in `C:\AI\ComfyUI\ComfyUI\`,
machine-specific). This file exists so the setup isn't lost if that install is ever reset —
it took a genuinely large amount of environment work to get both of these running, and none
of it is captured by git.

## What's here

- `graph_to_prompt.py` — converts a ComfyUI UI-format workflow JSON (the kind you'd export
  from the visual editor) into API-format JSON that can be POSTed directly to a running
  ComfyUI server's `/prompt` endpoint. Written because the Chrome browser extension wasn't
  connecting this session, so everything had to be driven headlessly via the API instead of
  the visual UI. Uses the *running server's own* `/object_info` endpoint as the source of
  truth for each node's input order — reliable even for custom nodes, since it's asking the
  live node registry, not guessing from source.

Usage: `python graph_to_prompt.py workflow.json > prompt.json`, then POST
`{"prompt": <contents of prompt.json>}` to `http://127.0.0.1:8188/prompt`.

## Why any of this exists

MiniMax-H3 fails on wide shots (`minimax-h3-pipeline/README.md`), and Wan 2.2 TI2V-5B fixed
that (`wan22-pipeline/README.md`) but produces silent video only. Two ComfyUI-based routes
were explored to add dialogue back onto Wan's sharp visuals:

1. **H3-FaceRefine** — re-render just the face region through MiniMax-H3 itself at high
   magnification, keeping native audio. Ended up **not fixing F01's actual blur** at default
   settings (see `minimax-h3-pipeline` README/tracker) — technically works, not adopted.
2. **Wan (silent) + Qwen3-TTS (voice-cloned dialogue) + MuseTalk (lip-sync)** — **this one
   works end-to-end**, verified 2026-08-26: cloned Jan's voice from a verified-correct
   MiniMax-H3 audio sample, generated new dialogue, lip-synced it onto a Wan clip. Whisper
   transcription of the final muxed video came back an exact match to the target text, and
   frame-by-frame inspection showed real varying mouth shapes (not a static/frozen mouth) with
   no visible seam artifacts.

**This is the answer if a Wan-based wide shot needs to carry dialogue.** Not yet wired into
a proper one-command script — this was validated via hand-built API calls (below). Worth
building a `gen_lipsync_clip.py` alongside `gen_wide_clip.py` next time this comes up.

## Environment setup required (all outside the git repo, in the ComfyUI install)

This ComfyUI install already had MiniMax-H3 support built in (`comfy_extras/nodes_minimax_h3.py`
is core, not a plugin) and several relevant custom nodes pre-installed (`ComfyUI-GGUF`,
`ComfyUI-QwenTTS`, `ComfyUI-VideoHelperSuite`). Getting H3-FaceRefine and MuseTalk running
needed all of the following, roughly in this order:

1. **`ComfyUI-H3-FaceRefine`** cloned into `custom_nodes/` (github.com/Carasibana/ComfyUI-H3-FaceRefine).
   Deps (`ultralytics`, `scipy`, `insightface`) installed via pip into the ComfyUI venv.
   `face_yolov8m.pt` downloaded to `models/ultralytics/bbox/` (from `Bingsu/adetailer` on HF).
2. **`ComfyUI-MuseTalk_FSH`** cloned into `custom_nodes/` (github.com/AIFSH/ComfyUI-MuseTalk_FSH).
3. **`ComfyUI-H3-NativeAudioLock`** — H3-FaceRefine's lipsync path needs this SEPARATE repo's
   node (`MiniMax-H3-NativeAudioLock`), not bundled with H3-FaceRefine itself. Clone
   `Shrek3OnVH5/MiniMax-H3-NativeAudio-MusicVideo-Workflow` and copy just its
   `custom_nodes/ComfyUI-H3-NativeAudioLock/` subfolder into your own `custom_nodes/`.
4. **Visual Studio Build Tools 2022 + the C++ workload** (`Microsoft.VisualStudio.Workload.VCTools`)
   — needed to compile `xtcocotools` (an mmpose dependency) from source. Requires elevation
   (UAC) — the installer's `--quiet`/`--passive` flags refuse to run unelevated.
5. **Full NVIDIA CUDA Toolkit** (matching the installed torch's CUDA version — 13.0 here,
   `developer.nvidia.com/cuda-13-0-0-download-archive`) — needed to compile `mmcv`'s CUDA
   ops from source. The small `nvcc_13.0 cudart_13.0`-only component selection is NOT
   enough (missing `include/crt/host_config.h` and other headers) — do a full `-s` install.
6. **`mmcv` had to be patched and built from source**, not just pip installed:
   - No prebuilt wheel exists for our CUDA 13.0/torch 2.13 combo, so it must compile from
     source (`pip install --no-build-isolation mmcv==2.1.0`, with `CUDA_HOME` set,
     `DISTUTILS_USE_SDK=1`, and `vcvars64.bat` run first).
   - **mmcv 2.1.0's own `setup.py` hardcodes `/std:c++17` for MSVC CPU extensions** — but our
     torch build's headers require C++20. This is NOT fixable via the `CL` environment
     variable (an explicit `/std:` flag on the compile command line always wins over `CL`'s
     default). Real fix: download the mmcv 2.1.0 sdist, edit `setup.py` to change that one
     `'/std:c++17'` to `'/std:c++20'`, and `pip install` from the patched local directory.
   - `mmcv-lite` (pure Python, no compiled ops) is NOT sufficient — mmpose's `EDPoseHead`
     needs the real compiled `MultiScaleDeformableAttention` CUDA op, which only exists in
     full `mmcv`.
   - `mmdet` requires `mmcv < 2.2.0` specifically — don't install a newer mmcv/mmcv-lite.
7. Assorted smaller pip fixes, all in the ComfyUI venv:
   - `pip install chumpy --no-build-isolation` (old package, `import pip` inside its own
     `setup.py` breaks under pip's modern isolated build sandbox) — needs `wheel` installed
     first too (`error: invalid command 'bdist_wheel'` otherwise).
   - `pip install -U filelock` — `ultralytics` needs `AsyncFileLock`, not in old filelock.
   - `pip install "moviepy==1.0.3"` — MuseTalk_FSH's code uses `from moviepy.editor import
     ...`, which moviepy 2.x removed.
   - `pip install "setuptools==79.0.1"` at one point, to get `pkg_resources` back (removed in
     setuptools 80+) for an old-style `setup.py` mid-chain — later builds still worked fine
     with the newer setuptools ComfyUI itself wanted, so this wasn't a permanent pin.
8. **`ComfyUI-GGUF`'s `loader.py` needed a source patch**: its `IMG_ARCH_LIST` whitelist
   didn't include `"ltx2"` — which is literally what our `minimax_h3_ref2va_turbo_Q4_K_M.gguf`
   file's own `general.architecture` metadata field says (likely a labeling artifact from
   however unsloth's conversion script was adapted from an LTX-2 conversion script). Added
   `"ltx2"` and `"minimax_h3"` to that set.
   - **The 32B qwen3vl text encoder GGUF (the same file our CLI pipeline uses) does NOT work
     via `CLIPLoaderGGUF`** — it lacks the `general.architecture` metadata ComfyUI-GGUF
     strictly requires for text models, and unlike the diffusion-model check above, there's
     no whitelist to extend around it (text models raise unconditionally on a missing/junk
     arch string). Fix: use the safetensors text encoder from `Comfy-Org/MiniMax-H3`
     instead (`text_encoders/qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors`, 15.7GB, loaded
     via plain `CLIPLoader` with `type: minimax` — avoids the whole GGUF architecture check).
9. **A real dtype bug in ComfyUI core's own MiniMax-H3 support**
   (`comfy/ldm/minimax/model.py`): `torch.lerp(table[i0], table[i0+1], (pos-i0).unsqueeze(1))`
   fails with `expected dtype Half but got float` because `pos` derives from a
   `torch.float32` tensor while `table` is in the model's working (Half) dtype — `torch.lerp`
   requires the interpolation weight to match. Fixed by adding `.to(table.dtype)` to that
   `unsqueeze(1)` call. This is core ComfyUI code, not a custom node — will need reapplying
   if ComfyUI is ever updated past this file.
10. **Two bugs in `ComfyUI-MuseTalk_FSH` itself**, both fixed by editing its source directly:
    - `inference.py`: a literal typo building the face-parse checkpoint path —
      `os.path.join(parent_directory,"models','face-parse-bisent','79999_iter.pth")` (a
      malformed single string instead of three comma-separated arguments). Fixed to
      `os.path.join(parent_directory,'models','face-parse-bisent','79999_iter.pth')`.
    - `nodes.py`'s `LoadVideo.load_video()` crashes (`'NoneType' object has no attribute
      'write_audiofile'`) on a video with no audio track — exactly what Wan produces, since
      it's video-only. Patched to skip audio extraction when `video_clip.audio is None`.
    - `MuseTalk_FSH`'s own `LoadVideo` class was also **shadowed by core ComfyUI's own
      `LoadVideo` node** (same registered name, core wins) — core's version returns a
      `VideoFromFile` object, but MuseTalk's own code expects a plain path string. Renamed
      the registration key in `__init__.py` to `"MuseTalkLoadVideo"` to un-shadow it.
    - Several `torch.load(...)` calls (in `musetalk/models/unet.py`,
      `musetalk/whisper/whisper/__init__.py`, and `musetalk/utils/face_parsing/*.py`) needed
      `weights_only=False` added — PyTorch 2.6+ changed that default to `True`, which breaks
      loading these older-format checkpoints. One more instance of the same issue lives in
      `mmengine/runner/checkpoint.py` itself (`load_from_local`) — patched there too.
11. **`MiniMax H3 NativeAudioLock`'s companion models** for face-parsing/pose used by
    H3-FaceRefine had to be downloaded manually (the repo doesn't auto-fetch them):
    `musetalk/pytorch_model.bin` + `.json`, `dwpose/dw-ll_ucoco_384.pth`,
    `face-parse-bisent/{resnet18-5c106cde.pth,79999_iter.pth}`,
    `sd-vae-ft-mse/{config.json,diffusion_pytorch_model.bin}`, `whisper/tiny.pt` — into
    `ComfyUI-MuseTalk_FSH/models/<subfolder>/`, matching its README's expected layout exactly.

**If any of this needs redoing on a fresh machine**: expect most of steps 4-9 to still be
necessary (they're forced by the mismatch between this project's very new CUDA/torch and
these older ML packages, not by anything specific to this exact install), but steps 1-3 and
11 (cloning repos, downloading models) are quick. Budget real time for the compiler/CUDA
toolkit installs specifically — they're large downloads and the patches took several
iterations to get right.

## Validated pipeline (2026-08-26)

```
1. Voice clone: AILab_Qwen3TTSVoiceClone_Advanced
   - reference_audio: a verified-correct MiniMax-H3 clip's audio (extracted, e.g. via ffmpeg
     -vn from an existing minimax-h3-pipeline output)
   - reference_text: the exact line spoken in that reference clip
   - target_text: the new line to generate
   -> outputs a cloned-voice audio file (SaveAudio node, or read back via history/outputs)

2. Lip-sync: MuseTalkLoadVideo (NOT the shadowed core "LoadVideo") + MuseTalk node
   - video: your silent Wan clip (must be in ComfyUI's input/ folder)
   - audio: pass the cloned voice audio's ABSOLUTE FILE PATH as a literal string directly in
     the API prompt (not a link from a LoadAudio node) -- this pack's "AUDIO"/"VIDEO" types
     are informal labels for raw path strings, not ComfyUI's real structured AUDIO/VIDEO
     objects, and LoadAudio's structured output breaks it (`expected str... not dict`)
   - fps: match your source video's actual fps (24 for our Wan clips, not the 25 default)
   -> outputs a lip-synced but SILENT video (MuseTalk doesn't mux audio back in itself)

3. Mux audio back in: simplest to just do this with ffmpeg directly rather than fight
   CombineAudioVideo's required bgm_AUDIO input (we have no real background music track):
   ffmpeg -i lipsynced.mp4 -i cloned_voice.flac -c:v copy -c:a aac -shortest final.mp4
```

Verified: Whisper transcription of the final muxed file exactly matched the target text, and
manual frame inspection across the clip showed real, varying mouth shapes in sync with
speech (not a static mouth) with clean blending, no visible seam.
