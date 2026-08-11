# 🎬 CIRCLE THE SQUARE — MASTER CARTOON SESSION PROMPT PACK (START FROM F01)
> **Style**: 🎨 **CARTOON** — stylised British sitcom comic art. **NOT photoreal.** See `CARTOON_CAST_BIBLE.md`.
> **Goal**: Single-session generation from Frame F01 to F61 to lock in 100% character visual consistency.
> **Platform**: **Google Flow** (Nano Banana 2) using the saved cartoon **Character entities** — that is what locks identity.
> CLI `generate_image` stays first choice while its quota holds; there, attach the cartoon sheets as `@tag` references.
> See `.agents/rules/cli_image_quota_rules.md` §0 — that rule overrides anything below.
> **Instructions**:
> 1. Run one continuous session so art style and character memory carry across frames.
> 2. For each frame, select the saved Flow Character entity (or pass the cartoon sheet in the CLI) for each `@tag`.
> 3. Send the **GLOBAL STYLE ANCHOR** + **FRAME PROMPT**.
> 4. Save each output as `storyboard-frames/Fxx.jpg` (e.g. `F01.jpg`, `F02.jpg`).
> 5. **CLI quota:** 12 images per rolling 4-hour window. On `429 RESOURCE_EXHAUSTED`, report the reset time and switch to Google Flow; return to the CLI once the window clears.
> 6. Each approved frame then becomes the **first frame of a Veo camera move** — describe only the move, not the content.

> ⛔ **Do not attempt photoreal characters.** Flow blocked photoreal Jan Peach three times — likeness
> protection on a real face, not content policy. Cartoon generated first try. See `HANDOVER.md` §2.

---

## 🎨 GLOBAL STYLE ANCHOR
*(Include this anchor in every prompt)*

```text
Stylised British sitcom comic art, clean bold line art, flat muted colour palette, expressive caricature, cel-shaded. NOT photorealistic. Single still frame. 2.39:1 widescreen crop. Character appearance must exactly match attached @-tagged reference images. Absolutely NO text, NO speech bubbles, NO captions, NO labels, NO lettering of any kind anywhere in the image.
```

**Also holds for every frame:** the company is **PRISM** (never Peach Corp) · the building is **low-rise
Cambridge, not London** (no Shard, no Gherkin, no Tower Bridge) · house accent burnt orange `#B0381F` on
every lanyard · **no lettering in panels**, the viewer draws its own speech bubbles · Flow renders **16:9**,
so crop to 2.39:1 after or accept it.

---

## 👥 CHARACTER IDENTITY ANCHORS
> Full specs in `CARTOON_CAST_BIBLE.md`. Sheets live in `character-refs/*_cartoon_sheet.jpg`.

* **`@jan`**: Jan Peach (52, CEO, soft overweight build, gut straining his shirt, thinning grey-brown comb-over, ruddy complexion, smug half-smile, navy suit, silver-grey tie, orange PRISM lanyard, oversized watch).
* **`@christina`**: Christina Dross (38, Comms Lead, slim and upright, sharp dark brown chin-length bob with blunt fringe, charcoal-navy trouser suit, cream blouse, orange lanyard, calm and dry).
* **`@sharon`**: Sharon Enfield (34, staff, curvy, shoulder-length wavy auburn hair, emerald green blouse, black pencil skirt, gold hoops, orange lanyard, unbothered).
* **`@chris`**: Chris (32, staff, lean, short dark brown hair swept up, light stubble, light blue button-down with sleeves rolled, charcoal trousers, orange lanyard, deadpan half-smirk).
* **`@rick`**: Rick (40, staff, sturdy broad muscular build, short salt-and-pepper hair, grey polo, navy work trousers, orange lanyard, flat deadpan, arms crossed). **Not security** — he is rank-and-file staff with a concealed prop taser in F57/F58/F61.
* **`@maureen`**: Maureen (58, canteen worker, sturdy, short greying curly hair pinned back, reading glasses on a chain, beige apron over white polo, kindly but no-nonsense). F47, F48, F51.

---

