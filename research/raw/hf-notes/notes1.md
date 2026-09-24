# Notes from HF workflows (SKILL.md)
Common UGC pipeline (review/unboxing/try-on/product, all v1.0-1.1):
- creator: soul_2, 3:4, quality 2k (or user photo) -> character_media_id, used for EVERY board+clip, never regenerate/describe inline
- board: gpt_image_2, 21:9, 2k, quality high; sheet of vertical 9:16 slots (review 8, unboxing 4, try-on 8, product 4). medias [product, character, (package), (prev cleaned board)]; prompt opens with @ImageN declarations matching medias order
- de-slop every board: media_import_url -> seedream_v5_pro role image_references 21:9 2k; exact prompt (KEEP EXACTLY ... CHANGE ONLY micro-realism ... flat authentic iPhone photo, deep focus ... AVOID ... bokeh, cinematic/DSLR). fallback seedream_v5_lite once; else raw
- clip: seedance_2_5, 9:16, 1080p, duration<=15, mode omni_reference, generate_audio true, medias [clean board, character, product]; board slots become internal hard cuts ("Hard cut to." markers only in clip prompts)
- duration table: 4-15s ->1 board; 16-19 ->2 balanced; 20-30 -> 15+rest...
- monologue density: <=10s 12-20 words; 11-12s 20-28; 13-15s 28-35
- first word never OK/So/Wait/Um/Like...; banned words literally/obsessed/game-changer/holy grail/hits different/elevate/seamless/effortless; never open Okay wait/OMG/Hey guys/Stop scrolling/Story time; friction openers ("I almost returned this."); one peak reaction per clip; one "but then" beat
- accent via text lands ~1 in 3; attach 5-10s voice sample as audio reference "accent and vocal delivery reference only — do not copy words"
- QA frozen frames: evenly spaced + every product closeup + 2-3 mid-word frames; one hero product; <=2 hands; absent features absent; prop state consistent; label not gibberish/mirrored; product scale matches hand; no doubled lip edges. Lip slop -> cut spoken words first. baked text -> rerun once then remove in post.
- stitch: ffmpeg concat -c copy hard cuts only, no transitions
- weight/grip physics: heavy two hands + strain; light one relaxed hand; tiny pinched near lens; never balance paired items on one palm. Two-handed actions force static camera; selfie POV leaves only one hand free.
- character re-roll: if board/clip fails twice, assume Soul render rejected (moderation) -> same prompt new seed, discard boards, cap 2.
- never empty medias to generate_video (silently T2V)
- Unboxing: slot1 PACKED sealed box, product not visible; slot2 REVEAL (box at edge or gone); slot3 product focus; slot4 satisfaction; box disappearance one-way; real package photo optional -> package_media_id as slot-1 reference; else generic brown taped box
- Try-on: 8 slots: PRE_WEAR (muted base outfit + plain kraft bag, never opened on camera) / WEARING (one twirl, static cam) / FRONT_POSE diff distance / TEXTURE_CLOSEUP hand-free macro VO / TURN over-shoulder / DETAIL hand-free macro different detail VO / STYLE_POSE different room / FINAL_LOOK loop-ready. No mirrors/reflections ever. Costume change carried by hard cut, never on camera. Lip-sync slots 1,2,3,5,7,8; macros voiceover with mouth closed. no CTA tail.
- Product-only: 4 slots INTRO/DEMO-A/DEMO-B/RESULT; product angle lock (only side visible in reference); person auxiliary, voice gender from product; VO only.

