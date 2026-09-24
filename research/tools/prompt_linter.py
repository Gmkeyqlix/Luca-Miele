#!/usr/bin/env python3
"""Cutroom storyboard + prompt linter: catch rule breaks before paying for video.

Encodes the rules in research/QUALITY-PLAYBOOK.md (section numbers in brackets
in each message). Free to run; exit code 1 when there are errors.

    python research/tools/prompt_linter.py research/tools/examples/good_fitcheck.json
    python research/tools/prompt_linter.py research/tools/examples/bad_fitcheck.json

Storyboard JSON (see examples/ for a full one):
{
  "model": "seedance_2_5" | "seedance_2_0" | "kling3_0" | "wan3_0",
  "mode": "board" | "separate",          # board = one call with internal hard cuts
  "duration": 15,
  "prompt": "full text sent to the model",
  "refs": [{"tag": "@Image1", "role": "identity|product|room|state|cut|motion|voice",
            "use": "...", "exclude": "...", "contains_product": false}],
  "shots": [{
     "seconds": 1.9, "pov": "SELFIE|STATIC|STATIC-CLOSE", "distance": "TIGHT|MID|WIDE",
     "camera_holder": "selfie|propped|friend|none", "beat": "SPEAK|DO",
     "left_hand": "phone|parked|<action>", "right_hand": "parked|<action>",
     "dialogue": "...", "action": "...",
     "props": {"mailer": ["sealed", "sealed"]}     # [state at start, state at end]
  }]
}
"""

import json
import re
import sys

PROMPT_CAPS = {"seedance": 2500, "kling_per_shot": 500}  # [12.1] silent truncation

BOOSTERS = r"\b(4k|8k|ultra[- ]?detailed|hyper[- ]?realistic|photorealistic|masterpiece|sharp focus|stunning|flawless|award[- ]winning)\b"
CINEMA = r"\b(bokeh|shallow depth of field|85 ?mm|35 ?mm|f/1\.\d|cinematic|film grain|halation|golden hour|warm sunset|ring ?light|softbox|studio lighting|editorial|teal[- ]and[- ]orange|anamorphic|arri|imax|dslr)\b"
POSED = r"\b(smiles at the camera|poses for the camera|poses|poised|elegant stance|warm smile|confident smile|flawless skin|glowing skin|radiant)\b"
CAMERA_GEAR = r"\b(phone in (her|his|their) hand|holding (the |a )?phone|selfie stick|tripod|gimbal|drone|mirror selfie)\b"
MIRROR = r"\b(mirror|reflection|shop window)\b"
LOOP_VERBS = r"\b(again|twice|back and forth|repeatedly|opens and closes|over and over)\b"
HANDHELD_WORDS = r"\b(handheld|shake|shaky|wobble|drift|sway|micro-shake)\b"
AI_PHRASES = r"\b(obsessed|game[- ]changer|holy grail|hits different|10/10|elevate|seamless|effortless|literally|you need this)\b"
BAD_OPENERS = ("ok", "okay", "so", "alright", "um", "well", "like", "wait", "hold on", "omg", "hey guys", "story time", "stop scrolling")
UNBRANDED = r"keep the product blank|unbranded"
REALISM_CUES = r"\b(iphone|phone|ugc|pores|handheld|real room|sensor noise|deep focus|front[- ]camera)\b"
NEGATED_OBJECT = r"\bno (blur|hands?|makeup|red|people|person|logo)\b"  # Seedance summons negated visible objects [4]
FIRST_PERSON_CLAIM = r"\b(i bought|i ordered|i've been wearing|changed my life|best purchase)\b"
STATE_WORDS = r"\b(rips?|tears?|pulls? (it )?on|pulls? over|unzips?|zips? up|puts? on|takes? off|changes into)\b"

# words per duration [4] (13-15 s -> 28-35)
WORD_BUDGET = [(10, 12, 20), (12, 20, 28), (15, 28, 35), (30, 28, 70)]


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def err(self, where, msg):
        self.errors.append(f"ERROR   {where}: {msg}")

    def warn(self, where, msg):
        self.warnings.append(f"warning {where}: {msg}")


def find(pattern, text):
    return sorted({m.group(0).lower() for m in re.finditer(pattern, text, re.I)})


