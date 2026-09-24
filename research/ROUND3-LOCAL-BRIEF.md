# Round 3: research only your Mac can do

The cloud session couldn't reach these sources: its network blocks most sites and it has no browser. Your **local** Claude (Desktop app → Code, on the `luca-miele` folder) can reach them, and can use your signed-in Chrome if Claude in Chrome is connected.

**How to use this:** open the local session and paste one block at a time. Each one is self-contained. None of them spend Higgsfield credits.

---

### Block 1: YouTube batch 2 (no browser needed)
```
Pull branch claude/jolly-davinci-yz64dv. Run:
python3 research/tools/harvest_transcripts.py --list research/harvest-urls.txt --max-priority 2
If YouTube blocks it, stop and tell me. Then read research/BRIEF.md and research/QUALITY-PLAYBOOK.md,
read every NEW file in research/transcripts/, and write research/10-transcripts-batch2.md in the same
format as research/09a-transcripts.md (findings marked NEW / EXTENDS / CONTRADICTS, with video id + timestamp).
Use at most 3 subagents. Commit and push to claude/jolly-davinci-yz64dv.
```

### Block 2: Higgsfield's own teaching (browser)
```
Read research/BRIEF.md. Using the browser, read these Higgsfield pages fully and extract every concrete
technique for realistic UGC / clothing / unboxing video (settings, prompt wording, limits, costs):
- higgsfield.ai/academy/courses/brand-visuals-ai (all lessons, esp. "Marketing Studio Try-Ons" and "Packaging & Unboxing")
- higgsfield.ai/blog/higgsfield-genjutsu and the Genjutsu cost/limits pages
- any Higgsfield page explaining "Anti-Slop" mode for Seedance 2.5
- higgsfield.ai/blog/generating-with-seedance-2-0
Don't click generate or buy anything. Write research/11-higgsfield-academy.md (BRIEF format), commit and push.
```

### Block 3: Official model docs the cloud couldn't open (browser)
```
Read research/BRIEF.md and research/02-model-guides.md. With the browser, read the official docs:
BytePlus/ModelArk Seedance 2.0 and 2.5 prompt guides, Kling quickstart (Elements, Motion Control,
Virtual Try-On, multi-shot), Alibaba Model Studio wan3 video generation guide. Only record what CHANGES or
ADDS to 02-model-guides.md (exact limits, reference syntax, parameters, negative prompt rules).
Write research/12-official-docs.md, commit and push.
```

### Block 4: What real people say (Reddit/X, via the signed-in browser)
```
Read research/BRIEF.md. In the browser, search Reddit (r/FacebookAds, r/aivideo, r/UGCcreators,
r/ecommerce, r/HiggsfieldAI) and X for 2026 threads on: AI UGC ads for clothing, "does AI UGC convert",
"how can you tell it's AI", Seedance/Kling product consistency, Higgsfield UGC tips. Read-only: no posting,
liking or following. Extract concrete tells viewers mention and fixes creators report, with links.
Write research/13-community.md, commit and push.
```

### Block 5: Real costs (browser, no generating)
```
In the browser, open Higgsfield and set up (but DO NOT click generate) a Seedance 2.5 video:
15 s, 720p, audio on; then 480p; then Seedance Fast 720p; then Kling 3.0 15 s std with audio off;
then Genjutsu Object Swap 10 s; Marketing Studio UGC 15 s. Record the credit cost shown on each
generate button. Write the table to research/14-costs.md, commit and push.
```

### Block 6: Two podcasts nobody could transcribe
Watch these yourself at 1.5× speed and note anything concrete, or run Block 1's tool on them:
- fal Podcast with Tim Simmons: `https://www.youtube.com/watch?v=deQNOjnDcwY`
- AI For Humans: `https://www.youtube.com/watch?v=EA3PGSRotwc`

---

When any block is pushed, tell the cloud session, or the local one, to "merge research/1x-*.md into QUALITY-PLAYBOOK.md".
