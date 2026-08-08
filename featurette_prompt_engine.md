# 🎬 CIRCLE THE SQUARE — FEATURETTE MICRO-CLIP PROMPT ENGINE
> **"Project Inception" — Shot-by-Shot Iterative Production Workflow**  
> **AI Targets**: Google Veo 2 · Veo 3 · Kling AI · Runway Gen-3 · Sora  
> **Rule**: Generate ONE shot → Review → Approve or Adjust → Then move to next  
> **Clip Duration**: 5–10 seconds per shot  
> **Total Shots**: 20 micro-clips → ~2:10 total cut runtime  
> **Status**: LOCKED ✅

---

## 🚦 GATE-BASED PRODUCTION WORKFLOW

```
GENERATE S01
    ↓
✅ APPROVE? → Move to S02
❌ REJECT?  → Update prompt → Regenerate S01 → Approve → Move to S02
    ↓
(Repeat for every shot through S20)
    ↓
STITCH all 20 approved clips in editor
    ↓
DUB Qwen3-TTS dialogue over each scene
    ↓
ADD SFX layer (plates, glass, taser, door clicks)
    ↓
EXPORT final cut
```

> 💡 **Key Rule**: If S01 is wrong (wrong location look, wrong character outfit, wrong lighting) — FIX the shared STYLE ANCHOR below before generating S02. All subsequent shots inherit the corrected anchor prompt.

---

## 🎨 SHARED STYLE ANCHOR
> Paste this into EVERY shot prompt to maintain visual consistency across all 20 clips.

```
Photoreal cinematic 35mm footage. Modern UK corporate office building interior. Warm cream/sand brick and pale concrete architecture. Fair-faced grey concrete columns. Full-height glazing with natural Northern European daylight. Oak/timber slat joinery accents. Grey carpet tile floors. No lens flare. No visible real-world branding or crests. Documentary-style handheld camera. British corporate mockumentary tone. Shallow depth of field on close-ups, deep focus on wide/establishing shots. 2.39:1 cinematic widescreen aspect ratio.
```

---

## 📋 SHOT STATUS TRACKER

| Shot | Scene | Duration | Status | Notes |
|------|-------|----------|--------|-------|
| S01 | Jan's Office — Establishing Wide | 6s | ⬜ PENDING | |
| S02 | Jan's Office — MCU Jan Pompous | 8s | ⬜ PENDING | |
| S03 | Jan's Office — OTS Christina Deadpan | 6s | ⬜ PENDING | |
| S04 | Jan's Office — CU Jan Stress Build | 5s | ⬜ PENDING | |
| S05 | Jan's Office — Wide Shirt Off & Arrow | 8s | ⬜ PENDING | |
| S06 | Jan's Office — MCU Door Sharon Enters | 4s | ⬜ PENDING | |
| S07 | Jan's Office — Reaction Sharon Glance | 5s | ⬜ PENDING | |
| S08 | Jan's Office — MCU Jan Locks Blinds | 5s | ⬜ PENDING | |
| S09 | Corridor — Tracking Wide Sharon Exits | 8s | ⬜ PENDING | |
| S10 | Corridor — 2-Shot Chris & Rick | 6s | ⬜ PENDING | |
| S11 | Open-Plan — High Wide Jan Announces | 8s | ⬜ PENDING | |
| S12 | Open-Plan — MCU Jan £50k Rage | 8s | ⬜ PENDING | |
| S13 | Open-Plan — Reaction Cuts Crowd | 6s | ⬜ PENDING | |
| S14 | Canteen — Wide Establishing Pastries | 6s | ⬜ PENDING | |
| S15 | Canteen — Handheld MCU Jan Rage Build | 8s | ⬜ PENDING | |
| S16 | Canteen — Wide Plates Crash Chair Smash | 10s | ⬜ PENDING | |
| S17 | Canteen — Low MCU Rick Taser Draw | 5s | ⬜ PENDING | |
| S18 | Canteen — INSERT Taser Flash | 3s | ⬜ PENDING | |
| S19 | Canteen — Wide Jan Slumps | 5s | ⬜ PENDING | |
| S20 | Canteen — 2-Shot Chris & Rick Aftermath | 8s | ⬜ PENDING | |

> Update Status: ⬜ PENDING → ✅ APPROVED → ❌ REJECTED → 🔄 REGENERATING

---

---

# SCENE 1 — INT. JAN'S OFFICE - DAY

---

## 🎥 S01 — Jan's Office Establishing Wide
**Duration**: 6 seconds | **Shot Type**: WIDE LOCKED-OFF  
**Beat**: Jan seated behind desk, Christina standing opposite — calm opening

### 📎 Attach These Images (2 Max)
| # | File | Role | Full Path |
|---|------|------|-----------|
| 1 | `IMG_20260804_131855397.jpg` | **Env Plate** — Faceted orange desk & triangle wall | `C:\ai\Circle the Square\building-reference\use-images\IMG_20260804_131855397.jpg` |
| 2 | `jan_peach_identity_sheet.jpg` | **Character** — Jan Peach CEO, navy suit, buttoned shirt | `C:\ai\Circle the Square\character-refs\jan_peach_identity_sheet.jpg` |

