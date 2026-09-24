#!/usr/bin/env python3
"""Free QA on a generated clip before a human reviews it (no credits, no AI calls).

Checks from research/QUALITY-PLAYBOOK.md (#30, 05 Auto-QA):
  - contact sheet of evenly spaced frames, for the frozen-frame review
    (face / product / hands / props / text), saved as a PNG
  - cut count vs the storyboard (Seedance/Kling can merge or invent cuts)
  - duplicate frames (FPS padding / dropped frames on long takes)
  - over-exposed first frames (Seedance runs hot at the start)
  - silence gaps and missing audio (frozen frames, dead air)

    python research/tools/qa_frames.py clip.mp4 --expect-cuts 7
    python research/tools/qa_frames.py clip.mp4 --frames 12 --out qa/

Run it on the RAW generated clip (before phone_finish.py): the finisher's
24->30 fps conversion adds repeated frames on purpose.

Exit code 1 if any check fails.
"""

import argparse
import json
import re
import shutil
import statistics
import subprocess
import sys
from pathlib import Path


def ffmpeg_bin():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("ffmpeg not found: install it (brew install ffmpeg) or `pip install imageio-ffmpeg`")


def run(ff, args):
    return subprocess.run([ff, "-hide_banner", *args], capture_output=True, text=True).stderr


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("clip")
    ap.add_argument("--frames", type=int, default=12, help="frames on the contact sheet")
    ap.add_argument("--expect-cuts", type=int, help="number of hard cuts the storyboard planned")
    ap.add_argument("--scene", type=float, default=0.3, help="scene-change threshold for cut detection")
    ap.add_argument("--out", default=None, help="output folder (default: next to the clip)")
    args = ap.parse_args()

    ff = ffmpeg_bin()
    clip = Path(args.clip)
    out = Path(args.out) if args.out else clip.with_suffix("").parent / (clip.stem + "_qa")
    out.mkdir(parents=True, exist_ok=True)

    banner = run(ff, ["-i", str(clip)])
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", banner)
    if not m:
        sys.exit(f"can't read {clip}")
    dur = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
    fps_m = re.search(r"([\d.]+) fps", banner)
    fps = float(fps_m.group(1)) if fps_m else 24.0
    has_audio = "Audio:" in banner
    report = {"clip": str(clip), "duration_s": round(dur, 2), "fps": fps, "checks": {}}
    fails = []

    # 1. contact sheet: N evenly spaced frames, 4 per row, timestamp burned in
    n = args.frames
    step = dur / n
    cols = 4
    rows = -(-n // cols)
    sheet = out / "contact_sheet.png"
    vf = (f"fps={n}/{dur:.4f},scale=270:-2,"
          f"drawtext=text='%{{pts\\:hms}}':x=6:y=6:fontcolor=white:box=1:boxcolor=black@0.6:fontsize=16,"
          f"tile={cols}x{rows}")
    err = run(ff, ["-y", "-i", str(clip), "-vf", vf, "-frames:v", "1", str(sheet)])
    if not sheet.exists():  # drawtext needs a font; fall back without timestamps
        run(ff, ["-y", "-i", str(clip), "-vf",
                 f"fps={n}/{dur:.4f},scale=270:-2,tile={cols}x{rows}", "-frames:v", "1", str(sheet)])
    report["contact_sheet"] = str(sheet) if sheet.exists() else None

    # 2. cuts
    err = run(ff, ["-i", str(clip), "-vf", f"select='gt(scene,{args.scene})',showinfo", "-an", "-f", "null", "-"])
    cut_times = [round(float(t), 2) for t in re.findall(r"pts_time:([\d.]+)", err)]
    report["checks"]["cuts"] = {"found": len(cut_times), "at_s": cut_times}
    if args.expect_cuts is not None and len(cut_times) != args.expect_cuts:
        fails.append(f"cuts: found {len(cut_times)}, storyboard planned {args.expect_cuts} (merged or invented cuts)")

    # 3. duplicate frames
    total = len(re.findall(r"\bn:\s*\d+", run(ff, ["-i", str(clip), "-vf", "showinfo", "-an", "-f", "null", "-"])))
    kept = len(re.findall(r"\bn:\s*\d+", run(ff, ["-i", str(clip), "-vf", "mpdecimate,showinfo", "-an", "-f", "null", "-"])))
    dup_pct = 100 * (total - kept) / total if total else 0
    report["checks"]["duplicate_frames"] = {"total": total, "near_duplicates": total - kept, "pct": round(dup_pct, 1)}
    if dup_pct > 15:
        fails.append(f"duplicate frames {dup_pct:.0f}%: padded/frozen footage; regenerate hero shots, de-dup b-roll")

    # 4. exposure: first 6 frames vs the clip median
    err = run(ff, ["-i", str(clip), "-vf", "signalstats,metadata=print:key=lavfi.signalstats.YAVG", "-an", "-f", "null", "-"])
    yavg = [float(v) for v in re.findall(r"lavfi\.signalstats\.YAVG=([\d.]+)", err)]
    if yavg:
        head = statistics.mean(yavg[:6])
        med = statistics.median(yavg)
        report["checks"]["exposure"] = {"first_frames_luma": round(head, 1), "median_luma": round(med, 1)}
        if head > med * 1.12 and head - med > 8:
            fails.append(f"first frames brighter than the clip (luma {head:.0f} vs {med:.0f}): trim the head (phone_finish --head)")

    # 5. audio: presence + silence gaps inside the clip
    if not has_audio:
        report["checks"]["audio"] = {"present": False}
        fails.append("no audio track: add VO / room tone")
    else:
        err = run(ff, ["-i", str(clip), "-af", "silencedetect=noise=-45dB:d=0.6", "-vn", "-f", "null", "-"])
        starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
        ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
        gaps = [(round(s, 2), round(e, 2)) for s, e in zip(starts, ends) if 0.3 < s and e < dur - 0.3]
        report["checks"]["audio"] = {"present": True, "silences_over_0.6s": gaps}
        if gaps:
            fails.append(f"dead-air gaps {gaps}: real phone audio always has room tone (and long silences can freeze Seedance frames)")

    report["fails"] = fails
    report["human_checklist"] = [
        "same face as the identity plate in every frame (markers: mole/earring)",
        "SANTO logo/print not garbled, mirrored or morphed; colour matches the swatch",
        "max 2 hands per person, no phone visible, product at real scale",
        "props in the right state (sealed/open) and never both",
        "no burned-in captions or random text; no mirrors",
        "mouth closed on voice-over shots; lips clean on mid-word frames",
    ]
    (out / "qa_report.json").write_text(json.dumps(report, indent=1))
    print(json.dumps(report, indent=1))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
