# 03 — What working AI filmmakers and ad-makers do (source: pros' interviews, BTS, published pipelines)

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
