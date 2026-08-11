# 🏢 CIRCLE THE SQUARE — CARTOON LOCATION PLATES

> **Purpose**: stills of the PRISM building and interiors in the cartoon house style, generated in
> Google Flow, to be used as **first frames for Veo drone / camera moves**.
> **Style anchor and cast**: `CARTOON_CAST_BIBLE.md`
> **Real-world source**: `building-reference/` — The Triangle, Cambridge (Eric Parry Architects)

---

## 🧱 THE REAL BUILDING — what every plate must honour

Taken from `building-reference/use-images/` and `Building overview.txt`.

| Element | Detail |
| :--- | :--- |
| **Massing** | Two five-storey blocks either side of a central entrance courtyard, linked by a bridge block. "E" shaped wings north of the plaza. Sharp angular **prow** corner where the site narrows toward the railway. |
| **Materials** | Pale buff sandy brick, precast concrete banding, glass. Warm and light, not grey. |
| **Windows** | Strict grid of **tall narrow vertical windows** in deep reveals. Very regular, almost institutional. |
| **The tower** | 39m slim brick tower topped by a **glazed timber-lined lantern box** that glows warm amber at dusk. The landmark — visible from arriving trains. |
| **Signature columns** | Slender columns at the entrance clad in **stacked glazed brick tiles shading indigo → cream → bronze**. Distinctive beaded/striped texture. |
| **Entrance** | Revolving doors into a double-height glazed reception under the bridge block. |
| **Setting** | **Low-rise Cambridge.** Trees, railway line, grass verge, wooden post-and-rail fence. Wide open sky. |
| **Interior atrium** | Double-height, pale cream tiled floor, white soffits, grid of **exposed dark grey concrete columns**, full-height glazing one side. First-floor gallery behind a **frameless glass balustrade**. |
| **Interior furniture** | **Burnt-orange moulded chairs** on the gallery (matches the PRISM accent), black and pale timber cafe chairs below, high poseur tables, timber-fronted servery counters, open stair with glass balustrade, hexagonal timber reception pod, security speedgates. |

> ⛔ **NEVER**: skyscrapers, the Shard, the Gherkin, Tower Bridge, London skyline, dark wood-panelled
> traditional offices. Earlier generations kept defaulting to London — the prompt must exclude it explicitly.

---

## 🎬 PLATE LIST

Status: ✅ generated · ⬜ pending
**Downloaded 2026-08-11 to [`location-refs/cartoon-plates/`](location-refs/cartoon-plates/)** — file names and
per-plate notes in `location-refs/cartoon-plates/PLATES_MANIFEST.md`. All are 1376×768 (16:9).

> **11 of 12 done.** Only **L04 (tower detail)** is still missing. An earlier version of this doc said
> 1 of 12 — that was badly out of date; the plates had been generated but never downloaded.

### Exterior — for drone moves

| # | Plate | Description | Drone move it feeds | Status |
|---|---|---|---|---|
| L01 | **Establishing wide** | Three-quarter view of the main block, prow corner leading, tower with lit lantern beside it, courtyard and trees at ground level | Slow push-in from wide | ✅ ×3 |
| L02 | **High aerial** | Looking down on the whole complex — two blocks, central courtyard, rooftop landscaped gardens between the finger wings, railway to one side | Descending orbit | ✅ |
| L03 | **Prow low angle** | Tight low-angle on the sharp angular corner, brick banding receding upward, sky behind | Rising crane reveal | ✅ |
| L04 | **Tower detail** | The brick tower and its glazed timber lantern box against dusk sky, warm amber glow | Vertical climb to the lantern | ⬜ **only gap** |
| L05 | **Courtyard approach** | Ground-level, walking toward the revolving doors, glazed reception ahead, the indigo-to-cream tiled columns either side | Forward tracking / entry move | ✅ ×2 |
| L06 | **Railway side** | The long flank seen across the railway line, fence and grass verge in foreground, tower at the far end | Lateral tracking | ✅ ×2 |

### Interior — for camera moves

