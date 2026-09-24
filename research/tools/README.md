# Cutroom research tools

These are free tools that turn `research/QUALITY-PLAYBOOK.md` into checks you can run. None of them spend Higgsfield credits.

Setup (once, on your Mac):
```
pip3 install imageio-ffmpeg youtube-transcript-api yt-dlp
```
(`brew install ffmpeg` also works instead of imageio-ffmpeg.)

| Tool | When | What it does |
|---|---|---|
| `prompt_linter.py` | **Before paying** for any video | Checks a storyboard JSON + prompt against the playbook rules and blocks the spend on errors. It checks: prompt length caps (Seedance ~2,500 characters, Kling ~500 per shot), banned look/AI words, the "unbranded" clause, realism in the first 30 words, No subtitles / no music, `Hard cut to.` count, reference roles, exclusions and upload order, the product in the person ref, the hand law (selfie = one hand), SPEAK vs DO, state changes inside a shot, anti-morph (same POV + distance), word budget, short-line mumble, Kling lip-sync limits. |
| `phone_finish.py` | After a clip is approved | Turns an AI clip into phone footage: trims hot and glitchy head/tail frames, applies a pitch-safe retime, adds irregular handheld drift, mild phone sharpening, luma sensor noise (not film grain), 1080×1920 at 30 fps, a phone-mic audio chain, optional real room tone + room impulse response, and an optional messenger-style lossy pass. |
| `qa_frames.py` | On every **raw** generation | Builds a contact sheet for the frozen-frame review, compares the cut count to the storyboard, and flags duplicate/frozen frames, over-exposed first frames and dead-air gaps. It also prints the human checklist. |
| `harvest_transcripts.py` | Research | Downloads YouTube transcripts (search or `research/harvest-urls.txt`) as markdown. It waits between videos and stops cleanly if YouTube blocks you. |

## Examples
```
python3 research/tools/prompt_linter.py research/tools/examples/good_fitcheck.json   # passes
python3 research/tools/prompt_linter.py research/tools/examples/bad_fitcheck.json    # 15 errors, shows every rule
python3 research/tools/qa_frames.py raw_clip.mp4 --expect-cuts 7
python3 research/tools/phone_finish.py raw_clip.mp4 final.mp4 --speed 1.15 --room-tone bedroom_tone.wav --room-ir bedroom_clap.wav
```

`examples/good_fitcheck.json` is the playbook's 15 s SANTO hoodie fit-check (8 cuts, one Seedance 2.5 board call, 32 spoken words, 2,183 characters). It's a ready template.

## Free assets to record once (phone, 5 minutes)
- `bedroom_tone.wav`: 30 s of the real room with nobody talking (iPhone Audio Mix on **Standard**, not Studio).
- `bedroom_clap.wav`: one sharp hand clap in the room, trimmed to ~1 s. This is the room's impulse response, so AI voices get that room's real echo.
- Foley: the real mailer tearing, a zip, fleece rustle, a hoodie landing on the bed.

## How it plugs into Cutroom
The storyboard JSON fields are the shot spec the playbook proposes (§1 #4). Cutroom should save each planned ad in this shape, run the linter before every paid call, run `qa_frames.py` on each result, and run `phone_finish.py` on keepers.
