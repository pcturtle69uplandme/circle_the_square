import os
import subprocess
import imageio_ffmpeg
import build_cartoon_building_trailer as b

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

TARGET_W, TARGET_H = 1920, 1080
LB_H = int(round(TARGET_W / 2.39))
PAD_Y = (TARGET_H - LB_H) // 2

scale_pad = (
    f"scale={TARGET_W}:{LB_H}:force_original_aspect_ratio=increase,"
    f"crop={TARGET_W}:{LB_H},"
    f"pad={TARGET_W}:{TARGET_H}:0:{PAD_Y}:black,"
    f"fps=24,format=yuv420p"
)

filter_graph = ""
total_dur = 0.0
for i, (name, dur, path) in enumerate(b.available_shots):
    start, max_dur = b.usable_window(path, name)
    actual_dur = min(dur, max_dur)
    end = start + actual_dur
    total_dur += actual_dur
    filter_graph += f"[{i}:v]trim=start={start:.2f}:end={end:.2f},setpts=PTS-STARTPTS,{scale_pad}[v{i}];"

concat_inputs = "".join([f"[v{i}]" for i in range(len(b.available_shots))])
filter_graph += f"{concat_inputs}concat=n={len(b.available_shots)}:v=1:a=0[vout_raw];"

video_fade_start = max(0.0, total_dur - 1.5)
filter_graph += f"[vout_raw]fade=t=out:st={video_fade_start:.2f}:d=1.5[vout];"

vol_expr = f"if(lt(t,2.5), t/2.5, 1.0)"
audio_filter = (
    f"[{len(b.available_shots)}:a]volume='{vol_expr}':eval=frame,"
    f"atrim=0:{total_dur:.2f},"
    f"afade=t=out:st={video_fade_start:.2f}:d=1.5,"
    f"aresample=48000[aout]"
)

full_filter = filter_graph + audio_filter
out_target = os.path.join(b.BASE_DIR, "clips", "CARTOON_BUILDING_TRAILER_FULL.mp4")

cmd = [FFMPEG, "-y"]
for p in b.clip_paths:
    cmd.extend(["-i", p])
cmd.extend(["-stream_loop", "-1", "-i", b.audio_bed])
cmd.extend([
    "-filter_complex", full_filter,
    "-map", "[vout]",
    "-map", "[aout]",
    "-c:v", "libx264",
    "-profile:v", "main",
    "-level", "4.1",
    "-pix_fmt", "yuv420p",
    "-preset", "medium",
    "-crf", "18",
    "-c:a", "aac",
    "-ar", "48000",
    "-ac", "2",
    "-b:a", "192k",
    "-movflags", "+faststart",
    "-t", f"{total_dur:.2f}",
    out_target
])

print(f"--- Rendering Fixed Trailer ({len(b.available_shots)} shots, target dur: {total_dur:.2f}s) ---")
res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
if res.returncode == 0:
    print("Render SUCCESS!")
else:
    print("Render FAILED:\n", res.stderr)