def lint_prompt(sb, r):
    p = sb.get("prompt", "")
    model = sb.get("model", "")
    low = p.lower()

    if model.startswith("seedance") and len(p) > PROMPT_CAPS["seedance"]:
        r.err("prompt", f"{len(p)} chars > ~{PROMPT_CAPS['seedance']}: Seedance silently truncates the end [12.1]")
    if model.startswith("kling"):
        for i, block in enumerate(re.split(r"(?i)\bshot \d+\b", p)[1:], 1):
            if len(block) > PROMPT_CAPS["kling_per_shot"]:
                r.err(f"prompt shot {i}", f"{len(block)} chars > ~500: Kling multi-shot truncates [12.1]")

    for label, pat, level in [
        ("booster words", BOOSTERS, "err"), ("cinema/studio look words", CINEMA, "err"),
        ("posed language", POSED, "err"), ("camera gear named", CAMERA_GEAR, "err"),
        ("mirror/reflection", MIRROR, "err"), ("loop verbs", LOOP_VERBS, "warn"),
        ("AI-script phrases", AI_PHRASES, "err"), ("first-person purchase claim", FIRST_PERSON_CLAIM, "err"),
    ]:
        hits = find(pat, p)
        if hits:
            (r.err if level == "err" else r.warn)("prompt", f"{label}: {', '.join(hits)} [5]")

    if re.search(UNBRANDED, p, re.I):
        r.err("prompt", "'keep the product blank/unbranded' strips the SANTO logo; replace with 'keep the logo/print exactly as in the reference' [1 #4]")

    first30 = " ".join(p.split()[:30])
    if not re.search(REALISM_CUES, first30, re.I):
        r.warn("prompt", "no phone/UGC realism cue in the first 30 words; realism goes at the START [4][12.1]")

    if "slow motion" not in low and "real-time" not in low and "real time" not in low:
        r.warn("prompt", "add 'real-time speed, never slow motion' [4 motion]")

    has_speech = any(s.get("dialogue") for s in sb.get("shots", []))
    if has_speech and "no subtitles" not in low:
        r.err("prompt", "dialogue without 'No subtitles.': the model burns in its own captions [6]")
    if model.startswith("seedance") and "no background music" not in low and "no music" not in low:
        r.warn("prompt", "add 'no background music' (otherwise Seedance invents an ad track) [6]")
    if model.startswith("kling") and sb.get("audio", True) and not has_speech:
        r.warn("prompt", "Kling adds music even when told not to: turn audio off for non-speech shots [12.5]")

    if model.startswith("seedance") and re.search(NEGATED_OBJECT, p, re.I):
        r.warn("prompt", f"negating a visible object ({', '.join(find(NEGATED_OBJECT, p))}) can summon it on Seedance; say it positively [4]")

    if sb.get("mode") == "board" and model.startswith("seedance"):
        n_cuts = len(sb.get("shots", []))
        markers = len(re.findall(r"Hard cut to\.", p))
        if n_cuts > 1 and markers != n_cuts - 1:
            r.err("prompt", f"{n_cuts} cuts need exactly {n_cuts - 1} 'Hard cut to.' markers, found {markers} [1 #1]")

    tags_in_prompt = re.findall(r"@(?:Image|Video|Audio) ?\d+", p)
    ref_tags = [x.get("tag", "").replace(" ", "") for x in sb.get("refs", [])]
    seen = []
    for t in tags_in_prompt:
        t = t.replace(" ", "")
        if t not in seen:
            seen.append(t)
    imgs_prompt = [t for t in seen if t.startswith("@Image")]
    imgs_refs = [t for t in ref_tags if t.startswith("@Image")]
    if imgs_prompt and imgs_refs and imgs_prompt != imgs_refs[: len(imgs_prompt)]:
        r.err("refs", f"upload order {imgs_refs} doesn't match first mention order in prompt {imgs_prompt}: roles swap [12.1]")


def lint_refs(sb, r):
    refs = sb.get("refs", [])
    images = [x for x in refs if x.get("tag", "").startswith("@Image")]
    if len(images) > 8:
        r.warn("refs", f"{len(images)} image refs: more refs degrade results, stay within 1-8 [4]")
    for x in refs:
        tag = x.get("tag", "?")
        if not x.get("role"):
            r.err(tag, "reference has no role [4]")
        if not x.get("exclude") and x.get("role") in ("identity", "room", "motion", "voice"):
            r.warn(tag, "no 'do not use …' exclusion line (e.g. room: 'do not use the people') [4]")
        if x.get("role") == "identity" and x.get("contains_product"):
            r.err(tag, "product baked into the person reference → product drift; use a person-only image [5]")
    products = [x for x in refs if x.get("role") == "product"]
    if len(products) > 1 and "one single" not in sb.get("prompt", "").lower():
        r.err("refs", "several product views without 'All these images define one single <item>. The output must contain only one.' [4]")


def words(s):
    return len(re.findall(r"[A-Za-z0-9'’]+", s or ""))