### 🎬 VIDEO PROMPT
```
A locked-off wide shot of a modern UK corporate glass-walled office. A 52-year-old overweight male CEO in a dark navy suit sits behind a desk with a smug thin-lipped expression, fingers steepled. Opposite him stands a 38-year-old female executive in a charcoal blazer and cream blouse, posture upright and composed, holding a tablet. They are mid-conversation. The background features a faceted ochre-orange reception desk and a striking black-and-white geometric triangle pattern wall. Warm office interior lighting. Static wide shot, 6 seconds. [PASTE STYLE ANCHOR HERE]
```

### 🔊 AUDIO PROMPT
```
Quiet office ambient. Low HVAC hum. Distant keyboard tapping. No music. Two voices in calm business conversation begin faintly — pompous senior British male, measured professional female.
```

### 🎭 CONTINUITY
- Jan: **Shirt buttoned**, suit jacket on, smug expression
- Christina: Charcoal blazer, composed

### ✅ GATE CHECK — Before Moving to S02, Verify:
- [ ] Office feels like a real UK corporate space (not generic)
- [ ] Orange faceted desk & triangle wall visible in background
- [ ] Jan reads as 50s, overweight, CEO-type in navy suit
- [ ] Christina reads as professional, poised female executive
- [ ] Lighting is warm indoor, not cold/sterile

---

## 🎥 S02 — Jan Pompous Explanation MCU
**Duration**: 8 seconds | **Shot Type**: MCU (Medium Close-Up) on Jan  
**Beat**: Jan explaining the breakfast meeting idea with self-important authority

### 📎 Attach These Images (2 Max)
| # | File | Role | Full Path |
|---|------|------|-----------|
| 1 | `IMG_20260804_131855397.jpg` | **Env Plate** — Office backdrop | `C:\ai\Circle the Square\building-reference\use-images\IMG_20260804_131855397.jpg` |
| 2 | `jan_peach_identity_sheet.jpg` | **Character** — Jan, smug default expression | `C:\ai\Circle the Square\character-refs\jan_peach_identity_sheet.jpg` |

### 🎬 VIDEO PROMPT
```
A medium close-up shot on a 52-year-old overweight male CEO in a dark navy suit sitting at his desk. He speaks with exaggerated self-importance — chin raised, brows half-raised, fingers steepled then gesturing. His expression is smug and convinced of his own brilliance. He references his MBA without any irony. Shallow depth of field, blurred office background with orange desk visible. Slight push-in as he speaks. 8 seconds. [PASTE STYLE ANCHOR HERE]
```

### 🔊 AUDIO PROMPT
```
Pompous senior British male voice, measured and self-assured. Office ambient very low under voice. No music.
```

### 🎭 CONTINUITY
- Jan: **Shirt buttoned**, no visible sweat yet, smug not red

### ✅ GATE CHECK — Before Moving to S03, Verify:
- [ ] Jan's face matches character sheet (age, weight, hair)
- [ ] Shirt clearly **buttoned** — continuity check
- [ ] Pompous, not yet stressed — wrong if he looks angry here

---

