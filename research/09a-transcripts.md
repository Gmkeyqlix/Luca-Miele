# 09a: YouTube transcript mining (batch A, 9 videos)

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
