# 08 — Podcasts & YouTube: what practitioners say they actually do

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