## 🎥 S03 — Christina Deadpan Response OTS
**Duration**: 6 seconds | **Shot Type**: OTS (Over The Shoulder — Jan's shoulder to Christina)  
**Beat**: Christina responds dryly. Zero emotional reaction. Slight head tilt.

### 📎 Attach These Images (2 Max)
| # | File | Role | Full Path |
|---|------|------|-----------|
| 1 | `IMG_20260804_131855397.jpg` | **Env Plate** — Office backdrop | `C:\ai\Circle the Square\building-reference\use-images\IMG_20260804_131855397.jpg` |
| 2 | `christina_dross_identity_sheet.jpg` | **Character** — Christina, deadpan composed expression | `C:\ai\Circle the Square\character-refs\christina_dross_identity_sheet.jpg` |

### 🎬 VIDEO PROMPT
```
An over-the-shoulder shot from behind a 52-year-old male CEO looking toward a 38-year-old female executive in a charcoal blazer. She responds to something with a completely flat, unimpressed deadpan expression — a slight head tilt is her only reaction. Her voice is measured and professionally savage. She holds a tablet at her side. Shallow depth of field. 6 seconds. [PASTE STYLE ANCHOR HERE]
```

### 🔊 AUDIO PROMPT
```
Measured, crisp British professional female voice. Deadpan delivery of a dry, quietly savage line. Office ambient barely audible.
```

### 🎭 CONTINUITY
- Christina: Charcoal blazer, composed, no emotional tell

### ✅ GATE CHECK — Before Moving to S04, Verify:
- [ ] Christina reads as deadpan — NOT smiling, NOT angry
- [ ] Two-shot depth feels natural — Jan's shoulder visible

---

## 🎥 S04 — Jan Stress Build CU
**Duration**: 5 seconds | **Shot Type**: CU (Close-Up) on Jan's face  
**Beat**: Jan is getting flustered. Face beginning to redden. Shirt collar being loosened.

### 📎 Attach These Images (2 Max)
| # | File | Role | Full Path |
|---|------|------|-----------|
| 1 | `IMG_20260804_131855397.jpg` | **Env Plate** — Blurred office behind | `C:\ai\Circle the Square\building-reference\use-images\IMG_20260804_131855397.jpg` |
| 2 | `jan_peach_identity_sheet.jpg` | **Character** — Jan, early stress state, reddening | `C:\ai\Circle the Square\character-refs\jan_peach_identity_sheet.jpg` |

### 🎬 VIDEO PROMPT
```
A tight close-up on the face of a 52-year-old overweight male CEO. His face is beginning to flush red at the cheeks and neck. He loosens his shirt collar with one finger. A thin film of sweat is starting to appear on his forehead. He is speaking through increasingly gritted teeth, trying to maintain authority but visibly losing it. Very shallow depth of field. 5 seconds. [PASTE STYLE ANCHOR HERE]
```

### 🔊 AUDIO PROMPT
```
CEO voice rising in pitch. Breathing slightly audible. A shirt collar rustle sound.
```

### 🎭 CONTINUITY
- Jan: **Shirt unbuttoning begins** — collar open, tie loosened. Face 30% red, sweat starting.

### ✅ GATE CHECK — Before Moving to S05, Verify:
- [ ] Clear visible transition from "smug" to "stressed" in face colour
- [ ] Shirt collar open/loosening — continuity bridge to S05

---

## 🎥 S05 — Jan Shirtless, Manscaped Arrow Reveal
**Duration**: 8 seconds | **Shot Type**: WIDE — dramatic reveal  
**Beat**: Jan removes shirt entirely. Manscaped chest arrow visible. Sharon walks in. Chaos.

### 📎 Attach These Images (3 Max)
| # | File | Role | Full Path |
|---|------|------|-----------|
| 1 | `IMG_20260804_131855397.jpg` | **Env Plate** — Office backdrop | `C:\ai\Circle the Square\building-reference\use-images\IMG_20260804_131855397.jpg` |
| 2 | `jan_peach_identity_sheet.jpg` | **Character A** — Jan, shirt off | `C:\ai\Circle the Square\character-refs\jan_peach_identity_sheet.jpg` |
| 3 | `sharon_enfield_identity_sheet.jpg` | **Character B** — Sharon State A: composed, emerald blouse | `C:\ai\Circle the Square\character-refs\sharon_enfield_identity_sheet.jpg` |

### 🎬 VIDEO PROMPT
```
A wide shot in a modern corporate glass-walled office. A flustered, sweating 52-year-old overweight male CEO has just removed his white dress shirt. His chest and stomach hair has been carefully shaved and styled into a large downward-pointing arrow toward his waistband. At that exact moment the glass office door opens and a 34-year-old curvy woman in a fitted emerald jewel-tone blouse enters the room without knocking. She looks at him. Her eyes travel briefly downward to the arrow. Her expression remains completely neutral and unbothered. The CEO freezes in horror and immediately begins scrambling to close the window blinds. 8 seconds. [PASTE STYLE ANCHOR HERE]
```

### 🔊 AUDIO PROMPT
```
CEO mid-sentence stops dead. Brief shocked silence. Venetian blind motor hum begins. No music. Documentary dry.
```

### 🎭 CONTINUITY
- Jan: **Shirt fully OFF**. Chest visible. Deeply flushed.
- Sharon: **State A** (composed) — this is her arrival state

### ✅ GATE CHECK — Before Moving to S06, Verify:
- [ ] Manscaped arrow is clearly visible and reads as intentional comedy
- [ ] Sharon's expression is **neutral** — NOT shocked, NOT laughing
- [ ] This is the comedy peak of Scene 1 — needs to land visually

---

## 🎥 S06 — Sharon's Unbothered MCU Reaction
**Duration**: 4 seconds | **Shot Type**: MCU on Sharon  
**Beat**: Sharon glances down, glances back up, completely unbothered. States what she wants.

### 📎 Attach These Images (2 Max)
| # | File | Role | Full Path |
|---|------|------|-----------|
| 1 | `IMG_20260804_131855397.jpg` | **Env Plate** — Office backdrop | `C:\ai\Circle the Square\building-reference\use-images\IMG_20260804_131855397.jpg` |
| 2 | `sharon_enfield_identity_sheet.jpg` | **Character** — Sharon, neutral unbothered expression | `C:\ai\Circle the Square\character-refs\sharon_enfield_identity_sheet.jpg` |

### 🎬 VIDEO PROMPT
```
A medium close-up on a 34-year-old curvy woman in a fitted emerald jewel-tone blouse. She glances briefly downward off-frame, then back up to face-level. Her expression does not change — completely flat, transactional, unbothered. She begins speaking matter-of-factly as if nothing unusual has happened. 4 seconds. [PASTE STYLE ANCHOR HERE]
```

### 🔊 AUDIO PROMPT
```
Warm confident British female voice — blunt, transactional, completely unruffled. States what she wants plainly.
```

### 🎭 CONTINUITY
- Sharon: **State A** (composed, emerald blouse buttoned, hair tidy)

### ✅ GATE CHECK — Before Moving to S07, Verify:
- [ ] Sharon reads as genuinely, comically unbothered — not nervous
- [ ] Emerald blouse reads as composed/professional — no dishevelment yet

---

## 🎥 S07 — Jan Locks Blinds MCU
**Duration**: 5 seconds | **Shot Type**: MCU Jan at window  
**Beat**: Jan yanks the blinds shut and locks the office door.

### 📎 Attach These Images (2 Max)
| # | File | Role | Full Path |
|---|------|------|-----------|
| 1 | `IMG_20260804_131855397.jpg` | **Env Plate** — Office backdrop | `C:\ai\Circle the Square\building-reference\use-images\IMG_20260804_131855397.jpg` |
| 2 | `jan_peach_identity_sheet.jpg` | **Character** — Jan, shirtless, panicked | `C:\ai\Circle the Square\character-refs\jan_peach_identity_sheet.jpg` |

### 🎬 VIDEO PROMPT
```
A medium close-up of a shirtless, sweating, deeply red-faced 52-year-old overweight man at a glass office window. He yanks down venetian blinds with both hands with panicked urgency. He then turns sharply and reaches to the door handle and clicks a lock. His breathing is heavy and audible. His expression is somewhere between mortified and resigned. 5 seconds. [PASTE STYLE ANCHOR HERE]
```

### 🔊 AUDIO PROMPT
```
Venetian blind mechanical slam-drop. Door lock click. CEO heavy breathing. No music. Complete office ambient silence outside.
```

### 🎭 CONTINUITY
- Jan: **Shirt still off**, deeply flushed, sweaty

### ✅ GATE CHECK — Before Moving to S08, Verify:
- [ ] Blinds close action reads clearly
- [ ] Jan is visibly shirtless — continuity from S05
- [ ] Scene transition is implied — blinds down = cut to corridor

---

---

# SCENE 2 — INT. CORRIDOR / OPEN-PLAN FLOOR — CONTINUOUS

---

## 🎥 S08 — Corridor Tracking: Sharon Exits Dishevelled
**Duration**: 8 seconds | **Shot Type**: WIDE TRACKING — corridor  
**Beat**: Sharon walks past Chris & Rick, dishevelled, heels in hand, completely unbothered.

### 📎 Attach These Images (2 Max)
| # | File | Role | Full Path |
|---|------|------|-----------|
| 1 | `P20.jpg` | **Env Plate** — Open-plan central aisle, corridor perspective | `C:\ai\Circle the Square\building-reference\use-images\P20.jpg` |
| 2 | `sharon_enfield_identity_sheet.jpg` | **Character** — Sharon, **State B** (dishevelled) | `C:\ai\Circle the Square\character-refs\sharon_enfield_identity_sheet.jpg` |

### 🎬 VIDEO PROMPT
```
A wide tracking shot down a modern open-plan corporate office corridor. A 34-year-old woman in a fitted emerald jewel-tone blouse walks past camera — her hair is visibly mussed, lipstick slightly smudged, blouse untucked at one side. She carries her heels in one hand and walks with complete unhurried confidence. Two male office workers lean against a nearby desk watching her pass — a lean 32-year-old in a light blue shirt with a deadpan smirk, and a stocky 40-year-old in a grey polo shirt with arms crossed and a flat expression. 8 seconds. [PASTE STYLE ANCHOR HERE]
```

### 🔊 AUDIO PROMPT
```
Office ambient hum. Faint distant printer. Sharon's flat footsteps on carpet — unhurried. No music.
```

### 🎭 CONTINUITY
- Sharon: **State B** — hair mussed, blouse untucked, heels in hand
- Chris & Rick: First appearance together — light blue shirt / grey polo

### ✅ GATE CHECK — Before Moving to S09, Verify:
- [ ] Sharon's dishevelment reads clearly — this is the visual joke
- [ ] Her expression is **unbothered** — critical comedy beat
- [ ] Chris & Rick visible in background watching

---

## 🎥 S09 — 2-Shot Chris & Rick Dry Exchange
**Duration**: 6 seconds | **Shot Type**: 2-SHOT MCU  
**Beat**: Chris and Rick exchange a look. Chris delivers a dry line.

### 📎 Attach These Images (2 Max)
| # | File | Role | Full Path |
|---|------|------|-----------|
| 1 | `P12.jpg` | **Env Plate** — Office desk rows, triangle screens | `C:\ai\Circle the Square\building-reference\use-images\P12.jpg` |
| 2 | `chris_identity_sheet.jpg` | **Character A** — Chris, smirking | `C:\ai\Circle the Square\character-refs\chris_identity_sheet.jpg` |

### 🎬 VIDEO PROMPT
```
A medium two-shot of two male office workers leaning against a desk in a modern open-plan office with white desk rows and hanging geometric triangle acoustic felt ceiling panels. A lean 32-year-old in a light blue shirt with sleeves rolled up delivers a dry, deadpan comment to camera with a barely-suppressed smirk. A stocky 40-year-old in a grey polo shirt with arms crossed responds flatly, completely unsurprised. They both look off-frame where Sharon just walked. 6 seconds. [PASTE STYLE ANCHOR HERE]
```

### 🔊 AUDIO PROMPT
```
Chris voice — dry, quick, South London baritone: "Christ! They don't even try to hide it anymore do they." Rick voice — flat, blunt, deep monotone: "Never have. Give it another five minutes." Low office ambient.
```

### 🎭 CONTINUITY
- Chris: Light blue shirt, sleeves rolled, deadpan smirk
- Rick: Grey polo, arms crossed, zero expression

### ✅ GATE CHECK — Before Moving to S10, Verify:
- [ ] Chris and Rick are visually distinct — different builds, colours
- [ ] Office background has hanging triangle baffles visible (key visual)
- [ ] Neither looks shocked — they've seen this before

---

## 🎥 S10 — Jan Claps, Announces Project Inception (Wide)
**Duration**: 8 seconds | **Shot Type**: HIGH ANGLE WIDE  
**Beat**: Jan re-enters, shirt re-buttoned askew, claps hands loudly to gather crowd.

### 📎 Attach These Images (3 Max)
| # | File | Role | Full Path |
|---|------|------|-----------|
| 1 | `P12.jpg` | **Env Plate** — Open-plan office desk rows & triangle screens | `C:\ai\Circle the Square\building-reference\use-images\P12.jpg` |
| 2 | `jan_peach_identity_sheet.jpg` | **Character A** — Jan, shirt re-buttoned askew, sweaty | `C:\ai\Circle the Square\character-refs\jan_peach_identity_sheet.jpg` |
| 3 | `rick_identity_sheet.jpg` | **Character B** — Rick in crowd | `C:\ai\Circle the Square\character-refs\rick_identity_sheet.jpg` |

### 🎬 VIDEO PROMPT
```
A high-angle wide shot of a modern open-plan corporate office floor. A 52-year-old overweight CEO in a dark navy suit (shirt re-buttoned visibly askew, collar crooked, still sweating) enters from one side and claps his hands loudly and repeatedly to summon the surrounding office workers. Workers at desks stop typing and reluctantly turn in their chairs or stand and drift toward him. The CEO plants himself in the central aisle between two desk rows with his hands on his hips, chest puffed out. Geometric triangle felt acoustic baffles hang from the ceiling above. 8 seconds. [PASTE STYLE ANCHOR HERE]
```

### 🔊 AUDIO PROMPT
```
Loud double hand-clap echoes in the office. Keyboard typing stops. Chairs scraping. Reluctant footsteps gathering. CEO voice rising: "Right guys, as you know—"
```

### 🎭 CONTINUITY
- Jan: **Shirt re-buttoned askew** — visible continuity from S07. Still sweaty. Face 50% red.

### ✅ GATE CHECK — Before Moving to S11, Verify:
- [ ] Shirt mis-buttoning is visible — key comedy continuity detail
- [ ] Office crowd gathering reads as reluctant/unenthusiastic
- [ ] Triangle ceiling baffles visible — establishes office environment

---

## 🎥 S11 — Jan MCU: Project Inception & £50k
**Duration**: 8 seconds | **Shot Type**: MCU push-in on Jan  
**Beat**: Jan announces he has named himself Project Inception lead and it comes with £50k on his salary.

### 📎 Attach These Images (2 Max)
| # | File | Role | Full Path |
|---|------|------|-----------|
| 1 | `P12.jpg` | **Env Plate** — Office, blurred crowd behind | `C:\ai\Circle the Square\building-reference\use-images\P12.jpg` |
| 2 | `jan_peach_identity_sheet.jpg` | **Character** — Jan, stress state, shirt askew | `C:\ai\Circle the Square\character-refs\jan_peach_identity_sheet.jpg` |

### 🎬 VIDEO PROMPT
```
A medium close-up with a slight push-in on a 52-year-old overweight CEO in a mis-buttoned dark navy suit shirt. He announces with complete self-satisfaction that the position of Project Lead has been filled — by himself — and that this will add £50,000 to his annual salary. His expression is a bizarre mix of smugness and defensive bluster — chin up, eyes scanning for dissent. Blurred office workers visible behind him. 8 seconds. [PASTE STYLE ANCHOR HERE]
```

### 🔊 AUDIO PROMPT
```
Pompous CEO voice peaks in self-satisfaction: "...the position has already been filled... by me." Pause. Then a wave of audible groans from surrounding workers.
```

### 🎭 CONTINUITY
- Jan: Shirt askew, sweaty, neck veins just visible at collar

### ✅ GATE CHECK — Before Moving to S12, Verify:
- [ ] Jan's self-satisfaction reads as genuinely deluded — not villainous
- [ ] Shirt mis-buttoning still visible

---

## 🎥 S12 — Crowd Reaction Cuts
**Duration**: 6 seconds | **Shot Type**: QUICK REACTION CUTS (3 × 2 second cuts)  
**Beat**: Eye-rolls, suppressed laughter, exasperated looks from assembled workers.

### 📎 Attach These Images (2 Max)
| # | File | Role | Full Path |
|---|------|------|-----------|
| 1 | `P12.jpg` | **Env Plate** — Office desk rows, workers assembled | `C:\ai\Circle the Square\building-reference\use-images\P12.jpg` |
| 2 | `chris_identity_sheet.jpg` | **Character** — Chris, barely containing amusement | `C:\ai\Circle the Square\character-refs\chris_identity_sheet.jpg` |

### 🎬 VIDEO PROMPT
```
Three rapid reaction cuts in a modern open-plan office. First cut: a lean 32-year-old in a light blue shirt with a barely-suppressed amused smirk. Second cut: a group of two or three anonymous office workers exchanging disbelieving glances. Third cut: a stocky 40-year-old in a grey polo shirt with arms crossed, giving a completely flat, unsurprised stare to camera. Each cut is approximately 2 seconds. Shallow depth of field on each. Documentary handheld style. 6 seconds total. [PASTE STYLE ANCHOR HERE]
```

### 🔊 AUDIO PROMPT
```
A ripple of low groans and suppressed sighs from the office crowd. Chris voice — shouted to general laughter: "You're dreaming Jan!" Beat. Jan voice rising: "What?!" Chris: "Inception is the name of a film about dreams, Jan."
```

### ✅ GATE CHECK — Before Moving to S13, Verify:
- [ ] Chris is recognisable from S09 — same shirt, same smirk
- [ ] Rick is recognisable — same grey polo, same flat stare
- [ ] Reactions feel authentic not pantomime

---

---

# SCENE 3 — INT. STAFF RESTAURANT / CANTEEN — NEXT MORNING

---

## 🎥 S13 — Canteen Establishing Wide
**Duration**: 6 seconds | **Shot Type**: WIDE LOCKED-OFF  
**Beat**: Morning canteen, pastries, workers eating — Jan is not here yet. Tray is empty.

### 📎 Attach These Images (2 Max)
| # | File | Role | Full Path |
|---|------|------|-----------|
| 1 | `ep_tri_372-c-raftery-lowe-resized.jpg` | **Env Plate** — Atrium/canteen space, concrete columns, large glazing | `C:\ai\Circle the Square\building-reference\use-images\ep_tri_372-c-raftery-lowe-resized.jpg` |
| 2 | `jan_peach_identity_sheet.jpg` | **Character** — Jan (NOT YET PRESENT — for ref continuity only) | `C:\ai\Circle the Square\character-refs\jan_peach_identity_sheet.jpg` |

### 🎬 VIDEO PROMPT
```
A wide locked-off establishing shot of a modern corporate staff canteen / restaurant set within a bright, large-windowed contemporary building interior with grey concrete columns. Morning light fills the space. Office workers in casual business attire sit at canteen tables eating pain au chocolat pastries. A canteen counter is visible to one side with a serving tray — the tray is now visibly empty, crumbs remaining. A canteen worker in a beige apron stands behind the counter. The CEO has not yet arrived. 6 seconds. [PASTE STYLE ANCHOR HERE]
```

### 🔊 AUDIO PROMPT
```
Morning canteen ambient — low cheerful background chatter, cutlery clinking, a coffee machine grinding. Warm and normal. No tension yet.
```

### ✅ GATE CHECK — Before Moving to S14, Verify:
- [ ] Canteen feels distinct from the office — different space, different furniture
- [ ] Empty pastry tray is clearly visible — plot-critical prop
- [ ] Canteen worker in beige apron is identifiable behind counter

---

## 🎥 S14 — Jan Arrives, Discovers Empty Tray
**Duration**: 8 seconds | **Shot Type**: HANDHELD MCU — tracks Jan to counter  
**Beat**: Jan strides in confidently, reaches counter, stares at empty tray. Face begins to change.

### 📎 Attach These Images (2 Max)
| # | File | Role | Full Path |
|---|------|------|-----------|
| 1 | `ep_tri_372-c-raftery-lowe-resized.jpg` | **Env Plate** — Canteen space | `C:\ai\Circle the Square\building-reference\use-images\ep_tri_372-c-raftery-lowe-resized.jpg` |
| 2 | `jan_peach_identity_sheet.jpg` | **Character** — Jan, early extreme stress state | `C:\ai\Circle the Square\character-refs\jan_peach_identity_sheet.jpg` |

### 🎬 VIDEO PROMPT
```
A handheld tracking shot following a 52-year-old overweight CEO in a dark navy suit as he strides purposefully into a corporate canteen. He reaches the serving counter and looks down at the pastry tray — which is completely empty, only crumbs remaining. He looks up at the canteen worker behind the counter with an expression of disbelief beginning to tip into rage. His face begins to flush deep red. A vein in his neck becomes visible. 8 seconds. [PASTE STYLE ANCHOR HERE]
```

### 🔊 AUDIO PROMPT
```
Confident CEO footsteps. Canteen ambient. Jan's voice — dangerously controlled: "Is there any more pain au chocolat?" Canteen worker voice — apologetic: "Sorry, all gone." Beat. Jan's breathing audibly deepens.
```

### 🎭 CONTINUITY
- Jan: **Full suit on**, sweating slightly. Rage building from 0%.

### ✅ GATE CHECK — Before Moving to S15, Verify:
- [ ] Jan's face transition from confident → disbelief → rage beginning reads clearly
- [ ] Empty tray is clearly visible — camera must show it

---

## 🎥 S15 — Jan Full Canteen Meltdown: Plates & Chair
**Duration**: 10 seconds | **Shot Type**: WIDE STATIC — action unfolds  
**Beat**: Jan explodes. Sweeps plates to floor. Screams about MBA. Hurls chair through window.

### 📎 Attach These Images (3 Max)
| # | File | Role | Full Path |
|---|------|------|-----------|
| 1 | `ep_tri_372-c-raftery-lowe-resized.jpg` | **Env Plate** — Canteen space with large windows | `C:\ai\Circle the Square\building-reference\use-images\ep_tri_372-c-raftery-lowe-resized.jpg` |
| 2 | `jan_peach_identity_sheet.jpg` | **Character** — Jan, extreme rage/meltdown state | `C:\ai\Circle the Square\character-refs\jan_peach_identity_sheet.jpg` |
| 3 | `rick_identity_sheet.jpg` | **Character B** — Rick visible in background crowd watching | `C:\ai\Circle the Square\character-refs\rick_identity_sheet.jpg` |

### 🎬 VIDEO PROMPT
```
A wide static shot of a corporate canteen. A 52-year-old overweight CEO in a dark navy suit, face a deep furious crimson with visible neck veins and heavy sweat, suddenly screams at full volume. He grabs the plates from the canteen counter with both hands and sweeps them violently onto the hard floor — a massive crash of shattering china. The entire canteen falls silent, everyone frozen, staring. He grabs a heavy corporate meeting chair from a nearby table, raises it above his head with effort, and hurls it directly into the nearest large floor-to-ceiling window. The glass shatters. He reaches for a second chair. Stunned canteen workers visible in background. A stocky 40-year-old man in a grey polo shirt is visible at the back of the crowd, quietly and calmly stepping forward. 10 seconds. [PASTE STYLE ANCHOR HERE]
```

### 🔊 AUDIO PROMPT
```
CEO erupts — screaming incoherent rage about his MBA. MASSIVE CRASH of china plates shattering on hard floor. Dead silence from crowd. Chair scraping table legs. A huge GLASS SHATTER impact. Ringing silence.
```

### 🎭 CONTINUITY
- Jan: **Full rage state** — deep crimson, neck veins, sweat-soaked shirt, jacket still on but dishevelled
- Rick: Visible in background — calmly stepping forward

### ✅ GATE CHECK — Before Moving to S16, Verify:
- [ ] The plate smash reads as shocking — this is the physical comedy climax
- [ ] Chair-through-window is clearly depicted
- [ ] Rick calmly stepping forward is visible in background

---

## 🎥 S16 — Rick Draws Taser (Low MCU)
**Duration**: 5 seconds | **Shot Type**: LOW ANGLE MCU on Rick  
**Beat**: Rick raises prop taser with the calm energy of a man who has been waiting for this moment.

### 📎 Attach These Images (2 Max)
| # | File | Role | Full Path |
|---|------|------|-----------|
| 1 | `ep_tri_372-c-raftery-lowe-resized.jpg` | **Env Plate** — Canteen, slightly blurred | `C:\ai\Circle the Square\building-reference\use-images\ep_tri_372-c-raftery-lowe-resized.jpg` |
| 2 | `rick_identity_sheet.jpg` | **Character** — Rick, calm, taser raised | `C:\ai\Circle the Square\character-refs\rick_identity_sheet.jpg` |

### 🎬 VIDEO PROMPT
```
A low-angle medium close-up on a stocky 40-year-old man in a grey polo shirt. With complete calm and no hurry, he reaches into his pocket and produces a small prop taser device — visibly toy-like and non-functional in appearance. He raises it deliberately toward something off-camera to his left. His expression does not change — flat, composed, entirely unsurprised. This is a man who has been waiting for this moment for years. 5 seconds. [PASTE STYLE ANCHOR HERE]
```

### 🔊 AUDIO PROMPT
```
Complete canteen silence except for Jan raging off-camera. A quiet, deliberate click as Rick arms the prop device. No music.
```

### 🎭 CONTINUITY
- Rick: Grey polo, arms steady, taser prop clearly looks fake/toy-like

### ✅ GATE CHECK — Before Moving to S17, Verify:
- [ ] Taser prop reads as **clearly non-functional/toy-like** — must NOT look like a real weapon
- [ ] Rick's expression is **flat calm** — NOT heroic, NOT angry, just matter-of-fact

---

## 🎥 S17 — INSERT: Taser Flash
**Duration**: 3 seconds | **Shot Type**: INSERT — extreme close-up  
**Beat**: POP-CRACKLE. Blue-white electric arc flash from prop taser.

### 📎 Attach These Images (1 Max)
| # | File | Role | Full Path |
|---|------|------|-----------|
| 1 | `ep_tri_372-c-raftery-lowe-resized.jpg` | **Env context only** | `C:\ai\Circle the Square\building-reference\use-images\ep_tri_372-c-raftery-lowe-resized.jpg` |

### 🎬 VIDEO PROMPT
```
An extreme close-up insert shot of a small toy-like prop taser device firing. A brief blue-white electric arc crackle flashes from the tip for approximately 2 seconds. The device reads as clearly fake/prop quality — not a real weapon. The flash illuminates the surrounding air. Cut to black. 3 seconds. [PASTE STYLE ANCHOR HERE]
```

### 🔊 AUDIO PROMPT
```
A sharp loud POP-CRACKLE electric discharge sound. Immediate dead silence after.
```

### ✅ GATE CHECK — Before Moving to S18, Verify:
- [ ] Electric arc is clearly a prop effect — comedic not threatening
- [ ] Short and punchy — 3 seconds max

---

## 🎥 S18 — Jan Slumps Face-Down
**Duration**: 5 seconds | **Shot Type**: WIDE  
**Beat**: Jan freezes mid-reach, drops the chair, slumps face-first onto the canteen floor unconscious.

### 📎 Attach These Images (2 Max)
| # | File | Role | Full Path |
|---|------|------|-----------|
| 1 | `ep_tri_372-c-raftery-lowe-resized.jpg` | **Env Plate** — Canteen floor space | `C:\ai\Circle the Square\building-reference\use-images\ep_tri_372-c-raftery-lowe-resized.jpg` |
| 2 | `jan_peach_identity_sheet.jpg` | **Character** — Jan, unconscious face-down final state | `C:\ai\Circle the Square\character-refs\jan_peach_identity_sheet.jpg` |

### 🎬 VIDEO PROMPT
```
A wide shot. A 52-year-old overweight CEO in a dark navy suit suddenly freezes mid-motion — arms dropping, body going limp — and falls heavily forward, landing face-first on the hard canteen floor with a loud thud. He lies completely motionless, one arm splayed to the side, jacket rucked up, surrounded by shattered china on the floor. The canteen is completely silent. Everyone stares. The cracked window is visible in background. 5 seconds. [PASTE STYLE ANCHOR HERE]
```

### 🔊 AUDIO PROMPT
```
A single heavy body-slump THUD on a hard floor. Broken china pieces settling. Then absolute complete silence. Not even ambient hum.
```

### 🎭 CONTINUITY
- Jan: Face-down, unconscious, splayed arm — matches character sheet "final state" reference note

### ✅ GATE CHECK — Before Moving to S19, Verify:
- [ ] Fall reads as sudden and physical — not slow or graceful
- [ ] Jan is clearly face-down and motionless
- [ ] Broken china on floor is visible — continuity from S15

---

## 🎥 S19 — Chris & Rick Aftermath 2-Shot (FINAL SHOT)
**Duration**: 8 seconds | **Shot Type**: 2-SHOT MCU — Chris crouching, Rick standing  
**Beat**: Chris crouches beside the unconscious Jan. Looks up at Rick. Delivers the line.

### 📎 Attach These Images (3 Max)
| # | File | Role | Full Path |
|---|------|------|-----------|
| 1 | `ep_tri_372-c-raftery-lowe-resized.jpg` | **Env Plate** — Canteen, broken glass bg | `C:\ai\Circle the Square\building-reference\use-images\ep_tri_372-c-raftery-lowe-resized.jpg` |
| 2 | `chris_identity_sheet.jpg` | **Character A** — Chris crouching, concerned-amused | `C:\ai\Circle the Square\character-refs\chris_identity_sheet.jpg` |
| 3 | `rick_identity_sheet.jpg` | **Character B** — Rick standing calmly, taser being pocketed | `C:\ai\Circle the Square\character-refs\rick_identity_sheet.jpg` |

### 🎬 VIDEO PROMPT
```
A medium two-shot in a wrecked corporate canteen. A lean 32-year-old in a light blue shirt is crouched down next to an unconscious overweight man lying face-down on the floor surrounded by broken china. He looks up at a stocky 40-year-old in a grey polo shirt who is calmly and methodically sliding a small prop taser back into his trouser pocket. The 32-year-old's expression is somewhere between concerned and amused. The 40-year-old's expression is completely flat and calm. Behind them: shattered window, overturned chairs, stunned canteen workers in the background. 8 seconds. [PASTE STYLE ANCHOR HERE]
```

### 🔊 AUDIO PROMPT
```
Complete silence. Then Chris voice — quiet, crouching: "Have you killed him?" Rick voice — calm, methodical, pocketing taser: "No relax, he will be out for a while. I knew this Taser would come in useful one day in this place. I think we need the police here..." Fade ambient.
```

### 🎭 CONTINUITY
- Chris: Light blue shirt — same as all prior appearances ✅
- Rick: Grey polo — same as all prior appearances ✅
- Jan: Unconscious face-down visible at bottom of frame

### ✅ GATE CHECK — This is the FINAL SHOT. Before approving full episode cut, verify:
- [ ] Chris's expression lands the comedy — not pure horror, not pure amusement — the mix
- [ ] Rick's flat calm delivery is the final punchline
- [ ] Jan's unconscious form is visible in foreground/frame
- [ ] Broken china, cracked window — visual mess matches S15-S18 continuity

---

## ✂️ POST-PRODUCTION ASSEMBLY ORDER

```
S01 → S02 → S03 → S04 → S05 → S06 → S07
    [SCENE 1 COMPLETE — cut on blinds snapping]
S08 → S09
    [SCENE 2A COMPLETE — cut on Jan entering]
S10 → S11 → S12
    [SCENE 2B COMPLETE — TIME CUT CARD: "NEXT MORNING"]
S13 → S14 → S15 → S16 → S17 → S18 → S19
    [SCENE 3 COMPLETE — FADE TO BLACK]
    [TITLE CARD: CIRCLE THE SQUARE / ALL UNDER ONE ROOF]
```

---

## 🎙️ DIALOGUE DUB ORDER (Qwen3-TTS)

| Scene | Character | Key Line | Audio File |
|-------|-----------|----------|-----------|
| S01–S03 | Jan | "I am liking the idea of this so far..." | `jan_qwen_custom.wav` |
| S02–S03 | Christina | "Friday statistically is the least productive day..." | `christina_qwen_custom.wav` |
| S05–S06 | Sharon | "I hear Christina is doing breakfast meetings now." | `sharon_qwen_custom.wav` |
| S10–S12 | Jan | "The position has already been filled... by me." | `jan_qwen_custom.wav` |
| S09 | Chris | "Christ! They don't even try to hide it anymore do they." | `chris_qwen_custom.wav` |
| S09 | Rick | "Never have. Give it another five minutes." | `rick_qwen_custom.wav` |
| S12 | Chris | "You're dreaming Jan!" | `chris_qwen_custom.wav` |
| S14 | Jan | "OH THAT IS IT!" (screaming) | `jan_qwen_custom.wav` |
| S19 | Chris | "Have you killed him?" | `chris_qwen_custom.wav` |
| S19 | Rick | "No relax, he will be out for a while..." | `rick_qwen_custom.wav` |

**TTS Prompts JSON**: `C:\ai\Circle the Square\qwen3_tts_voice_prompts.json`

---

## 📁 Full Asset Reference Index

| Asset | Full UNC Path |
|-------|--------------|
| Fountain Screenplay | `C:\ai\Circle the Square\CTS_Featurette_Episode.fountain` |
| Scene Shot List | `C:\ai\Circle the Square\featurette_shot_list.md` |
| Building Refs | `C:\ai\Circle the Square\building-reference\use-images\` |
| Character Sheets | `C:\ai\Circle the Square\character-refs\` |
| Location Sheets | `C:\ai\Circle the Square\location-refs\` |
| Audio Voice Refs | `C:\ai\Circle the Square\audio-refs\` |
| TTS Prompts JSON | `C:\ai\Circle the Square\qwen3_tts_voice_prompts.json` |
| Master Production Manual | `C:\ai\Circle the Square\MASTER_PRODUCTION_MANUAL.md` |
