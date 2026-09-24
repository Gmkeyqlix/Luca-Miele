# 09c: YouTube transcript mining (batch C, 9 videos)

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
