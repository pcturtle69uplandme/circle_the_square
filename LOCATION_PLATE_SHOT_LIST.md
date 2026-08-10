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

### Exterior — for drone moves

| # | Plate | Description | Drone move it feeds | Status |
|---|---|---|---|---|
| L01 | **Establishing wide** | Three-quarter view of the main block, prow corner leading, tower with lit lantern beside it, courtyard and trees at ground level | Slow push-in from wide | ✅ |
| L02 | **High aerial** | Looking down on the whole complex — two blocks, central courtyard, rooftop landscaped gardens between the finger wings, railway to one side | Descending orbit | ⬜ |
| L03 | **Prow low angle** | Tight low-angle on the sharp angular corner, brick banding receding upward, sky behind | Rising crane reveal | ⬜ |
| L04 | **Tower detail** | The brick tower and its glazed timber lantern box against dusk sky, warm amber glow | Vertical climb to the lantern | ⬜ |
| L05 | **Courtyard approach** | Ground-level, walking toward the revolving doors, glazed reception ahead, the indigo-to-cream tiled columns either side | Forward tracking / entry move | ⬜ |
| L06 | **Railway side** | The long flank seen across the railway line, fence and grass verge in foreground, tower at the far end | Lateral tracking | ⬜ |

### Interior — for camera moves

| # | Plate | Description | Move it feeds | Status |
|---|---|---|---|---|
| L07 | **Atrium wide** | Double-height hall, concrete column grid, gallery with orange chairs above, canteen tables below | Slow drift across the space | ⬜ |
| L08 | **Reception hall** | Inside the doors — speedgates, hexagonal timber pod, double-height glazing, stair beyond | Push through the gates | ⬜ |
| L09 | **Open-plan floor** | Desk rows, monitors, acoustic baffles overhead, glazed partitions to Jan's office | Glide down the desk run |⬜ |
| L10 | **Jan's office** | The black-and-white triangle acoustic feature wall, walnut desk with the orange-lit angled leg, dark plank floor, grey sofa with burnt-orange cushion, glazed partition | Slow orbit around the desk | ⬜ |
| L11 | **Canteen counter** | Stainless servery, pastry trays, timber-fronted counter, staff queueing | Track along the counter | ⬜ |
| L12 | **Gallery level** | Looking down over the glass balustrade to the floor below, orange chairs in foreground | Crane down over the edge | ⬜ |

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
