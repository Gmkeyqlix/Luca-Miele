# Shared research brief — read fully before starting

## Who / what
Luca runs SANTO Clothing (santo.clothing, streetwear/basics: jeans, hoodies, fleece, tees, leggings; ships in a branded poly mailer bag).
We are building "Cutroom", an internal app that makes 15-second UGC-style (TikTok/Reels, phone-filmed-looking) product ads with AI,
mainly through Higgsfield (Soul / Soul ID stills, Nano Banana edits ~1.5 credits, video on Seedance 2.x ~18 credits, Kling 3.x, Wan 3.0 ~3.5 credits).
Goal: reach "top of the bell curve" quality — outputs that read as a real person filmed on a phone — FIRST TIME, without paying for endless test videos.
The question is: WHAT DO WE CHANGE ON THE INPUT SIDE (references, frames, prompts, captured real material, model choice, shot design, finishing/post) to get there?

## Already known / already built (do NOT report these as new unless you have a materially better way of doing them)
- Model (person) reference image; product reference image; multiple references per shot, sometimes a reference video
- A "movement library" of stored motion references
- Generic brainstorm ideas we already have: first+last frame, cut-to-transform (hide state changes in cuts), real-hands inserts, product state photo kit, real room photos, phone camera profile/grain, real room sound, handheld shake, grey card colour check, storyboard gate, cheapest-model routing, rule mining from rejections, golden shot library.
  -> Only include these if you find EVIDENCE of how pros actually do it (specific settings, numbers, gotchas) — that's what we lack.

## Failures we keep hitting (map every finding to one or more)
F1 face/identity drift between shots and within a shot
F2 product drift: logo, print, colour, stitching, tag, garment details change or get invented
F3 hands: extra/merged fingers, impossible grips, phone-in-hand while both hands busy, giant/tiny product scale
F4 state changes break: ripping mailer bag open, pulling hoodie on, zipping, folding/unfolding
F5 fabric physics & garment fit look fake (leggings especially, denim stiffness, fleece)
F6 overall "AI look": too smooth/clean, 85mm portrait bokeh, perfect lighting, plastic skin, slow-mo floaty motion
F7 environment warps/changes (rooms, furniture, posters, random jewellery/props appearing)
F8 audio is silent or obviously AI; lip-sync/voice feels fake
F9 wasted credits: rerolls, no way to predict success, wrong model for the shot

## Output — write to your assigned file in this folder (markdown)
For EACH technique:
- **Name** (short)
- **What it is / exactly how to do it** — concrete: settings, prompt wording, numbers, order of steps
- **Fixes**: F-codes
- **Who does it / evidence**: source URLs (real ones you saw), and strength: A = official vendor docs or multiple independent pros showing results; B = one credible practitioner with shown results; C = claim/anecdote
- **Input change for Cutroom**: what the app would store/require/send differently
- **Cheapest test** + rough credit cost (0 if free)
Also include: a "STOP DOING" section (things pros say hurt quality) and "Open questions" section.
Prioritise depth and specificity over breadth. 12-30 strong techniques beats 60 vague ones. No fluff, no generic "use good lighting".

## Environment constraints (important)
- WebSearch WORKS (returns summarised results) — use MANY specific queries (15-40), vary phrasing, include year 2026/2025, names of people/tools.
- WebFetch is BLOCKED for almost all domains (medium, fal, magichour, reddit, higgsfield.ai, kling.ai, arxiv...). Don't waste time retrying; rely on WebSearch summaries.
- GitHub: raw.githubusercontent.com works via curl; `git clone --depth 1 https://github.com/owner/repo` works for public repos (clone into this research folder's `repos/` subdir). github.com web pages, GitHub search API and the GitHub MCP tools DO NOT work for other repos. Find repos via WebSearch ("site:github.com ...") then read READMEs/files via raw URLs or shallow clone.
- NEVER spend Higgsfield credits: no generate_*, execute_preset, motion_control, upscale, remove_background, reframe, outpaint, voice/dubbing, tiktok, publish or any paid/writing call. Never log into or act on anyone's accounts or browser.
- Today is 2026-09-24.