# 🎬 SCENE 1 — INT. JAN'S EXECUTIVE OFFICE — DAY
*Location Reference:* `@office` → `location-refs/jan_office_location_sheet.jpg`

### **F01** (Shot 01 — Wide Establishing, Greeting)
* **Attachments:** `@jan`, `@christina`, `@office`
* **Prompt:**
  `Stylised British sitcom comic art, clean bold line art, flat muted colour palette, expressive caricature, cel-shaded. NOT photorealistic. Single still frame. 2.39:1 widescreen crop. NO text or lettering anywhere. Wide still in executive office @office. @christina (38-year-old female, sharp dark bob haircut, charcoal blazer) enters and stands opposite @jan's desk, relaxed and professional. @jan (52-year-old male corporate executive, soft build, comb-over hair, navy suit) looks up from his desk toward her.`
* 💬 **Christina:** "Morning Jan. Survive the weekend?"

### **F02** (Shot 01 — Jan sighs)
* **Attachments:** `@jan`, `@office`
* **Prompt:**
  `Stylised British sitcom comic art, clean bold line art, flat muted colour palette, expressive caricature, cel-shaded. NOT photorealistic. Single still frame. 2.39:1 widescreen crop. NO text or lettering anywhere. Medium still on @jan (52-year-old male corporate executive, soft build, comb-over hair, navy suit) leaning back in his desk chair with a put-upon, exhausted expression, small sigh.`
* 💬 **Jan:** "Barely. Another day dealing with these morons..."

### **F03** (Shot 02 — Christina Pitches Idea)
* **Attachments:** `@christina`
* **Prompt:**
  `Stylised British sitcom comic art, clean bold line art, flat muted colour palette, expressive caricature, cel-shaded. NOT photorealistic. Single still frame. 2.39:1 widescreen crop. NO text or lettering anywhere. Medium close-up on @christina (38-year-old female, sharp dark bob haircut, charcoal blazer), upright, businesslike and mid-pitch holding a tablet.`
* 💬 **Christina:** "I see. Well, I might be able to help with that. I have an idea..."

### **F04** (Shot 02 — Jan Listens)
* **Attachments:** `@jan`
* **Prompt:**
  `Stylised British sitcom comic art, clean bold line art, flat muted colour palette, expressive caricature, cel-shaded. NOT photorealistic. Single still frame. 2.39:1 widescreen crop. NO text or lettering anywhere. Medium close-up on @jan (52-year-old male corporate executive, soft build, comb-over hair, navy suit), leaning forward slightly, genuinely curious.`
* 💬 **Jan:** "I'm listening."

### **F05** (Shot 02 — Christina Explains Breakfast Meeting)
* **Attachments:** `@christina`
* **Prompt:**
  `Stylised British sitcom comic art, clean bold line art, flat muted colour palette, expressive caricature, cel-shaded. NOT photorealistic. Single still frame. 2.39:1 widescreen crop. NO text or lettering anywhere. Medium close-up on @christina (38-year-old female, dark bob, charcoal blazer), explaining calmly and matter-of-factly with one hand gesturing.`
* 💬 **Christina:** "Well, every two weeks on a Friday we do a 'breakfast meeting' and offer some pastries loaded with sugar..."

### **F06a** (Shot 03 — Jan Enthused)
* **Attachments:** `@jan`
* **Prompt:**
  `Stylised British sitcom comic art, clean bold line art, flat muted colour palette, expressive caricature, cel-shaded. NOT photorealistic. Single still frame. 2.39:1 widescreen crop. NO text or lettering anywhere. Medium close-up on @jan (52-year-old male, soft build, comb-over hair, navy suit), eyes lighting up with steepled fingers, enthused.`
* 💬 **Jan:** "I am liking the idea of this so far! Strategic MBA thinking!"

### **F06b** (Shot 03 — Jan Gesturing)
* **Attachments:** `@jan`
* **Prompt:**
  `Stylised British sitcom comic art, clean bold line art, flat muted colour palette, expressive caricature, cel-shaded. NOT photorealistic. Single still frame. 2.39:1 widescreen crop. NO text or lettering anywhere. Medium close-up on @jan (52-year-old male, soft build, comb-over hair, navy suit), gesturing with an open hand, smugly convinced of his own brilliance.`
