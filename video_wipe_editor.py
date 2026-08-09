import os
import subprocess
import sys
import imageio_ffmpeg

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

def get_clip_duration(clip_path):
    cmd = [FFMPEG_EXE, "-i", clip_path]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
            hours, mins, secs = float(parts[0]), float(parts[1]), float(parts[2])
            return hours * 3600 + mins * 60 + secs
    return 5.0

def stitch_clips_with_wipes(clip_paths, output_path, transition_type="wipeleft", transition_duration=0.75):
    """
    Stitches a list of video clips together using FFmpeg xfade transition wipes.
    
    Supported transitions:
      - 'wipeleft', 'wiperight', 'wipedown', 'wipeup'
      - 'slideleft', 'slideright', 'slideup', 'slidedown'
      - 'circlecrop', 'rectcrop', 'radial', 'diagtl', 'diagtr', 'dissolve'
    """
    if len(clip_paths) < 2:
        print("Error: Need at least 2 video clips to apply wipe transitions.")
        return False

    durations = [get_clip_duration(p) for p in clip_paths]
    print(f"Loaded {len(clip_paths)} clips with durations: {[round(d, 2) for d in durations]}")

    filter_graph = ""
    last_stream = "[0:v]"
    current_offset = 0.0

    for i in range(len(clip_paths) - 1):
        duration_curr = durations[i]
        offset = current_offset + duration_curr - transition_duration
        current_offset = offset
        next_stream = f"[{i+1}:v]"
        out_stream = f"[v{i+1}]" if i < len(clip_paths) - 2 else "[vout]"
        
        t_type = transition_type[i % len(transition_type)] if isinstance(transition_type, list) else transition_type

        filter_graph += f"{last_stream}{next_stream}xfade=transition={t_type}:duration={transition_duration}:offset={offset:.2f}{out_stream};"
        last_stream = out_stream

    cmd = [FFMPEG_EXE, "-y"]
    for path in clip_paths:
        cmd.extend(["-i", path])

    cmd.extend([
        "-filter_complex", filter_graph,
        "-map", "[vout]",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        output_path
    ])

    print("\n--- Running FFmpeg Video Wipe Stitcher ---")
    print(f"Output Target: {output_path}")

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0 and os.path.exists(output_path):
        print(f"\n[SUCCESS] Stitched video with wipes successfully created: {output_path}")
        return True
    else:
        print(f"\n[ERROR] FFmpeg execution error:\n{res.stderr}")
        return False

if __name__ == "__main__":
    clips_dir = r"C:\ai\Circle the Square\clips"
    sample_clips = [
        os.path.join(clips_dir, "OPENING_S01_drone_orbit.mp4"),
        os.path.join(clips_dir, "OPENING_S02_KEEPER.mp4"),
        os.path.join(clips_dir, "OPENING_S03_KEEPER.mp4"),
        os.path.join(clips_dir, "OPENING_S04.mp4")
    ]
    
    valid_clips = [p for p in sample_clips if os.path.exists(p)]
    if len(valid_clips) >= 2:
        out_file = os.path.join(clips_dir, "OPENING_SEQUENCE_WIPE_DEMO.mp4")
        wipe_list = ["wipeleft", "wiperight", "circlecrop", "slideleft"]
        stitch_clips_with_wipes(valid_clips, out_file, transition_type=wipe_list, transition_duration=0.8)