def lint_shots(sb, r):
    shots = sb.get("shots", [])
    model = sb.get("model", "")
    total = sum(float(s.get("seconds", 0)) for s in shots)
    dur = float(sb.get("duration", total))
    if shots and abs(total - dur) > 0.3:
        r.err("shots", f"shot seconds sum to {total:.1f} but duration is {dur:.1f}")

    speech_words = sum(words(s.get("dialogue")) for s in shots)
    for max_d, lo, hi in WORD_BUDGET:
        if dur <= max_d:
            if speech_words and not lo <= speech_words <= hi:
                r.warn("script", f"{speech_words} spoken words for {dur:.0f}s; target {lo}-{hi} [4]")
            break

    for i, s in enumerate(shots, 1):
        hits = find(AI_PHRASES, s.get("dialogue") or "") + find(FIRST_PERSON_CLAIM, s.get("dialogue") or "")
        if hits:
            r.err(f"shot {i} script", f"AI-sounding or fake-customer line: {', '.join(hits)} [4][10]")

    first_line = next((s.get("dialogue") for s in shots if s.get("dialogue")), "")
    if first_line:
        opener = re.sub(r"^\[[^\]]*\]\s*", "", first_line.strip()).lower()
        for bad in BAD_OPENERS:
            if opener.startswith(bad + " ") or opener.startswith(bad + ","):
                r.err("script", f"opens with '{bad}': start on hook content [4]")

    t = 0.0
    talk_run = 0.0
    for i, s in enumerate(shots, 1):
        where = f"shot {i}"
        secs = float(s.get("seconds", 0))
        action = (s.get("action") or "")
        hands = [s.get("left_hand", "parked"), s.get("right_hand", "parked")]
        busy = [h for h in hands if h and h not in ("parked", "phone", "idle", "rest")]

        if s.get("camera_holder") == "selfie" and len(busy) > 1:
            r.err(where, "selfie uses one hand for the phone: a two-handed action needs camera_holder 'propped' [4 hand law]")
        if s.get("camera_holder") == "selfie" and "phone" not in hands:
            r.warn(where, "selfie: set one hand to 'phone' (off-frame) so the hand count adds up [4]")
        if s.get("beat") == "SPEAK" and busy:
            r.err(where, f"SPEAK beat with hand action ({', '.join(busy)}): split into SPEAK + DO, VO over the DO shot [4]")
        if s.get("beat") == "DO" and s.get("dialogue") and s.get("lipsync", True):
            r.warn(where, "DO beat with dialogue: make it voice-over (mouth closed), not lip-sync [4]")
        if s.get("pov") == "STATIC" and re.search(HANDHELD_WORDS, action, re.I):
            r.err(where, f"static shot uses handheld words ({', '.join(find(HANDHELD_WORDS, action))}): they leak motion [01 T6]")
        if re.search(STATE_WORDS, action, re.I):
            r.warn(where, f"on-camera state change ({', '.join(find(STATE_WORDS, action))}): hide it on the cut or use fixed-state wording [4][12.2 #47]")
        for prop, states in (s.get("props") or {}).items():
            if len(states) == 2 and states[0] != states[1]:
                r.err(where, f"'{prop}' changes {states[0]}→{states[1]} inside the shot: change states on the cut [4]")

        if i > 1:
            prev = shots[i - 2]
            if s.get("pov") == prev.get("pov") and s.get("distance") == prev.get("distance"):
                r.err(where, f"same POV+distance as shot {i-1} ({s.get('pov')}/{s.get('distance')}): cuts will morph [1 #1 anti-morph]")
            for prop, states in (s.get("props") or {}).items():
                pstates = (prev.get("props") or {}).get(prop)
                if pstates and pstates[-1] != states[0] and s.get("transition", "hard_cut") != "hard_cut":
                    r.err(where, f"'{prop}' state jumps across a non-hard-cut transition [01 T3]")

        dl = words(s.get("dialogue"))
        if s.get("beat") == "SPEAK" and 0 < dl <= 6 and secs >= 3:
            r.warn(where, f"{dl}-word line in {secs}s: short lines get filler mumble, use 8-12 words or shorten the shot [4]")
        if s.get("beat") == "SPEAK":
            talk_run += secs
            if model.startswith("kling") and t + secs > 10:
                r.err(where, "Kling lip-sync after ~10s drifts: put speech first, end on silent DO beats [12.1]")
        else:
            talk_run = 0
        if talk_run > 8 and model.startswith("kling"):
            r.warn(where, "more than 8s of continuous talking in one Kling generation [4]")
        if sb.get("mode") == "separate" and model.startswith("seedance") and secs < 2:
            r.warn(where, "Seedance rarely renders a separate shot under 2s [03 T15]")
        if model.startswith("kling") and sb.get("mode") == "board" and secs < 3:
            r.warn(where, "Kling multi-shot: keep each shot ≥3s [12.1]")
        t += secs

    if model.startswith("kling") and sb.get("mode") == "board" and len(shots) > 6:
        r.err("shots", "Kling multi-shot allows ≤6 shots [12.1]")
    if sb.get("mode") == "board" and len(shots) > 8:
        r.warn("shots", f"{len(shots)} cuts in one call: more than 8 over-compresses [12.1]")


def lint(sb):
    r = Report()
    lint_prompt(sb, r)
    lint_refs(sb, r)
    lint_shots(sb, r)
    return r


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    bad = 0
    for path in sys.argv[1:]:
        with open(path) as f:
            sb = json.load(f)
        r = lint(sb)
        print(f"\n== {path}: {len(r.errors)} errors, {len(r.warnings)} warnings")
        for line in r.errors + r.warnings:
            print("  " + line)
        if not r.errors:
            print("  OK to spend credits" + (" (review warnings)" if r.warnings else ""))
        bad += bool(r.errors)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