* 💬 **Jan:** "This is exactly the kind of strategic thinking they don't teach you unless you've got a real MBA."

### **F07** (Shot 04 — Christina Dry Reply)
* **Attachments:** `@christina`, `@jan`
* **Prompt:**
  `Stylised British sitcom comic art, clean bold line art, flat muted colour palette, expressive caricature, cel-shaded. NOT photorealistic. Single still frame. 2.39:1 widescreen crop. NO text or lettering anywhere. Over-the-shoulder still behind @jan toward @christina (38-year-old female, dark bob, charcoal blazer). Her expression is completely flat and dry.`
* 💬 **Christina:** "Diminishing returns don't really apply if there were no returns to begin with."

### **F08** (Shot 05 — Jan "Make It So")
* **Attachments:** `@jan`
* **Prompt:**
  `Stylised British sitcom comic art, clean bold line art, flat muted colour palette, expressive caricature, cel-shaded. NOT photorealistic. Single still frame. 2.39:1 widescreen crop. NO text or lettering anywhere. Medium close-up on @jan (52-year-old male, soft build, comb-over hair, navy suit), brisk and dismissive, waving his hand.`
* 💬 **Jan:** "Great. Make it so."

### **F09** (Shot 05 — Christina Confused)
* **Attachments:** `@christina`
* **Prompt:**
  `Stylised British sitcom comic art, clean bold line art, flat muted colour palette, expressive caricature, cel-shaded. NOT photorealistic. Single still frame. 2.39:1 widescreen crop. NO text or lettering anywhere. Medium close-up on @christina (38-year-old female, dark bob haircut), a flicker of genuine confusion crossing her flat expression.`
* 💬 **Christina:** "I am sorry, what?"

### **F10** (Shot 05 — Jan Star Trek Reference)
* **Attachments:** `@jan`
* **Prompt:**
  `Stylised British sitcom comic art, clean bold line art, flat muted colour palette, expressive caricature, cel-shaded. NOT photorealistic. Single still frame. 2.39:1 widescreen crop. NO text or lettering anywhere. Medium close-up on @jan (52-year-old male, soft build, comb-over hair, navy suit), mildly incredulous.`
* 💬 **Jan:** "You never seen Star Trek Next Generation?"

### **F11** (Shot 05 — Christina Sarcasm)
* **Attachments:** `@christina`
* **Prompt:**
  `Stylised British sitcom comic art, clean bold line art, flat muted colour palette, expressive caricature, cel-shaded. NOT photorealistic. Single still frame. 2.39:1 widescreen crop. NO text or lettering anywhere. Medium close-up on @christina (38-year-old female, dark bob haircut), deadpan with heavy sarcasm.`
* 💬 **Christina:** "Shockingly no."

### **F12** (Shot 06 — Jan Dismisses Her)
* **Attachments:** `@jan`
* **Prompt:**
  `Stylised British sitcom comic art, clean bold line art, flat muted colour palette, expressive caricature, cel-shaded. NOT photorealistic. Single still frame. 2.39:1 widescreen crop. NO text or lettering anywhere. Medium close-up on @jan (52-year-old male, soft build, comb-over hair, navy suit), waving a hand toward the door.`
* 💬 **Jan:** "Fine, just make it happen. Now get out, I have got to prepare..."

### **F13** (Shot 06 — Christina Needles Him)
* **Attachments:** `@christina`
* **Prompt:**
  `Stylised British sitcom comic art, clean bold line art, flat muted colour palette, expressive caricature, cel-shaded. NOT photorealistic. Single still frame. 2.39:1 widescreen crop. NO text or lettering anywhere. Medium close-up on @christina (38-year-old female, dark bob haircut), one eyebrow raised, needling him on her way out.`
* 💬 **Christina:** "Is this another one of your poorly rehearsed presentations?"