| # | Plate | Description | Move it feeds | Status |
|---|---|---|---|---|
| L07 | **Atrium wide** | Double-height hall, concrete column grid, gallery with orange chairs above, canteen tables below | Slow drift across the space | ✅ ×2 |
| L08 | **Reception hall** | Inside the doors — speedgates, hexagonal timber pod, double-height glazing, stair beyond | Push through the gates | ✅ ×2 |
| L09 | **Open-plan floor** | Desk rows, monitors, acoustic baffles overhead, glazed partitions to Jan's office | Glide down the desk run | ✅ ×3 |
| L10 | **Jan's office** | The black-and-white triangle acoustic feature wall, walnut desk with the orange-lit angled leg, dark plank floor, grey sofa with burnt-orange cushion, glazed partition | Slow orbit around the desk | ✅ *(skyline fixed)* |
| L11 | **Canteen counter** | Stainless servery, pastry trays, timber-fronted counter, staff queueing | Track along the counter | ✅ |
| L12 | **Gallery level** | Looking down over the glass balustrade to the floor below, orange chairs in foreground | Crane down over the edge | ✅ ×2 |

### Bonus plates not on the original list

| File | What it is |
| :--- | :--- |
| `EXTRA_breakout_foosball.jpg` | Breakout area with foosball table and planting |
| `EXTRA_corridor_art_panel.jpg` | Corridor with a colour art panel and fire point |
| `EXTRA_courtyard_picnic_tables.jpg` | Courtyard with picnic benches and hedging |
| `EXTRA_podium_courtyard_garden.jpg` | Landscaped podium courtyard between the wings |
| `TITLE_CARD_circle_the_square.jpg` | Title card — courtyard at dusk with *CIRCLE THE SQUARE* lettering. **The one plate that intentionally carries text.** |
| `SCENE_group_photo_prism.jpg` | The corporate group-photo gag with the cast and a PRISM banner — covers `GROUP_PHOTO_SHOT_SPEC.md` |

---

## ⚠️ WATCH FOR THE LONDON SKYLINE — it has already happened once

`L10_jans_office` came back with **The Shard and a full London skyline** through the window, titled
"Executive office with city view". Everything else about the plate was correct. It was fixed in Flow
with an edit rather than a regeneration, which preserved all the set dressing:

```
Change ONLY the view seen through the exterior glazing on the left. Completely remove the tall
pointed skyscraper and the entire dense city skyline. Replace that view with low-rise Cambridge:
two and three storey pale buff brick buildings, mature green trees, a railway line, and wide open
pale sky. Absolutely NO skyscrapers, NO tall towers, NO Shard, NO London landmarks, NO city
skyline. Keep every other element of the image exactly as it is - do not alter the black and white
geometric triangle feature wall, the walnut desk, the dark plank flooring, the grey sofa with the
burnt orange cushion, the potted plant, the glazed partitions, the ceiling, the lighting, or the
camera angle. Keep the identical stylised comic illustration style. Absolutely NO text, NO
lettering anywhere in the image.
```

**Two things this proves:**
1. **Editing works for scenery fixes.** The documented policy block applies to edits that *insert a
   person*, not to removing a building. Prefer an edit over a regeneration — it keeps the set dressing.
2. **Check every window in every interior plate** before trusting it. `EXTRA_corridor_art_panel` was
   checked and is clean; the rest of the interiors have no exterior view to contaminate.

---

## 📐 PLATE PROMPT TEMPLATE

```
Generate ONE image: a <EXTERIOR/INTERIOR> LOCATION PLATE in stylised comic illustration
style, NOT photorealistic. Subject: <PLATE DESCRIPTION using the elements table above>.
Setting: low-rise Cambridge, trees and railway beyond, wide pale sky. Absolutely NO
skyscrapers, NO London landmarks, no Shard, no Gherkin, no Tower Bridge.
Style: stylised British sitcom comic art, clean bold line art, flat muted colour palette,
cel-shaded, 2.39:1 widescreen crop. Absolutely NO text, NO signage lettering, NO captions
anywhere in the image.
```

## 🎥 USING THESE FOR DRONE SHOTS

Each plate is a **first frame**. In Flow, feed the plate into a video generation and describe the
move only — not the content — so the model animates the existing frame rather than reinventing it.
Keep moves slow and single-axis; comic-style plates hold up better under a steady push, orbit or
crane than under fast or compound moves.

Generate all plates in **one continuous Flow session** so the art style stays locked, exactly as
with the character sheets.
