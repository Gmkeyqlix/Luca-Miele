# 04 — Competitor AI-UGC tools, fashion try-on, and real UGC craft

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