### **F14** (Shot 07 — Jan Offended)
* **Attachments:** `@jan`
* **Prompt:**
  `Stylised British sitcom comic art, clean bold line art, flat muted colour palette, expressive caricature, cel-shaded. NOT photorealistic. Single still frame. 2.39:1 widescreen crop. NO text or lettering anywhere. Tight close-up on @jan (52-year-old male, soft build, comb-over hair), visibly offended, sitting up straight.`
* 💬 **Jan:** "Jesus! Everyone thinks they know better than me! I am the one with the MBA..."

### **F15** (Shot 07 — Christina Interrupts)
* **Attachments:** `@christina`
* **Prompt:**
  `Stylised British sitcom comic art, clean bold line art, flat muted colour palette, expressive caricature, cel-shaded. NOT photorealistic. Single still frame. 2.39:1 widescreen crop. NO text or lettering anywhere. Medium close-up on @christina (38-year-old female, dark bob haircut), cutting him off mid-sentence with a flat delivery.`
* 💬 **Christina:** "Made Up Place?"

### **F16** (Shot 07 — Jan Explodes)
* **Attachments:** `@jan`
* **Prompt:**
  `Stylised British sitcom comic art, clean bold line art, flat muted colour palette, expressive caricature, cel-shaded. NOT photorealistic. Single still frame. 2.39:1 widescreen crop. NO text or lettering anywhere. Tight close-up on @jan (52-year-old male, soft build, comb-over hair), face fully flushed red, screaming furiously, neck veins bulging.`
* 💬 **Jan (screaming):** "GET OUT NOW YOU STUPID COW! JUST GET THAT DAMN MEETING ORGANISED!"

### **F17** (Shot 08 — Christina Exits Calmly)
* **Attachments:** `@christina`
* **Prompt:**
  `Stylised British sitcom comic art, clean bold line art, flat muted colour palette, expressive caricature, cel-shaded. NOT photorealistic. Single still frame. 2.39:1 widescreen crop. NO text or lettering anywhere. Wide still. @christina (38-year-old female, dark bob haircut, charcoal blazer) walks out and shuts the glass office door calmly behind her, unbothered.`

### **F18** (Shot 09 — Jan Flustered Unbuttoning Shirt)
* **Attachments:** `@jan`
* **Prompt:**
  `Stylised British sitcom comic art, clean bold line art, flat muted colour palette, expressive caricature, cel-shaded. NOT photorealistic. Single still frame. 2.39:1 widescreen crop. NO text or lettering anywhere. Medium close-up on @jan (Jan Peach, 52-year-old male corporate executive with soft build, thinning brown comb-over hair, navy suit), alone behind his desk, flustered and sweating profusely, mid-motion unbuttoning his shirt collar and tie.`

### **F19** (Shot 09 — Jan Shirt Fully Off)
* **Attachments:** `@jan`
* **Prompt:**
  `Stylised British sitcom comic art, clean bold line art, flat muted colour palette, expressive caricature, cel-shaded. NOT photorealistic. Single still frame. 2.39:1 widescreen crop. NO text or lettering anywhere. Wide still. @jan (Jan Peach, 52-year-old male corporate executive, soft build, comb-over hair) has pulled his navy suit shirt fully off, chest bared with black necktie around his neck, mid-motion dropping the shirt onto his desk.`

### **F20** (Shot 10 — Sharon Enters Unannounced)
* **Attachments:** `@jan`, `@sharon`
* **Prompt:**
  `Stylised British sitcom comic art, clean bold line art, flat muted colour palette, expressive caricature, cel-shaded. NOT photorealistic. Single still frame. 2.39:1 widescreen crop. NO text or lettering anywhere. Wide still. @sharon (Sharon Enfield, 34-year-old female with auburn hair and emerald green blouse) opens the glass door walking in unannounced. Shirtless @jan (52-year-old male, soft build, comb-over hair, tie around neck) spins around in shock.`
* 💬 **Jan:** "BLOODY HELL SHARON. KNOCK ON THE DOOR WILL YOU!"

---

> Full Session Pack generated in `C:\kontitemp\ai\circle_the_square\MASTER_STORYBOARD_SESSION_PROMPTS.md`.
