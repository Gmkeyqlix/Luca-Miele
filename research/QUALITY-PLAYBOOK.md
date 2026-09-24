# Cutroom Quality Playbook: what the best people do, and what we change

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
