# SANTO / Cutroom — all AI-video quality research in one file

Compiled 2026-09-24. Start with Part 1 (the playbook, which is the merged and ranked result). Parts 2+ are the full source reports it was built from. Source links are inside each part. Transcripts and tool code live in the repo (branch claude/jolly-davinci-yz64dv, folder research/).

## Contents
1. Cutroom Quality Playbook: what the best people do, and what we change — `QUALITY-PLAYBOOK.md`
2. Shared research brief — read fully before starting — `BRIEF.md`
3. 01 — Higgsfield ecosystem: internal recipes, model facts, community repos — `01-higgsfield.md`
4. 02 — Model guides: the knobs Cutroom is not using — `02-model-guides.md`
5. 03 — What working AI filmmakers and ad-makers do (source: pros' interviews, BTS, published pipelines) — `03-filmmakers.md`
6. 04 — Competitor AI-UGC tools, fashion try-on, and real UGC craft — `04-ugc-tools-fashion.md`
7. 05 — GitHub open source + research: skills, tools, auto-QA, AI-detection signals — `05-github-research.md`
8. 06 — Winning apparel ads, courses/communities, prompt→output structures — `06-winning-ads-courses.md`
9. 07: What adjacent industries do: virtual influencers, 3D/digital twins, performance capture, audio, e-com capture — `07-adjacent-3d-audio.md`
10. 08 — Podcasts & YouTube: what practitioners say they actually do — `08-podcasts-youtube.md`
11. 09a: YouTube transcript mining (batch A, 9 videos) — `09a-transcripts.md`
12. 09b: Techniques mined from YouTube transcripts (batch b, 9 videos) — `09b-transcripts.md`
13. 09c: YouTube transcript mining (batch C, 9 videos) — `09c-transcripts.md`
14. Cutroom research tools — `tools/README.md`
15. Round 3: research only your Mac can do — `ROUND3-LOCAL-BRIEF.md`


---

# PART 1 — `QUALITY-PLAYBOOK.md`

## Cutroom Quality Playbook: what the best people do, and what we change

**Date:** 2026-09-24 · **For:** Luca / SANTO · **Question:** what do we change on the *input* side so AI UGC ads come out looking like a real person filmed on a phone, first time, without paying for endless test videos?

**How this was made:** eight parallel researchers, one per source type:
1. Higgsfield's own built-in recipes, read for free through the MCP
2. Official model guides
3. AI filmmakers and studios
4. Competitor UGC tools, fashion and real UGC craft
5. GitHub skill libraries, open-source tools and research papers
6. Winning ads, courses and contests
7. Adjacent industries: virtual influencers, 3D and audio
8. Podcasts and YouTube

About 600 searches in total. Roughly 30 GitHub repos were read in full. **No Higgsfield credits were spent.** The full reports are in `research/01-…08-*.md`, and they contain every source link. This file is the merged, ranked result.

**Evidence grades:**
- **A:** official vendor material, or several independent pros showing results
- **B:** one credible practitioner with shown results
- **C:** a claim, or our own inference

Failure codes (from `BRIEF.md`): F1 face drift · F2 product drift · F3 hands/scale · F4 state changes (rip, pull-on, zip) · F5 fabric/fit · F6 "AI look" · F7 room/props warp · F8 audio/lip-sync · F9 wasted credits.

---

## 0. The one-paragraph answer

The people getting top results don't get shots right first time. Higgsfield's own 90-minute feature kept about 1.5% of its video generations, and the Kalshi ad needed about 25 generations per kept shot. What they do differently is **where** they spend the retries and **what they feed the model**:

1. They make the whole ad from **one approved storyboard board in one video call**, so every cut shares one face, one product and one room.
2. They iterate on **cheap stills**, not video.
3. For anything physical (fit, tearing, pulling on, hands on product), they **film it for real on a phone and let the AI swap only the person**.
4. They write prompts from a **structured shot spec** full of hard rules: hand counts, who holds the phone, one state change per cut, reference roles and exclusions, a realism block at the start of the prompt, no slow motion.
5. They treat **audio as half of realism**: a real human voice, room tone, real foley, no music.

Cutroom already has the right instincts (references, a movement library, state photos). The top of the bell curve is getting the **architecture** right and **enforcing the rules in code**.

---

## 1. Top of the bell curve: the 7 changes that matter most

Ranked by impact × evidence ÷ effort. Do these before anything else.

### #1 Board → one video call (Higgsfield's own UGC pipeline) · A
**What:** Higgsfield's four shipped UGC workflows (review, unboxing, try-on, product-only) run the same four steps:
1. Creator still, **person only, no product**.
2. One **21:9 storyboard image with 4 or 8 vertical 9:16 panels**, made with gpt_image_2.
3. A mandatory **"de-slop" realism pass** (Seedream v5 Pro).
4. **One Seedance 2.5 `omni_reference` call per 15 s**, with the board, character and product as references, native audio, and the literal text `Hard cut to.` between cuts. Each panel becomes an internal hard cut.

Cutroom currently generates shot by shot and stitches the shots together. That is why faces, products and rooms drift between shots.

**Key rules that come with it:**
- **Anti-morph rule:** adjacent panels must differ in *both* camera position (selfie / static / static-close) *and* distance (tight / mid / wide). Otherwise Seedance blends them instead of cutting.
- **The board is a map, not a template.** The video prompt must describe *motion inside each cut*. A sparse prompt makes Seedance copy the panels frame for frame, which looks stiff.
- Slot counts: 8 for try-on and review, 4 for unboxing and product. The try-on timings for 15 s are 1.9 / 2.3 / 1.9 / 1.4 / 1.9 / 1.4 / 2.3 / 1.9 s.

**Fixes:** F1 F2 F7 F9. **Source:** `01-higgsfield.md` T1–T2, `06` T1–T2, `hf-workflows/`. Independently confirmed by joebenscoter's validated 3-panel pipeline (`05` #14).
**Test:** 1 board + 1 de-slop + 1 Seedance 15 s call on the best-selling hoodie. Run `get_cost` first (see §7).

### #2 Real body plate + AI identity swap for anything physical · A (principle) / B (2026 tools)
**What:** the virtual humans that look most real (Imma, Shudu, Lil Miquela), plus Mango, Zara and H&M, **never generate the clothes**. A real body wears the real garment in a real room, and only the identity is synthetic.

For us, a body double of similar build films the hard beats on a phone: tearing the mailer, pulling on the hoodie, a squat in leggings, a denim walk. Then only the person is swapped using one of:
- **Higgsfield Ad Multiplier** (keeps the source's motion, cuts, timing and real audio)
- **Genjutsu `hf_mult_replace_object`**
- **Wan Animate Replace**, which relights to the plate

**Why it's the biggest single lever:** fabric physics, fit, hand-on-product contact, the tear and the room are all *recorded*, so F2, F3, F4, F5, F6 and F7 are fixed at the source. It also answers the Mango backlash, where shoppers said AI bodies are "useless" for judging fit.

**Plate spec** (vendor docs):
- one continuous 3–30 s shot
- hands visible, never crossing the torso
- half-body beats full-body
- even front or window light
- the performer does the **real action with the real product** (never mimed)
- character-image aspect ratio = video aspect ratio
- body double's build ≈ persona's build (Wan Replace doesn't retarget)
- iPhone audio set to "Standard", not "Studio" mode

**Fixes:** F2 F3 F4 F5 F6 F7 (+F9). **Source:** `07` #1, #4, #12, #13; `01` T21; `02` T15; `03` T17.
**Test:** film one 6 s hoodie pull-on today (free), then one swap run. Check the cost with `get_cost`.

### #3 Iterate on stills, never on video; one approved composite still gates every paid clip · A
**What:** every competitor (HeyGen, Higgsfield UGC Factory, TopView, MakeUGC, Kling's fashion workflow) and every pro (PJ Ace, Hell Grind, Fazi) makes an **approved composite still** (person + garment + room) before any video. PJ Ace composites "over dozens of iterations" in Nano Banana (about 1.5 credits each), then animates with **simple prompts**.

Rules:
- **4 variants** per keyframe/board, approve 1.
- **Never run an image through a model twice in full.** Faces go plastic after about 2 passes. Make the point edit, then **mask only the changed region back onto the untouched master**.
- **Small fixes = model switch + one sentence** (NB2: "change the logo to the one in image two"), never a full re-prompt.
- **Generate in the final 9:16 ratio.** Cropping later is a silent failure.

**Fixes:** F1 F2 F3 F6 F9. **Source:** `03` T3, T5; `04` T1; `05` #7; `02` T18.

### #4 A structured shot spec + a prompt linter that enforces the rules · A
The same rules appear independently in Higgsfield's recipes, ByteDance's official Seedance guide, OpenAI's and Google's guides, and several validated GitHub libraries. Cutroom should store these as **fields** and refuse to spend credits when a rule fails.

| Field / rule | What it enforces | Fixes |
|---|---|---|
| `camera_holder` ∈ selfie / propped / friend (and mirror is banned, see STOP list) | A selfie uses one hand for the phone (off-frame), so **any two-handed action forces a propped static camera**. The phone is never visible. | F3 |
| `left_hand`, `right_hand` roles | ≤2 hand roles; the idle hand is "parked" explicitly; props rest on surfaces rather than float. Every hand shot gets: *"There are only two hands in the frame, both belonging to the same person, entering from the same sleeve."* | F3 |
| `pov` + `distance_band` | Anti-morph: adjacent shots differ in both | F1 F7 |
| `start_state` / `end_state` per prop | ≤1 state change per cut; the change happens on the cut, never mid-shot; the next shot restates the new state and bans the old one | F4 |
| `beat_type` = SPEAK or DO | **Never dialogue + hand action in the same shot.** DO beats get voice-over or silence. Lip-sync only frontal or ¾, hands low, face 20–40% of frame. | F8 F3 |
| Word budget | 13–15 s → 28–35 words; ≤10 s → 12–20; **≤6-word lines in a 4 s window produce mumble** (measured); talking segments ≤8 s per generation (Kling loses sync after second 8) | F8 |
| Reference roles | One line per reference: what to use + what *not* to use (`"@Image 4… use only the spatial layout and lighting. Do not use the people"`). Multi-view product: *"All these images define one single hoodie. The output must contain only one."* Never fill every reference slot (1–8 images). | F1 F2 F7 |
| Realism block **at the start** of the prompt | Seedance follows the first 2–3 instructions and drops things after about 8. Pores / anti-polish / light on 4 axes / 3–4 named clutter objects / micro-shake | F6 |
| Motion | "real-time speed, never slow motion"; counted beats ("takes four steps… in the final second"); one camera move with a named endpoint; no loop verbs ("again", "twice", "back and forth") | F6 |
| Scale | Real product dimensions converted to a **body landmark** ("top edge at her collarbone"); "move the camera closer, never enlarge the product"; never size by comparing to another object | F3 |
| Negatives per model | Seedance: negate sources, tracks and defects only (banning a visible object can make it appear); Kling: plain nouns in the negative field, and turn its audio off (it adds music regardless); Google: describe absence positively | F2 F6 F8 |
| Banned words | bokeh, shallow depth of field, 85mm, cinematic, golden hour, ring light, 8K, hyperrealistic, "smiles at the camera", "poses", "obsessed", "game-changer", "This is X, not Y" | F6 F8 |

**Source:** `01` T6–T8, T15–T16, T22; `02` T1–T11; `03` T8–T11; `04` T6–T9; `05` #2–#13.
**Test:** free. Run the linter over past rejected shots and count how many broke a rule.

### #5 Upgraded asset kits (person, product, room) · A
**Person** (`03` T2, `05` #1, `01` T13, `07` #2):
- An **identity plate**: close-up, person only, plain grey, visible pores, **never sent through a model again**.
- A **3-panel sheet**: face in ¾ view / **headless** full-body front / back. One face on the sheet means the model can't average two faces.
- An **angle set** of 4 in the same outfit and light, **including one open-mouth "teeth" frame** (otherwise the first line of dialogue invents a mouth).
- **2–3 deliberate identity markers** (a mole, a specific earring) so drift is visible.
- An **accessory inventory** ("no jewellery").
- A **likeness check** before use: Shein's AI model matched a real person at 99.9%.

**Product / SKU** (`01` T9–T10, `04` T2–T4, T11, `05` #3, `07` #20):
- A **canonical description** written once and pasted verbatim everywhere: shape, fabric weight, fit, closure positions ("front-center zip"), **absent features stated twice** ("no drawcords"), and one honest imperfection.
- Real dimensions.
- **On-body phone photos**, which carry drape and fit better than a flat-lay. HeyGen and FASHN both require one.
- **One reference per state** (sealed mailer ≠ torn mailer, folded hoodie ≠ worn hoodie). "A sheet is not a menu": the model shows whatever the sheet shows.
- ≥4 detail macros (label, print, cuff, rivets).
- A measured colour hex per colourway (models turn navy into black).
- True logo artwork for post patching.
- Shot with the phone's 2×/3× lens, a colour-checker card in the first frame, cross-polarised light for glossy prints and the mailer.
- **Auto-import from Shopify**, as every competitor does.

**Room** (`03` T7, `01` T14):
- 2–3 **real phone photos at ¾ angle** (not frontal).
- A **GEO text block**: anchor objects, which side the window is on, one light source.
- A clutter inventory.
- **No mirrors.**

### #6 Audio: a real human voice, no music, real room · A/B
- **A real person records the script** on a phone (Voice Memos set to Lossless, phone 35–45 cm away, soft room). Use it as the Seedance `@Audio` reference or re-sync with lipsync-2-pro at temperature 0.3. If the persona needs a different voice, convert with **speech-to-speech**, which keeps the real breaths and timing.
- **No music by default.** "Music signals ad." Use "iPhone microphone audio with natural room tone" plus named foley. Kling adds music even when told not to, so turn its audio off.
- **Record real foley once** (the mailer tear, a zip, fleece rustle) and reuse it forever. Unboxing is a format where "the sound is the content".
- **Phone-mic chain** for any clean VO: real room impulse response → high-pass ~150 Hz / low-pass ~7–8 kHz → light pumping compression → room tone at −45 dBFS → AAC. Or **"worldize"**: play it through a speaker in the real room and re-record it on the phone.
- **Brand pronunciation:** spell it phonetically in the spoken line only, and always add "No subtitles."
- For accents, attach a 5–10 s voice sample. Text alone gets an accent right about 1 time in 3.

**Fixes:** F8 F6. **Source:** `07` #14–#19, `01` T17, `03` T24, `05` #9–#10.

### #7 Finish like a phone, not a film · B
- **Phone spec, not film:** slight over-sharpening, luminance noise in the shadows, clipped highlights, one autofocus hunt, crooked horizon, flat and ungraded. **No film grain, halation, bokeh or teal-orange.**
- **Retime floaty clips 1.1–1.25×** (free test in ffmpeg). For fast actions that tend to deform (zip, rip), generate slower and **speed up 1.25–1.5× in post**.
- **Trim 10–15 frames from each end** of every clip. Treat a 15 s render as raw material for 3–5 shots, and **mine failed takes** for 1–3 s inserts.
- **No generative upscaling** for UGC (it adds AI-clean detail). **720p looks the same as 1080p** for phone-style UGC at about half the credits.
- **Logo patch:** planar-track the true artwork back onto the chest print or mailer in post. It's the only method that guarantees a pixel-perfect logo.
- Captions only in post, timed from a Whisper transcript, inside the safe zone (top 14%, bottom 20–35%, sides 6% kept clear).

**Fixes:** F6 F2 F9. **Source:** `03` T12–T14, `05` #15–#16, `07` #6, `04` T19–T20.

---

## 2. Full ranked technique list

The technique numbers in each row point to the detailed write-ups in the linked research reports. "Cost" is the cheapest test in credits. 0 means free: a prompt, lint, post-processing or phone capture.

| Rank | Technique | Fixes | Ev. | Cost | Where |
|---|---|---|---|---|---|
| 1 | Board → one Seedance omni-reference call, `Hard cut to.` | F1 F2 F7 F9 | A | ~1 video + 2 images | 01 T1, 06 T1 |
| 2 | Real body plate + identity swap (Ad Multiplier / Genjutsu / Wan Replace) | F2–F7 | A/B | 0 capture + 1 swap | 07 #1, 01 T21 |
| 3 | Approved composite still gate, 4 variants, masked point edits only | F1 F2 F3 F6 F9 | A | ~6 | 04 T1, 03 T3 T5 |
| 4 | De-slop realism pass on every board/keyframe (**edit out "keep product unbranded"**) | F6 F1 | A | 1 image | 01 T5, 06 T3 |
| 5 | Anti-morph cadence (adjacent shots differ in POV and distance) | F1 F7 | A | 0 lint | 01 T2 |
| 6 | Hand-count law + `camera_holder` + two-hands sentence | F3 | A | 0 lint | 01 T7, 03 T8, 04 T6 |
| 7 | One state per cut; change on the cut; next shot restates the state; one reference per state | F4 | A | 0 lint | 01 T3, 05 #3 |
| 8 | SPEAK vs DO beats, never both; VO over hand shots | F8 F3 | A/B | 0 | 03 T11, 04 T8 |
| 9 | Reference role + exclusion lines; "one single hoodie"; ≤8 references | F1 F2 F7 | A− | 0 | 02 T1–T3, 05 #2 |
| 10 | Canonical SKU description + garment lock + realistic-fit sentences, verbatim | F2 F5 | A | 0 | 01 T9 T10 |
| 11 | Identity plate + headless 3-panel sheet + angle set with teeth view | F1 F8 | A−/B | ~5 | 03 T2, 05 #1, 01 T13 |
| 12 | On-body phone photos per SKU (not just flat-lays) | F2 F5 | A | 0 + 3 | 04 T2, 03 T4 |
| 13 | Realism block at the start of the prompt; no booster words; located imperfections | F6 | A− | 0 | 02 T10 T19, 05 #11 |
| 14 | Kill slow motion: ban it by name, counted beats, fit the duration, retime | F6 | A | 0 | 03 T13, 02 T11 |
| 15 | Human VO → `@Audio` reference or re-sync; speech-to-speech for the persona voice | F8 | A/B | 1 video | 07 #14–16, 05 #10 |
| 16 | No music; room tone; real foley library; phone-mic chain / worldizing | F8 F6 | A/B | 0 | 07 #17 #19, 03 T24 |
| 17 | Script linter: word budget, banned openers and AI phrases, spoken register, specificity | F8 | A | 0 | 01 T16, 06 T13, 04 T9 |
| 18 | Scale as a body landmark from real dimensions | F3 | A/B | 0 | 01 T8, 05 #6 |
| 19 | Kling try-on rules: base already wears the same garment category; bottoms full-length with a long top | F2 F5 | A | ~6 | 04 T3 |
| 20 | Logo/print detail insert, where the print fills a big share of the frame (or a real insert); small logos never in wide or moving shots | F2 | A | ~3.5 | 04 T4, 01 T9 |
| 21 | Hand-free fabric macros with one passive motion cue per fabric | F5 F3 | A | ~3.5 | 01 T11, 06 T6 |
| 22 | No mirrors or reflections ("limb factory"); propped phone instead | F3 F7 | A | 0 | 01 T12 |
| 23 | Room plate at ¾ + GEO block + anchor object + clutter inventory + "do not use the people" | F7 | A− | 0 | 03 T7, 01 T14 |
| 24 | Mid-event first frame; first word within 0.4 s; loop ending, no CTA tail | perf, F6 | A | 0 | 01 T18, 06 T12 T19 |
| 25 | Repair with Seedance 2.5 edit (keep-list template) before re-rolling | F9 F2 | A− | 1 edit | 02 T16 |
| 26 | Lip-sync repair layer (lipsync-2-pro, temperature 0.3, occlusion on) instead of re-rolling | F8 F9 | A | pennies | 07 #16 |
| 27 | Logo patch in post (planar track the true artwork) | F2 | A (VFX) / C (AI) | 0 | 07 #6 |
| 28 | Phone finish profile; no film grain; 720p; no generative upscaling; trim ends; splice takes | F6 F9 | B | 0 | 03 T12 T14, 05 #15–16 |
| 29 | `get_cost` preflight + ledger (prompt diff, model, seed, verdict) + stop after 5 rerolls → simplify the shot | F9 | A/B | 0 | 01 T20, 03 T18 |
| 30 | Free auto-QA: face similarity, product similarity + colour difference + logo OCR, hand count, Whisper vs script, sync score ≥3, duplicate-frame and burned-in text checks | F1 F2 F3 F8 F9 | B | 0 | 05 Auto-QA |
| 31 | Model routing by shot type (see §4); lock one model per ad for persona shots | F9 F6 | B/C | bake-off | 02 routing, 07 #5 |
| 32 | Product-driven formats (fit check, fabric close-up, "3 ways to wear"), not first-person testimonials | F9, legal | A | 0 | 04 T14–15 |
| 33 | Hook library from TikTok Creative Center (Apparel, sorted by 6 s view rate) | perf | A/B | 0 | 06 T17 |
| 34 | Cheap derivatives from every ad (Post-It / meme text formats, the top Meta format for fashion) | F9 | A | 0 | 06 T23 |
| 35 | Gaussian-splat scan of the rigid mailer for exact-angle start frames | F2 F9 | B/C | 0 | 07 #7 |
| 36 | FASHN VTON 1.5 (the only commercially licensed open try-on) for garment keyframes | F2 F5 | B | ~$1 GPU | 05 #17 |

**Added from the podcast/YouTube research (`08`)**, mostly from Higgsfield's official YouTube episodes:

| Rank | Technique | Fixes | Ev. | Cost | Where |
|---|---|---|---|---|---|
| 37 | **Phone rehearsal → LLM writes the prompt second by second from the clip.** "Greybox = timing and path. References = identity and set. Mixing those jobs in one text prompt is how seats swap and hands melt." Store movement-library clips at the final shot length. | F3 F4 F7 F9 | B | 0 + 1 video | 08 #9 |
| 38 | **Blur small print in the product references** (care labels, size tags, tiny woven text): "short text survives, long text dies". Add a per-SKU `must_survive_marks[]` list checked on every take. | F2 | B | 0 | 08 #6 |
| 39 | **State changes behind something that hides the body, in timed windows** (official jersey ad: one reference image per look plus a second window, e.g. 0–3 s / 4–6.5 s / 7.5–13 s; change only while something covers the body, such as a hand over the lens, a door frame or a whip-pan; "a visible morph is a failed take") | F4 | B | 1 video | 08 #7 |
| 40 | **Paste the real face and real product into sheets** instead of letting the model redraw them (official love-story episode, 500M views) | F1 F2 | B | 0 + 1 video | 08 #12 |
| 41 | **Scale reference photo**: a real photo of a hand holding the folded tee or mailer at true size, tagged as the scale reference; fix hands on start frames in Photoshop | F3 | B | 0 | 08 #11 |
| 42 | **Face pack for Seedance: ≤3 stills, same session, same expression** ("expression variety → the model averages a midpoint face") | F1 | B | 0 | 08 #19 |
| 43 | **Finish:** trim or grade Seedance's over-exposed first frames; grain 2% (3% in dark scenes); 30 fps; retime **with the audio detached** (or it pitches up); optionally a second lossy pass (messenger recompression) | F6 | B/C | 0 | 08 #16–17 |
| 44 | **Hybrid real talking track + AI b-roll**: a real person's 15–30 s talk, cut every 4–6 s into AI try-on and product b-roll. Dara Denney says AI *voice-overs* pass as real but full AI avatars "still get punished". | F1 F6 F8 | B/C | 0 + b-roll | 08 #24 |
| 45 | **Use the video model as a turnaround generator**: a slow orbit of the model wearing the SKU, with frames extracted as matching multi-angle stills | F1 F2 | B/C | ~3.5 | 08 #23 |
| 46 | **Route handheld walk-and-talk to Kling** (Seedance's handheld looks "like a phone gimbal trying too hard"; Kling's has weightier micro-jitter); big physical actions to Seedance | F6 | C | bake-off | 08 #17 #21 |

---

## 3. Failure → fix map (what fixes each problem we keep hitting)

| Failure | Strongest fixes (in order) |
|---|---|
| **F1 face drift** | One-call board (#1) · identity plate never re-run + headless sheet + teeth view · reference roles with "do not use its person" · identity markers · face-similarity QA |
| **F2 product drift** | Real plate (#2) · canonical description verbatim + garment lock · one reference per state · on-body photos · detail insert for logos · never let the model *write* brand text · logo patch in post · colour hex + ΔE check |
| **F3 hands / scale** | `camera_holder` + hand law · two-hands sentence · SPEAK vs DO · body-landmark scale · props rest on surfaces · hands-off fabric macros · real plate for hand-on-product beats |
| **F4 state changes** | Hide the change in a hard cut (the vendor never shows it) · or "before → sound → after" · or a real plate of the real action · if shown: 5-part causal chain (structure → anchor → force → material reaction → end state) · never invent a tear strip the reference doesn't show |
| **F5 fabric / fit** | Real plate for fit-critical SKUs (`fit_critical` flag) · on-body photos · Kling try-on base-garment rule · physical-spec sentence · realistic-fit clause · calm camera · passive fabric cues |
| **F6 AI look** | De-slop pass · realism block at the start of the prompt · iPhone optics (23 mm, deep focus, sensor noise) · no bokeh/cinematic/golden hour · no slow motion + retime · phone finish · unposed, mid-action body language · ordinary casting |
| **F7 room warps** | One-call board · room plate at ¾ + GEO block + "do not use the people" · counted props · no mirrors · no legible text on props |
| **F8 audio** | Human VO / speech-to-speech · SPEAK beats only, frontal or ¾ · word budgets, ≥8 words per 4 s · ≤8 s talking per generation · no music · room tone + foley · phonetic brand spelling + "No subtitles" · lip-sync repair |
| **F9 credits** | Iterate on stills · `get_cost` · 720p · edit instead of re-roll · mine failed takes · ledger + 5-reroll stop · free auto-QA before paying · cheap draft rough cut first |

---

## 4. Model routing by shot type (current best evidence)

| Shot | First choice | Avoid / fallback |
|---|---|---|
| Whole 15 s UGC ad | **Seedance 2.5 omni_reference from a board** (Higgsfield's own choice) | Sora 2 (its API shuts down today) |
| Talking head (lip-sync) | Seedance 2.5 (when product and room references are needed); Kling 3.0 Turbo (budget lip-sync) | Wan 3.0 (weak lip-sync) |
| Hands + product | **Real plate + swap** → else Kling 3.0 image-to-video, cfg 0.7–0.8 | Wan 3.0 (soft hands) |
| Garment on body / fit | **Real plate + swap** → else Seedance with multi-angle garment references | Generating fit-critical beats from scratch |
| Unboxing / mailer | Hidden in a hard cut; or a real plate of the tear | A long single take over 10 s |
| Walk / lifestyle | Kling Motion Control with a reference framed to match | Close-up persona image with a full-body motion reference |
| Product B-roll (no people) | Wan 3.0 (cheapest), checking for invented logo details | — |
| Fixes | Seedance 2.5 edit (source ≤20 s); lipsync-2-pro for mouths | Re-rolling the whole clip |

All comparisons except the vendor-recipe rows are grade C. A small internal bake-off would settle them for our shot types: 3 shot types × 3 models × 2 seeds.

---

## 5. STOP DOING (merged from all eight reports)

1. **Generating shot by shot and stitching** when one board → one call keeps identity, product and room shared.
2. **Putting the product in the person/character image.** It breaks compositing and makes the product drift.
3. **Running an image through a model repeatedly** (a Nano Banana edit on a Nano Banana edit). Faces turn plastic after about 2 passes.
4. **Showing state changes on camera** (ripping, pulling on, zipping) or two states in one cut.
5. **Mirrors, mirror selfies and reflective surfaces** (a "limb factory"). This rules out the Skims mirror grammar for AI shots.
6. **Hands touching fabric in close-ups**, "holding the hoodie up to camera while talking", and dialogue during hand action.
7. **Bokeh / shallow depth of field / 85mm / cinematic / golden hour / ring light / film grain / 8K / hyperrealistic** in UGC prompts.
8. **Slow motion by default.** Ban it by name, and don't give a 3 s action 8 s of runtime.
9. **Filling every reference slot**, collage product sheets, or several product views without the "one single object" line.
10. **Negating visible objects on Seedance** ("no blur", "don't show hands"), and writing "no X" in Kling's negative field.
11. **Re-describing what a reference or keyframe already shows**, and paraphrasing the product description between shots.
12. **Letting the video model render text**: logos, captions, prices, prop labels. Small logos come out as gibberish or as a competitor's brand.
13. **Lines of ≤6 words in 4 s**, talking over 8 s per generation, line-by-line TTS, music with lyrics, and music by default.
14. **Clean LLM scripts** ("obsessed", "game-changer", "Okay so…", "This is X, not Y"). The script is the #1 tell viewers name.
15. **Paying for 1080p/4K or upscaling UGC.** 720p looks the same, and generative upscalers add the clean AI look.
16. **Re-rolling a whole clip for one local defect.** Edit the span, re-sync the lips, or patch the logo instead.
17. **Mixing video models inside one ad for persona shots.** Coca-Cola's 70,000 clips across 3 models still looked inconsistent.
18. **Emotional first-person "I bought this" testimonials from AI people.** They are the weakest format in the independent studies, and a disclosure and misleading-endorsement risk.
19. **Hiding or stripping AI labels or C2PA metadata.** TikTok detects it and requires the label (and says labelling doesn't reduce reach). NY law since June 2026; EU AI Act since August 2026.
20. **Using non-commercial tools in ads** (CatVTON, IDM-VTON, OOTDiffusion, and InsightFace's pretrained weights).

---

## 6. Cutroom v2 pipeline (what the product becomes)

1. **SKU intake:** import from Shopify → the app asks only for what's missing (on-body photos, detail macros, per-state photos, dimensions, colour-card frame, logo artwork). Write the canonical description once, then lock it. Set the `fit_critical` flag.
2. **Persona intake:** identity plate → 3-panel headless sheet → angle set with a teeth view → markers + accessory inventory → likeness check → voice (a real recording, or a clone from casual speech).
3. **Room intake:** 2–3 photos at ¾ angle, GEO block, clutter inventory, room tone + clap impulse-response recording.
4. **Script:** hook from the hook library → script linter (word budget, spoken register, banned phrases, no first-person purchase claims) → SPEAK/DO beats.
5. **Storyboard:** a shot spec per beat (camera holder, hands, POV/distance, states, speech mode, seconds, motion speed). **The linter blocks spend when a rule fails.** Beats that are fit-critical or physical are routed to **Plate + Swap** and the app shows the plate spec.
6. **Board / keyframes:** 4 variants → pick → masked point fixes → de-slop pass (brand clause edited) → free still QA (face, product, hands, scale, colour) → human approve.
7. **Rough cut (cheap):** keyframes plus Wan drafts, watched as a whole ad before paying for hero renders.
8. **Final render:** `get_cost` → one Seedance 2.5 omni-reference call per 15 s at 720p, with an `@Audio` human VO where lip-sync matters. Plate + Swap for physical beats.
9. **Video QA (free):** frame sampler + per-frame face and product curves, hand-count series, Whisper vs script, sync score, burned-in text, duplicate frames. A vision model triages which seconds a human checks first; a human decides.
10. **Repair, not re-roll:** Seedance edit span → lip re-sync → logo patch → only then re-roll, max 5, then simplify the shot.
11. **Finish:** trim ends, retime, phone finish profile, audio chain + foley + room tone, captions from the transcript inside the safe zone, AI label on, C2PA kept.
12. **Learn:** the ledger records every generation and its verdict. Rejection reasons feed rule-mining, and keep rates per shot type update the routing table.

---

## 7. Test plan: prove it cheaply before building

**First, resolve cost (free):** your notes say Seedance is about 18 credits, but a validated community run logged **~67 credits for 15 s at 720p with audio, and ~135 at 1080p**. Call `generate_video` with `get_cost:true` for each test below before running it.

| # | Test | What it proves | Credits (est.) |
|---|---|---|---|
| T0 | Linter over past rejected shots | How many failures the rules would have caught | 0 |
| T1 | Retime 5 existing floaty clips 1.1/1.2/1.3× + trim ends + phone finish; blind A/B with 5 people | The free post wins | 0 |
| T2 | Re-cut 5 rejected renders for usable 2–4 s segments | Salvage rate | 0 |
| T3 | Record real foley + room tone + a human VO; worldize it | The audio lift | 0 |
| T4 | De-slop pass on 2 existing keyframes (brand clause edited): does the logo survive? | Can #4 be adopted for SANTO? | ~2 images |
| T5 | **8-slot board → one Seedance 15 s call** (hoodie fit-check template, `06` §template) vs our current best stitched ad | The architecture change (#1) | board + 1 video |
| T6 | **Film a 6 s hoodie pull-on and a mailer tear on a phone → Genjutsu / Ad Multiplier swap** | Plate + Swap (#2) | 1–2 swaps |
| T7 | Same shot with `@Audio` human VO vs native TTS | Voice realism | 1 video |
| T8 | 4-slot vs 8-slot board for print legibility; small chest logo vs big back print | Logo limits | 2 videos |
| T9 | Mailer: hidden in a cut vs 5-part causal chain vs real plate | The F4 route | 2 short videos |
| T10 | Bake-off: 3 shot types × Kling / Seedance / Wan | Routing table | 150–250 |

Run T0–T4 this week for close to 0 credits. Then T5 and T6 are the two tests that decide the new architecture.

---

## 8. Contradictions between sources (settle by test, not opinion)

1. **One 15 s call vs short 3–5 s clips.** Higgsfield's recipe uses one 15 s omni-reference call with internal cuts. OpenAI, ByteDance and practitioners say shorter clips drift less. They're reconciled by the board: internal cuts are ~2 s each. Test T5.
2. **Show the pull-on vs hide it.** The MCP try-on recipe hides it behind a cut. Higgsfield's Marketing Studio PDF shows a t-shirt pull-on in a 4 s static full-body clip. Fazi's ad shows a hoodie *off* at the end of a block. Default to hiding it; test showing it.
3. **Grid board vs separate reference images.** Higgsfield and joebenscoter use a board; the gbeyrouti skill says separate images align better for exact composition. Test T5 vs our current approach.
4. **Seedance 2.5 resolution on Higgsfield.** The catalogue says 1080p, but ByteDance's API is natively 720p (higher tiers are upscales). Irrelevant if we default to 720p.
5. **The de-slop prompt says "keep product unbranded".** That contradicts the recipes' own label rules. Edit the clause and test (T4).
6. **Film grain.** Tutorials say add it; Higgsfield and the shipped UGC ad ban it. Use sensor noise, not film grain.
7. **Higgsfield's "beauty floor"** (its creator presets require model-attractive, symmetrical features) works against the "ordinary person on a phone" goal. Override the casting and keep the skin-texture anchors.

---

## 9. Where ideas come from: channels to keep mining

This is the list of ways to find new ideas you asked for, ranked by signal per hour.

| Channel | What to pull | How | Cadence |
|---|---|---|---|
| **Higgsfield MCP workflows** (`get_workflow_instructions` for ugc-try-on, ugc-unboxing, ugc-review, ugc-product, ad-multiplier, character-sheet) | Version bumps, new rules, new model routing | Free read-only calls; diff against `research/raw/hf-workflows/` | **Weekly** (highest signal, free) |
| **Higgsfield `models_explore` + presets** | New models, new parameters (start/end frames, edit modes, audio refs) | Free | Weekly |
| **GitHub skill libraries**: OSideMedia/higgsfield-ai-prompt-skill, LearnPrompt/awesome-seedance (497 verified cases, synced daily), gbeyrouti/seedance-prompting-claude-skill, joebenscoter86/higgsfield-ugc-workflow, smixs/visual-skills, krusemediallc/arcads-claude-code | Measured failure modes, validated templates | `git pull`, diff | Bi-weekly |
| **YouTube tutorials + podcasts** | How practitioners explain their workflows | `research/tools/harvest_transcripts.py` (run locally), then have Claude extract techniques | Monthly |
| **TikTok Creative Center Top Ads**: Apparel & Accessories, UK+US, sorted by 6 s view rate | Hooks, first-3-second frames, second-by-second retention curves | Manual, or an Apify actor | Weekly |
| **Meta Ad Library**: Gymshark, Oner Active, Represent, Skims, Corteiz | Ads running 30+ days (≈ winners): cut count, hook, text | Manual / swipe tools | Bi-weekly |
| **Our own ledger** | Keep rate per shot type × model × prompt feature; top rejection reasons | Cutroom's generation log | Continuous |
| **Higgsfield community feed** ("Recreate" shows the full prompt) and **Google Flow TV** (shows every clip's prompt) | Prompt → output pairs | Manual / API | Monthly |
| **Vendor docs changelogs**: Kling quickstart, BytePlus Seedance, Google Veo/Nano Banana guides, OpenAI cookbook, sync.so, ElevenLabs | New knobs | Manual (blocked from this cloud session; read locally) | Monthly |
| **Research papers**: Spotlight, Skyra, Artifact-Bench (what gives AI video away) | New tells → new countermeasures and QA checks | arXiv / GitHub | Quarterly |
| **Contests and galleries**: Higgsfield Adathon, Kling/Seedance contests | What judges reward as "realism" | Manual | Per contest |
| **Higgsfield Academy** "Build a Brand's Visuals with AI" (a fictional clothing brand, with lessons on try-ons, packaging and unboxing) | Our exact use case | Watch manually (free) | Once, then per update |
| **Communities**: Higgsfield Discord, AI Video Bootcamp, Ryan Collins' Skool, Dan Kieft | "Post your work" threads with prompt + output + critique | Human membership | Opportunistic |
| **Adjacent industries**: VFX (logo replacement, compositing), virtual-influencer studios, e-com photography, film sound (worldizing) | Solutions already proven elsewhere | Search + interviews | Quarterly |
| **Blind viewer tests** (5–10 people: "real or AI?") | The real "looks human" metric | In person / a form | Per major change |

---

## 10. Compliance (affects formats and scripts)
- **TikTok:** AI-generated realistic people need the AIGC label; C2PA is auto-detected; TikTok says labelling doesn't reduce distribution.
- **Meta:** labels automatically from C2PA.
- **Disclosure laws:** New York has required disclosure of synthetic performers since 9 Jun 2026. The EU AI Act's Article 50 has applied since 2 Aug 2026.
- **UK ASA:** misleading-testimonial rules apply to synthetic people.
- **Scripts:** write them as phone-filmed product demos ("this is the 400gsm one, look how thick"), never a synthetic person claiming "I bought this".
- **Paid-ad audio:** trending TikTok sounds aren't licensed for paid ads. Use the Commercial Music Library or original audio.
- **Open question:** which markets SANTO advertises in decides which laws apply.

---

## 11. Gaps in this research (for round 2)
- Reddit and X threads were unreachable, so viewer-tell evidence comes through summaries. A human skim of r/FacebookAds "AI UGC" threads would firm this up.
- No independent evidence on leggings or denim physics beyond "use real on-body references"; needs a squat/lunge test per model.
- Costs of Genjutsu, Ad Multiplier, Marketing Studio, gpt_image_2 boards and Seedream de-slop aren't exposed by `models_explore`. Use `get_cost`.
- The Higgsfield Academy lessons and Genjutsu cost guide couldn't be fetched from this session.
- Full YouTube and podcast transcripts: run the harvester locally (steps in chat); `08-podcasts-youtube.md` has the summary-level findings. `research/harvest-urls.txt` lists 64 of the most useful videos and episodes; run `python3 research/tools/harvest_transcripts.py --list research/harvest-urls.txt --max-priority 1` first.
- Two podcasts need a human to watch them: the fal Podcast with Tim Simmons (`deQNOjnDcwY`) and AI For Humans (`EA3PGSRotwc`).
- Higgsfield's Blender plugin mentions an "Anti-Slop" mode for Seedance 2.5; what it does is unknown.

---

## 12. Round 2: what 27 full YouTube transcripts added (`09a`, `09b`, `09c`)

These are 27 transcripts downloaded with the harvester and read in full. The best sources were `M73BrFnVPA8` (a Higgsfield power user), `eflfUwTdSEc` (Seedance 2.5 long takes), `lkL8mlpVScY` (a Seedance creator whose clip fooled a friend), `Xcg8aklWBGM` (OpenArt Seedance 2.5 UGC) and `b_RghITuQQM` (Kling 3.0 limits). Most of the others were UI tours or sponsored. Everything here is grade B/C (single creators); timestamps are in the 09 files.

### 12.1 Upgrades to the top 7

- **#1 one-call board → also attach a still per cut.** Make cut 1's still the start frame, and send the character sheet, room and **the other cuts' stills** as references. With only the sheet and room, "framing drifts long before your character does" (`M73BrFnVPA8 @07:56`). This settles contradiction §8.3: use the board *and* per-cut stills. Keep to 4–8 cuts per 15 s; 7 or more starts to over-compress.
- **#4 linter → new hard limits:**
  - **Prompt caps are silent.** Seedance truncates at **~2,500 characters** and Kling multi-shot at **~500 per shot** (`tfs8U3CbAOs @07:34`, `k6jn5xjqYSo @07:44`). Long lock/negative blocks at the end may never reach the model. That's one more reason the realism and lock text goes at the **start**.
  - **Upload order must match the @Image numbering**, or roles swap and the room gets treated as a character (`kC12eMs0SF0 @08:07`).
  - **Kling dialogue:** speech first, action last. Lip-sync drifts in the last ~5 s of a 15 s clip, with a hard ceiling around 10 s (`z84WQAn6U0I @03:06`, `b_RghITuQQM @22:41`). Kling multi-shot allows ≤6 shots, ≥3 s each, one action + one camera move per shot, and no multi-shot when both start and end frames are set.
  - **Never name camera gear in the visual prompt.** "FPV drone" puts a drone in frame, and a fixed pose gives "a mannequin" (`M73BrFnVPA8 @09:36`). Describe the vantage point and ongoing activity, not "phone/tripod/selfie stick". This matches Higgsfield's own ban on "phone in her hand".
  - **Explain why there's one camera.** Seedance invents extra angles unless told "one continuous shot because I'm holding the camera" (`lkL8mlpVScY @18:52`).
- **#3 stills → three new rules:**
  - **Add a relight line** to every composite/keyframe, written from the room's light source. Otherwise the flat-lit sheet "looks edited" (`M73BrFnVPA8 @03:37`).
  - **Make the "after" state by editing the "before" image** (the torn mailer from the sealed-mailer still, the worn hoodie from the pre-wear still) and attach both. Generated separately "they just come out as two different rooms" (`eflfUwTdSEc @13:04`).
  - **Build the end frame from the approved start frame**, with "match exactly" as the first line.
- **#5 person kit → real close photos beat sheet-only personas.** Include a side or back view and reject distant photos, because the model invents skin and moles. Build the sheet *from* real close photos and send the real photo alongside it (`lkL8mlpVScY @20:55–23:29`). Train Soul ID on flat, boring angles, since it learns dramatic lighting (`M73BrFnVPA8 @14:48`). Strip small accessories from sheets.

### 12.2 New techniques

| # | Technique | Fixes | Source |
|---|---|---|---|
| 47 | **Write a state change as fixed states:** "fully covered by X / changed the instant X comes away / changed from then on", plus "the only torn thing is…". For the mailer: "sealed while in her lap / open the instant her hands lift away / open from then on". | F4 | `eflfUwTdSEc @12:02` |
| 48 | **Anti-easing line whenever an end frame is locked:** "already at full speed in the first shot… no deceleration… still going as the last one ends". Otherwise the subject slows and "poses" at the end. | F6 F4 | `M73BrFnVPA8 @12:44` |
| 49 | **"Casual multi-camera TV shoot… fixed tripod angles joined by hard cuts, no zooms"** got Seedance to auto-cut 7 consistent angles from one prompt with no board, and tripod framing frees both hands. It's a cheaper board-free route worth A/B testing against #1. | F1 F3 F7 F9 | `eflfUwTdSEc @09:11` |
| 50 | **Start/end frames must be physically reachable:** every object needs a real path, on the same plane and in the same positions, or it melts through things. 5 s beats 10 s for the same pair. | F4 F7 | `aw6N7M4fPuo @02:33` |
| 51 | **Render +2 s longer than the script, then trim**, so the last action and line aren't cut off. Pad the whole clip, never a single action. | F8 F9 | `Xcg8aklWBGM @06:13`, `kC12eMs0SF0 @09:41` |
| 52 | **Scripted personal habit + written pause** ("looks off frame slightly, which is a thing I often do") in a 7 s single take. This was the clip that fooled a real person. | F6 F8 | `lkL8mlpVScY @21–23` |
| 53 | **Declare invariants once; only the touched object moves.** Write a camera reveal as an ordered list of what enters the frame. | F7 | `09b` F-4, F-5 |
| 54 | **Counted foley tied to contact events** ("two rustles as the hoodie lands on the bed"), with in-scene and added sound kept separate. | F8 | `09b` F-12 |
| 55 | **Audio-first gate:** approve the voice track before any video spend. | F8 F9 | `09c` C-18 |
| 56 | **"Action mapping" (Kling):** cover one physical action from 4–5 angles in one multi-shot, re-run with identical inputs, and splice the best bits. Use Kling multi-shot to *find* shots and single shots for keepers ("one great shot out of five"). | F9 | `Z3vY2U8ysL0 @05:47`, `BJ9H0Dq72lY @11:04` |
| 57 | **Colourway swap from one edited frame:** make one hoodie-colour variant by editing a single frame, then carry it through. | F2 F9 | `09b` F-16 |
| 58 | **Check Higgsfield reference eligibility before planning.** Some references fail the Seedance gate, and building a shot around them wastes credits. | F9 | `ez8gfygg8ho @04:07` |
| 59 | **Bring the persona in through the Higgsfield MCP as an uploaded Marketing Studio avatar**, not a Soul character called by name. Reported as more stable. | F1 | `wc4VOgT7S58 @01:33` |
| 60 | **Hands-only first-person POV:** face banned, "slow steady glide" rather than bare "handheld", which over-shakes. | F3 F6 | `eflfUwTdSEc @03:26` |

### 12.3 Cost data (it replaces the "~18 credits" assumption)
- **Seedance standard on Higgsfield ≈ 6 credits per second** (66 credits for 11 s) (`tfs8U3CbAOs @05:58`). **Seedance Fast is half the price at the same 720p**, so use it for iteration (`@03:48`). Community run: ~67 credits for 15 s at 720p with audio.
- **Seedance 2.5, 8 s at 480p ≈ 20 credits:** use it as a motion "proof render" before paying for a final (`M73BrFnVPA8 @16:51`).
- The same 5 s shot costs **15 vs 110 credits** depending only on resolution and audio (`M73BrFnVPA8 @16:21`).
- So the realistic budget for a finished 15 s ad is: a 480p/Fast proof (~20–45 credits) + one 720p final (~90 credits) + stills (~10–20 credits).

### 12.4 Contradictions resolved
| Topic | Creators say | Keep for SANTO UGC |
|---|---|---|
| Style block at the bottom (`kC12`) | Put it at the end | **Start.** Seedance reads the start, and the end is what gets truncated |
| Upscale / 1080p / 4K (several) | Upscale later | **720p, no generative upscale.** An open test: 480p + ByteDance "AIGC" upscale vs native 720p in the blind test |
| Music (`kC12`, `goZDcGw`) | Add background music | **No music by default** (film context vs UGC) |
| Shallow DoF, film grain, 35 mm f/1.8 (`k6jn`, `Zo8K`, `M73B`) | Realism | **Banned for phone UGC.** Keep only their method: ban unwanted qualities by name |
| LLM re-describes the approved still (`o-xhRksFBAc`) | "Bring the image to life" | **Describe motion and sound only** |
| Showing a state change on camera (`eflfUwTdSEc`) | Works as a long take | **Only behind something that hides it**, with fixed-state wording (#47) + before/after plates. Test on the mailer |
| Kling multi-shot one-call | Consistent from one reference | Cheaper alternative route; add it to the T10 bake-off |
| Sheet model (GPT Image 2 vs Seedream 5 Pro) | Split | 2-image A/B on the SANTO persona |

### 12.5 Added to STOP DOING
21. Locking an end frame without the anti-easing line.
22. Naming camera gear in the visual prompt.
23. Scripting dialogue to the exact render length (pad +2 s).
24. Trusting Kling's "no dialogue" or "no music" negatives. Turn audio off.
25. Prompts over ~2,500 characters (Seedance) or ~500 per shot (Kling). Text past the limit is silently lost.
26. Training Soul ID on dramatic or rim-lit photos.
27. Following "golden hour / warm cinematic" Veo recipes from tutorials for UGC.

---

## 13. Tools built from this playbook (free, in `research/tools/`)
- **`prompt_linter.py`**: the §1 #4 rules as code. Run it before any paid call; exit code 1 = don't spend. `examples/good_fitcheck.json` is a ready 15 s SANTO fit-check (8 cuts, 32 words, 2,183 characters) that passes. `bad_fitcheck.json` shows 15 caught errors.
- **`phone_finish.py`**: §1 #7 + §12.3 as one command (trim head/tail, pitch-safe retime, handheld drift, phone sharpening, sensor noise, 30 fps, phone-mic audio chain, real room tone and room reverb, optional messenger pass).
- **`qa_frames.py`**: the free parts of #30 (contact sheet, cut count vs plan, duplicate/frozen frames, hot first frames, dead air, and the human checklist). Run it on raw generations.
- **`harvest_transcripts.py`** + `research/harvest-urls.txt`: YouTube knowledge mining.
- See `research/tools/README.md`. Next research round (Mac-only sources): `research/ROUND3-LOCAL-BRIEF.md`.

**Tension to watch:** Higgsfield's own recipes write dense per-cut prompts ("4–10 sentences per cut"), but Seedance silently cuts off anything after ~2,500 characters. The linter's example fits 8 cuts in 2,183 characters by keeping each cut to one or two sentences and putting realism and locks first. If Higgsfield's MCP route turns out to accept longer prompts, raise the cap in `PROMPT_CAPS`.

---

# PART 2 — `BRIEF.md`

## Shared research brief — read fully before starting

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

---

# PART 3 — `01-higgsfield.md`

## 01 — Higgsfield ecosystem: internal recipes, model facts, community repos

Researcher scope: Higgsfield's own MCP workflow bundles (read-only calls only), `models_explore`, Higgsfield blog/help pages (via WebSearch summaries), and GitHub repos built around Higgsfield. **No credits were spent.** Date: 2026-09-24.

Evidence key: **A** = official vendor material (here, mostly Higgsfield's own shipped workflow code, read directly) or several independent practitioners. **B** = one credible practitioner with shown results. **C** = claim or anecdote.

Raw extracts are saved in `research/hf-notes/` (`notes1.md` plus full bundle files under `tryon/`, `unboxing/`, `review/`, `product/`). Cloned repos are in `research/repos/`.

---

## 0. The big picture (read this first)

Higgsfield ships its own UGC pipelines inside the MCP server as "workflows": `ugc-review-video` v1.1, `ugc-unboxing-video`, `ugc-try-on-video`, `ugc-product-video`, `ugc-tutorial-video`, `product-photoshoot`, `character-sheet`, and `ad-multiplier` v1.4. All four UGC video flows use **the same pipeline**, and it differs from what Cutroom does today:

1. **Creator:** one `soul_2` still (3:4, 2k), **person only, no product**. It becomes `character_media_id` and is reused unchanged for every board and every clip.
2. **Storyboard board:** one `gpt_image_2` image (21:9, 2k, quality high) that holds **4 or 8 equal vertical 9:16 "slots" in one row**. Each slot is one beat of the 15-second clip. The references go in as `[product, character, (real package photo), (previous cleaned board)]`, and the prompt opens with `@Image1/@Image2…` declarations in that same order.
3. **Mandatory "de-slop" pass:** `seedream_v5_pro` image-to-image on every board, with a fixed prompt that changes only micro-realism (pores, sensor noise, flat iPhone look, deep focus).
4. **One video call per 15 s:** `seedance_2_5`, `mode:"omni_reference"`, `generate_audio:true`, 9:16, 1080p, duration ≤15, with medias `[clean board, character, product]`. The prompt is a dense per-cut script with `Hard cut to.` markers, so **the 4 or 8 board slots render as internal hard cuts inside one generation**. Speech, lip-sync and room tone come natively from the same call.
5. **Frozen-frame QA** on stills. If a clip fails, only that clip is re-rolled. If the video is longer than 15 s, clips are joined with `ffmpeg -c copy`, hard cuts only.

The same design shows up in a community repo that was "reverse-engineered from a single autonomous run of Higgsfield's agent" (joebenscoter86, with a 3-panel variant), which independently confirms it. **The single strongest input change for Cutroom is to stop generating shot-by-shot clips from separate frames and move to this pattern: a board sheet as reference, one omni-reference Seedance call per 15 s, cuts inside the call.**

---

## 1. Techniques

### T1. Storyboard board as the video reference: one 15 s Seedance call with internal hard cuts
- **What / how:** Build one 21:9 sheet with N equal 9:16 slots in ONE row, separated by thin white gutters. There is no text anywhere on the sheet ("no baked slot labels"). Higgsfield's slot counts are **8 for talking-head review and try-on, and 4 for unboxing and product-only**. Pass the sheet plus the character plus the product as references to `seedance_2_5` `omni_reference`. The clip prompt maps Cut n → slot n, with cumulative timestamps (`Cut 1 (0-1.9s) … Hard cut to.`). There are exactly N−1 `Hard cut to.` markers and none after the last cut. Higgsfield's note: *"These are scene-edit instructions Seedance reads literally. Without them, cuts collapse into smooth motion."*
  - Time splits from the workflows. Try-on at 15 s: 1.9 / 2.3 / 1.9 / 1.4 / 1.9 / 1.4 / 2.3 / 1.9 (the macro cuts are shortest; the reveal and style cuts are longest; every cut ≥0.5 s). Unboxing at 15 s: 3.5 / 4.5 / 3 / 4.
  - Durations: 4–15 s = 1 board. 16–19 s = 2 boards balanced so each is ≥4 s. 20–30 s = 15 + remainder.
  - The board is a **narrative map, not a frame template.** *"If your prompt is sparse, Seedance will copy board panels frame-for-frame and the result will look stiff. Your prompt must be dense enough to dominate."* Rule of thumb from the recipe: "if a sentence in your Cut could be a caption for the board panel, you're transcribing — rewrite it as motion."
- **Fixes:** F1, F2, F7 (one generation shares identity, product and room across all cuts), F9 (the storyboard can be approved as a cheap still before any video spend).
- **Evidence:** A. Higgsfield MCP workflows `ugc-review-video`, `ugc-try-on-video`, `ugc-unboxing-video` and `ugc-product-video`, read from `get_workflow_instructions` and their `references/ugc-*-board.md` / `ugc-*-clip.md` files. Also B: github.com/joebenscoter86/higgsfield-ugc-workflow (GUIDE.md: "This single sheet is what you hand to the video model as the visual map … If the storyboard looks good, the video will look good").
- **Input change for Cutroom:** Add a "board" entity per 15 s ad (one image with N slots) as the required gate before video. Store the slot roles and POV/distance per slot. Send one video call with medias `[board, character, product]` instead of per-shot calls with separate frames.
- **Cheapest test:** Take one existing SANTO hoodie concept, build one 8-slot board on gpt_image_2 (a few credits) plus one Seedance 2.5 15 s omni_reference run. The video costs about 67 credits at 720p according to the repo figure for Seedance 2.0 at 15 s. Run `get_cost:true` first (see T20).

### T2. The anti-morph rule: adjacent slots must differ in both POV and distance band
- **What / how:** *"Seedance snaps a boundary into a hard cut only when the two beats are visually FAR apart; two low-delta neighbors MORPH into a blend."* No two adjacent slots may share both their POV (SELFIE / STATIC / STATIC-CLOSE) and their distance band (TIGHT / MID / WIDE). Across 8 slots, each band must appear at least twice. Name the framing explicitly in every slot (`TIGHT CLOSE-UP`, `MEDIUM`, `THREE-QUARTER`, `FULL-BODY-WIDE`, `MACRO`…).
  - Try-on default cadence: SELFIE → STATIC → STATIC → STATIC-CLOSE → STATIC → STATIC-CLOSE → STATIC → STATIC.
  - Matching distances: WAIST-UP → FULL-BODY → THREE-QUARTER → MACRO → THREE-QUARTER → MACRO → FULL-BODY-WIDE → MEDIUM-WIDE.
  - Every slot is frozen **mid-event**: "hand already clamped on the bag handle, grin already breaking — never walking up to the bag."
- **Fixes:** F1 and F7 (a morph between two similar framings is where faces and rooms melt), F4.
- **Evidence:** A (Higgsfield `ugc-try-board.md` Step 4.5 "POV & distance cadence — the anti-morph engine"; the same rule appears in the unboxing and product boards). B: the joebenscoter86 3-panel version uses Tight → Macro → Wide "to keep a 10 second clip from feeling static."
- **Input change for Cutroom:** A shot-design validator. Reject a storyboard if adjacent shots share both POV and distance band, and store POV and distance as required fields per shot.
- **Cheapest test:** Free as a validator on existing storyboards. Then A/B one board with same-band neighbours against one that follows the rule (two Seedance runs).

### T3. How Higgsfield hides state changes: evidence-backed rules for cutting to the change
Cut-to-transform is already known to you. Higgsfield encodes these specific rules for it.
- **What / how:**
  - *"State Change Minimization: maximum 1 state change per cut. Any prop state change … is a SHOWN action inside its cut — off-camera state changes render BOTH states at once."*
  - Try-on: slot 1 is the creator in a muted "pre-wear" outfit (tee plus lounge pants) holding a **plain kraft bag that is never opened on camera**. From slot 2 on, the garment IS the outfit. *"Never depict the character changing clothes on camera — the transition … is implicit, handled by the hard cut."* The bag and the pre-wear outfit never return.
  - Unboxing: the box disappears one way only. Slot 1 is sealed, slot 2 is just emptied at the frame edge or already gone, slots 3–4 have no box. The box is never lifted or carried; it rests on a surface. The opening is **one clean motion at the END of Cut 1** (for a branded package: finger-drumming, a few-cm slide, then "lift-off lid / magnetic flap … one clean motion, no fumbling"), then `Hard cut to.`, and Cut 2 opens with the product already emerging. *"Do not describe the opening motion within Cut 2."*
  - For a generic box the recipe uses a box-cutter: "slices the packing tape with one decisive motion … no lingering on the blade."
  - Never use a continuous "Set-Down/Pick-Up" camera move across a state jump. *"HARD LAW — never across an implicit state jump."*
  - "One state per prop per slot": a bag is closed and either held or standing, never both and never half-open.
- **Fixes:** F4 (mailer rip, hoodie on, zip), F7.
- **Evidence:** A (Higgsfield try-on, unboxing and product board/clip references).
- **Input change for Cutroom:** A per-shot `prop_state` field that allows exactly one state per shot and at most one transition per cut. Add the SANTO poly mailer as its own reference image, used only in the "sealed" beat. Default to rendering "open" as the last beat of cut N and "product out" as the first frame of cut N+1.
- **Cheapest test:** One 4-slot unboxing board with the real SANTO mailer photo as `package_media_id` (image only), then one 10 s Seedance run.

### T4. For the tear itself, write the causal chain (or don't show it)
- **What / how:** "Mimed manipulation" is the failure where hands work but the object never changes. The fix is to write, in order: (1) the initial structure ("mailer sealed along the adhesive flap at the top edge"), (2) the anchor ("left hand pins the bag flat on the bed"), (3) the force ("right thumb and forefinger at the corner of the flap, pulling across"), (4) the material feedback ("the flap peels, the poly film stretches and creases where it is held"), (5) the finished state ("flap fully open, fleece hem visible inside").
  - Routing rule: if the tear only *gets you to* the next state, use **two states and a sound** instead (sealed bag, tear heard off screen, hands already inside), because that "cannot fail this way".
  - Never invent a structure the reference can't show. If the tear strip or seal isn't visible in the mailer photo, cut around it or shoot it for real.
  - "Do not stack a legible brand face, a two-handed manipulation and a strong effect in one shot": the manipulation shot proves the mechanism, and a separate shot proves the label.
  - Higgsfield's own unboxing clip rules add: *"Single action per Cut … Forbidden action phrases: 'sprays again', 'presses repeatedly', 'back and forth', 'opens and closes', 'taps the lid twice' — Seedance interprets these as motion loops."*
- **Fixes:** F4, F3.
- **Evidence:** B/C for the causal chain (OSideMedia/higgsfield-ai-prompt-skill `FAILURE-MODES.md`, marked "[HOUSE … UNPROVEN HERE]"). A for single-action and loop phrases (Higgsfield `ugc-unboxing-clip.md` Step 5b).
- **Input change for Cutroom:** A "manipulation template" with five required fields for any tear, zip or fold shot, and a lint that bans repeat/loop verbs.
- **Cheapest test:** Two 5 s Seedance 2.0 mini / fast 480p runs of the mailer tear: plain verb against the 5-part chain.

### T5. Mandatory "de-slop" image pass before any video (with one fix for branded products)
- **What / how:** Every board goes through `seedream_v5_pro` i2i (role `image_references`, same aspect, 2k) before it reaches Seedance. *"Never feed a raw gpt_image_2 board to Seedance."* The fixed prompt, abridged but verbatim in its key phrases:
  > KEEP EXACTLY the framing, composition, slot layout, camera distances, poses, subjects and product … no reframe, no zoom, no crop … CHANGE ONLY micro-realism, applied identically in every slot: true-to-life pore-level skin with natural texture and fine vellus hair, real material detail, even natural daytime light with gentle highlight roll-off and faint true sensor noise, a flat authentic iPhone photo, deep focus. PRESERVE each face's exact shape / width / proportions 1:1 — do NOT squeeze / narrow / slim / stretch any face. AVOID AI-slop: waxy plastic skin, airbrushed poreless skin, beauty-filter smoothing, over-saturation, HDR glow / bloom / halos, oversharpening, teal-orange grade, shallow depth of field, bokeh, cinematic / DSLR look. Keep the product blank / unbranded, no added text, no watermark, no baked slot labels.

  On a moderation block, retry once with `seedream_v5_lite`; otherwise continue with the raw board. Gotcha: the i2i role rejects a job_id, so `media_import_url` the board URL first.
  - **SANTO caveat:** the stock prompt says "Keep the product blank / unbranded". That contradicts the same workflows' board rule that the product's real label comes from the reference. For SANTO, replace that clause with "keep the product's existing print, logo and tag exactly as they are, no added text".
- **Fixes:** F6 (plastic skin, bokeh, HDR), and F1 (the face-width clause targets the known slimming drift).
- **Evidence:** A (identical text in all four Higgsfield UGC video workflows).
- **Input change for Cutroom:** Add a "realism pass" stage on every keyframe or board, using this prompt with the brand clause edited. Nano Banana could be tried for it too, but Higgsfield locks Seedream v5 Pro for this step.
- **Cheapest test:** One Seedream v5 Pro i2i (image credits only) on an existing Cutroom keyframe. Compare skin, bokeh and the logo side by side.

### T6. iPhone front-camera optics language, plus the HARD-BAN list (for stills and clips)
- **What / how:**
  - For stills (Soul creator), add all of these:
    - `Self-portrait selfie shot on iPhone front-facing camera held by the subject at arm's length — head and shoulders fill the frame`
    - `Slightly off-center, slightly imperfect framing`
    - `Captured mid-moment, NOT a formal pose`
    - `Phone-sensor grain and realistic skin pores … no retouch, no smooth-skin filter`
    - `Subject in clear focus with the background falling out naturally as in any phone photo`
    - The closing block, appended verbatim to every prompt.
  - For boards and clips: "iPhone front-camera optics: wide 23mm-equivalent look, DEEP focus (background stays sharp — no shallow depth of field, no bokeh), slight wide-angle distortion at frame edges (never fisheye), mild HDR flattening with slight highlight clipping at the window". Also "slight phone-camera grain — faint digital sensor noise in the shadows, **never film grain**", "one small AE/AF adjustment mid-clip on a SELFIE cut only", "ONE motivated source (window/lamp), consistent white balance".
  - Lighting: **neutral cool daylight only; "NEVER golden hour, warm sunset, orange/amber cast"**.
  - HARD BAN phrases: `centered composition at eye-level`, `straight-on`, `editorial/fashion portrait`, `minimal depth of field`, `flattering and even illumination`, `glowing/flawless skin`, `radiant complexion`, `poised`, `elegant stance`, any "pose" verb, `warm smile at the camera`, `direct eye contact … confident smile`, ring light, beauty dish, `fisheye`, `ultra-wide`.
  - Use approved mid-action expressions instead, e.g. `mid-thought, slight half-smile, eyes glancing slightly off-lens` or `looking up from her phone with a relaxed, unguarded face`.
  - The body stays neutral: *"Creative body poses are an anatomy gamble — extended limbs warp, foreshortened hands grow fingers."*
  - Clip quality suffix (verbatim core): "Shot on iPhone, natural lighting, social media aesthetic … No cinematic color grade, film grain, shallow depth of field, bokeh, lens flare, slow motion, or beauty filter. No fisheye lens, no ultra-wide distortion. No third arm, no extra hands, no duplicated limbs, no deformed hands."
  - Static cuts get "locked-off static camera, absolutely static, zero camera movement … no shake, no drift, no breathing wobble". Selfie cuts get "slight natural handheld micro-shake from her grip". Never use handheld words inside a static cut, because "these leak motion into the render."
- **Fixes:** F6 (85 mm bokeh, slow-mo floaty motion, plastic skin), F3 (neutral body poses).
- **Evidence:** A (Higgsfield `ugc-character.md` "Camera & Atmosphere — iPhone UGC is the DEFINING feature"; `ugc-*-clip.md` Quality Suffix and "UGC camera realism"; `character-sheet` realism module).
- **Input change for Cutroom:** Keep a shared suffix library, plus a banned-phrase lint on every prompt that fails on bokeh / golden hour / 85mm / cinematic / ring light / "smiles at camera".
- **Cheapest test:** Free lint. Then one Soul 2 still with the Higgsfield block against Cutroom's current wording.

### T7. The hand-count law, selfie-only-one-hand, and weight/grip classes
- **What / how:**
  - *"The character has exactly two hands … total simultaneous hand-roles never exceed two … every slot names each hand's single role, the idle hand parked explicitly."*
  - **In selfie POV one hand IS the phone (off-frame).** So "never depict the character holding two objects in selfie POV. If the slot's action requires two free hands, the slot must be static camera POV with the phone not in frame." The phone object is never visible; banned words are `phone in her hand`, `holding phone up`, `mirror selfie`, `over-the-shoulder`.
  - "A prop floating unheld beside busy hands also spawns the third hand — it is held or it is resting, explicitly. Rest a prop on a surface when a stabilizer hand would otherwise be needed. Sequence multi-step actions across the hard cuts."
  - Weight classes: Heavy (two hands plus visible strain), Bulky-light (two hands, no strain), Light (one relaxed hand), Tiny (pinched between thumb and index, close to lens). "If ambiguous, default to the heavier class." Two-handed strain on a light item is also forbidden, because it reads over-acted. Never balance paired items on one palm.
  - Micro-beat discipline: "ONE movement at a time — simultaneous movements read as glitching."
- **Fixes:** F3.
- **Evidence:** A (Higgsfield board Step 5 and clip "THE HAND-COUNT LAW", identical across all flows).
- **Input change for Cutroom:** Per shot, store `left_hand_role`, `right_hand_role` and `pov`. Validate: selfie means only one role is available; ≥2 object holds means the camera must be static. Store a weight class per SKU (a folded hoodie is light; a stack of 3 items is bulky-light).
- **Cheapest test:** Free validator over existing rejected shots. Check how many violated the rule.

### T8. Realistic scale: hand-relative sizes in cm, and "move the camera, don't enlarge the product"
- **What / how:** *"Image models default to enlarging the product so the label is readable — this is forbidden. If the product is too small to read in frame, move the camera closer. Do not scale the product up."* Add the exact line: `Product is rendered at realistic real-world scale relative to the character's hand and body. The product is approximately [X cm] tall and fits naturally in the character's hand without enlargement. If the label is small in frame, the camera moves closer rather than scaling the product up.` State size as "palm-sized, fits entirely in one hand, ~15 cm". **Never size by comparison to another object** ("about the size of a water bottle"), because "object comparisons drift into oversized renders."
- **Fixes:** F3 (giant or tiny product), F2.
- **Evidence:** A (Higgsfield board Step 7 "Realistic Scale"; product-intake "staging contract").
- **Input change for Cutroom:** Store real dimensions per SKU (folded hoodie in the mailer, e.g. ~30×25×8 cm; mailer bag ~40×50 cm) and inject the scale sentence automatically.
- **Cheapest test:** Free (prompt change). Verify on the next board.

### T9. A canonical product description written once, reused verbatim everywhere
- **What / how:** At intake, write one `product_description` and paste it **verbatim** into every board and clip prompt. It covers: shape, material, colour, hand-relative size, **mechanism anatomy** ("which part is where, what moves"), **absent features stated visually**, the label, and **one honest imperfection**.
  - Clothing specifics: *"Closure / hardware anatomy — name what closes the garment and WHERE, once, in plain positional terms ('front-center zip') and reuse that exact phrasing in every board of the video. Vague hardware renders impossible geometry (a zip that migrates sides between slots)."*
  - *"Absent-by-design features … the image model hallucinates the default affordance back in. State the absence in BOTH places: the prompt body AND the closing negative run"* (e.g. "no drawstrings", "no front pocket").
  - Label: with a real photo, the label keeps its real text through the reference. **If the photo shows a big readable logo, warn once: wordmarks render as gibberish or as a real competitor brand.** Multiple product photos: *"show valid angles of the same garment … Switch angles only by hard cuts between slots, never by continuous rotation. Do not invent unseen design details."* For hard goods, the Angle Lock rule is "only the visible front-facing side … do not rotate, spin, flip, or reveal unseen sides."
- **Fixes:** F2.
- **Evidence:** A (Higgsfield `product-intake.md`, `ugc-try-board.md` Step 1 and Step 7).
- **Input change for Cutroom:** A SKU record that holds the canonical description text, closure anatomy, an absent-features list, an honest imperfection, and approved angle photos. The prompt builder must inject these verbatim.
- **Cheapest test:** Free. Write it for the best-selling hoodie, jeans and leggings.

### T10. Garment Consistency Lock and Realistic Fit sentences
- **What / how:** Insert verbatim: `GARMENT CONSISTENCY LOCK: across every slot in which the product is worn, the visible garment must keep identical silhouette, identical primary color, identical secondary color or print pattern, identical recognizable design details (collar style, hem shape, sleeve, neckline, hardware, prints, stitching). The character may turn or pose freely — the garment rotates naturally with her body — but the garment itself never changes color, never changes print, never gains or loses recognizable details between slots.` Also: `The product is rendered at realistic real-world proportions on the character's body — natural drape, natural fit, not exaggerated. Fabric falls naturally per its weight.` The reason given: "Fashion photography defaults to slimming / lengthening the wearer, but try-on UGC reads as fake when the fit is unrealistic."
  - Also: "exactly ONE garment … no look-alike garment of similar color / silhouette anywhere else in the slot (draped on a chair, hanging in an open closet)".
- **Fixes:** F2, F5.
- **Evidence:** A (Higgsfield `ugc-try-board.md` Step 7; `ugc-try-clip.md` Universal Rules).
- **Input change for Cutroom:** Auto-append both sentences to any shot where a SANTO garment is worn. Remove look-alike garments from room references.
- **Cheapest test:** Free (prompt change).

### T11. Texture close-ups with no hands, and one passive motion cue
- **What / how:** Texture and detail macros (slots 4 and 6) show fabric **only through framing, drape and light. NO touching, skimming, pulling, brushing or pinching, and no operator hand.** *"Even gentle brushing reads as 'someone touching her clothes during filming' in the rendered video."* Pick ONE passive cue per shot by garment type:
  - **Denim:** "wash gradient visible / seam line reads / fabric grain catches light"
  - **Knit / fleece:** "knit texture catches light / shoulder seam visible / weave reads clearly in macro framing"
  - **Pants:** "fabric falls along the leg with natural drape / cuff sits naturally"
  - **Tee:** "light catches the chest area as she breathes / fabric falls naturally over the chest with slight body sway"

  The second macro must show a **different** detail (hem, cuff, collar, print, seam). These macro cuts are voiceover cuts, and the mouth does not form words.
- **Fixes:** F5, F3 (hands on fabric are a hand-failure hotspot), F8.
- **Evidence:** A (Higgsfield `ugc-try-board.md` Step 9; clip Step 4b).
- **Input change for Cutroom:** Add a "texture macro" shot type with garment-type cue presets and hands forced off-frame. Fleece and leggings get their own cue lines, written in the same style.
- **Cheapest test:** Inside T1's test board.

### T12. No mirrors, ever (a "limb factory"), and no reflective surfaces showing the creator
- **What / how:** *"Reflective surfaces are a limb factory — they spawn extra hands and duplicated bodies."* That means no mirror selfies, shop windows, phone screens, or puddle reflections. Windows may appear but never show the character's reflection. Mirror selfies are the native try-on format on TikTok, yet Higgsfield bans them outright for AI try-on and uses a static "phone propped across the room" POV instead. (Note: Marketing Studio's `ugc_virtual_try_on` preset does mention "selfie or mirror framing"; the MCP recipe overrides it.)
- **Fixes:** F3, F7.
- **Evidence:** A (Higgsfield `ugc-try-board.md` Rendering Rules and Hard Restrictions; clip Universal Rules).
- **Input change for Cutroom:** Filter room photos that contain mirrors out of the environment references, or tell the model to use a wall without the mirror. Ban the word "mirror" in prompts.
- **Cheapest test:** Free.

### T13. Creator still: clean person, no product, and a multi-angle Element set with one "teeth" view
- **What / how:**
  - Higgsfield generates the creator **with nothing in their hands**: *"model bakes the bottle into the image, downstream compositing fails."* The joebenscoter86 repo adds: "it actually causes the product to drift and warp in the later steps."
  - For stronger identity, register a Higgsfield **Element** (`show_reference_elements action=create`, instant) from **3–4 images of the same person, same wardrobe and lighting (front, ¾ L, ¾ R, profile) in ONE create call**. Embed `<<<element_id>>>` in prompts. The backend auto-injects the images.
  - Higgsfield's Seedance 2.5 deck (via OSideMedia): generate views on neutral light-grey and make **one view a strong expression / wide smile showing teeth**, *"so the model learns the character's facial dynamics and teeth structure … a set of neutral views teaches the model the face at rest and nothing else, so the first line of dialogue invents a mouth."* The canonical four: front, back, face neutral, face with strong emotion and teeth.
  - When passing several views, say they are one subject: "All four images define one [person]. The output must contain only one [person]." Otherwise the model duplicates.
  - Character sheets leak their staging (grey backdrop, panel borders). Add: "Do not take the gray backdrop, the panel borders, or the multi-view layout."
  - Outfit changes without identity drift: a split sheet with a ghost-mannequin outfit on the LEFT and a "face matches input 100%" close-up on the RIGHT.
  - In the video prompt, **describe action, not appearance**. Re-describing a referenced character "creates conflict".
- **Fixes:** F1, F8 (mouth), F2.
- **Evidence:** A for no-product-in-character (all Higgsfield flows) and for the Elements capabilities (MCP tool description: "instant, single image, MULTIPLE references per generation, works with … Seedance 2.0, Kling 3.0, Cinema Studio Video 2/3.0"). B for the angle set and environment element (github.com/charlesdove977/UGC-Factory). B for the teeth view (github.com/OSideMedia/higgsfield-ai-prompt-skill, citing the "Higgsfield Seedance 2.5 deck").
- **Input change for Cutroom:** A model/person reference should become an **angle set of 4 including a talking/teeth frame**, all in the same outfit, with no product. Keep the product reference separate. Store an "is one subject" flag.
- **Cheapest test:** 3 Nano Banana edits to build the angle set from the existing model photo (~4.5 credits). Element creation is free, but it is a write call the user should make.

### T14. Environment lock: one clean room plate as its own reference, plus repeated negatives in every clip
- **What / how:** Register the room as an **environment Element**: "one clean plate of the room … category environment", embedded with the character "so the backdrop stays consistent even as the camera and person move." (Seedance 2.5 syntax: `Scene A references @Image 4. Use only the spatial layout, architecture, and lighting. Do not use the people in the image.`)
  - Higgsfield's own multi-clip try-on example (Marketing Studio PDF, via OSideMedia) puts a shared `LOCATION:` and `CAMERA: STATIC, FULL BODY SHOT, eye level. Same angle all 5 clips, never moves.` block on top, and **repeats the negative "NO bag, NO backpack, NO purse" in every clip** "when the model has been adding incidental props."
  - Other rules from the recipes: "No extras: no additional people or random objects"; "No legible text or numbers on props (receipts, tags, screens) — Seedance renders RANDOM characters"; "keep look-alike shapes off the staging"; "Character exits frame = gone for rest of clip."
- **Fixes:** F7.
- **Evidence:** A (Higgsfield rendering rules). B (UGC-Factory environment element; the Marketing Studio PDF example quoted in OSideMedia `higgsfield-marketing-studio/SKILL.md` §10.2).
- **Input change for Cutroom:** Real room photos become an **empty-room plate** reference with role "layout + light only, no people". Keep a per-room list of props that must not appear (jewellery, posters) and inject it into every clip.
- **Cheapest test:** Free (prompt). One board to verify.

### T15. Performance direction: 5+ named micro-beats per cut, one at a time, between phrases
- **What / how:** Seedance "under-renders energy; a flat-neutral prompt renders a wooden AI presenter." Every cut gets:
  - ≥5 concrete micro-beats that name the body part and the object ("tucks a strand behind her ear with one finger", never "fidgets"). Never write the emotion word; the movement carries it.
  - At least one within-cut change, and expression evolution across cuts, with no expression repeated.
  - Micro-beats are placed **between spoken phrases, never on a key word**, because "they smear lip-sync; they double as resync anchors".
  - "Locked camera does NOT mean a locked body": every static cut needs a weight transfer or pose shift.
  - At least one **unguarded beat** per clip ("recovered eye-flick / mid-thought stumble / quick self-correction … Wooden, posed-throughout performances read as AI").
  - An optional single **sound intrusion** ("a dog barking close, two bursts"): eyes flick off-frame, back within ~1.5 s, and the sound is written into the Audio line.
  - Peaks are body events, max 1–2 per clip, at human scale ("a real jaw-drop, a breaking grin"). Screaming only happens on an explicit "hyped" brief.
  - A requested quirk written small "renders ~2 of 9". Stage it 30% bigger with a single-event SFX ("one sharp tap", never "taps", because repeats loop).
  - Anti-patterns: "smiles at the camera", "poses for the camera", "holds the product and talks".
- **Fixes:** F6, F8.
- **Evidence:** A (Higgsfield `ugc-try-clip.md` Step 5 "Cinematic Specificity"; the same in the unboxing clip).
- **Input change for Cutroom:** Store the micro-beat list per shot in the shot schema; lint for ≥5 beats and no bare emotion words.
- **Cheapest test:** Free (prompt authoring).

### T16. Script density and wording rules that stop fake-sounding AI speech
- **What / how:**
  - **Density:** ≤10 s → 12–20 words; 11–12 s → 20–28; 13–15 s → 28–35 (~2 words/s).
  - **First word** must be hook content, never `OK/Okay/So/Alright/Um/Well/Like/Wait/Hold on/OMG/Hey guys/Story time/Stop scrolling`.
  - **Banned anywhere:** `literally, obsessed, game-changer, holy grail, changed my life, hits different, elevate, seamless, effortless, 10/10, you NEED this`, and "This is X, not Y" constructions.
  - **Friction openers** beat enthusiasm ("I almost returned this."). Use one "but then" beat and one peak reaction.
  - No greetings after board 1; later boards continue mid-thought.
  - Default frame for try-on is the **personal-want mini-story** ("I have been refreshing the tracker every hour for three days and it is finally here").
  - "NEVER write engineered or dramatic pauses — they bloat the line and break the render."
  - **Protect the mouth:** move the wordiest chunks onto voiceover cuts (macros), and include ≥1 closed-mouth recovery beat in the densest lip-sync cut. If lip slop appears, "cut spoken words first."
  - Delivery markup is allowed: ≤2 stretched vowels, ≤2 CAPS words per segment, one em-dash break, and 1–3 bracketed non-verbal sounds at the start of board 1 (`[*soft gasp*] [*small bright laugh*]`).
  - Measured by a community rig: lines of **≤6 words in a 4 s shot came back with invented filler babble every time; 8–12 words came back clean (~3 w/s)**. Also give every other visible face a positive at-rest mouth fact ("lips at rest").
- **Fixes:** F8.
- **Evidence:** A (Higgsfield `monologue-craft.md`, clip Step 6). B for the babble measurement (OSideMedia `FAILURE-MODES.md` "[MEASURED — sync-budget ladder, 2026-08-09 … Seedance 2.0]").
- **Input change for Cutroom:** A script linter covering word budget by duration, first-word ban, banned lexicon, minimum 8 words per ~4 s of lip-sync, and moving extra words to voiceover macro cuts.
- **Cheapest test:** Free lint.

### T17. Audio settings: native Seedance speech, iPhone mic room tone, no music, phonetic brand spelling, voice-sample reference
- **What / how:**
  - Use Seedance's own audio (`generate_audio:true` in the same call); "never call generate_audio" separately.
  - Audio line: "**iPhone microphone audio with natural room tone throughout**", plus named ambience ("fabric rustle on the twirl").
  - **Music: default none.** If used: "low in the mix under the voice … NO lyrics (lyrics fight lip-sync)."
  - "Every audible beat (tap, rustle) goes into the Audio line or renders mute."
  - **Accent/voice:** "Text-only accent enforcement lands about one render in three". Attach a 5–10 s voice sample as an audio reference with the note "accent and vocal delivery reference only — do not copy words, only the accent, melody, and timbre". Write accents "two levels stronger than asked", never "slight/subtle", and never use phonetic misspelling of dialogue.
  - **Brand pronunciation:** spell brand words phonetically **in the spoken line only** (e.g. "nustandardlabs" was read letter by letter, fixed by writing "Noo Standard Labz"; "vial" became "vile"). Always write "no subtitles", or Seedance burns its own captions in. For SANTO, test "Sahn-toe" vs "SANTO".
- **Fixes:** F8.
- **Evidence:** A (Higgsfield clip Step 6, SKILL.md accent note). B (joebenscoter86 GUIDE.md, "we hit the failures live and fixed them").
- **Input change for Cutroom:** A per-brand pronunciation dictionary. An optional recorded 5–10 s voice sample per creator persona (a real person's voice only with consent). A music toggle that defaults to off.
- **Cheapest test:** One Seedance 5 s 480p run with "SANTO" written two ways.

### T18. First 0.4 seconds: frame one mid-event, voice immediately, plus "accident of recording" openers
- **What / how:**
  - "Cut 1 opens ALREADY MID-EVENT … the first spoken word lands within 0.0–0.4s of frame one — no silent lead-in, no breath-before-speaking."
  - Optional H9 entry devices (selfie Cut 1 only, each with an "audio twin"):
    - **Drop-Catch:** the frame tumbles, then is caught; the first word lands during the catch; audio twin is fabric scrape plus a sharp breath.
    - **Walk-and-Slam.**
    - **Light Switch:** sound leads picture by 0.5 s.
    - **Zoom-Out Reveal.**
  - Real-phone opener: "candid HANDHELD iPhone ZOOM-IN toward the face — pushes in fast and a little unsteady, a tiny overshoot-and-correct, like a real hand pinch-zooming, never a smooth professional dolly".
  - At most one baked camera move per cut, never on every cut.
  - Endings: no CTA tail. Loop device: end mid-phrase, or frame-match the last cut to Cut 1.
- **Fixes:** F6 (a "directed" look), F8.
- **Evidence:** A (Higgsfield clip Step 4 "0.1-second hook law", "H9 Entry Device", Step 2b).
- **Input change for Cutroom:** Add an opener device field to cut 1, and an audio-twin requirement.
- **Cheapest test:** Inside any T1 run.

### T19. Frozen-frame QA checklist, failure salvage, and a re-roll protocol
- **What / how:**
  - Before showing or stitching, inspect evenly spaced stills, **every product close-up, and 2–3 mid-word frames**. Check:
    - exactly one hero product;
    - ≤2 hands per person, including mirrors and frame edges;
    - absent features still absent;
    - prop state consistent;
    - label not gibberish, mirrored, or another real brand;
    - product scale matches the hand;
    - no doubled lip edges;
    - face matches the reference;
    - no baked text.
  - Fix: re-roll that clip only, with a corrected prompt. Baked text: "rerun once, then remove in post."
  - **Character re-roll:** "If board generation or clip submission fails twice in a row on the same call, assume the Soul character render was rejected" (moderation). Re-generate with the same prompt and a new seed, discard boards, cap at 2.
  - "Never fall through to generate_video with an empty medias array, which silently becomes text-to-video of the wrong thing."
  - Community additions: one bad frame is enough to reject; mine failed takes for 1–3 s of usable inserts; FPS drift (dupes at 12–18 fps) → state "The video runs at 24 fps. No frame is repeated."
- **Fixes:** F9, F2, F3.
- **Evidence:** A (Higgsfield SKILL.md "Frozen-frame QA", "Failure handling"). B/C (OSideMedia FAILURE-MODES).
- **Input change for Cutroom:** An automatic frame sampler (N evenly spaced frames + mid-word frames from the transcript) and a checklist UI. Feed rejections into the rule-mining you already have. Add a hard guard against empty `medias`.
- **Cheapest test:** Free (ffmpeg frame extraction on existing outputs).

### T20. Cost control: `get_cost` preflight, 720p for phone-style UGC, patch only failed indices
- **What / how:**
  - `generate_video` accepts **`get_cost: true`**, which returns the credit cost without generating. The community pipeline makes it a mandatory gate.
  - Measured: Seedance 2.0 at 15 s was **~67 credits at 720p vs ~135 at 1080p, and "for this phone-selfie UGC format, 1080p looks no different"**. Render time is dominated by audio synthesis, so 720p isn't faster. There's **no 720p-draft → 1080p-final trick**, because audio is regenerated.
  - Higgsfield's own workflows lock 1080p for final output, but they never re-render the whole set: "Retry only rejected or failed indices, never the whole stage."
  - Product photoshoot flow caps: ≤2 refinements per image and ≤3 total submissions per index; refinements use the latest completed job of the same index as the single reference.
  - Higgsfield's blog adds: validate prompts at 720p first, because "going from 720p to 1080p roughly doubles the credit cost."
  - `kling3_0` `sound:"off"` lowers credits. `wan3_0` duration `-1` (smart) is billed as 10 s.
- **Fixes:** F9.
- **Evidence:** B (joebenscoter86 `skills/ugc-video/SKILL.md`, "validated 2026-06-22"). A (Higgsfield blog "Generating with Seedance 2.0: Full Tutorial", higgsfield.ai/blog/generating-with-seedance-2-0, via search summary; `models_explore` parameter descriptions).
- **Input change for Cutroom:** Call `get_cost` before every paid job and show the cost. Default to 720p for organic posts and 1080p only for paid placements. Keep a per-index retry budget.
- **Cheapest test:** 0 credits. `get_cost` is a flag on `generate_video`. I did not call it, per the brief's no-generate rule. Confirm it's truly free on one call.

### T21. Record the hard motions for real, then recast them with Ad Multiplier or Genjutsu
- **What / how:** For the shots AI can't do (mailer rip, hoodie pull-on, legging stretch, denim stiffness), **film a real 4–30 s phone clip** (any person, in the SANTO product, in a real room) and edit it instead of generating from scratch:
  - **Ad Multiplier** (`model:"ad_multiplier"`, Seedance 2.5-based, `mode:"video_edit"`, `generate_audio:false`, `duration: ceil(source)`, `duration_policy:"strict"`, 720p recommended) *"preserving source motion, framing, cuts, timing, aspect ratio, and default audio."* It replaces the person, product, clothing, background or objects, and restores the **source's real audio** with ffmpeg afterwards.
    - Person replacement: the `@ImageN` is authoritative for the complete look, including clothes, unless a separate garment image is mapped.
    - The required exclusion sentence reads: "The original source person … must never appear in any frame … retaining only the original performance, pose, blocking, interactions, and timing."
    - Prompt ≤3,900 characters, COMPACT or DETAILED template. It must contain: "Preserve every caption, subtitle, and other untargeted on-screen text element from @Video1 exactly as it appears…"
  - **Genjutsu** (`hf_mult_replace_object` for "swap a garment/product/character", `hf_mult_motion_control` for motion transfer). Inputs: one video (≤30 s) plus reference images (Higgsfield blog says up to 30 photos).
  - **Kling 3.0 Motion Control** checklist:
    - one clear subject;
    - head and body visible;
    - real human motion;
    - no cuts in the reference;
    - slow to moderate speed;
    - 3–30 s.

    "Matches Video" follows body movement; "Matches Image" suits camera-driven shots. "If output is suddenly shorter than the source, the motion is too fast/complex."
- **Fixes:** F3, F4, F5, F6 (real physics and handheld), F8 (real room sound), F9 (no rerolls on motion).
- **Evidence:** A (Higgsfield `ad-multiplier` v1.4 SKILL.md and `references/prompt-writer.md`; `/genjutsu` preset instructions; `models_explore`). A/B for Genjutsu limits (higgsfield.ai/blog/higgsfield-genjutsu via search summary). B for the Kling checklist (OSideMedia `higgsfield-motion/SKILL.md`).
- **Input change for Cutroom:** A "real capture" asset type: short phone clips of real hands doing the hard state changes in SANTO products, stored as **video references**, not just frames. The movement library already exists; this upgrades it from motion reference to source plate for editing.
- **Cheapest test:** One `hf_mult_replace_object` run, 5 s at 480p, swapping a plain hoodie in a real clip for the SANTO hoodie. Cost unknown (not exposed); use `get_cost`. Seedance 2.5 `video_edit` is "billed by that video's duration."

### T22. Seedance 2.5 reference grammar: a role and an exclusion for every reference
- **What / how:** For every reference, say what to use and what not to use:
  - `<Creator> corresponds to @Image 1. Use only the appearance, hairstyle, and clothing.`
  - `<Hoodie> corresponds to @Image 3. Use only the structure, material, and color.`
  - `<Bedroom> references @Image 4. Use only the spatial layout and lighting. Do not use the people in the image.`

  Other rules:
  - Declare a fidelity grade per material (full / partial / attribute-transfer onto a named target / loose).
  - **Beat lines name characters by name plus one visible marker, never by @handle.** "A handle used as a sentence subject is the classic way one character comes back as two people."
  - "Never place a reference handle in a shot where that subject is absent — the model forces it into frame."
  - Stable range is 1–8 distinct subjects in images. Video references are motion/pacing by default, not identity.
  - First/last frames are declared in prose ("@Image 1 is the first frame"), never merged in one sentence; the aspect ratio locks to the first image.
  - Physics anchors: name what stays put ("the tag stays attached; only the sleeve moves").
  - Action-reversal: a short action followed by leftover seconds plays in reverse, so chain 2–3 actions along the same vector and name the camera endpoint.
  - Truncated action: name the completion state ("the zip stops at the collar and stays").
- **Fixes:** F1, F2, F4, F6 (floaty back-and-forth), F7.
- **Evidence:** B (OSideMedia `higgsfield-seedance-2-5/SKILL.md`, tagged "[OFFICIAL — Dreamina]", i.e. ByteDance's own Seedance 2.5 prompt guide; FAILURE-MODES).
- **Input change for Cutroom:** The prompt builder auto-writes one role-plus-exclusion line per attached reference and uses names instead of @handles in action text.
- **Cheapest test:** Free (prompt builder change).

### T23. Marketing Studio presets as a cheap baseline (Unboxing accepts your real packaging)
- **What / how:**
  - `marketing_studio_video` (12–15 s, 480p–1080p, native audio) has presets for UGC, Tutorial, `ugc_unboxing`, Product Review, `ugc_virtual_try_on`, `virtual_try_on` (Pro), Hyper Motion, TV Spot and Wild Card.
  - Hook plus setting IDs work only on UGC / Tutorial / Unboxing / Product Review / UGC Virtual Try On. `ad_reference_id` instead **recreates an analysed reference video's scenario** (pacing, hook, narration) with your avatar and product. It is mutually exclusive with hook/setting. Max 1 avatar.
  - The Unboxing preset "accepts custom packaging image in the additional-asset slot", which here means the SANTO mailer.
  - Marketing copy claims the try-on "maps clothes … preserving textiles, seams, and branding details even during highly kinetic body movements" (C until tested).
  - The Higgsfield Marketing Studio PDF example for a garment pull-on: short **3–4 s clips, static full-body camera identical across clips**, "She reaches off-frame, grabs the … t-shirt, pulls it over her head and on — adjusts it, smooths it down." Pants were marked "changed off-screen".
- **Fixes:** F4, F9 (benchmark), F7.
- **Evidence:** A (`models_explore` parameter docs). B (OSideMedia marketing-studio SKILL, from Higgsfield livestream transcripts and PDF). C (higgsfield.ai/marketing-studio-intro claims).
- **Input change for Cutroom:** Treat Marketing Studio (with the SANTO mailer as the packaging asset) as the benchmark to beat. For a pull-on, isolate it in its own 3–4 s static full-body clip.
- **Cheapest test:** One Marketing Studio Unboxing generation with the mailer photo (cost via `get_cost`).

### T24. Soul ID vs Elements vs hybrid sheet: identity rules with numbers
- **What / how:**
  - **Soul (trained):** MCP says "5–20 photos, ~10 min, ONE person, usable only with `soul_2` and `soul_cinematic`, one soul_id per generation." Higgsfield's help pages and an older blog say minimum 20, up to 80, ideal 20–25 photos; varied expressions, angles, distances and lighting; no sunglasses or cropped faces; at least one full-height photo; recent photos; "a smaller set of clean, varied photos outperforms a large set of inconsistent ones."
  - **Elements:** instant; multiple per generation; work in Seedance 2.0 / Kling 3.0 / Nano Banana / GPT Image 2 / Seedream. Recommended for UGC because a product plus a person need two references.
  - **Real person:** a generated sheet from their photos "comes back as a lookalike actor, not the actual person". The hybrid: erase the heads on the body panels and paste the real photo into the portrait panel (only with consent).
  - For video, Higgsfield's own UGC flows use a single Soul 2 still plus the board. They never train an identity ("no identity training" is locked).
- **Fixes:** F1.
- **Evidence:** A (MCP `show_characters` / `show_reference_elements` descriptions; higgsfield.ai help center "How do I create and use a Soul ID character?" and blog "Soul-ID-AI-Character-Consistency" via search summary). B (hybrid sheet, OSideMedia soul SKILL citing a Higgsfield "AI Love Stories" tutorial).
- **Input change for Cutroom:** Keep a Soul ID only for recurring SANTO faces used in stills. For video, use the Element angle set (T13) plus the board.
- **Cheapest test:** Free to compare existing outputs. Soul training cost unknown.

---

## 2. Higgsfield internal recipes, verbatim-ish

### ugc-review-video v1.1 (talking-head creator ad)
- Output: one 9:16 MP4. **Boards: 21:9 sheet of 8 vertical 9:16 slots; one clip = 8 internal hard cuts.**
- Creator: `soul_2`, 3:4, 2k (or an authorised user photo). "Use one `character_media_id` for every board and clip. Never regenerate it mid-run or replace it with an inline description." Wardrobe fixed.
- Board: `gpt_image_2`, 21:9, 2k, quality high, medias `[product, character, (previous cleaned board)]`, sequential. Then the mandatory Seedream v5 Pro de-slop (T5).
- Clip: `seedance_2_5`, 9:16, 1080p, duration ≤15, `mode:"omni_reference"`, `generate_audio:true`, medias `[clean board, character, product]`, batched ≤12 per call. "Never call generate_audio."
- Duration → boards: 4–15 s = 1 (FULL_ARC: HOOK → MAIN → CLOSER); 16–19 s = 2 balanced; 20–30 s = 15 + rest; 31–45 s = 3; 46–60 s = 4 (HOOK, REVEAL, APPLY, CLOSER).
- Monologue: story mode by default. The product enters as a "supporting actor at 40–60% of runtime". One "but then" twist; the CTA rides inside the resolution; "the story must survive with the product deleted." Hook patterns H1–H8, including H8 "Product Cold Open" (slot 1 product-only, "rougher light, slightly compressed social-video texture, hands only, no face", then a hard cut to the creator mid-reaction). Truth contract: a generated creator is a host, never a customer; no invented results or ratings.
- QA and assembly: frozen-frame QA (T19), `ffmpeg -f concat -c copy`, hard cuts only. Captions are opt-in and burned from a **word-level Whisper transcript of the final audio, never planned beats**.
- References: product-intake, ugc-character, monologue-craft, ugc-board, ugc-clip, subtitles. "Do not load sibling UGC workflow references; their … contracts conflict."

### ugc-unboxing-video v1.0 (unboxing / first reaction / haul)
- 4-slot board: PACKED (sealed box, product not visible) → REVEAL (product just out; box at frame edge or gone) → PRODUCT-FOCUS (box gone) → SATISFACTION. Board 2+ (`BOARD_K_POST_REVEAL`) picks one shape: FIRST-USE / WRONG-TURN / CLOSE-STUDY / SHOW-OFF, with exactly one visual twist.
- Optional **real package photo** becomes `package_media_id`: "THIS package is the ONLY packaging anywhere … natural opening mechanism … determined by what's visible." Without one: a plain brown taped box with colour-matched tissue ("empty boxes read as AI-fake").
- Surface: table for small products, premium clean surface (light wood, marble, white lacquer); never workbench or garage.
- Cut 1 ends with one clean opening motion; Cut 2 opens with the product already emerging (T3). Weight/grip classes. Single action per cut. Loop-verb ban.
- Monologue: "caved-in confession frame" ("I saw this fourteen times on my feed. I caved."), surprise scripted as a BODY event, one "but then".
- Models identical to review (soul_2 → gpt_image_2 board → seedream_v5_pro → seedance_2_5 omni_reference 1080p audio).

### ugc-try-on-video v1.0 (try-on / fit check / OOTD)
- 8 slots: PRE_WEAR (muted base outfit plus one plain kraft bag, no logo, handles optionally tinted to the product colour, never opened; selfie) → WEARING (full-body, static, one twirl, peak reaction) → FRONT_POSE (different distance) → TEXTURE_CLOSEUP (hand-free macro, VO) → TURN (over-shoulder) → DETAIL (second hand-free macro, different detail, VO) → STYLE_POSE (a **different room** of the same home) → FINAL_LOOK (loop-ready).
- Lip-sync on slots 1, 2, 3, 5, 7 and 8 (including static POV: "the locked-off camera is still her phone propped … across the room"). Voiceover with the mouth closed on 4 and 6.
- Per-board progression: K=2 home tour; K=3 outdoor with light rain from slot 2 ("hair stays dry", droplets on fabric allowed, no puddle reflections); K=4 seated "settled-glow" reflection ("now that I've actually lived in this"); K≥5 loop.
- Hard rules: outfit continuity is one-way; no costume change on camera; no mirrors or reflections; garment consistency lock; realistic fit; no CTA tail; hairstyle locked; no text baked.
- Default pull-on is **implicit via cut**, which contrasts with the Marketing Studio PDF example that shows a pull-on inside a 4 s static clip.

### ugc-product-video v1.0 (product-only, no creator)
- 4 slots: PRODUCT-INTRO (native context, a hand at the edge at most) → DEMO-A → DEMO-B (materially different action, scale or context) → RESULT/hero.
- Person is auxiliary only (cropped, hands-only, first-person POV). Identity is not preserved. Their gender matches `voice_gender`, which comes from the product. The mouth is always closed. Voiceover only. **A product reference is required** ("do not invent, generate, or borrow a product image").
- Medias for the clip: `[board, product]`. Clothing demo pairing: "Garment held up by both hands, displayed front" vs "Worn on body (cropped: torso, hands smoothing the fabric)". Clothing usage sequence: "Hold up → wear → adjust fit → smooth fabric → point to detail". Product Angle Lock.
- Macro cut language: "MACRO locked-off on the [mechanism] — the [trigger…] depresses, [substance] emerges, [state change]". First-person POV means one visible hand; the phone hand never enters.

### character-sheet v1.0
- Slot architecture in fixed order: composition → "identical original [subject] on all views" → identity → face (for adults, a **mature structure**, "no babyface") → eyes with an anti-glare clause ("naturally muted catchlights, no oversized specular glare in the iris, eye color muted rather than glowing") → hair with *finish* → realism module → body → wardrobe top-to-toe → lighting → quality tail → negative tail.
- Realism module ("the whole trick"): "visible fine skin texture with natural pores, fine lines, subtle asymmetries … natural visible makeup with slightly uneven foundation blending … slight natural sheen rather than glossy or dewy retouched finish, no digital smoothing, no beauty filter, no AI-airbrushed look, skin completely free of artificial glare, shine or highlight blooms, matte-to-natural complexion", plus imperfection anchors (faint freckles, a small mole).
- Split-screen default: left is standing full-body with both feet visible; right is a tight chest-up. 16:9. Negative tail: "single subject only, exactly one person … no reflections, no props".
- Consistency carries forward: "every previously-established detail … carries forward unchanged … restate the rest so nothing silently drifts."

### product-photoshoot v1.0 (packshots / virtual model try-on)
- Model locked to `nano_banana_pro`, 2k, `role:"image_references"`, prompt ends with the literal line `resolution: 2k`. Distinct prompts per variant (not `count:N`). One product identity across a set: generate index 0 first, then reuse its job ID as the reference for the others (text-only products).
- The `virtual-model-tryout` mode explicitly "does NOT train an identity … not the literal same person". Template sections: [PRODUCT][MODEL][POSE][FRAMING][ENVIRONMENT][WARDROBE][LIGHTING][LENS][SKIN & DETAIL][PRODUCT FIDELITY DIRECTIVE][AVOID]. Anatomy: "specify finger position explicitly… eyes in the wrong direction is the most common tell." Note that this mode uses editorial and 85 mm, shallow-DoF language, which suits catalogue work, **not UGC**.
- Universal `[AVOID]` block: "no AI sheen on hair or skin, no doll-like rendering, no airbrush look … no oversaturated HDR, no HDR halos". Anti-uncanny: "no orange-tan skin … no warped jewelry or glasses, no stiff unnatural posture". Anti-text-warp: "no warped product label text, no garbled letters, no fake brand names … no doubled labels, no fictional logos".
- Refinement budget: ≤2 per index, ≤3 total submissions per index. Refine only observed defects; never "speculative visual refinements" without viewing the pixels.

### ad-multiplier v1.4
- See T21. Source must be 4.0–30.0 s (never trimmed or looped). One video analysis (`video_analysis_create`) provides scene timings. Outputs are submitted one at a time, `count:1`, with one retry per failed position. Missing adult replacements are generated on `soul_2` with a 140–190-word studio full-body paragraph. Finals get the source's default audio re-muxed and are QC-gated on duration, aspect, resolution and audio.

### /genjutsu preset
- Motion transfer → `hf_mult_motion_control`; object/garment/character swap → `hf_mult_replace_object`. `medias` = reference images (role `image`) plus exactly one source video (role `video`). "Never legacy motion_control or ad-multiplier for one Genjutsu edit."

---

## 3. Model capability table (from `models_explore`, live on 2026-09-24)

`models_explore` does **not** expose credit cost or a numeric max-reference count for most models. Where a number comes from elsewhere, the source is noted.

| Model id | Type | Duration | Resolution | Keyframes (start/end) | Image refs | Video ref | Audio ref | Native audio | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `seedance_2_5` | video | 4–30 s | 480/720/1080p | start_image, end_image roles listed | yes (Dreamina doc: ≤30 images, stable 1–8 subjects) | yes (≤10, ≤30 s total) | yes | yes (default on) | modes t2v / omni_reference / video_edit (billed by source length) / video_extension (fwd/back); bitrate high. The OSideMedia snapshot from 2026-08-07 said 720p max and no start/end, so the **live catalogue changed** |
| `seedance_2_0` | video | 4–15 s | 480p–4K (std); fast = 480/720 | yes | yes (HF blog: "up to 9 reference inputs") | yes | yes | yes | genre hint; supports unlim; ~67 cr at 15 s 720p, ~135 at 1080p (community-measured) |
| `seedance_2_0_mini` | video | 4–15 s | 480/720 | yes | yes | yes | yes | yes | budget |
| `ad_multiplier` | video | 4–30 s | 480–1080 | yes | yes | yes | yes | (workflow sets off) | Seedance 2.5-based video edit; workflow restores source audio |
| `hf_mult_replace_object` (Genjutsu) | video | source ≤30 s (blog) | 480–1080 | — | yes (blog: ≤30) | yes (1) | — | — | swap garment/product/person/location in real footage |
| `hf_mult_motion_control` (Genjutsu) | video | source ≤30 s | 480–1080 | — | yes | yes (driving) | — | — | motion transfer |
| `kling3_0` | video | 3–15 s | std / pro / 4k | start + end only | no (only via Elements) | no | no | on/off (off = cheaper) | multi-shot; supports unlim; Elements supported |
| `kling3_0_turbo` | video | 3–15 s | 720/1080 | start only | — | — | — | — | fast |
| `kling_video_edit` (3.0 Omni Edit) | video | source | std/pro/4k | — | yes | yes | — | — | text + image-guided edit of real footage |
| `wan3_0` / `wan3_0_prime` | video | 2–30 s, or −1 smart (billed 10 s) | 480/720/1080 | yes | yes | yes | yes | yes | `enable_thinking` = better prompt adherence (slower) |
| `wan2_7` | video | 2–15 s | 720/1080 | yes | — | — | yes | yes | supports unlim |
| `minimax_h3` | video | 4–15 s | 2K | yes | yes | yes | yes | — | batch 1–4 per job |
| `veo3_1` | video | 4/6/8 s | basic/high/ultra | start only | — | — | — | yes | — |
| `veo3_1_lite` | video | 4/6/8 s | — | start + end | — | — | — | optional | budget |
| `gemini_omni_flash_1_1` | video | 3–10 s (edit ≤30 s) | 360p–4K | yes | yes | yes | — | yes | edit mode on real footage |
| `flux_3_video` | video | 5–20 s | 720/1080 | yes | yes | yes | — | yes | `flux_3_video_edit` = 1 credit/s |
| `grok_video_v15` | video | 2–15 s | 480–1080 | start | yes | — | yes | — | — |
| `marketing_studio_video` | video | 12–15 s | 480–1080 | yes | + avatar (max 1) + product_ids | — | — | yes | presets; hook/setting or ad_reference_id |
| `cinematic_studio_video_v2` | video | 3–12 s | — | yes | — | — | — | on/off | multi_shots, speedramp, cfg_scale |
| `sync_so` (Lipsync 3) | video | — | — | — | — | input_video | input_audio | — | re-lip-sync real or generated video to real audio |
| `video_deflicker`, `topaz_video`, `bytedance_video_upscale` (preset `ugc` / `aigc`) | post | — | — | — | — | — | — | — | finishing |
| `soul_2` | image | — | 1.5k/2k | — | **max 1** image | — | — | — | `soul_id` param; supports unlim |
| `nano_banana_pro` | image | — | 1–4k | — | yes, no max stated (community: "no max") | — | — | — | Higgsfield's product-photo model; community reports the job may come back labelled `nano_banana_2` |
| `nano_banana_2` | image | — | 1–4k | — | yes + **mask / is_inpaint** | — | — | — | targeted fixes (logo, fingers) |
| `seedream_v5_pro` | image | — | ≤2k | — | yes, is_inpaint, remove_bg | — | — | — | Higgsfield's de-slop model |
| `gpt_image_2` | image | — | 1–4k, quality low/med/high | — | yes (role `image`) | — | — | — | Higgsfield's storyboard-board model (21:9 supported) |
| `ms_image` (DTC Ads) | image | — | 1–4k | — | max 14; product_ids ≤4 | — | — | — | brand-kit aware |
| Elements (`show_reference_elements`) | — | — | — | — | multi-image per element; many elements per prompt | — | — | — | works with Seedance 2.0, Kling 3.0, NB Pro/2, GPT Image 2, Seedream, Cinema Studio; not Soul |

---

## 4. STOP DOING (what Higgsfield's own recipes or pros say hurts quality)
1. **Bokeh, shallow depth of field, 85 mm/DSLR/cinematic, golden hour, warm sunset, ring light, "soft bokeh background"** in UGC prompts. Community skills (e.g. AKCodez `ugc-video-auto`: "Soft bokeh background, shallow depth of field … golden hour") still use these; every Higgsfield UGC recipe bans them.
2. **Putting the product into the creator/character image.** It breaks compositing and causes product drift or warping.
3. **Re-describing the referenced person's appearance in the video prompt.** Describe action. Re-description conflicts with the reference.
4. **Sparse video prompts over a board or keyframe.** They make Seedance copy the panel frame-for-frame (stiff). A blank or <2-sentence prompt produces gibberish.
5. **Showing state changes continuously** (pulling on, tearing open, changing) inside one cut, or using a camera set-down/pick-up across a state jump. Off-camera state changes written into one cut render both states at once.
6. **Mirrors, mirror selfies, shop windows, phone screens**: the "limb factory".
7. **Touching fabric in texture close-ups.** It reads as someone else touching the clothes and triggers hand failures.
8. **Similar adjacent shots** (same POV and same distance band). These morph instead of cutting.
9. **Loop verbs** ("again", "twice", "back and forth", "opens and closes", "taps"). Seedance renders motion loops.
10. **Small described logos or lettering, and any legible text on props** (receipts, tags, posters). They render as gibberish or as a real competitor brand. Only the product's own print, carried by the reference image, is legal text.
11. **Sizing the product by comparing it to another object**, or letting the model enlarge it for label readability.
12. **Warm-up openers and AI lexicon** ("Okay so", "obsessed", "game-changer", "literally", "10/10", "hits different"), **engineered dramatic pauses**, and **very short lines** (≤6 words in 4 s produced filler babble).
13. **Music with lyrics under speech**, and music by default.
14. **Using "@Image" handles as sentence subjects in action text**, or a handle in a shot where that subject is absent.
15. **Raw GPT-Image boards sent straight to video** (skipping the realism pass). Also: leaving Higgsfield's default "keep the product blank / unbranded" clause in the de-slop prompt for a branded garment.
16. **1080p for organic phone-style UGC tests** (~2× the credits with no visible gain). Rendering a 720p draft and then "upgrading" to 1080p doesn't work either: the audio re-rolls.
17. **Posed language**: "smiles at the camera", "poses", "warm smile", "confident eye contact", bare mood adjectives, creative limb-extended poses.
18. **Re-running a whole batch when one clip fails.** Re-roll only that index. Never submit `generate_video` with empty `medias` (it silently becomes text-to-video).

---

## 5. Open questions
1. **Branding vs de-slop:** Higgsfield's de-slop prompt says "Keep the product blank / unbranded", while its board rules keep the real label from the reference. Does a Seedream pass with the edited clause (T5) keep the SANTO logo, tag and print intact? Test before adopting.
2. **8 tiny panels vs garment detail:** At 21:9 each slot is small. Does the separate product reference fully carry print and stitching? Or should SANTO use a 4-slot board (3–4 s per cut) for garments with detailed prints?
3. **Seedance 2.5 on Higgsfield, live limits:** the catalogue now lists start/end roles and 1080p, but not max image references or cost. Also, Higgsfield's own SKILL.md passes the board with role `image` while its clip reference file uses `image_references`. Which binds better?
4. **Do Elements (`<<<id>>>`) work with `seedance_2_5`?** The tool description (truncated) lists Seedance 2.0 and Kling 3.0.
5. **Soul ID photo count:** the MCP says 5–20; Higgsfield help and blog pages say 20–80 (ideal 20–25). This may reflect Soul v1 vs v2 training. The UGC flows don't use trained identity at all.
6. **Credit cost** of Ad Multiplier, Genjutsu and Marketing Studio per 15 s. It isn't exposed by `models_explore`. Is `get_cost:true` free on all video models? The community says yes for Seedance; unverified here.
7. **Higgsfield's "beauty floor"** (every generated creator must have "high model facial features, symmetrical features") may push away from the "real person on a phone" goal. Is SANTO better off overriding it with ordinary-looking casting, keeping the skin-texture anchors?
8. **Pull-on on camera:** the MCP try-on recipe hides it behind a cut, while the Marketing Studio PDF example shows a t-shirt pulled on inside a 4 s static full-body clip. Which is more reliable for a SANTO hoodie? A cheap A/B test would settle it.
9. **Web search budget ran out** before I could read Higgsfield Academy "Marketing Studio Try-Ons", the Genjutsu cost guide (openyourais.com) or Recast / Draw-to-Video / Popcorn pages. Worth a follow-up if another researcher has budget.

## Sources
- Higgsfield MCP (read-only): `get_workflow_instructions` for ugc-review-video, ugc-unboxing-video, ugc-try-on-video, ugc-product-video, product-photoshoot, ad-multiplier, character-sheet; `get_workflow_bundle_file` (references/*); `get_preset_instructions` (/genjutsu, catalogue); `models_explore` list/get/recommend. Saved in `research/hf-notes/`.
- https://higgsfield.ai/blog/generating-with-seedance-2-0 (via search summary)
- https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-create-and-use-a-soul-id-character ; https://higgsfield.ai/blog/Soul-ID-AI-Character-Consistency ; https://note.com/laura_glory/n/n6ec46b730f4d (Soul ID photo guidance, via search)
- https://higgsfield.ai/blog/higgsfield-genjutsu ; https://higgsfield.ai/genjutsu (via search)
- https://higgsfield.ai/blog/Higgsfield-UGC-Factory-Explained ; https://higgsfield.ai/skills/ugc ; https://higgsfield.ai/marketing-studio-intro ; https://higgsfield.ai/academy/courses/brand-visuals-ai/marketing-studio-try-ons (titles and summaries via search)
- https://sacra.com/research/alex-mashrabov-higgsfield-ai-video-production/ (Mashrabov: camera control was the top creative-director complaint)
- GitHub (cloned to `research/repos/`): https://github.com/joebenscoter86/higgsfield-ugc-workflow ; https://github.com/charlesdove977/UGC-Factory ; https://github.com/OSideMedia/higgsfield-ai-prompt-skill ; https://github.com/AKCodez/higgsfield-claude-skills

---

# PART 4 — `02-model-guides.md`

## 02 — Model guides: the knobs Cutroom is not using

Source focus: official and expert prompting guides for the generation models (video + keyframe image editors), 2026-09-24.

**How much to trust this.** The Seedance, Kling and Wan ecosystems are flooded with SEO copy that repeats numbers that contradict each other. I weighted:
- **A (vendor docs):** OpenAI Cookbook Sora 2 guide and GPT Image guide (read raw from GitHub); Google Cloud "Ultimate prompting guide for Veo 3.1" and "…for Nano Banana" (fetched in full); Gemini and Veo API limits (from search summaries of ai.google.dev and cloud docs).
- **Seedance official guide, second-hand:** WebFetch blocks `docs.byteplus.com`. I read two independent practitioner repos that transcribe the BytePlus / Jimeng 2.0 and 2.5 prompt guides: Grégory Beyrouti's `seedance-prompting-claude-skill` (in French) and Serge Shima's `smixs/visual-skills`. They agree on the rules below, so I grade these **A-**.
- **Kling official material:** kling.ai quickstart and blog, known only from search summaries. Graded B unless noted.
- **"Model X wins at Y" comparisons:** mostly C. I say so wherever I use one.

Local copies are in `research/repos/`: `sora2.txt`, `image-gen-models-prompting-guide.txt`, `Generate_Images_With_High_Input_Fidelity.txt`, `seedance-prompting-claude-skill/`, `visual-skills/`, `awesome-kling/`, `awesome-seedance-2.5-api-prompts/`.

---

## 0. Hard facts that change routing today

| Model | Limits that matter for 15s 9:16 UGC | Source (strength) |
|---|---|---|
| **Seedance 2.0** | 4–15s. Up to 12 refs: ≤9 images, ≤3 videos (≤15s total), ≤3 audio (≤15s total). Every video/audio ref must be ≥2s. Audio refs need at least one image or video ref alongside them. **Rejects real human faces** in refs (Higgsfield reports this as a "visual restriction"). Negative prompts are fragile. | invideo / cliprise / magichour summaries; mindstudio / clipdance on faces (B) |
| **Seedance 2.5** (released 2026-07-31) | 4–30s single pass. Refs: 30 images (each ≤4K) + 10 videos (≤30s total) + 10 audio (≤30s total). Live API output is **480p/720p only** (1080p/4K are upscales). Bans ("no subtitles, no BGM") now work. Timestamps are honoured to the second, but windows must be ≥3s. Adds edit and extend modes, plus a `camera_fixed` flag and `return_last_frame`. | smixs seedance-25.md; gbeyrouti skill; awesome-seedance-2.5 README (A- / B) |
| **Kling 3.0 / Turbo / Omni** | 3–15s. Multi-shot up to 6 shots, each needing its own framing. Native audio and lip-sync in 5 languages. `cfg_scale` 0–1, default 0.5. Omni Elements: ≤4 multi-angle stills or one 3–8s video, plus 5–30s voice binding. Turbo caps at 1080p, but has the best lip-sync per dollar. | kling.ai blog and quickstart summaries; smixs kling.md (B) |
| **Kling Motion Control 3.0** | Reference video 3–30s; output length follows the reference. Orientation "image" allows up to 10s, "video" up to 30s. | kling.ai motion-control guide via search (A-) |
| **Wan 3.0** (formal release 2026-08-24) | Native 30s, up to 1080p, audio generated by default. Accepts text, image, video, audio, docs and URLs as references. Reviews flag: **soft hands, weak lip-sync, cuts to angles nobody asked for, invents small logo and colour details.** | Alibaba blog, TNGlobal; Curious Refuge, atlascloud and buildfastwithai reviews (B/C) |
| **Wan 2.2 Animate / VACE** | Animate has two modes, animation and replacement. Replacement uses a relighting LoRA to match the plate. VACE is best on clips ≤7s, and breaks when the first-frame pose doesn't match the reference. | wan.video blog; Wan2GP docs; ComfyUI wiki (B) |
| **Veo 3.1** | 4/6/8s; 16:9 or 9:16; 720p, 1080p, 4K. **Up to 3 asset reference images of a single person/character/product.** Passing refs, or choosing 1080p/4K, **locks duration to 8s**. Keep speech to ≤8s. | ai.google.dev/veo via search; Google Cloud blog (A) |
| **Sora 2** | **The API is removed today (2026-09-24). The app died 2026-04-26.** Don't build on it. Its guide's lessons carry over to other models (see T12). | OpenAI Help Center and multiple outlets (A) |
| **MiniMax H3 (Hailuo 3.0)** | 5–15s, up to 2K, 24fps, native stereo audio. Refs: 9 images + 3 videos + 3 audio. Accepts edits as one-sentence instructions. Practitioners say H3 "errs by omission" (drops shots from the list), Seedance 2.5 "errs by commission" (does every instruction, sometimes misusing a reference). | minimax.io blog; smixs (B/C) |
| **Runway Aleph** | Video-to-video edit. **5s maximum per pass**, 1 reference image in the API, prompts ≤1000 characters. | Runway help center summary (A-) |
| **Nano Banana Pro / NB2** | Up to 14 refs. **Pro: ≤6 high-fidelity object refs + ≤5 human character refs. NB2: ≤10 objects + ≤4 characters.** Numeric lens specs (50mm, f/2.8) are largely ignored. | Gemini docs via search; Google Cloud NB guide (A); smixs (B) |
| **GPT Image 2** | `input_fidelity` is fixed at high on gpt-image-2. On 1.5 you set `input_fidelity=high`. **The first input image keeps the finest detail.** Up to 16 refs. Results above 2560×1440 are "experimental". | OpenAI Cookbook (A) |
| **Seedream 4.5** | Up to 10 refs (some platforms say 14). Sweet spot is 30–100 words; beyond 150 words instructions start competing. | BytePlus docs via VEED / WaveSpeed summaries (B) |

---

## Techniques

### T1. Declare a role for every reference, and exclude what should not bleed through
**How:** One line per asset: what it defines, then what *not* to take from it. Seedance's official pattern:
```
<Model: Maya> corresponds to @Image 1. Use only the face, hair and body.
<Product: SANTO grey fleece hoodie> corresponds to @Image 2, @Image 3, @Image 4. All these images define one single hoodie. The output must contain only one hoodie. Use only its structure, fabric, colour, print and stitching. Do not use the image background.
<Room: Maya's bedroom> references @Image 5. Use only the spatial layout, furniture and lighting. Do not use any people in the image.
@Video 1 defines only the camera movement and pacing. Do not use its person, clothing or scene.
@Audio 1 defines only the voice timbre and accent. Do not copy its words.
```
Rules that go with it:
- **Never use the collective form.** "@Images 1–4 define four characters" is explicitly the forbidden pattern, because it never says which is which.
- **Don't re-describe in text what a reference already carries.** If @Video 1 defines the motion, restating the motion in prose fights the reference.
- **Re-@ the same asset several times** through the prompt. The official guide says repeated mentions increase accuracy.
- **Fixes:** F1, F2, F7 (props and posters leaking in from a room photo), F3 (a motion clip leaking its actor's hands).
- **Evidence:** BytePlus/Jimeng Seedance 2.0/2.5 guide as transcribed in `seedance-prompting-claude-skill/references/references-et-modes.md` and `visual-skills/video/references/seedance-25.md` §5 (A-).
- The same role-index rule appears in:
  - OpenAI GPT Image guide: "Reference each input by index and description… be explicit about which elements move where" (A).
  - Google's Nano Banana guide, formula `[Reference images] + [Relationship instruction] + [New scenario]` (A).
- **Input change:** each stored reference asset carries a `role` (identity / product / room / motion / voice) and an `exclude` list. Cutroom then auto-writes the declaration block in upload order, most important reference first ("the model weights early references more heavily", awesome-seedance-2.5; B).
- **Cheapest test:** one Seedance 2.x shot with the current prompt vs. the same refs plus the declaration block. 2 × ~18 cr.

### T2. Multi-angle product refs: separate images, declared as one object
**How:** Upload front, back and detail (tag, cuff, print) as **separate images, not a collage grid**. Always add: *"All these images define one single [hoodie]. The output must contain only one."* Without that line the model duplicates the subject, e.g. two hoodies or a second bag.
- In image editors, feed product angles as "valid angles of the same garment" and only switch angles at hard cuts. This is already in the HF workflow notes; Seedance's official guidance matches it.
- Comfort zone, per the official stability table:
  - 1–8 subjects across the image refs.
  - Up to 5 subjects: any multi-view sheet works.
  - More than 5 subjects: single views only.
  - Separate images beat a collage.
- **Fixes:** F2, F7 (duplicate products)
- **Evidence:** Seedance official guide via both repos (A-); `debug-et-limites.md` matrix row "Sujet dupliqué".
- **Input change:** the product kit stores each angle as its own file with an `angle` tag. Collages/contact sheets are not allowed as refs. Auto-append the one-object clause.
- **Cheapest test:** a 1-shot unboxing with 3 product angles, with vs. without the clause. 2 × 18 cr.

### T3. Pick the references needed for each shot; never fill every slot
**How:** Send only the references the shot needs: identity + product + room, and maybe one motion ref. ByteDance's own guidance is that using the full allowance *degrades* results, because the model can't tell what to prioritise. Keep to 1–8 image subjects and 1–5 video subjects of 5–10s each. For longer pieces use a per-scene `Use:` line (`Scene 1 | Use: <Maya>, <hoodie>, <bedroom>. Event: … End state: …`).
- **Kling Omni:** several practitioners report *visible image-quality loss the moment Elements/refs are enabled*. Enable Elements only when the shot needs cross-shot identity. For a one-off shot, use in-prompt labels instead.
- **Fixes:** F1, F2, F6, F9
- **Evidence:** invideo, citing ByteDance ("too many references… struggles to judge which ones to prioritize", B); smixs kling.md §7 (B).
- **Input change:** the shot spec carries an explicit `refs_used` subset. Warn at >5 images per shot.
- **Cheapest test:** the same shot with all refs vs. only the 3 needed. 2 × 18 cr.

### T4. First/last frame: declare each anchor separately, and pin the last frame to stop the ending drifting
**How:**
- The two images **must share the aspect ratio**, or the last frame gets stretched.
- Never write "@Images 1 and 2 are the first and last frames". Declare each separately, then add identity refs that don't override either composition:
```
@Image 1 is the first frame. It defines the opening composition, subject position, pose, prop state, scene, and camera direction.
@Image 2 is the last frame. It defines the ending composition, pose, prop state…
@Image 3 defines Maya's appearance. Do not change the first-frame composition defined by @Image 1 or the last-frame composition defined by @Image 2.
<one continuous action>. The video begins naturally from @Image 1 and reaches @Image 2 after the continuous action. Between them, maintain continuity in identity, prop structure and ownership, scene layout, camera direction.
```
- Pinning the last frame removes the "ending drifts" failure. The skill calls this "a cost tool as much as a quality tool".
- **Other models:**
  - Veo 3.1 (Google): describe the transition *and the audio* you want between the two frames.
  - Seedance 2.5 video-extend takes a `last_image` target.
- **Fixes:** F4, F1, F7
- **Evidence:** Seedance official guide via both repos (A-); Google Cloud Veo 3.1 guide (A).
- **Input change:** keyframe pairs are generated at the target 9:16 ratio and validated as the same ratio. The start/end prop state is stored explicitly: bag sealed / bag open, hoodie folded / on.
- **Cheapest test:** mailer-bag open with first+last frame vs. first frame only. 2 × 18 cr. Or 2 × 3.5 on Wan 3.0 as a pre-test.

### T5. Write each state change as a stage with a visible end state, and budget time instead of cramming it
**How:** One primary state change per stage, always ending in an observable state:
```
[Stage 1] Initial state: sealed grey SANTO mailer on the bed, Maya's right hand on it. Primary event: she tears the perforated strip along the top edge. End state: bag open, strip hanging, hoodie folded inside, not yet visible.
[Stage 2] Continue from previous: same bag, same hand. Primary event: she slides the folded hoodie out with both hands. End state: hoodie on her lap, empty bag on the bed to her left.
[Maintain Consistency] one bag, one hoodie, prop ownership, left/right positions.
```
Timing rules:
- Timecodes are **time budgets, not edit points**.
- Each window ≥3s, holding one core action + one camera move.
- Never ask for a rate ("three actions in one second").
- ≤4 shots in 30s. For 15s Cutroom ads that means ≤3 shots per generation.

Two more official tricks:
- **Consequence chains:** "hand grips the strip → the strip actually tears → the bag mouth opens". A broken chain shows a failed generation at a glance.
- **Directive + subtext:** after the physical directive, say why the character does it. "Emotion analysis: she's pleasantly surprised the fleece is heavier than expected."

The official guide says the **same character in two states is "the flakiest binding in 2.5 — budget re-rolls."** This backs your cut-to-transform rule: bind each state to a separate image slot and time range, or cut between them.
- **Fixes:** F4, F7, F1
- **Evidence:** smixs seedance-25.md §6/§11/§17 (A-); gbeyrouti structure-et-syntaxe.md (A-); Veo 3.1 timestamp prompting `[00:00-00:02] …` in the Google Cloud guide (A).
- **Input change:** the storyboard gate stores for each beat: `initial_state`, `event`, `end_state`, `emotional_state`. The prompt is compiled from those fields.
- **Cheapest test:** re-prompt a previously failed rip-open shot in stage format. 18 cr.

### T6. Negatives work differently per model: know what each one accepts
- **Seedance:** negate a *source*, a *track*, or a *manufacturing defect*. Never negate a visible object.
  - Works: `Do not use the people in @Image 2`, `no background music, no text overlay, no captions`, `no drift, no deformation, no flickering`.
  - Backfires: `no red car`, `no blur`, `don't show her hands`. These can summon the thing you banned. Rephrase positively: `sharp, in-focus`, `single window as the only light source`, `bare skin, slight redness around the nose`.
  - 2.5: bans are reliable. Repeat them in a global tail at the end.
  - 2.0: bans are fragile, so avoid even *mentioning* on-screen text or music.
- **Kling:** it has a dedicated negative field that reads everything as exclusion. **Write the noun, not "no X"**: `distorted hands, extra fingers, melted face, subtitles, logo, jitter`. Keep it short: "long negative stacks reduce motion and detail". For products: `wrong logo, gibberish typography, brand morph, label melt, extra bottles, plastic skin, exaggerated HDR`.
- **Veo / Nano Banana (Google):** describe the absence positively. "a desolate landscape with no buildings" beats "no man-made structures"; "empty street" beats "no cars".
- **Fixes:** F2, F6, F8, F9
- **Evidence:** Seedance official negation rule via gbeyrouti SKILL.md (A-); Kling via smixs kling.md §6 and awesome-kling negative-prompts.md (B); Google Cloud Veo and NB guides (A).
- **Input change:** keep a separate negative block per model family. Compile it to the right grammar at routing time.
- **Cheapest test:** free (a prompt linter). Then one A/B at 18 cr.

### T7. Audio: always write an audio block, and control music outside the model when you must
- **Seedance 2.5 has dedicated markers:**
  - dialogue in `{…}`
  - SFX in `<…>`
  - music in `(…)`
  - on-screen titles in `【…】`
  - language and accent go *before* the line, e.g. `Dialogue language: British English, London accent. She says casually: {Honestly heavier than I thought.}`
  - fal and most relays use plain double quotes instead.
  - With no audio block, Seedance invents a track, usually ad music. Always end with `no background music`.
- **Veo 3.1:** use a lead-in verb (`says`, `whispers`) and put modifiers before it. Colon form (`She says: "…"`) is often more reliable than a comma. Use `Audio:` / `SFX:` labels. Keep speech ≤8s, or the delivery speeds up unnaturally.
- **Kling 3.0 dialogue protocol, P1–P4 (from the fal guide):**
  - P1: a unique speaker label.
  - P2: **bind each line to a visual action first**, e.g. "Maya holds the hoodie up to camera and says:". Without that anchor, lip-sync drifts.
  - P3: voice tone inside the tag: `[Maya, relaxed low voice]:`.
  - P4: a linker such as "Immediately," between lines, or the lines overlap.
- **Kling ignores "no music":** the model lays music even against a negative prompt. Generate with `generate_audio` off, or strip the music track and add room tone and VO in post.
- **Line length:** Sora's guide puts a 4s shot at 1–2 short exchanges. Practitioner Seedance UGC templates keep each line under 12 words.
- **Fixes:** F8
- **Evidence:** Google Cloud Veo guide (A); Sora cookbook (A); smixs kling.md §3 citing fal (B); gbeyrouti audio section (A-).
- **Input change:** the script is stored per shot with a word budget derived from the shot's seconds. A per-model audio compiler emits the right markers.
- **Cheapest test:** one Kling talking shot with P2+P3 vs. a plain quoted line. 2 × Kling cost.

### T8. Never make the mouth speak while an action blocks it
**How:** When lip-sync collides with drinking, biting, pulling a hoodie over the head, or a phone covering the mouth, split it into two shots and cut: "action, no dialogue" + "dialogue, mouth unobstructed". The dialogue shot should have no occluding action.
- The Kling practitioner note says this directly for drinking + lines.
- The Higgsfield workflow notes (already in-house) do the same for macro shots: voice-over with the mouth closed.
- **Fixes:** F8, F4, F3
- **Evidence:** awesome-kling kling-3-omni.md tuning note (B); consistent with P2 above.
- **Input change:** a storyboard linter flags any beat with `dialogue` plus a mouth/face-occluding action.
- **Cheapest test:** free (a rule).

### T9. Borrow a real voice for timbre only
**How:**
- **Kling Omni:** bind a 5–30s voice clip to the element, then tag it `<<<voice_1>>>`. Don't also describe the voice in text.
- **Seedance:** attach `@Audio 1` as "voice timbre and accent reference only — do not copy its words". The ≥2s minimum applies, and an image or video ref must accompany it. The HF notes say text alone lands the accent about 1 in 3 times; the voice-sample fix already exists in those notes.
- **Seedance 2.5 edit mode** can re-dub an existing clip: "Remove only the original background music. Keep dialogue, lip sync, ambience…". Or replace the narration language while keeping performance and product.
- **Fixes:** F8
- **Evidence:** Kling Omni lip-sync blog via search (B); Seedance official edit pattern (A-).
- **Input change:** keep a per-persona voice sample of 5–10s, recorded or licensed, stored with the persona.
- **Cheapest test:** 1 Seedance shot with vs. without @Audio. 2 × 18 cr.

### T10. Put the realism layer in the first 20–30 words; don't tack it on at the end
**How:**
- Seedance follows the first 2–3 instructions faithfully. It deprioritises after about 8 requirements, or 150–200 words per block.
- So the order is: subject + action → consistency anchor → **texture/realism** → light → set → one camera move → emotional arc → audio → exclusions.
- The seven-layer UGC block (verbatim, from gbeyrouti `realisme-et-ugc.md`):
  - **skin:** `realistic skin texture, visible pores around the nose and cheeks, natural slight unevenness, no filter quality`. The official 2.5 "fidelity suffix" is `retaining real fine pores and skin texture`.
  - **anti-polish:** `handheld phone camera feel, casual unsteady framing, filmed in a real environment, not a professional set`. State it positively; negate only the production *register*.
  - **light on four axes:** direction, quality, shadow behaviour, skin exposure. E.g. `soft warm window light from camera-left, natural shadows across the face, no harsh highlights, skin not overexposed`.
  - **named clutter:** 3–4 *concrete* objects. "A charger cable on the nightstand reads as a real bedroom; 'a lived-in room' produces nothing."
  - **micro-motion:** `subtle handheld motion mimicking a propped-up phone, slight micro-shake from breathing`.
  - **emotional arc with visible cues:** opening, midpoint, close.
  - **anchor + exclusions:** `maintain exact appearance from @Image 1, no drift, no deformation … no background music, no captions`.
- The first words set the register. The practitioner Seedance UGC formula opens with `UGC creator` / `iPhone handheld`, and forgetting that "defaults the model to a slicker commercial look". Its claim of a 30%→70% hit rate is unmeasured (C).
- The OpenAI cookbook agrees for stills: prompt "as if a real photo is being captured in the moment… ask for real texture… avoid words that imply studio polish" (A).
- Sora's guide shows the same register switch: "the same details read very differently for a polished Hollywood drama vs a handheld smartphone clip — establish style early" (A).
- **Fixes:** F6
- **Evidence:** A- (Seedance official ordering rules) plus B/C (UGC layer).
- **Input change:** a prompt compiler with fixed slot order. The realism block is a required template field, not an optional suffix. Store 3–4 named clutter objects per real room photo.
- **Cheapest test:** the same shot with realism at the head vs. the tail. 2 × 18 cr, or 2 × 3.5 on Wan 3.0.

### T11. Fix slow, floaty motion with counted beats, a fitting duration, and speed ramps in post
**Why it happens:** Models default to slow motion "because gradual frame-to-frame changes are easier to keep consistent" (LTX; B). Frame rate does not fix it; the model decides how much change happens per frame.

**Prompt-side fixes:**
1. **Counted beats instead of vague verbs.** Sora guide: not "walks across the room" but "takes four steps to the window, pauses, and pulls the curtain in the final second" (A).
2. **Don't give a 3s action 8s of runtime.** An action that is too short for its clip gets stretched into slow motion. Match seconds to beats (≥3s per beat on Seedance). Sora: "stitch two 4s clips instead of one 8s" (A).
3. **Kling obeys tempo words:** "quick snap" (1–2s), "moderate" (3–5s), "slow and deliberate" (5–8s). Also `real-time`, `steady speed`, and a surface with friction (B).
4. **Model choice:** smixs reports that Kling's motion model "was trained on slow, deliberate movement". It suits fashion drift, and fights snappy UGC.

**Inverse trick for fast, deformation-prone actions** (zip pull, shake-out, rip): generate the action slower on purpose, then **speed-ramp it 1.25–1.5× in post**. "The model holds geometry at slower internal motion" (smixs kling.md §11; B).

**Open-source only:** lower CFG (LTX: cfg 2.0–2.5) gives more frame-to-frame motion.

- **Fixes:** F6, F3, F4
- **Input change:** each beat carries `seconds` and a `speed` tag (`real-time` / `snap` / `slow-then-ramp`). The finishing step applies a per-shot playback speed (1.0–1.5×) and trims dead head/tail frames.
- **Cheapest test:** free in post on existing floaty clips (retime to 1.2–1.4×). Then 1 regeneration with counted beats (18 cr).

### T12. Shorter clips drift less: put continuity in the edit, not the model
**How:**
- Seedance drifts after about 10s without anchoring: "the face slides, the logo dissolves, the camera loses its logic".
- Sora (OpenAI): "the model follows instructions more reliably in shorter clips".
- VACE works best at ≤7s; Aleph edits 5s per pass; Seedance editing works best on sources ≤20s.
- For a 15s ad: 3–4 generations of 3–5s, cut together, beat most single 15s passes on identity and product. The exception is Seedance 2.5 / Kling multi-shot *with* refs, where one pass keeps the voice and lighting continuous.
- **Fixes:** F1, F2, F7, F9 (a bad 4s shot costs less to re-roll than a bad 15s one)
- **Evidence:** OpenAI Sora cookbook (A); Seedance drift observation (gbeyrouti / wavespeed, B); VACE and Aleph docs (A-/B).
- **Input change:** the router picks the per-shot length. A "single long pass" is allowed only when the shot is dialogue-continuous.
- **Cheapest test:** a 15s single pass vs. 3 × 5s on the same model. Seedance cost scales with seconds, so the cost is roughly equal.

### T13. Image-to-video: the prompt describes only motion, and says what to preserve
**How:**
- When a keyframe exists, **don't re-describe what's in it**. Re-describing causes identity drift.
- Kling I2V: 20–40 words, motion-focused, led by an explicit preserve cue, e.g. `Preserve face, hoodie print and chest logo exactly. Slow handheld push-in. She turns the hoodie to show the back print, exhales a small laugh.`
- Veo: add `maintain the subject from the first frame`.
- **UI gotcha:** if a camera-lock toggle is on (Seedance `camera_fixed` / UI "fixed" mode), camera moves you asked for are silently ignored.
- **Fixes:** F1, F2, F7
- **Evidence:** smixs kling.md §10 and veo.md §7 (B); gbeyrouti structure-et-syntaxe.md T2V-vs-I2V table (A-).
- **Input change:** two prompt templates (T2V-like with refs vs. I2V from a keyframe). The I2V one strips appearance text automatically and injects a `Preserve:` line from product-kit critical features (logo, print, tag).
- **Cheapest test:** a re-run of a failed I2V shot with the stripped prompt. ~3.5–18 cr.

### T14. Kling Elements and multi-shot: settings that matter
- **Build Elements from 3–4 angles** (front, three-quarter, profile, back) or a **3–8s video**; the video also captures the voice.
  - Source images: 1080p+, even light ("hard shadows get mistaken for permanent facial features"), no text or watermark, clean background.
  - Make the *product* an element too.
  - Tag in prose: `@Maya holds up @SantoHoodie`, or `<<<element_1>>>` in syntax 2.0.
- **Multi-shot collapses into one take** if two adjacent shots share framing *and* angle. Each `Shot N (a–bs)` needs a different framing.
- **cfg_scale 0.7–1.0** for product / "do exactly this" shots; 0.3–0.4 for creative freedom.
- **Master Shot camera presets** are more stable than hand-written camera prose, and cost fewer re-rolls.
- **Fixes:** F1, F2, F9
- **Evidence:** Kling subject-binding blog / quickstart summaries (B); smixs kling.md §3/§7/§11 (B).
- **Input change:** the persona and product kits export a Kling element pack of 4 angles. The router sets cfg per shot type.
- **Cheapest test:** 1 Kling product shot at cfg 0.5 vs. 0.8.

### T15. Drive motion with a real phone-filmed performance, and keep the real product in frame when you can
**What's new beyond your existing "movement library":** the framing-match rules, and Wan's replacement mode.
- **Kling Motion Control:**
  - Reference 3–30s, clear, moderate-speed movement, subject roughly centred.
  - **Match the framing**: a full-body walk reference paired with a close-up portrait "compresses the skeleton", causing distortion.
  - Leave canvas around the character for arm moves; don't crop tight.
  - Orientation "video" allows up to 30s, "image" up to 10s.
  - Prompt pattern: `Motion reference: @video (body timing + camera energy only). Identity: @image. No identity bleed from motion clip.`
- **Wan 2.2 Animate:**
  - **Replacement mode** swaps only the person in *your real footage*. It keeps the plate's lighting and colour via the relighting LoRA.
  - So a real hand, real hoodie and real mailer stay real if they're outside the mask. This fixes F3/F4/F5 at the source.
  - Reference guidance: mid-shot with shoulders and hands visible, clear hand motion with no heavy blur, don't crop tight on the face.
- **VACE:**
  - Depth control keeps silhouette and camera parallax.
  - It falls apart if the first-frame pose differs from the reference, or if a close-up pose is paired with a full-body reference.
  - ≤7s.
- **Seedance 2.5 edit:** "replace the presenter with …; keep the camera movement, blocking, performance pacing, scene, **and product**" (official localisation pattern).
- **Fixes:** F3, F4, F5, F6
- **Evidence:** kling.ai motion-control guide (A-); wan.video Animate blog (A-); Wan2GP / ComfyUI docs (B); Seedance official edit pattern (A-).
- **Input change:**
  - New asset type: "real plate": 5–10s phone clip of the real product handled by a stand-in (hands visible, persona-matched framing).
  - Each movement-library clip is tagged with its framing (full / mid / close).
  - The router refuses a motion-ref + keyframe pair whose framing differs.
- **Cheapest test:** film one 6s real hoodie-on clip, then replace the person via Wan Animate or Higgsfield's motion/replace route. Roughly Wan tier, under ~10 cr.

### T16. Repair with edit and extend instead of re-rolling the whole shot
**How (Seedance 2.5 edit mode, official template):**
```
[Edit Goal] Edit @Video 1. Within 3–6s, replace the hoodie's chest print.
[Source Video Role] @Video 1 is the sole editing master…
[Target Material Role] @Image 1 defines the correct print.
[Edit Scope] Modify only the chest print area.
[Content to Preserve] Keep identity, face, hair, lip movement, original voice, speech rhythm, gestures, camera position, focal length, aspect ratio, room, total duration from @Video 1.
[Timeline Inheritance] (for object swaps) The new object inherits every appearance, motion, occlusion and exit of the original…
```
- "The longer the keep-list, the less drift."
- Source ≤20s; one edit target per pass; ratio and duration locked to the source (±0.3s).
- Background swap scope: "modify only the background outside the subject's silhouette".
- Where the platform has it, **segment reshoot** regenerates only the bad span and leaves everything else identical (Xiaoyunque).
- **Chaining settings:**
  - `return_last_frame=true` gives a watermark-free PNG for the next shot.
  - Use `mov` (yuv444) output when extending repeatedly.
  - Extension clause: "Keep each subject as the same continuous instance throughout: do not duplicate or split it."
- **Other edit tools:**
  - Runway Aleph (5s chunks): verb-led edits ("replace / remove / re-light") + what stays stable.
  - MiniMax H3 accepts one-sentence edits.
- **Fixes:** F9, F2, F7, F8
- **Evidence:** smixs seedance-25.md §12–14 (A-); awesome-seedance-2.5 native params (B); Runway help (A-).
- **Input change:** the QA-reject path offers "edit this span" before "re-roll". The rejection taxonomy maps to edit templates: wrong print → print swap; extra prop → object removal; music → audio-only edit.
- **Cheapest test:** one print-fix edit on an existing near-miss clip, vs. the re-roll cost (18 cr).

### T17. Use a storyboard grid or a camera-path sketch as one reference image
**How:**
- Seedance officially accepts one storyboard grid (≤15 panels, clean line art, little text). Declare the reading order and exclude its style: `@Image 1 provides a 4-panel storyboard grid for shot order and approximate composition. Read left to right, top to bottom. Do not use the grid's line-art style, text labels, or placeholder characters.` Then `Shot 1: … Shot N: …`.
- A top-down **camera-route sketch** also works as `@Image N`: "follow the camera route in @Image N".
- Independent keyframes align better than a grid when exact composition matters.
- **Corroboration:** Higgsfield's own UGC workflows (see `hf-notes/notes1.md`) send a 21:9 board of 9:16 slots to seedance_2_5 omni_reference, and the slots become hard cuts. That is the same mechanism, so it's validated in production.
- **Fixes:** F7, F9, F1
- **Evidence:** Seedance official (A-); HF workflow notes (A for the in-house platform).
- **Input change:** the storyboard gate's approved board image is passed as a reference directly, not only used for human review.
- **Cheapest test:** board generation ~1.5 cr (NB) + 18 cr clip.

### T18. Keyframe editors: reference order, slot limits, and restating the preserve list
- **GPT Image:**
  - "While all input images are preserved with high fidelity, **only the first one is preserved with extra richness in texture**."
  - Put the face first for persona shots, and the product first for product-macro shots.
  - For several faces, "**combine all needed faces into a single composite image** before sending".
  - gpt-image-2 always runs at high fidelity. On gpt-image-1.5 set `input_fidelity="high"`, which costs more input tokens.
  - Verbatim try-on prompt from OpenAI: "Do not change her face, facial features, skin tone, body shape, pose, or identity… Replace only the clothing, fitting the garments naturally to her existing pose and body geometry with realistic fabric behavior. Match lighting, shadows, and color temperature… Do not change the background, camera angle, framing… do not add accessories, text, logos."
  - **Iterate**: one change per iteration, and "repeat the preserve list on each iteration to reduce drift".
- **Nano Banana:**
  - **Pro:** ≤6 high-fidelity object refs, ≤5 human refs. **NB2:** ≤10 objects, ≤4 characters.
  - Role syntax: `[Image 1: face] [Image 2: garment] [Image 3: room] Combine… Match lighting and perspective.`
  - Specify material ("heavyweight grey cotton fleece", not "a hoodie").
  - Numeric lens values are ignored. Describe the look instead ("shallow depth of field", "wide-angle distortion").
  - "Edit, don't re-roll" when the image is ~80% right.
  - Some reports say Pro holds faces *worse* than NB2. Test both for persona series.
- **Seedream 4.5:** 30–100 words. Name each image's job ("replace the character in Image 2 with the character from Image 1, style of Image 3").
- **Flux Kontext:** "This person…" + change + "while maintaining the same facial features, hairstyle, expression". Name identity markers explicitly, or the edit drifts.
- **All image models:** generate in the **final 9:16 ratio**. Cropping after animation is a silent failure, and Seedance first/last frame locks the ratio to the first image.
- **Fixes:** F1, F2, F5, F7
- **Evidence:** OpenAI Cookbook high-input-fidelity and GPT Image guides (A); Gemini docs via search (A); Google Cloud NB guide (A); Seedream via BytePlus-derived summaries (B); Kontext (B/C).
- **Input change:** the reference-ordering policy per shot type is enforced in code. The preserve list is re-sent on every edit call. A persona with 2 people means pre-compositing faces into one image.
- **Cheapest test:** NB edit with the product first vs. the person first, checking logo sharpness. 2 × 1.5 cr.

### T19. De-slop keyframes by naming the capture chain, not by asking for "realistic"
**How:**
- Name the device and file path as a fact of the image:
  - `a real phone photo, auto HDR off, smeared shadow noise, slightly flat tone`
  - or `grabbed from handheld footage`
- **Place ≥3 located imperfections** ("creases at the elbow bend", "two flyaways above the crown", "scuffed baseboard behind her"). An unlocated imperfection is ignored or sprayed everywhere.
- **Ban booster words** in positive slots: 4K, 8K, ultra-detailed, hyperrealistic, masterpiece, sharp focus, flawless.
  - On GPT Image they actively degrade output.
  - On Nano Banana they're inert but push out the useful facts.
- **Settings:**
  - GPT Image: stay at `quality: medium` for unretouched looks. `high` sharpens micro-texture until it reads as retouching.
  - Nano Banana: add `natural contrast, no HDR look`. It tends toward overcooked HDR and oversaturation.
- **Selfie optics** (practitioner, C): front camera, arm's length, ~24mm wide. It slightly enlarges the nose bridge and compresses the ears.
- **Fixes:** F6
- **Evidence:** smixs de-slop.md and nano-banana.md (B); OpenAI photorealism example: "honest and unposed… real skin texture, worn materials… No glamorization, no heavy retouching" (A); Google NB guide on camera-hardware "visual DNA" (A).
- **Input change:** the realism block for stills is a template with slots for `capture_device`, `imperfections[3]` and `grade`. Booster words are linted out.
- **Cheapest test:** 2 NB stills. ~3 cr.

### T20. Never let the video model draw brand text; protect logo shape instead
**How:**
- Treat logos and wordmarks as geometry to preserve (I2V `Preserve chest logo exactly`, product refs), never as text to render.
- Exclude captions, titles and subtitles in every video prompt, and add them in post.
  - Seedance official: "subtitles, signs, product specs, brand typography: go through prepared references + post-production; the prompt alone guarantees nothing."
  - Wordmarks often render as gibberish, or as a *real competitor's* brand (HF notes).
  - Wan 3.0 reviewers saw it invent logo variations and wrong colours.
- For stills that must contain text:
  - GPT Image: quote it and spell it letter by letter, `quality high`, "render exactly once, no extra text".
  - Nano Banana: generate the text first in conversation, then ask for the image with that text.
- **Veo colour bleed:** mood words can recolour props. Veo's JSON format keeps product colours in a `continuity` block, away from `global_style`.
- **Fixes:** F2
- **Evidence:** Seedance official (A-); OpenAI Cookbook (A); Google NB guide (A); smixs veo.md §6 (B).
- **Input change:** product-kit fields `logo_zone` and `critical_text`. The video compiler never emits the brand string, only "the chest logo from @Image 2".
- **Cheapest test:** free lint. Then one NB logo-closeup keyframe (1.5 cr).

### T21. Hands: pick framing that suits the model; don't just describe hands
**Model guidance for hands:**
- Seedance names "fine hand gestures" as a real weakness.
- The fix hierarchy:
  1. Widen the framing, or frame hands out (`close-up on face, shoulders up`).
  2. `hands at rest`.
  3. Slow, deliberate gestures.
  4. Put the hand action in a separate insert shot.
- Positive anatomy phrasing on Seedance/Veo: `anatomically correct hands, clean finger separation, realistic proportions`.
- Kling: negative-field nouns (`fused fingers, extra fingers, deformed hands`).
- GPT Image stills: describe the interaction geometry ("hands naturally gripping the handlebars", "child-sized relative to the table").
- Kling element overload also "melts hands": fewer elements, fewer hand failures.

**Head-to-head:** comparison sites (C) claim Kling v3 is the most reliable at "picking up an object, turning a page" rigid interactions. Wan 3.0 is repeatedly called "soft hands".

- **Fixes:** F3
- **Evidence:** gbeyrouti debug matrix (A-/B); OpenAI Cookbook "People, pose, and action" (A); comparisons (C).
- **Input change:** each shot records `hands_in_frame` (0/1/2) and `hand_action_complexity`. Complex hand actions route to Kling or to a real-plate insert (T15).
- **Cheapest test:** the same pick-up-and-turn hoodie beat on Kling 3.0 vs. Seedance 2.x.

### T22. Draft cheap, then finish
- **Seedance 2.5:** "Draft at 480p, finish at 720p." Seeds keep generations "in the same neighbourhood", not identical. Save the winning seed.
- **Nano Banana:** 0.5K or NB2 Lite for variants → pick → re-render the winner at 2K.
- **GPT Image:** start at `quality=low` for exploration.
- **Wan 3.0 motion pre-test** before an 18-cr Seedance final: B/C evidence says Wan 3.0 holds first-frame fidelity well but invents details. Use it for motion and staging checks, not product fidelity.
- **Fixes:** F9
- **Evidence:** smixs seedance-25.md §18 and nano-banana.md (B); OpenAI Cookbook (A).
- **Input change:** each job has a `draft|final` mode, and seed persistence per approved shot.
- **Cheapest test:** free (settings).

---

## Model × shot-type routing table

Scope note: Higgsfield exposes Seedance 2.x/2.5, Kling 3.x and Wan 3.0 (plus motion/replace routes). Veo 3.1 appears only where it's available to you. Sora is dead as of today.

| Shot type | 1st choice | Why (evidence) | Fallback / avoid |
|---|---|---|---|
| **Talking head to camera (lip-sync)** | **Kling 3.0 Turbo** for budget lip-sync. **Seedance 2.5** when the same shot needs product + room refs. | Kling Turbo: "noticeably better lip-sync on talking heads", audio included (smixs, B). Seedance 2.0/2.5: strongest lip-sync in Curious Refuge's Wan 3.0 test, and highest on a blind audio benchmark (B/C). Veo 3.1 is the consensus most reliable dialogue, but the 8s lock and 3-ref cap limit it (A/C). | **Avoid Wan 3.0** for speech: "biggest weakness" (Curious Refuge, B). Seedance 2.0 rejects real faces in refs, so the persona must be AI-generated. |
| **Hands + product (pick up, turn, show tag)** | **Kling 3.0** (I2V from keyframe, cfg 0.7–0.8, product element) | Comparisons (C) rate Kling v3 best on rigid hand-object interaction. Kling's element binding holds clothing texture through motion (Vidau, C). | Best: real-plate insert or Wan Animate replacement (T15). Avoid Wan 3.0 (soft hands, B). |
| **Garment try-on / fit (leggings, denim, fleece on body)** | **Seedance 2.x/2.5** with multi-angle garment refs + the T2 one-object clause. Costume change hidden in a hard cut. | invideo FAQ: Seedance "holds weave, drape, garment-environment interaction best" (C). Curious Refuge: Seedance physics feel stronger than Kling 3.0 (B). The 2.5 notes claim improved cloth simulation (B). | Kling 3.0 for slow, deliberate "fashion drift" moves (its motion prior is slow; C). For keyframes: GPT Image try-on prompt (A) → I2V. |
| **Unboxing / mailer rip (state change)** | **Seedance 2.5** with stage/end-state prompt + first & last frame (T4, T5), or 2 shots with the rip hidden in a cut | Official: the two-state binding is flakiest, so budget re-rolls or cut (A-). The HF in-house unboxing flow uses 4 slots with one-way box disappearance. | Real-plate insert for the actual tear (T15). Avoid long single takes >10s (drift). |
| **Walk / lifestyle (movement, full body)** | **Kling Motion Control** with a framing-matched real reference, or Seedance with `@Video` motion ref ("camera and pacing only") | Kling MC official rules (A-). Seedance video ref = motion/rhythm by default (A-). | Wan Animate if you have the real plate. Avoid close-up persona image + full-body motion ref (skeleton compression). |
| **B-roll product (flat-lay, macro fabric, hanging garment, no people)** | **Wan 3.0** (cheapest, strong first-frame fidelity) or **Kling I2V** with `Preserve logo/print` | Wan 3.0: "wins on faithfulness and stability incl. first-frame fidelity" (atlascloud via search, B). But check for invented logo details. Kling is strong on product rotations and fabric (C). | Seedance 2.0 is fine here: no faces, so no face filter (smixs, B). |
| **Any shot needing a fix (wrong print, extra prop, music)** | **Seedance 2.5 edit** (≤20s source), or Runway Aleph (5s chunk) | Official edit templates (A-). Aleph 5s/1-ref (A-). | Re-roll only after one edit attempt. |

---

## STOP DOING

1. **Filling every reference slot.** ByteDance says more refs degrade prioritisation. Kling loses image quality with Elements on. Stay in the 1–8 image comfort zone, per shot. (T3)
2. **Collage product sheets as refs, or several product views without "one single object".** This causes duplicated products. (T2)
3. **"no X" in Kling's negative field, and "no blur" / "don't show hands" on Seedance.** Kling wants nouns. Seedance summons banned visible objects. Negate sources, tracks and defects only. (T6)
4. **Tacking realism words onto the end of the prompt, and booster words** ("8K, hyperrealistic, masterpiece"). They're ignored or push the model toward the glossy look. (T10, T19)
5. **Re-describing the keyframe's contents in an I2V prompt.** It causes identity drift. (T13)
6. **Dialogue during mouth-occluding actions,** and long lines (>8s speech on Veo; >1–2 short lines per 4s on Sora-class models). (T7, T8)
7. **Asking the video model to render SANTO text, captions or prices.** Add them in post. (T20)
8. **Giving a short action a long clip** (a 3s action in 8s). This produces slow-mo. (T11)
9. **Re-rolling a whole 15s clip for one local defect** when a Seedance 2.5 edit or segment reshoot exists. (T16)
10. **Any new build on Sora 2.** Its API is removed 2026-09-24.
11. **Trusting "4K" on Seedance 2.5.** The live API is 480p/720p. Higher tiers are upscales, so don't pay extra for them.
12. **Pairing a close-up persona image with a full-body motion reference** in Kling Motion Control or VACE. (T15)

## Open questions

- **Higgsfield parameter exposure.** Does Higgsfield expose Seedance 2.5 `camera_fixed`, `return_last_frame`, `mov` output, seed, and edit/extend modes? Does it expose Kling `cfg_scale`, the negative field and `generate_audio=false`? Check with `models_explore` (free) before building T11/T14/T16 around them.
- **Higgsfield's Seedance 2.5 resolution.** HF notes say Seedance 2.5 on Higgsfield runs at "1080p". Is that native or an upscale (the ByteDance API is 720p)? It affects grain and texture decisions.
- **Real faces.** Does Higgsfield's Seedance 2.5 route accept a real human face reference (2.5 lists realistic humans as a headline feature), or only Soul-generated personas as on 2.0?
- **No clean head-to-heads.** There is no independent benchmark for our shot types (leggings fabric, mailer tear, logo on fleece). The comparison claims above are C-grade. A small internal bake-off would settle it: 3 shot types × 3 models × 2 seeds ≈ 18 generations, ~150–250 credits.
- **Veo 3.1 access.** Veo has the best dialogue, but only 3 asset refs and an 8s lock with refs. Is it reachable through Higgsfield, and at what credit cost?
- **Wan 3.0 rules.** It has an Alibaba "official formula" doc (Model Studio `wan3-video-generation-guide`), which I couldn't read (egress blocked). Two points to check there: the reference syntax, and whether `"Generate single shot."` (the Wan 2.7 rule) still suppresses the unrequested angle cuts reviewers complain about.

---

# PART 5 — `03-filmmakers.md`

## 03 — What working AI filmmakers and ad-makers do (source: pros' interviews, BTS, published pipelines)

Researched 2026-09-24. Environment: WebSearch summaries only (WebFetch was blocked for thedaringcreatives, fxguide, nofilmschool and curiousrefuge). I also read three GitHub repos where practitioners published their full production packages:
- `repos/OSideMedia_higgsfield-ai-prompt-skill/skills/higgsfield-seedance/HELL-GRIND.md` and `production-benchmarks.md`. These hold Higgsfield's open-sourced pipeline from its 90-to-95-minute feature "Hell Grind" (Cannes 2026) and the "Road to Cannes" numbers.
- `repos/minhawork123-afk_guide-best-ai-filmmaking/` (by "Fazi"). A finished **AI UGC product ad** (Tess / LODE protein, 9:16, Seedance 2.5) with every asset and prompt published.
- `repos/jnMetaCode_ai-shortfilm-prompts/faq.md` and `methodology.md`. A distillation of Mx-Shell's livestream and Q&A about the viral Seedance short "Zombie Scavenger".

Strength key (from BRIEF): **A** = official vendor docs or several independent pros; **B** = one credible practitioner with shown results; **C** = claim or anecdote.

---

## 0. Published numbers (the context every recommendation below sits in)

| Production | Generated → kept | Time / cost | Source |
|---|---|---|---|
| Kalshi NBA Finals ad (PJ Accetturo, Veo 3) | 300–400 gens → 15 clips (~20–27 per kept shot) | 2–3 days, ~$2,000 | https://www.thedaringcreatives.com/creator-stories/pj-ace-nba-finals-ad/ , https://www.marktechpost.com/2025/06/14/ai-generated-ad-created-with-googles-veo3-airs-during-nba-finals-slashing-production-costs-by-95/ |
| Qatar Airways, 2 spots (PJ Ace / Genre.ai) | characters composited into base frames with Nano Banana "over dozens of iterations", then animated in Veo 3.1 | 14 hours | https://pjace.beehiiv.com/p/qatar-airways |
| "Air Head" (shy kids, Sora) | "300:1" (generated vs. kept for touch-up); clips 10–20 s | Heavy post: roto, recolour, retime | https://www.techradar.com/computing/artificial-intelligence/turns-out-the-viral-air-head-sora-video-wasnt-purely-the-work-of-ai-we-were-led-to-believe , https://www.fxguide.com/fxfeatured/actually-using-sora/ |
| Washed Out "The Hardest Part" (Paul Trillo, Sora) | ~700 clips → 55–56 used (~10%) | ~6 weeks | https://nofilmschool.com/ai-music-video |
| Toys"R"Us (Native Foreign, Sora) | "hundreds" of shots → "a few dozen". Sora "got us 80–85% of the way", then about a dozen people did corrective VFX | a few weeks | https://digiday.com/marketing/why-toysrus-used-openais-sora-to-create-an-ai-generated-video/ |
| Coca-Cola 2024 (Secret Level / Silverside / Wild Card) | 10,000 frames, 5,000 video segments, 18,000 images by 17 artists | ~2 months | https://www.hollywoodreporter.com/business/digital/ai-coke-ad-holiday-studio-interview-1236420358/ |
| Coca-Cola 2025 (Silverside) | ~70,000 clips, ~100 staff. Used animals to avoid uncanny humans | ~1 month | https://futurism.com/artificial-intelligence/coke-ai-holiday-ad |
| Hell Grind 90-min feature (Higgsfield team) | 108,859 gens. **Acceptance ~1.0% image / ~1.5% video**. Lead character took ~800 iterations to lock (600 Soul Cinema + 200 GPT Image 2). One 10-s establishing shot took 72 gens | 14 days, 15 people, ~$400k generation, ~$500k total | repos/OSideMedia_higgsfield-ai-prompt-skill/production-benchmarks.md |
| Community Seedance shorts (13 projects) | ~65–100 gens per kept shot. **61% of all gens were TESTS** | — | same file, "Community-corpus anchors" |
| "Zombie Scavenger" (Mx-Shell, Seedance 2.0) | ~400 images + 200+ video gens → ~40 clips (~5:1). Rerolls per shot ranged from 2–3 to 20+ | 10 days, ~20,000 RMB | repos/jnMetaCode_ai-shortfilm-prompts/faq.md |
| Karen X Cheng (hybrid real + AI) | "50–100 tests and combinations per clip" | — | https://x.com/karenxcheng/status/1564626773001719813 |
| Hashem Al-Ghaili short | — | 1 person, $600, 2 weeks | https://getsuperintel.com/p/interview-with-hashem-al-ghaili-96cc3bcab199c3c1 |

**Takeaway for "first time right":** No pro gets shots first time. Keep rates run from ~5:1 on simple shots with locked keyframes (Mx-Shell) up to 100:1+ on complex cinema. What separates cheap productions from expensive ones is **where the iteration happens**. The cheap ones iterate on stills (PJ: "dozens of iterations" in Nano Banana, then "simple prompts" in Veo) and on shot design (split, simplify, cut away). They do not iterate by rerolling video. Cutroom's lever is to move rerolls to the ~1.5-credit image stage and to design shots that only need 2–4 good seconds each.

---

## 1. Techniques

### T1. Assets first: lock person, product and room as text + image before any video
- **What / how:** An "asset" is a pair: a **reference image plus a verbatim text descriptor**, and that descriptor is pasted **word for word, never shortened** into every prompt. Hell Grind's rule 1: "Do not generate a single shot until every character, location, and prop is locked and stress-tested. This one rule saves more money than everything else combined." PJ Ace makes the same point for text-only work: each prompt must "fully describe the scene as if Veo 3 has no context of the shot before or after it — re-describe the setting, the character, and the tone every time."
- **Fixes:** F1, F2, F7, F9
- **Evidence:** A. Sources: Hell Grind brief (repos/OSideMedia…/HELL-GRIND.md); PJ Ace (https://x.com/PJaccetturo/status/1932893267668185525); the Fazi UGC guide (repos/minhawork123…/GUIDE.md: "Style DNA is written once and reused byte-identical at the end of every block").
- **Input change for Cutroom:** Each Person, SKU and Room record stores a **canonical descriptor string** (frozen, versioned) next to its images. The prompt builder always injects it verbatim and never lets an LLM paraphrase it. Add a "stress-tested" flag: an asset can't be used in a paid video until it has passed one cheap test render.
- **Cheapest test:** Re-run one existing failed shot with the frozen descriptor injected verbatim, changing nothing else. About 18 credits (1 Seedance).

### T2. The character sheet has three panels and one of them is headless
- **What / how:** Panel 1 is a face close-up (large, **3/4 view**, not straight-on). Panel 2 is the full body from the front **with no head**. Panel 3 is the full body from the back. Why: "On wide shots the model kept sourcing the face from the small full-body figure on the sheet… Remove that head and the model has exactly one place to take the face from." Fazi's version: "If two full faces appear, Seedance averages them into a blurred identity. One face, used twice, locks the model onto a single identity." Keep the sheet **deliberately boring**: neutral grey background, flat light, real skin with visible pores, no retouching. "Bake film grain and a cinematic lens into the sheet and the character carries that look into every scene and stops reacting to new light." In the prompt, say which panel to take the face from ("take the face from the LEFT chest-up portrait panel. The centre panel omits the head deliberately. Tess has a head and face in every shot").
- **Fixes:** F1, F6
- **Evidence:** A−. Hell Grind (official Higgsfield feature) plus Fazi's shipped UGC ad, whose published assets include the headless centre panel (repos/minhawork123…/examples/tess-lode-ugc/).
- **Input change for Cutroom:** The Person asset becomes a generated **3-panel sheet** (face 3/4 / headless front body / back) on neutral grey. Cutroom sends that sheet, not the single model photo or a collage. Per-panel role text is auto-added to every prompt.
- **Cheapest test:** Build the sheet with 2–3 Nano Banana edits from the existing model photo (~3–5 credits). Then run one Seedance wide/medium shot where face drift happens today (~18 credits) and compare against the current reference.

### T3. Never run a whole image through a model twice. Make point edits and mask them back onto the original
- **What / how:** Clothes, blood and scars are "point changes". Make the change in Nano Banana Pro or Seedream, then **bring only the changed region back onto the original with a mask** in any editor. "An image never runs through a model twice in full. Every extra pass destroys texture and drifts color. After two passes the face turns symmetrical, plastic, and lifeless — and that dead texture later damages the character's acting in video."
- **Fixes:** F1, F2, F6
- **Evidence:** B. Hell Grind brief (official, from a production that shipped). No second independent source, but it matches the widely reported NB "plastic after re-edit" behaviour.
- **Input change for Cutroom:** Keep the **untouched master** of every keyframe. When a Nano Banana edit changes, say, the hoodie print, Cutroom computes a diff/mask (or asks the user to brush one) and composites **only that region** onto the master with PIL/OpenCV before sending the frame to video. Never chain NB edit → NB edit → video.
- **Cheapest test:** Take one keyframe that has had 2+ NB passes. Rebuild it as master + one masked edit and animate both versions. ~1.5 + 2×18 credits.

### T4. Photograph the real garment ON a real body, in the real space, before generating
- **What / how:** For the Guess / Vogue AI model, Seraphinne Vallora "employed a real model, who, over the course of a week, was photographed in the studio wearing Guess clothing. That informed how the clothes looked on an AI model." Hundreds of iterations followed to perfect "the texture, movement and details of the advertised product". H&M's digital twins were built from many photos "in motion, from different angles and in different lighting". Every output then passes **human QC for garment accuracy and colour fidelity**. PJ Ace's Qatar spots began with "reference photography of the real cabin", with shots laid out in Figma before any generation.
- **Fixes:** F2, F5, F7
- **Evidence:** B. Sources: https://www.cnn.com/2025/07/31/style/vogue-ai-models-guess-campaign ; https://fashionunited.uk/news/fashion/h-m-turns-to-ai-digital-twins-in-new-campaign-as-fashion-grapples-with-blurred-realities/2025070482637 ; https://pjace.beehiiv.com/p/qatar-airways
- **Input change for Cutroom:** The "product state photo kit" already exists. The new part is **on-body shots**. For each SKU, store 6–10 phone photos of the garment **worn by any real person**: front, back, 3/4, sitting (leggings/denim creasing at the knee and hip), arms raised (hoodie hem lift), a macro of the logo/print/tag/stitching, and one frame in the target room light. Use these as the garment reference instead of flat-lays. The fabric physics then come from a real body. The AI only swaps the identity to the model and recomposes the shot.
- **Cheapest test:** Free to shoot (10 minutes with a phone). Then one NB compose, "model from sheet wearing exactly this garment, pose from photo" (~1.5 credits), and one video (~18).

### T5. Iterate on keyframes, not on video; keep the video prompt simple
- **What / how:** PJ Ace's Qatar workflow: shots laid out in Figma → characters **composited into base frames with Nano Banana over dozens of iterations** → animated in Veo 3.1 **with simple prompts**. Hell Grind and the Seedance community keep a **FINAL KEYFRAMES** folder, "the locked frames each shot was built from". Fazi's order: portrait (fix the face) → 3-panel sheet → skin-realism pass → location plate → only then video. Mx-Shell's exception: for *dynamic* motion he does **not** lock start/end frames ("let the AI generate freely"). He saves keyframe locking for character and scene continuity.
- **Fixes:** F1, F2, F7, F9
- **Evidence:** A−. PJ (https://pjace.beehiiv.com/p/qatar-airways); Higgsfield community corpus (production-benchmarks.md); Fazi GUIDE.md; Mx-Shell methodology.md.
- **Input change for Cutroom:** Make the **approved keyframe** a required, human-approved gate for each shot. It should be a composited still containing the person, the garment (from T4) and the room, not a set of loose references. The video prompt then shrinks to **action + camera + audio**, because appearance is already in the frame. Leave the end frame empty for fast, loose motion. Use first+last only where continuity with the next shot matters.
- **Cheapest test:** Take one shot and spend up to 8 NB iterations on the keyframe (~12 credits) before a single Seedance render. Compare its keep rate against the current flow over 3 shots.

### T6. Frozen reference-slot order, and name each reference's job
- **What / how:** Fazi: "Upload order is fixed. Never change it across generations. The prompt binds to slots, not to filenames." (@Image1 = person sheet, @Image2 = product, @Image3–5 = location plates, @Image4 = **last frame of the previous block** from block 2 onward.) Hell Grind: state each reference's role, and **ban inheritance** on location references: "take only the space and the texture… Do not use as a starting frame, do not inherit the composition, the angle, or the grade." Otherwise the model "copies the composition instead of the face, or the face instead of the color palette".
- **Fixes:** F1, F2, F7
- **Evidence:** A−. Hell Grind plus Fazi's shipped ad.
- **Input change for Cutroom:** A fixed slot schema per template (1 person sheet, 2 product/garment, 3 room plate, 4 previous-shot last frame). Each slot gets an auto-generated role line, and room plates always carry the no-inheritance clause.
- **Cheapest test:** 0 extra credits. Apply it to the next generation you were going to run anyway.

### T7. Room: a floor plan written in text, an anchor object, 3/4 plates, one light source, and a real phone photo of the room
- **What / how:** Hell Grind's **GEO SPATIAL LAYOUT** block is written once per scene and pasted unchanged into every shot. It lists landmarks, frame-left/frame-right **from the camera**, distances in metres, and which side of the 180° line the camera stays on. It contains no people and no action. Also: "Leave an anchor in every location — 'The character at the lamp, facing the door' works. 'The character in the room' is a lottery." Shoot location plates **in 3/4, not frontal**: a frontal plate "becomes flat wallpaper… past its edges the model invents new surroundings". Keep **one light logic** ("never two suns"). Give a static dialogue "a corner of the room, not the whole room". For reverse angles, render a short **empty-room walkthrough video** and screenshot the angles you need. Fazi's UGC kitchen plate was literally prompted as a "*Real phone photo of an empty small rented apartment*", with a named light conflict ("cold blue window light disagreeing with warm tungsten under-cabinet light").
- **Fixes:** F7, F6
- **Evidence:** A−. Hell Grind plus Fazi.
- **Input change for Cutroom:** A Room asset = 2–3 **real phone photos taken at 3/4** + a stored GEO text block (anchor objects, window side, lamp) + a named light source. Every shot template must say where the person stands relative to an anchor ("at the bed edge, window frame-right").
- **Cheapest test:** Free to write the GEO block. Then re-run one room-warp failure with the GEO block and the 3/4 plate (~18 credits).

### T8. Hands: state the headcount and where the hands enter, keep them busy, and cap hand action
- **What / how:** A Higgsfield Studio breakdown recorded a solo close-up (one person picking a lock) that **grew a third hand**. The fix goes in every close-up on hands: `There are only two hands in the frame, both belonging to the same person, entering from the same sleeve.` It states the count, the owner **and the entry point** ("count alone still lets a correctly-numbered pair arrive from two directions"). In groups, cap hand action at two characters; the rest watch. Hell Grind's acting rule is "**Keep the hands busy**": characters fix, count, pour and talk over it, and "the strongest accent of a scene is the moment they stop that work". Fazi's UGC ad never has hands and dialogue at the same time (see T11), and product-handling shots are **"No face in frame — hands and torso only."**
- **Fixes:** F3
- **Evidence:** B. Sources: repos/OSideMedia…/FAILURE-MODES.md § Orphan limbs ([FIELD — Higgsfield Studio, RED FLAG breakdown, 2026-08-19]); Hell Grind; Fazi prompts-seedance.md.
- **Input change for Cutroom:** Auto-append the two-hands line to any shot tagged "hands/product". Add a "phone" rule: if the phone is the camera (selfie), the prompt must say "one hand holds the phone (off-frame); only the other hand is visible". For two-handed product actions, the shot type must be **propped phone** (Fazi: "Phone propped low on the kitchen counter, static but noticeably crooked"), never a selfie. This removes the "phone in hand while both hands busy" failure at the design stage.
- **Cheapest test:** Re-run your worst hands shot with the headcount line and the propped-phone framing (~18 credits).

### T9. State changes (ripping the mailer, pulling on the hoodie, zipping): start mid-action, or use two states and a sound
- **What / how:** There are three pro patterns.
  1. **Start the prompt with the action already underway** (Hell Grind, "solutions born under deadline"): a door wouldn't break until "the action opens the prompt — 'he is ALREADY mid-swing, the door ALREADY cracking'". The approach becomes a separate shot. Complex action "never sits in the middle of the timing".
  2. **Two states + sound**: "sealed pack, a tear heard off screen, hands already inside it; it is cheaper and it cannot fail." Also: "never invent a structure the reference cannot show: if the notch, the seal or the catch is not visible in the material you hold, open it off screen, cut around it, or shoot it for real."
  3. If the manipulation *is* the point of the shot, write the **causal chain**: initial structure → anchor (the other hand grips the bag body) → force (thumb and forefinger at the tear strip, pulling across) → material feedback (the poly film stretches then parts along the perforation) → finished state (a continuous opening, garment visible). "Do not stack a legible brand face, a two-handed manipulation and a strong effect in one shot — the manipulation shot proves the mechanism, a separate shot proves the label."

  Fazi's shipped UGC ad does include a hoodie-off, but only at the **end** of a block, followed by "She speaks only after the hoodie is off and she has stopped moving", and it **ENDs ON THAT FRAME**. The next block restates the post-change state as a **CONTINUITY — CRITICAL** paragraph ("the cream hoodie is already off and must not appear").
- **Fixes:** F4, F3, F2
- **Evidence:** B for 1 and the Fazi pattern (from shipped productions). C for the causal-chain wording (the repo marks it "[HOUSE… UNPROVEN HERE]").
- **Input change for Cutroom:** Make state changes a **shot-type enum**: `already-mid` / `before→sound→after` / `causal-chain`. Default to `before→sound→after` for the mailer. The mailer's product photo kit must show the **tear strip/adhesive flap close-up** (the "structure the reference can show"). After any state change, the next shot automatically gets a CONTINUITY paragraph describing the new state and banning the old one.
- **Cheapest test:** The mailer as two stills (sealed in hand / hands already pulling the hoodie out of the open bag) plus a real tear SFX. 2 NB (~3 credits) + 2 short Wan drafts (~7) versus one Seedance full tear (~18).

### T10. Describe physical movement instead of emotion words; keep faces alive
- **What / how:** Hell Grind: emotion words ("sad", "angry") give "something shallow". Describe **muscle work** ("jaw sets and releases twice", "a light exhale through the nose"). Other rules: **phased blinking** ("one lazy blink → a quick DOUBLE-BLINK → one HARD reset-blink"); the **micro-life rule** of "one visible micro-event every one or two seconds" (breath lifts the chest, a brow tenses); "Describe stillness as held tension, never as a freeze"; and "The reaction starts before the other line ends". Write actions in positive form: "The model ignores 'does NOT fall on his back'… Write 'falls on his stomach.'" Fazi's system prompt: "Physical actions only, never interior states"; "Involuntary motion needs a mechanism"; when a mistake is likely, "name the wrong version inline".
- **Fixes:** F6, F1
- **Evidence:** A−. Hell Grind plus Fazi.
- **Input change for Cutroom:** The LLM prompt-writer's system prompt should forbid emotion adjectives and require a micro-event every 1–2 s in any face shot longer than 2 s.
- **Cheapest test:** Free (prompt only). Validate on the next talking-head render.

### T11. Never overlap dialogue and physical action; put voiceover over hands-only inserts
- **What / how:** Fazi's shipped UGC prompt: "PACING: dialogue and physical action never overlap. She speaks, or she moves — never both. Leave real silence between lines." Product handling runs as "Voiceover, no lip sync, landing mid-action" over hands/torso-only shots. Then "a second and a half of only scoop-and-plastic sound with no voice". Hell Grind keeps lines only in the AUDIO block and adds: "everyone speaks **only** the line in quotes; whoever has no line stays completely silent". Short lines leave "audio air the model fills with invented mumble" (measured at ≤6 words on a 4-s shot).
- **Fixes:** F3, F8, F1
- **Evidence:** B+. Fazi's finished ad plus Hell Grind.
- **Input change for Cutroom:** The script format forces each beat to be `SPEAK` (face, near-static) or `DO` (hands/body, VO or silence), never both. The storyboard gate rejects a beat that has both. Lines under 6 words on a 4-s+ shot get a warning (pad the line or shorten the shot).
- **Cheapest test:** Free. Restructure the next script.

### T12. The phone look is its own spec, not "film look". Drop grain and halation
- **What / how:** Fazi's UGC LOOK block is the most specific published phone spec I found: "shot on a recent smartphone. HDR, mild digital over-sharpening on edges, visible luminance noise in the dim apartment, slight rolling shutter on pans, clipped highlights near windows. **Flat and ungraded**." CAMERA: "held at arm's length… real hand tremor, small organic drifts, slightly crooked horizons. **Autofocus hunts once and resettles in the first two seconds.** Never a tripod, never a gimbal, never slow motion." NEGATIVE: "**No film grain, no halation, no cinematic or teal-and-orange grade.**" Ending: "She reaches toward the lens to stop the recording and the clip CUTS HARD mid-movement, before her hand arrives. No outro." (Cinema pipelines add grain as dither after upscaling. That is the opposite register and wrong for UGC.) Mx-Shell ships at **720p** ("platforms recompress anyway; save the compute for more rerolls"). A vendor claim that "68% of top-performing UGC is 1080p or lower" is C.
- **Fixes:** F6
- **Evidence:** B. Fazi's shipped ad plus Mx-Shell for resolution.
- **Input change for Cutroom:** Replace any "film grain / cinematic" style preset for UGC with a **phone-capture DNA block**, byte-identical in every shot (the phone profile idea already exists; this is the tested wording). Also: generate at 720p/1080p (never pay for 4K on UGC), and in post add phone artefacts (sharpening, luma noise) rather than film grain.
- **Cheapest test:** Swap in the LOOK/CAMERA/NEGATIVE block on one shot you already have a render of (~18 credits).

### T13. Kill slow motion: ban it by name, ask for real-time speed, retime in post
- **What / how:** shy kids on "Air Head": most Sora clips "looked like they were shot in slow motion" although nobody asked for it. "There was quite a bit of adjusting timing to keep it all from feeling like a big slowmo project" (retimed in post). The Higgsfield failure log says: "Ban slow motion by name, and say real-time speed… the model's default is already the failure." Fazi writes "never slow motion" in both CAMERA and NEGATIVE.
- **Fixes:** F6
- **Evidence:** A. Several independent productions.
- **Input change for Cutroom:** Every prompt carries "real-time speed, never slow motion". Add a post step that speeds each clip up by a per-clip factor (a stored field, default 1.0) and offer the user 1.1× / 1.2× previews. No pro published a standard factor; see Open questions.
- **Cheapest test:** 0 credits. Retime existing renders in ffmpeg (`setpts=PTS/1.15`) and A/B them by eye.

### T14. Generate long, keep the best seconds, splice takes
- **What / how:** In the Seedance community corpus, 15-s multi-shot generations dominated: "generate long multi-shot clips, cut the best seconds". "Takes are spliced — one generation's opening cut with another's ending into a single shot." Fazi: "Trim the top and tail of each block (**first and last 10–15 frames** often have motion artifacts)". Cut on action, at the peak of a movement. A vendor-documented episode (C): 164 clips → 41 used, **~5 s kept of each 15-s clip**.
- **Fixes:** F9, F1, F6
- **Evidence:** A−. Higgsfield corpus, Fazi, and Mx-Shell ("Trim a piece here… splice. Saves money on rerolls").
- **Input change for Cutroom:** Treat one ~15-s Seedance render as **raw coverage for 3–5 shots** of the 15-s ad, not as the ad. Store in/out points per keeper, auto-drop the first and last ~12 frames, and let the editor take shot 2 from render A and shot 3 from render B. Scoring becomes per usable second, not per render.
- **Cheapest test:** 0 credits. Re-cut the last 5 rejected renders for usable 2–4 s segments.

### T15. Shot length: 2–4 s per shot; Seedance fails below 2 s
- **What / how:** Fazi's Seedance rules: "3–4 seconds for most beats, 5–6 for travel or reveals, 2 seconds for a fast cut. **Under 2 rarely renders**." Shot durations must add up exactly to the block length. Mx-Shell: general shot 5–10 s, a blink or glance 4–5 s, openings 15 s. Editors' rule of thumb: 2–5 s baseline and "cut before AI artifacts become conscious distractions", because "a 2-second cut is more forgiving than a 6-second hold" (C, https://medium.com/@info_13818/optimal-shot-length-for-ai-generated-motion-based-on-viewer-retention-a7d86e8c8969).
- **Fixes:** F1, F3, F6
- **Evidence:** B.
- **Input change for Cutroom:** A 15-s ad = 4–6 shots of 2–4 s. Timestamps inside a Seedance multi-shot prompt must sum to the block length, and no segment may be under 2 s.
- **Cheapest test:** Free (template change).

### T16. When continuity is expensive, cut into the body; carry motion direction across cuts
- **What / how:** "When full-body continuity is too expensive, cut into the body. Quick inserts of hands, waist and feet hide transitions… a close-up of feet is far harder to break than a wide shot of two bodies." Mx-Shell joins clips "by motion direction continuity: …he gets pushed out of frame one side. Next shot, he enters from the same side." Pros keep faces out of shots that don't need them. Mx-Shell: "Not every story needs a face". Coca-Cola 2025 moved to animals; El Eternauta's AI building collapse was "kept fairly dark, which helps to obscure any potential shortcomings" (https://www.primetimer.com/features/netflix-generative-ai-eternaut-scene).
- **Fixes:** F1, F4, F5
- **Evidence:** A−.
- **Input change for Cutroom:** A shot library of **insert types** (hands on zip, waistband snap, hem tug, sleeve cuff, feet stepping into jeans) used as bridges across state changes. The face appears only in SPEAK beats.
- **Cheapest test:** Wan drafts of 3 inserts (~10 credits).

### T17. Put the camera move and the performance on a phone, framed to match the keyframe
- **What / how:** Asteria projects "begin with original, artist-created sources such as illustration, animation, or live-action plates" (https://www.topazlabs.com/news/asteria-is-building-the-future-of-filmmaking-with-hybrid-ai-workflows-and-topaz-video). Staircase Studios builds its ForwardMotion pipeline on "voices and expressions from performers" (https://variety.com/2025/film/news/staircase-studios-ai-pouya-shahbazian-1236326853/). Jon Finger shoots object-blocking with toys and phones and restyles it. The practical tip (C, vendor write-up of a creator): one person spent "50+ generations… trying to prompt a single complex camera move — and a single phone-recorded reference clip delivered it in one pass". Also "**Match your phone frame to the first frame you've generated**; the closer it lines up, the better the output" (https://www.vp-land.com/p/step-by-step-the-state-of-ai-filmmaking-workflows).
- **Fixes:** F3, F4, F6, F9
- **Evidence:** B for the hybrid principle (Asteria, Staircase, shy kids); C for the "one pass" number.
- **Input change for Cutroom:** The movement library exists already. The new requirement is that each motion reference is **re-shot or cropped to the same framing and aspect as the approved keyframe** (same distance, same side), and that motion clips are tagged by framing (selfie arm's-length / propped-low / over-shoulder).
- **Cheapest test:** Record one 4-s phone clip matching an existing keyframe, then run one motion-control/reference render (~18 credits).

### T18. Iteration discipline: change one line, log it, and simplify the shot after 10–15 tries
- **What / how:** Hell Grind: "Every iteration is surgical: one line changes, everything else stays word for word… Everything goes into the log: prompt version, what changed, verdict." "**If a shot has not come together in 10–15 iterations, the problem is not the wording.** Simplify the shot: split it in two, remove an action, change the angle." Folder discipline from the community: TESTS / FINAL KEYFRAMES / FINAL GENERATIONS / **FAILED GENERATIONS kept on purpose**. Promise's MUSE platform "records each version of prompts, settings and approvals" (https://www.forbes.com/sites/maureenkerr/2026/07/24/dave-clarks-ai-studio-promise-aims-for-films-hollywood-can-release/). PJ: ask the LLM for "**5 prompts at a time — any more than that and the quality starts to slip**".
- **Fixes:** F9
- **Evidence:** A. Hell Grind, Promise, PJ, community corpus.
- **Input change for Cutroom:** A generation ledger (prompt diff vs. the previous attempt, reference slot hashes, model, seed, verdict + reason). A hard **stop at N rerolls per shot** (suggested 5 for UGC), after which the UI forces "split / remove action / change angle". The prompt-writing LLM is batched at 5 shots or fewer per call.
- **Cheapest test:** Free (software).

### T19. Assemble the whole thing rough first, then spend on the moments that carry it
- **What / how:** Hell Grind schedule: "Week 1 = full feature assembly — every scene present, even if rough. Week 2 = key-moment refinement… accept rougher takes elsewhere." Mx-Shell: "shot two test scenes, saw the texture was OK, then started." In the community corpus, 61% of gens were TESTS: "budget for the tests as the work, not as overhead."
- **Fixes:** F9
- **Evidence:** A−.
- **Input change for Cutroom:** A two-pass render plan per ad. Pass 1: every shot as keyframe + cheap Wan draft (≈3.5 credits each) → a rough 15-s cut reviewed as a whole. Pass 2: Seedance only on the 1–2 hero shots (hook + product moment). Weak inserts stay on the cheap model.
- **Cheapest test:** One ad in Pass 1 only: ~5 shots × (1.5 + 3.5) ≈ 25 credits.

### T20. Fix colour and texture at the image stage; grade lightly (AI video has little colour depth)
- **What / how:** Mx-Shell: "AI-generated video has **low color bitrate**… Push it too far and you get color banding and noise… lock your color tone at the image-generation stage… do only minor transitions in post." For cinema delivery, USC ETC used a Topaz chain (Nyx to deband/denoise → Gaia to upscale → Hyperion for SDR→HDR, 8-bit→16-bit) with grain as dither (https://www.vp-land.com/p/the-topaz-ai-workflow-that-turns-8-bit-ai-into-16-bit-cinema-quality). Asteria uses Topaz as the layer that "glues everything together". That is overkill for 9:16 UGC; the useful part is "don't grade hard".
- **Fixes:** F6
- **Evidence:** B.
- **Input change for Cutroom:** The grey-card colour check happens on the **keyframe** (before video), not in post. The post grade is limited to small exposure/WB trims.
- **Cheapest test:** Free.

### T21. Unfiltered, high-detail references, plus a skin-realism pass on the sheet
- **What / how:** Mx-Shell: why does it look like cheap CG? "**Over-beautified reference photos**… Use clear large headshots, not over-filtered ones… Too perfect = fake." Also "Describing flaws = describing reality": "preserve minor facial blemishes". Low-detail references transfer their *style* (CG, anime) rather than their design. Fazi's skin-realism pass on the approved sheet: "Take this exact image and increase skin and overall realism only. Keep the same identity, pose, outfit, panel layout, background, and lighting exactly as shown… real visible pores across the forehead, cheeks and nose, subtle natural uneven tone… NEGATIVE: no smooth, plastic, waxy… No beauty filter." Note the tension with T3: do this pass **once**, on the sheet, and mask it back if identity moves.
- **Fixes:** F6, F1
- **Evidence:** B.
- **Input change for Cutroom:** Reject person references that show beauty-filter signs (low high-frequency energy on skin), and run the realism pass once per sheet.
- **Cheapest test:** ~1.5 credits (one NB pass).

### T22. Count the props, and never let the model add or clone objects
- **What / how:** Hell Grind's SCENE CONTEXT opens with a count header ("EXACT 3 CHARACTERS — NO DUPLICATES") and "repeated set dressing gets a direct ban with a count: 'Exactly ONE mannequin, NEVER render a second one… Two trays, never more.'" Counted objects go in POSITIVE LOCKS, "phrased as what is in the frame". Fazi's NEGATIVE lists "No other people".
- **Fixes:** F7 (random jewellery/props), F1
- **Evidence:** B.
- **Input change for Cutroom:** The Person asset stores an explicit **accessory inventory** ("no jewellery; one black hair tie on LEFT wrist"), injected as a positive lock. The room GEO block lists counted props.
- **Cheapest test:** Free (prompt).

### T23. Pick the model per shot type, not per project
- **What / how:** Dor Brothers: the skill "is knowing… 'if I want natural movement, this one is better; if I want cinematic looks, this one is better; if I want frame-to-frame features, this is the only one available'" (https://www.digitalcameraworld.com/features/anyone-whos-complaining-about-ai-now-will-use-it-later-yonatan-from-the-dor-brothers). The Higgsfield corpus runs Seedance 2.0 for all video, Soul Cinematic for volume stills, GPT Image 2 for sheet edits, and Nano Banana Flash for exposure-matching plate edits. Mx-Shell: "Use Seedance 2.0, not Seedance 2.0 Fast. Fast… skimps on detail." Fashion practitioners (C) keep **tight garment close-ups on Kling** for label accuracy and use Seedance for fabric/drape and body-environment interaction (https://www.aifire.co/p/nano-banana-2-kling-3-0-cinematic-ai-ad-workflow-2026 , https://invideo.io/faq/what-is-the-best-ai-video-model-for-fashion-product/).
- **Fixes:** F9, F2, F5
- **Evidence:** B/C.
- **Input change for Cutroom:** A routing table by shot type (talking hook → Seedance; garment macro/logo → Kling; filler insert → Wan) that gets updated from the ledger in T18.
- **Cheapest test:** Same keyframe, garment macro on Kling vs. Seedance: 2 renders.

### T24. Audio: SFX and room tone only, voice specified as a person, music (if any) in post
- **What / how:** Hell Grind prompts end "SFX only. No music." (house note: "prefer **`NO BGM`**… reads as a hard spec"): "music belongs to post-production, and a generated soundtrack only gets in the way of the edit." Write the mix itself: "voices clean and close to the microphone, ambience under them, ambience dips when someone speaks." Fazi's UGC: "**No music. UGC authenticity lives in silence and room tone. Music signals 'ad.'**" The audio line reads: "real room tone… the scoop against plastic, the shaker lid, the bag zip… **Audio slightly hot and a little clipped, like a phone mic in a reverberant room.**" The voice line reads: "natural, warm, human female voice. Casual conversational cadence, real pitch variation, small natural imperfections, **one slightly swallowed word**. Low energy, faintly tired, underselling… NOT an ad read." Also lock the voice as a text descriptor (register, tempo, accent, manner), pasted as-is every time, and "open every new generation with the line that closed the previous one" so emotion carries across the seam. Room tone also needs to fill the gaps: TTS "absolute silence between words" is a giveaway (C).
- **Fixes:** F8
- **Evidence:** B+. Hell Grind plus Fazi's shipped ad.
- **Input change for Cutroom:** A per-person **voice descriptor** stored with the asset; a UGC audio block template (hot/clipped phone mic, named foley for the product: mailer crinkle, zip, fleece rustle); default "NO BGM"; a real room-tone bed under everything in post.
- **Cheapest test:** Prompt-only change on the next render.

---

## 2. Pro pipeline, step by step (synthesis across PJ Ace/Genre, Hell Grind, the Seedance community, Fazi's UGC ad, Mx-Shell, shy kids, Native Foreign, Asteria, Coca-Cola)

1. **Brief → script in camera language.** Write physical actions only. Every beat is SPEAK or DO, never both. An LLM drafts, a human picks (PJ, Dor Brothers, Fazi).
2. **Script → shot list with durations.** Shots are 2–4 s (≥2 s for Seedance) and add up exactly to each block. Say which side of the frame things happen on and where the camera is. Batch the LLM at ≤5 prompts per call (PJ).
3. **Real capture first.** Photograph the location (3/4 angles), the product (including the structures that change state: tear strip, zip pull, tag), the garment **on a real body**, and any hard motion or camera move on a phone framed like the shot (PJ Qatar, Guess/Seraphinne Vallora, H&M, Asteria, shy kids).
4. **Build assets (text + image) and stress-test them.** Headless 3-panel person sheet (boring, neutral, pores); product sheet; 3/4 location plates with an anchor and one light source; a GEO block per room; a voice descriptor; an accessory/prop count. Don't shoot anything until the assets pass (Hell Grind rule 1). Expect a lot of iteration here; Hell Grind's lead took ~800 image iterations. This is the cheap place to iterate.
5. **Keyframes per shot.** Composite person + garment + room in the image model over "dozens" of cheap iterations. Point edits are masked back onto the master, never re-run in full. Check colour and exposure here (grey card), because there is no grading room later (PJ, Hell Grind, Mx-Shell).
6. **Animatic / rough assembly.** Cut the whole piece from keyframes or cheap drafts before spending on hero renders (Hell Grind Week 1, Mx-Shell's test scenes, Coca-Cola and Toys"R"Us storyboarding).
7. **Video generation.** Frozen slot order. Name each reference's role. The descriptor is verbatim. Style/phone DNA is byte-identical. Positive-form actions, physical-movement acting, and a two-hands line on hand shots. State changes go "already mid-action" or before→sound→after. Ban slow motion. SFX/no BGM. Generate ~15-s multi-shot coverage, and from block 2 on, feed the last frame of the previous block.
8. **Select.** Keep the best **seconds**, not whole takes. Trim 10–15 frames from each head and tail. Splice takes. Change one line per retry and log it. After 10–15 failed tries (pros) or ~5 (sensible for UGC), simplify the shot rather than the words.
9. **Fix in post.** Recolour or composite the real product/logo where it drifted (Air Head recoloured the balloon; Native Foreign's "corrective VFX" took the last 15–20%). Retime slow-mo clips. Hide problems with inserts, cut-on-action and motion-direction continuity.
10. **Finish for the platform.** UGC: flat, phone artefacts, 720p–1080p, no grain, room tone, hot phone-mic voice, hard-cut ending. Cinema: Topaz deband/upscale, grain as dither, light grade.
11. **Sound last but deliberately.** Keep native SFX. Lay real room tone under everything. Add music only in post and only if the format wants it (never for UGC, per Fazi).

---

## 3. STOP DOING (things pros say hurt quality)

- **Running one image through the model repeatedly** (NB edit on NB edit). It makes faces symmetrical and plastic and damages the video performance later (Hell Grind).
- **Sheets with two visible faces**, a small face on the full-body figure, or a cinematic grade/grain baked into the sheet (Hell Grind, Fazi).
- **Beauty-filtered or low-detail reference photos**. The model copies the style instead of the design (Mx-Shell).
- **Frontal "pretty" location plates** and "the character in the room" with no anchor object (Hell Grind).
- **Rewriting the whole prompt between retries.** You lose the parts that worked (Hell Grind).
- **Asking an LLM for more than 5 shot prompts at once** (PJ Ace).
- **Emotion adjectives** ("excited", "happy with the hoodie") and negative-form actions ("does NOT drop it") (Hell Grind).
- **Dialogue and hand action in the same shot**; short lines on long shots, which the model fills with mumble (Fazi, Hell Grind).
- **Complex state changes in the middle of a shot's timing** (Hell Grind), or a brand face + two-handed manipulation + effect in one shot.
- **Stacked camera moves** (handheld + push + rack) (Higgsfield failure log).
- **Seedance shots under 2 s** (Fazi).
- **Generated music in the clip** (Hell Grind: SFX only / NO BGM; Fazi: "music signals 'ad'").
- **Film grain, halation or teal-orange on UGC.** That is the cinema register, not phone (Fazi).
- **Heavy grading of AI footage.** Low colour depth → banding (Mx-Shell, USC ETC).
- **Writing ages** in prompts. It triggers stricter filtering; give role, clothes and action instead (Hell Grind).
- **Keyframe-locking fast, loose motion.** Lock only for continuity (Mx-Shell).
- **Using the "Fast" model variant for finals** (Mx-Shell on Seedance 2.0 Fast).
- **Expecting first-try perfection.** Every pro plans for rerolls. The fix is making rerolls cheap (images, drafts) and shots simpler, not hoping.

---

## 4. Open questions (not answered by any pro source I could reach)

1. **Retime factor for floaty motion.** Air Head retimed clips but gave no number. Is 1.1–1.25× right for Seedance/Kling UGC? Test with ffmpeg on existing renders (free).
2. **Does the headless-sheet trick carry over from Seedance to Kling 3.x and Wan 3.0,** and how does it compare with Soul ID? Hell Grind used Soul Cinema for the lead but still built sheets.
3. **Can real phone footage of hands (e.g. actually ripping a SANTO mailer) be intercut with AI shots without a visible grade or texture mismatch?** Asteria and shy kids mix real and AI in principle, but nobody published a UGC-specific grade-match recipe. Candidate: shoot the real insert under the same light as the room plate and push both through the same phone-artefact post chain.
4. **Keep rate for 15-s UGC with locked keyframes.** Published ratios are for cinema (1–10%) or a solo short (~20%). Cutroom's own ledger (T18) is the only way to get a real number.
5. **The causal-chain wording for manipulations (T9 #3) is marked unproven in its own source.** It needs an A/B against the "two states + sound" pattern on the mailer.
6. **Kling vs. Seedance for garment macros.** The only claims are vendor/SEO blogs (C). Needs a same-keyframe A/B (T23).

---

## Sources actually seen (URLs from search results or read locally)
- PJ Ace: https://x.com/PJaccetturo/status/1932893267668185525 ; https://pjace.beehiiv.com/p/qatar-airways ; https://pjace.beehiiv.com/p/i-can-t-believe-disney-allowed-us-to-run-this-ai-ad-during-the-nba-finals-f77e73388ab4ca62 ; https://www.thedaringcreatives.com/creator-stories/pj-ace-nba-finals-ad/ ; https://themediabrain.substack.com/p/ais-disruption-of-advertising-and
- Air Head: https://www.fxguide.com/fxfeatured/actually-using-sora/ ; https://www.techradar.com/computing/artificial-intelligence/turns-out-the-viral-air-head-sora-video-wasnt-purely-the-work-of-ai-we-were-led-to-believe ; https://techcrunch.com/2024/04/27/creators-of-sora-powered-short-explain-ai-generated-videos-strengths-and-limitations/
- Paul Trillo: https://nofilmschool.com/ai-music-video
- Toys"R"Us / Native Foreign: https://digiday.com/marketing/why-toysrus-used-openais-sora-to-create-an-ai-generated-video/ ; https://creativitysquared.com/podcast/ep48-nik-kleverov-openais-sora-text-to-video-model/
- Coca-Cola: https://www.hollywoodreporter.com/business/digital/ai-coke-ad-holiday-studio-interview-1236420358/ ; https://futurism.com/artificial-intelligence/coke-ai-holiday-ad ; https://www.topazlabs.com/news/branded-content-reimagined-secret-level-and-coca-colas-ai-driven-holiday-classic
- Asteria / Topaz / USC ETC: https://www.topazlabs.com/news/asteria-is-building-the-future-of-filmmaking-with-hybrid-ai-workflows-and-topaz-video ; https://www.vp-land.com/p/the-topaz-ai-workflow-that-turns-8-bit-ai-into-16-bit-cinema-quality
- Promise / MUSE: https://www.forbes.com/sites/maureenkerr/2026/07/24/dave-clarks-ai-studio-promise-aims-for-films-hollywood-can-release/
- Staircase: https://variety.com/2025/film/news/staircase-studios-ai-pouya-shahbazian-1236326853/
- Dor Brothers: https://www.digitalcameraworld.com/features/anyone-whos-complaining-about-ai-now-will-use-it-later-yonatan-from-the-dor-brothers
- Hashem Al-Ghaili: https://getsuperintel.com/p/interview-with-hashem-al-ghaili-96cc3bcab199c3c1
- El Eternauta: https://www.primetimer.com/features/netflix-generative-ai-eternaut-scene
- Guess / Seraphinne Vallora: https://www.cnn.com/2025/07/31/style/vogue-ai-models-guess-campaign ; H&M: https://fashionunited.uk/news/fashion/h-m-turns-to-ai-digital-twins-in-new-campaign-as-fashion-grapples-with-blurred-realities/2025070482637
- Karen X Cheng: https://x.com/karenxcheng/status/1564626773001719813 ; hybrid phone reference: https://www.vp-land.com/p/step-by-step-the-state-of-ai-filmmaking-workflows
- Curious Refuge (character sheet: front/side/back + close-up): https://curiousrefuge.com/blog/how-to-create-an-ai-film
- GitHub (read locally): github.com/OSideMedia/higgsfield-ai-prompt-skill (HELL-GRIND.md, production-benchmarks.md, FAILURE-MODES.md); github.com/minhawork123-afk/guide-best-ai-filmmaking (GUIDE.md, examples/tess-lode-ugc); github.com/jnMetaCode/ai-shortfilm-prompts (faq.md, methodology.md)
- Vendor/SEO, used only as C-grade: invideo.io FAQ pages on shot length, grain and cut-hide; aifire.co NB2+Kling3 workflow.

---

# PART 6 — `04-ugc-tools-fashion.md`

## 04 — Competitor AI-UGC tools, fashion try-on, and real UGC craft

Scope: (A) what commercial AI-UGC products require as input and how they fake "product in hand", (B) apparel/try-on specifics, (C) what makes footage read as phone-filmed by a real person, plus performance/compliance data.
Method: about 45 WebSearch queries (the search budget ran out at the end), GitHub repos other agents had already cloned into `repos/`, and vendor docs quoted in search summaries. WebFetch and curl were blocked for every vendor, Reddit and help-centre domain I tried, so Reddit and X evidence only arrives through third-party summaries. It is marked C where that applies.
Strength key: A = vendor docs or several independent pros; B = one credible practitioner or vendor blog showing the method; C = claim or anecdote.

---

## TL;DR (the strongest findings)
1. **Every serious competitor gates video behind an approved *composite still* (avatar + product).** HeyGen Product Placement ("Generate Combined Images", then video), Higgsfield UGC Factory (4 Nano Banana keyframes per run, then Seedance), TopView and MakeUGC ("choose the best frame that shows your product"), and the Kling fashion MCP workflow ("approve model concepts → use product photos as refs *before adding motion* → test a few, then scale"). No competitor sends a product photo straight into a video model.
2. **Competitors are best at a person *talking about* a product, not *handling* one.** Arcads unboxing output fails about 20% of the time (product parts missing or misrendered). About 30% of actors show visible tells, and roughly only the top 20% pass a scroll test. HeyGen says its placement is optimised for *small handheld* items and that large items get scaled down. For SANTO, garments are the wrong shape for "product in hand" features, so shots should be designed as wear/try-on/detail shots, not holding shots.
3. **Kling's official try-on guide gives rules we don't apply yet.** The base model should already wear the *same garment category* (short sleeve for short sleeve). For bottoms, use full or lower body with a long top, and avoid boots or dresses. Half-body framing improves logo retention. Logos and fine text fail when the garment fills a small part of the frame.
4. **The #1 tell practitioners name in 2026 is the *script*, not the pixels.** Real speech uses contractions, starts with "And/But", trails off, repeats itself and has fillers. After that come mouth-audio lag, over-even lighting, eyes that don't track, hands and teeth, all noticed "within the first 2 seconds".
5. **Performance data favours AI only for product-driven, direct formats.** In the Ipsos/Syracuse study (20 ads, 3,000 US consumers), human ads scored +14% on short-term and +17% on long-term effectiveness. AI ads used a proven story structure 30% of the time against a 49% norm. NIQ (EEG) found AI ads rated "annoying/boring/confusing" with lower memory activation. Vendor-published "AI beats UGC" numbers are all self-interested.
6. **Compliance changed in 2026.** New York's synthetic-performer ad disclosure law has applied since 9 Jun 2026 ($1k first violation, $5k after that). EU AI Act Art. 50 applies from 2 Aug 2026. TikTok requires an AIGC label or disclaimer and detects C2PA; it says labelling does not reduce distribution. Meta auto-labels from C2PA and may move the label next to "Sponsored" for photoreal AI people. Icon (the "AI Admaker") went dark in Feb/Mar 2026 and now sells *human-only* UGC.

---

## Competitor input requirements table

| Tool | Product input | Person input | How "product in hand" is done | What users say fails | What they sell as "quality" | Source strength |
|---|---|---|---|---|---|---|
| **HeyGen** (Product Placement, Avatar IV / Veo 3.1) | Upload product photo(s), **≥720p, product front and centre**. Recommends **at least two images: product-only plus someone using or interacting with it**. Optimised for small/handheld products; large items "may appear scaled down to fit in the hand". | Stock/custom avatar (Avatar IV) | Two-stage: **"Generate Combined Images" (~60 s) → pick → optional "Custom Motion" text (gestures/expressions) → video at 720p/1080p**. Avatar IV for single natural scenes, Veo 3.1 for multi-scene. | Corporate/polished look; their own agency guide warns against "overly polished avatars with perfect skin and studio lighting" | Avatar IV gestures + lip-sync; scene-aware placement ("where it logically belongs") | A — help.heygen.com/en/articles/12704854, community.heygen.com agency cert parts 4–5, x.com/HeyGen_Official/status/1935702900195619312, x.com/diegocabezas01/status/1881855151293497853 |
| **Arcads** | Product photo upload ("so it knows exactly what your product looks like"); Product Showcase and Unboxing presets | 1,500+ stock actors or custom; many underlying models (Sora 2/Pro, Veo 3.1, Kling 2.6/3.0, Seedance 1.5/2.0, Nano Banana, GPT Image) | Custom avatar generated *holding* the product in stills. Talking-actor mode can't physically interact. | ~20% unboxing failure (product elements missing or misrendered). ~30% of actors show tells (robotic cadence, eye movement, stiff gestures). Trustpilot 3.0–3.3 and polarised: "glitchy, not lip-synced, clearly AI", marketing uses curated outputs. | Talking-head realism, actor library, multi-model access, Workflows (Jun 2026) | B — shhots.ai/blog/arcads-ai-review, trustpilot.com/review/arcads.ai, codingem.com/arcads-ai-review, intercom.help/arcads (platform guide) |
| **Creatify** (AdMax, Aurora, Product Avatar) | Product URL (scrapes store page) or JPG/PNG images + MP4/MOV (≤200 MB); "remove any low-quality images" | Stock avatar, custom avatar, DYOA (design your own) | Upload product image → avatar holding it; 2 avatar variations generated for review. Also "Avatar Showcase" (using/wearing). **Aurora best-practice base prompt: "4K studio interview, medium close-up shoulders-up, solid light-grey seamless backdrop, uniform soft key-light, presenter faces lens, steady eye-contact, *hands remain below frame, body perfectly still*, ultra-sharp."** | Works "for packaged goods, electronics, beauty — anything with clear visual identity" (i.e. rigid items) | Audio-driven lip-sync (Aurora), mood boards from competitor trends (AdMax) | A — help.creatify.ai/en/articles/12667081-aurora-model-best-practices, creatify.ai/blog/character-creator…, help.creatify.ai/en/articles/13757587-product-video |
| **MakeUGC** | Product **photo or video** (you "choose the best frame that shows your product clearly"); motion described in text | Stock or custom AI actors | "Product in Hand": hold, rotate, "demonstrate from multiple angles", even consume. Pro/Enterprise only. | — (no specific review data found) | Hold/rotate/consume product | B — makeugc.ai/product-in-hand-feature, makeugc.ai/features/how-to-make-ai-hold-your-product |
| **TopView** | Product photo or URL | Template avatar | Pick template → upload product → auto-placed in hand → choose video model, duration, prompt | "Depending on product's shape or size, fit in the hand can look slightly off". Reviewer: "product accurate… but hands distorted", "could tell it was AI". | Speed, template props | B — unite.ai/topview-ai-review, topview.ai/guides/how-to-create-product-avatar-with-ai |
| **Higgsfield UGC Factory / Marketing Studio** | Product URL (auto-extracts name, description, images) or **up to ~5 images** | 40+ presets or custom via Soul 2.0 / Soul ID | Modes: UGC review, unboxing, tutorial, **try-on**, TV spot, ASMR. **Each run makes 4 keyframes with product at different angles, placements and sizes**, and Nano Banana "locks text, logos, product form". Creator + product saved as *Elements* (angle set) and reused across clips. | — (vendor claims "preserves textiles, seams, branding during kinetic movement", unverified) | Consistency via Elements; Nano Banana placement | A/B — higgsfield.ai/blog/Higgsfield-UGC-Factory-Explained, higgsfield.ai/skills/ugc, repo charlesdove977/UGC-Factory (`skill/frameworks/seedance-elements.md`) |
| **Captions / Mirage Studio** | Prompt describing speaker "age, gender, clothing, background, **products**"; can upload audio/video of a winning ad to remix | Fully generated non-existent actors | Generated in-model (no product-photo lock) | — | Foundation model "trained on real human performances", micro-expressions | B — mirage.app/blog/mirage-worlds-first-foundation-model-for-ugc-video, help.mirage.app/docs/project/ad-studio |
| **Icon (icon.com)** | (was URL-to-ads) | — | — | "Slow, unusable, clunky" (Reddit, since mid-2025), billing complaints; **site locked Feb/Mar 2026; now "6 human UGC ads for $1000 (no AI / 100% real)"** | Now sells *human* creators | B — techstartups.com/2026/03/05/icon-the-ai-ad-startup-shuts-down…, adtechradar.com/2026/03/05/…, icon.com |
| **Tagshop** | Shopify/Amazon/Woo URL or images; script ≤1,000 chars | Custom avatar image <10 MB | "hold, wear, use, eat, pour, apply" | — | Format breadth | B — tagshop.ai, tagshop.ai/blog/how-to-create-ai-generated-ugc-videos… |
| **Billo** | Real creator marketplace + AI assist | Real creators | Real hands | — | Hybrid: "AI to test hooks at volume, humans to scale winners"; data from 150k ads, $280M tracked | B — billo.app/blog/ai-generated-ads-performance, billo.app/blog/creative-performance-engine |
| **Zeely** | Product link | Stock avatars | Template | "Awkward avatar delivery slips through on first pass", off-sync lip-sync for some accents, generic hooks | Speed, Meta launch | B — designkit.com/blog/zeely-reviews, trustpilot.com/review/zeely.ai |
| **Hedra** (Character-3) | Image (JPEG/PNG/WEBP) + audio | Character image | Product in the start image; animated with audio | Accuracy drops on fast or shouted speech and on non-frontal angles | Lip-sync "95% on clear audio <30 s" (vendor-adjacent claim) | B — hedra.com/blog/ai-lip-sync-video-guide, selfielabstudio.com Hedra tutorial |
| **Argil** (clone) | — | **~2 min (capture 3) of unedited talking footage**, camera at eye level, head **20–30% from frame top**, seated at desk, **arms still, face expressive**, best mic (a $20 lav helps a lot), no cuts or black frames | N/A (talking clone) | — | Personal clone | A — docs.argil.ai/resources/training-tips |
| **Synthesia** (Express-2, Selfie Avatars) | — | Small set of selfies → avatar in varied outfits/settings | N/A | "Looks professional rather than casual", weak for UGC | Multilingual, corporate | B — tomsguide.com (Selfie Avatars), synthesia.io |
| **Pippit (CapCut)** | Garment upload; "AI fashion model" / clothes swap by selecting regions | AI model with body types or your own photo | Try-on/clothes swap (image) → video templates | — | Speed/templates | C — pippit.capcut.com/resource/avatar-outfits |

**Pattern across all of them:** (1) product URL ingestion, (2) composite still first, (3) talking beats kept frontal with hands low or out of frame, (4) handling and unboxing is where they fail. None of them asks for a 3D scan or turntable. MakeUGC takes a product *video* and picks a frame from it, and HeyGen asks for an "in use" photo. Those are the closest any of them get to multi-view input.

---

## Techniques

### T1. Composite-keyframe gate with 4 variants (product placed in the still, then animated)
- **What / how:** Before any video credit is spent, generate the *exact start frame* with person + garment/product composited (Nano Banana edit from Soul ID still + product refs). Generate **4 variants per shot with different product angle, placement and scale** (Higgsfield UGC Factory default), approve 1, and only then animate with image-to-video. Rama Khalifa (Medium, Jun 2026) makes several start frames per concept: "holding the product", "product placed in front of them", "looking at the product". Kling's fashion MCP workflow says to "test, then scale: generate a few videos first, correct shared problems, then continue with the collection."
- **Fixes:** F2, F3, F9
- **Evidence:** HeyGen help article 12704854 ("Generate Combined Images" before video); higgsfield.ai/blog/Higgsfield-UGC-Factory-Explained ("four keyframes of your product at different angles, placements, and sizes"); kling.ai/blog/claude-kling-mcp-fashion-video-workflow; layer3labs.io/guides/best-ai-video-tools-for-product-placement ("fixing a wrong logo or color is far easier on a still than across 120 video frames"). **A**
- **Input change for Cutroom:** A shot's status can't reach "video" without an `approved_keyframe_id`. The keyframe step always produces 4 variants and the reviewer ticks logo, print, colour, hand and scale on the *still*. Store rejected stills with a reason code for rule mining.
- **Cheapest test:** 4 Nano Banana edits for one shot ≈ 6 credits, compared with ~18 per Seedance reroll.

### T2. Two-image product kit per SKU: clean product shot + real on-body photo
- **What / how:** HeyGen asks for **≥2 product images: "a clear image of the product" + "someone using or interacting with it"**, at ≥720p with the product front and centre. FASHN's rule is "maximum shape information, minimum clutter: an on-model reference beats a flat-lay", while flat-lay "still works". Ghost-mannequin images need cleaning before FASHN can use them. For SANTO, each SKU needs (a) a flat-lay/packshot and (b) a real phone photo of someone wearing it, standing front-on in even light. Image (b) carries drape, fit, length and how the print sits on a body, which a flat-lay can't show.
- **Fixes:** F2, F5
- **Evidence:** HeyGen help/X (diegocabezas01 thread), FASHN blog + claid.ai/blog/article/flatlay-to-model-ai-tools. **A**
- **Input change:** SKU record gets required slots `packshot_front`, `packshot_back`, `on_body_front` (phone photo), `on_body_side`, `detail_print`, `detail_label`. Block shot creation if `on_body_front` is missing for wear/try-on shots.
- **Cheapest test:** 0 credits to shoot. A/B one Nano Banana try-on with flat-lay only against flat-lay + on-body ref (2 × 1.5 credits).

### T3. Match the base garment before try-on or swap (Kling official rules)
- **What / how:** Kling's AI Virtual Try-On guide says:
  - **Tops:** use a **half-body** model image, which "enhances clarity and improves retention of logo details". The model must already wear the **same type of garment** (short sleeve for a short-sleeve top, and by extension a hoodie-like layer for a hoodie).
  - **Bottoms:** use a model image that shows the **full body or at least the lower half**, and the model should wear a **long top**. Avoid boots and dresses.
  - **Known failure:** "discrepancies… especially when the clothing occupies a small portion of the image or contains fine text."

  So for SANTO leggings or jeans shots, the Soul ID base still should be full-length in plain leggings or jeans with a longer top and trainers. For a hoodie shot, the base should be half-body in a plain hoodie of similar bulk.
- **Fixes:** F2, F5 (garment volume and silhouette don't have to be invented)
- **Evidence:** kling.ai/quickstart/ai-virtual-try-on-guide (via search summary), fal.ai Kolors try-on model page. **A**
- **Input change:** The model/avatar library stores per-person "base wardrobe" stills: plain tee half-body, plain hoodie half-body, plain leggings full-body with long top, plain jeans full-body. The shot planner picks the base that matches the SKU category.
- **Cheapest test:** 2 base stills + 2 swaps ≈ 6 credits. Compare against swapping onto a mismatched base.

### T4. Give the logo pixels: a dedicated detail shot for every printed SKU
- **What / how:** Text and logo fidelity fall apart when the garment is a small part of the frame (Kling guide). Research benchmarks treat "logo preservation" as its own fidelity dimension because it distorts first (arXiv 2608.29804). Commercial tools fail most on unboxing/detail handling (Arcads ~20%). So don't rely on the wide shot to carry the logo. Plan one **tight insert (chest print, woven label, hem tag) where the print fills ≥30–40% of the frame**. Hold the camera still or move it slowly, and use no body motion that folds the print. In wide and moving shots, accept a soft logo and keep them short.
- **Fixes:** F2
- **Evidence:** Kling try-on guide; arxiv.org/pdf/2608.29804 (dimension-wise garment fidelity, logo separate); TED-VITON paper notes most try-on models can't reproduce text like "Wrangler/Vans" (arxiv.org/pdf/2411.17017). **A** for the principle; the 30–40% figure is my working number and needs testing.
- **Input change:** Storyboard template for any SKU with a print requires a `detail_insert` beat. It can come from the real `detail_print` photo animated lightly (Wan ~3.5 credits) or be real phone footage.
- **Cheapest test:** Animate the real detail photo with a 3 s gentle push-in on Wan (~3.5 credits).

### T5. Identity angle set (3–4 angles, same wardrobe and light) + role-labelled refs, and don't over-stack product refs
- **What / how:** Build the person reference as an **angle set: front, ¾ left, ¾ right, profile, all in the same wardrobe and lighting**, registered as one element/ref group. The krusemediallc Arcads workspace ships 10-shot influencer sets named `01-hero-front, 02-3q-left, 03-3q-right, 04-profile-left, 05-profile-right, 06-face-closeup, 07-back-shoulder, 08-medium-portrait, 09-full-body-3q, 10-above-angle`. For *products* the Nano Banana guides warn the opposite: "one hero reference often beats a noisy stack of similar frames". Adding more refs sometimes made outfits drift or got the garment "swapped out entirely". When several images are passed, **state each one's job in the prompt**: "Image 1 is the garment source, image 2 is the pose reference, image 3 is the background."
- **Fixes:** F1, F2
- **Evidence:** repos/charlesdove977_UGC-Factory/skill/frameworks/seedance-elements.md ("A single front portrait limits how believably Seedance can turn the person… 3 to 4 images… front, three-quarter left, three-quarter right, profile"); repos/krusemediallc_arcads-claude-code/references/influencers/*; gennanobanana.com/guides/ai-reference-images; Seedance fashion guidance (cyprus-mail.com 2026-08-10) says to use "three reference groups instead of one crowded mood board", with the identity group showing the person under neutral conditions. **B**
- **Input change:** Person asset = angle set (min 4). Product refs are capped at 2–3 *distinct* views per call, and the prompt builder auto-inserts "Image N is …" role labels.
- **Cheapest test:** Same shot with a 1-image vs a 4-angle person ref where the subject turns ¾ (2 × Seedance ≈ 36; do it on Wan first ≈ 7).

### T6. Design "who is holding the phone" into every shot (fixes phone-in-hand-while-both-hands-busy)
- **What / how:** Real fit-check/haul content is filmed one of 4 ways, and each has fixed hand logic:
  - **Mirror selfie:** phone visible in one hand in the mirror, other hand free. This is the native fit-check format: "film vertically… as if the model is holding a smartphone herself while standing in front of a full-length mirror".
  - **Arm-length front-camera selfie:** one arm out of frame, one hand free. Wide, slightly distorted, close face.
  - **Tripod or propped phone:** both hands free, static frame, creator walks in and out. Creators use tripods and "mark your last foot placement" between outfit changes.
  - **Friend-filmed:** both hands free, handheld drift, back-camera look.

  Choose one mode per shot and write it into the prompt ("mirror selfie, her right hand holds an iPhone visible in the mirror; left hand tugs the hoodie hem"). Most "phone in hand while both hands busy" errors come from shots that never say who holds the camera.
- **Fixes:** F3, F6
- **Evidence:** TikTok discover pages "how to film a try-on haul / outfit TikToks"; creator workflow (tripod, foot marks). **B/C.** The hand-logic rule is my synthesis from how real creators film.
- **Input change:** Required shot field `camera_holder ∈ {mirror_selfie, arm_selfie, tripod, friend}`. It drives prompt text, lens look (front vs back camera) and a "max free hands" constraint the storyboard gate checks against the action.
- **Cheapest test:** Nano Banana still of the same action in mirror_selfie vs unspecified mode (3 credits).

### T7. One event per beat; never "hold + talk + open + turn" in one generation
- **What / how:** Competitors are reliable at talking-about and unreliable at handling (Arcads). Layer3's guidance: "Instead of asking a product to rotate, open, change environment, produce particles, and move into a user's hand at the same moment, assign those events to separate beats: establish the product in a stable position… rotate it slowly while preserving shape and label placement." For SANTO:
  - (a) mailer on the bed, still;
  - (b) hand tears the strip (real insert or AI, short);
  - (c) garment already out and held up (cut hides the state change);
  - (d) wearing it.

  A hoodie is not a small handheld object: HeyGen says large items get scaled down to fit the hand, so avoid "hold hoodie up to camera while talking".
- **Fixes:** F3, F4, F9
- **Evidence:** shhots.ai Arcads review; layer3labs.io guide; HeyGen help. **B**
- **Input change:** Storyboard linter counts verbs and objects per shot and rejects >1 state change or >1 hand interaction per generation.
- **Cheapest test:** 0 credits (linter rule), then one Wan comparison (~7).

### T8. Talking beats = frontal or ¾, hands low, body quiet; action beats = no lip-sync (VO over)
- **What / how:** All vendors that do lip-sync converge on the same constraints:
  - Creatify Aurora's base prompt keeps **hands below frame, body perfectly still, steady eye contact, uniform key light**.
  - Hedra: use **front or ¾ angles** ("models are trained primarily on frontal views"), clean, uncompressed, natural-pace audio, and **10–30 s** scripts. Accuracy drops on fast or shouted speech.
  - Argil trains clones on footage with **arms still, face expressive, head 20–30% from frame top**.

  So split the ad. **Lip-synced lines only in frontal/¾ selfie framing with hands low or out of frame. Every beat with hands, turning or garment action is voice-over or silent with on-screen text.** The front-camera arm-selfie is the one natural UGC frame where "hands below frame, body still" looks normal rather than stiff.
- **Fixes:** F8, F3, F1
- **Evidence:** help.creatify.ai/en/articles/12667081; hedra.com/blog/ai-lip-sync-video-guide; docs.argil.ai/resources/training-tips. **A**
- **Input change:** Shot type flag `speech ∈ {lipsync, vo, none}`. `lipsync` forces framing ∈ {arm_selfie, mirror_selfie close}, head-on or ¾, and max 1 hand action. The VO track is generated once for the whole ad and laid over the action beats.
- **Cheapest test:** 0 credits (rule), then 1 lip-sync shot.

### T9. Write the script like speech (the tell practitioners rank #1)
- **What / how:** "The tell is almost always the script. Real people don't speak in complete sentences — contractions, start thoughts with 'And'/'But', trail off, repeat themselves, filler ('honestly', 'I mean', 'basically', 'like'). Default LLM output reads like a press release wearing a hoodie." (AdMake AI). HeyGen agency guide:
  - Hook in **1–2 lines** that leads with a problem or outcome.
  - Structure **hook → benefit → proof/feature → CTA**.
  - **Max 1–2 on-screen callouts of 3–6 words.**

  Flare's creator guidance on reactions is the "pause before the punchline": a beat (inhale, glance up) before speaking, so it reads as forming a thought, not delivering a line. AppAgent A/B tests a scripted version against a freestyle version of each ad (their claimed ROI gain is 15–25%, **C**).
- **Fixes:** F8, F6
- **Evidence:** admakeai.com/blog/what-is-ai-ugc-ad; community.heygen.com agency cert part 5; joinflare.app/blog/ugc-unboxing-video-filming-techniques; appagent.com/blog/ugc-filming-guide; oakgen.ai/blog/realistic-ai-ugc-ads-checklist ("the voice matches the face"). **B** (several practitioners agree)
- **Input change:** A script linter pass rewrites into spoken register with ≥2 contractions, ≥1 filler and ≥1 self-correction or trail-off per 15 s, and no sentence over 12 words. It adds a `[beat]` marker before the reaction line, which becomes "pauses, glances up, then says…" in the video prompt.
- **Cheapest test:** 0 credits (LLM rewrite), then TTS only.

### T10. Garment image → image-to-video only; lock the garment in the prompt tail; calm camera
- **What / how:** Fashion practitioners agree that the garment must come from a still (real or try-on). "Image-to-video from a real or virtually tried-on still is the mandatory starting point… rules out text-to-video for the clothes themselves." Specific prompt levers:
  - "**keep full body in frame, hem visible**" (preserves garment length, avoids crops)
  - "**keep the garment's exact color, print and proportions unchanged**" as a prompt tail
  - "**Do not alter clothing category or primary color**" when wardrobe drifts
  - **reduce motion intensity**, because over-specified motion ("waving arms") causes warping
  - "**camera calmer than your coffee**": slow or medium moves let fabric read
  - **even, soft light**, because hard shadows get baked into the still and then warp in motion
  - keep **one palette** across iterations, since changing it raises flicker risk
  - one **fabric note** per material (the guide's example: "silk floats, denim holds, leather shines")
- **Fixes:** F2, F5, F7
- **Evidence:** morphed.app/blog/ai-video-generator-for-fashion; crepal.ai/blog/aivideo/kling-fashion-video-guide; wearview.co blog; fashionweekonline.com Seedance 2.5 consistency; cyprus-mail.com Seedance fashion. **B**
- **Input change:** The prompt builder auto-appends the garment-lock tail and the SKU's fabric note to every video prompt for a wear shot. Camera-move presets for garment shots are capped at "slow" or "medium".
- **Cheapest test:** Same keyframe with and without the lock tail on Wan (≈7 credits).

### T11. SKU "physical spec" sentence (fabric, weight, cut, fit, how it sits)
- **What / how:** The Seedance fashion guides say to describe "every garment in physical detail — fabric, weight, cut, colour, wear, fit, how it sits on the body". Use ghost-mannequin style outfit references (full outfit, no body). Keep a **continuity sheet** per shot (look, accessories, hair, location, light, any movement that affects the garment). Example for SANTO: "heavyweight 400gsm brushed-back fleece hoodie, dropped shoulders, boxy fit ending at the hip, ribbed cuffs and hem, kangaroo pocket, puff-print logo across chest; fabric is thick and holds shape, folds in soft rounded creases, doesn't flutter." Leggings: "high-waisted, matte opaque compression knit, smooth taut across thighs, slight sheen only on the curve of the knee, no wrinkles except at the ankle bunch."
- **Fixes:** F5, F2
- **Evidence:** fashionweekonline.com/how-to-write-seedance-2-5-prompts…; cyprus-mail.com/2026/08/10/seedance-2-0-for-fashion…; sweetsofties.com Seedance fashion films. **B/C** (guides, not controlled tests)
- **Input change:** SKU record gets `physical_spec` (1–2 sentences, written once from the real garment) and `motion_behaviour` (how it folds, stretches or holds). Both are injected into every image and video prompt for that SKU.
- **Cheapest test:** 2 Wan runs of a leggings squat with and without the spec (≈7 credits).

### T12. Garment continuity QC checklist (auto-built from the SKU)
- **What / how:** Inspect "hems, lapels, closures, prints, seams, pockets, straps, jewelry, shoes, and the relationship between layers — a garment should not gain or lose construction details as the model turns". PCTechMag's framing is to diagnose *which* continuity rule broke and *when* (character, product or environment) before changing the prompt. Identity drift shows most in profile views, fast movement, expression changes, and cuts between wide and close.
- **Fixes:** F2, F1, F7, F9 (targeted reroll instead of blind reroll)
- **Evidence:** cyprus-mail.com Seedance fashion; pctechmag.com/2026/08/from-face-drift-to-product-distortion…. **B**
- **Input change:** The rejection form is a checklist generated from SKU fields (pocket? drawcord? cuffs? print position? label?) plus a `failed_at_second` field. That feeds rule mining ("profile turns > 1 s drift → cap turns").
- **Cheapest test:** 0 credits.

### T13. Shot-duration budget: 1.5–3 s used per shot, generated at 4–5 s
- **What / how:** Current short-form pacing is about **0.5–0.8 cuts per second (≈1.25–2 s average shot length)** with a scene change every **2–3 s**. Practitioners also say 0.5 s jump-cut spam "looks dated now" and argue for "purposeful cuts". A 15 s SANTO ad is therefore 6–9 shots. Generate each at the model's shortest useful length and **keep only the cleanest 1.5–3 s window**. Drift (face, print, room) accumulates with time, so short windows hide it.
- **Fixes:** F1, F2, F7, F9
- **Evidence:** Pacing: editingmachine.com / billo.app/blog/ugc-video-editing / joinflare.app TikTok playbook (search summaries). **B** for pacing. The drift benefit is my inference, **C**, and should be tested.
- **Input change:** Storyboard enforces a 15 s = 6–9 beats template. The generation request sets the minimum duration. The editor UI picks an in/out window per clip rather than using the full clip.
- **Cheapest test:** 0 credits. Re-cut an existing rejected 5 s clip to its best 2 s and re-review.

### T14. Choose product-driven formats; avoid emotional "testimonial story" formats for AI
- **What / how:** Ipsos + Syracuse Newhouse (20 real brand ads, 3,000 US consumers): human-made ads scored **+14% short-term and +17% long-term** effectiveness. AI ads used a proven storytelling structure **30% vs 49% norm**. AI did best on "straightforward, product-driven" briefs and in "formats a brand has already proven out". NIQ neuroscience (2,000+ viewers, ~150 on EEG) found AI ads rated more "annoying, boring, confusing" with **lower memory activation even when high quality**. Klaviyo/Datalily (Dec 2025): 7% trust a brand more for visible AI content, 31% less. For SANTO the AI-friendly formats are fit check, fabric close-up, "3 ways to wear", size comparison and unboxing reveal. AI is weak at "my story" testimonials. Hybrid is standard: AI tests hooks and angles, then humans or real footage re-shoot the winners (Billo, AdMake).
- **Fixes:** F9 (don't spend credits on formats AI loses on), F6
- **Evidence:** news.syr.edu/2026/05/18/newhouse-research-finds-ai-ads-fall-short-on-sales-impact; phys.org/news/2026-05-ai-ads-indistinguishable-human-dont.html; nielseniq.com 2024 AI-ads study; marketingdive.com NIQ coverage; billo.app/blog/ai-generated-ads-performance. **A** (independent studies). Note that vendor claims like "12–23% higher CTR" (trylapis) or "85–110% of UGC CTR" come from AI-tool sellers, **C**.
- **Input change:** The format picker defaults to product-demo formats and flags "personal testimonial" formats as high-risk (performance and legal, see T15). Tag each ad with its format so results can be compared.
- **Cheapest test:** 0 credits.

### T15. Disclosure-safe authenticity: "phone-filmed look", not "fake customer"
- **What / how:**
  - **NY GBL §396-b (in effect 9 Jun 2026)** requires a "conspicuous disclosure" when an ad contains a synthetic performer, in any medium, with $1,000 then $5,000 penalties.
  - **EU AI Act Art. 50 applies from 2 Aug 2026** (final guidelines 20 Jul 2026).
  - **TikTok** requires the AIGC label or a clear caption, watermark or sticker for realistic AI people. Undisclosed ads get rejected or restricted, TikTok detects C2PA, and it states labelling doesn't reduce distribution.
  - **Meta** auto-labels from C2PA/IPTC and "for a photorealistic AI-generated person the label can move next to 'Sponsored'".
  - **UK ASA** has no blanket AI-disclosure rule, but the misleading-testimonial rules apply. A synthetic person saying "I bought this and…" is a fabricated endorsement (Oakgen makes the same point).

  So the realism target is a phone-filmed *product demonstration*, scripted in the demo voice ("this is the 400gsm one, look how thick…"), not a first-person purchase claim.
- **Fixes:** Risk control. It also reduces F9, because rejected or restricted ads waste the whole spend.
- **Evidence:** cooley.com 2026-01-29 insight; governor.ny.gov announcement; afslaw.com; artificialintelligenceact.eu/transparency-rules-article-50; ugcvids.ai/cinerads TikTok policy summaries; seller-us.tiktok.com AIGC restrictions; coinis.com Meta 2026 labeling; asa.org.uk AI disclosure articles. **A**
- **Input change:** Each ad record stores `ai_disclosure` (label/caption used) and `markets`. The script linter blocks first-person purchase or outcome claims from synthetic performers. Keep C2PA intact on export; don't strip it to evade labels.
- **Cheapest test:** 0 credits.

### T16. Unboxing: sound is the content; slow handheld; reaction beat
- **What / how:** Flare's unboxing craft notes:
  - "Unboxing is one of the few UGC formats where **ambient audio is part of the experience**": tape peel, crinkle, tissue.
  - "**Move slowly, keep the phone handheld, let the product fill the frame.**"
  - Reactions get the pre-line beat from T9.
  - "The second it looks like a commercial, the illusion breaks."

  For the SANTO poly mailer, record *real* foley once (tear strip, poly crinkle, garment slide-out, fleece rustle on the bed) and reuse it. The tear itself can be a real-hands insert, which brief item "real-hands inserts" already covers.
- **Fixes:** F8, F4
- **Evidence:** joinflare.app/blog/ugc-unboxing-video-filming-techniques; recharm.com unboxing guide ("crinkle of paper, the snap of a seal"). **B**
- **Input change:** Asset library gets a `foley` category tied to packaging type (poly mailer) and fabric type (fleece, denim, jersey). The unboxing template requires foley tracks and forbids a music-only bed.
- **Cheapest test:** 0 credits (phone recording).

### T17. Ingest the product page automatically (every competitor does this)
- **What / how:** Creatify, Tagshop, TopView, Zeely and Higgsfield Marketing Studio all start from a **product URL** and pull images, title, description and price. For SANTO this means pulling the Shopify product: all media (angles), variant colours, material and description text. That gives a complete multi-angle SKU kit with no manual upload errors, and the description seeds `physical_spec` (T11). A Shopify connector is available in this environment.
- **Fixes:** F2, F9
- **Evidence:** creatify.ai/blog/turn-product-link-into-a-video-ad…; higgsfield.ai/blog/Higgsfield-UGC-Factory-Explained; tagshop.ai. **A**
- **Input change:** "New SKU" = paste the santo.clothing product URL or pick from Shopify. The app auto-fills packshots and description, then asks only for the missing real photos (on-body, detail, label).
- **Cheapest test:** 0 credits.

### T18. Lighting and lens vocabulary that reads as phone, not studio
- **What / how:**
  - "Studio lighting is the AI tell that kills more UGC prompts than any other single element."
  - Remove "Canon R5 / cinema camera" terms, which pull the model toward magazine output.
  - Name a specific phone *and camera*: "iPhone 12 front camera" gives a different signature from "iPhone 15 Pro back camera".
  - Real creator lighting is a **window at ~45° to the side**: not behind the subject (silhouette), not straight in front (flat, blown background).
  - Real creators use the **back camera** for sharper b-roll and product shots and the front camera for selfie talking.

  Match that split: selfie talking beats get the "front camera, arm's length, slight wide-angle distortion, everything in focus" look, and product/detail b-roll gets the "back camera, close focus".
- **Fixes:** F6
- **Evidence:** james-palm.medium.com (UGC prompt structure); myup.ai/blog/ai-ugc-ads-realistic-prompt-guide; recharm.com/blog/5-tips-to-shoot-ugc-videos; useclip.com/how-to-film-ugc-at-home. **B/C.** The brief already has a "phone camera profile"; this adds the front/back split tied to `camera_holder` (T6).
- **Input change:** `camera_holder` maps to a lens/look preset (front: ~24–26 mm-equivalent wide, deep focus, slight sensor noise; back: normal lens, close focus). Words like "studio", "softbox", "bokeh", "85mm" and "cinematic" are on a banned list for UGC prompts.
- **Cheapest test:** 2 Soul stills, studio-free vs default (≈3 credits).

### T19. Finishing numbers practitioners quote (order matters)
- **What / how:**
  1. Upscale with **low denoise**; aggressive denoise gives "waxy skin".
  2. **0.3–0.8 px Gaussian** softness to kill AI edge crispness on hair and edges.
  3. Grain/noise **after** upscaling. Grain applied at generation resolution smears when upscaled. Use 20–40% opacity Soft Light for a handheld feel, "if you can see it consciously it's too much".
  4. Export **1080p, 30 fps (not 60), H.264, medium bitrate**. For phone feel, add slight motion blur and chromatic aberration.
- **Fixes:** F6
- **Evidence:** invideo.io/blog/ai-video-post-production; invideo.io/faq/does-adding-film-grain…; videoai.me blog. **C** (vendor blogs, no A/B shown). Only included because the brief lacks numbers.
- **Input change:** The FFmpeg finishing preset uses these defaults, with grain opacity as one slider.
- **Cheapest test:** 0 credits (post only).

### T20. Put the fought-for detail inside the platform safe zone
- **What / how:** Reels UI covers the **top 14%, bottom 20–35%, and 6% each side** (1440×2560: ~358 px top, up to 896 px bottom, ~87 px sides). Compose keyframes so the chest print, label and face sit in the centre safe band. Otherwise the one element that took 4 rerolls to get right sits under the caption or CTA. TikTok marketing science data: original audio gave **+52% awareness** against registered tracks (VidMob via TikTok); voiceover appears in only 39% of ads; 90% of recall impact is captured in the first 6 s.
- **Fixes:** F2 (in effect), F8, F9
- **Evidence:** blog.adnabu.com/meta-ads/meta-safe-zones; billo.app/blog/meta-ads-safe-zones; ads.tiktok.com/business/creativecenter (Power of Creative Elements); ads.tiktok.com/business/en/creative-codes. **A**
- **Input change:** The keyframe review UI shows a safe-zone overlay, and the logo/face bounding box must fall inside it.
- **Cheapest test:** 0 credits.

---

## Authenticity checklist (evidence-backed)
Use as the storyboard and review gate. Each line cites where the claim comes from.

**Script and voice**
- [ ] Spoken register: contractions, a sentence starting "And/But", ≥1 filler, ≥1 trail-off or self-correction per 15 s. *(AdMake AI; Oakgen "voice matches the face")*
- [ ] Hook ≤2 lines, value in first 3 s; ≤2 on-screen callouts of 3–6 words. *(HeyGen agency cert pt 5; TikTok Creative Codes)*
- [ ] A beat (inhale or glance) before the reaction line. *(Flare)*
- [ ] No first-person purchase or outcome claims from a synthetic person; AIGC label planned. *(NY GBL 396-b; TikTok AIGC; ASA; Oakgen)*

**Framing and bodies**
- [ ] Every shot declares who holds the phone (mirror / arm selfie / tripod / friend), and the hand count adds up. *(creator filming practice, T6)*
- [ ] Lip-synced lines only frontal or ¾, hands low, body mostly still; everything else is VO. *(Creatify Aurora, Hedra, Argil docs)*
- [ ] One state change or hand interaction per generation. *(Layer3; Arcads unboxing failure rate)*
- [ ] Garments are worn or shown, not "held up to camera" like small products. *(HeyGen: large items get scaled down)*

**Garment fidelity**
- [ ] Base person still already wears the same garment category; bottoms shot full-length with a long top. *(Kling try-on guide)*
- [ ] Garment enters via an approved still (try-on or real), never text-to-video. *(Morphed, Layer3, Kling MCP workflow)*
- [ ] Printed SKU has a detail insert where the print fills a large share of the frame. *(Kling: small area → text errors)*
- [ ] Prompt carries the lock tail + SKU physical spec + "hem visible" for full-body shots. *(Wearview, CrePal, Seedance fashion guides)*
- [ ] QC checklist: hems, cuffs, pockets, drawcords, print position, label, layers the same at start and end of the clip. *(Seedance fashion continuity sheet)*

**Look**
- [ ] No "studio / softbox / 85mm / bokeh / cinematic / Canon" words; name a phone and which camera. *(UGC prompt guides)*
- [ ] Window side-light at ~45°, never behind; not perfectly even. *(creator lighting guides; HeyGen "avoid studio lighting")*
- [ ] Background is a normal lived-in room, not "too perfect". *(Oakgen)*
- [ ] Slow or medium camera on garment shots; handheld energy only on the hook. *(CrePal; UGC-Factory beat movement)*

**Edit and sound**
- [ ] 6–9 shots in 15 s, each 1.5–3 s; purposeful cuts, no 0.5 s spam. *(pacing guides)*
- [ ] Real ambient and foley on unboxing (tape, poly crinkle, fabric). *(Flare)*
- [ ] Burned-in captions and logo inside safe zone (top 14% / bottom 35% / sides 6% clear). *(Meta safe-zone docs)*
- [ ] Finishing: low-denoise upscale → subtle blur → grain → 1080p30 H.264. *(invideo; C-grade)*

**Known viewer tells to scan for in the first 2 s** *(AdMake, Pictory, Mammoth summaries)*: mouth lagging audio, micro-expression mismatch, eyes not tracking, lighting too even, hands and teeth in close-up, product "subtly wrong".

---

## STOP DOING
1. **Sending a product/garment photo straight into a video model.** No competitor does it; they all composite and approve a still first. *(T1)*
2. **"Holding the product while talking" shots for garments.** Tools built for this (Arcads, TopView, HeyGen) fail most on handling, unboxing and large items. *(T7)*
3. **Lip-sync in profile, while turning, or with busy hands.** Vendor docs restrict it to frontal/¾ with a still body. *(T8)*
4. **LLM-clean scripts.** This is the most-cited 2026 tell. *(T9)*
5. **Stacking many near-duplicate product refs.** It can make the garment drift or get swapped; use 1 hero + 1–2 distinct views, each with a stated role. *(T5)*
6. **Swapping a garment onto a base that wears a different category**, e.g. a hoodie onto a tank top or leggings onto a dress. *(T3)*
7. **Expecting the logo to survive in wide or moving shots.** Give it a detail insert instead. *(T4)*
8. **Fast or big body motion in garment shots** ("waving arms", spins). It warps prints. *(T10)*
9. **Studio/cinema vocabulary** in UGC prompts. *(T18)*
10. **Emotional first-person testimonial formats with AI people.** Weakest in the Ipsos/NIQ data, and a misleading-endorsement and disclosure risk in NY, the EU and under ASA rules. *(T14, T15)*
11. **Trusting AI-UGC vendors' performance stats** (e.g. "+12–23% CTR"). They are self-published; independent studies show a gap. *(T14)*
12. **Stripping C2PA or hiding AI use.** Platforms detect it and require the label, and TikTok says labelled content isn't down-ranked. *(T15)*

---

## Open questions
1. **Logo frame-share threshold:** at what share of the frame does a SANTO chest print stay stable on Seedance, Kling and Wan? My 30–40% figure is a guess. Test with one print at 3 crop sizes on Wan (≈10 credits).
2. **Does the "short window" edit really hide drift enough** to make 5 s generations → 2 s used cheaper than aiming for perfect 5 s clips? Track the reroll rate against the used-window length.
3. **Higgsfield Marketing Studio "try-on" mode vs our own Nano Banana → Seedance chain.** Is the preset's garment fidelity better, and what does it cost per usable shot? (I couldn't open the Higgsfield Academy "Marketing Studio Try-Ons" page: higgsfield.ai/academy/courses/brand-visuals-ai/marketing-studio-try-ons.)
4. **Which markets does SANTO advertise in?** That decides whether NY GBL 396-b or EU Art. 50 disclosure applies. UK-only still needs ASA testimonial care.
5. **Does the AIGC label cost performance for fashion UGC specifically?** TikTok says no; there's no independent data. Worth a paired test once ads run.
6. **Reddit and X evidence gap:** Reddit and X were not reachable (WebFetch blocked; search returned no specific r/aivideo, r/UGCcreators or r/FacebookAds threads), so the "viewer tells" list relies on agency blog summaries. A human skim of r/FacebookAds "AI UGC" threads would firm this up.
7. **Leggings and denim physics:** I found no independent evidence on what fixes fake-looking compression fabric beyond fabric description and calm motion. Real on-body reference photos (T2) are the best-supported lever; a squat or lunge test per model is needed.

---

# PART 7 — `05-github-research.md`

## 05 — GitHub open source + research: skills, tools, auto-QA, AI-detection signals

Scope: I read the repos listed below, either as shallow clones in `research/repos/` or as raw files. The 2026 skill libraries for Seedance and Higgsfield turned out to be the most useful source: several contain **measured or field-logged** rules, and some come from Higgsfield Studio's own production breakdowns as re-documented by OSideMedia. Stars could not be verified because the GitHub API is blocked; recency is the **last-commit date read from the clone**.

Evidence strength: **A** = vendor docs or several independent practitioners showing results. **B** = one credible practitioner or team with shown or measured results. **C** = claim, re-derived heuristic or my own engineering proposal.
Credit costs use the BRIEF's figures: Nano Banana (NB) ≈1.5, Seedance ≈18, Wan ≈3.5. **Note:** joebenscoter's validated log says Seedance 2.0 at 15 s, 720p, with audio costs **~67 credits** (1080p is ~135). See Open questions.

---

## Part A — Techniques (inputs, prompts, finish)

### 1. Person-only identity plate + "untouched base" + face-lock crop
- **What/how:**
  1. Generate the creator as a **close-up portrait, person only, no product, no props, plain grey background**.
  2. That close-up is the **only face source**. **Never run it through a model again**: every later look, wardrobe or state is composited *around* it with masks.
  3. On any character sheet, **crop the heads out of the full-body panels**. At full-body scale the face is "a few dozen pixels", and averaging it with the close-up drags identity toward generic.
  4. Sheets go on **plain grey**, not a set or gradient. A busy sheet costs rerolls because the video model can't tell character from world.
  5. If the person must turn, build the Element from an **angle set**: 3–4 images of the same person in the same wardrobe and light (front, ¾ left, ¾ right, profile), registered in ONE element-create call.
- **Fixes:** F1, F6 (every model pass softens skin toward plastic), F2 (product in the portrait "causes compositing drift").
- **Evidence:** joebenscoter/higgsfield-ugc-workflow `skills/ugc-base-character/SKILL.md`: "PERSON ONLY… product in the base portrait causes compositing drift" (validated run, 2026-06). OSideMedia `skills/higgsfield-soul/SKILL.md` § Untouched Base [FIELD — Higgsfield Studio ONEIRIC + ADILIADA breakdowns, 2026-08]. `skills/higgsfield-seedance-2-5/VFX-PIPELINE.md` § face-lock crop and grey background [FIELD — Higgsfield "AI vs VFX" build, 2026-08-08]. charlesdove977/UGC-Factory `frameworks/seedance-elements.md` (angle set). **B**
- **Cutroom input change:** store `identity_plate` as an immutable, hash-locked file that is never sent as an edit input. Store `body_panels` with heads blanked. Refuse any pipeline step that regenerates the plate. Store the angle set as one Element.
- **Cheapest test:** 2 Seedance generations of the same shot: full sheet vs plate + head-cropped sheet (≈36, or ≈134 at the 67-credit rate).

### 2. Reference roles with explicit inherit / do-not-inherit lists
- **What/how:** give each reference one stable token and reuse it verbatim. List what to take from it **and** what not to take. Never use a grouped reference like "@Images 1–4 define four characters".
  ```
  [Characters] <Maya> corresponds to @Image 1. Use only the face, hair, skin tone and build. Do not use its background, pose, framing or lighting.
  [Wardrobe] <SANTO hoodie> corresponds to @Image 2 and @Image 3. All these images define one single hoodie; the output must contain only one. Use only the structure, fabric, colour, print placement and stitching.
  [Scene] <Bedroom> references @Image 4. Use only the spatial layout, furniture and window light. Do not use the people in the image.
  ```
  Break the outfit into named garments ("same outfit" drifts). Restate the same-face requirement for head turns, looking down, a hand near the face and fast motion. That is where identity drifts hardest.
- **Fixes:** F1, F2, F7.
- **Evidence:** gbeyrouti/seedance-prompting-claude-skill `references/references-et-modes.md` (2026-08). LearnPrompt/awesome-seedance `docs/templates/en/character-reference-lock.md`: "The inherit-nothing-else clause is what separates working locks from broken ones" (derived from 497 verified cases, 264 cross-model retests: 193 reproduced / 68 degraded / 3 failed). smixs/visual-skills `video/references/universal-rules.md`. **B** (three independent libraries agree).
- **Cutroom input change:** every stored reference gets `token`, `role`, `inherit[]` and `exclude[]` fields. The prompt compiler emits these lines automatically. A multi-view product automatically gets the "one single object" line.
- **Cheapest test:** 0 extra (a prompt change on the next paid shot).

### 3. One reference sheet per STATE ("a sheet is not a menu")
- **What/how:** "If it sees a detail, it will try to show it." In the logged failure, a mecha sheet showed a hatch open, so the model opened it in most shots or deformed the design. For SANTO this means separate assets for: mailer **sealed**, mailer **torn open**, hoodie **folded**, hoodie **worn**, zip **closed**, zip **open**, jeans **folded** vs **worn**.
  - Attach only the state that is visible in that shot.
  - Give a mechanism (zip pull, mailer tear strip) its own close-up input.
  - Labels on a sheet teach nothing. Describe the operation as physical action in the prompt.
- **Fixes:** F4, F2.
- **Evidence:** OSideMedia `skills/higgsfield-soul/SKILL.md` § "A sheet is not a menu" [FIELD — Higgsfield Studio ZEPHYR breakdown, 2026-08-06]. **B**
- **Cutroom input change:** the product kit is keyed by `state`. Each shot declares `start_state`/`end_state`, and the compiler attaches only the matching state images. This makes the existing "product state photo kit" enforceable.
- **Cheapest test:** 2 NB state images (≈3) + 1 video.

### 4. Write manipulations as a causal chain; never let hands "mime"
- **What/how:** the named failure is "mimed manipulation": fingers work over a pack that never opens. Write it as five facts, in order:
  1. **initial structure**
  2. **anchor** (the other hand)
  3. **force** (where the force is applied and in which direction)
  4. **material feedback**
  5. **finished state**, held for a beat

  Example for the mailer: *"The grey SANTO poly mailer is sealed along the top flap. Her left hand pins the bag flat against her thigh; her right thumb and forefinger pinch the corner of the flap and pull it diagonally toward her chest. The plastic stretches, then the adhesive strip peels away with a crinkle; the bag creases where her left hand grips it. The flap now hangs open and the folded black hoodie is visible inside; she holds still for half a second."*

  Also name the **completion state** of every action. Otherwise the cut lands mid-action ("truncated action"). Alternatively, open the next shot on the result already being true.
  - **Routing rule:** if the manipulation only *gets you to* the next state, use "two states + a sound": sealed bag → tear SFX off screen → hands already inside. That version cannot fail.
  - Never stack a legible brand face, a two-handed manipulation and an effect in one shot.
- **Fixes:** F4, F3.
- **Evidence:** OSideMedia `skills/higgsfield-seedance/FAILURE-MODES.md` § Mimed manipulation and § Truncated action. It is labelled "HOUSE — re-derived from nutllwhy/seedance-tvc-director evaluation. UNPROVEN HERE". **C/B** (named mechanism, no A/B yet)
- **Cutroom input change:** a shot with `manipulation` must fill the five fields. If any field is unknown (the notch or seal isn't visible in the reference), Cutroom forces the cut-around route.
- **Cheapest test:** the mailer rip, chain version vs verb version: 2 Seedance generations.

### 5. Hand headcount, ownership and "who holds the phone"
- **What/how:** in every hand close-up, add: *"There are only two hands in the frame, both belonging to the same person, entering from the same sleeve."* A solo lock-picking close-up grew a **third hand**; a count alone still let hands arrive from two directions.
  - For selfie beats, the phone hand is off-frame. Only ONE hand may touch product, or switch to "phone propped on the dresser" framing.
  - The useapi tutorial pins hand state explicitly: *"keeping both hands on the mug while she speaks… both hands resting on the table again by the eight-second mark."*
  - Add *"realistic hands"* explicitly (LearnPrompt UGC template: "product handling is where finger count fails").
  - Never have the creator **walk and do fine manipulation in the same beat**. Split them.
- **Fixes:** F3.
- **Evidence:** OSideMedia FAILURE-MODES § Orphan limbs [FIELD — Higgsfield Studio RED FLAG breakdown, 2026-08-19]. useapi/google-flow-api `ugc-product-video/prompts.json` + README (2026-09). LearnPrompt `docs/templates/en/ugc-creator-review.md` (pitfalls drawn from 11 filed UGC cases). **B**
- **Cutroom input change:** shot schema field `camera_holder: selfie_L | selfie_R | propped | mirror | second_person`. The compiler refuses two-handed product actions when `selfie_*` and emits the hand clause for any shot with hands.
- **Cheapest test:** free lint + next paid shot.

### 6. Scale as a computed body landmark, plus an asymmetry lock
- **What/how:** a bare number ("110 cm railing") did nothing. Converting it to a body landmark held: *"the railing is 110 cm; on a 185 cm man the top rail lands just above his belt."* **The landmark must be arithmetically true.** A wrong anchor is obeyed and the object gets resized to match. When unsure, prompt the item *smaller*, never larger: undersized reads as distance, oversized reads as fake. For SANTO: *"the mailer is 38 × 50 cm; held against her chest its top edge sits at her collarbone and the bottom edge at her navel"*. Compute this from real product dimensions and the creator's height.
- **Fixes:** F3 (giant/tiny product).
- **Evidence:** OSideMedia `VFX-PIPELINE.md` § Scale law [FIELD — AI-vs-VFX 2026-08-08 + RED FLAG 2026-08-19]. **B**
- **Cutroom input change:** the product record stores real dimensions. The creator record stores height. The compiler generates the landmark sentence, so it is never hand-written.
- **Cheapest test:** 2 NB stills (≈3).

### 7. Route image models by asset class; fix sheets with a one-line NB edit
- **What/how:** Higgsfield's own VFX build found **no single best image model**:

  | Asset | Model |
  |---|---|
  | Face match / character sheets | Nano Banana 2 |
  | Clothing, wardrobe, **branded garments** | **GPT Image 2** |
  | Locations | Soul Cinema. NB makes locations "too clean and too symmetrical"; GPT skews yellow. |

  **Small fixes are a model switch plus one sentence, not a re-prompt.** Attach the flawed sheet plus the correct asset to NB 2 and write e.g. *"change the logo to the one in image two."* Re-prompting the whole sheet re-rolls everything that was already right. The two recurring image-stage tells are **warped logos** and **blue-ish colour shifts**; check for them before a sheet is locked.
- **Fixes:** F2, F7, F6, F9.
- **Evidence:** OSideMedia `VFX-PIPELINE.md` § Stage 1 [FIELD — Higgsfield AI-vs-VFX build, 2026-08-08]. **B** (one vendor production team; not tested on streetwear)
- **Cutroom input change:** an `asset_class → model` router table. A "Fix" button always runs NB with [flawed, correct-asset] + one sentence and never re-generates.
- **Cheapest test:** the same SANTO hoodie still on GPT Image 2 vs NB (2 image generations) + one logo-fix edit (≈1.5).

### 8. "Hub frame" clips: the same approved still as start AND end frame
- **What/how:** each clip is generated with the approved still as **both** `start_image` and `end_image`, so every clip opens and closes on the same frame. Any clip can then follow any other, and the face, room and product are re-anchored at both ends.
  - Choreograph by the clock: *"by the eight-second mark the mug is back down… for the final two seconds she holds completely still."* Without that, the model runs the line long and snaps into the end frame.
  - About **20 words fit 10 s**.
  - Describe the voice **identically in every clip**; nothing carries a voice between generations.
  - **Trim to the sound, not the picture.** The presenter goes still before she stops talking.
  - Seedance rule: first and last frames must share an aspect ratio, or the last frame stretches.
- **Fixes:** F1, F7, F9, F8.
- **Evidence:** useapi/google-flow-api `ugc-product-video/README.md` + `prompts.json` (tutorial 2026-09-04, Veo/Omni Flash). gbeyrouti `references/debug-et-limites.md` (first/last frame ratio lock). **B** (Veo-side; untested on Seedance via Higgsfield)
- **Cutroom input change:** shot type `hub` (start = end = approved still). Editor trims per clip, stored as `trimStart`/`trimEnd` after an audio check.
- **Cheapest test:** 1 Seedance generation with start = end.

### 9. Dialogue budget and formatting (measured)
- **What/how:**
  - **Short lines cause filler-babble.** In a measured test (Seedance 2.0, English, 4 s, 480p), *every take with ≤6 words* came back wrapped in invented mumble or the line said twice. 8- and 12-word lines were **4/4 clean**, with no truncation up to 12 words (~3 words/s).
  - Either extend the line to fill the window or script the silence with a named pause, SFX or action.
  - Give every other visible face a positive mouth state: "lips at rest, jaw closed".
  - Reliable-sync budget for English ≈ **16–20 words per ~15 s clip**, 5–10 per line (community field numbers). joebenscoter validated **~32 words / 15 s** as speakable, but *speakable ≠ synced*.
  - Format: open the prompt with **one voice spec line** (tone, age, gender, language, accent). Introduce lines as `she says: "…"`, not `saying, "…"`. No em-dashes in the VO. End with **"No subtitles."**
  - **Phonetic respelling in the spoken quote only.** `nustandardlabs` was read letter-by-letter and `New Standard Labs` came out "labbers"; `Noo Standard Labz` worked. Use "z" for voiced plurals. Anchor awkward words to a known one-syllable word: `vial` → `vile`.
  - Add explicit pacing cues ("leaves a beat of silence after each sentence"), because models default to fast speech.
- **Fixes:** F8, F9.
- **Evidence:** OSideMedia FAILURE-MODES § Filler-babble [MEASURED — sync-budget ladder 2026-08-09, EN × 4 s × 480p × Seedance 2.0; small n]. `skills/higgsfield-audio/SKILL.md` § Per-language budgets [FIELD — community Emily2040/seedance-2.0 v6.6.0]. joebenscoter `skills/ugc-multicut-script/SKILL.md` § VO Pronunciation Playbook (validated 2026-06-22). krusemediallc/arcads-claude-code `prompt-library/seedance-2-ugc.md` (pacing rule). **B**
- **Cutroom input change:** a script linter computes words per beat and words/s. It flags ≤6-word lines in ≥3 s windows and flags a missing voice spec or "No subtitles.". A brand **pronunciation lexicon** table (written form → spoken form) is applied only inside `says:` quotes; captions keep the correct spelling.
- **Cheapest test:** a 4 s 480p/720p line test, 6 vs 10 words (2 cheap generations; audio is resolution-independent).

### 10. Drive lip-sync with a real voice recording (@Audio reference)
- **What/how:** on surfaces that accept an audio reference, an attached, rights-cleared **voice recording drives the mouth directly** instead of synthesizing a voice. Field reports call this the most reliable path, especially outside English.
  - An audio reference can have three jobs: *output* (plays as-is: timestamp-anchor it and remove all ambient/music tokens), *driver* (beat sync) or *performance*. Scope it to the one job you want, or it also lends its voice.
  - Higgsfield's Seedance `medias` roles include `audio` (per joebenscoter's `models_explore` output).
  - Record the VO on a phone in a real room. That also solves "AI voice" and room-tone realism at once.
- **Fixes:** F8.
- **Evidence:** OSideMedia `skills/higgsfield-audio/SKILL.md` § Voice-reference lip-sync path [FIELD — community seedance-2.0 v6.6.0]. **C/B**
- **Cutroom input change:** a `vo_recording` asset (phone-recorded, with consent), attached as `role: audio`. The script's spoken lines must match the recording.
- **Cheapest test:** 1 Seedance generation with an audio reference vs native TTS.

### 11. Realism layer: located imperfections, a capture pipeline stated as fact, no boosters
- **What/how:** the model's default attractor is the "polished commercial" look. Seven layers go **high in the prompt**, because clauses after ~8 requirements get deprioritized:
  1. Skin texture — *"visible pores around the nose and cheeks, natural slight unevenness, no filter quality"*
  2. Anti-polish in **positive** form — *"handheld phone camera feel, casual unsteady framing, filmed in a real environment, not a professional set"*
  3. Light in 4 axes: direction, quality, shadow behaviour, skin exposure — *"soft warm window light from camera-left, natural shadows across the face, no harsh highlights, skin illuminated without overexposure"*
  4. **3–4 named** clutter objects, e.g. "charger cable on the nightstand" (not "lived-in room")
  5. Breathing micro-shake — *"subtle handheld motion mimicking a propped-up phone… no static locked-off framing"*
  6. Emotional arc tied to visible cues
  7. Consistency + exclusions — *"maintain exact appearance from @Image 1, no drift, no deformation… no background music, no text overlay, no captions"*

  Other rules:
  - Name the **device/medium as a fact** ("a real phone video frame, auto-HDR off"), not "realistic".
  - Place imperfections at locations: "creases at the elbow bend, collar sitting slightly askew on the left".
  - **Ban boosters:** 4K, 8K, ultra-detailed, photorealistic, masterpiece, sharp focus, crisp, stunning, perfect, cinematic, professional, studio.
  - Camera-defect vocabulary is used in 23 phone-look cases: hand shake, focus hunting, exposure breathing, drifting composition, occasional accidental face cropping.
  - Arcads skin cue bank: pick 2–3. Avoid "acne/blemish"; *real ≠ dermatological*.
  - Seedance 2.0 sweet spot is **100–260 words**; >~150 words per block gets ignored.
- **Fixes:** F6, F7.
- **Evidence:** gbeyrouti `references/realisme-et-ugc.md`. smixs/visual-skills `image/references/de-slop.md`. arcads-claude-code `prompt-library/seedance-2-ugc.md` + `ugc-product-selfie.md` ("tested and approved"). LearnPrompt `handheld-ugc-vlog.md` (23-case corpus). **A−** (four independent libraries converge; none publishes A/B clips for our category)
- **Cutroom input change:** store **capture profiles** (iPhone front-cam selfie / phone propped on dresser / mirror selfie / friend filming) as prompt blocks with named imperfections. Store the real room's clutter inventory from the room photos. The linter removes booster words.
- **Cheapest test:** free prompt change; compare on the next NB still (≈1.5).

### 12. Framing caps and label rules
- **What/how:**
  - **Cap the tightest face framing at chest-up.** "Big close-ups expose AI faces"; the boyfriend-POV case bans faces filling the frame.
  - **Never hold a macro on printed text or labels.** Brand text is almost always rendered wrong. Keep tight shots off the print, use an unbranded surface, or cut to a real insert.
  - Decompose the product lock into parts (shape, material, colour, hardware, proportions), like the sunglasses review.
  - End on the two-part hero beat: **product alone in frame, then creator holding it to camera**. All 16 ad-type cases in the corpus close this way.
  - Generated on-screen text is garbled, so leave a clean tail frame and add text in post.
- **Fixes:** F1, F2.
- **Evidence:** LearnPrompt `ugc-creator-review.md`, `handheld-ugc-vlog.md`, `product-commercial-shotlist.md`. **B**
- **Cutroom input change:** the shot planner rejects `framing < chest-up` for talking beats and rejects `macro` on any product region tagged `print/logo/label` unless that shot is `source: real_insert`.
- **Cheapest test:** 0.

### 13. Motion discipline: one move, a named endpoint, real-time speed
- **What/how:**
  - **One dominant camera motion per shot.** Compound moves go in timed phases ("rises 0–3 s, holds, pushes in 4–8 s").
  - **Name the endpoint** of every camera move.
  - Chain **2–3 same-direction actions** so the motion fills the clip. Otherwise "action-reversal fill" happens: the model plays the action backwards to use up time.
  - **Ban slow motion by name and state "real-time speed"**. Models reach for slow-mo on their own, and that is the floaty look.
  - Walking: *"heel lands first, strict left-right alternation, one foot always on the ground"*.
  - Name adjacent-object invariants: *"the poster stays flat on the wall; only the hoodie moves"*.
  - Open mid-action. Frame one carries state, not setup.
- **Fixes:** F6, F7.
- **Evidence:** OSideMedia FAILURE-MODES (action-reversal [EMPIRICAL — dramaclaw corpus]; walking [FIELD — RED FLAG 2026-08-19]; physics-state anchor), `VFX-PIPELINE.md` (open mid-action). smixs `universal-rules.md` ("do not stack three camera moves in a 5-second clip"). **B**
- **Cutroom input change:** shot schema has a single `camera_move` enum + `endpoint` + `speed: real-time`, plus `invariants[]` taken from the room inventory.
- **Cheapest test:** 0 (lint).

### 14. Storyboard sheet: how the validated pipeline does it
- **What/how:**
  - joebenscoter's validated pipeline uses **one 16:9 NB Pro image holding three 9:16 panels** (Tight hook / Macro hands-on-product / Wide recommendation), with the character and product as references.
  - It passes that sheet + portrait + product as three `image` refs to one Seedance call: 720p, 15 s, audio on.
  - Gate: "three distinct panels, same face, same product; if two panels look alike, regenerate".
  - Caveats from gbeyrouti: a storyboard conveys **order and approximate composition, not a literal panel reproduction**. Say *"Read it left to right; do not use the grid's line-art, labels or placeholder characters."* Independent images align better than a collage.
- **Fixes:** F1, F2, F9.
- **Evidence:** joebenscoter `GUIDE.md` + `skills/ugc-storyboard-sheet/SKILL.md` (validated 2026-06-22). gbeyrouti `references-et-modes.md`. **B** (they partly conflict; see Open questions)
- **Cutroom input change:** the storyboard gate (already planned) stores a `sheet_mode: grid | separate` field so the two can be A/B'd.
- **Cheapest test:** ≈1.5 for the sheet + 2 videos for the A/B.

### 15. Resolution and credit hygiene
- **What/how:**
  - For phone-selfie UGC, **720p (~67 credits) looked no different from 1080p (~135)**. The render is audio-bound, so 720p is not faster. There is no "draft then final" two-step because audio is resolution-independent.
  - Always run a `get_cost` preflight.
  - **Mine failed takes.** A "failed" Seedance clip usually has 1–3 s of usable footage; bank those as inserts.
  - **Frame-level review is mandatory**: one bad frame kills a cut, so budget 30–60 s of scrubbing per 10 s clip.
  - Log **every** generation with a verdict, successes included. Without the denominator you can't get takes-per-kept per shot type. Production-grade AI cinema ran at ~1% image / 1.5% video acceptance.
- **Fixes:** F9.
- **Evidence:** joebenscoter `skills/ugc-video/SKILL.md` § Resolution (validated 2026-06-22). OSideMedia FAILURE-MODES (salvage, frame review; Cannes feature) + `DISCIPLINE.md` (ledger, "5-second rule" for logging). **B**
- **Cutroom input change:** default 720p. The ledger row per generation holds shot type, model, cost, verdict, failure codes and salvage in/out points. The UI shows predicted takes-per-kept by shot type.
- **Cheapest test:** 0.

### 16. Finish: roughen, don't polish
- **What/how:** the prompt gets you to ~90%; the last 10% is post, about **2–3 min per reel**:
  - an **extra shake layer** (generated micro-shake is too regular)
  - **light grain at low intensity**
  - a **warm iPhone grade** (the model's colour science is too neutral)
  - trending audio added in post
  - **native captions in post, never burned in by the model**

  Do **not** upscale UGC with generative upscalers. SeedVR2 "hallucinates plausible detail", which pushes toward the clean AI look, and 720p already matches 1080p for this format. Grain should follow exposure, not float uniformly (ComfyUI-Optical-Realism's key point). A phone sensor gives colour noise in shadows plus smeared noise reduction, not film grain. That node's bokeh/halation presets are a *film* look; skip them for phone UGC.

  Concrete ffmpeg starting point (my construction, tune by eye):
  ```
  ffmpeg -i in.mp4 -vf "crop=iw-48:ih-86:24+9*sin(2*PI*t*0.9)+4*sin(2*PI*t*2.3):43+7*sin(2*PI*t*0.7)+3*sin(2*PI*t*1.9),scale=1080:1920:flags=bicubic,colortemperature=temperature=5600:mix=0.35,noise=c0s=5:c0f=t+u:c1s=3:c1f=t:c2s=3:c2f=t,unsharp=5:5:0.35:5:5:0,format=yuv420p" -c:v libx264 -preset slow -crf 22 -c:a aac -b:a 128k out.mp4
  ```
  - Irregular two-frequency sine crop = extra handheld drift.
  - Temporal chroma + luma noise = sensor noise.
  - Mild unsharp = phone sharpening halo.
  - Then let the platform recompress.
- **Fixes:** F6.
- **Evidence:** gbeyrouti `realisme-et-ugc.md` § post-production (**B**). skatardude10/ComfyUI-Optical-Realism README (2026-04, **C** for phone use). WaveSpeed SeedVR2-vs-Topaz write-up, from the search summary (**C**). ffmpeg chain = **C**.
- **Cutroom input change:** a `finish_profile` per capture profile (shake amplitude/frequencies, noise strengths, WB shift) that is applied deterministically. No upscaler node in the UGC path.
- **Cheapest test:** 0 credits. Run a blind 10-person A/B, raw vs finished, on 3 existing clips.

### 17. Garment fidelity before video: open-source virtual try-on (license-checked)
- **What/how:** when a garment keeps drifting, make the **keyframe of the creator wearing the exact SANTO garment** with a try-on model, then animate from that still.
  - **FASHN VTON v1.5** is the only permissively licensed option: Apache-2.0, released 2026-01-27. It is maskless and pixel-space, takes a **flat-lay or on-model garment photo**, has categories `tops|bottoms|one-pieces`, and runs in ~5 s on an H100 or ~2 GB weights locally. CLI flags: `--garment-photo-type`, `--num-samples`, `--guidance-scale` (default 1.5), `--num-timesteps`.
  - A ComfyUI node exists: drphero/ComfyUI-FASHN-VTON (2026-02).
  - **CatVTON, IDM-VTON, OOTDiffusion and CatV2TON (video try-on, 256/512 px) are all CC BY-NC-SA 4.0: not for commercial ads.**
  - Higgsfield also has "UGC Virtual Try On" and "Pro Virtual Try On" presets in Marketing Studio, which are worth comparing.
- **Fixes:** F2, F5.
- **Evidence:** fashn-AI/fashn-vton-1.5 README + `examples/basic_inference.py` (read). LICENSE files of the others (read). OSideMedia `skills/higgsfield-marketing-studio/SKILL.md` (preset list). **B** for the tool; untested on hoodies, fleece or leggings in motion.
- **Cutroom input change:** the product kit requires a **flat-lay per garment on a plain background** (front + back). Add a try-on step: `identity_plate body shot + flat-lay → try-on still → QA (§ Auto-QA) → video`.
- **Cheapest test:** free on a local or rented GPU (≈$1): 3 garments × 4 samples.

### 18. Lip-sync post-fix + sync gate
- **What/how:**
  - **LatentSync 1.6** (ByteDance, Apache-2.0, 512 px, **18 GB VRAM**). `inference_steps` 20–50. `guidance_scale` 1.0–3.0: higher improves sync but "may cause distortion or jitter".
  - It ships `eval/eval_sync_conf.sh` (SyncNet confidence). Its own data filter drops clips with **sync confidence < 3**, so use the same threshold as a QA gate.
  - **MuseTalk** (MIT, ~30 fps on V100) is the fast fallback.
  - Use this path when a generated take is perfect except the mouth, or to lay a real recorded VO onto a silent take.
- **Fixes:** F8, F9.
- **Evidence:** bytedance/LatentSync README (read; last commit 2025-06-20; ~5.9k stars per sync.so). TMElyralab/MuseTalk (MIT, 2025-09). **B**
- **Cutroom input change:** store `sync_conf` per take. The re-sync step runs only on takes with good picture but sync < 3.
- **Cheapest test:** free (local GPU): run the eval script on 5 existing takes.

### 19. Relight composited stills; post face repair (secondary tools)
- **What/how:**
  - **IC-Light** (Apache-2.0; last commit 2025-02; SD1.5-based) has a **background-conditioned** mode. Relight a real product or person cut-out into the room photo's light before animating. This kills the "sticker" look of pasted products.
  - For single drifted faces in an otherwise good take: vrgamedevgirl's FaceFix node set (active 2026-09-23) **detects and tracks the face → re-renders only the crop (LTX) → composites back**. FaceFusion (OpenRAIL-AS; active 2026-09-13) is the heavier alternative. Use either only on your own synthetic creator.
  - HandRefiner (2024, SD1.5 depth-ControlNet; the authors warn strength 1.0 loses texture) is superseded by a one-line NB edit on the still.
- **Fixes:** F1, F2, F6, F7.
- **Evidence:** READMEs read. **C** for this use case.
- **Cheapest test:** free local runs on 2 stills.

---

## Repos worth using

| Repo | Recency (last commit) / signal | What it gives us | How to plug into Cutroom |
|---|---|---|---|
| [OSideMedia/higgsfield-ai-prompt-skill](https://github.com/OSideMedia/higgsfield-ai-prompt-skill) | 2026-08-22; 32 sub-skills; tags each rule MEASURED / FIELD / UNPROVEN | Seedance failure-mode catalog (babble, mimed manipulation, third hand, action reversal, FPS drift), Higgsfield Studio field notes (untouched base, sheet-is-not-a-menu, scale law, model-per-asset) | Port `FAILURE-MODES.md` § Self-repair checklist into the prompt linter; map each failure to F-codes in the rejection taxonomy |
| [LearnPrompt/awesome-seedance](https://github.com/LearnPrompt/awesome-seedance) | 2026-09-24 (synced daily); 497 verified cases, 264 cross-model retests (193 ✅ / 68 ⚠️ / 3 ❌), >$300 of retest spend | 25 templates distilled from cases, each with pitfalls (UGC review, handheld vlog, reference lock, fashion lookbook) | Seed the golden-shot library from retested ✅ cases; use the pitfalls as linter rules |
| [gbeyrouti/seedance-prompting-claude-skill](https://github.com/gbeyrouti/seedance-prompting-claude-skill) | 2026-08-10 (French docs, English prompts) | Negation rule (negate sources/tracks/defects, never visible objects), 7-layer realism block, @reference role syntax, symptom → fix matrix, pre-delivery checklist | Base template for the Seedance prompt compiler |
| [joebenscoter86/higgsfield-ugc-workflow](https://github.com/joebenscoter86/higgsfield-ugc-workflow) | 2026-06-23; run on Higgsfield MCP with validated numbers | Person-only portrait → 3-panel storyboard → one Seedance call; cost gate; 720p default; VO pronunciation lexicon | Closest existing twin of Cutroom's flow; copy the cost-gate and lexicon patterns |
| [krusemediallc/arcads-claude-code](https://github.com/krusemediallc/arcads-claude-code) | 2026-09-22; Arcads (commercial UGC vendor) workspace | 9-layer Seedance UGC formula, skin cue bank, forbidden words, reference ordering for NB (identity first, ≤3 style refs), `analyze-video` (ffmpeg frames + Whisper → template) | Use `analyze-video` to turn real SANTO-competitor TikToks into templates |
| [useapi/google-flow-api](https://github.com/useapi/google-flow-api) `ugc-product-video/` | 2026-09-21 | Four-view 2×2 product sheet prompt; start = end hub-frame clips; checkpointed resumable pipeline (`ugc_state.json`); trim-to-sound | Copy the checkpoint/resume design so a crash never re-pays for clips |
| [smixs/visual-skills](https://github.com/smixs/visual-skills) | 2026-09-16 | `de-slop.md` (beautification prior table, located imperfections, booster ban); Kling `cfg_scale` 0.7–1.0 for product work; Kling negative field takes positive nouns | Kling routing notes; image de-slop checklist |
| [charlesdove977/UGC-Factory](https://github.com/charlesdove977/UGC-Factory) | 2026-06-29 | Higgsfield Elements with angle sets + environment element; "never blank script" | Element registration pattern. **Ignore its genre style skills** (generic; invented specs such as "99% sRGB") |
| [aditya10/Spotlight](https://github.com/aditya10/Spotlight) | 2026-06-25; ECCV 2026; dataset on Seedance/Veo3/LTX-2 videos | VLM prompts for error detection and localization (6 types; multi-agent, sliding-window, merge) | Auto-QA VLM pass after generation |
| [fashn-AI/fashn-vton-1.5](https://github.com/fashn-AI/fashn-vton-1.5) | 2026-01 release; **Apache-2.0** | Maskless try-on from flat-lay | Garment keyframe step (Technique 17) |
| [bytedance/LatentSync](https://github.com/bytedance/LatentSync) | 2025-06-20; ~5.9k stars (sync.so) | Lip re-sync + SyncNet confidence script | F8 fix + sync gate |
| [Vchitect/VBench](https://github.com/Vchitect/VBench) | 2026-08-21 | `--mode=custom_input` for subject_consistency (DINO), background_consistency (CLIP), motion_smoothness, dynamic_degree | Post-video drift scores. **Don't gate on aesthetic/imaging quality** |
| [deepinsight/insightface](https://github.com/deepinsight/insightface) | 2026-09-09 | ArcFace face embeddings | Face-drift metric. **Pretrained models are non-commercial research only**; see Open questions |
| [google-ai-edge/mediapipe](https://github.com/google-ai-edge/mediapipe) | 2026-09-24 (Apache-2.0) | Hand Landmarker (21 points per hand), face detection | Hand-count and hand-scale checks per frame |
| [facebookresearch/dinov2](https://github.com/facebookresearch/dinov2) + [facebookresearch/sam2](https://github.com/facebookresearch/sam2) / [IDEA-Research/GroundingDINO](https://github.com/IDEA-Research/GroundingDINO) | 2026-06 / 2024-12 / 2024-08 | Text-prompted product crop + embedding similarity | Product-drift metric (Auto-QA) |
| [PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) | 2026-09-16 | OCR | Logo-text check + burned-in-subtitle detector |
| [hzwer/Practical-RIFE](https://github.com/hzwer/Practical-RIFE) | 2026-08-27 (MIT) | Frame interpolation | Only to repair duplicate-frame (FPS-drift) B-roll; never on hero shots |
| [lllyasviel/IC-Light](https://github.com/lllyasviel/IC-Light) | 2025-02 (Apache-2.0) | Background-conditioned relight | Relight pasted product/person into room photo before video |
| [vrgamegirl19/comfyui-vrgamedevgirl](https://github.com/vrgamegirl19/comfyui-vrgamedevgirl) | 2026-09-23 | FaceFix (track → crop → re-render → composite), film grain, colour match, video compare | Post face repair; finish nodes if Cutroom adopts ComfyUI |
| [skatardude10/ComfyUI-Optical-Realism](https://github.com/skatardude10/ComfyUI-Optical-Realism) | 2026-04-28 | Exposure-dependent grain, highlight roll-off, chromatic aberration (0.001–0.003), barrel distortion | Borrow the grain-by-exposure idea for the finish profile; skip the film/bokeh presets |
| [Emily2040/seedance-2.0](https://github.com/Emily2040/seedance-2.0) | 2026-09-08; has `evals/` + validation | Source of the per-language sync budgets and voice-reference path | Read `skills/seedance-audio` when building F8 |
| [chenhaoxing/Awesome-AI-Generated-Video-Detection](https://github.com/chenhaoxing/Awesome-AI-Generated-Video-Detection) | 2026-05-12 | Index of detection papers + code (NSG-VD physics, DeCoF, DeMamba/GenVideo) | Reference only |
| Non-commercial, avoid for ads: [Zheng-Chong/CatVTON](https://github.com/Zheng-Chong/CatVTON), [yisol/IDM-VTON](https://github.com/yisol/IDM-VTON), [levihsu/OOTDiffusion](https://github.com/levihsu/OOTDiffusion), [Zheng-Chong/CatV2TON](https://github.com/zheng-chong/catv2ton) | CC BY-NC-SA 4.0 (LICENSE files read) | — | Research comparison only |
| Low value: AKCodez/higgsfield-claude-skills (2026-04, Playwright UI automation, prompts use "soft bokeh"); drinkyouroj product-to-ad ("product… with one hand, phone in the other"); n8n Automated-UGC-Ad (asks for "shallow depth of field" + "sharp focus" + "cinematic") | — | Examples of the anti-patterns in STOP DOING | — |

---

## Auto-QA checks we could run for free before or after paying for video

Design principle: **deterministic metrics gate; the VLM triages; a human decides.** Spotlight (ECCV 2026) found humans beat the best VLMs by **~2×** at localizing errors in Seedance and Veo3 output. Its dataset shows **adherence and physics errors are most common and last longest**, while appearance/disappearance and body-pose errors are short, which argues for per-frame scoring rather than a single summary.

### Before paying (on the keyframe or still, the prompt and the references): all free/local
1. **Prompt linter** (text only, 0 cost). Checks:
   - words/s per spoken beat; ≤6-word lines in ≥3 s windows
   - voice-spec line present; `No subtitles.` present
   - negation of a visible object (regex for `no <noun>` outside the allowed families: music, captions, text, drift, deformation, flicker)
   - booster words
   - >1 camera move, or no endpoint
   - a visible non-speaker without a mouth state
   - every attached reference has a role and inherit/exclude lines
   - >~150 words per block or >8 requirements
   - two-handed product action while `camera_holder=selfie`
   - macro on a print/logo region
   - (Sources: gbeyrouti checklist, OSideMedia Self-repair checklist, Arcads adaptation checklist.)
2. **Face identity vs plate.** ArcFace embedding cosine between the still's face and `identity_plate`. Reject below a threshold calibrated on ~20 approved vs ~20 rejected Cutroom stills (see Open questions). Fixes F1.
3. **Product fidelity.** GroundingDINO or SAM2 crop with the text prompt ("black hoodie", "grey mailer bag"), then:
   - DINOv2 cosine vs the product-kit crops of the same state (VBench also uses DINO for subject consistency);
   - mean **ΔE2000** in Lab on the garment mask vs the kit swatch, measured under the grey-card-corrected photo;
   - **OCR** of the logo region: must equal "SANTO" or be empty (empty passes; garbled text fails).
   - Fixes F2.
4. **Hands.** MediaPipe Hand Landmarker:
   - hands ≤ 2 per person;
   - if `selfie`, at most one hand in frame, touching product;
   - **hand-length ÷ face-height ≈ 0.9–1.1**. Anthropometric heuristic (**C**); outside ~0.7–1.4 flags giant or tiny hands.
   - Landmarker always fits 5 fingers, so it can't count bad fingers. Send the **hand crops** to a VLM with one narrow question: "count fingers on each hand; are any fused, bent backwards, or missing?"
   - Fixes F3.
5. **Scale.** Product-box height ÷ face-box height vs the ratio expected from real dimensions (Technique 6). Fixes F3.
6. **Narrow VLM questions on the still**, Spotlight multi-agent style (one call per error type). Questions: "Is a phone, selfie stick or mirror-camera visible?" "List every object not present in reference images 1–4." "Is there any jewellery, tattoo or accessory not in @Image 1?" Fixes F7, F1.

### After paying (on the video): all free/local
7. **Per-frame identity curve.** ArcFace on every 3rd frame: report the minimum and the standard deviation, and flag dips during head turns. Fixes F1 within-shot drift.
8. **Per-frame product curve.** DINOv2 on the tracked product crop (SAM2 video propagation), plus ΔE per frame. Fixes F2 drift after ~10 s (gbeyrouti: "drift appears typically after ~10 s").
9. **VBench `custom_input`**: `subject_consistency`, `background_consistency` (F7 room warps), `motion_smoothness`, `dynamic_degree`. **Don't gate on `aesthetic_quality` or `imaging_quality`**: they reward the polished look we are trying to avoid.
10. **Hand-count time series.** A spike to 3 hands, or hands flickering in and out = the third-hand or merge event. Output the timestamps for human review. Fixes F3.
11. **Duplicate-frame / FPS-drift check.** `ffmpeg -vf mpdecimate` drop count, or frame-hash runs. OSideMedia: Seedance pads with repeated frames under load. Hero shots with dupes → re-generate; B-roll → de-dup + RIFE. Fixes F6, F9.
12. **Audio vs script.** Whisper transcript vs script word diff catches filler-babble, doubled lines and dropped words; it can't reliably judge brand pronunciation, which stays a human listen. Add **SyncNet confidence ≥ 3** (LatentSync `eval/eval_sync_conf.sh`). Fixes F8.
13. **Unwanted music.** Run an audio-event classifier (e.g. PANNs/YAMNet, **C**) when the prompt said "no music". Kling "lays music even against a negative prompt" (smixs), so for Kling, strip audio instead. Fixes F8.
14. **Burned-in text.** OCR on 1 fps: any text in a clip whose prompt asked for none → reject or crop.
15. **Beat and cut check.** PySceneDetect: cut count and timings vs the shot plan. Kling 3.0 merges shots whose framing and angle match. Fixes F9.
16. **VLM sliding-window pass** (Spotlight `WINDOW_PROMPT` + `MERGE_PROMPT`, 2–3 s windows) on the error types physics / appearance-disappearance / logical / motion / anatomy / adherence. Its output **only decides which seconds a human scrubs first**; it never auto-accepts.
17. **Salvage marker.** Any segment ≥1.5 s where checks 7–14 all pass gets auto-banked as an insert candidate (Technique 15).

---

## AI-detection signals → countermeasures

Research context:
- **Human** spotters on r/RealOrAI rely mainly on **perceptual cues** (scene, visual artifacts, anatomy/physics, lighting, behaviour, text, audio): **70%** of reasoning, with provenance at 4% (arXiv 2605.24287).
- Forensic **detectors** are brittle. VidAudit (arXiv 2606.31004) found a 3-feature **clip-length** classifier hits AUC 0.998 on GenVidBench, and at a 0.1% false-positive rate "multiple high-AUC methods fall to single-digit recall".
- So optimise for human perception, not detector evasion.
- Taxonomies used: Skyra (CVPR 2026) L2 = colour/light anomaly, texture anomaly, motion forgery, object inconsistency, interaction inconsistency, violation of causality, violation of commonsense, unnatural movement. Spotlight (6 types). Artifact-Bench (30 fine-grained types: surface / structural / temporal-semantic).

| Detection signal (source) | Countermeasure on the input side | Countermeasure at finish/QA | F |
|---|---|---|---|
| **Texture anomaly: poreless, waxy skin; uniform clean surfaces** (Skyra; r/RealOrAI "lighting and textures on skin and clothes") | Located skin imperfections high in the prompt; untouched identity plate (no re-passes); capture medium stated as fact; no boosters; no generative upscaling | Exposure-dependent sensor noise, mild sharpening halo, platform recompression | F6 |
| **Colour/light anomaly: subject lit differently from the room; perfect balanced light; blue shift on stills** (Skyra; OSideMedia image-stage tells) | Light in 4 axes, one source; one light logic (don't mix "4K cinematic" with handheld); IC-Light relight for composited stills; Soul Cinema for location plates | Warm phone grade; ΔE check on garment; grey-card-corrected product kit | F6, F2 |
| **Texture crawl / high-frequency flicker over time** (noise-amplification and native-scale detectors; gbeyrouti flicker definition) | Avoid fine repeating patterns in generated backgrounds (mesh, small check, dense text); keep small SANTO prints out of long tight shots; use real inserts for print detail | Temporal grain slightly masks residual crawl (**C**); VBench background_consistency flag | F7, F2 |
| **Object appearance/disappearance, identity inconsistency** (Skyra L3; Spotlight) | Environment element / room plate with "do not use the people"; named invariants; explicit "absent from source keyframe" clause when something must appear; per-state sheets | Per-frame DINO/CLIP background + ArcFace curves | F1, F7 |
| **Interaction inconsistency / violation of causality: hands don't change the object; bag never opens** (Skyra; Spotlight: physics and adherence errors dominate) | Causal-chain manipulation; completion states; two-states-plus-sound route; one fine manipulation per beat | VLM "did the object change state?" question; human scrub | F4, F3 |
| **Anatomy: extra or merged fingers, third hand, impossible grips** (Spotlight anatomy; r/RealOrAI anatomy) | Hand headcount + ownership + entry point; camera-holder rule; chest-up cap; hands at rest when not acting | MediaPipe hand-count series + VLM finger check on crops | F3 |
| **Unnatural movement: slow-mo float, gliding walk, there-and-back motion** (Skyra "unnatural movement"; OSideMedia) | "Real-time speed", slow-mo banned by name; walking-cycle clause; 2–3 same-direction actions; named camera endpoint; 1 camera move | Duplicate-frame check; extra irregular shake layer | F6 |
| **Kinematic mismatch between facial regions; lip/eye desync** ("Beyond Flicker", arXiv 2512.04175) | Line length 8–12 words per 4 s; mouth state for non-speakers; voice-reference audio; no extreme face close-ups | SyncNet ≥3 gate; LatentSync re-sync | F8, F1 |
| **Text garbled** (r/RealOrAI "text") | Never request text; "No subtitles"; no macro on labels | OCR burned-in check; captions in post | F2 |
| **Audio tells: silence, stock music bed, flat TTS, filler-babble** (r/RealOrAI "audio") | Audio exclusions; "phone mic, quiet room tone"; real recorded VO as @Audio; phonetic lexicon | Whisper diff; music classifier; add real room tone | F8 |
| **Compositional polish: centred, symmetric, tidy, 85 mm bokeh, idealised casting** (smixs beautification-prior table) | Named clutter; off-centre and tilted framing; deep phone DOF (never "shallow depth of field"); ordinary casting; capture profile per shot | — | F6, F7 |
| **Missing sensor/compression signature** (bit-plane and noise detectors) | — | Finish noise + re-encode. **Do not strip provenance metadata or AI labels.** Platforms (TikTok/Meta) label AI content and EU AI Act Art. 50 transparency duties apply from Aug 2026 (verify for SANTO's markets). The goal is believable craft, not undisclosed deception. | F6 |

---

## STOP DOING
1. **Putting the product in the base character portrait** (causes drift in storyboard and video; joebenscoter).
2. **Negating visible things** ("no blur", "no makeup", "no red car"). Negate only sources, generated tracks and defects: "no background music, no captions, no drift" (gbeyrouti).
3. **Booster words**: 4K, 8K, ultra-detailed, photorealistic, masterpiece, cinematic, professional, stunning, perfect, studio, sharp focus (smixs, Arcads forbidden list).
4. **Mixing light logics.** "Handheld authentic" + "cinematic 4K lighting", or "shallow depth of field" + "sharp focus" (as in the n8n template), "lands in plastic territory" (LearnPrompt).
5. **Default Kling negative lists that include "shaking camera"** on UGC shots. They kill handheld. Also, Kling's negative field wants positive nouns, not "no X" (smixs).
6. **Rich all-states sheets.** "Presence beat proportion"; the model shows whatever is on the sheet (OSideMedia).
7. **Re-prompting a whole sheet or re-rolling an unchanged prompt** to fix a small flaw. Use a one-line NB edit, and change one variable at a time.
8. **≤6-word lines in 4 s windows** (babble), and long run-on VO lines (sync slips; cut words, don't add lip-sync adjectives).
9. **Generating on-screen text, slogans or captions**, and holding macros on printed labels.
10. **Walk + fine manipulation in one beat**, and stacked camera moves.
11. **Paying for 1080p or upscaling UGC** "for quality". No visible gain; generative upscalers add AI-clean detail.
12. **Gating on aesthetic or imaging-quality scores** (VBench aesthetic/imaging, LAION aesthetic). They reward the look we are removing.
13. **Using CatVTON, IDM-VTON, OOTDiffusion or CatV2TON in production ads** (CC BY-NC-SA). InsightFace pretrained weights are also non-commercial research only.
14. **Importing generic genre "style skills"** (UGC-Factory / AKCodez ecommerce, fashion): marketing prose with invented specs, and they push the polished look.
15. **Prompting a phone *and* two busy hands** ("holds product in one hand, phone in the other" while also opening something).

---

## Open questions (cheapest resolving test in brackets)
1. **Grid storyboard vs separate images vs a 2×2 product sheet.** joebenscoter validated a 3-panel sheet. gbeyrouti says independent images align better than a collage. useapi uses a 2×2 four-view sheet. Which binds SANTO garments best on Seedance via Higgsfield? [3 Seedance generations, same shot]
2. **Seedance credit cost.** The BRIEF says ~18; joebenscoter logged ~67 at 720p/15 s with audio and ~135 at 1080p. Is it duration, audio or tier? [`get_cost` preflight only: 0 credits]
3. **Does Higgsfield's Seedance honour an `audio` media role as a lip-sync driver** for a user-recorded VO, and does it keep the phone-mic timbre? [1 generation]
4. **ArcFace threshold and licence.** The same-person cosine threshold must be calibrated on Cutroom's own approved/rejected set. InsightFace weights are non-commercial: is internal QA acceptable, or do we swap in a commercially licensed face embedder or a VLM identity judge? [0 credits: offline calibration]
5. **FASHN VTON on streetwear.** Does it hold hoodie drawcords, fleece pile and legging seams, and do those details survive Seedance animation from the try-on still? [free try-on + 1 video]
6. **Measured babble rule on Seedance 2.x via Higgsfield at 720p** (the source measured Seedance 2.0 at 480p on another lane). [2 cheap 4 s generations]
7. **Does the finish profile (grain, shake, grade) measurably raise "real" ratings?** [0 credits: blind A/B with 10 viewers on 3 clips]
8. **How much VLM triage saves in human scrub time** on our own failures, given Spotlight's 2× human advantage. [0 credits: run the Spotlight prompts on 20 archived takes vs human labels]

---

## Sources read (repos cloned or raw files)
- github.com/joebenscoter86/higgsfield-ugc-workflow: GUIDE.md, skills/*/SKILL.md, examples/surfboards/script.md
- github.com/gbeyrouti/seedance-prompting-claude-skill: README, references/realisme-et-ugc.md, debug-et-limites.md, references-et-modes.md
- github.com/charlesdove977/UGC-Factory: frameworks/seedance-elements.md, character-creation.md, stitching-broll.md, styles/13, 07
- github.com/LearnPrompt/awesome-seedance: README (retest stats), docs/templates/en/{ugc-creator-review, handheld-ugc-vlog, character-reference-lock, fashion-lookbook, product-commercial-shotlist}.md
- github.com/OSideMedia/higgsfield-ai-prompt-skill: DISCIPLINE.md, skills/higgsfield-seedance/FAILURE-MODES.md, skills/higgsfield-seedance-2-5/VFX-PIPELINE.md, skills/higgsfield-soul/SKILL.md, skills/higgsfield-audio/SKILL.md, skills/higgsfield-marketing-studio/SKILL.md
- github.com/krusemediallc/arcads-claude-code: prompt-library/seedance-2-ugc.md, ugc-product-selfie.md, kling-3.md, veo-3-1.md, analyze-video/SKILL.md
- github.com/smixs/visual-skills: image/references/de-slop.md, video/references/kling.md, fixes-and-skeletons.md, universal-rules.md
- github.com/useapi/google-flow-api: ugc-product-video/README.md, prompts.json
- github.com/anirudhaeran/Automated-UGC-Ad (n8n JSON prompts); github.com/myccarl/ai-shortVideo-pipeline (CLIP gate, threshold 0.22 Chinese-CLIP)
- github.com/aditya10/Spotlight: README, prompts/*.py
- github.com/fashn-AI/fashn-vton-1.5 (README, examples); github.com/Zheng-Chong/CatV2TON (README); LICENSE files of CatVTON, IDM-VTON, OOTDiffusion, IC-Light, PuLID, LatentSync, MuseTalk, FaceFusion, RIFE, SeedVR2 node; insightface README licence section
- github.com/bytedance/LatentSync README; github.com/Vchitect/VBench README; github.com/lllyasviel/IC-Light README; github.com/wenquanlu/HandRefiner README; github.com/skatardude10/ComfyUI-Optical-Realism readme; github.com/vrgamegirl19/comfyui-vrgamedevgirl README; github.com/chenhaoxing/Awesome-AI-Generated-Video-Detection README
- Papers (via search summaries): Spotlight arXiv 2511.18102; Skyra arXiv 2512.15693 (CVPR 2026); VidAudit arXiv 2606.31004; Artifact-Bench arXiv 2605.18984; BrokenVideos arXiv 2506.20103; r/RealOrAI arXiv 2605.24287; Noise Amplification arXiv 2606.16742; Beyond Flicker arXiv 2512.04175

---

# PART 8 — `06-winning-ads-courses.md`

## 06 — Winning apparel ads, courses/communities, prompt→output structures

Researcher scope: (A) what winning apparel/UGC ads look like shot by shot, (B) what courses, communities and contests teach, (C) documented prompt→output structures we can copy.
Method: about 45 WebSearch queries (WebFetch and curl are blocked for almost every domain), plus **free, read-only** Higgsfield MCP calls (`get_preset_instructions`, `get_workflow_instructions`, `get_workflow_bundle_file`). **No credits were spent.**

> **The main find:** Higgsfield's MCP server ships its own internal production recipes for `ugc-try-on-video`, `ugc-unboxing-video`, `ugc-review-video`, `ugc-product-video` and others. They are versioned (try-on v1.0) and include exact model routing, timings per cut, prompt skeletons, banned-word lists and a QA checklist. This is the vendor's own "golden path" for exactly our use case. It is a stronger source than any third-party course. I saved the raw files to `research/hf-workflows/` (`tryon-clip.md`, `tryon-board.md`, `ugc-character.md`, `unboxing-clip.md`). Several techniques below come from them, marked **[HF-WF]**. Evidence strength for these is **A (official vendor doc)**. Note: they encode what Higgsfield *prescribes*, not a published A/B result.

---

## Part A — What winning apparel UGC actually looks like (evidence digest)

| Finding | Number / specifics | Source | Strength |
|---|---|---|---|
| Ad recall is decided early | 90% of ad-recall impact lands in the first 6 s. TikTok recommends a hook → body → close structure | TikTok Creative Codes https://ads.tiktok.com/business/en-US/creative-codes | A |
| Key message and product appear early | 63% of the highest-CTR TikTok ads show the key message or product within the first 3 s | TikTok research, cited in https://sink-or-swim-marketing.com/blog/tiktok-creative-center-best-practices-hook-retention-2025/ and https://www.mbadv.agency/tiktok-ads/creative-best-practices | B |
| Fashion-specific hook guidance | TikTok's own fashion tips: highlight price or promotion in the first 3 s. Hook types: hacks/tips, price, audience call-out, unbox/comparison/question, lists, reviews, product features | https://ads.tiktok.com/business/creativecenter/quicktok/online/creative-tips-fashion-apparel/pc/en ; https://ads.tiktok.com/business/creativecenter/quicktok/online/Fashion_2024/pc/en | A |
| Product on body in the first 2 s; state size | Try-on hauls: show the garment on a body within 2 s. The creator states their measurements and the size worn within 15 s | https://www.influencers-time.com/try-on-haul-optimization-the-brief-that-cuts-return-rates/ | C |
| Length | 9–15 s is the sweet spot for fashion (claimed +25% watch-through). Meta counts a ThruPlay at 15 s, so a 15 s ad completes as a full ThruPlay | https://www.picjam.ai/blog/how-long-should-a-tiktok-ad-be ; ThruPlay benchmarks https://www.get-ryze.ai/blog/meta-video-ad-benchmarks-thruplay-hook-and-hold-rate-2026 | C |
| Cut rhythm | New visual every 2–3 s; static shots over 5 s lose viewers. Average TV-ad scene length is about 2 s. Editors aim for clips of 1.5–3.5 s and cut pauses over 0.3 s | https://www.picjam.ai/blog/how-long-should-a-tiktok-ad-be ; https://afterhourscreatorclub.com/guides/how-to-edit-ugc-videos/ ; https://www.usetwirl.com/ugc-diaries/editing-dos-and-don-ts-elevating-your-ugc-content-quality | B/C |
| Text is near-universal | 86% of TikTok ads use text boxes and 71% use text overlays. Voiceover appears in only 39% of ads but gives stronger recall; VO drove 71% higher recognition than ASMR audio | TikTok "Power of Creative Elements" https://ads.tiktok.com/business/creativecenter/quicktok/online/Power_Creative_Elements/pc/en (via search summary) | A |
| Sound and captions on Meta | Music or VO in Reels gives up to 13% more incremental conversions. Captions add about 12% view time | https://www.socialmediatoday.com/news/meta-shares-tips-on-reels-hooks-creative-diversification-in-ads-and-threa/808182/ ; https://benly.ai/learn/meta-ads/meta-ads-reels-ads-guide | B |
| Hook and hold targets | Meta hook rate (3 s views / impressions): 25% healthy, 30%+ good, 35–45% elite. **Apparel should clear 30% before scaling.** Hold rate target is 20–25% or more | https://sepia-lab.com/en/blog/hook-rate-benchmarks ; https://www.sparkugc.com/resources/hook-rate-benchmarks-2026 | B |
| Format choice in fashion | Motion 2026 ($1.29B spend, 578k creatives): **the top Meta format for Fashion & Apparel is "Post-It"**, with Meme also in the top 5. "Culturally fluent and playful visuals produce the most winners." Raw hit rate: text-only 11.6%, product image + text 8.75%, UGC 7.56%. Only about 5% of all ads become winners | https://motionapp.com/library/research/creative-benchmarks-2026/visual-formats-by-vertical ; https://adliftr.com/blog/ad-creative-testing-statistics-2026 | A (large dataset) |
| Which formats sell apparel | GRWM, haul reaction, styling challenge and OOTD convert best. For streetwear, **fit-check videos drive more purchases than unboxing** (unboxing drives engagement) | https://www.gethookd.ai/learn/4-tiktok-clothing-ads-examples-tips-for-2026/ ; https://www.veicolo-agency.com/post/streetwear-brand-growth | C |
| Skims format | Always the same grammar: mirror, phone, honest verdict. The audience learns to read it as a customer video. Note: mirrors are dangerous for AI (see STOP DOING) | https://www.thebrief.ai/blog/ugc-video-ads-guide-formats/ (via summary) | C |
| Gymshark | Video ads average about 25 s and are influencer-UGC heavy. The language is body-specific: "it hugs your body in the right places" | https://www.gomarble.ai/library/brands/gymshark/ | B |
| UGC fatigue | UGC holds efficiency for about 10–14 days, then CTR/CVR drop 25–40%. Studio creative lasts 18–25 days | https://www.finsi.ai/blog/ugc-ads-performance-benchmarks/ | C |
| AI UGC vs real UGC | CTR can match (1.5–3%). Real UGC is reported at 2.1–2.8x the 90-day ROAS of AI equivalents. Ipsos 2026 found human-made ads scored 14% higher short-term and 17% higher long-term. The pattern: use AI for hook testing, then reshoot the winners with a real person | https://inbeat.agency/blog/ai-ugc-ads-vs-real-ugc ; https://billo.app/blog/ai-generated-ads-performance/ | B/C |
| Hybrid beats pure avatar for basics | "Real product footage + AI voice-over outperforms pure avatar ads for apparel basics like t-shirts and activewear" | https://adlibrary.com/posts/ai-ugc-for-ecommerce | C |
| Pro AI-ad yield | PJ Accetturo's Kalshi NBA Finals spot took 300–400 Veo 3 generations for 15 usable clips (about 20–27 gens per keeper), 2–3 days, under $2k. He had Gemini write prompts 5 at a time ("more than that and quality slips"), and **every prompt described its scene completely, as if the model had no memory of other shots** | https://www.thedaringcreatives.com/creator-stories/pj-ace-nba-finals-ad/ ; https://www.yahoo.com/entertainment/articles/chaotic-kalshi-ad-during-nba-173937071.html | B |

---

## Techniques

### T1. Storyboard sheet → ONE multi-cut Seedance clip (8 beats, 7 internal hard cuts) [HF-WF]
- **How:** Don't generate 8 separate clips and stitch them. Higgsfield's own try-on pipeline works like this:
  1. Generate a character still with Soul 2 (3:4, 2k).
  2. Generate a **21:9 storyboard sheet** of **8 equal 9:16 vertical slots in one row**, thin white gutters, no text. Use `gpt_image_2` at 2k, quality high. Pass `medias` in the order [product, character, previous_board] and declare them in the prompt as `@Image1/@Image2…` in that same order.
  3. Run a mandatory "de-slop" pass on the board (T3).
  4. Make one `generate_video` call: `seedance_2_5`, `mode:"omni_reference"`, 9:16, 1080p, `generate_audio:true`, `medias:[board, character, product]` all with role `image_references`, duration 4–15 s.
  5. Mark every cut in the prompt with the literal string `Hard cut to.` (7 markers for 8 cuts). "Without them, cuts collapse into smooth motion."
  6. Clips longer than 15 s are chained as extra boards, and each new board is conditioned on the previous one. Stitch with `ffmpeg -f concat -c copy`, hard cuts only.
- **Rule the vendor stresses:** the board panels are *sequence and timing references only*. The text prompt must describe **motion inside each cut** (weight shift, breath, fabric settling), not caption the panel. "Repeating the panel composition in the text gives Seedance two identical signals and produces stiff, lifeless output."
- **Fixes:** F1, F2, F4, F7, F9 (one 18-credit call replaces 5–8 separate clips).
- **Evidence:** Higgsfield MCP `ugc-try-on-video` v1.0 SKILL.md and `references/ugc-try-clip.md` / `ugc-try-board.md` (saved in `research/hf-workflows/`). **A**
- **Input change for Cutroom:** add a "board" stage. Cutroom stores one 21:9 N-slot board per clip, with per-slot metadata (beat, POV, distance band, VO or lip-sync, hand roles). The video call sends board + character + product as omni references plus a timestamped cut list.
- **Cheapest test:** 1 board (gpt_image_2, cost unknown, roughly an image generation) + de-slop (Seedream, roughly an image generation) + 1 Seedance 2.5 clip at 15 s (~18+ credits). Total about 20–25 credits. Compare against our current multi-clip hoodie ad.

### T2. The "anti-morph" cadence: adjacent shots differ in BOTH POV and distance band [HF-WF]
- **How:** Label every slot/cut with a POV (SELFIE / STATIC / STATIC-CLOSE) and a distance band (TIGHT/MACRO, MID, WIDE/FULL-BODY).
  - **No two adjacent cuts may share both POV and band.** Sharing both is exactly what makes the model morph instead of cutting.
  - Each band appears at least twice across the 8 cuts.
  - Canonical try-on cadence: `SELFIE → STATIC → STATIC → STATIC-CLOSE → STATIC → STATIC-CLOSE → STATIC → STATIC`, with distance alternating MID → WIDE → WIDE(different distance) → MACRO → WIDE → MACRO → WIDE(new room) → MID/WIDE.
  - Every POV or distance change sits on a hard cut, never on a smooth move.
- **Fixes:** F1, F2, F4, F7 (the model hides discontinuities in cuts instead of morphing through them).
- **Evidence:** `ugc-try-board.md` § "POV & distance cadence — the anti-morph engine". **A**
- **Input change:** a storyboard validator in Cutroom that rejects shot lists where adjacent shots share POV+band.
- **Cheapest test:** 0 credits to lint existing storyboards. Then compare one re-planned clip against a failed one (~18 credits).

### T3. "De-slop" pass on every keyframe/board before video (exact prompt) [HF-WF]
- **How:** After the board or keyframe is generated, import its URL (`media_import_url`) and run Seedream i2i (`seedream_v5_pro`, same aspect, 2k, role `image_references`) with this prompt, **verbatim**:
  > KEEP EXACTLY the framing, composition, slot layout, camera distances, poses, subjects and product of this horizontal storyboard sheet and every one of its side-by-side vertical slots — no reframe, no zoom, no crop, no re-layout, no change to the scene, to any person's face / hair / body, or to the product design. CHANGE ONLY micro-realism, applied identically in every slot: true-to-life pore-level skin with natural texture and fine vellus hair, real material detail, even natural daytime light with gentle highlight roll-off and faint true sensor noise, a flat authentic iPhone photo, deep focus. PRESERVE each face's exact shape / width / proportions 1:1 — do NOT squeeze / narrow / slim / stretch any face. AVOID AI-slop: waxy plastic skin, airbrushed poreless skin, beauty-filter smoothing, over-saturation, HDR glow / bloom / halos, oversharpening, teal-orange grade, shallow depth of field, bokeh, cinematic / DSLR look. Keep the product blank / unbranded, no added text, no watermark, no baked slot labels.
  - If moderation blocks it, retry once on `seedream_v5_lite`. If that fails too, continue with the raw board.
  - **SANTO caveat:** the stock prompt says "keep the product blank / unbranded". For SANTO we must *replace* that clause with "keep the product's logo/print exactly as in the reference", or the de-slop pass will strip our branding (F2).
- **Fixes:** F6 mainly; also F1 (the "do NOT squeeze face" clause).
- **Evidence:** identical mandatory step in the try-on and unboxing workflows. **A**
- **Input change:** a new post-keyframe stage `deslop(image)`, with the prompt stored as a versioned template. Apply it to Soul/Nano Banana keyframes too, not only boards.
- **Cheapest test:** 1 Seedream edit on an existing "plastic" keyframe (about image cost; Seedream price not verified). Judge side by side.

### T4. Hide state changes in hard cuts: exact vendor rules for bag/box and garment-on [HF-WF] (evidence upgrade for our known "cut-to-transform" idea)
- **How:**
  - **Try-on:** cut 1 is the PRE_WEAR outfit (boring base: basic tee + lounge pants / oversized hoodie + shorts) with ONE plain kraft bag, held by one handle or set upright on a surface.
    - The creator **does not open it, peek inside, or lift the product out**.
    - `Hard cut to.` → cut 2 is already wearing the product, full body, static camera, with one natural twirl.
    - Never describe changing, pulling on, lifting fabric over the head, or zipping. "The hard cut carries it."
    - The bag "ceases to exist" after cut 1. The pre-wear outfit never returns.
  - **Unboxing:** cut 1 PACKED (sealed, product not visible) → cut 2 REVEAL (product just out; box at frame edge or gone) → cut 3 PRODUCT-FOCUS (box gone) → cut 4 SATISFACTION. 15 s split: **3.5 / 4.5 / 3 / 4 s**.
    - Generic box: one knife-slice of the tape, "one decisive motion".
    - **User-supplied branded package: no knife, no tape, no tissue.** Build excitement with knuckle taps and a sideways slide of a few cm, then **one clean opening motion** that matches the package's real mechanism.
    - The Set-Down/Pick-Up one-take device is **forbidden across a state jump**.
  - **For SANTO's poly mailer:** pass a real photo of the mailer as `package_media_id` for slot 1 (the workflow supports this). Describe its real mechanism: "peel-strip flap lifted and pulled open in one motion". The rip itself is never shown; it is a hard cut.
- **Fixes:** F4, F2, F3.
- **Evidence:** `ugc-try-on-video` SKILL + `tryon-clip.md` § "Bag Presence per Cut" / "No on-screen costume change"; `ugc-unboxing-video` SKILL + `unboxing-clip.md` Case A/B. **A**
- **Input change:** Cutroom stores a **real photo of the SANTO mailer, sealed**, as a required asset. The storyboard schema gets a `state_before` / `state_after` field; any slot pair with a state change is forced to a hard cut, and the prompt linter strips verbs like "pulls on", "rips", "unzips".
- **Cheapest test:** one 4-cut unboxing clip at 10 s with the real mailer photo (~18 credits).

### T5. Hand-count law + parked hands + "phone never visible" [HF-WF]
- **How:**
  - Every cut names the role of **each** hand, with at most 2 simultaneous hand roles.
  - One-hand actions must also say where the other hand is parked ("resting at her side", "flat on the counter"). In SELFIE the parked hand *is* the phone grip, off-frame.
  - SELFIE = 1 free hand, so **any two-handed action forces a STATIC (propped-phone) camera.**
  - A prop that would need a stabilising hand is **rested on a surface** instead ("a prop floating unheld beside busy hands spawns a third hand").
  - Multi-step actions are split across hard cuts, never piled into one beat.
  - The phone object is never in frame. Words like "phone in her hand", "mirror selfie", "over-the-shoulder" are banned in SELFIE cuts because they make Seedance draw the phone.
  - Scale props against the hand ("palm-sized, fits in one hand, ~15 cm"), never against another object.
- **Fixes:** F3 (also the "phone-in-hand while both hands busy" failure specifically).
- **Evidence:** `tryon-clip.md` § "THE HAND-COUNT LAW"; `unboxing-clip.md` § Hand Allocation; `product-intake.md` (hand-relative size). **A**
- **Input change:** the shot schema adds `left_hand`, `right_hand` and `pov`. The linter blocks >2 roles and two-handed actions in SELFIE, and auto-inserts "parked" text.
- **Cheapest test:** 0 credits to lint past failed prompts. Re-run the worst hand failure (~18 credits).

### T6. Hand-free fabric macros, with a motion recipe per garment type [HF-WF]
- **How:** Texture/detail close-ups (try-on cuts 4 and 6, about 1.4 s each in a 15 s clip) show fabric through **framing, drape and light only**.
  - **No hand touches the fabric**, and no operator hand enters. "Even gentle brushing reads as someone touching her clothes."
  - Each macro gets ONE passive motion, and cut 6 shows a *different* detail from cut 4:
    - Denim: "wash gradient visible as the leg shifts / seam line reads / fabric grain catches light".
    - Knit/fleece: "knit texture catches light as the body breathes / weave reads clearly in macro framing".
    - Tee/top: "light catches the chest area as she takes a slow breath".
    - Pants/leggings: "fabric falls along the leg with natural drape as she shifts weight / seam line visible as the body settles".
  - These cuts are **voiceover** with the mouth closed, which moves words away from risky lip-sync.
- **Fixes:** F2, F3, F5.
- **Evidence:** `tryon-clip.md` § Step 4b (table). **A**
- **Input change:** store the per-SKU fabric type and pull the matching motion phrase automatically. Store 2+ named detail zones per SKU (e.g. hoodie: chest print, cuff rib, drawcord tip).
- **Cheapest test:** a Wan 3.0 (~3.5 credits) macro-only shot of SANTO fleece with the "breath" motion, vs our current hand-rub macro.

### T7. Garment consistency lock + realistic-fit clause + "absent features stay absent" + big-lettering rule [HF-WF]
- **How:** Put these clauses verbatim in every prompt where the product appears.
  - **Lock:** "The garment keeps identical silhouette, primary color, print, and recognizable design details (collar style, hem, sleeve, neckline, hardware, stitching) across every Cut… rotates naturally with her body."
  - **Fit:** "rendered at realistic real-world proportions on the character's body — natural drape per the fabric weight, natural fit, not exaggerated" (the vendor notes that fashion priors slim and lengthen the wearer).
  - **Absent features:** if something is missing by design (no drawcord, no hardware, no pocket), write the absence visually, e.g. "clean kangaroo pocket, no zipper anywhere". Otherwise the model "hallucinates the default back in".
  - **Lettering:** small logos and tiny lettering render as gibberish; **large letterforms render clean**. Big-logo products get a warning. All *props* get "label turned away, too small to read".
  - **Multiple product angles:** "The product may appear only from these provided angles… Switch angles only by hard cuts, never by continuous rotation. Do not invent unseen design details."
- **Fixes:** F2, F5.
- **Evidence:** `tryon-board.md` Step 7; `tryon-clip.md` Universal Rules; `product-intake.md`. The Segwise QC guide agrees independently: "prompt volatility (changing wording between scenes) is one of the most common triggers of drift" (https://segwise.ai/blog/ai-ugc-product-consistency). **A**
- **Input change:** per-SKU record fields: `absent_features`, `logo_size_class` (large/small), `approved_angles[]`. Any SKU with a small chest logo is flagged "needs real insert or post-comp".
- **Cheapest test:** 0 credits to classify SKUs. Then one clip of a small-logo tee vs a big-print hoodie (~36 credits) to confirm the rule on our own products.

### T8. One canonical "product staging description", written once and reused verbatim [HF-WF]
- **How:** Write the product description once. It covers: shape, material, colour, **hand-relative size**, mechanism anatomy (what moves, where it opens), absent features stated visually, the label, plus **"one honest imperfection"**. Paste it verbatim into every board, clip and retry. Tier (luxury/premium/drugstore) and category are decided once and never re-detected.
- **Fixes:** F2, F3, F1 (less wording drift overall).
- **Evidence:** `product-intake.md`; Segwise "scene-graph template" (same idea; each scene binds the same product reference). **A**
- **Input change:** a `product_description` text field per SKU, locked after approval. The prompt builder refuses to paraphrase it.
- **Cheapest test:** 0 credits (text only).

### T9. Character still: a CLEAN person (nothing in hands) + the iPhone closing block + a hard-ban list [HF-WF]
- **How:** Generate the creator with Soul 2 at 3:4, 2k.
  - **No product, prop or object in the hands.** Compositing happens later. "Model bakes the bottle into the image, downstream compositing fails."
  - Lighting is **cool neutral daylight only**. Golden hour, sunset and amber casts are hard-banned: they make the persona look like a stock-photo ad.
  - Body pose stays neutral. Energy lives in the face, via an approved "mid-action" expression (e.g. "mid-thought, slight half-smile, eyes glancing slightly off-lens"). Creative poses are "an anatomy gamble".
  - Append this closing block verbatim:
    > Self-portrait selfie shot on iPhone front-facing camera held by the subject at arm's length — head and shoulders fill the frame, casual handheld framing, slight natural tilt, slightly off-center, slightly imperfect, not posed. Phone-sensor grain and realistic skin texture preserved, no retouch, no smooth-skin filter. No fisheye lens, no ultra-wide distortion. Authentic UGC creator phone selfie, NOT editorial portrait, NOT fashion magazine.
  - **Hard-banned phrases** (they flip Soul into editorial mode): "centered composition at eye-level", "straight-on", "editorial/fashion portrait", "minimal depth of field", "flattering and even illumination", "glowing/flawless skin", "poised/elegant stance", "warm smile at the camera", any "pose" verb.
  - Wardrobe colour must share a tone with the room palette. Only one loud accent colour per image.
- **Fixes:** F6, F1.
- **Evidence:** `ugc-character.md` (Higgsfield). The imperfection cues match Ryan Collins' course material ("shot on iPhone", "off-center composition", "harsh window light on one side") via https://www3.skool.com/ai-ad-lab-9711/about and MyUP https://myup.ai/blog/ai-ugc-ads-realistic-prompt-guide. **A**
- **Input change:** the model-reference generator gets the ban list as a linter, plus a "no props in character image" rule. Our current model refs may break this if the person holds anything.
- **Cheapest test:** 2 Soul stills (old prompt vs new block), a few credits.

### T10. A written spec for UGC camera realism (and the grain nuance) [HF-WF]
- **How:** Add this to Style & Mood and the Static Description: "23mm-equivalent wide, DEEP focus (background stays sharp), slight wide distortion at frame edges, never fisheye; smartphone sharpness, mild HDR flattening, slight highlight clipping, faint shadow noise; ONE motivated light source (window/lamp/daylight), consistent white balance; one small AE/AF adjustment mid-clip on a SELFIE cut only; real weight and inertia, correct contact shadows, hair and fabric react to movement."
  - The quality suffix also **bans** "cinematic color grade, film grain, shallow depth of field, bokeh, lens flare, slow motion, beauty filter".
  - **Nuance:** the vendor bans *film grain* (a cinematic cue) in the video prompt but asks for *faint true sensor noise* in the still de-slop. Several tutorials say "add film grain" (https://influencermarketinghub.com/ai-features-ugc-video-quality/). Following the vendor, sensor noise is phone-like and film grain is cinema.
- **Fixes:** F6 (bokeh, slow-mo floatiness, perfect lighting).
- **Evidence:** `tryon-clip.md` § "UGC camera realism" and Step 8. **A**
- **Input change:** make this the default suffix template. The "phone camera profile" post step should add sensor noise and HDR flattening, not film grain.
- **Cheapest test:** included in T1's test.

### T11. Camera-word hygiene: STATIC and SELFIE vocabularies must not leak [HF-WF]
- **How:**
  - **STATIC cuts** must *not* contain `handheld, shake, drift, wobble, sway, slight movement, micro-shake, natural movement, subtle movement`. These "leak motion into the render". Use "absolutely frozen and locked off… Only the subject moves." At the same time, **a locked camera must not mean a locked body**: every static cut needs a weight transfer, a mid-cut pose shift, a head or body turn, and lip-sync motion. "A STATIC cut with the subject standing perfectly still = REWRITE."
  - **Baked camera moves:** at most one per cut, never on every cut ("reads mechanical"). Only deliberate moves (slow push-in / ease-back) or a "candid handheld iPhone ZOOM-IN… tiny overshoot-and-correct" opener.
  - **Energy:** "Seedance under-renders energy; a flat-neutral prompt renders a wooden AI presenter." Each cut needs 5+ concrete micro-beats, and the expression must change across cuts; the same expression twice is forbidden.
- **Fixes:** F6 (floaty motion, wooden presenter), F7.
- **Evidence:** `tryon-clip.md` Steps 2b, 4, 5. **A**
- **Input change:** the prompt linter bans the handheld word list in static shots and requires ≥1 subject-motion verb per shot.
- **Cheapest test:** 0 credits to lint the movement library prompts.

### T12. The 0.1-second hook law + "accident of recording" openers [HF-WF + TikTok data]
- **How:**
  - **Timing:** frame 1 is already **mid-motion** (e.g. hands already at the mailer, body mid-turn), never a settled pose. The first spoken word (or a bracketed non-verbal sound like `[*soft gasp*]`) lands within **0.0–0.4 s**. The only allowed delay is a staged freeze of ≤0.7 s.
  - **Optional "H9" entry devices** (SELFIE only, max one):
    - Drop-Catch: frame already tumbling, caught and righted.
    - Walk-and-Slam: mid-stride, frame settles on the creator already talking.
    - Light Switch: near-black, a lamp clicks on, sound leads picture by 0.5 s.
    - Zoom-Out Reveal: extreme digital zoom on a textless texture, then a quick zoom out.
  - Each device **must carry its sound in the Audio line** ("a silent camera event renders as a glitch").
  - This lines up with TikTok's data: 90% of recall happens in the first 6 s, and 63% of top-CTR ads show the product or message within 3 s.
- **Fixes:** mainly performance. F8 (audio leads).
- **Evidence:** `tryon-clip.md` / `unboxing-clip.md` § "0.1-second hook law", "H9 Entry Device"; TikTok Creative Codes. **A**
- **Input change:** the storyboard requires `shot1.first_frame_state = mid-action` and a first line (or sound) of ≤0.4 s. Add a hook-type field chosen from a hook library (T17).
- **Cheapest test:** A/B two clips with the same body, one settled start and one mid-motion (~36 credits), then compare 3 s hook rate in a $20 test.

### T13. Scriptwriting rules: word budget, banned openers and AI-tell phrases, the specificity law [HF-WF]
- **How:**
  - **Density:** ≤10 s → 12–20 words; 11–12 s → 20–28; **13–15 s → 28–35 words**, at about 2 words/s.
  - **Frame:** a personal-want mini-story ("been eyeing this for months → it landed → fit moment → verdict"). Friction openers beat enthusiasm ("I almost returned this.").
  - **Banned first words:** OK/Okay/So/Alright/Um/Well/Like/Wait/Hold on/OMG/Hey guys/Story time/Stop scrolling.
  - **Banned anywhere:** obsessed, literally (as filler), game-changer, holy grail, hits different, 10/10, elevate/seamless/effortless, "you NEED this", and **"This is X, not Y" constructions** ("dead giveaway of AI writing").
  - **Specificity law:** every claim carries a concrete detail (a number, a place on the body, a named comparison: "sits at my waist like it was cut for me"). At most one peak reaction per clip, and no phrase repeated across cuts.
  - **Claims:** with no approved-claims list, no numeric or comparative product claim may appear.
  - **Apparel extra (C):** state height and size worn, e.g. "I'm 5'10, wearing a large".
- **Fixes:** F8 (fake-sounding speech is the #1 tell; per Oakgen, viewers "forgive a slightly imperfect synthetic presenter faster than a fake-sounding line": https://oakgen.ai/blog/realistic-ai-ugc-ads-checklist).
- **Evidence:** `ugc-try-on-video` SKILL step 4 + `tryon-clip.md` Step 6. The Atlas Cloud workflow uses a "panel of harsh judge agents" to rewrite scripts "until it sounds said and not written" (https://www.atlascloud.ai/blog/tips/how-to-make-ai-ugc-ads). **A**
- **Input change:** a script linter (ban list, word budget per duration, a "concrete detail present" check). Add an approved-claims list per SKU.
- **Cheapest test:** 0 credits.

### T14. Audio model: lip-sync only where the face is on screen, VO on macros, iPhone mic room tone, no music by default [HF-WF]
- **How:**
  - Seedance 2.5 renders speech natively (`generate_audio:true`); no separate TTS.
  - Faces on camera (cuts 1/2/3/5/7/8) get lip-sync. **Macro cuts are voiceover with "mouth not forming words"**. Lip-sync pauses when the back is to camera.
  - **Protect the mouth:** lip-sync is "the weakest render zone" (doubled lip edges, smeared corners). Add a closed-mouth beat in the densest cut and move wordy chunks onto the VO cuts.
  - Always write "iPhone microphone audio with natural room tone throughout" plus named foley ("fabric rustle on the twirl").
  - **Music is opt-in only.** It must be ducked under the voice with **no lyrics** ("lyrics fight lip-sync"). If music is wanted, add a platform track in post, not a generated one.
  - **Accents:** "text-only accent enforcement lands about one render in three". Attach a 5–10 s voice sample as an audio reference ("accent and vocal delivery reference only — do not copy words"), and write the accent "two levels stronger than asked".
- **Fixes:** F8, F9.
- **Evidence:** `tryon-clip.md` Step 6; `ugc-unboxing-video` SKILL step 3 (the 1-in-3 figure). The Meta Reels figure of +13% incremental conversions with music/VO is in Part A. **A**
- **Input change:** each shot gets `audio_mode ∈ {lipsync, vo, sfx_only}`. Cutroom stores a 5–10 s **real voice sample** (a staff member or hired voice) as the persona's audio reference, and a foley list per SKU (fleece rustle, denim swish, mailer crinkle).
- **Cheapest test:** a single 10 s clip with and without the voice-sample reference (~36 credits).

### T15. Frozen-frame QA before anything is stitched or shown [HF-WF + Segwise]
- **How:** For every clip, pull evenly spaced stills, **every garment close-up**, and **2–3 mid-word frames**. Check:
  - the garment matches the reference (silhouette, colour, print);
  - no hand on the fabric in macros, no mirror or reflection;
  - bag/box only where allowed, and prop states consistent (a cap is ON or OFF, never both);
  - ≤2 hands per person (edges included); product scale matches the hand;
  - lips have no doubled edges on mid-word frames and are closed during VO;
  - the face matches the reference; no baked text; the label is not gibberish or mirrored.

  On a staging failure, fix the prompt and re-roll *that clip only*. On lip slop, **cut spoken words first**.
- **Fixes:** F9 (stop shipping or iterating on broken clips), F1, F2, F3.
- **Evidence:** both HF workflows (step 8); Segwise: "skipping the QC step is where most broken-product ads slip through". **A**
- **Input change:** an automatic frame extractor (ffmpeg, free) plus a VLM checklist pass. Each failure is logged against the prompt feature that caused it, which feeds our "rule mining".
- **Cheapest test:** 0 credits (run on existing outputs).

### T16. Full re-description per shot + small prompt batches + a realistic yield budget [Kalshi / Segwise]
- **How:** Every shot prompt restates the character, wardrobe, room and product in full ("as if the model has no memory of the shot before or after"). Generate prompts **5 at a time** from the LLM (quality drops beyond that). Budget for yield: a pro freeform workflow averaged ~20–27 generations per usable clip. The structured HF pipeline plus QA is how you move away from that number.
- **Fixes:** F1, F7, F9.
- **Evidence:** PJ Accetturo / Kalshi (https://www.thedaringcreatives.com/creator-stories/pj-ace-nba-finals-ad/). **B**
- **Input change:** the prompt builder always inlines the full canonical blocks, never "same as before". Track gens-per-keeper as a KPI.
- **Cheapest test:** 0 credits.

### T17. Hook library mined from TikTok Creative Center, specific to apparel
- **How:** In TikTok Creative Center → Top Ads, set region = UK/US, industry = **Apparel & Accessories** (industry ID `22111000000`), last 30 days, sorted by **6-second view rate**. Screenshot the first 3 s of the top 20 (practitioner workflow). Open "See Analytics" on each: it shows **second-by-second CTR/CVR/retention curves** and names the **"highlight frames"** where the metric spiked. Tag each hook as visual (frame 1), text (a 2–5 word overlay readable in under 2 s), and verbal (the first line). Top UGC hooks reach **65–70% 3-second retention against an average under 30%** (C).
- **Fixes:** performance and F9 (better concept selection before spending credits).
- **Evidence:** https://www.stackmatix.com/blog/tiktok-creative-center-guide (workflow); https://admanage.ai/blog/tiktok-creative-center-guide (analytics/highlight frames); https://apify.com/automation_craft/tiktok-creative-center-scraper/examples/tiktok-cc-retention-curves (industry ID, retention curves). **A/B**
- **Input change:** a `hooks` table (visual/text/verbal/type/source URL/retention-curve peak second). The storyboard picks one hook row.
- **Cheapest test:** 0 credits manually. The Apify actor costs a few dollars per run (not Higgsfield credits).

### T18. On-screen text: burned in post, placed in the safe zone, native look
- **How:**
  - **Never bake text into a generation** (HF-WF: models "render RANDOM characters"). Add text in post, timed from a **word-level transcript of the final audio**, not from planned beats.
  - **1080×1920 safe zone:** keep 130 px clear at the top, **484 px at the bottom**, 140 px on the right, 44 px on the left. **The screen centre is the only guaranteed-clear area for the hook text.**
  - Design for sound-off first; text mirrors the spoken hook.
  - Ad caption: ≤100 characters.
- **Fixes:** F6 (garbled AI text), F9.
- **Evidence:** HF-WF step 10 + `subtitles.md`; TikTok safe zones https://admanage.ai/blog/tiktok-ad-specs and https://zeely.ai/blog/tiktok-safe-zones/; Meta captions +12% view time. **A/B**
- **Input change:** the Cutroom finishing stage gets a transcript-timed caption burner and a safe-zone overlay check.
- **Cheapest test:** 0 credits (ffmpeg + whisper).

### T19. Loop-engineered ending, no CTA tail [HF-WF]
- **How:** The final cut delivers the verdict, then ends with **either**
  - (a) a **mid-phrase timing cut**, so the last phrase is still in the creator's mouth when the clip ends, **or**
  - (b) a **frame-match** to cut 1's framing, without bringing back the pre-state.

  No "link in bio"; the platform's CTA button does that job.
- **Fixes:** performance (completion and replays). Also F4, because the ending never returns to a pre-state.
- **Evidence:** `tryon-clip.md` § "Loop-engineered ending". TikTok rewards completion (TikTok Creative Codes). **A** for the prescription; the performance effect is untested.
- **Input change:** add `ending_mode ∈ {mid_phrase, frame_match}` to the storyboard.
- **Cheapest test:** included in T1.

### T20. The one-take illusion: Set-Down / Pick-Up (at most once per clip) [HF-WF]
- **How:** One `Hard cut to.` may be replaced with a phone move:
  - **Set-Down** (SELFIE → STATIC): "she lowers the phone below the frame line — the frame swings down, tilts, and settles leaning at a slight low angle, slightly crooked. A perfectly level set-down reads fake." She steps back into view still talking.
  - **Pick-Up** (STATIC → SELFIE): she "reaches past the lens — never 'grabs the phone'", the frame lifts, shakes for a beat, and her face lands close.

  The voice runs unbroken through the move. It costs about 1.5 s. **Never across a state change.** Best spot: a VO macro cut into a lip-sync cut, just before the closer.
- **Fixes:** F6 (reads as real phone footage), F8 (continuous audio).
- **Evidence:** `tryon-clip.md` § Set-Down / Pick-Up. **A**
- **Input change:** add a `transition` field per boundary (hard_cut | set_down | pick_up) with the legality rules built in.
- **Cheapest test:** 1 clip (~18 credits).

### T21. Hybrid real + AI is legitimate, and it is what wins
- **How:** Keep real footage wherever AI is weakest (logo close-ups, hand-on-fabric, mailer rip). Use AI for the person, rooms and variety. Higgsfield's own Adathon allowed **up to 49% non-AI footage**, and its judges scored **"realism"** as one of four equally weighted criteria. Practitioner claim: real product footage + AI voice-over beats pure avatar ads for basics (tees, activewear).
- **Fixes:** F2, F3, F4, F5.
- **Evidence:** Adathon rules/judging https://www.adweek.com/creativity/higgsfield-ai-launches-85000-adathon-contest-in-partnership-with-adweek/ , https://higgsfield.ai/contests/adathon (A for the rules). Hybrid-wins claim https://adlibrary.com/posts/ai-ugc-for-ecommerce (C).
- **Input change:** already partly known (real-hands inserts). New: a phone-shot **SANTO B-roll kit** per SKU: logo macro, print macro, stretch/drape, mailer rip, all 9:16, 1–2 s each, with the same room and light as the AI keyframes.
- **Cheapest test:** 0 credits (shoot on a phone).

### T22. Disclosure is mandatory and detectable, so plan for the label
- **How:** TikTok ad policy (updated April 2026) allows AI-generated or significantly edited media **only with the AIGC label or a clear disclaimer**. Undisclosed AI content is **rejected or restricted**. TikTok **auto-detects via C2PA Content Credentials**. Synthetic faces, voice clones, AI backgrounds and photoreal AI product shots are all in scope. Meta and the NY law have similar rules.
- **Fixes:** F9 (rejected ads waste spend); brand risk.
- **Evidence:** https://ugcvids.ai/blog/tiktok-ai-content-disclosure-rules-2026 ; https://novoads.ai/en/blog/ai-ad-label-rules-2026 ; https://seller-us.tiktok.com/university/essay?knowledge_id=491489038501663&lang=en . **A/B**
- **Input change:** Cutroom's export sets the AI-disclosure flag and keeps a record of what was AI. **Do not try to strip C2PA metadata.** Measure hook rate with the label on.
- **Cheapest test:** 0 credits (policy).

### T23. Make text-led variants too (Fashion's top Meta format is "Post-It" / meme)
- **How:** Motion's 2026 dataset shows Fashion & Apparel's top-hit-rate Meta format is "Post-It" (sticky-note text over an image/video), with Meme also in the top 5. Text-only ads have the highest raw hit rate (11.6%), above UGC (7.56%). From each generated 15 s ad, Cutroom should also export 2–3 cheap derivatives: a Post-It style note over the best still or the loop, and a meme caption variant.
- **Fixes:** F9 (more winners per credit).
- **Evidence:** https://motionapp.com/library/research/creative-benchmarks-2026/visual-formats-by-vertical ; https://adliftr.com/blog/ad-creative-testing-statistics-2026 . **A** (large dataset; hit rate, not ROAS)
- **Input change:** an export stage for derivative formats.
- **Cheapest test:** 0–1.5 credits (Nano Banana edit, or plain compositing).

### T24. Energy register and persona written as one vivid line [HF-WF]
- **How:** The default register is NATURAL ("genuine delight… lively but human, never staged screaming"). HYPED is used only on explicit request. For personas, put one line first: `[identity] + [attitude in plain words] + "speaks and moves exactly like that."` The rationale: "a vivid persona line retrieves a whole person; feature lists get averaged away". Restate it verbatim in every board and clip; clips generated separately drift apart otherwise.
- **Fixes:** F1, F8.
- **Evidence:** `tryon-clip.md` Step 5 + persona passthrough. **A**
- **Input change:** each saved persona carries one locked persona sentence.
- **Cheapest test:** included in T14.

---

## 15-second apparel UGC template (evidence-backed)

**Basis:** Higgsfield's canonical try-on arc and its 15 s time split (A), combined with TikTok/Motion hook and text data (A/B) and apparel practitioner rules (C). One Seedance 2.5 omni-reference call from a de-slopped 8-slot board. About 30–34 spoken words. Hard cuts only. No music (a platform sound can be added in post). Captions burned in post.

**Variant 1: "Finally here → fit check" (SANTO hoodie / fleece / jeans).** Arc and timings are straight from `tryon-clip.md` (15 s row).

| Cut | Time | Beat | POV / distance | Audio | What's on screen (SANTO example) | Text overlay (post) | Main guards |
|---|---|---|---|---|---|---|---|
| 1 | 0.0–1.9 | PRE_WEAR hook | SELFIE / MID (optional candid zoom-in opener) | Lip-sync. First sound ≤0.4 s: `[*soft gasp*]` + "Been waiting on this drop for actual months —" | Already mid-motion: SANTO mailer (real photo ref) set on the bed, creator in a boring grey tee. Mailer unopened | Centre hook, 2–5 words: "the hoodie everyone asked about" | Mailer never opened; 1 free hand |
| 2 | 1.9–4.2 | WEARING + 1 twirl | STATIC / WIDE full body | Lip-sync, pauses during twirl, + fabric rustle | Already wearing the hoodie. One twirl shows the back print, then settles | "6'0 / wearing L" (the size rule) | Hard cut hides the change; garment lock |
| 3 | 4.2–6.1 | FRONT_POSE | STATIC / WIDE at a different distance | Lip-sync: "heavier than the photos — sits right at my hips" | Weight onto one hip, one hand smooths the front hem | — | Realistic fit clause |
| 4 | 6.1–7.5 | TEXTURE macro | STATIC-CLOSE / MACRO | VO, mouth closed: "brushed fleece inside, feels like a blanket" | Fleece face catches window light as the body breathes; **no hand** | — | Hands off the fabric |
| 5 | 7.5–9.4 | TURN | STATIC / WIDE | Lip-sync: "and the back —" | Mid-turn, glance over the shoulder, back print reads | — | Big print renders clean; small logo → real insert |
| 6 | 9.4–10.8 | DETAIL macro #2 | STATIC-CLOSE / MACRO | VO: "rib cuffs don't go baggy" | Cuff rib at the wrist, hand relaxed, not touching | — | Different detail from cut 4 |
| 7 | 10.8–13.1 | STYLE_POSE, new room | STATIC (or Pick-Up → SELFIE) / MEDIUM-WIDE | Lip-sync: "wore it straight out to get coffee" | Kitchen doorway, keys-free pose (≤1 accessory) | Optional price/offer sticker (TikTok fashion tip) | Room ref photo; no mirrors |
| 8 | 13.1–15.0 | FINAL_LOOK + loop | STATIC or SELFIE / MID | Lip-sync, cut mid-phrase: "not taking this off till —" | Confident look to the lens, mid-motion, frame-matches cut 1's distance | — | No CTA tail; loop |

**Why these numbers (evidence):**
- Product is on the body by 1.9 s (TikTok: 63% of top-CTR ads show the product within 3 s; apparel guidance says within 2 s).
- Hook text is visible 0–2.5 s in the screen centre (safe-zone data).
- Cuts are 1.4–2.3 s long (the 2–3 s rule; editor norm of 1.5–3.5 s).
- 30–35 words, about 2 w/s (HF density table).
- The macro cuts carry VO so the riskiest lip-sync is avoided (HF "protect the mouth").
- 15 s total is the fashion sweet spot and a full Meta ThruPlay.

**Variant 2: "Mailer → reveal → on" (unboxing-led).** For the SANTO mailer this is **our own extension**; the vendor keeps unboxing and try-on as separate flows. Use a director-tier 8-slot board:
1. PACKED (0–1.8 s, real mailer photo, knuckle taps, one clean peel-flap motion as the last beat).
2. `Hard cut` REVEAL (1.8–3.8 s, hoodie held up by the shoulders with both hands, STATIC, mailer at the frame edge).
3. PRODUCT-FOCUS (3.8–5.0 s, macro of the print, VO).
4. `Hard cut` WEARING (5.0–7.3 s, STATIC full body; the change is hidden).
5. TEXTURE macro (7.3–8.7 s).
6. TURN (8.7–10.6 s).
7. STYLE_POSE (10.6–13.0 s).
8. FINAL (13.0–15.0 s, mid-phrase).

Two state jumps, both on hard cuts. **Untested:** the vendor's evidence is for each arc on its own. Streetwear practitioners also report that fit-check drives purchases while unboxing drives engagement, so test Variant 1 first.

---

## Prompt → output structures we can copy (Part C)

1. **Higgsfield Seedance clip skeleton** (`tryon-clip.md` § Prompt Structure). Order:
   - `Style & Mood:` (UGC iPhone aesthetic, light, POV cadence, "social media vertical format")
   - `Narrative Summary:` (1 sentence + register phrase)
   - `Dynamic Description:` `Cut n (a–b s) — [DISTANCE] [POV] (BEAT): …4–10 sentences… Hard cut to.`
   - `Static Description:` (1–2 sentences)
   - `Audio:` (per-cut lip-sync/VO + "iPhone microphone audio with natural room tone")
   - quality suffix, ending with negatives: no mirror/reflection, no on-screen text, no legible text except the product's own label, no cinematic grade / film grain / DoF / bokeh / lens flare / slow motion / beauty filter, no fisheye, no third arm / extra hands, no CTA tail.

   Full text is in `research/hf-workflows/tryon-clip.md` lines 71–97.
2. **Higgsfield Soul creator prompt** (`ugc-character.md` § Prompt Structure + kitchen reference example, lines 638–665). A 7-line template ending with the iPhone closing block (T9).
3. **De-slop prompt** (T3), verbatim.
4. **Product-preservation block** from Higgsfield's `label-trace` / `texture-track` presets (Seedance 2.0, 6 s, 1080p, `bitrate_mode: high`, no audio): "Preserve the exact product identity, silhouette, proportions, materials, colors, logo placement, packaging structure, and readable label text in every frame… Do not morph, melt, duplicate, replace, or redesign the product. Do not add people, hands, unsupported claims, extra logos…" Their prep frame puts the product at **60–70% of the frame**. This fits clean product-only inserts (not UGC) and is usable as a fidelity reference shot.
5. **Kalshi method:** script → LLM shot list → self-contained prompts, 5 per batch → about 25 gens per keeper → edit in CapCut/Premiere.
6. **Community prompt directories:** UlazAI (1,945+ community prompts for Seedance 2 / Veo 3.1 / Kling 3 / Wan, https://ulazai.com/directory/); Luma's 12 UGC-style examples (https://lumalabs.ai/news/ugc-style-ai-video-prompts); Higgsfield Seedance 2.5 prompt library (blog, covered by another researcher). Quality is unverified; treat them as structure ideas only.

---

## Part B — What courses, communities and contests teach (condensed)

| Source | What it teaches that's specific | Usefulness |
|---|---|---|
| **Higgsfield Academy, "Build a Brand's Visuals with AI"** (a fictional clothing brand "Higgs": Inventing the Brand, Creating the Products, Marketing Studio Try-Ons, Packaging & Unboxing, Social Video Content, The AI Marketing Workflow) https://higgsfield.ai/academy/courses/brand-visuals-ai | It is literally our use case (clothing brand + packaging + UGC). The UGC Try-On preset is described as "multiple short beats showing the avatar putting on different items and finishing facing the camera in the complete outfit", which matches the 8-beat hard-cut arc above | High. Lesson pages were not fetchable; worth watching manually (free) |
| **Higgsfield MCP workflows** (above) | The most concrete material found anywhere | Highest |
| **AI Video Bootcamp** (Mateo Starcevic, 24k creators) https://aivideobootcamp.com/ | Most-asked question: "why does my ad look like AI when I want it to look like a phone?" Answer: a fixed set of realism cues + selfie framing + "real person in a real room". Their negative prompt list: studio lighting, perfect composition, professional photography | Medium (corroborates T9/T10) |
| **Ryan Collins "AI UGC + Ads" Skool** ($67; 8 yrs, 2,000+ ads) https://www3.skool.com/ai-ad-lab-9711/about | Character and location consistency with Nano Banana → Veo 3.1 / Sora 2. Imperfection cues: "harsh window light on one side, slightly uneven exposure", "visible pores, faint natural shine", "tiny handheld wobble" | Medium |
| **Dan Kieft** (YouTube + Skool, 58k) | JSON-structured prompts for AI-influencer UGC; tips on voice consistency; monthly competitions with prompts shared | Medium (JSON = a structured schema like T1) |
| **Alec Wilcock** (YouTube full tutorial) https://www.classcentral.com/course/youtube-how-to-make-ai-ugc-ads-full-tutorial-445449 | Master ChatGPT script prompt → AI influencer → AI B-roll → Meta Ad Library for inspiration → "editing touches" | Low–medium |
| **Curious Refuge, AI Advertising** (4 weeks, Discord) https://curiousrefuge.com/ai-advertising | Brand consistency with AI photography, editing and sound design, motion graphics. Their contest-winner interview (Dave Clark): taste, story and strategy beat spectacle | Low for UGC realism |
| **Higgsfield Adathon** (Adweek, Sept 2026). Judges: Adweek CCO, Monzo CMO, WPP CIO | **Criteria (equal weight): idea, brand storytelling/effectiveness, craft (camerawork, sound), realism.** ≥51% AI visuals; the rest can be real footage. The winner ("Don't Kill the AI Stars") was self-aware humour, not photorealism | Medium (hybrid is legitimate; sound design is judged) |
| **Kling NextGen contest** (4,600 entries, 122 countries) | Winners were cinematic shorts (the Grand Prix was oil-painting style) | Low for UGC |
| **Higgsfield Seedance 2.0 contest** ($50k), Global Film Festival ($1M) | Film-oriented | Low |
| **Motion Creative Strategy Bootcamp / library** | Hook tactic leaderboards by vertical | High for concepts, not rendering |

---

## Idea sources we should mine on a schedule

| Source | What to pull | How (tool-friendly) | Cadence |
|---|---|---|---|
| **Higgsfield MCP workflows** (`get_workflow_instructions` → `ugc-try-on-video`, `ugc-unboxing-video`, `ugc-review-video`, `ugc-product-video`, `ugc-tutorial-video`, `character-sheet`, `ad-multiplier`) | Version bumps, new banned phrases, new timings, new model routing | Free, read-only MCP calls; diff against `research/hf-workflows/` | **Weekly** (cheapest and highest-signal source) |
| Higgsfield presets (`get_preset_instructions`, `get_presets source:marketing_studio`) | Master prompts and parameters for product inserts | Free MCP read | Monthly |
| **Higgsfield community feed** (each post has a **Recreate** button with the full prompt and model) | Trending prompt→output pairs; filter for UGC and fashion | Parse.bot "Higgsfield AI Community API" returns prompt, params, seed, image URL and views/likes, sorted by trending (https://parse.bot/marketplace/9bed17eb-74d2-48e0-9c14-9fe123cb924b/higgsfield-ai-api). Images only per the listing; check for video | Weekly |
| **TikTok Creative Center Top Ads**, Apparel & Accessories (`22111000000`), UK + US, 30 days, sorted by 6 s view rate | Hooks, first-3 s frames, second-by-second CTR/CVR/retention curves, "highlight frames" | Manual, or the Apify actor `automation_craft/tiktok-creative-center-scraper` (retention curves; industry filter) | **Weekly** |
| Meta Ad Library: Gymshark, Oner Active, Represent, Skims, Corteiz, plus UK streetwear peers | Long-running ads (running 30+ days ≈ winners): hook, cut count, text | Manual, or swipe tools (Foreplay, Atria's 25M-ad library, gomarble brand pages such as https://www.gomarble.ai/library/brands/gymshark/) | Bi-weekly |
| Motion Creative Benchmarks / Thumbstop Pulse | Hook-tactic and format leaderboards by vertical | Read the reports | Quarterly |
| Google **Flow TV** (every clip shows its exact Veo prompt; channels) https://labs.google/flow/tv/faq | Prompt structure for realistic motion and sound | Manual browse | Monthly |
| Kling Explore / prompt pages https://kling.ai/explore/kling_ai_prompt ; Dreamina Seedance prompt pages | Copyable prompts per model | Manual | Monthly |
| UlazAI prompt directory (1,945+ prompts, per model) | Structures for Seedance 2 / Wan / Kling | Manual | Monthly |
| Higgsfield Discord, AI Video Bootcamp, Ryan Collins Skool, Dan Kieft Skool | "Post your work" threads where people share prompt + output + critique | Human membership (no scraping) | Opportunistic |
| Adathon and other contest galleries (Higgsfield, Curious Refuge) | What judges reward on "realism" | Manual | Per contest |

---

## STOP DOING (what pros and the vendor say hurts quality)

1. **Showing the state change** (ripping the mailer, pulling the hoodie on, zipping). The vendor's pipelines never render it; the hard cut does. (HF-WF)
2. **Mirror selfies and any reflective surface.** The vendor calls reflections "a limb factory (extra hands, duplicated bodies)". This rules out the Skims mirror grammar for AI; use a propped-phone STATIC shot instead. (HF-WF)
3. **Hands touching fabric in close-ups** and "operator hands" entering the frame. (HF-WF)
4. **Props, or the product, in the character reference image.** (HF-WF)
5. **Golden hour / warm light, "editorial", "portrait", "poses", "flawless skin", centred eye-level framing** in any prompt. (HF-WF)
6. **"Film grain", "shallow depth of field", "bokeh", "slow motion", "cinematic grade" in video prompts.** Phone realism means deep focus plus sensor noise. (HF-WF)
7. **Handheld/shake words in static shots**, and camera moves on every cut. (HF-WF)
8. **Baking captions or text into generations.** Small logos and prop text come out as gibberish or as a competitor's brand. (HF-WF)
9. **Opening with "OK so / Hey guys / Wait / OMG / Stop scrolling"**, saying "obsessed / literally / game-changer / 10/10", or using "This is X, not Y" sentences. (HF-WF)
10. **Music with lyrics under lip-sync**, or silent audio. Default to iPhone room tone + foley + voice. (HF-WF; Meta sound data)
11. **Paraphrasing the product description between shots** ("prompt volatility" → drift). (Segwise; HF-WF)
12. **Pure-avatar talking heads for basics.** Hybrid real product footage wins; AI is for hook testing, and winners get reshot or hybridised. (C: adlibrary, inBeat)
13. **Hiding the AI.** Undisclosed AI ads are rejected on TikTok, and C2PA is auto-detected. Brand backlash (Guess/Vogue 2025, Gucci 2026, Valentino 2025) came when AI was presented as craft or representation. Aerie's anti-AI "You can't prompt this" campaign reported +23% sales. (https://www.breef.com/breefingroom/articles/the-ai-marketing-backlash-why-ai-first-brands-are-starting-to-fall-flat)
14. **Settled first frames** and a silent lead-in before the first word. (HF-WF; TikTok)

---

## Open questions

1. Does Higgsfield's web UI use this same board → Seedance 2.5 pipeline (e.g. the Marketing Studio "UGC Try-On" preset)? If so, Cutroom could call the workflow's logic directly.
2. **Credit cost** of `gpt_image_2` 21:9 boards and `seedream_v5_pro` de-slop on our plan (read free with `models_explore` before testing).
3. The stock de-slop prompt says "keep the product blank / unbranded". Does replacing that clause (to keep SANTO's logo) weaken the realism gain?
4. Does an 8-cut single clip keep our **small chest logo** legible? The vendor's own rule says small lettering renders as gibberish, so we likely need a real-footage logo insert or post-comp.
5. Does the TikTok/Meta AI label hurt hook rate for UGC-style apparel ads? Needs a small paid A/B.
6. Fit-check vs unboxing-led for SANTO's cold traffic: practitioner claims (fit-check sells, unboxing engages) are C-grade.
7. Does Parse.bot's Higgsfield community API return **video** generations with prompts, or images only?
8. Higgsfield Academy "Packaging & Unboxing" and "Marketing Studio Try-Ons" lesson content could not be fetched. Someone should watch them (free) and note specifics.

---

# PART 9 — `07-adjacent-3d-audio.md`

## 07: What adjacent industries do: virtual influencers, 3D/digital twins, performance capture, audio, e-com capture

Researcher scope: agencies and fields that already dealt with our failures: virtual-influencer studios, AI fashion-model vendors, CGI/FOOH studios, mocap and motion-transfer tools, voice/lip-sync/sound, and e-commerce product photography.
Method: about 55 WebSearch queries (WebFetch blocked) plus one raw GitHub read of an ElevenLabs v3 tag reference. Strength grades follow BRIEF (A = vendor docs or several independent pros; B = one credible practitioner with results; C = claim).

---

## The big finding (read this first)

**The virtual-human studios that look most real never generated the clothes. They put a synthetic head on a real body that wore the real garment in a real place.**
- **Imma** (Aww Inc / ModelingCafe): "each image rendered by transposing her 3D head onto a live-action body and background" ([mymodernmet](https://mymodernmet.com/imma-cgi-virtual-model/), [interestingengineering](https://interestingengineering.com/culture/meet-imma-the-worlds-first-computer-generated-model)).
- **Shudu** (Cameron-James Wilson / The Diigitals) uses a roster of real stand-in "muses". In his words, designers lack 3D garments, "so to dress the model effectively you need to shoot on a real model and then merge the images together" ([Shudu wiki](https://en.wikipedia.org/wiki/Shudu_Gram), [stylist](https://www.stylist.co.uk/beauty/fenty-cameron-james-wilson-3d-digital-supermodel/193080)).
- **Lil Miquela** (Brud): critics noted "her clothes have a reality, an unmistakable drape and weight and texture… in contrast to her CGI skin". The images are composites ([Forbes](https://www.forbes.com/sites/mattklein/2020/11/17/the-problematic-fakery-of-lil-miquela-explained-an-exploration-of-virtual-influencers-and-realness/), [cut-the-saas](https://cut-the-saas.com/ai/the-ai-behind-virtual-influencer-lil-miquela)).
- **Mango**'s all-AI Teen campaign "began with shooting real photos of each garment" ([Mango Fashion Group](https://mangofashiongroup.com/en/w/mango-crea-la-primera-campa%C3%B1a-generada-con-inteligencia-artificial-para-su-l%C3%ADnea-teen)). **Zara** takes real shoots of real models and uses AI to *re-dress* them ([technology.org](https://www.technology.org/2025/12/19/zara-deploys-ai-technology-to-virtually-dress-real-models-in-new-campaigns/)).

In 2026 this "real body, synthetic identity" pipeline can be run with video tools: Wan 2.2 Animate *Replace* mode, Higgsfield Genjutsu (Object Swap / Motion Transfer, launched 1 Sep 2026), Runway Aleph 2.0, and Kling 3.0 Motion Control. It is the single input change most likely to fix F2/F3/F4/F5/F7 together. The cost moves into a cheap phone capture instead of rerolls. The rest of this file adds the capture specs, audio chain and reference-photo rules that make it work.

---

## A. Virtual influencer and AI fashion-model practice

### 1. Real body plate + identity swap ("Imma method")
- **How**: A body double (friend, staff, paid local creator, about £20–50 an hour) wears the actual SANTO garment. They film the whole 15 s beat handheld on a phone in a real room: tear the mailer, pull on the hoodie, zip, squat in leggings. Then only the identity is replaced:
  - Wan Animate **Replace** mode keeps the original camera, background and body. A SAM2 mask covers the character, and you can shrink it toward head and hair ("mask expansion" is configurable). A **Relighting LoRA** (trained on IC-Light composites) matches skin tone and light to the plate ([Wan-Animate paper](https://arxiv.org/pdf/2509.14055), [HF model card](https://huggingface.co/Wan-AI/Wan2.2-Animate-14B), [comfy.org workflow](https://comfy.org/workflows/use-cases/ai-character-replacement/)).
  - Higgsfield Genjutsu **Object Swap** changes "a selected character, outfit, product… while preserving the rest of the shot". It takes 3–30 s reference video and up to about 30–40 reference images ([higgsfield blog](https://higgsfield.ai/blog/higgsfield-genjutsu), [rekreate](https://rekreate.ai/news/higgsfield-genjutsu)). The MCP routes it via `generate_video` → `hf_mult_replace_object` / `hf_mult_motion_control`. Other researchers cover Higgsfield specifics.
  - Runway Aleph 2.0 edits real footage "changing only that" element, clips up to 30 s at 1080p ([runway](https://runway.com/product/aleph-2)).
- **Why it works**: fabric physics, fit, hand-product contact, the bag tear and the room are all *recorded*, not generated. Only the face, which the persona pipeline already controls, is synthetic.
- **Fixes**: F2, F3, F4, F5, F7, plus F6 (real handheld motion and real light). F1 is handled by the identity reference.
- **Evidence**: A for the principle (Imma, Shudu, Miquela, Zara all use it). B for doing it with 2026 video models (Wan paper and vendor docs; independent UGC results not seen).
- **Gotchas**: Wan skips pose retargeting in Replace mode, so a body double with a very different build from the persona causes deformation (paper). Swap engines "read held objects as part of the body geometry" ([higgsfield face-swap guide](https://higgsfield.ai/blog/AI-Face-Character-Swap-in-Video-Photo-PRO-Guide)). That is good here because the object held is the *real* product. Aleph edits drift "when the target becomes occluded, changes scale, or moves quickly" ([techpoint review](https://techpoint.africa/guide/runway-ai-aleph-review/)).
- **Input change for Cutroom**: a new shot type, "Plate + Swap". It stores `plate_video` (phone, continuous, 3–30 s), `body_double_id` (with height/build) and `swap_scope` = head | head+hair | full-character. The swap uses the persona reference pack. Plate spec: see #12.
- **Cheapest test**: 1 plate (film today, 0 credits) → 1 Wan-class replace run. Check the per-second cost via `models_explore` (free). Compare against the current best full-gen of the same beat (about 18 credits on Seedance).

### 2. Persona "digital twin" capture protocol (H&M / Uncut; The Clueless)
- **How H&M/Uncut do it**: they shot the 30 real models "from different angles, with different lighting, in a variety of poses and in motion". A twin is considered accurate "only once all the person's special features, including birthmarks and typical movement patterns, have been captured" ([sourcingjournal](https://sourcingjournal.com/topics/technology/h-and-m-artificial-intelligence-models-digital-twin-1234741894/), [retail-optimiser](https://retail-optimiser.de/en/hm-plans-to-advertise-with-digital-twins-of-models/), [apparelresources](https://apparelresources.com/business-news/manufacturing/hm-unveils-first-ai-generated-digital-model-twins-ads-social-media/)). The Clueless (Aitana López) uses character LoRAs, batch generation, then **manual Photoshop passes for face consistency**, with a "character bible" (backstory, pet, zodiac) ([cut-the-saas](https://cut-the-saas.com/ai/aitana-lopez-blending-ai-and-style-in-the-age-of-virtual-influencers), [netinfluencer](https://www.netinfluencer.com/the-clueless/)).
- **For Cutroom**: the persona pack should hold more than 1–3 face shots:
  - (a) 3 head angles (front, 3/4, profile) × 2 lights (window daylight, warm lamp)
  - (b) a neutral, a talking and a laughing expression
  - (c) full-body front and side, for build (needed for #1 body-double matching)
  - (d) 1 motion clip (a 5 s walk or turn)
  - (e) **2–3 deliberate identity markers** (mole position, eyebrow scar, chipped nail polish colour, specific earring). These make drift *detectable* by a reviewer or VLM check. H&M's twins count birthmarks as part of identity.
  - Kling 3.0 Motion Control now takes **multiple character reference images plus "Element Binding"** for the face. 2.6 took one ([atlascloud](https://www.atlascloud.ai/blog/guides/kling-ai-motion-control), [ai-creators.tech](https://en.ai-creators.tech/media/creative/kling3-motion/)).
- **Fixes**: F1, F7 (markers stop random jewellery appearing: "earring = small silver hoop, left ear only").
- **Evidence**: A (H&M/Uncut reporting from several outlets; Kling docs).
- **Input change**: schema `persona.reference_pack` with required slots and `persona.markers[]`. The auto-QC compares every generated keyframe's markers.
- **Cheapest test**: build the pack with Soul ID / Nano Banana, about 10 images × 1.5 = **~15 credits** once per persona.

### 3. Persona clearance: accidental real-person likeness
- **What went wrong**: Shein's (vendor-supplied) AI model image scored a **99.9% facial-recognition match to Luigi Mangione**. The listing was pulled and a public investigation followed ([CNN](https://www.cnn.com/2025/09/03/business/shein-shirt-luigi-mangione), [Vice](https://www.vice.com/en/article/shein-is-using-an-ai-luigi-mangione-as-a-t-shirt-model/)). Separately, models sued a brand in 2026 over AI doppelgängers ([PetaPixel](https://petapixel.com/2026/06/24/models-claim-fashion-brand-used-ai-to-create-their-doppelgangers/), [OECD.AI](https://oecd.ai/en/incidents/2026-05-30-7108)).
- **How**: before a persona goes live, run its hero face through a reverse face search (PimEyes, FaceCheck-type) and a celebrity-lookalike check. Log the result. If a body double's face could leak into frames, get a signed likeness release. H&M and Zara pay models "identical to classical image use" ([Zara, cityam](https://www.cityam.com/zara-turns-to-ai-edited-models-amid-shop-closures/)).
- **Fixes**: legal/brand risk (no F-code). It is also why a persona should never be "inspired by" a real creator.
- **Evidence**: A (widely reported incident).
- **Input change**: `persona.clearance {date, tool, result}` must be present before the persona can be used in export. `body_double.release_signed` is a boolean.
- **Cheapest test**: 0 credits.

### 4. Garment-truth rule for fit categories (the Mango and Levi's lesson)
- **What went wrong**: the Mango Teen AI campaign was called "#falseadvertising". The shopper quote was "When I order clothes… I look at the pictures to see how the actual clothes fit. AI pics are completely useless for that" ([Yahoo](https://www.yahoo.com/tech/mango-ai-models-slammed-false-192812823.html)). Levi's/Lalaland was attacked on framing (it was pitched as "diversity"). Its e-com use case was sound ([CampaignsLive](https://campaignslive.com/blog/levis-lalaland-controversy/)). A PowerReviews survey says 28% of apparel returns come from appearance mismatch ([metamodels](https://metamodels.ai/feeds/blog/ai-model-photography-what-fashion-brands-get-wrong)).
- **How**: for **leggings, jeans and fleece fit beats** (the F5 shots), use #1 (real body plate). Keep full generation for shots where fit is not the claim (a hook face, a reaction, a mailer on the doorstep).
- **Fixes**: F5, F2, plus trust and returns.
- **Evidence**: A (public backlash, several outlets).
- **Input change**: each product gets a `fit_critical: true/false` flag. When true, the storyboard gate needs a plate for any shot showing the garment on the body in motion.
- **Cheapest test**: 0 credits (a policy).

### 5. Brute force doesn't buy consistency (Coca-Cola 2025)
- **What went wrong**: Secret Level made Coke's 2025 holiday ad from **70,000+ generated clips** by 100+ people in 30 days across Sora, Veo 3 and Luma. It was still panned as "inconsistent… switching between realism and cartoonish", with "mismatched styles across the clips" ([vp-land](https://www.vp-land.com/p/coca-cola-s-ai-holiday-ad-how-70-000-generated-clips-built-a-familiar-yet-new-commercial), [contentgrip](https://www.contentgrip.com/coca-cola-ai-holiday-ad-backlash/)). Seraphinne Vallora's Guess/Vogue models took "hundreds of iterations… to perfect texture, movement and details of the advertised product" ([CNN](https://www.cnn.com/2025/07/31/style/vogue-ai-models-guess-campaign)).
- **Takeaway for Cutroom**: rerolls are the budget sink (F9). Mixing generator models *inside one 15 s ad* creates visible style seams (F6). Lock one video model per ad for all persona-on-camera shots. Buy consistency with captured inputs (plates, packs), not more rolls.
- **Evidence**: A.
- **Input change**: `ad.primary_video_model` is locked at storyboard. Any shot overriding it must justify it (e.g. an insert with no persona in it).

---

## B. Digital twins / 3D for product fidelity

### 6. Planar-track the real logo or print back on (VFX logo replacement)
- **How**: this is standard VFX logo replacement ([Boris FX Mocha](https://borisfx.com/blog/learn-how-to-do-planar-tracking-with-mocha-pro/), [curved surfaces](https://blog.pond5.com/20827-how-to-track-and-replace-logos-on-curved-surfaces-with-mocha-pro/)):
  1. Store the true artwork (vector/PNG) of every SANTO print, logo, woven label and mailer-bag graphic.
  2. After generation, draw a spline around the drifted logo region and planar-track it forward and backward. The track captures position, scale, rotation, shear and perspective.
  3. Corner-pin the true artwork, multiply or overlay onto the fabric, add a small blur to match focus, and add grain.
  4. Use a manual Surface track when auto fails.
  - It works best on **mostly planar areas**: hoodie chest print, flat mailer bag, tee front, leggings waistband logo. It fails on heavy folds or quick turns. For folds, a mesh warp (Mocha Pro) is needed.
- **Fixes**: F2 (logo/print/text drift). This is the only method in this report that *guarantees* pixel-true logos.
- **Evidence**: A as a VFX technique. C as an applied fix for AI UGC (no case study found).
- **Input change**: `product.artwork[]` holds vector/PNG plus real-world size and placement. Add a post stage, "logo patch", triggered when the logo is at least about 5% of frame area and visible for more than 0.5 s. Headless automation is possible: OpenCV/CoTracker point tracks → homography → composite. Worth a spike.
- **Cheapest test**: 0 credits. Take one existing drifted clip, patch it in AE/Mocha or DaVinci Fusion's planar tracker, and judge the result.

### 7. Scan the rigid products (mailer bag, folded stack, tags) as Gaussian splats; render exact-angle stills as start frames
- **How**: capture the sealed SANTO mailer, a folded hoodie stack, and the hang-tag or woven label with Polycam, KIRI or Luma. Shoot 4K video, walk slowly, cover many angles and heights, 1–3 min ([polyvia3d capture guide](https://www.polyvia3d.com/guides/gaussian-splatting-mobile-capture), [swyvl](https://swyvl.io/blog/how-to-create-gaussian-splats/)). Render the exact camera angle the storyboard needs (e.g. mailer on a bed from a 35° high angle) and use it as the Nano Banana composite source or the start frame. Practitioners describe this "3D-as-reference for 2D pipelines": the start frame is "grounded in real geometry" ([wavespeed TripoSplat](https://wavespeed.ai/blog/posts/triposplat-image-to-3d/)).
- **Limits**: good only for rigid or nearly rigid items. Worn garments deform, so use #1 for those. Splat texture is only as sharp as the capture frames, so fine text softens; pair with #6. Cross-polarised light (#20) during capture avoids baked glare on the glossy mailer.
- **Higgsfield note (not called)**: `generate_3d` (image → GLB) and `scene_builder_3d_*` exist. Generic image-to-3D models bake lighting into albedo and have uneven texel density ([rundiffusion/cinevva comparisons](https://app.cinevva.com/guides/ai-3d-model-generators)). Do **not** expect logo fidelity from an image-to-3D mesh. Use it only for blocking and camera angles (#8).
- **Fixes**: F2 (exact angles without re-shooting), F9 (no rerolls to "find" an angle).
- **Evidence**: B/C (workflow described by tool vendors; no ad case study with metrics).
- **Input change**: `product.scan_url` (splat/GLB) for rigid SKUs and packaging. The shot planner can request a render at a named angle.
- **Cheapest test**: 0 credits. Scan the mailer in KIRI or Polycam (free tier) and compare 3 rendered angles with real photos.

### 8. 3D blockout → depth/pose control video for environment and camera lock
- **How**: block the room and camera move in Blender (or Higgsfield's 3D scene builder / Blender plugin, which exports MP4, a still or GLB: [higgsfield 3D Jutsu](https://higgsfield.ai/blog/higgsfield-3d-jutsu), [blender plugin](https://higgsfield.ai/plugins/blender)). Export depth, OpenPose and canny passes. Drive a video model with them (Wan VACE-class). Depth locks scene structure, OpenPose locks pose, canny locks silhouettes ([runcomfy Blender→ComfyUI](https://www.runcomfy.com/comfyui-workflows/blender-to-comfyui-ai-renderer-2-0-workflow-cinematic-video-output), [flick](https://flick.art/blog/blender-ai-filmmaking), [ComfyUI depth docs](https://docs.comfy.org/tutorials/controlnet/depth-controlnet)).
- **Verdict for Cutroom**: this is overkill for handheld UGC. A **real phone plate of the real room** gives the same lock for free, with a real camera shake. Keep it only for impossible shots (a product "hero orbit").
- **Fixes**: F7.
- **Evidence**: B (open workflows).
- **Cheapest test**: skip unless a hero-orbit shot is needed.

### 9. 3D garment tools (CLO3D / Browzwear / Style3D / Marvelous): evaluated and deprioritised
- These need pattern files (DXF) and a fabric-property setup per SKU. CLO's AI Studio composites a portrait or AI face onto a rendered garment ([CLO support](https://support.clo3d.com/hc/en-us/articles/33832336587545-AI-Render)). Marvelous Designer simulates fabric weight, stretch and stiffness per material ([toolworthy](https://www.toolworthy.ai/tool/marvelous-designer)). Shudu's creator says most brands lack 3D garments, so he shoots on a real model instead. **For a small streetwear brand, a body double (#1) beats a 3D garment twin on cost and realism.** Revisit only if SANTO's manufacturer already supplies CLO files.
- **Fixes**: would address F5 in theory. **Evidence**: B. **Cost**: licence plus hours per SKU.

### 10. FOOH / CGI-ad finishing checklist (what makes an inserted element "sit")
- **How pros finish** ([maverickframe](https://maverickframe.com/blog/what-is-fooh/), [dialect](https://www.dialectinc.com/thoughts/fake-out-of-home)): real plate first → camera track → match lighting direction and colour → **contact shadows** → reflections → grade → **matched grain** as the last step.
- Apply this to every Nano Banana composite and every Plate + Swap: check contact shadow under the product on the bed, light direction consistent with the window in the plate, then add grain after grading, not before.
- **Fixes**: F6, F7. **Evidence**: A (industry-standard VFX order).
- **Input change**: a QC checklist item "contact shadow present / light direction matches plate". The post chain orders `grade → grain → codec`.

---

## C. Performance capture from a phone

### 11. Tool routing for "real performance → AI character"
| Need | Best fit | Why / limits |
|---|---|---|
| Keep the real room, camera and product; swap who is on screen | **Wan Animate Replace** / **Genjutsu Object Swap** | Keeps the original camera and background; relighting LoRA; deformation if body shapes differ ([wanvideogenerator comparison](https://wanvideogenerator.com/blog/ai-motion-control-kling26-vs-wan22-animate), [fylia](https://fylia.ai/blog/detail/Motion-Transfer-Showdown-Kling-vs-Wan-Which-One-Nails-Your-Character-Animation-1403c7f44bf5/)) |
| Persona in a *new* generated scene copying a filmed move | **Kling 3.0 Motion Control** / Genjutsu Motion Transfer | Element Binding for face; "Match video" vs "Match image" orientation modes; ref 3–30 s ([Kling guide](https://kling.ai/quickstart/motion-control-user-guide)) |
| Change one element (colourway, outfit) in real footage | **Runway Aleph 2.0** | Up to 30 s at 1080p; drifts on occlusion or fast motion |
| Face acting and dialogue on a still persona | **Runway Act-Two** | Gesture control only with image input; face centred, shoulders up ([Runway help](https://help.runwayml.com/hc/en-us/articles/42311337895827-Performance-Capture-with-Act-Two)) |
| Talking head only | **Hedra Character-3** | Stiff full body, over-dramatic hands, "over-smiling, head tilting" ([magichour](https://magichour.ai/blog/guide-to-hedra-ai), [morphed](https://morphed.app/blog/hedra-alternatives)) |
| Not for realism | Viggle | Simple moves only; edge artifacts when clothing blends with background ([flowith](https://flowith.io/blog/viggle-ai-faq-motion-transfer-custom-characters-commercial-rights/)) |
- Kling's own report claims a large win rate over Act-Two ([Kling-MotionControl tech report](https://arxiv.org/html/2603.03160v1)). That is a vendor claim. **Fixes**: F9 (right tool first time), F1, F3. **Evidence**: A (vendor docs) / B (comparisons).

### 12. Phone plate / driving-video capture spec (consolidated from vendor docs)
Store this as the **Plate Spec** the app shows before upload, and auto-check what it can:
1. **One continuous shot, no cuts**, 3–30 s (Kling, Act-Two, Genjutsu all require this). Aim for 5–10 s per beat.
2. **Subject fully in frame the whole time.** For Kling, avoid camera movement in the motion reference ([Kling guide](https://kling.ai/quickstart/motion-control-user-guide)). For Wan Replace, handheld is fine because it keeps the camera.
3. **Hands visible, never in pockets or behind the back**, if the output needs hands ([atlascloud](https://www.atlascloud.ai/blog/guides/kling-ai-motion-control)). **Avoid hands crossing in front of the torso or limbs overlapping**, which Kling users call "spaghetti limbs" ([invideo](https://invideo.io/blog/kling-motion-control/)).
4. **Half-body is more stable than full-body.** Hands close to the lens fail in Wan (fingers blur and merge). Keep hand-product action at mid-distance ([wan-animate guide](https://wan-animate.com/posts/wan-2-2-animate-motion-types-style-consistency-guide)).
5. **Clothing contrasts with the background.** Fitted beats baggy for motion extraction ([Move AI via cgchannel](https://www.cgchannel.com/2023/11/move-ai-releases-move-one/), [Viggle](https://www.seedance.tv/blog/viggle-ai-motion-control-settings)). Note: SANTO hoodies are loose, so for *motion-transfer* references have the performer wear something fitted. For *Plate + Swap*, wear the real SANTO garment because the garment stays in the output.
6. **Even front or window light; no backlight; no harsh shadows** (Move One, Kling, Act-Two).
7. **Face**: for dialogue or Act-Two, face centred, shoulders up, looking at the lens, never leaving frame.
8. **Aspect ratio of the character image = aspect ratio of the reference video**. Character image framing matches the reference: full body if the motion is full body (Kling).
9. **Props**: "if your character holds objects, your performance should mirror that" (Runway). Hold the *real product* or a same-size stand-in.
10. **Body double build ≈ persona build** (Wan: no retargeting in Replace mode).
- **Fixes**: F1, F3, F4, F9. **Evidence**: A (vendor docs from several companies).
- **Input change**: plate upload form with checkboxes and auto-checks (duration, cut detection via scene-change, aspect-ratio match, face-in-frame ratio via face detection).
- **Cheapest test**: 0 credits. Re-shoot one existing motion-library clip to spec and compare the next Kling/Wan run against the old one.

### 13. Act the object, not the gesture
- **How**: for F3/F4 beats (ripping the mailer, pulling the hoodie over the head, zipping), the plate performer does the *real action with the real object*. Do not mime it and hope the model invents the object. Swap engines treat the held object as body geometry, which works for us when it's the real SANTO bag. When using prompts with Wan, name the interaction explicitly ("person tearing open a grey polyethylene mailer bag with both hands"). Wan docs say explicit object prompts beat inference from pose ([wan-animate guide](https://wan-animate.com/posts/wan-2-2-animate-motion-types-style-consistency-guide)).
- **Fixes**: F3, F4. **Evidence**: B.
- **Input change**: movement-library entries record `props_held[]`. The shot is refused if the storyboard prop ≠ library prop.

---

## D. Audio / voice realism (F8)

### 14. Perform first, convert second: human VO → speech-to-speech
- **How**: someone (Luca, the body double, any friend) records the script on an iPhone, conversationally, in a soft-furnished room. Settings: Voice Memos set to **Lossless** (Settings → Voice Memos → Audio Quality), phone **14–18 in (35–45 cm)** from the mouth, bottom mic toward the mouth, bedroom or wardrobe full of clothes ([Flare](https://joinflare.app/blog/ugc-audio-quality-no-pro-mic)). If the persona needs a different voice, run it through **Voice Changer / speech-to-speech**. It "preserves the original performance: emotions, timing, pacing and pronunciation" (max 5 min) ([ElevenLabs STS docs](https://elevenlabs.io/docs/api-reference/speech-to-speech/convert), [blog](https://elevenlabs.io/blog/speech-to-speech)). Higgsfield also has a `voice_change` tool (not called). Real breaths, "um"s, restarts and laughs come through intact, and those are the cues TTS fakes worst.
- **Fixes**: F8. **Evidence**: A (vendor docs); pros use STS to "infuse the performance" TTS cannot.
- **Input change**: `shot.vo_source` = human_recording | sts(persona_voice) | tts. Default to human_recording or STS for talking UGC. Store the raw take for lip-sync.
- **Cheapest test**: 0 credits for recording. STS on ElevenLabs costs about 1 min of credits on the free or starter tier.

### 15. Audio-first video: drive the video from the final VO
- **How**:
  - **Seedance 2.x** accepts up to **3 audio refs (@audio1–3), total ≤15 s, ≤50 MB each; MP3 is most reliable; trim refs to 3–8 s**. It uses them for rhythm, timing and lip-sync alignment ([cutout.pro](https://www.cutout.pro/learn/blog-seedance-2-0-audio-guide/), [seedance2pro](https://seedance2pro.io/blog/does-seedance-2-accept-voice-reference), [mindstudio](https://www.mindstudio.ai/blog/seed-audio-reference-seedance-video-generation-workflow)). Clean WAV behaved more predictably than messy phone-memo MP3s. **Long uneven silences can cause frozen frames**, so trim dead air to ≤0.4 s before upload ([ugccopilot](https://ugccopilot.ai/blog/seedance-2-native-audio-generation-guide/)).
  - **Length walls**: Seedance lip-sync is tight at the start of a 15 s clip but drifts by the end ([crepal](https://crepal.ai/blog/aivideo/blog-seedance-2-0-lip-sync-voiceover-fix/)). Kling 3.0 has a "**second-8 wall**" where lips and audio separate after about 8 s ([Maxfusion](https://maxfusion.ai/blog/ai-video-models-lip-sync-2026)). **Rule**: talking segments ≤8 s per generation. Word budget ≤12 words per 5 s, ≤20 words per 10 s ([atlascloud](https://www.atlascloud.ai/blog/tips/kling-ai-lip-sync)).
  - Generate **one continuous VO for the whole ad**, then slice it per shot. This avoids voice drift between shots, which Seedance docs flag as "jumps in pitch, speed… room sound… obvious at the cut" ([seedance.tv](https://www.seedance.tv/blog/how-to-keep-voices-consistent-in-seedance-2-5)).
- **Fixes**: F8, F9 (no rerolls for sync). **Evidence**: B (several practitioner guides agree).
- **Input change**: the storyboard stores `vo_master.wav` and per-shot `vo_slice` (start/end). The shot generator attaches the slice as the audio ref. It auto-splits any talking shot longer than 8 s.
- **Cheapest test**: one 6 s talking shot on Seedance with an audio ref (~18 credits) vs the same shot with native audio.

### 16. The lip-sync fix layer: settings that matter
- **Sync lipsync-2-pro** ([sync.so docs](https://sync.so/docs/compatibility-and-tips/improving-lip-sync-quality), [models](https://sync.so/docs/models/lipsync)):
  - `temperature` 0–1, default 0.5. Use **0.3 for subtle, casual UGC**; high values look like over-enunciation.
  - Face should be **20–40% of the frame**; input ≥480p.
  - The model generates the mouth region at **512×512**, so extreme close-ups (face over 50% of a 1080p frame) can look softer than the surrounding pixels.
  - Set `occlusion_detection_enabled: true` when a hand, hoodie drawstring, hair or product crosses the mouth. It is slower.
  - Extreme profile fails. Use one visible speaker, or speaker selection.
  - Ranking by testers: Sync-3 > Sync-2-Pro for angles, occlusion and close-ups. Kling lip-sync is "general-purpose, not avatar-optimised". Hedra is cheapest but over-smiles and misses complex phonemes ([veed ranking](https://www.veed.io/learn/best-lipsync-api), [magichour](https://magichour.ai/blog/best-ai-lip-sync-tools)).
- **Workflow**: generate the visuals silent or with native audio. If lips miss, re-sync with the *human VO* (#14) instead of rerolling the video.
- **Fixes**: F8, F9. **Evidence**: A (vendor docs) + B (comparisons).
- **Input change**: `lipsync.params {model, temperature: 0.3, occlusion: auto}`. The storyboard warns when the planned face size is outside 20–40%.
- **Cheapest test**: re-sync one existing clip that has bad sync (sync.so pay-per-second, pennies).

### 17. Make clean audio sound like a phone recorded it (the "acoustic fingerprint" chain)
- **Why UGC voice sounds fake**: AI audio has no room reverb, no mic colouration and no AGC/codec artefacts. It "exists in a digital vacuum" ([UncannyAI guide](https://uncannyai.io/blog/how-to-fix-ai-video-audio)).
- **Chain, in this order**:
  1. **Convolution** with a real small-room impulse response (bedroom or office). Not an algorithmic reverb plugin.
  2. **EQ**: high-pass about 120–150 Hz, low-pass or roll-off about 7–8 kHz to kill the "studio condenser" sheen.
  3. **Phone-mic/AGC behaviour**: fast compressor/limiter that pumps slightly.
  4. **Room-tone bed** at about −45 to −50 dBFS, recorded in the same real room as the plate.
  5. **AAC encode** (the codec signature).
  6. Optional micro pitch/level jitter.
  - UncannyAI productises this, including iPhone MEMS mic response, AGC and AAC ([uncannyai.io](https://uncannyai.io/)).
- **Cheapest, most authentic alternative: "worldizing"** (Walter Murch, *American Graffiti*). Play the clean VO through a small speaker in the real room and re-record it with the phone at the camera position. You get the real room and real mic "for free" ([filmsound.org](http://www.filmsound.org/terminology/worldizing.htm), [designingsound](https://designingsound.org/2012/12/31/analog-worldization/)).
- **iPhone gotcha**: iPhone 16+ "Audio Mix → **Studio**" mode *removes* reverb and background ([MacRumors](https://www.macrumors.com/how-to/iphone-16-edit-spatial-audio-in-video-audio-mix/)). That is exactly the wrong direction for UGC. Keep plate and room-tone recordings on **Standard**.
- **Fixes**: F8, F6 (audio is half of the "AI look"). **Evidence**: B (the vendor explains the mechanism; worldizing is a documented film technique).
- **Input change**: `room.impulse_response.wav` and `room.tone.wav` per real room. Capture an IR with a balloon pop or hand clap on the phone, 0 cost. Post chain: `vo → convolve(room IR) → EQ → comp → +room tone → AAC`, one preset per room.
- **Cheapest test**: 0 credits (ffmpeg `afir` + `highpass`/`lowpass` + `acompressor`). Blind A/B with 3 people.

### 18. Voice clone recipe that sounds casual, not narrated
- **ElevenLabs facts** ([IVC docs](https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/instant-voice-cloning), [PVC docs](https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/professional-voice-cloning)):
  - Instant clone: **1–2 min** of clean audio. **More than 3 min gives little gain and can hurt.**
  - Pro clone: **30 min minimum, 2–3 h ideal**. WAV at 44.1/48 kHz, 24-bit, **−23 to −18 dB RMS, true peak −3 dB**.
  - The clone **copies the style of its training audio**, so "if you have… many 'uhm's… the AI will mimic those". **For UGC, record the clone sample as relaxed talking to a friend**, not read-aloud narration. That makes casual delivery the model's default.
- **Eleven v3 prompting** ([v3 tags](https://elevenlabs.io/blog/v3-audiotags), [best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices), [tag reference](https://github.com/troykelly/hermes-voip/blob/main/docs/reference/elevenlabs-v3-audio-tags.md)):
  - Stability on **Natural** (or Creative for more emotion; Robust ignores tags).
  - Inputs **over about 250 characters** are more stable. A 15 s script is about 35–40 words ≈ 200–240 chars, right on the edge, so **generate the whole ad's VO in one call**, never line by line.
  - Use **1–2 tags max** from the safe set: `[laughs]`, `[sighs]`, `[clears throat]`, `[excited]`, `[whispers]`.
  - **Avoid `[pause]` and break tags**, which cause instability and speed-ups. Use "…" and em-dashes instead.
- **Fixes**: F8. **Evidence**: A (vendor docs).
- **Input change**: `persona.voice {provider, voice_id, clone_source: conversational, stability: natural}`. The TTS call always sends the full-ad script.
- **Cheapest test**: 0–1 credits (a free-tier ElevenLabs generation).

### 19. Native-audio prompting and the foley/music layer
- **Veo 3.x / Seedance native audio**:
  - Format dialogue as `Character says: …` (no quotes) and add **"(no subtitles)"**.
  - For phone intimacy: "**Ambient noise: close, dead room tone. No reverb.**"
  - Always state the background explicitly, otherwise models hallucinate things like a "live studio audience".
  - Keep ambience "low under the voice" and use **≤5 audio elements** ([Replicate Veo 3 guide](https://replicate.com/blog/using-and-prompting-veo-3), [Leonardo](https://leonardo.ai/news/how-to-prompt-audio-for-veo-3), [prompt-architects](https://prompt-architects.com/blog/150-prompting-audio-in-veo-3-1-sound-music-ambience)).
- **Foley sells state changes (F4)**:
  - Record the **real SANTO mailer tearing**, a zip, and a hoodie pulled over the head on the phone once, and reuse the files forever (0 cost).
  - If you must generate, the ElevenLabs SFX prompt should name material, size, distance and space. Use 10–60 words, 1–3 s duration, prompt influence default 30% ([ElevenLabs SFX docs](https://elevenlabs.io/docs/overview/capabilities/sound-effects)). Example: "thin grey polyethylene mailer bag torn open by hand, close phone mic, small carpeted bedroom".
- **Music / trending sounds**:
  - Trending consumer sounds are **not cleared for paid ads**, and boosting an organic post as a Spark Ad doesn't clear them.
  - Business accounts only see the **Commercial Music Library**. Original audio and voiceover are always safe ([Soundstripe](https://www.soundstripe.com/blogs/why-can-i-only-use-commercial-sounds-on-tiktok), [Third Chair](https://usethirdchair.com/blog/tiktok-commercial-library-what-brands-can-really-use)).
  - Fashion ads tend to work at **120–140 BPM**; rotate music every **7–14 days** ([TikAdSuite](https://tikadsuite.com/blog/best-music-for-tiktok-ads/)).
  - Higgsfield has `tiktok_music_trending` (not called). Check that its tracks are CML-cleared before paid use.
- **Fixes**: F8, F4. **Evidence**: A (Veo guides, TikTok terms) / B.
- **Input change**: a `sfx_library/` of real recorded foley per product action. Each music track gets `license: CML | original | royalty-free`, and export is blocked for paid placements otherwise.

---

## E. Product-photography conventions for the reference kit

### 20. Garment Reference Pack spec (what pros shoot per SKU)
Combined from Zalando's partner image guide ([apparel guide](https://partner.zalando.com/university/article/apparel-image-guide)), try-on vendors' input rules ([FASHN/Kolors via fal](https://fal.ai/explore/virtual-try-on-apis), [Botika](https://botika.com/products/on-model)) and e-com lighting practice:
1. **Views**: front, back, side packshot (whole garment, nothing cropped, no heavy folds, nothing overlapping). Add **ghost-mannequin or on-hanger** for structure (hoodies, jeans) and **flat lay** for print legibility. Ghost mannequin conveys shape and drape; flat lay is easier and better for reading the print ([wearview](https://www.wearview.co/faq/what-is-the-difference-between-flat-lay-and-ghost-mannequin), [weshop](https://www.weshop.ai/blog/ghost-mannequin-vs-flat-lay-which-one-makes-fashion-products-sell-better/)). Botika-style tools take **front + back** mannequin or flat-lay shots and claim "every stitch preserved".
2. **Detail macros** (Zalando "detail/informational view"): neck label or woven tag, print at 1:1, logo embroidery or puff texture, stitching or overlock, zip pull, cuff and hem, leggings waistband, denim rivets and back patch, hang-tag, mailer-bag print. These are the details models invent when they are missing (F2).
3. **Lens**: 50–100 mm full-frame equivalent. On a phone use the **2×/3× telephoto, not 0.5×/1× close up**, which stretches the edges ([replica surfaces](https://www.replicasurfaces.com/blogs/q-as/what-focal-length-lenses-minimize-distortion-in-flat-lay-photos), [pixel retouching](https://pixelretouching.com/best-lens-for-clothing-product-photography)). Keep the camera parallel to the surface and at the same distance for every SKU (tripod or boom).
4. **Colour**:
   - Continuous light **5600 K, CRI/TLCI ≥95**, large diffused softboxes ([Colbor](https://www.colborlight.com/blogs/articles/set-up-lighting-for-clothing-photography)).
   - **ColorChecker in the first frame of each session** → build a per-session camera profile → apply it to all shots. ΔE00 <1 is achievable ([X-Rite](https://www.xrite.com/service-support/color_management_workflow_with_dng_camera_profiles), [Lensrentals](https://www.lensrentals.com/blog/2019/07/how-to-use-an-x-rite-colorchecker-to-get-perfect-color/)).
   - Store the **measured hex/Lab per colourway**. AI tools render navy as black and flatten tonal prints ([metamodels](https://metamodels.ai/feeds/blog/ai-model-photography-what-fashion-brands-get-wrong)).
5. **Glossy surfaces** (plastisol or puff prints, the poly mailer): **cross-polarise**, with polariser film on the light and a CPL on the lens rotated to extinction. This removes glare and keeps texture. It costs about 1–2 stops of light and **needs its own colour profile** because the filters aren't neutral ([photographyattic](https://www.photographyattic.com/blog/2025/11/a-practical-guide-to-cross-polarisation-photography/), [xangle](https://xanglecs.com/doc16/photogrammetry/cross-polarization)).
6. **Label the role of each reference in the prompt**: "Image 1 = garment source (front), Image 2 = print detail, Image 3 = persona, Image 4 = room" ([apiyi](https://help.apiyi.com/en/nano-banana-pro-flat-lay-to-model-photo-apparel-workflow-en.html), [Leonardo](https://leonardo.ai/news/nano-banana-prompt-guide)). Nano Banana Pro accepts up to 14 refs.
- **Fixes**: F2 (main), F5 (on-hanger/mannequin shows drape), F9. **Evidence**: A (Zalando guide, X-Rite, several try-on vendors).
- **Input change**: `product.reference_pack` with required slots (front, back, side, flat, structure, macros[≥4], colour_hex, artwork[] for #6, optional scan for #7). Upload is rejected if it lacks a ColorChecker frame or was shot at 0.5×/1× below 60 cm (EXIF focal length check).
- **Cheapest test**: 0 credits. Re-shoot one hoodie to spec, then run the same Nano Banana composite with the old pack and the new pack (2 × 1.5 = **3 credits**).

---

## STOP DOING (with who says so)
1. **Generating garments on moving bodies for fit-critical beats** (leggings squats, denim walks, hoodie pull-on). Imma, Shudu, Miquela, Zara and Mango all keep the garment real. Mango's backlash was precisely about fit (#1, #4).
2. **Mimed prop actions in motion references.** Act the real object (Runway Act-Two docs, #13).
3. **Motion refs with hands in pockets, crossed arms, hands crossing the torso, or camera moves** (Kling docs and users, #12).
4. **Mixing generators within one ad for on-camera persona shots.** Coke's 70k clips across 3 models still read as inconsistent (#5).
5. **Rerolling a whole video to fix lip-sync.** Re-sync with lipsync-2-pro instead (#16). **Talking segments over 8 s per generation** (Kling second-8 wall, Seedance late drift).
6. **Line-by-line TTS and short TTS calls under about 250 chars**; overusing `[pause]` or break tags (ElevenLabs docs, #18).
7. **Cloning a persona voice from polished read-aloud audio** when the target is casual UGC. The clone copies the delivery style (#18).
8. **Algorithmic reverb on AI VO.** Use a real room IR or worldize (#17). Don't record plates or room tone with iPhone Audio Mix "Studio" mode.
9. **Trending TikTok sounds in paid ads.** They are not licensed; use CML or original audio (#19).
10. **Shooting references with the phone's wide lens up close**, without a colour target, or with glare on prints (#20).
11. **Expecting image-to-3D (`generate_3d`, Tripo, Hunyuan) to preserve logos.** Lighting is baked in and texel density is low. Use it for angles or blocking only (#7).
12. **Launching a persona without a likeness check** (Shein/Mangione, #3).

## Open questions
1. What does Higgsfield charge per second for Genjutsu Object Swap and Wan-class replace vs Kling 3.0 Motion Control? (Check via free `models_explore`; don't generate.) This decides whether Plate + Swap beats full-gen on credits as well as quality.
2. Can Wan Replace / Genjutsu be restricted to **head-only** so hands and garment pixels come through untouched? The Wan workflow exposes mask expansion; it is unclear whether Higgsfield exposes a mask.
3. How well does face swap hold when the performer pulls a hoodie over their head (face fully occluded, then revealed)? This is probably the hardest F1×F4 case. Test it early.
4. Can Seedance take the human VO as @audio **and** a persona image **and** a plate in one call, or does audio + video reference exceed the multimodal limits?
5. Automating logo patch (#6) headlessly: are CoTracker/OpenCV homographies good enough on cloth, or is Mocha-grade planar tracking needed?
6. Does SANTO's manufacturer have CLO/Browzwear files? If so, #9 becomes cheap for exact-colour, exact-print stills.
7. Legal/disclosure: do TikTok and Meta AI-content labels apply when only the face is synthetic on a real plate? H&M watermarks all AI twin content.

---

# PART 10 — `08-podcasts-youtube.md`

## 08 — Podcasts & YouTube: what practitioners say they actually do

Researcher: podcasts/YouTube track. Date: 2026-09-24.

## How this was sourced (read this first)
- YouTube, podcast platforms, transcript sites, jina, invidious and piped are all blocked (checked: HTTP 000). There are no direct transcripts.
- The best route in turned out to be **GitHub repos that transcribe or extract YouTube videos**:
  - `nick-choudhary/higgsfield-ai-youtube-skills`: PLAYBOOK.md files extracted from 23 videos on the **official Higgsfield AI YouTube channel** (descriptions, linked prompt articles, spoken briefs, "key learnings"). It is cloned at `repos/higgsfield-ai-youtube-skills/`.
  - `joebenscoter86/higgsfield-ugc-workflow`: the long-form GUIDE.md that goes with the Higgsfield UGC reel/video `gUafcCMHClQ`. Another researcher already cloned it as `repos/joebenscoter86_higgsfield-ugc-workflow`.
- Everything else comes from WebSearch summaries of video pages, show notes and write-ups of talks. When a claim comes from a search summary and not from a primary text, I say so.
- The "Existing" tag means the idea is on our known list (BRIEF). It is included only because the source gives specifics we did not have.

---

## TECHNIQUES

### 1. The "cheap stills first, one paid video" pipeline, with specifics (Existing: storyboard gate, but new details)
- **How**, as the Higgsfield agent run was reverse-engineered by Joe Benscoter (companion to YouTube `gUafcCMHClQ`):
  1. **Product profile.** This is a clean product image plus the *exact physical usage steps*, which become the on-camera actions. Hoodie example: "pull over head, tug hem down, push sleeves up".
  2. **One-page brief** with a 3-cut map: **tight selfie hook → macro hands-on-product → wide recommendation**. The tight/macro/wide rhythm stops a 10–15 s clip from feeling static.
  3. **Base character portrait: person only, NO product.** Quote: "Do not put the product in this image… it actually causes the product to drift and warp in the later steps."
  4. **One wide image with 3 vertical storyboard panels** (tight / macro / wide), generated with the portrait and product as refs. Check that all 3 panels show the same face and product, and regenerate if two panels look alike.
  5. **Script with phonetic spellings** (see T14), which always includes "no subtitles".
  6. **Seedance video with exactly 3 refs**: storyboard sheet + face + product. Voice, lip-sync and room sound come in one pass.
  7. Captions and music are added locally afterwards.
- **Numbers.** "About 67 credits at 720p. At this phone-selfie style, 1080p costs about twice as much and looks no different." Wall-clock time is bound by audio synthesis, so a lower resolution is cheaper but not faster.
- **Fixes:** F1, F2, F8, F9.
- **Evidence:** B. One practitioner, with a worked example repo (surfboard ad). It is derived from Higgsfield's own agent run. https://www.youtube.com/watch?v=gUafcCMHClQ · https://github.com/joebenscoter86/higgsfield-ugc-workflow
- **Input change for Cutroom:**
  - Store a `usage_steps[]` field per SKU.
  - Forbid the product in the identity portrait.
  - Make the **approved 3-panel storyboard sheet itself a required reference** on the video call, not just a gate.
  - Default to 720p for close/selfie shots.
- **Cheapest test:** Same brief, 2 runs. Run A: current refs. Run B: portrait without product + storyboard sheet as the 3rd ref. About 2×Nano Banana (≈3 cr) + 2×Seedance (≈36 cr).

### 2. Grey-background asset sheets + "face erase" on multi-view sheets
- **How.** This comes from official Higgsfield videos: "3-Step Workflow to Make Ultra-Realistic AI Ads", "5-Step 4K short films" and the VFX-challenge episode.
  - Build every asset on **plain solid grey** before any video:
    - **Product sheet:** `Make a product sheet with front and 3/4 perspective views of the [product] from @image_1.`
    - **Character sheet:** split-frame. Left is a face close-up. Right is full-body **front + back** views, "matched in framing, scale and lighting", with "vertical divider lines separating each view".
  - Then run the edit **`Erase the face from the full-body shot on the right panel.`** so the sheet carries only ONE face for the model to lock onto.
  - Outfit variants are made by editing the sheet ("Edit this character sheet so he's wearing…"). Do not regenerate it.
- **Their key learnings, quoted:** "Grey background assets are the single highest-leverage consistency technique." "Always erase extra faces from multi-view sheets." "Consistency lives in the stills, not the video model."
- **Fixes:** F1, F2.
- **Evidence:** A. Repeated across several official Higgsfield channel videos. https://www.youtube.com/watch?v=3rDs6FhFoUQ · https://www.youtube.com/watch?v=HSON-SoFz7s · playbooks in `repos/higgsfield-ai-youtube-skills/`
- **Input change for Cutroom:**
  - Per model (person): a grey sheet with a face panel plus faceless front/back full-body panels.
  - Per garment: a grey product sheet (front, 3/4, back, detail).
  - Keep these sheets separate from the "look" start frames.
- **Cheapest test:** Make both sheets for 1 model + 1 hoodie with Nano Banana (~4 edits ≈ 6 cr). Rerun one known-failing shot with the sheets swapped in for the raw photos (≈18 cr).

### 3. "Positive Locks" + an identical technical header on every shot
- **How.** Every Seedance prompt in the official videos ends with a **POSITIVE LOCKS** block that states what must stay identical. For example: "Only the man is replaced; his face, hair… and jacket logo stay 100% consistent with @ref in every frame". Every character line ends with "100% matches the reference."
  - The **same technical/style header** is pasted on every scene of a project.
  - **Exact shot counts** go in the technical block ("exactly four cuts"). Quote: "Exact shot counts in the technical block stop over-generation."
  - Quote: "Positive locks (what must stay identical) outperform negative instructions." Emotion is "written beat-by-beat, never via negative prompts."
- **Fixes:** F1, F2, F7, F9.
- **Evidence:** A. Official Higgsfield channel, several episodes (car commercial `GNxmt_4IifA`, VFX challenge, Santiago film `0HIRIT7px9Y`).
- **Input change for Cutroom:** A per-project frozen header plus a per-shot auto-generated POSITIVE LOCKS block, built from SKU fields (logo text, print position, colourway, stitching) and the model's identity markers. Do not use negative prompts for identity or product.
- **Cheapest test:** A/B on one shot with a negative-list prompt vs a positive-locks prompt (2×18 cr).

### 4. Give every reference a named role; max 2 people
- **How.**
  - Tag each upload (`@hero`, `@hoodie_front`, `@room`, `@video1`, `@audio_1`) and write one line per tag that says what it controls.
  - The official v2v prompt writes `@video1 — source footage: master for camera, framing, focus, motion, expression timing, background, lighting, grain and duration.`
  - "Seedance 2.0 Is INSANE… But There's a Catch" warns that without roles "your character reference becomes a background and your style reference becomes a character", and that "three or more characters = faces drift, bodies warp… keep it to two max".
  - Curious Refuge gives the Omni caps: 9 images, 3 videos, 3 audio.
- **Fixes:** F1, F2, F7.
- **Evidence:** B. https://www.youtube.com/watch?v=gDP4bkeWbUs · https://curiousrefuge.com/blog/how-to-use-seedance-2-omni
- **Input change for Cutroom:** The reference store needs a `role` enum (identity / wardrobe / product / location / motion / voice / style). The prompt builder emits the role line automatically. Block more than 2 people per shot.
- **Cheapest test:** 0 cr (a prompt-builder change). Validate on the next scheduled shot.

### 5. The target frame beats the text: a costume/product lock in words loses to a contradicting still
- **How.** From the official Higgsfield animation breakdown, quoted: "Written costume locks lose to a camera still that contradicts them. Put the headphones in the target frames."
  - For SANTO, the start frame, the end frame and each storyboard panel must *show* the correct garment state: logo side, tag, colour, hood up/down. Describing it in the prompt is not enough.
- **Fixes:** F2, F4.
- **Evidence:** B. https://www.youtube.com/watch?v=reFzEtCG_m8
- **Input change for Cutroom:** A QC gate on stills, where the garment in every frame fed to video is checked against the SKU sheet *before* spend.
- **Cheapest test:** 0 cr (review rule). Optionally, one Nano Banana correction (1.5 cr).

### 6. Print/text survival rule: short text survives, long text dies, so pre-blur small print, and use a numeric print-lock checklist
- **How.**
  - The car commercial episode, quoted: "Short text on props survives; long text dies. Pre-blur small print."
  - In the official apparel (HIGGS jersey) Meta-ads episode, reviewers "reject a take that morphs clothes on screen, drops 54 / 001 / 246, or adds extra people". Each garment has a short list of must-survive marks that gets checked on every take.
  - For SANTO:
    - Keep the big chest logo sharp in the references.
    - **Blur care labels, size tags and tiny woven text in the reference image**. Otherwise the model invents garbled text.
    - Show the real tag only in a real macro insert.
- **Fixes:** F2.
- **Evidence:** B. https://www.youtube.com/watch?v=GNxmt_4IifA · https://www.youtube.com/watch?v=BTfEd6vVTKA
- **Input change for Cutroom:** A per-SKU `must_survive_marks[]` (e.g. "SANTO wordmark chest, left-sleeve tab") used for auto-QC, and an auto-blur step for small text in product refs.
- **Cheapest test:** Pre-blur the tag on one product ref, then 1 Seedance run vs baseline (≈18 cr). Count invented text.

### 7. Hidden-cut state changes with timed windows behind an occluder
- **How.** This is the official HIGGS jersey Video 1: "Elevator, 13s. One woman, three looks. **Hidden cuts inside passing floor slabs.** Outfit order `@Image 2` 0–3s → `@Image 1` 4–6.5s → `@Image 3` 7.5–13s."
  - "Outfit changes only while a slab covers the body. A visible morph is a failed take."
  - Each state has its own reference image and an explicit second window, with a ~1 s occluded gap between windows.
- **Fixes:** F4.
- **Evidence:** B. Official channel, with the exact timing published. https://www.youtube.com/watch?v=BTfEd6vVTKA
- **Input change for Cutroom:** The state-change shot type gets fields for `states[] {ref_image, t_start, t_end}` and `occluder` (door frame, hoodie pulled over the camera lens, a hand covering the lens, a whip-pan). The prompt builder writes the timeline.
- **Cheapest test:** A 2-state hoodie-on shot (hood down → hood up) with a hand-over-lens occluder: 1 Seedance run (≈18 cr).

### 8. Film the hard action for real on a phone, then v2v-replace only what must change
- **How.** Hard actions are ripping the mailer, pulling the hoodie on, zipping and folding. Several independent tools and creators converge on this:
  - **Seedance 2.5 v2v prompt (official, VFX-challenge episode):** sections SCENE CONTEXT / ACTIVE REFERENCES / EDIT INSTRUCTION / PHYSICS / LIGHTING / WARDROBE / STYLE / POSITIVE LOCKS. Key lines:
    - "inherits his exact performance frame by frame… same mouth aperture and blink timing… Silhouette scale and screen position match the original at every frame."
    - "grain, motion blur, focus falloff, compression character and color match @video1 so the replaced man is indistinguishable from originally shot footage."
    - "every pixel outside the replaced man remain exactly as in @video1."
  - **Higgsfield Genjutsu Object Swap:** launched 2026-09-01. It replaces one element (person, outfit or product) and keeps the rest. Clips run up to 30 s. Limits: "Faces, small text, hands, occlusions… can still drift", and source quality matters a lot.
  - **Kling Motion Control workflow** (Julian Goldie / Alici write-ups of the YouTube tutorials):
    1. Screenshot frame 1 of your phone clip.
    2. In Nano Banana/GPT, "replace the person with a UGC-style avatar with the same lighting and background".
    3. Feed that image + the clip to Motion Control.
    - Filming rules: solid-colour clothes, plain wall.
  - **Higgsfield Recast** takes 5–15 s source clips.
- **SANTO-specific variant (the strongest):** a stand-in wears the **real SANTO garment** and rips the **real mailer**, filmed on a phone. Then v2v replaces only the face/identity. The product, hands and fabric physics stay real footage, so F2, F3 and F5 largely go away.
- **Fixes:** F3, F4, F5, F6 (and F2 when the product stays real).
- **Evidence:** A (official Higgsfield video + vendor docs + multiple tutorials). https://app.therundown.ai/guides/swap-the-product-and-keep-the-performance-with-higgsfield · https://higgsfield.ai/blog/higgsfield-genjutsu · https://www.youtube.com/watch?v=Utono2euM24 · https://www.youtube.com/watch?v=mYL2ETf5zRI
- **Input change for Cutroom:**
  - A "real-capture" shot type: upload a phone clip (≤15 s, 1080p, 30 fps, even light) + an identity ref.
  - A v2v prompt template with the sections above.
  - A choice between "replace person" and "replace object".
- **Cheapest test:** Film a 5 s mailer rip on a phone (0 cr). Run 1 Wan 3.0 / Kling motion-control swap (≈3.5–? cr), then 1 Seedance v2v (≈18 cr), and compare.

### 9. Blockout-driven generation: a greybox or phone rehearsal carries the timing, references carry the look
- **How.** This is from the official "How To Save AI Credits With Higgsfield + Blender" (2026-08-28, 19:48).
  - "Lock camera, cuts, and timing first. Spend credits only after the move is already right."
  - Render the blockout at the final duration (1920×1080, 24 fps). Attach it as `@Video 1` + character/location stills.
  - Ask the LLM: "Write a 30-second Seedance prompt based on this video blocking. Read the input video and write out the prompt second by second to match the camera moves in the clip."
  - Quote: "Greybox = timing and path. References = identity and set. **Mixing those jobs in one text prompt is how seats swap and hands melt.**"
  - Product proxies get no faces and no hands. Leave liquids/sims as black gaps for the model to fill.
- **For Cutroom**, the "blockout" can be a 10-second phone rehearsal in the real room, not Blender.
- **Fixes:** F3, F4, F7, F9.
- **Evidence:** B. https://www.youtube.com/watch?v=OiULPvTJ-0E
- **Input change for Cutroom:**
  - Movement-library entries must be stored **at the final shot duration** with a machine-written second-by-second action transcript.
  - The prompt builder derives timing from the clip, not from free text.
- **Cheapest test:** Rehearse 1 shot on a phone (0 cr). Have the LLM write a per-second prompt (0 cr). Run 1 Seedance ref-video gen (≈18 cr).

### 10. Hand-motion reference clips: bare hand, plain background, 3–8 s, one move
- **How.**
  - The Seedance video-reference tutorials say a simple clip of "just your hand, plain background, steady light" lets Seedance "lock onto the motion in a way words alone hadn't".
  - "Shorter clips of 3–8 seconds with a single clear camera move replicate most accurately."
  - The reference video controls motion only. The text and image refs define the look.
- **Fixes:** F3.
- **Evidence:** B/C. Tutorial `ikPGQGoUjQ0` plus WaveSpeed/NemoVideo write-ups, search summaries only. https://www.youtube.com/watch?v=ikPGQGoUjQ0 · https://wavespeed.ai/blog/posts/blog-how-to-use-seedance-2-0-reference-video/
- **Input change for Cutroom:** Movement-library capture spec: 3–8 s, one action, one camera move, plain background, even light, the real product in hand.
- **Cheapest test:** Film one grip clip (0 cr) + 1 Seedance gen (≈18 cr).

### 11. Scale lock with a "size-fit frame" or scale sketch
- **How.**
  - Official episodes feed a **pencil scale sketch** or "size-fit frames" as a reference "so height difference never drifts". The love-story film used this for giant vs boy, the VFX challenge for rider vs dragon.
  - For SANTO, use a still of a hand holding the folded tee or mailer at true scale (real photo), labelled as the scale reference.
  - A search summary adds: say "correct scale" and "natural grip" explicitly, and "human + product is where Nano Banana struggles most". Fix those stills in Photoshop; the official animation team lists "Hand correction: Photoshop" as a pipeline step.
- **Fixes:** F3.
- **Evidence:** B. https://www.youtube.com/watch?v=QfylrxtQSSs · https://www.youtube.com/watch?v=reFzEtCG_m8
- **Input change for Cutroom:** Each SKU stores a real "in-hand at true scale" photo, tagged `role=scale`. Add a manual hand-retouch step on start frames before video.
- **Cheapest test:** 0 cr for the photo. 1 Seedance gen with vs without the scale ref (≈36 cr).

### 12. Hybrid face trick (paste real, don't regenerate)
- **How.** Official love-story episode (500M views): "generate costume and body first, **erase the head, paste the real photo onto the portrait panel**. Faces read as the actual people, not lookalikes."
  - The same logic applies to product. Composite the **real product photo** into sheet panels rather than letting the image model redraw the garment.
- **Fixes:** F1, F2.
- **Evidence:** B. https://www.youtube.com/watch?v=QfylrxtQSSs
- **Input change for Cutroom:** A sheet-builder step that composites real face/product crops into generated sheets (needs local image ops, not a model call).
- **Cheapest test:** 0 cr (Photoshop/PIL composite) + 1 Seedance gen (≈18 cr).

### 13. Clean, fixed location plates with everything baked in; light fixed to the world
- **How.** From the official episodes:
  - "Clean every plate. Anything the model can break will break."
  - "Bake crowds into the location plate so background extras never turn to mush."
  - The harbor plate has a "sun position fixed so light stays consistent across generations".
  - "Light is world-fixed. Faces move through the key. Do not parent the key to the character."
  - "3/4 angle locations give the camera room to move without breaking continuity."
  - For SANTO:
    - Photograph the real room from a 3/4 angle.
    - Remove posters, jewellery and clutter you don't want reinvented, or keep them and accept they must stay put.
    - Reuse the same plate for every shot in that room.
- **Fixes:** F7, F6.
- **Evidence:** B/A (multiple official episodes). https://www.youtube.com/watch?v=GNxmt_4IifA · https://www.youtube.com/watch?v=QfylrxtQSSs
- **Input change for Cutroom:** Room plates stored as `role=location` with a "cleaned" flag, a camera-angle note and a light-direction note. The same plate ID is reused across a whole ad.
- **Cheapest test:** Clean one real-room photo in Nano Banana (1.5 cr) and rerun a warping shot (≈18 cr).

### 14. Phonetic spelling in the spoken line only, correct spelling in captions, "no subtitles"
- **How.**
  - Seedance voices the literal text. Real failures from Benscoter: `nustandardlabs` was read letter by letter, so it was respelled `Noo Standard Labz` ("Labs" came out "labbers" until spelled "Labz"). `vial` was read "vawl", so it was respelled `vile`.
  - The official HIGGS video does the same: "Brand spoken /hɪgz/, written Hig's."
  - Keep the real spelling in the burned-in captions. Always include "no subtitles" in the prompt or the model burns its own captions.
  - For SANTO, test "SAHN-toh" vs "Santo" vs "San toe".
- **Fixes:** F8.
- **Evidence:** A/B (two independent sources). GitHub guide above · https://www.youtube.com/watch?v=BTfEd6vVTKA
- **Input change for Cutroom:** A per-brand `pronunciation_map` applied only to voice text, with a mandatory human "brand name heard correctly" check after each generation.
- **Cheapest test:** 3 phonetic variants in the cheapest audio-capable model (Wan 3.0 ≈3.5 cr each) before any Seedance spend.

### 15. Audio: name the sound, no music in-model, reuse a voice via audio reference
- **How.**
  - Krea's Seedance 2.5 UGC guide: "name the sound you want, because an unspecified track comes back **scored like a commercial** and stops reading as UGC."
  - The official style header on every scene reads "Audio: Diegetic dialogue and environmental SFX only. No music. No subtitles." Animation episode: "No music in Seedance. Score in the edit."
  - Use an `@audio_1` voice reference to keep one voice across a campaign. Official: "Audio reference is the only reliable way to keep a hummed melody on pitch." The jersey unboxing used `@audio_1` VO with exact lines.
  - Face + voice refs are "the consistency lock" for talking heads. Review lip-sync and face match before spending on the rest of the take list.
  - Speaking practitioners: **Barry Hott** runs an ad that is "my voice done by AI on another character" with no comments suspecting AI. **Dara Denney** says AI voiceovers can be indistinguishable, while full AI avatars still get punished.
  - Curious Refuge on Seedance Omni performance: "the delivery is super robotic… hard to get a nuanced performance".
- **Fixes:** F8, F6.
- **Evidence:** A. https://www.krea.ai/blog/seedance-2-5-makes-a-full-30-second-ugc-ad-in-one-shot-2026-guide · https://www.youtube.com/watch?v=reFzEtCG_m8 · https://www.youtube.com/watch?v=NuvA32_dmtg · https://www.youtube.com/watch?v=6jvIXIjieyA
- **Input change for Cutroom:**
  - Every prompt gets an explicit `audio:` line naming the room tone and foley (paper-mailer rip, fleece rustle, zipper).
  - Hard-code "No music. No subtitles."
  - Store 1–2 real recorded voice clips (a consenting person) as `role=voice` refs, and prefer real recorded VO over TTS for hero lines.
- **Cheapest test:** The same 5 s shot with vs without the named-foley line (2×Wan ≈7 cr).

### 16. Generation-loss finishing: grain 2–3%, 30 fps, messenger recompression, fix the first frame
- **How.**
  - desightstudio's "4 Edits in 2 Minutes":
    - **Film grain 2% baseline, 3% in darker scenes**, back down in bright ones (mimics sensor noise).
    - Add ambient room audio.
    - Re-encode **1080p / 30 fps / H.264 / medium bitrate** ("real phone videos typically use 30 fps").
    - **Re-upload through the Telegram Bot API** to pick up the compression that real UGC gets from being shared through messengers.
  - Curious Refuge: "**Seedance often has higher exposure for the first frame** and Runway over-saturates". Fix in post: trim or grade the first frames. Topaz is their upscaler of choice "most true to the original".
  - Another write-up: "a light blur to kill the artificial sharpness, fine grain…"
- **Fixes:** F6.
- **Evidence:** B/C (article + Curious Refuge). https://www.desightstudio.com/en/insights/make-ai-videos-look-real-4-edits-in-2-minutes · https://curiousrefuge.com/blog/how-to-make-realistic-ai-videos
- **Input change for Cutroom:** Deterministic ffmpeg finishing:
  - trim the first ~3–5 frames or match their exposure;
  - slight blur/unsharp inverse;
  - grain 2% (3% below a luma threshold);
  - fps → 30;
  - H.264 at a phone bitrate;
  - optionally a second lossy re-encode pass.
- **Cheapest test:** 0 cr. Run it on existing rejected clips and blind-rate them.

### 17. Floaty/slow-mo motion: retime in post with the audio detached, and prompt for friction
- **How.**
  - Speed clips up in post, but because Seedance generates synced audio, "speeding the clip with that audio attached shifts its pitch upward. Detach or mute the audio, retime the video only, then re-lay the original sound at normal speed."
  - Prompt fixes for floaty motion: "steady speed", "gentle ease-out", and naming surfaces with friction ("rough linen, grippy rubber mat"). Flat backgrounds and ambiguous depth cause "floaty, warpy weirdness".
  - Comparison test: Seedance handheld "a tad floaty, like a phone gimbal trying too hard"; Kling handheld "weightier with micro-jitters that read like real camera shake".
- **Fixes:** F6, F9.
- **Evidence:** C/B (search summaries of practitioner blogs). https://crepal.ai/blog/aivideo/blog-seedance-2-0-vs-kling-ai-marketing-videos/ · https://sagnikbhattacharya.com/blog/fix-bad-motion-seedance
- **Input change for Cutroom:** A finishing option "retime 1.1–1.2× video-only". Keep the audio at 1.0× or re-lay room tone. Route "handheld walk-and-talk" shots to Kling.
- **Cheapest test:** 0 cr (post on existing clips).

### 18. Unglamorous identity refs; never use a cinematic style header for UGC
- **How.**
  - Krea: "The actor should be deliberately unglamorous with bare face and natural morning light, as **anything that reads as a studio portrait will produce an ad that reads as an ad**."
  - Starpop (David Ishag, weeks of testing): prompting Seedance "like a trailer or brand film… may look impressive but perform poorly as UGC". Sora 2 gave "a studio vibe instead of authentic UGC, with product sizing that's a bit off".
  - Contrast with Higgsfield's own *cinematic* ad episodes, whose headers say "85mm portrait lens, shallow depth of field", "8K IMAX", "ARRI". These are exactly the F6 triggers, so do not reuse those headers.
  - Keep the grey identity sheet neutral, but make the **start frame** a phone-look still. Other phone-look cues: "front-facing phone camera with slight wide-angle distortion", visible defects "focus hunting, auto-exposure shifts, imperfect framing — not an abstract adjective", "no excessive depth of field".
- **Fixes:** F6.
- **Evidence:** B. https://www.krea.ai/blog/seedance-2-5-makes-a-full-30-second-ugc-ad-in-one-shot-2026-guide · https://starpop.ai/blog/articles/seedance-2-vs-sora-2-ugc
- **Input change for Cutroom:** Two separate reference kinds: `identity_sheet` (neutral grey) and `start_frame` (phone-look: bare skin, window light, deep focus). A lint check rejects "85mm/bokeh/cinematic/ARRI/IMAX" in UGC prompts.
- **Cheapest test:** Start frame "studio" vs "bare-face morning window light" (2 Nano Banana ≈3 cr) → 2 Seedance (≈36 cr).

### 19. Face-consistency reference-pack rules (and Soul ID training specifics)
- **How.**
  - **Seedance pack** (WaveSpeed guide surfaced in the Tim Simmons search):
    - **3 stills max**: straight-on, 3/4, profile.
    - Same session and lighting.
    - **Same expression in all** ("too much expression variety causes the model to pick a midpoint face").
    - Simplify the background.
    - "Desaturate skin slightly if tone keeps drifting".
    - If the jawline won't hold, lean on hair shape, ear jewellery and wardrobe fit, since viewers read identity from those at distance.
  - **Soul ID** (official):
    - 20+ photos (min ~5, up to 80).
    - No sunglasses, heavy shadows or cropped faces.
    - At least one full-height photo for body proportions.
    - Photos from the last 4–5 months.
    - Training takes ~3–5 min.
- **Fixes:** F1.
- **Evidence:** B (WaveSpeed guide, attributed only indirectly to Tim Simmons) / A (Soul ID docs). https://wavespeed.ai/blog/posts/blog-character-consistency-seedance-2-0/ · https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-create-and-use-a-soul-id-character
- **Input change for Cutroom:** A model-ref validator: ≤3 stills to the video model, matched expression and lighting, plus one full-body photo in the Soul ID set.
- **Cheapest test:** 0 cr to re-pick refs + 1 Seedance run (≈18 cr).

### 20. Budgeting reality and shot iteration discipline
- **How.**
  - **PJ Accetturo** (Kalshi NBA Finals spot, interviews and thread): **300–400 Veo 3 generations for 15 usable clips (~25 takes per kept shot)**, $2k, 2–3 days.
    - He asks the LLM for "**no more than 5 prompts at a time**" because quality dips beyond that.
    - "Each prompt should fully describe the scene **as if the model has no context of the shot before or after it**. Re-describe the setting, the character, and the tone every time."
  - Official Higgsfield:
    - "Batch 3–4 takes per scene and stitch the keepers."
    - "Generate the anchor shot (dialogue or position lock) first."
    - "Split overloaded prompts."
    - "Iterate only the failing shots; do not regenerate the whole sequence."
    - "Credits burn fast on long complex shots. Spot slop early."
  - Benscoter: fix cheap things (profile, portrait, storyboard, script) and "you usually nail the video on the first paid try".
- **Fixes:** F9.
- **Evidence:** A. https://www.thedaringcreatives.com/creator-stories/pj-ace-nba-finals-ad/ · https://threadreaderapp.com/thread/1932893260399456513.html · official playbooks
- **Input change for Cutroom:** Treat each shot prompt as standalone (no "same as before"). Cap LLM batch size at 5. Track takes-per-kept-shot as a KPI per shot type to predict cost.
- **Cheapest test:** 0 cr (a logging change).

### 21. Model routing evidence from reviewers
- **How.**
  - **Curious Refuge head-to-head:**
    - Seedance "physics feel stronger… especially in bigger physical actions".
    - But "Seedance currently outputs at 720p, while Kling 3.0 supports 1080p, so Kling has the edge in overall sharpness… even with upscaling, Seedance doesn't fully recover tiny details".
    - Background faces and small elements get messy on both.
  - **Official:** "4K holds detail in wide shots where 1080p collapses."
  - **Krea:** Seedance 2.5 30 s renders took **10m48s–22m03s**.
  - **EP (X article, Higgsfield partner):** with Seedance 2.5, "most revisions needed only in the first or second generation".
  - **Comparison summaries:** Veo 3.1 has the edge for photoreal talking head. Kling is cheapest for stable presenter shots and b-roll. Seedance leads for product demos from refs.
  - **Practical routing:**
    - Close selfie/talking head → Seedance 720p.
    - Wide shots where logo detail matters → higher res or Kling 1080p.
    - Handheld walking → Kling.
    - Big physical action (rip, pull-on) → Seedance.
- **Fixes:** F9, F2, F6.
- **Evidence:** B. https://x.com/CuriousRefuge/status/2024950081380909547 · https://curiousrefuge.com/blog/how-to-use-seedance-2-omni · https://x.com/eptwts/article/2085439131887550534
- **Input change for Cutroom:** A routing table keyed on (framing, action size, logo-detail-needed, talking?).
- **Cheapest test:** One wide logo shot in Seedance 720p vs Kling 1080p (≈18 + Kling cost).

### 22. Direct the performance explicitly (against "dead" AI acting)
- **How.**
  - Official acting lines reused on every scene: "micro-pauses before reactions, precise eye-line, living eyes with catch-lights, chest rise from breathing. Characters never standing still, always reacting." "Every person moving from frame one."
  - The animation team on subtle acting: "Push one facial feature per beat. Keep the face asymmetrical."
  - Skin: "Pore-level realism — vellus hair, asymmetric moles, capillary flush."
- **Fixes:** F6, F1.
- **Evidence:** B (official channel, but cinematic context, so the camera lines are unsuitable).
- **Input change for Cutroom:** A per-beat `performance` field (one facial action per beat) + a standard "alive" line. Drop the cinematic camera lines.
- **Cheapest test:** A/B one talking shot (2×18 cr).

### 23. Use the video model as a multi-angle still generator
- **How.** Official car-commercial episode: "Seedance can serve as an image editor: generate a multi-angle static video, screenshot the frames, **they match perfectly**." This gives you perfectly consistent turnaround stills of person+garment from one generation.
- **Fixes:** F1, F2.
- **Evidence:** B/C (one official episode, no numbers). https://www.youtube.com/watch?v=GNxmt_4IifA
- **Input change for Cutroom:** An optional "turnaround" job: a slow orbit of the model wearing the SKU, with frames extracted as the storyboard-panel source.
- **Cheapest test:** 1 Wan 3.0 orbit (≈3.5 cr) → extract frames (0 cr) → judge consistency.

### 24. Strategy from creative strategists: use AI where it isn't the face of the claim
- **How.**
  - **Dara Denney** (Motion, 100K YouTube): "avoid AI UGC avatars except for voiceovers… 99% of brands still get punished by audiences for full AI avatars", while AI VO can be indistinguishable.
  - **Barry Hott** (Motion talk "How to Make AI Native Ads Look Human"): there are two kinds of AI content, one trying to look human and one leaning into the weird, and both work if people want to consume it. His playbook: voice-clone real VO, mix B-roll, amplify founder stories, and escalate to "shakier cameras, weirder takes, messier delivery".
  - A hybrid pattern reported in the search: take a real creator's 30 s testimonial, **cut every 4–6 s**, and fill the cuts with AI b-roll matched to the line.
- **Fixes:** F1, F6, F8 (by avoiding the hardest AI shot).
- **Evidence:** B/C (spoken opinions, no numbers shown in what we could access). https://www.youtube.com/watch?v=6jvIXIjieyA · https://motionapp.com/library/expert/dara-denney/
- **Input change for Cutroom:** A template where a real 15 s talking track is cut every 4–6 s into AI try-on/product b-roll. Cutroom generates only the b-roll.
- **Cheapest test:** 0 cr (edit existing real footage) + 2–3 b-roll shots (≈36–54 cr).

---

## STOP DOING (what pros say hurts quality or burns credits)
1. **Putting the product into the base identity portrait.** It makes the product drift and warp later (Benscoter).
2. **Uploading references without role labels, or putting 3+ people in a shot.** Roles get swapped and faces and bodies warp ("Catch" video).
3. **Using negative prompts for identity, emotion or product fidelity.** Use Positive Locks and beat-by-beat emotion instead (official).
4. **Letting the model add music or captions.** Always "No music. No subtitles." Score and caption in the edit (official + Benscoter).
5. **Leaving the soundtrack unspecified.** It comes back "scored like a commercial" (Krea).
6. **Using cinematic headers for UGC** (85mm, shallow DOF, ARRI, IMAX, "high-end commercial look"), studio-portrait actor refs, or trailer-style prompting (Krea, Starpop).
7. **Expecting long or small text to survive.** Pre-blur small print. Only short, bold marks hold (official).
8. **Describing the garment in words while the start/storyboard frame shows it differently.** The still wins (official).
9. **Morphing on screen for state changes.** Change only while the body is occluded. A visible morph is a failed take (official).
10. **Regenerating whole sequences.** Reroll only the failing shot. Anchor shot first, and split overloaded prompts (official).
11. **Asking an LLM for more than 5 shot prompts at once, or writing prompts that depend on the previous shot** (PJ Accetturo).
12. **Paying for 1080p on close selfie shots.** Benscoter says it doesn't look different. (But see Open Q: wide/logo shots may need more res.)
13. **Speeding up Seedance clips with the audio attached.** It pitches up (retiming write-up).
14. **Using mixed-expression or mixed-lighting identity packs.** The model averages them into a "midpoint face" (WaveSpeed).
15. **Using full AI avatars as the face of a testimonial** (Dara Denney's view; untested for SANTO).

## Open questions
- **Credits discrepancy.** Benscoter's 10 s Seedance run cost ~67 credits at 720p with audio, but our brief says Seedance 2.x is ~18 credits. Is that a different duration, version or tier? It is worth checking on the Generate button before routing decisions.
- **"Anti-Slop mode"** is listed in the official Higgsfield Blender plugin guide for Seedance 2.5 ("use it when hands or physics go soft"). What does it actually do, and is it available in the web/MCP flow at all? Nothing public explains it.
- **Genjutsu Object Swap on garments with logos.** Does it hold the SANTO wordmark and preserve real hands? The vendor itself warns about "small text, hands, occlusions". It needs a 1-clip test.
- **Telegram / messenger recompression.** Does it measurably help on Meta/TikTok, which recompress anyway, or is grain + 30 fps + bitrate enough?
- **The fal Podcast with Tim Simmons** (`deQNOjnDcwY`, 2026-08-07) and **AI For Humans w/ Theoretically Media** (`EA3PGSRotwc`) probably contain the most concrete spoken Seedance 2.5 advice. No transcript was reachable, so a human should watch them (priority 1 in the harvest list).
- **The 13.5 ROAS claim** in the official jersey episode has no published breakdown, so treat it as a claim only.
- **Seedance first-frame over-exposure** (Curious Refuge): is it still present in 2.x on Higgsfield? It needs a check on our own clips.

## Harvest list
The full list is in `harvest-urls.txt` (tab-separated: URL, priority, title). Priority 1 = watch first for technique.

| Pri | Channel / show | Title | Why |
|---|---|---|---|
| 1 | Higgsfield AI (official) | 3-Step Workflow To Make Ultra-Realistic AI Ads — https://www.youtube.com/watch?v=3rDs6FhFoUQ | Grey sheets, face-erase, positive locks |
| 1 | Higgsfield AI (official) | I Used GPT 6 Astra to Automate Meta Ads Campaigns (13.5 ROAS) — https://www.youtube.com/watch?v=BTfEd6vVTKA | **Apparel (jersey)**: hidden-cut outfit changes, print-lock QC, one-hand unboxing, phonetic brand |
| 1 | Higgsfield AI (official) | How To Save AI Credits With Higgsfield + Blender — https://www.youtube.com/watch?v=OiULPvTJ-0E | Blockout-driven v2v, second-by-second prompts |
| 1 | Higgsfield (UGC reel) / Joe Benscoter | Higgsfield AI UGC Tutorial: Make Hyperrealistic Video Ads (Full Workflow) — https://www.youtube.com/watch?v=gUafcCMHClQ | Full staged UGC pipeline, costs, phonetics |
| 1 | fal Podcast | Seedance 2.5 Advice with Tim Simmons — https://www.youtube.com/watch?v=deQNOjnDcwY | Spoken Seedance advice, needs a human to watch |
| 1 | Theoretically Media | Seedance 2.0 Omni Reference Mode — https://www.youtube.com/watch?v=3B5Fw98CoIA | Reference roles |
| 1 | (tutorial) | Complete Seedance 2.0 Video Reference Tutorial — https://www.youtube.com/watch?v=ikPGQGoUjQ0 | Motion refs for hands |
| 1 | (test) | Seedance 2.0 Textured Fabric & Clothing Movement Visual Test — https://www.youtube.com/watch?v=jgO4iZpfSbw | F5 fabric evidence |
| 1 | (tutorial) | Kling Motion Control 3.0 Full Tutorial — https://www.youtube.com/watch?v=Utono2euM24 | Real-performance transfer |
| 1 | Motion / Barry Hott | How to Make AI Native Ads Look Human — https://www.youtube.com/watch?v=6jvIXIjieyA | Strategist view |
| 1 | (tutorial) | How To Create Insanely Realistic UGC Videos for Print on Demand — https://www.youtube.com/watch?v=QqnAIb49sEs | Apparel/POD UGC |
| 1 | (review) | I Tried Higgsfield's New Seedance 2.0 UGC Studio so You Don't Have to — https://www.youtube.com/watch?v=P0DsYvG1WY8 | Honest Marketing Studio review |
| 1 | (tutorial) | How to Prompt for Ultra Realistic AI Videos in Seedance 2.5 — https://www.youtube.com/watch?v=70I52_Ex6H4 | Realism prompting |
| 1 | Rundown guide | Swap the product and keep the performance (Genjutsu) — https://app.therundown.ai/guides/swap-the-product-and-keep-the-performance-with-higgsfield | Object swap steps |

The .txt file has 64 entries in total: 15 are priority 1, 33 priority 2 and 16 priority 3. Every URL was seen in search results or in the extracted playbooks. None were invented.

---

# PART 11 — `09a-transcripts.md`

## 09a: YouTube transcript mining (batch A, 9 videos)

**Date:** 2026-09-24 · **Source:** full transcripts in `research/transcripts/`, read end to end. No web search, no credits spent.
**Citation format:** `VIDEOID @mm:ss` = the start of the 30-second transcript chunk where the statement appears.
**Tags:** NEW = not in `QUALITY-PLAYBOOK.md`. EXTENDS #N = adds specifics to playbook item/rank N. CONTRADICTS = conflicts with the playbook (explained in §3).
**Grades:** B = one practitioner showing the result on screen; C = claim, vendor promo, or my inference. Nothing here reaches A: every video is a single creator, and most are sponsored or affiliate content.

---

## 1. Videos: one-line summary and relevance (0–3)

| Video | Speaker / channel (from content) | Topic | Rel. |
|---|---|---|---|
| `M73BrFnVPA8` | Unnamed Higgsfield power user / affiliate ("using Higgsfield… for years", sells a "bonus package") | Full credit-efficient Higgsfield production: GPT Image 2 split sheet, environment plate, 5 keyframes, three ways to animate them on Seedance 2.5 (compared on screen), Cinema Studio start/end frames, Soul ID training spec, 480p draft → upscale | **3** |
| `Xcg8aklWBGM` | Unnamed OpenArt creator (Skool community, "master template") | AI UGC on OpenArt + Seedance 2.5: GPT Image 2 persona, NB2 sheet with one face, LLM master template, product ad / unboxing / 3-outfit try-on haul, each in one Seedance call | **3** |
| `TKkg-8P7jTM` | Jack (Jack Vs. AI; VFX artist in advertising for 10+ years), on Artlist | Kling 3.0 camera-move prompt templates (handheld, tracking, dolly, tilt, crash zoom, whip, orbit) with start/end frames from Nano Banana Pro | **2** |
| `BJ9H0Dq72lY` | Khalil ("AI for Real Life") | Kling 3.0 vs 3.0 Omni in real projects: Elements library, multi-shot reliability, invented gibberish dialogue, multi-shot used as a shot-discovery tool | **2** |
| `0fh9PqTDmBo` | Unnamed short, Higgsfield affiliate | Using your own face in Seedance 2.0 on Higgsfield (eligibility check); 15 s price dropped 90 → 68 credits | **1** |
| `XjEG0cAIdac` | "Profit Studio" | Higgsfield: Nano Banana avatar + tactical vest composite, pose/environment variants, Veo 3 8 s clips. Mostly a counter-example (golden hour, cinematic prompts), but one audio-leak gotcha | **1** |
| `ApmRSLNMgMk` | Harry Blake (video "made by Higgsfield AI") | Higgsfield Click-to-Ad (product URL → ad), style presets, Lipsync Studio with Kling Avatar 2.0 | **1** |
| `3-S9YjGfYtI` | Unnamed tutorial | Higgsfield UGC Factory click-through (template → avatar+product combine → action → line → voice/emotion/accent → background sound) | **1** |
| `59ILpFm-JnA` | "Create With AI (Zero to AI Hero)" | Maxfusion AI promo: emotion cues within a line, product placement in hands, localisation | **1** |

None of the nine is fully irrelevant. The three rated 1 are mostly UI tours or sponsored promos. Each yields at most one detail.

---

## 2. Findings (BRIEF format)

### 2.1 Put every planned cut's keyframe into the one-call render as a reference, not just the person and room · EXTENDS #1 (and settles contradiction §8.3)
- **How:** Build one still per cut (same model/settings, person sheet + room plate as refs). In the single Seedance 2.5 15 s call: **cut 1's keyframe = start frame**; the **character sheet, environment image, and the other keyframes = references**; the prompt is written as N shots with hard cuts. "That gives every cut a composition to match instead of leaving the model to work out what the next shot should look like halfway through." `M73BrFnVPA8 @07:56`
- **The on-screen A/B/C:** (a) each keyframe animated alone = face holds but no flow between clips `@07:25`; (b) the one-call version above = "one continuous 15-second scene with four hard cuts… same gym and I look the same in every cut" `@08:28`; (c) sheet + location only, shots described in text = identity holds but **"framing drifts long before your character does"**. "The model knows who I am and where I am. It just has to guess what an extreme wide and an extreme close-up actually mean inside that room." `@09:05`
- **Keyframe detail:** freeze the peak instant ("caught at the exact moment of impact… gives the video model an exact composition to match") `@05:11`. This also supports playbook #24 (mid-event first frame).
- **Fixes:** F1 F7 F9 (framing/shot-design drift, which the playbook doesn't name separately).
- **Evidence:** `M73BrFnVPA8` @07:25–09:05, grade **B** (results shown side by side; affiliate creator).
- **Cutroom input change:** in the board step, keep each panel as a **separate keyframe image** alongside the grid. Pass keyframe 1 as `start_image`, keyframes 2..N as references with a role line each ("@Image k = composition of cut k only"). Count the refs against the ≤8 comfort limit (sheet + room + product + ≤5 keyframes).
- **Cheapest test:** the playbook's T5 with one arm added: grid board vs separate keyframes-as-refs, same prompt. 2 × ~67 credits (15 s 720p).

### 2.2 Anti-easing clause whenever an end frame is locked · NEW
- **How:** "Locking a start and an end frame makes the model want to ease into the first one and settle onto the last one. So, if you don't say it, you get a car that pulls up and poses at the finish line." His fix is repeated through the prompt: **"already at full speed in the first shot… no deceleration at any point… still going forward as the last one ends."** `M73BrFnVPA8 @12:44`. Also: vary the distance between the two frames ("going wide on this one after going tight on the first so the sequence has somewhere to travel instead of ending up where it started") `@12:12`.
- **Why it matters for UGC:** this is the mechanism behind "floaty", posed endings (the person freezes into the end-frame pose, the hand settles on the product). It is the first+last-frame gotcha the brief says we lack.
- **Fixes:** F6 (posed, slow-motion endings), F4 (a state change that crawls into the end frame).
- **Evidence:** `M73BrFnVPA8` @12:12–13:15, grade **B**.
- **Cutroom input change:** if `end_frame` is set, the prompt builder auto-adds: "Motion is already under way in the first frame; no easing in; no slowing down or settling; still mid-movement in the final frame." The linter warns when start and end frames share the same `distance_band`.
- **Cheapest test:** one 5 s Seedance or Kling start+end clip (walk toward the camera), with and without the clause, at 480p. ~2 × 7–15 credits.

### 2.3 Build the end frame FROM the approved start frame, with the "match exactly" line first · EXTENDS brief "first+last frame"
- **How:** Generate the end-frame still with the **approved start frame as a reference** plus the character sheet. The **first sentence** of the prompt says the recurring objects "have to match that start frame exactly", "so I get the same helmet coming back instead of a second version of it". Rule: "anything you don't want the model changing has to be locked in both of them." `M73BrFnVPA8 @11:42–12:12`. When there is no end frame, the prompt must describe what gets revealed. For anything intricate, make a finishing frame instead. `TKkg-8P7jTM @17:42–18:12`
- **Fixes:** F2 F7 F1.
- **Evidence:** `M73BrFnVPA8` (B); `TKkg-8P7jTM` Jack (B).
- **Cutroom input change:** the end-frame job type must receive the start frame as reference #1 and use a template whose first line is "The [SKU canonical name], [persona], and room must match Image 1 exactly."
- **Cheapest test:** 2 Nano Banana end-frame edits, with and without the lead line, then compare the logo/print. ~3 credits.

### 2.4 "Relight me" clause in every composite / keyframe prompt · NEW to the playbook (05 #19 has a tool route via IC-Light)
- **How:** The character sheet was shot in flat white studio light. "If I don't say it, I'll get dropped into that dark gym still carrying studio lighting on my face and it will look edited instead of me being fully integrated in the scene. So every prompt says to relight me with that amber key from above and the [cyan, transcribed "scan"] rim behind." Called "the one instruction… that matters more than anything else". `M73BrFnVPA8 @03:37–04:08`
- **Fixes:** F6 (the pasted-in look; the "subject lit differently from the room" tell listed in 05's auto-QA), F7.
- **Evidence:** `M73BrFnVPA8`, grade **B**.
- **Cutroom input change:** the room kit's GEO block already stores "one light source, which side the window is on". Generate a relight sentence from it automatically: "Relight [persona] and the [SKU] to the room: soft daylight from the window on the left, falling off to the right; no studio fill on the face." It goes in every composite still and keyframe prompt. It matters most because our identity plate is plain grey/flat light by design.
- **Cheapest test:** 2 Nano Banana composites (persona into a real room photo), with and without the clause. ~3 credits.

### 2.5 Never name the camera device (or a fixed pose) in the visual prompt · NEW (extends the F6 "unposed body language" rule)
- **How:** "Anything you name as an object is something the model will try to render. So, writing FPV drone puts an actual drone in the frame. That's why I'll describe the movement instead." And: "a fixed pose gives you a mannequin every time. So, I'll describe what his body is doing while he stands there instead." `M73BrFnVPA8 @09:36–10:08`
- **Why it matters for UGC (inference, C):** this is a likely source of our F3 "phone in hand while both hands are busy" and phones in mirrors. Prompts such as "filmed on an iPhone", "selfie stick", "tripod" or "ring light" name objects. Describe the **vantage and behaviour** instead: "seen from arm's length slightly above eye level, the frame drifting with her breathing". Keep "iPhone" only in the audio/finish lines, if at all. (Jack's templates also describe moves without naming gear, e.g. "tripod-like stability" is used as an adjective, not a noun. `TKkg-8P7jTM` prompt list.)
- **Fixes:** F3 F6 F7.
- **Evidence:** `M73BrFnVPA8` (B for the drone case). The UGC transfer is C.
- **Cutroom input change:** add to the banned-word linter any device nouns in the visual part of the prompt: phone, iPhone, smartphone, camera, tripod, selfie stick, gimbal, drone, ring light, microphone. Map `camera_holder` to vantage phrases. Replace pose words ("poses", "standing straight") with an ongoing activity ("shifting weight, adjusting her sleeve").
- **Cheapest test:** 2 Nano Banana stills of a selfie-POV frame: "shot on iPhone selfie" vs a vantage description. Count visible phones. ~3 credits.

### 2.6 Draft motion at 480p, check the price live, pay full only for keepers · EXTENDS #29 and §7 (numbers)
- **How:** Higgsfield shows the credit cost before submitting, and it updates live. "The same model on the same 5-second shot comes back at **15 credits with one set of settings and 110 with another**… from the resolution and the audio alone." `M73BrFnVPA8 @16:21`. For a risky shot: **Seedance 2.5, 8 s, 480p = 20 credits** vs the same at 4K on Seedance 2.0 = 176. "I'm not judging quality yet. I'm checking whether the timing and the movement are right." `@16:51`. Separately, a 15 s Seedance 2.0 clip on Higgsfield is now **68 credits** (was 90) `0fh9PqTDmBo @01:34`. That confirms the playbook's ~67 figure, not the ~18 in the brief.
- **Fixes:** F9.
- **Evidence:** `M73BrFnVPA8` (B, prices shown in UI), `0fh9PqTDmBo` (C). Also consistent with `02` ("Draft at 480p, finish at 720p").
- **Cutroom input change:** add a `draft` render tier (480p, audio off where lip-sync isn't being judged). A shot can only be promoted to the 720p final after a human ticks "timing and motion OK" on the draft. Record both costs in the ledger.
- **Cheapest test:** `get_cost` for Seedance 2.5 at 480p/720p × audio on/off × 5/8/15 s. 0 credits.
- **Caveat:** his next step (upscale the 480p draft to 2K with ByteDance video upscale, "AIGC" preset, which "only lifts the resolution" `@17:22`) conflicts with the playbook. See §3.2.

### 2.7 Persona sheet: a split-frame two-panel sheet whose prompt is mostly skin, then remove the second face · EXTENDS #11 / #5
- **M73B recipe:** GPT Image 2, 2K, 16:9, **one real photo** as reference. One image split down the middle: **full body standing straight on the left, tight chest-up close-up on the right**. Background "pure white and completely empty on purpose so that the video model doesn't get confused". "The longest part of the whole prompt is about the details on skin… visible pores, fine lines, and uneven skin tone, and no smoothing or beauty filter anywhere." Then "I never describe my face in a prompt again. I just attach this image." `M73BrFnVPA8 @01:03–02:34`
- **Xcg8 recipe (3 panels + the exact way to make it headless):** NB2 with the persona still as reference: *"a character reference sheet of my character presented in three separate poses. A chest up close-up shot facing forward, a full-body shot facing forward, and a full-body back view shot. All behind a pure gray background to avoid harsh lighting."* 16:9, 4K `Xcg8aklWBGM @02:03`. Then **edit → select the face in the full-body panel → prompt "remove selection"**. Reason given: "faces in full-body shots are usually low detail and a little blurry. By removing them, you're telling the AI to only pull facial features from the crisp close-up." `@02:37–03:08`. This is the missing *how* for the playbook's "headless" sheet.
- **Fixes:** F1 F6.
- **Evidence:** both B (sheet and results shown).
- **Cutroom input change:** the persona intake produces the sheet via a masked "remove selection" edit (a local mask edit, which respects the "never run the whole image twice" rule). Store the sheet at 16:9 even for 9:16 ads. The sheet prompt gets a fixed skin-texture paragraph.
- **Cheapest test:** 1 sheet + 1 masked edit. ~3 credits.

### 2.8 Soul ID training set: 6 flat, boring angles, and it only works in Soul models · NEW specifics (answers `01` open question 5 in part)
- **How:** From the sheet, GPT Image 2 generates **6 images, changing nothing but the angle: front, ¾ left, ¾ right, profile left, profile right, one skin-texture close-up**. The prompt is "deliberately boring": **one big frontal softbox, no hard shadows, no rim light, no colour cast, plain mid-grey background, 85 mm head-and-shoulders centred**. "A soul learns everything in the images you give it. Lighting included. If you train it on dramatic rim lit shots… it puts that same lighting back into every shot." `M73BrFnVPA8 @14:17–14:48`. He trained with 6 images and it worked.
- **Gotcha:** "a trained soul only works with Soul 2.0 and Soul Cinema. So it won't work with GPT image 2, Cinema Studio, Seedream, or Seedance. So the character sheet is still what you'd attach for everything else." `@15:18`
- **Fixes:** F1 F6.
- **Evidence:** `M73BrFnVPA8`, grade **B**.
- **Cutroom input change:** if we keep Soul ID for stills, the training pack is a fixed 6-slot spec with flat light. Route rule: Soul ID → Soul 2.0/Cinema stills only. Every video call gets the sheet.
- **Cheapest test:** the training cost is unknown; check `get_cost`. It's only worth doing if Soul 2.0 stills are a production step.
- **Tension:** generating the 6 angles means extra model passes on the face (see §3.5).

### 2.9 Add a +2 s duration buffer beyond the scripted length · NEW
- **How:** "For the duration, add two extra seconds beyond whatever your prompt's duration was set to. My prompt was 20 seconds, so I'll set it to 22… gives the generation breathing room to get through any dialogue without cutting off mid-sentence or glitching. This single trick has saved me countless regenerations." `Xcg8aklWBGM @06:13–06:45`. He used it on all three ads (20→22, 25→27, 20→22).
- **For a 15 s ceiling:** plan the script and shot timings for **13 s** inside a 15 s render. This also fits the playbook's "trim 10–15 frames from each end".
- **Fixes:** F8 F9.
- **Evidence:** `Xcg8aklWBGM`, grade **B** (on OpenArt's Seedance 2.5, which evidently accepts more than 15 s).
- **Cutroom input change:** the script linter's word budget counts against `render_seconds − 2`. The shot plan's summed seconds must be ≤ render − 2.
- **Cheapest test:** free. Re-check our past cut-off dialogue rejections against the scripted vs rendered length.

### 2.10 Reference order = tag order; check every @image mapping before paying · EXTENDS #9
- **How:** The LLM prompt names image 1 = character sheet, image 2 = product, so the uploads must go in that order ("drag the character sheet in first and then the product image second"). "Review your prompt to make sure each image tag is correctly formatted… if not, manually go through and tag the correct image to the correct reference." `Xcg8aklWBGM @05:43–06:13`
- **Fixes:** F1 F2 F9.
- **Evidence:** B.
- **Cutroom input change:** the builder emits refs and `@Image N` tags from one array. The linter fails if any tag has no upload, or any upload has no role line.
- **Cheapest test:** free.

### 2.11 Generate the product's "other state" by editing the master product image · EXTENDS #5 (one reference per state) and #7
- **How:** For an unboxing plus build, two product refs: assembled, then an NB2 edit *"using that image one, disassemble it and lay out each individual part separately, set against a clean pure gray background."* "If you only give the AI the finished product, it has no idea what the individual parts look like… By feeding it both states, the whole build sequence stays believable." `Xcg8aklWBGM @08:17–08:48`
- **For SANTO:** use real phone photos per state first. This edit route is the **fallback** for states we haven't shot yet (hoodie folded in the mailer, mailer torn open), generated from the real master photo, and then checked by a human for logo and print survival.
- **Fixes:** F4 F2.
- **Evidence:** B (the result shows parts that stay consistent through the build).
- **Cutroom input change:** each SKU has `states[]`. A missing state can be filled with a "derive state from master" NB edit job, flagged `synthetic_state` for review.
- **Cheapest test:** 1 NB edit: the real folded-hoodie photo → "the same hoodie inside a torn-open grey poly mailer". ~1.5 credits.

### 2.12 Fashion try-on haul in one call, with no dialogue · EXTENDS #32 and #8
- **How:** 3 outfit refs + the one-face sheet. Shot list: "show off each set of clothing through three poses then swap to the next… zero dialogue, just visuals", 20 s (+2). "Every clothing set came through clean, the character stayed consistent." "For fashion content, the visuals do all the selling." `Xcg8aklWBGM @11:28–12:36`. The outfit swap happens on the hard cut, not on camera (consistent with #7 of the playbook).
- **Fixes:** F8 (by removing the lip-sync risk), F1, F9.
- **Evidence:** B (shown, but on a generic model; fit realism was not tested).
- **Cutroom input change:** add a `try_on_haul` format: N outfits × 3 DO beats, `speech_mode = none`, room tone + fabric foley only, text overlays in post.
- **Cheapest test:** 1 Seedance 15 s call with 2 SANTO outfits (hoodie set, leggings set). ~67 credits.

### 2.13 Audio-on models invent speech: Kling "gibberish" dialogue, and prompt text spoken aloud · EXTENDS #4 (negatives) and #6
- **How:** Kling 3.0 multi-shot: "if you don't explicitly bake dialogue into your prompt and even sometimes when you give it a negative prompt saying no dialogue, it'll often generate this gibberish sort of dialogue." `BJ9H0Dq72lY @11:04–11:35`. Jack puts **"music" and "dialogue"** in Kling's negative field for every shot. `TKkg-8P7jTM @09:52`. In `XjEG0cAIdac` @08:50 the final Veo 3 clip contains an unscripted line that sounds like direction text: "Hold the tension in the rope. We're initiating the slow zoom out now. Maintain that focus." (C: it could be a music-bed sample, but it reads like prompt text spoken aloud.)
- **Fixes:** F8 F9.
- **Evidence:** B (Khalil, Jack); C (XjEG).
- **Cutroom input change:** for any beat with `speech_mode = none` on Kling, **turn native audio off** (also cheaper) and add foley in post. Don't rely on the negative field. Where audio is on, put spoken lines only inside quotes after "says:", and add "No other speech; no narration." Camera direction goes in plain descriptive form, never imperative second person.
- **Cheapest test:** 2 Kling 5 s silent-beat clips (negative "dialogue" vs audio off). Listen for invented speech. ~2 × Kling std.

### 2.14 Kling multi-shot is for finding shots, single shots are for keepers; harvest the still · NEW (partly contradicts #1 for Kling, see §3.1)
- **How:** "You might get one great shot out of five. You might get four great shots out of five… I use the multi-shot for exploration, but I use the single shots for quality." Single and two-shot sequences are where Kling shines `BJ9H0Dq72lY @11:04–12:41`. His workflow for an angle the image model couldn't produce (a reverse angle): a Kling Omni 2-shot multi-shot (over-the-shoulder, then a reverse close-up) with Elements locked. Then "take the still frame from that result, feed it back into my image tool, clean it up, lock the details, and use it as a new start frame" for a single-shot render `@12:41–14:18`.
- **Fixes:** F7 (new angle of the same room/person), F9.
- **Evidence:** B.
- **Cutroom input change:** add a "discover angle" job: a cheap multi-shot → frame picker → NB clean-up → it becomes a keyframe. This also turns failed takes into keyframes (extends "mine failed takes").
- **Cheapest test:** 1 Kling 2-shot at the lowest tier for a reverse angle of our room. ~Kling std 10 s.

### 2.15 Kling 3.0 Omni Elements as the asset library, including a "costume" element · EXTENDS `02` T14 (not in the playbook)
- **How:** Create an element from an image (or video). Choose the tag type **character, item, costume, scene or effect**. Add your own description or let it auto-describe. "Add multiple angles or multiple shots to give it coverage". Then tag it in the prompt instead of describing it ("instead of saying living room, you tag the living room") `BJ9H0Dq72lY @08:55–10:00`. Advice: "pick one platform and make it your Omni headquarters", because elements don't transfer and rebuilding costs time `@08:22`.
- **SANTO angle (C):** a **costume** element per SKU (garment on-body angles), separate from the **character** element, maps directly onto the playbook's "no product in the person image" rule.
- **Fixes:** F1 F2 F7.
- **Evidence:** B (Khalil, Kling native platform). `02` notes practitioners report image-quality loss with Elements on, so use it only for cross-shot identity.
- **Cutroom input change:** Cutroom stays the source of truth for assets and pushes them to the platform's element store (Higgsfield Elements or Kling Elements) with a stable id per SKU/persona/room. It never rebuilds them by hand.
- **Cheapest test:** create elements (Higgsfield Elements are described as instant/free in `01`); 1 Kling Omni 5 s clip with costume + character + scene tags.

### 2.16 Camera-move grammar: move + constant speed + named exclusions of the other axes · EXTENDS #4 (Motion row) and #46
- **How (Jack's Kling 3.0 templates, verbatim):**
  - Handheld: *"Frantic handheld camera movement with natural micro-shake and imperfect stabilisation. Responsive, slightly uneven translation. No intentional zoom."* `TKkg-8P7jTM @14:01`
  - Tracking: *"have the camera translate forward at a steady running pace, matching the moving subject's speed. Stabilised tracking. No zoom."* `@15:36`
  - Dolly: *"Camera dollies forward in a straight line toward the frame centre. Smooth stabilised motion. No zoom."* `@11:27`
  - Tilt: *"Smooth vertical tilt upward at constant speed. Tripod-like stability. No pan, no roll, no dolly."* `@08:49`
  - Pattern: one move + speed profile + an explicit list of the axes that must **not** move, then a one-line action. For long moves, have an LLM number the beats and "spread them out evenly across say 15 seconds" `@05:12`.
- **UGC use:** for a friend-held phone, drop "frantic" and keep "natural micro-shake, imperfect stabilisation, slightly uneven translation, no intentional zoom". Handheld reads as "documentary… grounds the material"; tracking reads as detached, "witnessing" `@14:35–16:08`. So UGC wants handheld, not tracking.
- **Fixes:** F6.
- **Evidence:** B (Jack, a VFX professional, results shown).
- **Cutroom input change:** the `camera_move` field emits from templates with an `exclude_axes[]` list. Never write "zoom" unless zoom is the move.
- **Cheapest test:** 1 Kling 5 s handheld talk-to-camera, UGC variant of the template. ~Kling std 5 s.

### 2.17 Short durations for single moves; generate slow, speed up in the edit · EXTENDS #14 / #7
- **How:** Tilt "around 4 to 5 seconds… Sometimes generations for certain camera moves, you'll get a better result with a shorter length" `TKkg-8P7jTM @09:20–09:52`. Crash zoom in a **3 s** generation. "It's better for it to be slower as your AI generation and then… speed it up in the edit" `@19:15`.
- **Fixes:** F6 F9.
- **Evidence:** B. This confirms the playbook's retime rule from a second, independent pro.
- **Cutroom input change:** default `seconds` per camera move (tilt 4–5, push-in 4–5, whip/crash 3). The retime factor is stored per shot.
- **Cheapest test:** free (retime existing clips).

### 2.18 The video prompt covers motion and camera only; stills settle everything else · EXTENDS STOP #11 (confirmation)
- "Because the reference images already fix my wardrobe, the environment, the color, and the lighting. The video prompt only has to cover motion and camera. So, describing anything a second time just gives the model a chance to change something that was already settled." `M73BrFnVPA8 @06:14–06:45`. Grade B. There's nothing new to change; it's a second source for the playbook rule. Note: it has to coexist with the "sparse prompt → frame-for-frame copy" warning. Describe motion richly, and describe appearance not at all.

### 2.19 Look control by banning qualities one by one · EXTENDS #13 (with a caveat)
- "What's actually controlling the look here is a list of things I'm switching off by name. So, no HDR, no oversaturation, no digital sharpening, and no plastic skin… banning them one by one works better than asking for a look." `M73BrFnVPA8 @11:10–11:42` (GPT Image 2 stills, cinematic job).
- **UGC version:** ban *qualities*, never *objects*: "no HDR, no oversaturation, no beauty smoothing, no plastic skin, no studio lighting". This agrees with the playbook's Seedance rule (negate defects, not visible objects). Drop his "natural film grain and gentle vignette" and "no digital sharpening" for UGC (see §3.4).
- **Fixes:** F6. **Evidence:** B/C. **Test:** 2 NB stills. ~3 credits.

### 2.20 Macro "detail" beats make a sequence read as filmed · EXTENDS #21
- "A detail shot like this is one of the easiest ways to make a sequence feel filmed. Real footage is full of shots like this and generated footage almost never is." `M73BrFnVPA8 @04:40`. A wide shot with the subject small "tells the viewer the location is a real space rather than a background you've stuck yourself in front of" `@04:08`.
- **For SANTO:** one hands-free fabric macro (fleece pile, denim twill, rib cuff) per ad, plus one wider room-establishing beat. Both are already allowed by the playbook's hand-free macro rule; this adds a reason to require them in the board. **Fixes:** F6 F7. Grade C (claim).

### 2.21 Eligibility check on every start frame before rendering · NEW (small gotcha)
- Seedance on Higgsfield requires an eligibility check on uploaded start images with faces. Celebrity likenesses are rejected; generated faces and real family photos pass `0fh9PqTDmBo @00:00–01:00`. M73B runs all five keyframes through the check (upload media → image generation) before animating `M73BrFnVPA8 @05:43–06:14`.
- **Fixes:** F9 (a failed or blocked submit mid-batch). **Evidence:** C/B.
- **Cutroom input change:** run the eligibility check as a preflight step on every keyframe when the board is approved, not at render time. It also acts as a free likeness screen alongside the playbook's likeness check.

### 2.22 Emotion shift inside one line · NEW (C)
- Script lines carry split emotion cues: "I mark the first part of the line as skeptical and the second part as genuinely impressed, so the performance naturally shifts from doubt to excitement." `59ILpFm-JnA @02:03`. This is a vendor promo (Maxfusion "Riz" model). It's worth trying as bracketed cues in Seedance dialogue: `says, doubtful at first: "I thought this would be thin —" then, surprised: "it's actually heavy."`
- **Fixes:** F8. **Test:** 1 Seedance 5 s talking beat at 480p, with and without cues. ~7 credits.

### 2.23 Higgsfield's built-in UGC pipelines as a free field map and a baseline · EXTENDS #1 (C)
- UGC Factory exposes these inputs: template (general, selfie, selling something, **ASMR**, podcast) → avatar + optional product "combine image" (returns several variants in ~1 min) → action text → spoken line → **voice type, emotion, language, accent** → **background sound** (city noise, crowd, rain) → model → 720p/1080p `3-S9YjGfYtI @00:00–03:05`. Click-to-Ad takes a Shopify/Amazon URL and auto-extracts images, brand colours and logos. Then comes style (UGC, clean minimal, unboxing, review, cozy mornings, product stories, luxury). "Always make sure the correct product clips are selected… If needed, you can also upload your own clips manually" `ApmRSLNMgMk @01:34–04:44`. Lipsync Studio: Kling Avatar 2.0, "pro" quality `@05:47`.
- **Use:** these give a checklist of fields Cutroom's shot spec should also cover (voice emotion, accent, a background-sound bed). The ASMR template is a candidate for a fabric/unboxing sound-first format. Run one Click-to-Ad on a SANTO URL as the "vendor default" baseline for the blind real-or-AI test. **Fixes:** F9. **Evidence:** C (sponsored).

### 2.24 Composite-still edit wording for a worn product (C)
- *"Place the tactical fitness vest naturally on the avatar's torso. Make sure the straps and shadows align realistically. Keep the character's face and body shape unchanged."* `XjEG0cAIdac @03:37`. For SANTO: "Dress her in the hoodie from Image 2… hem, cuffs and drawcord-free hood exactly as in Image 2; fabric folds and shadows follow her posture; keep her face and body shape unchanged." EXTENDS #3. Grade C (one example, and the channel's video prompts otherwise use banned "golden hour / cinematic" wording).

---

## 2b. STOP DOING (from these transcripts)
1. **Describing shots only in text inside a one-call render.** Identity survives, framing doesn't (`M73BrFnVPA8 @09:05`).
2. **Locking an end frame without an anti-easing clause.** The subject "pulls up and poses" (`M73BrFnVPA8 @12:44`).
3. **Naming camera gear or fixed poses in visual prompts** ("FPV drone" → a drone in frame; fixed pose → a mannequin) (`M73BrFnVPA8 @09:36`).
4. **Pasting a flat-lit sheet into a scene without a relight line** (`M73BrFnVPA8 @03:37`).
5. **Training Soul ID on dramatic or rim-lit images.** The lighting is learned (`M73BrFnVPA8 @14:48`).
6. **Scripting dialogue to the exact render length** (`Xcg8aklWBGM @06:13`).
7. **Trusting Kling's "no dialogue" negative.** Turn audio off instead (`BJ9H0Dq72lY @11:04`).
8. **Relying on Kling multi-shot for final coverage** (`BJ9H0Dq72lY @12:07`).
9. **Following "golden hour / warm cinematic lighting / cinematic soft shadows" Veo recipes for UGC** (`XjEG0cAIdac @04:41, @07:16`). They produce the ad look the playbook bans.

## 2c. Open questions
1. Does a 480p Seedance 2.5 draft (same seed, same refs) predict the 720p final's motion closely enough to promote it? M73B upscaled the draft itself, so he never tested this.
2. Does ByteDance video upscale ("AIGC" preset) add the AI-clean look to phone-style footage, or is it a neutral resolution lift? It could replace a 720p re-render. See §3.2.
3. Does Higgsfield's Seedance 2.5 accept >15 s like OpenArt's did (22–27 s in `Xcg8`)? If so, the +2 s buffer costs almost nothing.
4. Does "shot on iPhone" in a visual prompt actually render phones on Seedance/NB? Test 2.5 settles it.
5. Does a Soul ID trained on 6 *generated* angles drift from the real face over time? (The playbook says faces go plastic after about 2 passes.)
6. Do Higgsfield Elements expose a "costume" type like Kling Omni does, and does a garment element beat a plain garment reference for logo survival?

---

## 3. Contradictions with the playbook

1. **One call with many cuts (playbook #1) vs "multi-shot is for exploration"** (`BJ9H0Dq72lY @11:04–12:41`, Kling 3.0 multi-shot: "one great shot out of five… four great shots out of five"). **Reconciliation:** the model matters, and so do the inputs. Khalil's multi-shot ran on Kling with elements but *without per-cut keyframes*. `M73BrFnVPA8` and `Xcg8aklWBGM` both show Seedance 2.5 one-call results holding identity across 4–8 cuts, and M73B shows that per-cut keyframes are what keep the framing (finding 2.1). Keep #1 for Seedance with keyframes. Don't route multi-cut ads to Kling multi-shot.
2. **Generative upscaling.** The playbook says no generative upscaling for UGC (it adds AI-clean detail) and to stay at 720p. `M73BrFnVPA8 @17:22` drafts at 480p, then uses ByteDance video upscale (AIGC preset) to 2K, and claims "that only lifts the resolution. Everything else about the shot stays exactly as it was." That was for cinematic work, and no UGC evidence was shown. Test it on one 480p UGC draft against a native 720p render in the blind test before accepting it. If it passes, it's cheaper than re-rendering at 720p.
3. **Talking length per generation.** The playbook says talking segments ≤8 s per generation (Kling loses sync after second 8). `Xcg8aklWBGM` gets clean dialogue across a 22 s single Seedance 2.5 call with 5 cuts (`@06:45–07:16`). The ≤8 s rule is Kling-specific. On Seedance with internal cuts, the per-cut lines are short anyway. Keep ≤8 s for Kling only.
4. **Film grain / sharpening.** `M73BrFnVPA8 @11:10` adds "natural film grain and a gentle vignette" and bans "digital sharpening". The playbook's phone finish wants *slight over-sharpening* and *no film grain*. His context is a cinematic 21:9 racing piece, not UGC. The playbook stands for UGC. Take only his method (ban qualities by name).
5. **Re-running the face through models.** The playbook says never run an image through a model twice in full, and the identity plate is never re-run. Both creators build sheets (M73B also builds 6 Soul ID angles) by regenerating from the real photo through GPT Image 2/NB2. Their results looked consistent on screen, but it can't be judged on YouTube compression. Keep the playbook rule for the plate. Treat generated angle sets as derived assets and compare each one to the plate with a face-similarity score.
6. **Sheet background.** M73B uses pure **white**, empty. Xcg8 uses pure **grey** "to avoid harsh lighting". The playbook says plain grey. Minor; grey plus a relight clause (2.4) covers both.
7. **Still resolution.** `XjEG0cAIdac @02:35` says 1K stills are "more than enough" because social platforms compress. The others use 2K–4K for sheets and keyframes. For *reference* stills that must carry print and stitching detail (F2), use 2K+. Low resolution is fine only for throwaway exploration.
8. **Product states generated vs photographed.** `Xcg8` generates the second product state by editing the master image. The playbook's product kit wants real per-state photos. Real photos come first, and generated states are a flagged fallback (2.11).

---

## 4. Top 5 most valuable findings

1. **Per-cut keyframes as references in the one Seedance call** (keyframe 1 = start frame; sheet + room + other keyframes = refs). Without them "framing drifts long before your character does." `M73BrFnVPA8 @07:56–09:05` (B) → F1 F7 F9.
2. **Anti-easing clause whenever an end frame is locked:** "already at full speed in the first shot… no deceleration… still going as the last one ends". Otherwise the subject "pulls up and poses". `M73BrFnVPA8 @12:44` (B) → F6 F4.
3. **Relight clause in every composite/keyframe**, generated from the room's light source, because the flat-lit sheet otherwise "looks edited". `M73BrFnVPA8 @03:37` (B) → F6 F7.
4. **Never name camera gear or a fixed pose in visual prompts** ("FPV drone puts an actual drone in the frame"; a pose gives "a mannequin"). Ban phone/tripod/selfie-stick nouns and describe vantage and ongoing activity instead. `M73BrFnVPA8 @09:36` (B; UGC transfer C) → F3 F6.
5. **Cheap-draft economics plus a timing buffer:** the same 5 s shot costs 15 vs 110 credits from resolution and audio alone; Seedance 2.5 8 s at 480p = 20 credits to check motion before any final (`M73BrFnVPA8 @16:21–16:51`). Render 2 s longer than the script (`Xcg8aklWBGM @06:13`) → F9 F8.

---

# PART 12 — `09b-transcripts.md`

## 09b: Techniques mined from YouTube transcripts (batch b, 9 videos)

**Date:** 2026-09-24. **Source:** full transcripts in `research/transcripts/`. No web access was used and no credits were spent.
**Baseline:** `QUALITY-PLAYBOOK.md`. Anything the playbook already covers is left out unless the video adds numbers, exact wording, settings or gotchas.
**Tags:**
- **NEW:** not in the playbook.
- **EXT #N:** adds specifics to playbook item #N. The number is the rank in §1–2 of the playbook.
- **CONTRA:** conflicts with the playbook.

Citations use the form `VIDEOID @mm:ss`.

---

## 1. Per-video summary

Relevance: 0 = irrelevant, 3 = directly usable.

| Video | Speaker / channel (from content) | Topic | Rel. |
|---|---|---|---|
| `eflfUwTdSEc` | Unnamed creator on a Higgsfield-affiliate tutorial channel | Seedance 2.5: five 30 s one-prompt short films. Covers headless character sheets, "freeze rules", ordered reveals, a multi-camera auto-cut phrase, **named-state continuity**, and **before/after room plates made from one master** | **3** |
| `b_RghITuQQM` | Unnamed AI-filmmaking creator using OpenArt, with a free Skool community (probably the same creator as `Zo8KaTs0l6k`) | Complete Kling 3.0 guide: multi-shot, Omni references, **the lip-sync wall at about 10 s**, reference-count glitches, what the tool cannot do | 2 |
| `Zo8KaTs0l6k` | Probably the same creator as above; sponsored by Higgsfield | "AI realism" with Soul, Seedream 5.0 Pro sheets and Seedance 2.5: identity wording, accent formula, 3-stage scene prompts, counted foley, light post work. The look is cinematic, not UGC | 2 |
| `aw6N7M4fPuo` | Unnamed short-form creator, Freepik/Higgsfield | Kling 2.5 Turbo start/end frames: **the physically-achievable-path rule**, colourway-swap transitions, 5 s vs 10 s | 2 |
| `Z3vY2U8ysL0` | Unnamed creator (4th video in a beginner AI-film series), Freepik affiliate. Made a Toyota of Oxnard dealer ad | Kling 3.0 multi-shot "action mapping": one action covered from 4–5 angles in one generation; splicing identical re-runs | 2 |
| `boxfGGa4sXk` | ECom Outlooks (AI-ad agency) | A real client UGC ad for bar stools. Claude does angle research, then a script split into 8 s scenes with **"character lock" and "setting lock"** blocks pasted into each scene | 2 |
| `fmgVm-fxPDM` | **Higgsfield AI official** (presenter Adele), 271k views, 2026-05-18 | Marketing Studio beauty brand: UGC preset with hooks and settings, a product-preservation sentence, brand-kit reference, Hyper Motion and TV Spot | 2 |
| `ez8gfygg8ho` | Unnamed female creator (persona "Iza"), Higgsfield affiliate | Seedance 2.0 in four 15 s segments. Higgsfield Character from your own photos, and the **"check eligibility" gate** on references. Hair drifts between segments | 1–2 |
| `aZV03WzrUPI` | Unnamed creator, Higgsfield Marketing Studio (the concept is credited to Girl in Blue Studios) | Fictional ice brand: logo, products and Marketing Studio UGC. Useful mainly as a **counter-example**: its scripts use "game changer" and "obsessed" | 1 |

---

## 2. Findings

### F-1. Named-state continuity: write a state change as fixed states, not as an action · NEW
- **What / how:** for a state change inside a *continuous* take, the creator doesn't describe the action harder. He lists the exact states the object passes through, and closes the set of things that carry the state:
  - The states: *"The hand fully wrapped in the towel with no skin showing, dry the instant the towel comes away, and dry from then on."*
  - The closed set: *"the only wet things in the whole scene are his hands before that, his sleeve cuffs, and the rain on the window, so nothing else accidentally looks wet."*

  The pattern has three parts:
  1. **An occluded transition state.** The change happens while something covers the object.
  2. **An instant-after state.**
  3. **A persistence clause** ("from then on").

  Add the closed list of affected objects.
- **SANTO example (mailer):**
  - "The mailer's top edge is fully covered by her right hand, with no bag edge showing."
  - "Torn open along the top the instant her hand comes away, and torn from then on."
  - "The only torn thing in the scene is the top edge of the grey SANTO mailer."

  Hoodie: "hoodie fully over her head, with no face showing / face out the instant the hood clears her chin / wearing it from then on."
- **Fixes:** F4 (and F2/F7 through the closed set).
- **Evidence:** `eflfUwTdSEc @12:02–12:32`, Seedance 2.5 creator. The shown 30 s one-take held continuity; the only defect he flagged was a dog's boot jerk. **B**
- **Cutroom input change:** the shot spec gets `state_sequence = [occluded_state, instant_after, persists]` and `state_scope = [only objects that change]`. Both are rendered verbatim into the prompt. This fits alongside the existing `start_state` / `end_state`, and the linter requires the occluder to be named.
- **Cheapest test:** one 5–6 s Seedance clip of a mailer opening written in this pattern, vs the playbook's hidden-cut version. That's 1–2 videos; run `get_cost` first (18–67 cr each).

### F-2. Make the "after" plate by editing the "before" master, then give the video model both · EXT #7 / #23
- **What / how:**
  1. Build the **clean master** first: one wide shot of the whole room, which "locks the entire layout".
  2. Make the other state by **attaching that master and editing it** ("the same room just completely trashed"), not by describing it from scratch. *"If I described both of them separately, they just come out as two different rooms and would never cut together."*
  3. Attach **both plates plus the character sheets** (4 references) to Seedance 2.5 and write the scene so it "starts in the messy state and ends cleaned up".

  The result "ends up exactly matching that clean plate… nothing just disappears between the cuts".
- **SANTO use:**
  - The sealed mailer photo is real. If no real torn-mailer photo was captured, make one with a single Nano Banana edit *of that same photo*.
  - Same for "hoodie folded on the bed", then "bed without hoodie" for the room after pull-on.
  - Supply both as state references.
- **Fixes:** F4 F7 F2.
- **Evidence:** `eflfUwTdSEc @13:04–13:34` (method), `@14:40` (result), same creator. **B**
- **Cutroom input change:** the state kit stores `derived_from` for each generated state image. Generation of the state-B image is only allowed as an edit of state A. Video calls attach both state images, labelled "start state" and "end state".
- **Cheapest test:** one Nano Banana edit (~1.5 cr), then eyeball both for the layout match (free). Then fold it into the F-1 test.

### F-3. A "multi-camera tripod" phrase makes Seedance cut the scene into many angles on its own · NEW
- **What / how:** instead of one moving camera, describe the shoot as *"a casual multi-camera TV shoot… a set of fixed tripod angles joined by hard cuts with no zooms"*. Seedance 2.5 returned **7 angles** (wide, blender close-up, face), all hard cuts with consistent characters and "nothing that looks inconsistent", with no editing. The board-free alternative to playbook #1 for UGC:
  - "two phones filming: one propped on the dresser (wide) and one on a mini tripod on the desk (close). Fixed angles joined by hard cuts, no zooms, no camera movement."
  - Tripod framing also frees both hands (F3).
- **Fixes:** F1 F7 F3 F9 (no board step).
- **Evidence:** `eflfUwTdSEc @09:11–09:41`, same creator (4 characters, 4 lines and 1 physical gag in a single prompt). **B**
- **Cutroom input change:** add `camera_holder = propped_multi` as a mode. The prompt block names 2–3 physical phone positions (from the room GEO block). The anti-morph lint still applies (each position = a different distance band).
- **Cheapest test:** one Seedance 15 s with this phrase vs the same prompt with a single propped camera. 1–2 videos.

### F-4. Declare the invariants once; only the touched object moves · NEW
- **What / how:** *"I say once that everything except him and that one object doesn't move, and I don't have to repeat or restate it ever again."* The only object allowed to change is the one the hand touches. The creator calls these "freeze rules".
- **UGC version:** "The only objects that move are her hands and the hoodie she is holding; every other object in the room stays exactly where it is." This is one sentence, placed once, early in the prompt, and not repeated. It fits the playbook's "Seedance follows the first 2–3 instructions".
- **Fixes:** F7 (props appearing or moving), F2.
- **Evidence:** `eflfUwTdSEc @02:55–03:26` (a 30 s take held it). **B/C** (shown on a stylised scene, not UGC).
- **Cutroom input change:** auto-generate a `moving_objects[]` sentence from the hand roles and state scope, and insert it once.
- **Cheapest test:** A/B inside the F-1 or F-3 test, adding one sentence. 0 extra.

### F-5. Write a camera reveal as an ordered list of what enters the frame · NEW
- **What / how:** *"Instead of describing the final wide shot and hoping it comes out right, I write the layers in the exact order I want them shown. The cup, then the house, then the village… the model just moves outward through that list."*
- **SANTO example (pull-back):** "starts on the embroidered SANTO chest logo → her chin and face → her whole upper body in the hoodie → the bedroom behind her."
- **Fixes:** F7 F2 (the product is the first, sharpest element).
- **Evidence:** `eflfUwTdSEc @06:36–07:07`. **B/C**
- **Cutroom input change:** a `reveal_order[]` field for any shot with a camera move, rendered as "first… then… then…".
- **Cheapest test:** one Wan 3.0 draft (~3.5 cr).

### F-6. First-person hands-only POV: face banned, "slow steady glide" · EXT #6 (`camera_holder`) / CONTRA (micro-shake)
- **What / how:**
  - For first-person takes: *"the camera stays at his eye level and only ever shows his hands and arms, never his face or his reflection."*
  - Unspecified first-person movement "tends to start shaking, which looks like handheld footage that's hard to watch", so he prompts *"a slow, steady glide instead"*.
  - A face-free POV unboxing removes face drift and lip-sync risk completely; voice-over carries the audio.
- **Fixes:** F1 F8 F3 F6.
- **Evidence:** `eflfUwTdSEc @12:32` (hands-only rule; 30 s one-take, 3 characters, 7 lines of Japanese dialogue from others), `@03:26` (glide). **B**
- **Cutroom input change:** add `camera_holder = pov_chest` / `pov_eye`, and auto-insert "never her face or her reflection". Use a *named, small* motion ("gentle breathing sway") rather than "handheld", which over-shakes in POV.
- **Cheapest test:** one Seedance 10 s POV mailer open with VO.

### F-7. Seedance 2.5 long-take settings and observed failure modes · EXT playbook contradiction 8.1, #14, #30
- **What / how:**
  - Settings: **30 s one continuous take, audio ON, 720p, 16:9**. "Anything I want to hear has to be written straight into the prompt, which is why **every prompt I'll use ends with a paragraph describing the sound**."
  - Observed defects:
    - **"visibly drops frames halfway in"** on a 30 s take
    - slow motion still crept into a small hand action ("the slow-motion part like when he was putting this little toy car on the shelf")
- **Fixes:** F9 F6.
- **Evidence:** `eflfUwTdSEc @00:31–01:33`, `@02:55`, `@05:31`, `@14:40`. **B**
- **Cutroom input change:**
  - The sound paragraph is a mandatory last block. The realism block stays first.
  - Duplicate-frame QA is mandatory for any take over 15 s.
  - Keep the "real-time speed, never slow motion" clause even on small placing actions.
- **Cheapest test:** free. Run the duplicate-frame detector on existing long takes.

### F-8. Character-sheet template specifics (settings, swap paragraphs, extras) · EXT #11
- **What / how:**
  - **Panels:** headless full-body front / back *with* head / tight face close-up. "Taking the face out of that panel forces the model to lock in the body and outfit on their own."
  - **Settings:** GPT Image 2, **quality high, 4K, 16:9**.
  - **Template:** the structural prompt is written once. Only **two paragraphs are swapped per person: "who they are" and "what they're wearing"**.
  - **Non-humans:** a side profile replaces the headless front, and a prop the animal will use (a shoe in its mouth) is pre-placed in the sheet.
  - **Background people get no sheet**; they're described in the prompt only.
  - What he checks on each sheet: "little folds on her blouse", "messy-looking hairs", "slight dark circles".
  - Kling/Freepik equivalent (`Z3vY2U8ysL0 @07:19–09:41`): base character on a neutral background, then 3 views (full body, front close-up, side profile), registered as a named character and called as `@presenter` in each shot. `b_RghITuQQM @10:19` uses side / front / back.
- **Fixes:** F1 F2 F5.
- **Evidence:** `eflfUwTdSEc @03:58–04:29`, `@07:38`, `@08:09`. **B**
- **Cutroom input change:**
  - The persona template holds a fixed structure plus two swappable paragraphs.
  - The outfit paragraph is filled from the SKU canonical description, so the sheet already wears the exact SKU.
  - Sheet QA checks include "fabric folds present".
- **Cheapest test:** one GPT Image 2 sheet (cost via `get_cost`).

### F-9. Identity-reference wording, and strip small accessories from sheets · EXT #9 / #5
- **What / how:**
  - Attach the sheet **plus the original character image** "just so that I have an extra reference of him".
  - Prompt: *"Image one is used for his identity"* + descriptors + *"do not recast, do not beautify, do not use as an image background."*
  - He **removed a small hat from the sheet**: "you don't want to have the AI use such small details… it's not going to look sharp… it might even change the characteristics of your character."
  - He prefers **Seedream 5.0 Pro** (transcribed as "SeaArt") at 2K for sheets over GPT Image 2, which he finds "way too noisy". He also finds "each time the image gets slightly worse" across passes, which agrees with the playbook's 2-pass rule.
- **Fixes:** F1 F6 ("do not beautify" counters the beauty floor).
- **Evidence:** `Zo8KaTs0l6k @04:46–05:50`. **B**
- **Cutroom input change:** the identity reference line template gets the "do not recast, do not beautify, do not use as background" suffix. The persona accessory inventory defaults to none (no small hats or rings); identity markers must be large enough to survive (a mole, not a tiny stud).
- **Cheapest test:** 0. Add the wording to the next scheduled render.

### F-10. Accent and voice by text: a 5-part formula · EXT #6
- **What / how:** "You don't just want to write out add in an Irish accent." Name the speaker, then give **region, pace, energy, emotional state, exact line**. His example:

  > *"[Clement] speaks English with an unhurried Kingston accent, natural, not exaggerated, not a comedy voice. When the shock hits, the voice jumps and the words get short."*

  Put spoken lines in a dedicated delimiter so Seedance knows the words are dialogue. He uses separate symbols for dialogue, SFX and music. The exact symbols aren't legible in the transcript.
- **SANTO example:** "She speaks English with a relaxed South-London accent, natural, not exaggerated, not a presenter voice; mid-energy, slightly amused; when she sees the fleece inside, her voice drops and slows."
- **Fixes:** F8.
- **Evidence:** `Zo8KaTs0l6k @10:05–10:35` (shown Jamaican-accent result). **B.** The playbook says text alone gets an accent right about 1 time in 3; this formula is the text half to pair with the 5–10 s voice sample.
- **Cutroom input change:** persona voice fields `accent_region`, `pace`, `energy`, `anti_caricature` ("natural, not exaggerated"), plus `emotion_shift` per beat.
- **Cheapest test:** one Kling 3.0 Turbo talking shot, formula vs "British accent".

### F-11. Three-stage scene prompt (setup / primary event / end state) plus performance verbs · EXT #4 (motion)
- **What / how:**
  - Structure each continuous take as:
    1. **setup** (where, who, "no one else is present")
    2. **primary event**, including who speaks first, the tone ("quiet and broken"), the interruption and pauses
    3. **"the end state of this scene is…"**, a frozen description of the final frame
  - Acting uses **physical performance words per beat**, not emotions: "riding happily with loose shoulders and a broad smile" → "loses the smile and tightens the fingers" → "looks behind slowly and reluctantly" → "releases one shaky breath".
- **Fixes:** F6 (acting), F8, F4 (the end state pins the final frame).
- **Evidence:** `Zo8KaTs0l6k @08:29–09:33`, `@11:07–11:38`. **B**
- **Cutroom input change:** the shot prompt renderer emits `SETUP / EVENT / END STATE` sections. The `end_state` field (which exists) is rendered as a literal final-frame description.
- **Cheapest test:** 0. Template change on the next render.

### F-12. Counted foley tied to contact events; diegetic vs non-diegetic kept separate · EXT #6
- **What / how:**
  - Sounds are written as **counted, per-contact events**: *"each step produces one closed rubber sole squeak followed immediately by one small wet splash beneath the corresponding foot"*; *"a soft hydraulic door closing with a hiss with a heavy steel door slam."*
  - Non-diegetic sound (sub-bass hits, music) is named as such and delimited separately.
  - For UGC, keep diegetic only (playbook: no music).
- **SANTO example:** "each time her fingers grip the mailer there is one dry plastic crinkle; one long papery rip as the top tears; one short zip rasp that stops when the zip reaches her chin."
- **Fixes:** F8.
- **Evidence:** `Zo8KaTs0l6k @16:25–18:12`. **B**
- **Cutroom input change:** add a `foley[]` field per shot as {event, count, material, sync-to-visual}. It's rendered into the closing sound paragraph (F-7), and each item is tied to a hand action that exists in the spec.
- **Cheapest test:** 0 extra. Add it to the F-1 test render.

### F-13. Kling 3.0 multi-shot: limits and gotchas · EXT #26, §4 routing
- **What / how:**
  - **Limits:** up to **6 shots in 15 s**, with custom per-shot lengths. Omni takes **up to 7 references**.
  - **Multi-shot is unavailable when both start and end frames are set.**
  - **More references means more glitches.** With 4 references, a dog grew a tail out of its head.
  - **Lip-sync breaks after about 10 s.** "Let the dialogue happen in the first 10 seconds, and then have the rest of the 5 seconds… as action… not dialogue."
  - **Morphing in longer scenes.** Fix with "less complex prompts, or make it less than 10 seconds".
- **Positives:**
  - It carries **motion momentum across cuts**: a lean-in continues in the next shot.
  - An **unreferenced secondary character stayed consistent** across the shots of one generation.
  - Strong on expressions and emotion.
- **Negative:** props **appear from nowhere** ("grabbing a prawn out of thin air").
- **Prompt order per shot:** camera → subject → action → environment → (lighting, texture, audio optional).
- **Meta-prompting:** he loads Kling's official guides into a custom GPT that writes multi-shot prompts from the reference image plus an idea, but "still double-check and rewrite sentences".
- **Continuation:** grab the last frame of a clip as the next start frame.
- **Fixes:** F8 F7 F9 F1.
- **Evidence:** `b_RghITuQQM @01:31–02:32`, `@05:09–06:11`, `@09:47`, `@12:53`, `@15:24`, `@16:56–17:26`, `@20:03`, `@21:36–22:08`, `@22:41–23:42`. **B**
- **Cutroom input change:** Kling routing lint:
  - speech only inside 0–10 s of any generation (tighter: the playbook's 8 s)
  - ≤3 references per Kling Omni call
  - don't request multi-shot with an end frame
  - a "hands empty unless the prop is on a surface in frame 1" rule against props appearing from nowhere
- **Cheapest test:** 0. Lint past Kling renders for speech after 10 s vs rejected lip-sync.

### F-14. "Action mapping": cover one physical action from 4–5 angles in one Kling multi-shot · EXT #1 (Kling variant), #28
- **What / how:**
  1. Pick **one physical action** (walks in → opens the door → gets in).
  2. Cover it the way a crew would: wide, side, close-up on the handle, interior, reaction. Put all of it in **one Kling 3.0 multi-shot from one anchor frame**.
  3. Use 4–5 shots in 15 s, about 3 s each. **Keep each shot instruction simple**: "Kling is great at realism, lighting and texture, but it can struggle when you ask for complex camera moves."
  4. Make the anchor frame in Nano Banana Pro, generating variants "until you get one that looks like it could be a real photo".
  5. **Run the same multi-shot several times with identical first frame and prompts, and splice the best parts.**
- **SANTO map for "opens the mailer":**
  - wide (propped phone)
  - hands on the mailer (close)
  - face reaction
  - hoodie held up (mid)

  Cutting on the action also hides the tear (a cut-to-transform).
- **Fixes:** F1 F7 F4 F9.
- **Evidence:** `Z3vY2U8ysL0 @01:37–06:18` (shipped a car-dealer ad), with the dialogue variant at `@09:08–10:44`. **B**
- **Cutroom input change:** a storyboard "action" object with `coverage[]` angles. The same seed/prompt is run N=2–3 times and the output goes to a splice picker rather than a reroll.
- **Cheapest test:** one Kling 3.0 15 s multi-shot of the mailer action (cost via `get_cost`).

### F-15. Start/end frames: the physically-achievable-path rule · EXT (first+last frame, known in BRIEF)
- **What / how:**
  - A start→end pair works when the transition is **something a real camera or object could do**: "If I had to do that in real life, all that is is just zooming out as a camera."
  - **Every object in the start frame needs a path to the end frame.** His failure: man seated at a table → standing in front of it. "Where does that table go?" He walked through the table and it vanished.
  - **Start and end must share the same plane and object positions.** A dial rotated differently in the start frame caused a morph; the fix was an end-frame crop re-used as the start.
  - Impossible jumps survive only with a **360° orbit** between them.
  - Prompts stay short: *"slow zoom out with snake coming out of the shoe."*
  - **5 s beat 10 s** for the same pair: the 10 s version was slower and still hallucinated. If a clip reads slow, generate at 10 s and speed it up.
  - **720p until final.**
- **Fixes:** F4 F7 F9.
- **Evidence:** `aw6N7M4fPuo @01:01–03:37`, `@03:37–04:08`, `@05:09–05:40`, `@06:42–07:46`. **B**
- **Cutroom input change:** a start/end lint that diffs the object inventory of both frames (vision model, free):
  - Any object present in one frame and absent from the other, with no exit path, blocks the call.
  - The camera delta must be one real move (zoom, pan, orbit).
  - Default duration 5 s.
- **Cheapest test:** 0. Run the lint on past start/end pairs vs their verdicts.

### F-16. Colourway-swap transition from one edited frame · NEW
- **What / how:** take a product frame, edit it with Nano Banana Pro into a **different colour or silhouette with everything else in exactly the same position**, and use it as the end frame. Prompt a simple transition. He cites Balenciaga's Instagram doing the same with a bag.
- **SANTO use:** the same hoodie in black → heather grey on the same bed or body. It shows the range in one 5 s clip and is a cheap derivative for product-only B-roll.
- **Colour rule:** use the **real photo of each colourway** as the edit target reference (keep the ΔE check), not the model's idea of "grey".
- **Fixes:** F9 (a cheap derivative), F2 if real colourway photos are used.
- **Evidence:** `aw6N7M4fPuo @04:08–04:38`. **B/C**
- **Cutroom input change:** a "colourway reveal" template: start = approved still, end = masked recolour of the same still using the colourway's hex and photo.
- **Cheapest test:** one Nano Banana edit (1.5 cr) + one Kling 2.5 Turbo / Wan 5 s.

### F-17. "Character lock" and "setting lock" blocks pasted verbatim into every scene; the LLM told the tool's clip limit · EXT #10
- **What / how:**
  - Tell the script LLM the generator's limit ("my AI tool only generates eight-second clips"), so it **splits the script into 8 s scenes**.
  - Have it output a **Character Lock** and a **Setting Lock** section. Paste both unchanged into every scene: "Don't modify those. Simply copy them over exactly as they are."
  - Per scene, only **the reference image and the scene-specific prompt** change.
  - Upstream: Claude analyses the site and product page → generates angles → picks one ("durability") → script.
  - The shipped script is **spec-dense**: "500-lb capacity, 18-gauge welded steel… 4 in of fire-deterrent foam, chrome footring, 5-year frame warranty".
- **Fixes:** F1 F7 F2.
- **Evidence:** `boxfGGa4sXk @00:32–01:03`, `@01:03–02:05`, `@02:37–04:42` (agency client ad; no performance numbers). **C/B**
- **Cutroom input change:** canonical blocks for **persona and room**, not just the SKU, stored once and injected byte-identical. The model's per-generation length limit is passed to the script step so beat splits match generation boundaries. For the script: numbers-first product claims ("400 gsm", "brushed-back fleece").
- **Cheapest test:** 0. Diff past prompts for paraphrased persona or room text.

### F-18. Higgsfield reference "eligibility" gate: check before you plan · NEW (gotcha)
- **What / how:**
  - In Higgsfield, each generated character or location asset must pass **"check eligibility"** before Seedance 2.0 will take it as a reference. "Not every generation will come back as eligible on the first try. So if it does not pass, just regenerate until you get one that does."
  - She checks again at upload in the video tab.
  - Characters made from your own photos use "clear, well-lit shots from different angles".
- **Fixes:** F9 (a board or keyframe is built around an asset that later can't be used).
- **Evidence:** `ez8gfygg8ho @02:33–03:04`, `@04:07–04:39`. **B**
- **Cutroom input change:** run an eligibility check at **asset intake** (persona, room) and store an `eligible_for[seedance]` flag. The storyboard can't use ineligible assets. Open question: is it exposed through the MCP or API, and is it free?
- **Cheapest test:** 0 if the check is free. Check the current persona and room assets.

### F-19. Hair drifts between segments even with identical references · EXT #11 (identity markers)
- **What / how:** with the same references and settings across four 15 s Seedance 2.0 segments, the persona's **hair differed from the reference in one segment** and was back to normal in the next. "Fine details like hair can drift slightly from one generation to the next… factor in when you are choosing which generations to keep." Complex motion (a windmill into a head spin) "took a few tries".
- **Fixes:** F1.
- **Evidence:** `ez8gfygg8ho @05:10–05:41`, `@06:41`. **B/C**
- **Cutroom input change:** personas get a **simple, fixed hairstyle** (tied back, or short). Hair outline is added to the face-similarity QA as a separate check. Shots after the first repeat a one-line hair descriptor.
- **Cheapest test:** 0. Add it to the QA checklist.

### F-20. Higgsfield Marketing Studio UGC preset: exact settings and behaviours · EXT playbook T23 (Marketing Studio baseline)
- **What / how (official channel):**
  - **One product per ad.** "I already separated them one by one."
  - Avatar plus a **minimal prompt**: *"a cozy home setting as the woman removes the cap. She says, 'Okay, I finally got it.'"*
  - **Hook presets:** Epic fail, Product crush, Random object mic, "spicy". **Setting presets:** rooftop, volcano, airplane wing.
  - Output settings: **9:16, 1080p, 15 s**.
  - **A blank prompt produces an auto-script** from the product description. It came out as "best one I've tried this year", "Trust Grandma", which is exactly what the script linter bans.
  - Avatars can be made from text ("elegant 60-year-old woman").
  - **Only one avatar slot.** A second person goes in as an attached reference.
  - A **location image can be a second input** (made in Soul Cinema).
  - TV Spot and Wildcard are 16:9. The presenter quotes "nine bucks" for a Wildcard ad.
- **Fixes:** F9 (baseline), F8 (script QA still needed).
- **Evidence:** `fmgVm-fxPDM @07:47–10:56`, `@11:58`, `@15:53`, `@17:58`; `aZV03WzrUPI @05:12–06:47` (Claude writes a "scene-by-scene 15-second breakdown" script for the same preset). **B**
- **Cutroom input change:** the benchmark run uses one SKU per ad, a real room photo as the location input, and a *Cutroom-linted* script (never the blank-prompt auto-script).
- **Cheapest test:** one Marketing Studio UGC run with a SANTO hoodie and a real room photo (cost via `get_cost`).

### F-21. Product-preservation sentence + a brand-kit sheet as a single reference · EXT #10
- **What / how:**
  - The official demo attaches a brand-kit image (logo, palette, typography, products) and says: *"Use the products from the attached image exactly as shown. Preserve their shape, design, and proportions. Do not redesign them."*
  - Logos, tiny text and product shapes stayed consistent across the poster and billboard.
  - Earlier product variants were made by **referencing the first product's packaging** so the family matches (`aZV03WzrUPI @04:12`).
- **Fixes:** F2.
- **Evidence:** `fmgVm-fxPDM @04:42–06:45`. **B** (vendor demo, stills only).
- **Cutroom input change:** add the verbatim "preserve… do not redesign" sentence after the product reference line on every still. Build a SANTO brand-kit sheet (logo, true colour hexes, mailer, hero SKUs) as the reference for static derivatives.
- **Cheapest test:** one GPT Image 2 / Nano Banana still (~1.5 cr).

### Minor / not carried forward
- **Post (`Zo8KaTs0l6k @19:19–21:56`):**
  - Trim out slow-motion segments (known).
  - A slow digital push 100%→120% for emphasis.
  - A light noise overlay: "especially the noise plays a huge part".
  - Edge blur and 10–15% cinema bars. These are cinematic, **not for UGC**.
- The noise overlay supports the playbook's "sensor noise" finish.
- `ez8gfygg8ho @07:11`: Seedance native audio landed a "beat dropping to silence" exactly on a freeze. This is evidence that sound events described in the prompt sync to visual beats (it supports F-12).

---

## 3. Contradictions with the playbook

1. **Showing state changes on camera (STOP #4) vs F-1/F-2.** `eflfUwTdSEc` shows continuous 30 s takes where state changes (wet → dry hand, messy → clean room) hold. It works because the change is written as occluded state → instant-after → persists, with explicit before/after plates. **Reconcile:** it's not "never show". The change happens *under an occluder* inside the shot, which is the playbook's "behind something that hides the body" (#39) done in one take. Test the mailer both ways (T9).
2. **Handheld micro-shake vs "slow, steady glide"** (`eflfUwTdSEc @03:26`). In first-person POV, unspecified handheld over-shakes. **Reconcile:** never write bare "handheld" for POV. Name a small, specific motion (breathing sway) or a glide.
3. **Lip-sync wall: 8 s (playbook) vs about 10 s** (`b_RghITuQQM @22:41`). Same direction, looser number. Keep 8 s as the lint and treat 10 s as the hard ceiling.
4. **One 15 s call vs a 30 s single take** (`eflfUwTdSEc`). Seedance 2.5 does hold 30 s, but the creator saw **dropped frames halfway** and creeping slow motion. This supports keeping ≤15 s blocks for ads and QA-ing anything longer for duplicate frames.
5. **Cinematic realism recipe vs the banned-word list** (`Zo8KaTs0l6k @05:50`): "35 mm, f/1.8, shallow depth of field, visible fine film grain, muted desaturated grade", plus edge blur and cinema bars. This is a *cinema* look, not phone UGC, so it doesn't override the ban. His "do not beautify" and noise overlay do agree with the playbook.
6. **Sheet model choice.** `Zo8KaTs0l6k` drops GPT Image 2 for sheets ("way too noisy", degrades on each pass) in favour of Seedream 5.0 Pro. `eflfUwTdSEc` and Higgsfield's recipe use GPT Image 2 (4K, high). This is unresolved: a 2-image A/B on the SANTO persona.
7. **1080p, background music and first-person purchase claims** (`boxfGGa4sXk`: "I bought 24 for my second location", music added; `fmgVm-fxPDM`: 1080p). These conflict with 720p, no music, and no first-person testimonials. No performance data was offered, so the playbook stands.
8. **Kling multi-shot consistency from a single reference** (`b_RghITuQQM`, `Z3vY2U8ysL0`) vs the playbook's "Seedance board first". This isn't a real conflict, but it means Kling multi-shot is a credible *cheaper* one-call route for short action coverage. Add it to the T10 bake-off.

---

## 4. Top 5 most valuable findings

1. **Named-state continuity (F-1)** (`eflfUwTdSEc @12:02`): write a state change as "fully covered by X / changed the instant X comes away / changed from then on", plus "the only [torn] thing is…". This is a concrete prompt pattern for the mailer rip and hoodie pull-on (F4).
2. **Make the "after" state by editing the "before" master, and attach both (F-2)** (`eflfUwTdSEc @13:04`): generated separately they "come out as two different rooms". Fixes F4/F7 for about 1.5 credits.
3. **The "multi-camera, fixed tripod angles, hard cuts, no zooms" phrase (F-3)** (`eflfUwTdSEc @09:11`): Seedance auto-cut 7 consistent angles from one prompt. It's a board-free one-call route, and tripod framing frees both hands (F1 F3 F7 F9).
4. **Kling 3.0 limits (F-13)** (`b_RghITuQQM @12:53–23:42`): dialogue only in the first 10 s; no multi-shot with an end frame; more references means more glitches; props appear from nowhere. Plus **action mapping with identical re-runs spliced (F-14)** (`Z3vY2U8ysL0 @05:47`). All of it can be linted for free.
5. **The start/end physically-achievable-path rule (F-15)** (`aw6N7M4fPuo @02:33–05:40`): every object needs a real path between frames, on the same plane and positions; 5 s beats 10 s. This can be a free lint. Runner-up: **character and setting lock blocks pasted verbatim, with the script split to the model's clip limit (F-17)**, and the **Higgsfield eligibility gate (F-18)** as an F9 gotcha.

---

## 5. STOP DOING (new, from this batch)
- Writing a state change as an action verb ("he dries his hand"). Write the states instead (F-1).
- Generating before and after state images independently (F-2).
- Bare "handheld" for first-person POV. It over-shakes (F-6).
- Kling: talking after about 10 s; more than 3 references; asking for multi-shot with an end frame (F-13).
- Start/end pairs where an object has no physical path, or where the planes differ (F-15).
- Small accessories (hats, tiny jewellery) on identity sheets (F-9).
- Marketing Studio blank-prompt auto-scripts ("best one I've tried this year", "game changer", "obsessed") (F-20, `aZV03WzrUPI @06:15`).

## 6. Open questions
- Is Higgsfield's "check eligibility" exposed through the MCP, is it free, and what fails it (realistic faces, real-person likeness)?
- Which delimiters does Seedance 2.5 actually treat as dialogue, SFX and music? (`Zo8KaTs0l6k @10:35`, `@17:41`; the symbols aren't legible in the transcript.)
- Does the named-state pattern (F-1) hold for a *tear* (irreversible, with a new geometry), or only for simple wet→dry and messy→tidy changes?
- Does the multi-camera phrase (F-3) respect the anti-morph distance rule by itself, or do the camera positions need explicit distance bands?

---

# PART 13 — `09c-transcripts.md`

## 09c: YouTube transcript mining (batch C, 9 videos)

**Date:** 2026-09-24 · **Source:** full transcripts in `research/transcripts/` (no web search). Timestamps are the transcript's `[mm:ss]` markers, so a quote sits in the ~30 s block that starts at the cited time.
**Tags:** NEW = not in `QUALITY-PLAYBOOK.md` · EXTENDS #N = adds specifics to playbook item/rank N · CONTRADICTS = conflicts with the playbook (see §3).
**Grades:** B = one credible practitioner showing results on screen · C = claim or anecdote. None of these is A: they are single creators, most of them sponsored.

---

## 1. Per-video summary

| Video | Speaker / channel (from content) | Topic | Relevance 0–3 |
|---|---|---|---|
| `goZDcGw-WsU` | "Digital Assets" (sponsored by Elser AI) | Kling 3.0 prompt frameworks: 6-part order, an 8-layer "prompt spine", multi-shot up to 6 beats, JSON prompts. Cinematic and anime focus. | 1 |
| `iWLTy0B5_NE` | Unnamed FlashBoards creator (sponsored) | Style tests of a new Seedance version (product ad, sitcom, vlog, POV, long takes) plus an old vs new comparison. Almost no settings. | 1 |
| `k6jn5xjqYSo` | Arthur Winer, AI Master (own platform) | Kling 3.0 walk-through: Elements (character and product sets), multi-shot limits, start/end frames, known weaknesses (distance, text). | 2 |
| `kC12eMs0SF0` | Unnamed creator with a Skool community (OpenArt affiliate) | Seedance 2.5 short-film workflow: Claude MD template → portrait → 3-panel sheet → location → 30 s blocks. Gives exact image settings, reference order and duration padding. | 2 |
| `lkL8mlpVScY` | Unnamed creator with a Skool community (Higgsfield affiliate) | Seedance 2 masterclass: timeline prompting, rules blocks, the character limit, one-take "logic rule", real-photo references vs sheets, a voice-clone realism test. **Best source in this batch.** | 3 |
| `o-xhRksFBAc` | Unnamed tutorial creator (Arcads affiliate) | Arcads.ai skincare testimonial: audio-first A-roll, Nano Banana Pro keyframes ×3, Veo 3.1 B-roll. | 2 |
| `tfs8U3CbAOs` | Jamie, "Teachers Tech" (sponsored by Higgsfield) | Seedance 2.0 on Higgsfield for beginners. Hard numbers: reference limits, Fast = half credits, 66 credits per 11 s, 2,500-character prompt cap. | 2 |
| `wc4VOgT7S58` | "Indie No-Code" | Higgsfield MCP inside Claude: a Soul character brought into Marketing Studio as an avatar, then a batch of UGC prompts made from a folder of product photos. | 2 |
| `z84WQAn6U0I` | Jack (channel unnamed; runs his tests on Higgsfield) | Kling 3.0 review: multi-shot limits, late-clip dialogue drift, 3×3 grid storyboard trick, product-ad tests vs Kling 2.6. | 2 |

No video in this batch is fully irrelevant. `goZDcGw-WsU` and `iWLTy0B5_NE` are mostly hype with one or two usable lines each.

---

## 2. Findings

### C-01 Seedance "Fast" costs half and outputs the same 720p: use it for iteration. Cost data point: 66 credits per 11 s · EXTENDS #29 and §7
- **How:** On Higgsfield's Seedance 2.0 there are two versions: "fast is going to be half the credit… Both can output in 720p… if you're iterating lots… I would definitely use fast" (`tfs8U3CbAOs @03:48`). An **11 s, 720p, 16:9 clip with audio on standard cost 66 credits**, and "If I turned it to fast, it'd be about half that" (`@05:58`). That is **~6 credits/s on standard and ~3 on Fast**, which is far above the brief's "~18 credits" and in line with the playbook's community figure (67 credits for 15 s). Duration runs 4–15 s; resolution options are 480p and 720p (`@04:20`). He also finds standard follows detailed prompts better (`@03:48`).
- **Fixes:** F9
- **Evidence:** Jamie (Teachers Tech), `tfs8U3CbAOs @03:48, @04:20, @05:58`. Grade **B** (credit cost shown in the UI).
- **Cutroom input change:** add a `render_tier` field: `draft` (Fast, 480–720p) for any shot template not yet proven, `final` (standard, 720p) only once the draft passes QA. Store credits/s per model × tier in the router and show the cost before spending.
- **Cheapest test:** `get_cost` on Seedance standard vs Fast at 480p and 720p for 11 s and 15 s (0 credits).

### C-02 480p "proof render" for prompts you are unsure of · EXTENDS #28
- **How:** "It's quite expensive Seedance in 1080p… sometimes 720p is worth it… especially if you're not sure about a prompt, I would maybe even do 480p just to save some credit. But… if you're pretty sure about your prompt, just do 1080p" (`lkL8mlpVScY @03:40–04:11`). The same speaker suggests upscaling a 720p clip later; the playbook says no generative upscaling (see §3).
- **Fixes:** F9
- **Evidence:** Unnamed Seedance creator, `lkL8mlpVScY @03:40`. Grade **C**.
- **Cutroom input change:** new shot templates render at 480p Fast first. Promote to 720p standard only when timing, blocking and hands pass. Never promote to 1080p for UGC.
- **Cheapest test:** re-render one existing rejected shot at 480p Fast and check whether the defect shows at 480p too. If it does, 480p is a valid predictor (~1/4 of the standard 720p cost; confirm with `get_cost`).

### C-03 Hard prompt length caps; overflow is silently cut off · NEW
- **How:** Seedance 2.0 on Higgsfield: "2500 characters is the limit" (`tfs8U3CbAOs @05:26`), and "if it didn't fit in, it will just get cut off" (`@07:34`). His method is to tell the LLM "you have 2500 characters to work with" (`@05:58`). **Kling 3.0 multi-shot: each shot's prompt is capped at 500 characters** (`k6jn5xjqYSo @07:44`, repeated in the recommended workflow at `@19:17`).
- **Why it matters for us:** Cutroom appends long blocks (canonical SKU description, realism block, reference-role lines). If they go past the cap, the tail is lost without warning. That is usually the garment lock or the negatives, so this is a hidden cause of F2.
- **Fixes:** F2 F9 (and F6 if the realism block sits at the end)
- **Evidence:** `tfs8U3CbAOs @05:26, @07:34`; `k6jn5xjqYSo @07:44`. Grade **B**.
- **Cutroom input change:** the linter hard-fails any Seedance prompt over 2,500 characters and any Kling multi-shot shot prompt over 500. Order blocks so the must-survive ones (reference key, realism, garment lock) come first. Tell the LLM prompt-writer the exact budget.
- **Cheapest test:** 0. Measure character counts of the last 20 Cutroom prompts and count how many went over.

### C-04 Kling 3.0 multi-shot limits and per-shot rules · EXTENDS #4
- **How:**
  - Up to **6 shots per 15 s** on Higgsfield (`z84WQAn6U0I @02:04`). Also: "you can go up to six shots per prompt if the motion hierarchy is clean" (`goZDcGw-WsU @04:22`).
  - **Each shot at least 3 s** on AI Master's Kling (`k6jn5xjqYSo @07:44`). Jack's Higgsfield UI appears to allow shorter shots ("one scene that's 2 seconds", `z84WQAn6U0I @01:33`), so the floor may differ by host.
  - Duration is any whole number from 3 to 15 s (`k6jn5xjqYSo @01:02`).
  - Two ways to write it: one prompt that describes every shot, or per-shot fields with their own durations (`z84WQAn6U0I @01:02–01:33`).
  - "Each shot has one purpose, one dominant action, one clear camera move… don't overload each shot" (`goZDcGw-WsU @04:22, @06:38`).
  - "We're not spinning the camera. We're not changing lighting midscene" (`@06:00`).
  - The 8-layer spine adds **"Reaction: what responds to the action"** and **"Constraints… underrated"** (`@02:18–03:21`).
- **Fixes:** F9 F6 F7
- **Evidence:** Jack `z84WQAn6U0I`; Arthur Winer `k6jn5xjqYSo`; Digital Assets `goZDcGw-WsU`. Grade **B**.
- **Cutroom input change:** give the shot-spec validator per-model limits. For Kling multi-shot: ≤6 shots, ≥3 s each (≥2 s on Higgsfield, to be verified), ≤500 characters per shot, exactly one action and one camera move per shot, lighting fixed across shots. Add a `reaction` field (what the fabric, bag or hair does in response) to fabric beats.
- **Cheapest test:** 0 (validator). Confirm the Higgsfield per-shot minimum with `models_explore` (free).

### C-05 Kling dialogue drifts in the last ~5 s: front-load speech and end on silent beats · EXTENDS #4 and #8
- **How:** "the dialogue can drift… at the end of long videos. So, if you are doing a 15-second video and you add a lot of dialogue towards the end, then you will probably start to see it kind of going off… use a lot of dialogue at the start of the video and then maybe use non-speaking scenes towards the end" (`z84WQAn6U0I @03:06`). In his home-style product ad: "the last 5 seconds or so, the dialogue kind of goes all weird and… out of sync" (`@09:33`). Too much dialogue makes it rush the lines: "it tries to get through all of the dialogue within the 15 seconds… make sure not to add too much" (`@15:38–16:09`). Kling 3.0 **doesn't invent speech when none is prompted** (2.6 did) (`@13:49`).
- **Fixes:** F8 F9
- **Evidence:** Jack, `z84WQAn6U0I @03:06, @09:33, @15:38, @13:49`. Grade **B**. It matches the playbook's "Kling loses sync after second 8".
- **Cutroom input change:** add a beat-order rule for Kling. SPEAK beats go in seconds 0–~9, and the final ~5 s are DO or product beats with no lip-sync (room sound or VO only). The script word budget is checked against the speaking window, not the whole clip.
- **Cheapest test:** one Kling 15 s clip with the same script front-loaded vs spread evenly (2 videos; `get_cost` first).

### C-06 Reference upload order must match the prompt's reference key · EXTENDS #9
- **How:** The LLM output includes an "upload order section" and a "reference key", e.g. female character sheet = reference 1, male sheet = reference 2, location = reference 3. "Follow the asset order Claude gave you exactly. Get it wrong characters might end up doing the opposite of their role, or your location gets treated as a character. Getting this order right the first time is what saves you from wasting credits" (`kC12eMs0SF0 @07:36–08:39`). The same practice appears as labelled references: "I labeled each and every one… subject, image one, young man. Then… secondary subject, image two" (`lkL8mlpVScY @09:21–09:54`).
- **Fixes:** F1 F7 F9
- **Evidence:** `kC12eMs0SF0 @08:07`, `lkL8mlpVScY @09:54`. Grade **B**.
- **Cutroom input change:** never let a human or LLM order the uploads. The app builds the reference array and the prompt's reference key from the same list (e.g. 1 = persona sheet, 2 = product, 3 = room), and the linter checks that every `@Image N` in the prompt matches the role of the Nth upload.
- **Cheapest test:** 0 (code). Look for role swaps among past rejects.

### C-07 Pad the render by +2 s so the last action completes, then trim · NEW (in tension with #14)
- **How:** "Always add two extra seconds to whatever your prompt's duration is… instead of 17 seconds, I'll set it to 19… AI video models often rush or cut off the final action of a shot when they're squeezed for time. That extra 2 seconds gives the model enough room to actually finish the motion naturally" (`kC12eMs0SF0 @08:39–09:41`). He says it's "the reason I rarely have to regenerate". The timeline stays as written; only the render length grows, and the extra is trimmed in CapCut (`@09:41`). Related evidence: a 15 s prompt with 10 shots squeezed the beats: "even this part being like 3 seconds, we couldn't really do all of that" (`lkL8mlpVScY @06:47`).
- **Fixes:** F9 F4 (actions cut off mid-state)
- **Evidence:** `kC12eMs0SF0 @08:39`. Grade **C** (a claim, no A/B shown).
- **Cutroom input change:** `render_seconds = min(cap, storyboard_seconds + 2)`. The playbook's end-trim (10–15 frames) takes off the pad. This must be squared with "don't give a 3 s action 8 s" (§3). The +2 s is spread over the whole timeline, not one action.
- **Cheapest test:** the same Seedance shot at 13 s vs 15 s with the same 13 s timeline, checking whether the last action completes (+2 s ≈ +12 credits on standard).

### C-08 Persona asset settings: portrait anchor → headless 3-panel sheet · EXTENDS #11 and #5
- **How:**
  - **Portrait first:** GPT Image 2, **4:5, 4K, quality high** ("You can also test Nano Banana 2. It's cheap"). "This clean, well-lit portrait becomes the anchor for your character's identity. Everything after this references back to it" (`kC12eMs0SF0 @04:30–05:01`).
  - **Sheet:** GPT Image 2, **16:9, 4K, high**, with the portrait attached and "add the image at the very start of the prompt" (`@05:01–05:33`). The panels are a close-up, a headless front full-body and a back full-body: "That headless center pose… locks in the character's face just once, instead of confusing the AI with multiple faces" (`@06:04`).
  - **Location:** Nano Banana 2 at 16:9 4K (Nano Banana Pro and GPT Image 2 also fine) (`@06:36`).
  - Second source: GPT Image 2 makes better sheets than Nano Banana Pro from one real photo. Nano Banana's "zoomed out versions are not that great" (`lkL8mlpVScY @19:53–20:25`).
- **Fixes:** F1
- **Evidence:** `kC12eMs0SF0`, `lkL8mlpVScY`. Grade **B** (same headless-sheet trick as the playbook, now with settings).
- **Cutroom input change:** persona intake presets: portrait (GPT Image 2, 4:5, high) → sheet (GPT Image 2, 16:9, high, portrait passed as the first input). Room plates on Nano Banana 2.
- **Cheapest test:** ~2 images: a GPT Image 2 sheet vs a Nano Banana Pro sheet from the same identity plate, compared on face similarity.

### C-09 Real close-up photos beat synthetic sheets; include a side or back view; reject distant photos · EXTENDS #11 and #44
- **How:**
  - A reference taken from far away makes the model invent the face: "I'm standing way too far away… the AI has to fill in all of the details, like… moles, all of the little skin texture" (`lkL8mlpVScY @20:55`).
  - A front-only reference makes the model guess the sides: "it only knows the front of your face… it doesn't know that the back of my hair is a bit longer" (`@19:53`).
  - A clip made from a **sheet only** "was obviously a bit more AI… I've noticed that this works best if you have like real selfies or real images of yourself" (`@22:59`).
  - The clip that fooled a friend used a **real screenshot from his own video + his voice clone + a 7 s single take** (`@22:28`).
  - Outfit swaps: append "But change his outfit to…" to the end of an otherwise unchanged prompt (`@21:26–21:57`).
- **Fixes:** F1 F6
- **Evidence:** `lkL8mlpVScY @19:53–23:29`. Grade **B** (on-screen comparison plus an informal n=1 blind check).
- **Cutroom input change:** persona intake needs a real close photo where the face fills most of the frame, plus a ¾ or profile view and a back-of-head view. Reject identity references where the face is small. For SANTO this favours building personas from a real (consenting, paid) model's selfies rather than purely synthetic Soul faces, with the sheet made *from* those.
- **Cheapest test:** one 7 s talking clip from a real-selfie reference vs sheet-only (2 short videos).

### C-10 Write habitual micro-behaviour and self-interruptions into the one-take · NEW
- **How:** The clip that fooled a friend was prompted as "7-second video, one shot, podcast mic, check, one take… the shot is, 'Okay, testing 1 2 3.' He looks off frame slightly, which is a thing I often do. Then, 'Is my mic working? Okay, pause. Okay, great.'" (`lkL8mlpVScY @22:28`). The realism comes from a personal tic, a glance off frame, a filler line and an explicit pause, not from adjectives.
- **Fixes:** F6 F8
- **Evidence:** `lkL8mlpVScY @21:57–22:28`. Grade **B/C** (shown result, anecdotal test).
- **Cutroom input change:** the persona record gets `mannerisms[]` (2–3 habits, e.g. "glances off-frame at her phone screen", "tucks hair behind her left ear"). One is injected into each SPEAK beat. The script allows written pauses and a throwaway opener that isn't a hook cliché.
- **Cheapest test:** one 7 s SPEAK clip with vs without a mannerism line and pause (2 short videos).

### C-11 One-take "logic rule": say why there is only one camera · NEW (extends the `camera_holder` field)
- **How:** "The thing I applied here is the logic rule… I just wanted to have it as one continuous shot because I'm holding the camera, I'm vlogging me… Not that it has multiple different camera angles because [Seedance] loves to do that. If you don't give it those instructions, then it will just come up with any type of camera angle… That is also why we only have one shot here, which is 0 to 10 seconds long" (`lkL8mlpVScY @18:52–19:23`). In his vlog prompt the capture device is named ("black DJI Osmo Pocket 4 with a flip screen") and he passes **a reference image of the device** as one of only two references (`@16:15–16:46`). Separately: "when it's like one shot like that, there's less chance of errors" (`tfs8U3CbAOs @07:02`).
- **Fixes:** F6 F7 F3
- **Evidence:** `lkL8mlpVScY @18:52`, `@16:15`; `tfs8U3CbAOs @07:02`. Grade **B**.
- **Cutroom input change:** for `camera_holder = selfie` beats rendered on their own, emit a causal one-take clause ("one continuous take from 0 to N s; the only camera is the phone in her right hand, so there are no cuts and no other angles"). This goes with the anti-morph board, not against it: use it for the selfie SPEAK segment. If a device ever shows (it shouldn't for SANTO), pass its real photo as a reference.
- **Cheapest test:** one Seedance selfie SPEAK beat with vs without the logic clause, counting unwanted cuts (2 short videos).

### C-12 Prompt diet: cut the LLM's invented detail; fewer shots per 15 s · EXTENDS #4
- **How:** A ~10-shot, two-page timeline in 15 s skipped and squashed beats ("we couldn't really see her pausing or reading the room"). "You might want to go easy on some of the details. Like, Claude just finds ways to put words in your mouth. The best thing you could do here is just go over the prompt, delete a few things… or let [Seedance] do the rest" (`lkL8mlpVScY @05:45–07:49`). The structure he recommends: first half is context (subject, wardrobe, environment, mood, music, colour logic, style), second half is timestamped shots (`@01:36–02:06`).
- **Fixes:** F9 F6 F4
- **Evidence:** `lkL8mlpVScY`. Grade **B**.
- **Cutroom input change:** cap actions per timestamped shot (one verb phrase per ≥1.5–2 s). Lint the LLM-expanded prompt against the shot spec and **strip any action, prop or line the spec didn't ask for**.
- **Cheapest test:** 0. Diff LLM-expanded prompts against their specs for the last 10 ads.

### C-13 A "RULES:" block of must-always invariants, added after a failure, and name every prop · EXTENDS brief "rule mining" and #9
- **How:** "I specifically gave it a few rules… the selected cards must always be an ace of hearts, and the woman in the red dress is the one who plays the card back… the reason why I came up with this rule is because after generating this like two times, it started doing it wrong… I also gave the negative prompt" (`lkL8mlpVScY @08:20`). He still got two aces on screen at once (`@08:51`), so a rule doesn't stop a prop being duplicated. Unspecified props go wrong: "I have a driver and a par three… I never specified that in the prompt" and "there was two balls rolling on the green" (`tfs8U3CbAOs @03:17`).
- **Fixes:** F2 F7 F4
- **Evidence:** `lkL8mlpVScY @08:20`, `tfs8U3CbAOs @03:17`. Grade **B/C**.
- **Cutroom input change:** each SKU or template holds `invariants[]` rendered as a short "RULES:" block ("The mailer bag is always the matte black SANTO bag; there is exactly one mailer in the scene"). Every rejection reason can become a new invariant. Every visible prop is counted ("exactly one").
- **Cheapest test:** 0. Turn the last 10 rejection reasons into invariants and apply them on the next scheduled render.

### C-14 Keep identity-critical people close; wide shots soften faces · EXTENDS #4 and #20
- **How:** "When your character is far away from the camera, the quality drops significantly… in wide shots or establishing shots… the facial details tend to soften… keep your characters close to the camera… Frame your shots tighter" (`k6jn5xjqYSo @17:11–17:44`). This matches the reference-side lesson in C-09.
- **Fixes:** F1 F6
- **Evidence:** Arthur Winer, `k6jn5xjqYSo @17:11`. Grade **B**.
- **Cutroom input change:** add a `distance_band` rule. Any beat where the face matters is mid or closer. Wide beats are back views, faces turned away or product-led, and kept short.
- **Cheapest test:** 0 (lint over past rejects: were the face-drift rejects wide shots?).

### C-15 Product and person "Element" sets: 4 angle photos plus a description; clone needs an emotion photo · EXTENDS #5 and #9
- **How:**
  - **Kling 3.0 product Element:** "a name, description, and four photos of your product from different angles." Referenced with `@name` in every shot prompt (`k6jn5xjqYSo @04:06, @08:47`).
  - **Kling person clone:** photos from different angles, "at least one photo showing emotions", plus a short verification video (`@03:36`).
  - **Higgsfield Seedance Elements:** 3 photos are enough; categories are character, location, prop or auto; the description is optional (`tfs8U3CbAOs @10:13`).
  - **Seedance watch ad:** "these images, each showing a different angle and detail of the watch" gave a detail-consistent product (`iWLTy0B5_NE @01:56–02:27`).
  - Kling Elements also accept **video** uploads of a character (`z84WQAn6U0I @11:38`).
- **Fixes:** F2 F1
- **Evidence:** `k6jn5xjqYSo`, `tfs8U3CbAOs`, `iWLTy0B5_NE`, `z84WQAn6U0I`. Grade **B**.
- **Cutroom input change:** each SKU and persona is saved once as a Higgsfield Element (category `prop` / `character`) built from the canonical kit (4 angles + detail + description). Prompts reference the element by `@name` in *every* shot, not just the first. Test a 5–10 s turntable video upload as the element source.
- **Cheapest test:** create one SKU element (element creation cost unknown; check it) and render one Kling multi-shot with vs without `@element` in every shot.

### C-16 Cheap storyboard: Higgsfield image "multi-shot" 3×3 grid → "generate the frames in sequence" · EXTENDS #1
- **How:** Make one keyframe, then "hover over the image, you can click on multi-shot where it will use that image and create nine different images from that scene… it still keeps the consistency". Download the whole grid as one image, upload it to Kling 3.0 at 15 s with the prompt **"generate the frames in sequence as per the storyboard"**. "It might not use all nine of those images, but it does a really nice job at cutting between" (`z84WQAn6U0I @05:40–07:13`). Text-only multi-shot from one start image also held person, bike and location consistent (`@08:32–09:02`).
- **Fixes:** F1 F7 F9
- **Evidence:** Jack, `z84WQAn6U0I @05:40`. Grade **B** (shown).
- **Cutroom input change:** add a board-generation route (one approved keyframe → 9-panel grid) as a cheap alternative to the gpt_image_2 21:9 board. Keep the 4/8-panel rule for the final call, since 9 panels in 15 s gets panels dropped. Use the grid mainly as a source of angle-consistent start frames.
- **Cheapest test:** one grid from an approved SANTO keyframe (cost unknown; check it) and a check of whether the garment print survives across all 9 panels before any video.

### C-17 Higgsfield MCP: bring the persona in as a Marketing Studio avatar (uploaded image), not a Soul character by name · NEW
- **How:** "You can try telling Claude to use the Soul character directly. Sometimes it works, but it is prone to breaking and not reliable enough for a production workflow. So… we are bringing the character we created into Marketing Studio as an avatar. This is the stable path… generate avatar from text or upload an image. We are choosing upload. Drag and drop the best image from the angles we generated" (`wc4VOgT7S58 @01:33–02:04`). Then Claude reads a folder of product photos and writes one UGC prompt per product with the same avatar (`@03:07–03:37`). Traits the presenter praised in the output: "soft, single source" lighting and "the way the clip ends mid-motion like a real social post" (`@04:38`), which matches playbook #24. **Counter-example:** the generated scripts are full of banned phrases ("Oh my god. Where has this been my whole life?", "Game over. Nothing else compares", "today years old", `@05:09–05:41`). This is exactly what the script linter must block.
- **Fixes:** F1 F9 (and F8 via the linter)
- **Evidence:** Indie No-Code, `wc4VOgT7S58`. Grade **C** (one presenter's reliability claim).
- **Cutroom input change:** since Cutroom drives Higgsfield through the MCP, store `marketing_studio_avatar_id` per persona (from an uploaded, approved identity image) and use it for Marketing Studio UGC calls, rather than relying on a Soul ID reference by name.
- **Cheapest test:** free first: `show_marketing_studio_v2` / `show_characters` to see what the avatar path exposes. Then one Marketing Studio UGC with the uploaded avatar vs Soul ID (`get_cost` first).

### C-18 Audio-first gate: approve the voice track before any video · NEW (order of operations for #15)
- **How:** In Arcads, write the script, **annotate lines with emotions** ("type a slash and choose from different emotions"), set the voice's "style, exaggeration, and speaking speed", then "click generate so we can review the audio first and make sure everything sounds good. **The video is built on top of the audio.** So, this step is important" (`o-xhRksFBAc @01:35–02:07`). B-roll keyframes are made 3 at a time in Nano Banana Pro ("images don't always come out perfect"), one is picked, then animated with Veo 3.1 as a start frame (`@02:38–03:10`). The product-in-hand keyframe used both the model and product references with a small, specific action ("squeezing a pea-sized amount of the cream onto her fingertips", `@04:12`).
- **Fixes:** F8 F9
- **Evidence:** `o-xhRksFBAc`. Grade **B** (vendor workflow shown). The format itself (before/after skincare testimonial) is on our STOP list (#18).
- **Cutroom input change:** the pipeline blocks the video render until an audio track (human recording, or TTS with per-line emotion tags and speed set) is approved. The approved audio goes in as the `@Audio` reference, so a bad read is never discovered after paying for video.
- **Cheapest test:** 0–1 credit (TTS or a phone recording), then compare against the last native-audio rejects.

### C-19 Seedance 2.x reference capacity and length ceiling · EXTENDS #9 and contradiction #1
- **How:** Seedance 2.0 on Higgsfield takes "up to nine images, three video clips, and three audio clips in a single generation" (`tfs8U3CbAOs @01:33`). Seedance 2.5 on OpenArt has a **30 s cap per call**, so the workflow groups shots into 30 s blocks (`kC12eMs0SF0 @07:36`). A 180 s one-prompt film was possible, but "working with 30 seconds is much more precise" (`iWLTy0B5_NE @08:29`). ≥3 characters in one prompt "might get a bit glitchy" (`lkL8mlpVScY @13:33–14:04`).
- **Fixes:** F1 F7 F9
- **Evidence:** as cited. Grade **B/C**.
- **Cutroom input change:** the reference budget per model is stored in the router (Seedance 2.0: 9 images / 3 video / 3 audio; the playbook still says don't fill every slot). Max 1–2 people per generation. Stay at ≤15 s for UGC even where 30 s is allowed.
- **Cheapest test:** 0.

### C-20 Text renders only when spelled out in the prompt, and only if short · EXTENDS STOP #12 (partial nuance)
- **How:** The new Seedance "works very well with text added in the video… but only with what is clearly specified in the prompt. Outside of that, distortion is still very much present" (`iWLTy0B5_NE @09:16`). Kling 3.0: "simple text seems to work okay, but complex text with multiple lines, symbols… It's a mess" (`k6jn5xjqYSo @17:44–18:15`). A menu from a GPT Image 2 reference came out unreadable and "even in reverse" in Seedance (`lkL8mlpVScY @10:24`). A drink label "stays perfect throughout" a Kling 3.0 multi-shot VO ad (`z84WQAn6U0I @10:36`).
- **Fixes:** F2
- **Evidence:** four creators, consistent. Grade **B**.
- **Cutroom input change:** if a short wordmark must appear, quote the exact string in the prompt (`chest print reads exactly "SANTO"`). All other text (care labels, size tags, poster text) is blurred or kept off-frame. A logo patch in post remains the guarantee.
- **Cheapest test:** fold into playbook T8: one render with the exact wordmark quoted vs not quoted.

### C-21 Run the reference eligibility check before spending · NEW (minor)
- **How:** "before you upload reference images, Higgsfield has a built-in eligibility checker. I would always recommend running images through it first… Copyright characters and celebrity photos will get rejected" (`tfs8U3CbAOs @11:54`).
- **Fixes:** F9
- **Evidence:** `tfs8U3CbAOs`. Grade **C**.
- **Cutroom input change:** pre-flight every new persona or reference image through the checker (or `media_confirm`) at intake, not at render time. This matters if personas come from real people (C-09).
- **Cheapest test:** 0.

---

## 3. Contradictions with the playbook

1. **Where the "style" block goes.** kC12 appends the "style DNA… at the bottom of every prompt" (`kC12eMs0SF0 @07:36`). The playbook (#4, #13) puts the realism block **at the start** because Seedance follows the first 2–3 instructions and drops things after ~8. With the 2,500-character cap (C-03), a block at the bottom is also the first thing truncated. **Keep it at the start**, but a cheap A/B would settle it.
2. **Duration padding vs "fit the duration".** C-07's +2 s pad against playbook #14 ("don't give a 3 s action 8 s of runtime"). They can be reconciled: the pad is spread across the whole clip and trimmed at the end, and it is not added to any single action. Still a claim with no A/B shown. Test it.
3. **Upscaling and resolution.** `lkL8mlpVScY @03:40` ("720p… You can upscale it later") and `tfs8U3CbAOs @04:20` (Higgsfield video upscale to 4K) vs the playbook (no generative upscaling; 720p ≈ 1080p for UGC). `kC12eMs0SF0 @08:39` renders at 1080p. These are film and cinematic creators; for phone UGC the playbook stands.
4. **Music.** kC12 adds "your own background music" in the edit (`@09:41`), and Digital Assets includes music in the audio layer (`goZDcGw-WsU @03:21`). This contradicts "no music by default" (#6). It is film context, not UGC; the playbook stands.
5. **"Shallow depth of field" praised as realism** (`k6jn5xjqYSo @15:31–16:02`). This is cinematic taste and directly against the playbook's banned list (bokeh / shallow DoF). The playbook stands.
6. **LLM re-describes the approved still for the video prompt.** Arcads workflow: paste the picked image into ChatGPT and ask for a video prompt "to bring the image to life" (`o-xhRksFBAc @02:38–03:10`). Playbook STOP #11 says don't re-describe what the keyframe already shows; describe motion only. Keep the playbook rule, and tell the LLM "describe motion and sound only".
7. **Sheet vs real photos** (nuance, not a flat contradiction). `lkL8mlpVScY @22:59` says sheet-only personas look "more AI" than real-selfie ones. The playbook (#11) makes the headless sheet central. Reconciled by C-09: build the sheet *from* real close photos, and give the model the real photo alongside the sheet.
8. **One call with many cuts vs single shot.** `tfs8U3CbAOs @07:02` ("when it's like one shot… less chance of errors") and the 10-shot overload in `lkL8mlpVScY` add weight to the playbook's existing contradiction #1 (one 15 s board call vs short clips). Seven or more cuts per 15 s over-compresses; the playbook's 4–8 panel cadence is at the upper limit.
9. **Text rendering** (C-20). This softens STOP #12 only for a short wordmark quoted exactly in the prompt; it does not replace the logo patch.

---

## 4. Top 5 most valuable findings

1. **C-01 + C-02 + C-03: cost and limits.** Seedance Fast is half the credits at the same 720p (`tfs8U3CbAOs @03:48`); standard is 66 credits per 11 s, about 6/s (`@05:58`); 480p proof renders for untested prompts (`lkL8mlpVScY @03:40`). A **2,500-character** Seedance prompt cap and a **500-character** per-shot Kling cap both **truncate silently**, which may be quietly cutting our garment-lock and negative blocks (F2, F9).
2. **C-06 + C-07: reference order = reference key; wrong order swaps roles or turns the room into a character.** Pad the render +2 s so the last action isn't cut off, then trim (`kC12eMs0SF0 @08:07–09:41`) (F1, F7, F9).
3. **C-09 + C-10: real close photos, including a side or back view, beat sheet-only personas; distant references make the model invent skin and moles.** The clip that fooled a friend was a real screenshot + voice clone + a 7 s single take with a personal tic ("looks off frame slightly, which is a thing I often do") and a written pause (`lkL8mlpVScY @20:55–23:29`) (F1, F6, F8).
4. **C-05 + C-04: Kling dialogue drifts in the last ~5 s of 15 s**, so front-load SPEAK beats and end on silent DO beats (`z84WQAn6U0I @03:06, @09:33`). Kling multi-shot is ≤6 shots, ≥3 s each, one action and one camera move per shot (F8, F9).
5. **C-11: one-take "logic rule".** Seedance "loves" inventing extra camera angles unless told *why* there is one camera ("one continuous shot because I'm holding the camera", `lkL8mlpVScY @18:52`). A single shot also has "less chance of errors" (`tfs8U3CbAOs @07:02`) (F6, F7). Close runner-up: **C-17**, the stable Higgsfield MCP path is an uploaded Marketing Studio avatar rather than a Soul character by name (`wc4VOgT7S58 @01:33`).

---

## STOP DOING (new from this batch)
- Sending prompts over 2,500 characters to Seedance, or over 500 characters per Kling multi-shot shot. The tail is silently dropped (C-03).
- Letting an LLM expand the shot spec unchecked. It adds actions and lines that crowd a 15 s clip (C-12).
- Uploading references in an order that doesn't match the prompt's reference key (C-06).
- Placing Kling dialogue in the final ~5 s of a 15 s clip (C-05).
- Using distant or front-only photos as identity references (C-09).
- Test renders at standard quality or 1080p for prompts not yet proven. Use Fast at 480p or 720p (C-01, C-02).
- More than 2–3 people per generation (C-19).

## Open questions
- Does the Higgsfield Kling multi-shot UI allow shots under 3 s (Jack shows 2 s) while other hosts enforce 3 s? Check via `models_explore`.
- Is the 2,500-character cap the same for Seedance 2.5 on Higgsfield and for the MCP `generate_video` path, and does the MCP warn on truncation?
- Credit cost of Higgsfield image "multi-shot" (3×3 grid) and of Element creation.
- Does the +2 s pad improve completion of end actions, or just add slow motion? It needs a paired test.
- Is the Marketing Studio avatar path really more stable than Soul ID via the MCP, or was that a one-off failure?

---

# PART 14 — `tools/README.md`

## Cutroom research tools

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

---

# PART 15 — `ROUND3-LOCAL-BRIEF.md`

## Round 3: research only your Mac can do

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
