# 06 — Winning apparel ads, courses/communities, prompt→output structures

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
