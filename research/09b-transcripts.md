# 09b: Techniques mined from YouTube transcripts (batch b, 9 videos)

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
