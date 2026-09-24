# 05 — GitHub open source + research: skills, tools, auto-QA, AI-detection signals

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
