# 🎬 CIRCLE THE SQUARE — MASTER PRODUCTION & PRE-VISUALIZATION MANUAL

> 🎨 **VISUAL STYLE: CARTOON.** Stylised British sitcom comic art — **not photoreal.**
> Style anchor and full cast specs in **`CARTOON_CAST_BIBLE.md`**.
> **Deliverable: an animated cartoon video**, not a comic-strip slideshow.
> Photoreal was abandoned on 2026-08-10 after Google Flow blocked photoreal Jan Peach three times
> (likeness protection on a real face). Do not go back — see `HANDOVER.md` §2.

> **LOCKED PRODUCTION SPECIFICATION**  
> **Project**: *Circle the Square*  
> **Episode**: "Project Inception" (Featurette Episode)  
> **Company in-fiction**: **PRISM** — every lanyard, nameplate, mug and sign reads PRISM, never Peach Corp  
> **Primary Accent Color**: Burnt Orange (`#B0381F`)  
> **Genre & Tone**: Contemporary British Workplace Mockumentary / Corporate Satire  
> **Location**: The Triangle, **Cambridge** — low-rise, **not London**  

---

## 1. 📌 WORKSPACE & SYSTEM RULES MEMORY

All AI agents, scripts, and future sessions are locked to the following permanent workspace rules:

1. 💳 **Google AI Pro Subscription Preference (£0 API Fees)**:
   * The user exclusively uses their **£18.99/month Google AI Pro Subscription**.
   * Do NOT execute paid per-token API scripts (`gen_image.py`, `gen_video.py`) that incur pay-as-you-go Cloud API billing charges.
   * All media generation, model sheet creation, storyboarding, and script analysis are performed directly inside the AI assistant chat environment under the subscription.
2. 📁 **Render Path & Filename Output**:
   * Every time a render or media asset finishes, the assistant and scripts MUST explicitly list both the **Filename** AND the **Full Absolute Pathname** formatted as a clickable markdown file link (`file:///C:/path/to/file`).
3. ⏱️ **Paced Batch Generation Rule**:
   * NEVER generate large sets of images rapidly back-to-back in big bursts.
   * ALWAYS generate images in small focused groups of **2 to 3 images per batch** with short pauses so rate limits and quota triggers are NEVER encountered.

---

## 2. 🎭 MASTER CARTOON CHARACTER SHEET ROSTER

> 🎨 **CARTOON.** Full specs for every character in **`CARTOON_CAST_BIBLE.md`** — that is the cast source of truth.
> One sheet per character (four-view turnaround: front, three-quarter, side, back).

