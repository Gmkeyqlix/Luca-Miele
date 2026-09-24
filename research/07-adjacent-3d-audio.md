# 07: What adjacent industries do: virtual influencers, 3D/digital twins, performance capture, audio, e-com capture

Researcher scope: agencies and fields that already dealt with our failures: virtual-influencer studios, AI fashion-model vendors, CGI/FOOH studios, mocap and motion-transfer tools, voice/lip-sync/sound, and e-commerce product photography.
Method: about 55 WebSearch queries (WebFetch blocked) plus one raw GitHub read of an ElevenLabs v3 tag reference. Strength grades follow BRIEF (A = vendor docs or several independent pros; B = one credible practitioner with results; C = claim).

---

## The big finding (read this first)

**The virtual-human studios that look most real never generated the clothes. They put a synthetic head on a real body that wore the real garment in a real place.**
- **Imma** (Aww Inc / ModelingCafe): "each image rendered by transposing her 3D head onto a live-action body and background" ([mymodernmet](https://mymodernmet.com/imma-cgi-virtual-model/), [interestingengineering](https://interestingengineering.com/culture/meet-imma-the-worlds-first-computer-generated-model)).
- **Shudu** (Cameron-James Wilson / The Diigitals) uses a roster of real stand-in "muses". In his words, designers lack 3D garments, "so to dress the model effectively you need to shoot on a real model and then merge the images together" ([Shudu wiki](https://en.wikipedia.org/wiki/Shudu_Gram), [stylist](https://www.stylist.co.uk/beauty/fenty-cameron-james-wilson-3d-digital-supermodel/193080)).
- **Lil Miquela** (Brud): critics noted "her clothes have a reality, an unmistakable drape and weight and texture… in contrast to her CGI skin". The images are composites ([Forbes](https://www.forbes.com/sites/mattklein/2020/11/17/the-problematic-fakery-of-lil-miquela-explained-an-exploration-of-virtual-influencers-and-realness/), [cut-the-saas](https://cut-the-saas.com/ai/the-ai-behind-virtual-influencer-lil-miquela)).
- **Mango**'s all-AI Teen campaign "began with shooting real photos of each garment" ([Mango Fashion Group](https://mangofashiongroup.com/en/w/mango-crea-la-primera-campa%C3%B1a-generada-con-inteligencia-artificial-para-su-l%C3%ADnea-teen)). **Zara** takes real shoots of real models and uses AI to *re-dress* them ([technology.org](https://www.technology.org/2025/12/19/zara-deploys-ai-technology-to-virtually-dress-real-models-in-new-campaigns/)).

In 2026 this "real body, synthetic identity" pipeline can be run with video tools: Wan 2.2 Animate *Replace* mode, Higgsfield Genjutsu (Object Swap / Motion Transfer, launched 1 Sep 2026), Runway Aleph 2.0, and Kling 3.0 Motion Control. It is the single input change most likely to fix F2/F3/F4/F5/F7 together. The cost moves into a cheap phone capture instead of rerolls. The rest of this file adds the capture specs, audio chain and reference-photo rules that make it work.

---

## A. Virtual influencer and AI fashion-model practice

### 1. Real body plate + identity swap ("Imma method")
- **How**: A body double (friend, staff, paid local creator, about £20–50 an hour) wears the actual SANTO garment. They film the whole 15 s beat handheld on a phone in a real room: tear the mailer, pull on the hoodie, zip, squat in leggings. Then only the identity is replaced:
  - Wan Animate **Replace** mode keeps the original camera, background and body. A SAM2 mask covers the character, and you can shrink it toward head and hair ("mask expansion" is configurable). A **Relighting LoRA** (trained on IC-Light composites) matches skin tone and light to the plate ([Wan-Animate paper](https://arxiv.org/pdf/2509.14055), [HF model card](https://huggingface.co/Wan-AI/Wan2.2-Animate-14B), [comfy.org workflow](https://comfy.org/workflows/use-cases/ai-character-replacement/)).
  - Higgsfield Genjutsu **Object Swap** changes "a selected character, outfit, product… while preserving the rest of the shot". It takes 3–30 s reference video and up to about 30–40 reference images ([higgsfield blog](https://higgsfield.ai/blog/higgsfield-genjutsu), [rekreate](https://rekreate.ai/news/higgsfield-genjutsu)). The MCP routes it via `generate_video` → `hf_mult_replace_object` / `hf_mult_motion_control`. Other researchers cover Higgsfield specifics.
  - Runway Aleph 2.0 edits real footage "changing only that" element, clips up to 30 s at 1080p ([runway](https://runway.com/product/aleph-2)).
- **Why it works**: fabric physics, fit, hand-product contact, the bag tear and the room are all *recorded*, not generated. Only the face, which the persona pipeline already controls, is synthetic.
- **Fixes**: F2, F3, F4, F5, F7, plus F6 (real handheld motion and real light). F1 is handled by the identity reference.
- **Evidence**: A for the principle (Imma, Shudu, Miquela, Zara all use it). B for doing it with 2026 video models (Wan paper and vendor docs; independent UGC results not seen).
- **Gotchas**: Wan skips pose retargeting in Replace mode, so a body double with a very different build from the persona causes deformation (paper). Swap engines "read held objects as part of the body geometry" ([higgsfield face-swap guide](https://higgsfield.ai/blog/AI-Face-Character-Swap-in-Video-Photo-PRO-Guide)). That is good here because the object held is the *real* product. Aleph edits drift "when the target becomes occluded, changes scale, or moves quickly" ([techpoint review](https://techpoint.africa/guide/runway-ai-aleph-review/)).
- **Input change for Cutroom**: a new shot type, "Plate + Swap". It stores `plate_video` (phone, continuous, 3–30 s), `body_double_id` (with height/build) and `swap_scope` = head | head+hair | full-character. The swap uses the persona reference pack. Plate spec: see #12.
- **Cheapest test**: 1 plate (film today, 0 credits) → 1 Wan-class replace run. Check the per-second cost via `models_explore` (free). Compare against the current best full-gen of the same beat (about 18 credits on Seedance).

### 2. Persona "digital twin" capture protocol (H&M / Uncut; The Clueless)
- **How H&M/Uncut do it**: they shot the 30 real models "from different angles, with different lighting, in a variety of poses and in motion". A twin is considered accurate "only once all the person's special features, including birthmarks and typical movement patterns, have been captured" ([sourcingjournal](https://sourcingjournal.com/topics/technology/h-and-m-artificial-intelligence-models-digital-twin-1234741894/), [retail-optimiser](https://retail-optimiser.de/en/hm-plans-to-advertise-with-digital-twins-of-models/), [apparelresources](https://apparelresources.com/business-news/manufacturing/hm-unveils-first-ai-generated-digital-model-twins-ads-social-media/)). The Clueless (Aitana López) uses character LoRAs, batch generation, then **manual Photoshop passes for face consistency**, with a "character bible" (backstory, pet, zodiac) ([cut-the-saas](https://cut-the-saas.com/ai/aitana-lopez-blending-ai-and-style-in-the-age-of-virtual-influencers), [netinfluencer](https://www.netinfluencer.com/the-clueless/)).
- **For Cutroom**: the persona pack should hold more than 1–3 face shots:
  - (a) 3 head angles (front, 3/4, profile) × 2 lights (window daylight, warm lamp)
  - (b) a neutral, a talking and a laughing expression
  - (c) full-body front and side, for build (needed for #1 body-double matching)
  - (d) 1 motion clip (a 5 s walk or turn)
  - (e) **2–3 deliberate identity markers** (mole position, eyebrow scar, chipped nail polish colour, specific earring). These make drift *detectable* by a reviewer or VLM check. H&M's twins count birthmarks as part of identity.
  - Kling 3.0 Motion Control now takes **multiple character reference images plus "Element Binding"** for the face. 2.6 took one ([atlascloud](https://www.atlascloud.ai/blog/guides/kling-ai-motion-control), [ai-creators.tech](https://en.ai-creators.tech/media/creative/kling3-motion/)).
- **Fixes**: F1, F7 (markers stop random jewellery appearing: "earring = small silver hoop, left ear only").
- **Evidence**: A (H&M/Uncut reporting from several outlets; Kling docs).
- **Input change**: schema `persona.reference_pack` with required slots and `persona.markers[]`. The auto-QC compares every generated keyframe's markers.
- **Cheapest test**: build the pack with Soul ID / Nano Banana, about 10 images × 1.5 = **~15 credits** once per persona.

### 3. Persona clearance: accidental real-person likeness
- **What went wrong**: Shein's (vendor-supplied) AI model image scored a **99.9% facial-recognition match to Luigi Mangione**. The listing was pulled and a public investigation followed ([CNN](https://www.cnn.com/2025/09/03/business/shein-shirt-luigi-mangione), [Vice](https://www.vice.com/en/article/shein-is-using-an-ai-luigi-mangione-as-a-t-shirt-model/)). Separately, models sued a brand in 2026 over AI doppelgängers ([PetaPixel](https://petapixel.com/2026/06/24/models-claim-fashion-brand-used-ai-to-create-their-doppelgangers/), [OECD.AI](https://oecd.ai/en/incidents/2026-05-30-7108)).
- **How**: before a persona goes live, run its hero face through a reverse face search (PimEyes, FaceCheck-type) and a celebrity-lookalike check. Log the result. If a body double's face could leak into frames, get a signed likeness release. H&M and Zara pay models "identical to classical image use" ([Zara, cityam](https://www.cityam.com/zara-turns-to-ai-edited-models-amid-shop-closures/)).
- **Fixes**: legal/brand risk (no F-code). It is also why a persona should never be "inspired by" a real creator.
- **Evidence**: A (widely reported incident).
- **Input change**: `persona.clearance {date, tool, result}` must be present before the persona can be used in export. `body_double.release_signed` is a boolean.
- **Cheapest test**: 0 credits.

### 4. Garment-truth rule for fit categories (the Mango and Levi's lesson)
- **What went wrong**: the Mango Teen AI campaign was called "#falseadvertising". The shopper quote was "When I order clothes… I look at the pictures to see how the actual clothes fit. AI pics are completely useless for that" ([Yahoo](https://www.yahoo.com/tech/mango-ai-models-slammed-false-192812823.html)). Levi's/Lalaland was attacked on framing (it was pitched as "diversity"). Its e-com use case was sound ([CampaignsLive](https://campaignslive.com/blog/levis-lalaland-controversy/)). A PowerReviews survey says 28% of apparel returns come from appearance mismatch ([metamodels](https://metamodels.ai/feeds/blog/ai-model-photography-what-fashion-brands-get-wrong)).
- **How**: for **leggings, jeans and fleece fit beats** (the F5 shots), use #1 (real body plate). Keep full generation for shots where fit is not the claim (a hook face, a reaction, a mailer on the doorstep).
- **Fixes**: F5, F2, plus trust and returns.
- **Evidence**: A (public backlash, several outlets).
- **Input change**: each product gets a `fit_critical: true/false` flag. When true, the storyboard gate needs a plate for any shot showing the garment on the body in motion.
- **Cheapest test**: 0 credits (a policy).

### 5. Brute force doesn't buy consistency (Coca-Cola 2025)
- **What went wrong**: Secret Level made Coke's 2025 holiday ad from **70,000+ generated clips** by 100+ people in 30 days across Sora, Veo 3 and Luma. It was still panned as "inconsistent… switching between realism and cartoonish", with "mismatched styles across the clips" ([vp-land](https://www.vp-land.com/p/coca-cola-s-ai-holiday-ad-how-70-000-generated-clips-built-a-familiar-yet-new-commercial), [contentgrip](https://www.contentgrip.com/coca-cola-ai-holiday-ad-backlash/)). Seraphinne Vallora's Guess/Vogue models took "hundreds of iterations… to perfect texture, movement and details of the advertised product" ([CNN](https://www.cnn.com/2025/07/31/style/vogue-ai-models-guess-campaign)).
- **Takeaway for Cutroom**: rerolls are the budget sink (F9). Mixing generator models *inside one 15 s ad* creates visible style seams (F6). Lock one video model per ad for all persona-on-camera shots. Buy consistency with captured inputs (plates, packs), not more rolls.
- **Evidence**: A.
- **Input change**: `ad.primary_video_model` is locked at storyboard. Any shot overriding it must justify it (e.g. an insert with no persona in it).

---

## B. Digital twins / 3D for product fidelity

### 6. Planar-track the real logo or print back on (VFX logo replacement)
- **How**: this is standard VFX logo replacement ([Boris FX Mocha](https://borisfx.com/blog/learn-how-to-do-planar-tracking-with-mocha-pro/), [curved surfaces](https://blog.pond5.com/20827-how-to-track-and-replace-logos-on-curved-surfaces-with-mocha-pro/)):
  1. Store the true artwork (vector/PNG) of every SANTO print, logo, woven label and mailer-bag graphic.
  2. After generation, draw a spline around the drifted logo region and planar-track it forward and backward. The track captures position, scale, rotation, shear and perspective.
  3. Corner-pin the true artwork, multiply or overlay onto the fabric, add a small blur to match focus, and add grain.
  4. Use a manual Surface track when auto fails.
  - It works best on **mostly planar areas**: hoodie chest print, flat mailer bag, tee front, leggings waistband logo. It fails on heavy folds or quick turns. For folds, a mesh warp (Mocha Pro) is needed.
- **Fixes**: F2 (logo/print/text drift). This is the only method in this report that *guarantees* pixel-true logos.
- **Evidence**: A as a VFX technique. C as an applied fix for AI UGC (no case study found).
- **Input change**: `product.artwork[]` holds vector/PNG plus real-world size and placement. Add a post stage, "logo patch", triggered when the logo is at least about 5% of frame area and visible for more than 0.5 s. Headless automation is possible: OpenCV/CoTracker point tracks → homography → composite. Worth a spike.
- **Cheapest test**: 0 credits. Take one existing drifted clip, patch it in AE/Mocha or DaVinci Fusion's planar tracker, and judge the result.

### 7. Scan the rigid products (mailer bag, folded stack, tags) as Gaussian splats; render exact-angle stills as start frames
- **How**: capture the sealed SANTO mailer, a folded hoodie stack, and the hang-tag or woven label with Polycam, KIRI or Luma. Shoot 4K video, walk slowly, cover many angles and heights, 1–3 min ([polyvia3d capture guide](https://www.polyvia3d.com/guides/gaussian-splatting-mobile-capture), [swyvl](https://swyvl.io/blog/how-to-create-gaussian-splats/)). Render the exact camera angle the storyboard needs (e.g. mailer on a bed from a 35° high angle) and use it as the Nano Banana composite source or the start frame. Practitioners describe this "3D-as-reference for 2D pipelines": the start frame is "grounded in real geometry" ([wavespeed TripoSplat](https://wavespeed.ai/blog/posts/triposplat-image-to-3d/)).
- **Limits**: good only for rigid or nearly rigid items. Worn garments deform, so use #1 for those. Splat texture is only as sharp as the capture frames, so fine text softens; pair with #6. Cross-polarised light (#20) during capture avoids baked glare on the glossy mailer.
- **Higgsfield note (not called)**: `generate_3d` (image → GLB) and `scene_builder_3d_*` exist. Generic image-to-3D models bake lighting into albedo and have uneven texel density ([rundiffusion/cinevva comparisons](https://app.cinevva.com/guides/ai-3d-model-generators)). Do **not** expect logo fidelity from an image-to-3D mesh. Use it only for blocking and camera angles (#8).
- **Fixes**: F2 (exact angles without re-shooting), F9 (no rerolls to "find" an angle).
- **Evidence**: B/C (workflow described by tool vendors; no ad case study with metrics).
- **Input change**: `product.scan_url` (splat/GLB) for rigid SKUs and packaging. The shot planner can request a render at a named angle.
- **Cheapest test**: 0 credits. Scan the mailer in KIRI or Polycam (free tier) and compare 3 rendered angles with real photos.

### 8. 3D blockout → depth/pose control video for environment and camera lock
- **How**: block the room and camera move in Blender (or Higgsfield's 3D scene builder / Blender plugin, which exports MP4, a still or GLB: [higgsfield 3D Jutsu](https://higgsfield.ai/blog/higgsfield-3d-jutsu), [blender plugin](https://higgsfield.ai/plugins/blender)). Export depth, OpenPose and canny passes. Drive a video model with them (Wan VACE-class). Depth locks scene structure, OpenPose locks pose, canny locks silhouettes ([runcomfy Blender→ComfyUI](https://www.runcomfy.com/comfyui-workflows/blender-to-comfyui-ai-renderer-2-0-workflow-cinematic-video-output), [flick](https://flick.art/blog/blender-ai-filmmaking), [ComfyUI depth docs](https://docs.comfy.org/tutorials/controlnet/depth-controlnet)).
- **Verdict for Cutroom**: this is overkill for handheld UGC. A **real phone plate of the real room** gives the same lock for free, with a real camera shake. Keep it only for impossible shots (a product "hero orbit").
- **Fixes**: F7.
- **Evidence**: B (open workflows).
- **Cheapest test**: skip unless a hero-orbit shot is needed.

### 9. 3D garment tools (CLO3D / Browzwear / Style3D / Marvelous): evaluated and deprioritised
- These need pattern files (DXF) and a fabric-property setup per SKU. CLO's AI Studio composites a portrait or AI face onto a rendered garment ([CLO support](https://support.clo3d.com/hc/en-us/articles/33832336587545-AI-Render)). Marvelous Designer simulates fabric weight, stretch and stiffness per material ([toolworthy](https://www.toolworthy.ai/tool/marvelous-designer)). Shudu's creator says most brands lack 3D garments, so he shoots on a real model instead. **For a small streetwear brand, a body double (#1) beats a 3D garment twin on cost and realism.** Revisit only if SANTO's manufacturer already supplies CLO files.
- **Fixes**: would address F5 in theory. **Evidence**: B. **Cost**: licence plus hours per SKU.

### 10. FOOH / CGI-ad finishing checklist (what makes an inserted element "sit")
- **How pros finish** ([maverickframe](https://maverickframe.com/blog/what-is-fooh/), [dialect](https://www.dialectinc.com/thoughts/fake-out-of-home)): real plate first → camera track → match lighting direction and colour → **contact shadows** → reflections → grade → **matched grain** as the last step.
- Apply this to every Nano Banana composite and every Plate + Swap: check contact shadow under the product on the bed, light direction consistent with the window in the plate, then add grain after grading, not before.
- **Fixes**: F6, F7. **Evidence**: A (industry-standard VFX order).
- **Input change**: a QC checklist item "contact shadow present / light direction matches plate". The post chain orders `grade → grain → codec`.

---

## C. Performance capture from a phone

### 11. Tool routing for "real performance → AI character"
| Need | Best fit | Why / limits |
|---|---|---|
| Keep the real room, camera and product; swap who is on screen | **Wan Animate Replace** / **Genjutsu Object Swap** | Keeps the original camera and background; relighting LoRA; deformation if body shapes differ ([wanvideogenerator comparison](https://wanvideogenerator.com/blog/ai-motion-control-kling26-vs-wan22-animate), [fylia](https://fylia.ai/blog/detail/Motion-Transfer-Showdown-Kling-vs-Wan-Which-One-Nails-Your-Character-Animation-1403c7f44bf5/)) |
| Persona in a *new* generated scene copying a filmed move | **Kling 3.0 Motion Control** / Genjutsu Motion Transfer | Element Binding for face; "Match video" vs "Match image" orientation modes; ref 3–30 s ([Kling guide](https://kling.ai/quickstart/motion-control-user-guide)) |
| Change one element (colourway, outfit) in real footage | **Runway Aleph 2.0** | Up to 30 s at 1080p; drifts on occlusion or fast motion |
| Face acting and dialogue on a still persona | **Runway Act-Two** | Gesture control only with image input; face centred, shoulders up ([Runway help](https://help.runwayml.com/hc/en-us/articles/42311337895827-Performance-Capture-with-Act-Two)) |
| Talking head only | **Hedra Character-3** | Stiff full body, over-dramatic hands, "over-smiling, head tilting" ([magichour](https://magichour.ai/blog/guide-to-hedra-ai), [morphed](https://morphed.app/blog/hedra-alternatives)) |
| Not for realism | Viggle | Simple moves only; edge artifacts when clothing blends with background ([flowith](https://flowith.io/blog/viggle-ai-faq-motion-transfer-custom-characters-commercial-rights/)) |
- Kling's own report claims a large win rate over Act-Two ([Kling-MotionControl tech report](https://arxiv.org/html/2603.03160v1)). That is a vendor claim. **Fixes**: F9 (right tool first time), F1, F3. **Evidence**: A (vendor docs) / B (comparisons).

### 12. Phone plate / driving-video capture spec (consolidated from vendor docs)
Store this as the **Plate Spec** the app shows before upload, and auto-check what it can:
1. **One continuous shot, no cuts**, 3–30 s (Kling, Act-Two, Genjutsu all require this). Aim for 5–10 s per beat.
2. **Subject fully in frame the whole time.** For Kling, avoid camera movement in the motion reference ([Kling guide](https://kling.ai/quickstart/motion-control-user-guide)). For Wan Replace, handheld is fine because it keeps the camera.
3. **Hands visible, never in pockets or behind the back**, if the output needs hands ([atlascloud](https://www.atlascloud.ai/blog/guides/kling-ai-motion-control)). **Avoid hands crossing in front of the torso or limbs overlapping**, which Kling users call "spaghetti limbs" ([invideo](https://invideo.io/blog/kling-motion-control/)).
4. **Half-body is more stable than full-body.** Hands close to the lens fail in Wan (fingers blur and merge). Keep hand-product action at mid-distance ([wan-animate guide](https://wan-animate.com/posts/wan-2-2-animate-motion-types-style-consistency-guide)).
5. **Clothing contrasts with the background.** Fitted beats baggy for motion extraction ([Move AI via cgchannel](https://www.cgchannel.com/2023/11/move-ai-releases-move-one/), [Viggle](https://www.seedance.tv/blog/viggle-ai-motion-control-settings)). Note: SANTO hoodies are loose, so for *motion-transfer* references have the performer wear something fitted. For *Plate + Swap*, wear the real SANTO garment because the garment stays in the output.
6. **Even front or window light; no backlight; no harsh shadows** (Move One, Kling, Act-Two).
7. **Face**: for dialogue or Act-Two, face centred, shoulders up, looking at the lens, never leaving frame.
8. **Aspect ratio of the character image = aspect ratio of the reference video**. Character image framing matches the reference: full body if the motion is full body (Kling).
9. **Props**: "if your character holds objects, your performance should mirror that" (Runway). Hold the *real product* or a same-size stand-in.
10. **Body double build ≈ persona build** (Wan: no retargeting in Replace mode).
- **Fixes**: F1, F3, F4, F9. **Evidence**: A (vendor docs from several companies).
- **Input change**: plate upload form with checkboxes and auto-checks (duration, cut detection via scene-change, aspect-ratio match, face-in-frame ratio via face detection).
- **Cheapest test**: 0 credits. Re-shoot one existing motion-library clip to spec and compare the next Kling/Wan run against the old one.

### 13. Act the object, not the gesture
- **How**: for F3/F4 beats (ripping the mailer, pulling the hoodie over the head, zipping), the plate performer does the *real action with the real object*. Do not mime it and hope the model invents the object. Swap engines treat the held object as body geometry, which works for us when it's the real SANTO bag. When using prompts with Wan, name the interaction explicitly ("person tearing open a grey polyethylene mailer bag with both hands"). Wan docs say explicit object prompts beat inference from pose ([wan-animate guide](https://wan-animate.com/posts/wan-2-2-animate-motion-types-style-consistency-guide)).
- **Fixes**: F3, F4. **Evidence**: B.
- **Input change**: movement-library entries record `props_held[]`. The shot is refused if the storyboard prop ≠ library prop.

---

## D. Audio / voice realism (F8)

### 14. Perform first, convert second: human VO → speech-to-speech
- **How**: someone (Luca, the body double, any friend) records the script on an iPhone, conversationally, in a soft-furnished room. Settings: Voice Memos set to **Lossless** (Settings → Voice Memos → Audio Quality), phone **14–18 in (35–45 cm)** from the mouth, bottom mic toward the mouth, bedroom or wardrobe full of clothes ([Flare](https://joinflare.app/blog/ugc-audio-quality-no-pro-mic)). If the persona needs a different voice, run it through **Voice Changer / speech-to-speech**. It "preserves the original performance: emotions, timing, pacing and pronunciation" (max 5 min) ([ElevenLabs STS docs](https://elevenlabs.io/docs/api-reference/speech-to-speech/convert), [blog](https://elevenlabs.io/blog/speech-to-speech)). Higgsfield also has a `voice_change` tool (not called). Real breaths, "um"s, restarts and laughs come through intact, and those are the cues TTS fakes worst.
- **Fixes**: F8. **Evidence**: A (vendor docs); pros use STS to "infuse the performance" TTS cannot.
- **Input change**: `shot.vo_source` = human_recording | sts(persona_voice) | tts. Default to human_recording or STS for talking UGC. Store the raw take for lip-sync.
- **Cheapest test**: 0 credits for recording. STS on ElevenLabs costs about 1 min of credits on the free or starter tier.

### 15. Audio-first video: drive the video from the final VO
- **How**:
  - **Seedance 2.x** accepts up to **3 audio refs (@audio1–3), total ≤15 s, ≤50 MB each; MP3 is most reliable; trim refs to 3–8 s**. It uses them for rhythm, timing and lip-sync alignment ([cutout.pro](https://www.cutout.pro/learn/blog-seedance-2-0-audio-guide/), [seedance2pro](https://seedance2pro.io/blog/does-seedance-2-accept-voice-reference), [mindstudio](https://www.mindstudio.ai/blog/seed-audio-reference-seedance-video-generation-workflow)). Clean WAV behaved more predictably than messy phone-memo MP3s. **Long uneven silences can cause frozen frames**, so trim dead air to ≤0.4 s before upload ([ugccopilot](https://ugccopilot.ai/blog/seedance-2-native-audio-generation-guide/)).
  - **Length walls**: Seedance lip-sync is tight at the start of a 15 s clip but drifts by the end ([crepal](https://crepal.ai/blog/aivideo/blog-seedance-2-0-lip-sync-voiceover-fix/)). Kling 3.0 has a "**second-8 wall**" where lips and audio separate after about 8 s ([Maxfusion](https://maxfusion.ai/blog/ai-video-models-lip-sync-2026)). **Rule**: talking segments ≤8 s per generation. Word budget ≤12 words per 5 s, ≤20 words per 10 s ([atlascloud](https://www.atlascloud.ai/blog/tips/kling-ai-lip-sync)).
  - Generate **one continuous VO for the whole ad**, then slice it per shot. This avoids voice drift between shots, which Seedance docs flag as "jumps in pitch, speed… room sound… obvious at the cut" ([seedance.tv](https://www.seedance.tv/blog/how-to-keep-voices-consistent-in-seedance-2-5)).
- **Fixes**: F8, F9 (no rerolls for sync). **Evidence**: B (several practitioner guides agree).
- **Input change**: the storyboard stores `vo_master.wav` and per-shot `vo_slice` (start/end). The shot generator attaches the slice as the audio ref. It auto-splits any talking shot longer than 8 s.
- **Cheapest test**: one 6 s talking shot on Seedance with an audio ref (~18 credits) vs the same shot with native audio.

### 16. The lip-sync fix layer: settings that matter
- **Sync lipsync-2-pro** ([sync.so docs](https://sync.so/docs/compatibility-and-tips/improving-lip-sync-quality), [models](https://sync.so/docs/models/lipsync)):
  - `temperature` 0–1, default 0.5. Use **0.3 for subtle, casual UGC**; high values look like over-enunciation.
  - Face should be **20–40% of the frame**; input ≥480p.
  - The model generates the mouth region at **512×512**, so extreme close-ups (face over 50% of a 1080p frame) can look softer than the surrounding pixels.
  - Set `occlusion_detection_enabled: true` when a hand, hoodie drawstring, hair or product crosses the mouth. It is slower.
  - Extreme profile fails. Use one visible speaker, or speaker selection.
  - Ranking by testers: Sync-3 > Sync-2-Pro for angles, occlusion and close-ups. Kling lip-sync is "general-purpose, not avatar-optimised". Hedra is cheapest but over-smiles and misses complex phonemes ([veed ranking](https://www.veed.io/learn/best-lipsync-api), [magichour](https://magichour.ai/blog/best-ai-lip-sync-tools)).
- **Workflow**: generate the visuals silent or with native audio. If lips miss, re-sync with the *human VO* (#14) instead of rerolling the video.
- **Fixes**: F8, F9. **Evidence**: A (vendor docs) + B (comparisons).
- **Input change**: `lipsync.params {model, temperature: 0.3, occlusion: auto}`. The storyboard warns when the planned face size is outside 20–40%.
- **Cheapest test**: re-sync one existing clip that has bad sync (sync.so pay-per-second, pennies).

### 17. Make clean audio sound like a phone recorded it (the "acoustic fingerprint" chain)
- **Why UGC voice sounds fake**: AI audio has no room reverb, no mic colouration and no AGC/codec artefacts. It "exists in a digital vacuum" ([UncannyAI guide](https://uncannyai.io/blog/how-to-fix-ai-video-audio)).
- **Chain, in this order**:
  1. **Convolution** with a real small-room impulse response (bedroom or office). Not an algorithmic reverb plugin.
  2. **EQ**: high-pass about 120–150 Hz, low-pass or roll-off about 7–8 kHz to kill the "studio condenser" sheen.
  3. **Phone-mic/AGC behaviour**: fast compressor/limiter that pumps slightly.
  4. **Room-tone bed** at about −45 to −50 dBFS, recorded in the same real room as the plate.
  5. **AAC encode** (the codec signature).
  6. Optional micro pitch/level jitter.
  - UncannyAI productises this, including iPhone MEMS mic response, AGC and AAC ([uncannyai.io](https://uncannyai.io/)).
- **Cheapest, most authentic alternative: "worldizing"** (Walter Murch, *American Graffiti*). Play the clean VO through a small speaker in the real room and re-record it with the phone at the camera position. You get the real room and real mic "for free" ([filmsound.org](http://www.filmsound.org/terminology/worldizing.htm), [designingsound](https://designingsound.org/2012/12/31/analog-worldization/)).
- **iPhone gotcha**: iPhone 16+ "Audio Mix → **Studio**" mode *removes* reverb and background ([MacRumors](https://www.macrumors.com/how-to/iphone-16-edit-spatial-audio-in-video-audio-mix/)). That is exactly the wrong direction for UGC. Keep plate and room-tone recordings on **Standard**.
- **Fixes**: F8, F6 (audio is half of the "AI look"). **Evidence**: B (the vendor explains the mechanism; worldizing is a documented film technique).
- **Input change**: `room.impulse_response.wav` and `room.tone.wav` per real room. Capture an IR with a balloon pop or hand clap on the phone, 0 cost. Post chain: `vo → convolve(room IR) → EQ → comp → +room tone → AAC`, one preset per room.
- **Cheapest test**: 0 credits (ffmpeg `afir` + `highpass`/`lowpass` + `acompressor`). Blind A/B with 3 people.

### 18. Voice clone recipe that sounds casual, not narrated
- **ElevenLabs facts** ([IVC docs](https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/instant-voice-cloning), [PVC docs](https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/professional-voice-cloning)):
  - Instant clone: **1–2 min** of clean audio. **More than 3 min gives little gain and can hurt.**
  - Pro clone: **30 min minimum, 2–3 h ideal**. WAV at 44.1/48 kHz, 24-bit, **−23 to −18 dB RMS, true peak −3 dB**.
  - The clone **copies the style of its training audio**, so "if you have… many 'uhm's… the AI will mimic those". **For UGC, record the clone sample as relaxed talking to a friend**, not read-aloud narration. That makes casual delivery the model's default.
- **Eleven v3 prompting** ([v3 tags](https://elevenlabs.io/blog/v3-audiotags), [best practices](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices), [tag reference](https://github.com/troykelly/hermes-voip/blob/main/docs/reference/elevenlabs-v3-audio-tags.md)):
  - Stability on **Natural** (or Creative for more emotion; Robust ignores tags).
  - Inputs **over about 250 characters** are more stable. A 15 s script is about 35–40 words ≈ 200–240 chars, right on the edge, so **generate the whole ad's VO in one call**, never line by line.
  - Use **1–2 tags max** from the safe set: `[laughs]`, `[sighs]`, `[clears throat]`, `[excited]`, `[whispers]`.
  - **Avoid `[pause]` and break tags**, which cause instability and speed-ups. Use "…" and em-dashes instead.
- **Fixes**: F8. **Evidence**: A (vendor docs).
- **Input change**: `persona.voice {provider, voice_id, clone_source: conversational, stability: natural}`. The TTS call always sends the full-ad script.
- **Cheapest test**: 0–1 credits (a free-tier ElevenLabs generation).

### 19. Native-audio prompting and the foley/music layer
- **Veo 3.x / Seedance native audio**:
  - Format dialogue as `Character says: …` (no quotes) and add **"(no subtitles)"**.
  - For phone intimacy: "**Ambient noise: close, dead room tone. No reverb.**"
  - Always state the background explicitly, otherwise models hallucinate things like a "live studio audience".
  - Keep ambience "low under the voice" and use **≤5 audio elements** ([Replicate Veo 3 guide](https://replicate.com/blog/using-and-prompting-veo-3), [Leonardo](https://leonardo.ai/news/how-to-prompt-audio-for-veo-3), [prompt-architects](https://prompt-architects.com/blog/150-prompting-audio-in-veo-3-1-sound-music-ambience)).
- **Foley sells state changes (F4)**:
  - Record the **real SANTO mailer tearing**, a zip, and a hoodie pulled over the head on the phone once, and reuse the files forever (0 cost).
  - If you must generate, the ElevenLabs SFX prompt should name material, size, distance and space. Use 10–60 words, 1–3 s duration, prompt influence default 30% ([ElevenLabs SFX docs](https://elevenlabs.io/docs/overview/capabilities/sound-effects)). Example: "thin grey polyethylene mailer bag torn open by hand, close phone mic, small carpeted bedroom".
- **Music / trending sounds**:
  - Trending consumer sounds are **not cleared for paid ads**, and boosting an organic post as a Spark Ad doesn't clear them.
  - Business accounts only see the **Commercial Music Library**. Original audio and voiceover are always safe ([Soundstripe](https://www.soundstripe.com/blogs/why-can-i-only-use-commercial-sounds-on-tiktok), [Third Chair](https://usethirdchair.com/blog/tiktok-commercial-library-what-brands-can-really-use)).
  - Fashion ads tend to work at **120–140 BPM**; rotate music every **7–14 days** ([TikAdSuite](https://tikadsuite.com/blog/best-music-for-tiktok-ads/)).
  - Higgsfield has `tiktok_music_trending` (not called). Check that its tracks are CML-cleared before paid use.
- **Fixes**: F8, F4. **Evidence**: A (Veo guides, TikTok terms) / B.
- **Input change**: a `sfx_library/` of real recorded foley per product action. Each music track gets `license: CML | original | royalty-free`, and export is blocked for paid placements otherwise.

---

## E. Product-photography conventions for the reference kit

### 20. Garment Reference Pack spec (what pros shoot per SKU)
Combined from Zalando's partner image guide ([apparel guide](https://partner.zalando.com/university/article/apparel-image-guide)), try-on vendors' input rules ([FASHN/Kolors via fal](https://fal.ai/explore/virtual-try-on-apis), [Botika](https://botika.com/products/on-model)) and e-com lighting practice:
1. **Views**: front, back, side packshot (whole garment, nothing cropped, no heavy folds, nothing overlapping). Add **ghost-mannequin or on-hanger** for structure (hoodies, jeans) and **flat lay** for print legibility. Ghost mannequin conveys shape and drape; flat lay is easier and better for reading the print ([wearview](https://www.wearview.co/faq/what-is-the-difference-between-flat-lay-and-ghost-mannequin), [weshop](https://www.weshop.ai/blog/ghost-mannequin-vs-flat-lay-which-one-makes-fashion-products-sell-better/)). Botika-style tools take **front + back** mannequin or flat-lay shots and claim "every stitch preserved".
2. **Detail macros** (Zalando "detail/informational view"): neck label or woven tag, print at 1:1, logo embroidery or puff texture, stitching or overlock, zip pull, cuff and hem, leggings waistband, denim rivets and back patch, hang-tag, mailer-bag print. These are the details models invent when they are missing (F2).
3. **Lens**: 50–100 mm full-frame equivalent. On a phone use the **2×/3× telephoto, not 0.5×/1× close up**, which stretches the edges ([replica surfaces](https://www.replicasurfaces.com/blogs/q-as/what-focal-length-lenses-minimize-distortion-in-flat-lay-photos), [pixel retouching](https://pixelretouching.com/best-lens-for-clothing-product-photography)). Keep the camera parallel to the surface and at the same distance for every SKU (tripod or boom).
4. **Colour**:
   - Continuous light **5600 K, CRI/TLCI ≥95**, large diffused softboxes ([Colbor](https://www.colborlight.com/blogs/articles/set-up-lighting-for-clothing-photography)).
   - **ColorChecker in the first frame of each session** → build a per-session camera profile → apply it to all shots. ΔE00 <1 is achievable ([X-Rite](https://www.xrite.com/service-support/color_management_workflow_with_dng_camera_profiles), [Lensrentals](https://www.lensrentals.com/blog/2019/07/how-to-use-an-x-rite-colorchecker-to-get-perfect-color/)).
   - Store the **measured hex/Lab per colourway**. AI tools render navy as black and flatten tonal prints ([metamodels](https://metamodels.ai/feeds/blog/ai-model-photography-what-fashion-brands-get-wrong)).
5. **Glossy surfaces** (plastisol or puff prints, the poly mailer): **cross-polarise**, with polariser film on the light and a CPL on the lens rotated to extinction. This removes glare and keeps texture. It costs about 1–2 stops of light and **needs its own colour profile** because the filters aren't neutral ([photographyattic](https://www.photographyattic.com/blog/2025/11/a-practical-guide-to-cross-polarisation-photography/), [xangle](https://xanglecs.com/doc16/photogrammetry/cross-polarization)).
6. **Label the role of each reference in the prompt**: "Image 1 = garment source (front), Image 2 = print detail, Image 3 = persona, Image 4 = room" ([apiyi](https://help.apiyi.com/en/nano-banana-pro-flat-lay-to-model-photo-apparel-workflow-en.html), [Leonardo](https://leonardo.ai/news/nano-banana-prompt-guide)). Nano Banana Pro accepts up to 14 refs.
- **Fixes**: F2 (main), F5 (on-hanger/mannequin shows drape), F9. **Evidence**: A (Zalando guide, X-Rite, several try-on vendors).
- **Input change**: `product.reference_pack` with required slots (front, back, side, flat, structure, macros[≥4], colour_hex, artwork[] for #6, optional scan for #7). Upload is rejected if it lacks a ColorChecker frame or was shot at 0.5×/1× below 60 cm (EXIF focal length check).
- **Cheapest test**: 0 credits. Re-shoot one hoodie to spec, then run the same Nano Banana composite with the old pack and the new pack (2 × 1.5 = **3 credits**).

---

## STOP DOING (with who says so)
1. **Generating garments on moving bodies for fit-critical beats** (leggings squats, denim walks, hoodie pull-on). Imma, Shudu, Miquela, Zara and Mango all keep the garment real. Mango's backlash was precisely about fit (#1, #4).
2. **Mimed prop actions in motion references.** Act the real object (Runway Act-Two docs, #13).
3. **Motion refs with hands in pockets, crossed arms, hands crossing the torso, or camera moves** (Kling docs and users, #12).
4. **Mixing generators within one ad for on-camera persona shots.** Coke's 70k clips across 3 models still read as inconsistent (#5).
5. **Rerolling a whole video to fix lip-sync.** Re-sync with lipsync-2-pro instead (#16). **Talking segments over 8 s per generation** (Kling second-8 wall, Seedance late drift).
6. **Line-by-line TTS and short TTS calls under about 250 chars**; overusing `[pause]` or break tags (ElevenLabs docs, #18).
7. **Cloning a persona voice from polished read-aloud audio** when the target is casual UGC. The clone copies the delivery style (#18).
8. **Algorithmic reverb on AI VO.** Use a real room IR or worldize (#17). Don't record plates or room tone with iPhone Audio Mix "Studio" mode.
9. **Trending TikTok sounds in paid ads.** They are not licensed; use CML or original audio (#19).
10. **Shooting references with the phone's wide lens up close**, without a colour target, or with glare on prints (#20).
11. **Expecting image-to-3D (`generate_3d`, Tripo, Hunyuan) to preserve logos.** Lighting is baked in and texel density is low. Use it for angles or blocking only (#7).
12. **Launching a persona without a likeness check** (Shein/Mangione, #3).

## Open questions
1. What does Higgsfield charge per second for Genjutsu Object Swap and Wan-class replace vs Kling 3.0 Motion Control? (Check via free `models_explore`; don't generate.) This decides whether Plate + Swap beats full-gen on credits as well as quality.
2. Can Wan Replace / Genjutsu be restricted to **head-only** so hands and garment pixels come through untouched? The Wan workflow exposes mask expansion; it is unclear whether Higgsfield exposes a mask.
3. How well does face swap hold when the performer pulls a hoodie over their head (face fully occluded, then revealed)? This is probably the hardest F1×F4 case. Test it early.
4. Can Seedance take the human VO as @audio **and** a persona image **and** a plate in one call, or does audio + video reference exceed the multimodal limits?
5. Automating logo patch (#6) headlessly: are CoTracker/OpenCV homographies good enough on cloth, or is Mocha-grade planar tracking needed?
6. Does SANTO's manufacturer have CLO/Browzwear files? If so, #9 becomes cheap for exact-colour, exact-print stills.
7. Legal/disclosure: do TikTok and Meta AI-content labels apply when only the face is synthetic on a real plate? H&M watermarks all AI twin content.