# try-on board/clip refs (ugc-try-board.md 100KB, ugc-try-clip.md 99KB) -- extracted to hf-notes/tryon/
- product intake staging contract: shape, material, color, hand-relative size ("palm-sized... ~15cm" never object comparisons), mechanism anatomy, absent features stated visually, label, one honest imperfection. Big readable logo -> warn: wordmarks render gibberish or real competitor brand.
- Absent-by-design features: state absence in prompt body AND closing negative run.
- Closure/hardware anatomy: name once positionally ("front-center zip") reuse exact phrasing every board.
- Multi product images: "valid angles of same garment... Switch angles only by hard cuts between slots, never continuous rotation. Do not invent unseen details."
- Realistic Fit sentence (verbatim).
- ANTI-MORPH: adjacent slots must differ in POV AND distance band; Seedance snaps to hard cut only when beats visually far apart; low-delta neighbors MORPH. Each band TIGHT/MID/WIDE >=2 times across 8. Default cadence SELFIE→STATIC→STATIC→STATIC-CLOSE→STATIC→STATIC-CLOSE→STATIC→STATIC; distance WAIST-UP→FULL-BODY→THREE-QUARTER→MACRO→THREE-QUARTER→MACRO→FULL-BODY-WIDE→MEDIUM-WIDE
- Every slot frozen MID-EVENT
- Hand allocation rule verbatim; selfie = one hand only; two objects -> static.
- hand-free macros: no touching fabric ("even gentle brushing reads as someone touching her clothes"); passive cue per garment: denim "wash gradient visible / seam line reads / fabric grain catches light"; knit "knit texture catches light"
- mirrors = "limb factory" banned
- lighting: never golden hour; one motivated source; neutral daylight window left/right
- iPhone front camera optics: 23mm-eq wide, DEEP focus, slight wide distortion edges, mild HDR flattening, slight highlight clipping at window, faint sensor noise shadows (never film grain)
- text: product own print only legal text; described lettering must be BIG (small logos render gibberish); no legible text on props
- one state per prop per slot; state changes only across hard cuts
- exactly one hero garment; no look-alike garments anywhere
- Clip: prompt is primary signal; board fed as ref; sparse prompt -> Seedance copies panels frame-for-frame = stiff. Don't transcribe board; write motion.
- Structure: Style & Mood / Narrative Summary / Dynamic Description Cut n (a-bs) ... "Hard cut to." / Static Description / Audio / quality suffix
- Time slicing 15s: 1.9/2.3/1.9/1.4/1.9/1.4/2.3/1.9 ; each cut >=0.5s
- STATIC language: "absolutely frozen, locked off, zero movement..." forbidden words handheld/shake/drift/wobble/sway/subtle movement in static cuts. Locked camera != locked body (weight transfer, pose shift required)
- SELFIE: phone NEVER visible; forbidden: mirror selfie, holding phone, phone screen...
- 0.1s hook law: first clause motion; first word within 0.0-0.4s
- H9 entry devices (drop-catch, walk-and-slam, light switch, zoom-out) with audio twin
- Baked camera moves: at most one per cut; candid handheld zoom-in opener with overshoot-and-correct
- micro-beats 5+/cut; ONE movement at a time (simultaneous reads as glitching); place beats BETWEEN phrases never on key word (smear lip sync); every audible beat into Audio line or renders mute
- unguarded micro-beat per clip (stumble/self-correct); sound intrusion (dog bark two bursts) max one
- goofy beat in 3 cuts
- "Hard cut to." verbatim markers, without them cuts collapse into smooth motion
- Set-Down / Pick-Up device replaces one hard cut; never across a state jump (outfit change)
- Audio: bias wordiest chunks to VO macro cuts (no lips to slop); protect the mouth: >=1 closed-mouth recovery beat in densest cut; delivery markup stretched vowel max 2, CAPS 1-2 words/cut, one em-dash break, one whisper-to-spike
- bracketed non-verbal sounds [*soft gasp*] at start of board 1 (max 3)
- No music default; if music: ducked, NO lyrics (fight lip-sync)
- "iPhone microphone audio with natural room tone throughout"
- Quality suffix verbatim (No cinematic color grade, film grain, shallow DOF, bokeh, lens flare, slow motion, beauty filter...)
- UGC camera realism: 23mm, deep focus, one small AE/AF adjustment mid-clip on selfie cut; physics: real weight, contact shadows, hair and fabric react
- State change minimization: max 1 state change per cut; off-camera state changes render BOTH states at once -> show it or hide with hard cut
- Mechanism locked (zipper: name part, position, motion once identical)
- Cause before effect
- accent: persona sentence first; write accent two levels stronger; never phonetic spelling
- quirk small-written renders ~2 of 9 -> stage 30% bigger; single-event SFX ("one sharp tap" not "taps" -> loops)
- Loop ending: mid-phrase timing cut or frame-match to cut 1
- ~2 words/second