All character reference assets are stored in:  
📁 **[`C:\kontitemp\AI\circle_the_square\character-refs\`](file:///C:/kontitemp/AI/circle_the_square/character-refs/)**

### Principals — voices attached in Flow

| Character | Role | Cartoon Sheet | Voice |
| :--- | :--- | :--- | :--- |
| **Jan Peach** | CEO | [`jan_peach_cartoon_sheet.jpg`](file:///C:/kontitemp/AI/circle_the_square/character-refs/jan_peach_cartoon_sheet.jpg) | ✅ British RP, "boardroom" |
| **Christina Dross** | Comms Lead | [`christina_dross_cartoon_sheet.jpg`](file:///C:/kontitemp/AI/circle_the_square/character-refs/christina_dross_cartoon_sheet.jpg) | ✅ Clear British London RP |
| **Sharon Enfield** | Staff | [`sharon_enfield_cartoon_sheet.jpg`](file:///C:/kontitemp/AI/circle_the_square/character-refs/sharon_enfield_cartoon_sheet.jpg) | ✅ Welsh, subtle lilt |
| **Chris** | Staff | [`chris_cartoon_sheet.jpg`](file:///C:/kontitemp/AI/circle_the_square/character-refs/chris_cartoon_sheet.jpg) | ✅ Dry South London Estuary |
| **Rick** | Staff | [`rick_cartoon_sheet.jpg`](file:///C:/kontitemp/AI/circle_the_square/character-refs/rick_cartoon_sheet.jpg) | ✅ Flat Midlands / East Anglian |

> The five voices **already existed in Flow** and match the bible exactly. **Do not create new ones** — select the existing ones.

### Supporting

| Character | Role | Cartoon Sheet | Appears |
| :--- | :--- | :--- | :--- |
| **Maureen** | Canteen worker | [`maureen_canteen_cartoon_sheet.jpg`](file:///C:/kontitemp/AI/circle_the_square/character-refs/maureen_canteen_cartoon_sheet.jpg) | F47, F48, F51 |
| **Gemma Ashcroft** | Receptionist | [`gemma_ashcroft_cartoon_sheet.jpg`](file:///C:/kontitemp/AI/circle_the_square/character-refs/gemma_ashcroft_cartoon_sheet.jpg) | Reception atrium |
| **Priya Raghavan** | Office staff | [`priya_raghavan_cartoon_sheet.jpg`](file:///C:/kontitemp/AI/circle_the_square/character-refs/priya_raghavan_cartoon_sheet.jpg) | Background |
| **Barbara Whitlock** | Senior administrator | [`barbara_whitlock_cartoon_sheet.jpg`](file:///C:/kontitemp/AI/circle_the_square/character-refs/barbara_whitlock_cartoon_sheet.jpg) | Background |
| **Dev Osei** | Junior data analyst | [`dev_osei_cartoon_sheet.jpg`](file:///C:/kontitemp/AI/circle_the_square/character-refs/dev_osei_cartoon_sheet.jpg) | Background |
| **Tomasz Wojcik** | Facilities & maintenance | [`tomasz_wojcik_cartoon_sheet.jpg`](file:///C:/kontitemp/AI/circle_the_square/character-refs/tomasz_wojcik_cartoon_sheet.jpg) | Background |

### ⛔ Retired — photoreal archive

The 10 photoreal sheets in [`character-refs/_photoreal-archive/`](file:///C:/kontitemp/AI/circle_the_square/character-refs/_photoreal-archive/)
are kept **as written spec only**. Google Flow blocked photoreal Jan Peach on three separate attempts —
likeness protection on a real face, not content policy. **Do not use them as generation references.**
See `HANDOVER.md` §2.

---

## 3. 🏛️ MASTER LOCATION SPEC SHEET ROSTER

> ⚠️ **These are photoreal-era sheets.** Cartoon replacements are the live task — the plan and prompts
> live in **`LOCATION_PLATE_SHOT_LIST.md`** (12 plates, L01–L12). Until those land, attach the sheets
> below **for architecture only** and let the cartoon style anchor override their rendering.
>
> The earlier version of this roster listed nine locations, seven of which named files that were never
> created. Below is the **actual on-disk inventory**.

**The real building**: The Triangle, Cambridge (Eric Parry Architects) — photos in
[`building-reference/use-images/`](file:///C:/kontitemp/AI/circle_the_square/building-reference/use-images/).
Pale buff brick, tall narrow windows, 39m brick tower with a glazed timber lantern box.
**Low-rise Cambridge — NOT London.** No Shard, no Gherkin, no Tower Bridge, no skyline.

All location reference assets are stored in:  
📁 **[`C:\kontitemp\AI\circle_the_square\location-refs\`](file:///C:/kontitemp/AI/circle_the_square/location-refs/)**

| Location | File | Used as | Cartoon plate |
| :--- | :--- | :--- | :--- |
| Exterior Forecourt & Main Entrance | [`exterior_forecourt_location_sheet.jpg`](file:///C:/kontitemp/AI/circle_the_square/location-refs/exterior_forecourt_location_sheet.jpg) | — | L01 ✅ / L05 ⬜ |
| Reception & Double-Height Atrium | [`reception_atrium_location_sheet.jpg`](file:///C:/kontitemp/AI/circle_the_square/location-refs/reception_atrium_location_sheet.jpg) | — | L07, L08 ⬜ |
| Jan's Office (glass meeting room) | [`jan_office_location_sheet.jpg`](file:///C:/kontitemp/AI/circle_the_square/location-refs/jan_office_location_sheet.jpg) | `@office` — Scene 1 | L10 ⬜ |
| Open-Plan Office Floor | [`open_plan_floor_location_sheet.jpg`](file:///C:/kontitemp/AI/circle_the_square/location-refs/open_plan_floor_location_sheet.jpg) | `@openplan` — Scene 2 | L09 ⬜ |
| Staff Restaurant / Canteen | [`canteen_location_sheet.jpg`](file:///C:/kontitemp/AI/circle_the_square/location-refs/canteen_location_sheet.jpg) | `@canteen` — Scene 3 | L11 ⬜ |
| Scene 2 master reference | [`scene2_master_reference.jpg`](file:///C:/kontitemp/AI/circle_the_square/location-refs/scene2_master_reference.jpg) | Continuity | — |
| Scene 3 master reference | [`scene3_master_reference.jpg`](file:///C:/kontitemp/AI/circle_the_square/location-refs/scene3_master_reference.jpg) | Continuity | — |

**Style-transfer method that works** for building cartoon plates — attach a real photo and restyle it,
rather than describing the building from scratch. `"Only change the rendering style"` is doing the heavy
lifting; without it the model reinvents the building. Full prompt in `LOCATION_PLATE_SHOT_LIST.md`.

---

## 4. 📄 LOCKED FOUNTAIN SCREENPLAY

The screenplay is saved at:  
📄 **[`C:\kontitemp\ai\circle_the_square\CTS_Featurette_Episode.fountain`](file:///C:/kontitemp/ai/circle_the_square/CTS_Featurette_Episode.fountain)**

---

## 5. 🎬 DIRECTOR'S SHOT LIST & STAGING SUMMARY

The complete scene-by-scene shot list is locked at:  
📄 **Filename**: `featurette_shot_list.md`  
📄 **Full Path**: [`file:///C:/kontitemp/ai/circle_the_square/featurette_shot_list.md`](file:///C:/kontitemp/ai/circle_the_square/featurette_shot_list.md)

Contents:
- ✅ Scene 1 shot-by-shot breakdown (Jan's Office)
- ✅ Scene 2 shot-by-shot breakdown (Corridor & Open-Plan Floor)
- ✅ Scene 3 shot-by-shot breakdown (Canteen Meltdown & Taser)
- ✅ Character + location ref assignments per shot
- ✅ Jan shirt continuity tracker across all scenes
- ✅ Sharon wardrobe state A/B tracker
- ✅ Production notes (branding masking, canteen extra)

---

## 6. 🔁 SCENE TRANSITIONS & EDITORIAL MAP

```
[SCENE 1: Jan's Office]
    ──(Christina exits, glass door click)──>
[SCENE 1B: Jan's Office — Sharon enters without knocking]
    ──(Blinds snap down, door locks)──>
[SCENE 2: Corridor — Chris & Rick watch, Sharon exits dishevelled]
    ──(Jan re-buttons shirt, claps hands)──>
[SCENE 2B: Open-Plan Floor — Project Inception announcement]
    ──(TIME CUT: "Next Morning")──>
[SCENE 3: Staff Restaurant / Canteen — Pastry shortage → Meltdown → Taser]
    ──(FADE OUT)──>
[END TITLE CARD]
```

---

## 7. 🔊 AUDIO & SOUND DESIGN CUE SHEET

Sound effects, foley impacts, room tone, glass smashes, and taser arcs are delegated directly to **Video AI Native Audio Generation** (e.g., Google Veo 2 / Sora video-with-audio prompts) during clip synthesis. Character dialogue is dubbed using the locked local Qwen3-TTS GPU voices.

Key audio events per scene:
- **Scene 1**: Office ambient hum, glass door click, blinds mechanical snap
- **Scene 2**: Corridor ambient, printer hum, crowd groan SFX, stress ball squeak
- **Scene 3**: Canteen clatter, CRASH of plates, GLASS SHATTER, POP-CRACKLE taser arc, body slump

Dialogue audio files: [`C:\kontitemp\ai\circle_the_square\audio-refs\`](file:///C:/kontitemp/ai/circle_the_square/audio-refs/)

---

## 8. 🧰 COSTUME & PROP MASTER INVENTORY

| Character | Props | Continuity Notes |
| :--- | :--- | :--- |
| **Jan Peach** | Black phone, oversized watch, Prism mug, meeting chair (for window smash) | Shirt: Scene 1 = buttoned → unbuttoned → off; Scene 2 = re-buttoned askew; Scene 3 = shirt off, tie gone |
| **Christina Dross** | Tablet/clipboard, travel mug | Scene 1 only — exits before Scene 2 |
| **Sharon Enfield** | Handbag, phone | State A (composed arriving) → State B (dishevelled leaving); heels carried in Scene 2 |
| **Chris** | Coffee cup, Project Inception stress ball | Present Scenes 2 & 3 |
| **Rick** | Concealed prop taser (must read fake/non-functional) | Taser drawn only in Scene 3 finale |
| **Canteen Worker** | Apron, empty pastry tray, serving tongs | Walk-on, one line only |
| **SET DRESSING** | 1,000 Project Inception stress balls/pens/t-shirts (background), pain au chocolat pastries (Scene 3), broken china (post-smash), shattered window prop, **venetian blinds on Jan's office windows (raised/open)** | Continuity: pastry tray must be visibly empty when Jan arrives. Blinds must be visible and open from Scene 1's first shot — F26a pays them off by having Jan yank them shut, so they cannot be introduced only at that point. Found missing from `jan_office_location_sheet.jpg` on 2026-08-25; fixed reference is `jan_office_location_sheet_fixed.png` — still needs the blinds added on top of that skyline fix (not yet done as of this note). |

---

## 9. 🖼️ PANEL-BY-PANEL STORYBOARD PROMPT ENGINE

> 🎨 **Live cartoon docs — use these:**
> - **[`featurette_storyboard_image_prompts.md`](file:///C:/kontitemp/AI/circle_the_square/featurette_storyboard_image_prompts.md)** — all 64 keyframes (F01–F61), cartoon style anchor, `@tag` legend. **The working doc.**
> - **[`MASTER_STORYBOARD_SESSION_PROMPTS.md`](file:///C:/kontitemp/AI/circle_the_square/MASTER_STORYBOARD_SESSION_PROMPTS.md)** — ready-to-paste cartoon prompts, Scene 1 from F01.
> - **[`LOCATION_PLATE_SHOT_LIST.md`](file:///C:/kontitemp/AI/circle_the_square/LOCATION_PLATE_SHOT_LIST.md)** — 12 cartoon plates and the camera move each one feeds.

⛔ **Superseded (photoreal era, kept for reference only):** the 5-shot opening sequence Veo 2 / Gemini
prompt engine at [`storyboard_prompt_engine.md`](file:///C:/kontitemp/AI/circle_the_square/storyboard_prompt_engine.md),
plus `featurette_prompt_engine.md` and `featurette_shot_list.md`. Its shot *structure* is still sound;
its photoreal style blocks and glass-tower imagery are not.

Contents:
- ✅ Shot 01 Prompt (High Aerial & Prow Swoop) + 2 image refs
- ✅ Shot 02 Prompt (Forecourt Plaza Push) + 2 image refs
- ✅ Shot 03 Prompt (Atrium Speed Gate Push-Through) + 2 image refs
- ✅ Shot 04 Prompt (Office Central Aisle Flyby) + 2 image refs
- ✅ Shot 05 Prompt (Group Photo Meltdown Stinger) + 3 image refs
- ✅ Per-shot native audio prompts
- ✅ Supplementary character & location reference sheet table
- ✅ What NOT to do (attention dilution rules)

---

## 10. 🗂️ FEATURETTE PRODUCTION PACKAGE

The full featurette production package consists of:

| Document | Filename | Full Path |
| :--- | :--- | :--- |
| **Fountain Screenplay** | `CTS_Featurette_Episode.fountain` | [`file:///C:/kontitemp/ai/circle_the_square/CTS_Featurette_Episode.fountain`](file:///C:/kontitemp/ai/circle_the_square/CTS_Featurette_Episode.fountain) |
| **Scene-by-Scene Shot List** | `featurette_shot_list.md` | [`file:///C:/kontitemp/ai/circle_the_square/featurette_shot_list.md`](file:///C:/kontitemp/ai/circle_the_square/featurette_shot_list.md) |
| **Featurette Prompt Engine** | `featurette_prompt_engine.md` | [`file:///C:/kontitemp/ai/circle_the_square/featurette_prompt_engine.md`](file:///C:/kontitemp/ai/circle_the_square/featurette_prompt_engine.md) |

---

## 10.1. 🛸 OPENING TITLE SEQUENCE & MOCK PHOTO PLAN

The locked FPV drone-to-interior fly-through and group photo stinger plan is recorded at:  
📄 **Filename**: `OPENING_TITLE_SEQUENCE_PLAN.md`  
📄 **Full Path**: [`file:///C:/kontitemp/ai/circle_the_square/OPENING_TITLE_SEQUENCE_PLAN.md`](file:///C:/kontitemp/ai/circle_the_square/OPENING_TITLE_SEQUENCE_PLAN.md)  

Interactive Visual Asset Portal:  
📄 **Filename**: `opening_sequence_preview.html`  
📄 **Full Path**: [`file:///C:/kontitemp/ai/circle_the_square/opening_sequence_preview.html`](file:///C:/kontitemp/ai/circle_the_square/opening_sequence_preview.html)  

6-Panel Vector Director's Storyboard Board:  
📄 **Filename**: `opening_sequence_storyboard.html`  
📄 **Full Path**: [`file:///C:/kontitemp/ai/circle_the_square/opening_sequence_storyboard.html`](file:///C:/kontitemp/ai/circle_the_square/opening_sequence_storyboard.html)  

---

## 11. 🎙️ LOCKED VOICE SPECIFICATION & AUDIO ROSTER (QWEN3-TTS & NEURAL)

Local hyper-realistic voice generation is locked and configured inside ComfyUI (`ComfyUI-QwenTTS`):

* **Custom Node**: `C:\ai\ComfyUI\ComfyUI\custom_nodes\ComfyUI-QwenTTS\`
* **Models Directory**: `C:\ai\ComfyUI\ComfyUI\models\TTS\Qwen3-TTS\`
* **Sample Workflow**: `C:\ai\ComfyUI\ComfyUI\custom_nodes\ComfyUI-QwenTTS\example_workflows\QwenTTS_sample_workflow.json`
* **Pre-Coded Prompts JSON**: 📄 **[`C:\kontitemp\ai\circle_the_square\qwen3_tts_voice_prompts.json`](file:///C:/kontitemp/ai/circle_the_square/qwen3_tts_voice_prompts.json)**

| Character | Age | Accent & Vocal Style | Locked Local GPU Audio (`.wav`) | Locked Neural MP3 (`.mp3`) |
| :--- | :--- | :--- | :--- | :--- |
| **Jan Peach** | 52 | Pompous Senior British RP Male Executive | `jan_qwen_custom.wav`<br>[`file:///C:/kontitemp/ai/circle_the_square/audio-refs/jan_qwen_custom.wav`](file:///C:/kontitemp/ai/circle_the_square/audio-refs/jan_qwen_custom.wav) | `jan_human_sample.mp3`<br>[`file:///C:/kontitemp/ai/circle_the_square/audio-refs/jan_human_sample.mp3`](file:///C:/kontitemp/ai/circle_the_square/audio-refs/jan_human_sample.mp3) |
| **Christina Dross** | 38 | Crisp British RP Female Corporate Strategist | `christina_qwen_custom.wav`<br>[`file:///C:/kontitemp/ai/circle_the_square/audio-refs/christina_qwen_custom.wav`](file:///C:/kontitemp/ai/circle_the_square/audio-refs/christina_qwen_custom.wav) | `christina_human_sample.mp3`<br>[`file:///C:/kontitemp/ai/circle_the_square/audio-refs/christina_human_sample.mp3`](file:///C:/kontitemp/ai/circle_the_square/audio-refs/christina_human_sample.mp3) |
| **Sharon Enfield** | 34 | Warm Confident Adult Female (Subtle Welsh Lilt) | `sharon_qwen_custom.wav`<br>[`file:///C:/kontitemp/ai/circle_the_square/audio-refs/sharon_qwen_custom.wav`](file:///C:/kontitemp/ai/circle_the_square/audio-refs/sharon_qwen_custom.wav) | `sharon_human_sample.mp3`<br>[`file:///C:/kontitemp/ai/circle_the_square/audio-refs/sharon_human_sample.mp3`](file:///C:/kontitemp/ai/circle_the_square/audio-refs/sharon_human_sample.mp3) |
| **Chris** | 32 | Sarcastic South London British Baritone | `chris_qwen_custom.wav`<br>[`file:///C:/kontitemp/ai/circle_the_square/audio-refs/chris_qwen_custom.wav`](file:///C:/kontitemp/ai/circle_the_square/audio-refs/chris_qwen_custom.wav) | `chris_human_sample.mp3`<br>[`file:///C:/kontitemp/ai/circle_the_square/audio-refs/chris_human_sample.mp3`](file:///C:/kontitemp/ai/circle_the_square/audio-refs/chris_human_sample.mp3) |
| **Rick** | 40 | Deep Gravelly British Bass-Baritone Monotone | `rick_qwen_custom.wav`<br>[`file:///C:/kontitemp/ai/circle_the_square/audio-refs/rick_qwen_custom.wav`](file:///C:/kontitemp/ai/circle_the_square/audio-refs/rick_qwen_custom.wav) | `rick_human_sample.mp3`<br>[`file:///C:/kontitemp/ai/circle_the_square/audio-refs/rick_human_sample.mp3`](file:///C:/kontitemp/ai/circle_the_square/audio-refs/rick_human_sample.mp3) |


