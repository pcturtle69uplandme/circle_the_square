# 🎨 CIRCLE THE SQUARE — CARTOON CAST BIBLE

> **Status**: 11 cartoon character model sheets generated in Google Flow on 2026-08-10, downloaded and committed to `character-refs/`.
> **Style**: stylised British sitcom comic art (see anchor below).
> **Why cartoon**: photoreal renders of Jan Peach were blocked repeatedly by Google Flow's
> likeness protection. The identical frame in comic style generated first try. See
> `.agents/rules/cli_image_quota_rules.md` and `character-refs/README.txt`.

---

## 🎨 STYLE ANCHOR — paste into every prompt

```
Stylised British sitcom comic art, clean bold line art, flat muted colour palette,
expressive caricature, cel-shaded, 2.39:1 widescreen crop. NOT photorealistic.
Absolutely NO text, NO speech bubbles, NO captions, NO labels, NO sound effects,
NO lettering of any kind anywhere in the image.
```

**Two standing continuity rules:**
- **No lettering in panels.** `storyboard_slideshow.html` draws its own speech bubbles.
- **The company is PRISM.** Every lanyard, nameplate, mug and sign reads PRISM — never Peach Corp.

## 🏢 WORLD

**Building** — The Triangle, Cambridge (Eric Parry Architects). Buff/pale stone with a gently
curved corner, horizontal ribbon windows, a glazed timber-lined rooftop lantern on a brick tower,
a paved courtyard with young trees, and a glazed ground-floor atrium link with dark vertical fins.
**Low-rise Cambridge — NOT London. No Shard, no Gherkin, no skyscrapers.**

**Jan's office** — black-and-white geometric triangle-pattern acoustic feature wall (the signature
element), walnut executive desk with an angled orange-lit leg, dark plank flooring, grey mesh
chair, black open shelving, fiddle-leaf fig, grey sofa with a burnt-orange cushion, black-framed
glazed partitions onto the open-plan floor.

**House accent colour** — burnt orange `#B0381F`. Every PRISM lanyard uses it.

---

## 👔 PRINCIPAL CAST

### Jan Peach — CEO, PRISM
52 · White British · 178cm · soft overweight build, gut straining his shirt buttons · thinning
grey-brown hair receding into a comb-over · ruddy complexion · default smug half-smile, chin up.
**Wardrobe**: navy suit, pale shirt, silver-grey tie, black oxfords, orange PRISM lanyard,
oversized flashy watch, gold wedding ring.
**Notes**: complexion reddens under stress with a sweat sheen; shirt grows progressively
dishevelled through the episode; chest out and finger-jabbing when angry.

### Christina Dross — Comms Lead
38 · White British · 168cm · slim, upright · sharp dark brown chin-length bob with a blunt fringe ·
calm, dry, never visibly rattled.
**Wardrobe**: charcoal-navy trouser suit, cream blouse, black low-heel courts, fine gold necklace,
orange PRISM lanyard.

### Sharon Enfield — Staff
34 · White British · 165cm · curvy · shoulder-length wavy auburn hair · transactional,
plain-spoken, unbothered.
**Wardrobe**: emerald green blouse, black pencil skirt, black heels, gold hoops, orange lanyard.

### Chris — Staff
32 · White British · 180cm · lean · short dark brown hair swept up, light stubble · office
smart-mouth, deadpan half-smirk, quick with a jab.
**Wardrobe**: light blue button-down, sleeves rolled, dark charcoal trousers, dark trainers,
black watch, orange lanyard.

### Rick — Staff
40 · White British · 183cm · sturdy broad muscular build · short salt-and-pepper hair · blunt
realist, calm under pressure, flat deadpan, arms crossed.
**Wardrobe**: grey polo, navy work trousers, black belt, brown work shoes, orange lanyard.
**Prop**: concealed prop taser (F57, F58, F61).

---

## 👥 SUPPORTING CAST

### Maureen — Canteen worker
58 · White British · 162cm · sturdy · short greying curly hair pinned back · kindly but
no-nonsense · reading glasses on a chain.
**Wardrobe**: beige apron over white polo, black trousers, black non-slip flats.
**Appears**: F47, F48, F51 — fills the gap flagged in `featurette_storyboard_image_prompts.md`.

### Gemma Ashcroft — Receptionist, front of house
26 · White British · 170cm · slim · sleek dark blonde high ponytail · polished
customer-service smile.
**Wardrobe**: white blouse, slate-grey blazer and pencil skirt, black low heels, orange
lanyard, discreet telephone headset.
**Appears**: reception atrium.

### Priya Raghavan — Office staff
29 · British Indian · 164cm · slim · long dark hair in a low ponytail · bright, alert.
**Wardrobe**: mustard cardigan over white blouse, navy trousers, tan ankle boots, orange lanyard.

### Barbara Whitlock — Senior administrator
55 · White British · 160cm · short, round · ash-blonde greying bob · large round glasses on a
beaded chain · sceptical, pursed.
**Wardrobe**: teal blouse, navy cardigan, grey A-line skirt, low black heels, orange lanyard.

### Dev Osei — Junior data analyst
26 · Black British · 178cm · slim · short cropped black hair · thick black-rimmed glasses ·
earnest, slightly nervous.
**Wardrobe**: burgundy jumper over pale blue collared shirt, dark grey chinos, white trainers,
orange lanyard.

