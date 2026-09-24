#!/usr/bin/env python3
"""Make an AI clip look and sound like it came off a phone (free, no credits).

Implements the finishing rules in research/QUALITY-PLAYBOOK.md (#7, 12.3):
trim the model's glitchy/over-exposed head and tail frames, optional retime
(pitch-safe), irregular handheld drift, mild phone sharpening, luma sensor
noise (not film grain), 30 fps, 1080x1920 H.264, and a phone-mic audio chain
(band-limit + light compression, optional real room tone and room impulse
response). No generative upscaling.

    pip install imageio-ffmpeg        # only if ffmpeg isn't installed
    python research/tools/phone_finish.py in.mp4 out.mp4
    python research/tools/phone_finish.py in.mp4 out.mp4 --speed 1.15 \
        --room-tone assets/bedroom_tone.wav --room-ir assets/bedroom_clap.wav
    python research/tools/phone_finish.py in.mp4 out.mp4 --messenger   # extra lossy pass

Tune by eye: --noise 0 turns grain off, --shake 0 turns drift off.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys


def ffmpeg_bin():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("ffmpeg not found: install it (brew install ffmpeg) or `pip install imageio-ffmpeg`")


def probe(ff, path):
    """Duration and whether the file has audio, parsed from ffmpeg's banner (no ffprobe needed)."""
    out = subprocess.run([ff, "-hide_banner", "-i", path], capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", out)
    if not m:
        sys.exit(f"can't read {path}:\n{out[-500:]}")
    dur = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
    return dur, "Audio:" in out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--head", type=float, default=0.25, help="seconds trimmed from the start (Seedance's first frames run hot)")
    ap.add_argument("--tail", type=float, default=0.4, help="seconds trimmed from the end")
    ap.add_argument("--speed", type=float, default=1.0, help="retime, e.g. 1.15 for floaty clips; audio tempo is kept pitch-correct")
    ap.add_argument("--shake", type=float, default=1.0, help="handheld drift amount (0 = off, 1 = subtle)")
    ap.add_argument("--noise", type=float, default=5, help="luma sensor noise strength (0 = off; ~5 subtle)")
    ap.add_argument("--sharpen", type=float, default=0.35, help="phone over-sharpening amount")
    ap.add_argument("--room-tone", help="wav/m4a of the real room's background tone, mixed low under everything")
    ap.add_argument("--room-tone-db", type=float, default=-38, help="room-tone level in dB relative to the source")
    ap.add_argument("--room-ir", help="impulse response of the real room (a recorded hand clap) for real reverb")
    ap.add_argument("--messenger", action="store_true", help="extra lossy re-encode, like a clip shared through a messenger")
    ap.add_argument("--crf", type=int, default=22)
    args = ap.parse_args()

    ff = ffmpeg_bin()
    dur, has_audio = probe(ff, args.input)
    keep = dur - args.head - args.tail
    if keep <= 0.5:
        sys.exit(f"clip is {dur:.2f}s, too short for --head/--tail trimming")

    # video: trim -> retime -> fill 9:16 frame with room for drift -> irregular drift crop -> sharpen -> noise -> 30fps
    s = args.shake
    margin_x, margin_y = int(48 * s) or 2, int(86 * s) or 2
    drift = (
        f"crop=1080:1920:"
        f"{margin_x // 2}+{9 * s:.2f}*sin(2*PI*t*0.9)+{4 * s:.2f}*sin(2*PI*t*2.3):"
        f"{margin_y // 2}+{7 * s:.2f}*sin(2*PI*t*0.7)+{3 * s:.2f}*sin(2*PI*t*1.9)"
    )
    vf = [
        f"setpts=(PTS-STARTPTS)/{args.speed}",
        f"scale={1080 + margin_x}:{1920 + margin_y}:force_original_aspect_ratio=increase:flags=bicubic",
        f"crop={1080 + margin_x}:{1920 + margin_y}",
        drift,
    ]
    if args.sharpen > 0:
        vf.append(f"unsharp=5:5:{args.sharpen}:5:5:0")
    if args.noise > 0:
        vf.append(f"noise=c0s={args.noise}:c0f=t+u")
    vf += ["fps=30", "setsar=1", "format=yuv420p"]

    cmd = [ff, "-hide_banner", "-y", "-ss", f"{args.head:.3f}", "-t", f"{keep:.3f}", "-i", args.input]
    inputs = 1
    tone_idx = ir_idx = None
    if args.room_tone:
        cmd += ["-stream_loop", "-1", "-i", args.room_tone]
        tone_idx, inputs = inputs, inputs + 1
    if args.room_ir:
        cmd += ["-i", args.room_ir]
        ir_idx, inputs = inputs, inputs + 1

    fc = [f"[0:v]{','.join(vf)}[v]"]
    if has_audio:
        a = f"[0:a]asetpts=PTS-STARTPTS,atempo={args.speed}" if args.speed != 1.0 else "[0:a]asetpts=PTS-STARTPTS"
        fc.append(f"{a}[a0]")
        cur = "a0"
        if ir_idx is not None:
            fc.append(f"[{cur}][{ir_idx}:a]afir=dry=8:wet=2[air]")
            cur = "air"
        # phone mic: band-limit, light pumping compression
        fc.append(f"[{cur}]highpass=f=150,lowpass=f=7500,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2[amic]")
        cur = "amic"
        if tone_idx is not None:
            fc.append(f"[{tone_idx}:a]volume={args.room_tone_db}dB,highpass=f=80[tone]")
            fc.append(f"[{cur}][tone]amix=inputs=2:duration=first:normalize=0[amix]")
            cur = "amix"
        fc.append(f"[{cur}]alimiter=limit=0.95[a]")

    cmd += ["-filter_complex", ";".join(fc), "-map", "[v]"]
    if has_audio:
        cmd += ["-map", "[a]", "-c:a", "aac", "-b:a", "128k", "-ar", "44100"]
    cmd += ["-c:v", "libx264", "-preset", "slow", "-crf", str(args.crf), "-movflags", "+faststart", args.output]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode:
        sys.exit("ffmpeg failed:\n" + res.stderr[-1500:])

    if args.messenger:
        tmp = args.output + ".tmp.mp4"
        shutil.move(args.output, tmp)
        res = subprocess.run([ff, "-hide_banner", "-y", "-i", tmp, "-c:v", "libx264", "-preset", "veryfast", "-crf", "28",
                              "-maxrate", "2.5M", "-bufsize", "5M", "-c:a", "aac", "-b:a", "96k", args.output],
                             capture_output=True, text=True)
        if res.returncode:
            sys.exit("messenger pass failed:\n" + res.stderr[-1500:])
        import os

        os.remove(tmp)

    out_dur, _ = probe(ff, args.output)
    print(json.dumps({"input_s": round(dur, 2), "output_s": round(out_dur, 2), "speed": args.speed,
                      "room_tone": bool(args.room_tone), "room_ir": bool(args.room_ir), "output": args.output}))


if __name__ == "__main__":
    main()