# unboxing refs
- Box logic Case1 real package ref -> THIS package only; opening mechanism read from ref. Case2 generic brown box + color-matched tissue (empty boxes read as AI-fake)
- Box never lifted/carried; rests on surface; disappears after slot2 forever
- Cut1 Case A: box-cutter slices tape one decisive motion; Case B (branded package): finger drumming, slide/nudge few cm, then one clean opening motion at END of cut 1; Hard cut; Cut 2 product already emerging ("Do not describe the opening motion within Cut 2")
- Time split 15s: 3.5/4.5/3/4
- Realistic scale: "If label small in frame, the camera moves closer rather than scaling the product up" + "~X cm tall fits naturally in hand without enlargement"; image models default to enlarging product for label readability
- Weight classes Heavy/Bulky-light/Light/Tiny; default heavier if ambiguous
- one hero product; no look-alike shapes on surface
- Single action per cut; forbidden loop phrases: "sprays again","back and forth","opens and closes","taps the lid twice"
- cap removal before action; after removed never describe where it goes
- Post-reveal shapes FIRST-USE/WRONG-TURN/CLOSE-STUDY/SHOW-OFF, one twist/board
# review
- monologue: story mode default; product enters at 40-60% of runtime; one "but then" twist; hook patterns H1-H8 (H8 product cold open: slot 1 product-only rougher light slight compression, hard cut to creator mid-reaction)
- NEVER write engineered/dramatic pauses — bloat line and break render
- Silent/ASMR: zero synthetic voice is itself anti-slop; restate "no on-screen words" (model bakes karaoke subtitles into ASMR)
- series mode: reuse same character_media_id, persona sentence verbatim
- persona sentence restated verbatim in every prompt or it drifts
# character (soul_2)
- No products in character image (baked product breaks downstream compositing)
- Beauty floor anchors: high model facial features, symmetrical features, well-proportioned figure, natural skin texture (NB: Higgsfield default = attractive; might be counter to "real person")
- Mandatory iPhone phrasing list, HARD BAN list (centered composition, straight-on, editorial, minimal DOF, flattering even illumination, glowing/flawless skin, poses, warm smile at camera, ring light...)
- Approved mid-action expressions list
- Body pose neutral only — creative poses anatomy gamble (extended limbs warp, foreshortened hands grow fingers)
- Neutral cool daylight only, never golden hour
- Closing block verbatim
- Wardrobe Style DNA: silhouette contrast; one metal; PRINT SIZE LAW (big prints clean, small logos gibberish)
- anti-clone: differ in >=2 of age/hair color/hair style/build
# character-sheet workflow
- anti-glare eye clause "naturally muted catchlights, no oversized specular glare in the iris, eye color muted rather than glowing"
- realism module: "visible fine skin texture with natural pores, fine lines, subtle asymmetries ... slightly uneven foundation blending ... slight natural sheen rather than glossy or dewy retouched finish, no digital smoothing, no beauty filter, no AI-airbrushed look, skin completely free of artificial glare... matte-to-natural complexion" + imperfection anchors freckles, small mole
- mature facial structure (avoid babyface); split-screen full-body + chest-up close; 16:9; negative tail single subject etc.
- consistency carries forward: restate all established details on iteration
# ad-multiplier
- model ad_multiplier, mode video_edit, generate_audio false, source 4-30s, duration ceil(source), 720p rec; preserves motion/framing/cuts/timing; replace person/product/clothing/background; source audio restored via ffmpeg
- person replacement @ImageN authoritative for complete look incl clothing unless separate garment image mapped (clothing_override)
- Soul 2.0 replacement person prompt 140-190 word paragraph, studio white full-body
- prompt <=3900 chars; Genjutsu routes: hf_mult_motion_control (motion transfer), hf_mult_replace_object
# product-photoshoot
- model nano_banana_pro locked, 2k, role image_references, end prompt with "resolution: 2k"; distinct prompts per variant not count:N; max 2 refinements/index, 3 submissions/index total; refinement uses latest job of same index as single ref; sanitize photographer names
- one product identity across set: generate index 0 first, reuse its job id as ref for rest
# models_explore (2026-09-24) video
seedance_2_5: modes t2v/omni_reference/video_edit/video_extension(backward|forward); 4-30s; 480/720/1080; audio default true; bitrate high; roles start_image,end_image,image_references,video_references,audio_references. video_edit billed by source duration.
seedance_2_0: 4-15s; std/fast (fast 480/720 only); up to 4k; genre; audio; same 5 roles; unlim
seedance_2_0_mini: 480/720; budget
kling3_0: 3-15s; std/pro/4k; sound on/off (off lowers credits); roles start_image,end_image ONLY; 16:9/9:16/1:1
kling3_0_turbo: start_image only; 720/1080
kling_video_edit (3.0 Omni Edit): video_references + image_references; std/pro/4k
wan3_0 / wan3_0_prime: 2-30s or -1 smart (billed 10s); enable_thinking (better adherence); 5 roles incl first/last frame, image/video/audio refs
wan2_7: start/end + audio refs
minimax_h3: 4-15s 2K, batch 1-4, 5 roles
veo3_1: start_image only, 4/6/8s; veo3_1_lite start+end
gemini_omni_flash_1_1: modes t2v/i2v/ref/edit (edit up to 30s), 360p-4k
flux_3_video: 5-20s, start/end/image/video refs, audio; flux_3_video_edit 1 credit/sec
grok_video_v15: start, image refs, audio refs
hf_mult_motion_control (Genjutsu motion transfer), hf_mult_replace_object (Genjutsu replace): image_references + video_references, 480-1080
ad_multiplier: Seedance 2.5 based; video_edit
marketing_studio_video: 12-15s; avatar_ids max1; product_ids; hook_id/setting_id (UGC, Tutorial, Unboxing, Product Review, UGC Virtual Try On); ad_reference_id recreates analyzed scenario of reference video
sync_so (Sync Lipsync 3): input_video+input_audio; sync_mode bounce/loop/cut_off/silence/remap
cinematic_studio_video_v2: multi_shots, speedramp, cfg_scale
video_deflicker, topaz_video, bytedance_video_upscale (preset ugc / aigc)
# image
soul_2: medias max 1 image; soul_id; 1.5k/2k
soul_cast, soul_location
nano_banana_pro: image_references (no max listed); 1-4k
nano_banana_2: image_references + mask, is_inpaint
seedream_v5_pro: image_references, is_inpaint, remove_bg, up to 2k
gpt_image_2: role image, 1-4k, quality low/med/high
ms_image (DTC ads): medias max 14, product_ids max 4
No cost / max-ref numbers exposed by models_explore.
# GitHub
## charlesdove977/UGC-Factory (skill/frameworks)
- Elements (show_reference_elements create) vs Soul: Elements instant, multi refs per generation, work in Seedance 2.0/Kling 3.0/NBP/GPT Image 2/Seedream/Cinema Studio; Soul only Soul V2/Cinema, one person, 5-20 photos ~10min
- Multi-angle character element: 3-4 images same person same wardrobe/lighting (front, 3/4 L, 3/4 R, profile) in ONE create call -> stronger identity lock and realistic turns
- Environment element: one clean plate of the room, category environment, embed <<<env_id>>> to keep backdrop consistent
- Never blank/thin prompt (< ~2 sentences) -> gibberish
- 15s ad: 1 clip, 2 elements, 2-3 images total
## joebenscoter86/higgsfield-ugc-workflow (reverse-engineered from Higgsfield's agent)
- storyboard 16:9 three 9:16 panels Tight hook / Macro hands action / Wide recommendation via nano_banana_pro
- Seedance 2.0 15s 720p ~67 credits; 1080p ~135 "looks no different" for phone selfie; render audio-bound, 720p not faster; no 720 draft->1080 final (audio differs)
- generate_video get_cost:true preflight returns credit cost without generating (cost gate)
- phonetic spelling of brand in spoken line only ("Noo Standard Labz", vial->vile, Joe Bee); "no subtitles" else burns captions
- no product in character portrait (causes drift/warp)
## OSideMedia/higgsfield-ai-prompt-skill (seedance-2-5 SKILL, FAILURE-MODES)
- Seedance 2.5 (Dreamina doctrine): every material explicit role + exclusion ("@Image 2 defines the workbench and window light. Do not use the people in the image.")
- fidelity grade: full-preserve/partial/attribute-transfer/loose
- material budget 30 images/10 videos/10 audio, 50 max; stable 1-8 subjects; edit source <=20s + 1-5 refs
- several views of one subject must say one subject "output must contain only one X" else duplicates
- character sheet leak: grey backdrop/panel layout renders as set -> exclusion
- Beat lines name characters (name + one marker), never @handles (handle as subject -> two people)
- Official HF Seedance 2.5 deck: views on light-grey ground, one view strong expression (teeth) else first line of dialogue invents a mouth. Canonical four: front, back, facial neutral, facial dynamics/teeth
- first/last frame declared in prompt ("@Image 1 is the first frame"), never merged in one sentence; aspect locks to first image
- FAILURE MODES: FPS drift (state "24 fps. No frame is repeated"); frame-level review; salvage 1-3s from failed takes; keyframe-consistency forces invention (state absence explicitly); physics-state-anchor ("magnet stays attached... only X moves"); action-reversal fill (chain 2-3 actions same vector; name camera endpoint); filler-babble on short lines (<=6 words in 4s -> babble; 8-12 words clean ~3 w/s; give other faces at-rest mouth fact); truncated action (name completion state, hold 0.15-0.35s); mimed manipulation (write causal chain: initial structure, anchor, force, material feedback, finished state; or two states + sound off screen; never invent structure not visible in ref; don't stack brand face + two-hand manipulation + effect in one shot)
- repo says 2.5 on HF 720p max & no start/end (snapshot 2026-08-07) — LIVE models_explore 2026-09-24 shows 1080p + start/end roles => changed
