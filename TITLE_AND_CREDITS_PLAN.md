# 🎬 CIRCLE THE SQUARE — TITLE SEQUENCE, THEME SONG & END CREDITS PLAN

**Project:** *Circle the Square* / *ALL UNDER ONE ROOF*  
**Format:** Opening Title Sequence (30s) & End Credits Outro (25s)  
**Tone:** Modern British Corporate Satire / Mockumentary  
**Branding Palette:** Ink Navy (`#0B0D12`), Burnt Orange (`#B0381F`), Slate Grey (`#4A5568`), Bone White (`#F4F3EF`)  
**Date:** August 2026

---

## 🎵 1. OPENING TITLE SONG & THEME MUSIC CONCEPT

### Music Style & Instrumentation
* **Genre**: Modern British workplace satire (in the style of *The Thick of It*, *W1A*, or *Succession* mockumentary scoring).
* **Instrumentation**: Rhythmic acoustic guitar, light pizzicato strings, tuned marimba/glockenspiel, subtle sub-bass drone, and a short satirical corporate choir vocal harmony.
* **Music Engine**: Lyria 3 Pro Engine (`lyria-3-pro-preview`) / Custom Local Arranger.

### ⏱️ Time-Coded Audio Track Breakdown (30 Seconds)

| Timestamp | Musical Layer | Mood / Energy | Cue Beat |
|---|---|---|---|
| `0:00 - 0:08` | Solitary 7/8 time acoustic guitar strumming over low HVAC hum | Quiet, mechanical, early morning | Drone approaches acute prow |
| `0:08 - 0:16` | Light pizzicato strings & marimba tick join with crisp hi-hat | Bouncy corporate optimism | Drone orbits high over roof courtyards |
| `0:16 - 0:24` | Low sub-bass swell & muted brass accent building tension | Pompous corporate escalation | Fast interior cuts (gates, pod, desk rows) |
| `0:24 - 0:28` | Satirical corporate choir vocal harmony (*"Aaaa-ll Under One Roof..."*) | Grand administrative crescendo | High aerial pull-back |
| `0:28 - 0:30` | **TENSION DROP SILENCE**: Music cuts out dead on a single glass door click | Sudden abrupt cutoff | **TITLE CARD DROPS** |

---

## 🎥 2. OPENING TITLE SEQUENCE — SHOT LIST (30 Seconds)

### Shot T-01: Low Drone Flyby — The Acute Prow (6s)
* **Visual**: Smooth drone camera sliding low over the perimeter roadway towards the curved buff-brick prow of the triangular mothership at first light. Cold silver-blue dawn light, zero humans on the street.
* **Text Overlay**: None.
* **Audio**: Acoustic guitar strumming + faint distance train rumble.

---

### Shot T-02: High Drone Orbit — The Triangular Atrium (8s)
* **Visual**: Drone ascending high above the 2.5-hectare plot, rotating slowly over the glazed link building and the three planted roof courtyards (pines, boulders, fritted glass).
* **Text Overlay**: Lower-left corner in monospace: `LAT 52.1912° N, LONG 0.1284° E — CAMBRIDGE UK`
* **Audio**: Pizzicato strings & marimba tick join score.

---

### Shot T-03: Fast Interior Flash Cuts — The Corporate Machine (8s)
* **Visual Cuts**:
  * *Cut A (2s)*: Speed gates in the atrium (`DL-EPA-CA-4821`), glass leaves opening in unison.
  * *Cut B (2s)*: Pristine open-plan desk rows with the hanging triangle felt sculpture (`20250207_084330`).
  * *Cut C (2s)*: Wall plaque reading `STAFF ENTRANCE ONLY` on blue paneling.
  * *Cut D (2s)*: Wall sign: `Cambridge Assessment looks forward to welcoming you`.
* **Audio**: Sub-bass swell & muted brass building tension.

---

### Shot T-04: The Title Drop (8s)
* **Visual**: High drone pull-back revealing the entire triangular building against the horizon. Fine burnt-orange geometric vector lines trace the site triangle on screen, settling into the title graphic:

```text
    ┌───────────────────────────────────────────────┐
    │                                               │
    │         C I R C L E   T H E   S Q U A R E     │
    │         ─────────────────────────────────     │
    │               ALL UNDER ONE ROOF              │
    │                                               │
    │           PRISM HQ — CAMBRIDGE ASSESSMENT     │
    │                                               │
    └───────────────────────────────────────────────┘
```

* **Typography**: Title in **Outfit Bold (800)** in bone white (`#F4F3EF`); Subtitle in **Inter Medium** in burnt orange (`#B0381F`); Location in **JetBrains Mono** in slate grey.
* **Audio**: Choir crescendo, then **DEAD SILENCE CUTOFF** as the title hits.

---

## 📜 3. END CREDITS SEQUENCE & OUTRO (25 Seconds)

### Epilogue Aerial Shot (12s)
* **Visual**: High drone hovering station above the railway embankment at blue hour. The glazed lantern crown at the top of the brick tower glows warm amber against the deep navy twilight sky. One train slides past silently in the distance.
* **Audio**: Lyria Bed A acoustic guitar reprise.

---

### End Credits Roll Layout (13s)
* **Visual**: Smooth slow-scrolling or card-fade credits over dark ink-navy background (`#0B0D12`):

```text
====================================================================
                        CIRCLE THE SQUARE
                        ALL UNDER ONE ROOF
====================================================================

                             CAST
        Jan Peach (CEO) .................... Local Qwen3-TTS
        Christina (Strategy) ............... Local Qwen3-TTS
        Sharon (Operations) ................ Local Qwen3-TTS
        Rick (Security) .................... Local Qwen3-TTS
        Trevor ............................. Self (Unvoiced)

                    PRODUCTION & AI PIPELINE
        Directed & Written by .............. You
        Visual Generation .................. FLUX1 Kontext (ComfyUI)
        Video AI Clip Synthesis ............ Google Veo 2 / Sora
        Music & Score ...................... Lyria 3 Pro Engine
        Native Sound Design ................ Video AI Audio Synthesis

                    FILMED ON LOCATION AT
        The Triangle Building, Shaftesbury Road, Cambridge UK
        (Cambridge Assessment Mothership Site)

                   © 2026 PRISM CREATIVE UNIT
====================================================================
```

* **Final Outro Sound Cue (`[SFX-22]`)**: As the end credits finish and fade to black, a distant **Police Siren Wail** (`sfx_22_siren_fade.wav`) slowly fades in over the black screen before dissolving into total silence.

---

## 🛠️ 4. Python Title Card Generator (`build_title_card_v3.py`)

A zero-cost Python script using PIL & FFMPEG to generate the exact 16:9 / 2.39:1 opening title card clip (`clips/title_card_v03.mp4`):

```powershell
cd "C:\kontitemp\ai\circle_the_square"
python build_title_card_v3.py
```

*This title and credits plan is integrated into [`MASTER_PRODUCTION_MANUAL.md`](MASTER_PRODUCTION_MANUAL.md) and [`production_portal.html`](production_portal.html).*
