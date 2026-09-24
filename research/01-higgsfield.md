# 01 — Higgsfield ecosystem: internal recipes, model facts, community repos

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
