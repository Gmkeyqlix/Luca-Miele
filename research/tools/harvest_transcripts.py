#!/usr/bin/env python3
"""Download YouTube transcripts (tutorials, podcasts, talks) as markdown for research.

Needs network access to youtube.com. Run it on your own computer, or in a cloud
session whose network policy allows youtube.com.

    pip install youtube-transcript-api yt-dlp

    # every URL in a harvest list (URL<TAB>priority<TAB>title, one per line)
    python research/tools/harvest_transcripts.py --list research/harvest-urls.txt

    # search YouTube and take the top N results per query
    python research/tools/harvest_transcripts.py --search "seedance 2.0 ugc ad tutorial" --per-query 10

    # only priority 1 items from the list
    python research/tools/harvest_transcripts.py --list research/harvest-urls.txt --max-priority 1

Output: research/transcripts/<video_id>.md (title, channel, url, duration,
description, chapters and the full transcript with [mm:ss] timestamps every ~30s).
Already downloaded videos are skipped, so it is safe to re-run.
"""

import argparse
import re
import sys
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent / "transcripts"
ID_RE = re.compile(r"(?:v=|youtu\.be/|shorts/|live/|embed/)([A-Za-z0-9_-]{11})")


def video_id(url):
    m = ID_RE.search(url)
    if m:
        return m.group(1)
    return url if re.fullmatch(r"[A-Za-z0-9_-]{11}", url) else None


def read_list(path, max_priority):
    items = []
    for line in Path(path).read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split("\t")
        prio = int(parts[1]) if len(parts) > 1 and parts[1].strip().isdigit() else 3
        if prio <= max_priority:
            items.append(parts[0].strip())
    return items


def search(query, n):
    import yt_dlp

    opts = {"quiet": True, "extract_flat": True, "skip_download": True}
    with yt_dlp.YoutubeDL(opts) as ydl:
        res = ydl.extract_info(f"ytsearch{n}:{query}", download=False)
    return [f"https://www.youtube.com/watch?v={e['id']}" for e in res.get("entries", []) if e.get("id")]


def metadata(url):
    import yt_dlp

    opts = {"quiet": True, "skip_download": True}
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            return ydl.extract_info(url, download=False) or {}
    except Exception as e:  # metadata is nice-to-have; transcript is what matters
        print(f"  metadata failed: {e}", file=sys.stderr)
        return {}


def transcript(vid):
    from youtube_transcript_api import YouTubeTranscriptApi

    api = YouTubeTranscriptApi()
    try:
        return api.fetch(vid, languages=("en", "en-US", "en-GB")).to_raw_data()
    except Exception:
        # fall back to any available transcript, translated to English when possible
        tl = api.list(vid)
        t = next(iter(tl))
        if t.language_code != "en" and t.is_translatable:
            t = t.translate("en")
        return t.fetch().to_raw_data()


def fmt_ts(sec):
    sec = int(sec)
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def to_markdown(url, meta, segs):
    lines = [
        f"# {meta.get('title', url)}",
        "",
        f"- URL: {url}",
        f"- Channel: {meta.get('channel') or meta.get('uploader', '?')}",
        f"- Uploaded: {meta.get('upload_date', '?')}",
        f"- Duration: {fmt_ts(meta.get('duration') or 0)}",
        f"- Views: {meta.get('view_count', '?')}",
        "",
    ]
    if meta.get("chapters"):
        lines += ["## Chapters", ""]
        lines += [f"- [{fmt_ts(c['start_time'])}] {c['title']}" for c in meta["chapters"]]
        lines.append("")
    if meta.get("description"):
        lines += ["## Description", "", meta["description"].strip(), ""]
    lines += ["## Transcript", ""]
    para, next_mark = [], 0
    for seg in segs:
        if seg["start"] >= next_mark:
            if para:
                lines.append(" ".join(para))
                lines.append("")
            para = [f"[{fmt_ts(seg['start'])}]"]
            next_mark = seg["start"] + 30
        para.append(seg["text"].replace("\n", " "))
    if para:
        lines.append(" ".join(para))
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", help="harvest list file: URL<TAB>priority<TAB>title")
    ap.add_argument("--max-priority", type=int, default=3)
    ap.add_argument("--search", action="append", default=[], help="YouTube search query (repeatable)")
    ap.add_argument("--per-query", type=int, default=10)
    ap.add_argument("urls", nargs="*")
    args = ap.parse_args()

    urls = list(args.urls)
    if args.list:
        urls += read_list(args.list, args.max_priority)
    for q in args.search:
        urls += search(q, args.per_query)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    done = failed = skipped = 0
    seen = set()
    for url in urls:
        vid = video_id(url)
        if not vid or vid in seen:
            continue
        seen.add(vid)
        out = OUT_DIR / f"{vid}.md"
        if out.exists():
            skipped += 1
            continue
        print(f"-> {url}")
        try:
            segs = transcript(vid)
        except Exception as e:
            print(f"  no transcript: {e.__class__.__name__}", file=sys.stderr)
            failed += 1
            continue
        watch = f"https://www.youtube.com/watch?v={vid}"
        out.write_text(to_markdown(watch, metadata(watch), segs))
        done += 1
    print(f"\nsaved {done}, skipped {skipped} existing, failed {failed} -> {OUT_DIR}")


if __name__ == "__main__":
    main()
