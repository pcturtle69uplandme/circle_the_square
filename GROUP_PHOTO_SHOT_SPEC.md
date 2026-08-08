# 📸 CORPORATE GROUP PHOTO GONE WRONG — SHOT & PROMPT SPECIFICATION

**Project:** *Circle the Square* / *ALL UNDER ONE ROOF*  
**Shot ID:** `S58.5` (Post-Credits Corporate Website Stinger)  
**Setting:** Grand Atrium Lobby (`IMG_20260804_131855397`) — Faceted orange-ochre reception desk & black-and-white triangle wall  
**Format:** 16:9 (Cinematic 2.39:1 crop framing), High-Resolution Group Plate  
**Tone:** Corporate Mockumentary Chaos / Satire

---

## 📌 Creative Concept

A staged "Meet the Prism Team" corporate website photo shoot that collapses into total dysfunctional office chaos. 

The banner text on the photographer's tripod sign reads:  
> **"PRISM — INNOVATION, INTEGRITY, TOGETHER."**

---

## 🎭 Character Stances & Postures

| Character | Position in Frame | Wardrobe | Gesture & Expressive Beat |
|---|---|---|---|
| **Jan Peach (CEO)** | Front Center | Charcoal suit jacket unbuttoned, slate shirt | Face red with pure rage, jaw open mid-shout, fists clenched at waist ("Jan being Jan"). |
| **Christina (Strategy)** | Front Right | Chic beige blazer, navy silk top | Completely ignoring the camera, holding a gold compact mirror, applying lipstick. |
| **Sharon (Operations)** | Center Left | Severe grey power suit, navy lanyard | Arms tightly crossed over chest, severe unimpressed death-stare at Chris and Rick. |
| **Chris & Rick** | Background Center | Chris (grey polo shirt), Rick (navy security uniform + radio) | Mucking about: Rick putting bunny ears behind Chris's head; Chris pulling a funny face holding a burnt-orange stress ball. |
| **Trevor** | Far Left | Charcoal overcoat, slate shirt, cross-body messenger bag | Standing perfectly still, deadpan blank stare into the camera lens ("Why am I here?"). |
| **Receptionist (`EXTRA-AT-01`)** | Far Right (Behind Desk) | Navy blazer, white blouse | Ducking down behind the orange reception desk to avoid collision. |

---

## 📝 1. FLUX Kontext Image Generation Prompt (ComfyUI Local)

```markdown
PROMPT:
A chaotic group photo of five corporate office employees standing in a modern corporate atrium lobby in front of a faceted orange-ochre reception desk with a black-and-white triangle wall. 

In the center front, a 45-year-old male CEO with short grey hair and a red furious face is shouting with clenched fists. To his right, a 35-year-old female executive in a beige blazer ignores the camera to check her compact mirror and apply lipstick. To his left, a stern 40-year-old female operations director with crossed arms gives an unimpressed glare to the background. In the background, a security guard and tech worker are mucking about doing bunny ears behind each other. On the far left, a quiet man in a grey overcoat and cross-body messenger bag stands motionless with a blank deadpan expression looking into the camera.

Cinematic 35mm photograph, wide 1-point perspective framing, bright indoor office lighting, 2.39:1 aspect ratio, sharp focus across all figures, corporate satire style.
```

---

## 📹 2. Video AI Clip Synthesis Prompt (Google Veo 2 / Sora)

```markdown
PROMPT (Video + Native Audio):
Cinematic wide tripod shot of a corporate lobby team photo gone wrong. In the atrium of Prism HQ, five employees pose awkwardly for a website banner photo. The male CEO in the center explodes in anger, shouting and gesticulating violently. The female strategy lead on the right checks her compact mirror and powders her face, unbothered. The female operations manager on the left glares in disbelief as two male colleagues in the back goof around and throw peace signs. A quiet man on the far left stands motionless staring deadpan into the lens. 

NATIVE AUDIO PROMPT:
"Furious shouting from CEO, low laughter from background workers, compact mirror snap click, ambient atrium echo, sudden camera flash pop sound."
```

---

## 🐍 3. Python Script Setup (`make_group_photo.py`)

A local generation script prepped in `C:\ai\kimi\docs\prompts\make_group_photo.py` to trigger this group render via ComfyUI FLUX Kontext:

```powershell
cd C:\ai\kimi\docs\prompts
python make_group_photo.py
```

*This shot specification has been added to [`MASTER_PRODUCTION_MANUAL.md`](MASTER_PRODUCTION_MANUAL.md) and [`STORYBOARD_V3.md`](../kimi/docs/prompts/STORYBOARD_V3.md).*