### Tomasz Wojcik — Facilities & maintenance
35 · Polish British · 186cm · tall, heavyset · shaved head, short dark beard · calm, unhurried.
**Wardrobe**: dark blue work shirt with sleeves rolled, tool pouch on belt, black work trousers,
brown work boots, orange lanyard.

---

## 📏 HEIGHT TABLE — the shared scale

Every sheet must be drawn against this one scale. These are small differences and they must
*look* small: the tallest principal is only 18cm above the shortest.

| Character | Height | | Character | Height |
| :--- | :-- | :-- | :--- | :-- |
| Tomasz Wojcik | 186cm | | Gemma Ashcroft | 170cm |
| **Rick** | **183cm** | | **Christina Dross** | **168cm** |
| **Chris** | **180cm** | | **Sharon Enfield** | **165cm** |
| Dev Osei | 178cm | | Priya Raghavan | 164cm |
| **Jan Peach** | **178cm** | | Maureen | 162cm |
| | | | Barbara Whitlock | 160cm |

> **Rick is only 5cm taller than Jan.** If a group shot shows him towering, it is wrong.

---

## 📐 MODEL SHEET PROMPT TEMPLATE

> ### ⚠️ Why this template changed — 2026-08-12
>
> The original 11 sheets each drew their character **filling the frame**, alone on plain grey.
> Rick at 183cm and Christina at 168cm therefore occupy identical pixel heights. **The sheets
> encode no shared scale**, so when several are used as ingredients in one image the model has
> nothing to compare against and sizes each from its build words alone — Rick's "sturdy broad
> muscular build" renders him roughly **1.5× everyone else**, towering and standing forward of
> the line. This was hit on the title sequence and could not be fixed by any img2img edit; three
> increasingly explicit rewrites all came back unchanged.
>
> **The fix is the measuring wall below.** It puts an identical ruler behind every character, so
> relative height is carried *visually* in the ingredient rather than hoped for in the prompt.
> Regenerate every sheet with it, and use it for all future characters.

Reusable for rerolls or new characters:

```
Generate ONE image: a CHARACTER MODEL SHEET in stylised comic illustration style,
NOT photorealistic.

Subject: <NAME>, <ROLE> at PRISM. <AGE, ETHNICITY, BUILD, HAIR, DEFAULT EXPRESSION>.
HEIGHT: <HEIGHT>cm.
Wardrobe: <ITEMS>, burnt-orange PRISM lanyard with ID badge.

LAYOUT: one sheet showing the SAME <man/woman> four times in a row at identical scale -
front view, three-quarter view, side view, back view - full body, standing straight,
all four with their feet flat on one shared ground line across the bottom of the image.

MEASURING WALL - draw this exactly the same on every sheet:
Behind the figures, a plain neutral grey studio wall marked with thin horizontal rules
every 10cm, labelled up the left-hand edge in small plain grey numerals: 150, 160, 170,
180, 190, 200. The 200cm rule sits just below the top edge of the image and the ground
line is at the very bottom, so the whole 0-200cm range fills the frame height.
Draw the figure so that THE TOP OF THE HEAD TOUCHES THE <HEIGHT>cm RULE EXACTLY,
leaving clear empty wall above the head up to the 200cm rule.
The wall, the rule spacing and the numerals must be identical and at the same scale on
every character's sheet, so that two sheets can be compared side by side.

Style: stylised British sitcom comic art, clean bold line art, flat muted colour palette,
expressive caricature, cel-shaded.
NO text, NO labels, NO captions anywhere EXCEPT the small height numerals on the wall.
```

**The one rule that matters**: the head touches its own height rule and there is *empty wall
above it*. A character who fills the frame has failed the sheet, however good the face is.

> **Lettering exception.** The standing "no lettering" rule is for **story panels and location
> plates**. Model sheets are reference art and may carry the measuring-wall numerals. Nothing else.

## ✅ DONE

- **All 11 sheets are downloaded and committed** to `character-refs/*_cartoon_sheet.jpg`.
- **Cartoon entities do not re-trigger the filter** that blocked photoreal Jan — confirmed by the
  sheets generating successfully. A cartoon is not a real likeness, as theorised.
- **5 principals have voices** attached in Flow (Jan, Christina, Sharon, Chris, Rick). These
  **already existed** and match this bible exactly — select them, do not create new ones.

## ⚠️ OPEN ITEMS

- **Flow Character entities: 7 of 11 saved** per `HANDOVER.md` §4 — Jan, Christina, Sharon, Chris,
  Rick, Maureen, Gemma. Still to add: **Priya Raghavan, Barbara Whitlock, Dev Osei, Tomasz Wojcik**
  (background roles, no voices needed). Saving the entity is what locks identity across frames.
  ⚠️ This count is unverified against the live project — check Flow before trusting it.
- **Location plates**: ✅ **11 of 12 done and downloaded** to `location-refs/cartoon-plates/`.
  Only **L04 (tower detail)** is missing. This is no longer the bottleneck — see
  `LOCATION_PLATE_SHOT_LIST.md`.
- **Trevor** (data analyst, exists as a photoreal Flow Character) has no cartoon sheet and
  appears in no storyboard frame. Add only if he earns a scene.
- **Existing clips are photoreal.** All 17 files in `clips/`, including the three trailer masters,
  need re-rendering in cartoon. Their establishing shots also show a glass skyscraper, which is
  wrong for The Triangle regardless of style. Audio beds and edit structure survive.
