# 🎞️ CIRCLE THE SQUARE — FEATURETTE STORYBOARD / FLIPBOOK IMAGE PROMPTS
> **"Project Inception" — Nano Banana Still-Frame Flipbook Workflow**
> **Source of truth**: `CTS_Featurette_Episode.fountain` (the full screenplay)
> **Generator**: Nano Banana (Gemini image model) via the **CLI `generate_image` tool ONLY — no browser, no AI Studio** (see `.agents/rules/cli_image_quota_rules.md` §0). Not the metered API script, not Flow, not fal.ai. Every frame passes its own reference images, tagged with `@name` so the model knows who's who.
> **Viewer**: `storyboard_slideshow.html` (same folder) — scene-by-scene comic-style viewer with speech bubbles, since video rendering has been unreliable.
> **Total Frames**: 64 (across 35 shots / 3 scenes)
> **Status**: DRAFT v3 — Nano Banana `@tag` attachment format

---

## 🧭 HOW TO USE THIS DOC

1. Pick the next frame, in order, **one at a time — no batching. Quota is 12 images per rolling 4-hour window; on `429 RESOURCE_EXHAUSTED`, stop and wait for the reset rather than switching tools.**
2. In one continuous CLI session, pass that frame's attachment images **in the order listed**, matching each to its `@tag`.
3. Send the **IMAGE STYLE ANCHOR** + that frame's **PROMPT** (already written using the `@tags`).
4. Generate, approve or reroll.
5. Save the result as `storyboard-frames/<FRAME ID>.jpg` (e.g. `storyboard-frames/F01.jpg`) — the slideshow picks it up automatically on refresh.
6. Tick the frame off in the tracker below.

**Action only, no re-description**: prompts don't restate appearance — that's what the attached reference images are for. Continuity state flags (shirt on/off, dishevelment) are kept since Nano Banana can't infer plot state from a static identity sheet.

---

## 🏷️ @TAG ATTACHMENT LEGEND
> Master list — every `@tag` used below maps to exactly one of these files.

| Tag | File | Type |
|---|---|---|
| `@jan` | `character-refs/jan_peach_identity_sheet.jpg` | Character |
| `@christina` | `character-refs/christina_dross_identity_sheet.jpg` | Character |
| `@sharon` | `character-refs/sharon_enfield_identity_sheet.jpg` | Character |
| `@chris` | `character-refs/chris_identity_sheet.jpg` | Character |
| `@rick` | `character-refs/rick_identity_sheet.jpg` | Character |
| `@office` | `location-refs/jan_office_location_sheet.jpg` | Location (Scene 1) |
| `@openplan` | `location-refs/open_plan_floor_location_sheet.jpg` | Location (Scene 2) |
| `@canteen` | `location-refs/canteen_location_sheet.jpg` | Location (Scene 3) |

> **No reference sheet exists yet for the Canteen Worker** (walk-on role). For F47/F48/F51, don't attach a character image for them — just describe minimally in-prompt as "a canteen worker in a beige apron" and let Nano Banana invent it, or generate a quick identity sheet for them first if you want continuity across their 3 frames.

---

## 🎨 IMAGE STYLE ANCHOR
> Paste into EVERY still prompt.

```
Photoreal single film-still frame, not video. Documentary British mockumentary photographic tone. Natural Northern European daylight. Shallow depth of field on close-ups, deep focus on wides. No visible real-world branding or crests. 2.39:1 cinematic widescreen still crop. Character appearance must exactly match the attached @-tagged reference images — do not invent or alter appearance, age, or wardrobe colour beyond what this prompt specifies as a state change (e.g. shirt off, dishevelled). Location architecture must match the attached location reference.
```

---

## 📋 FRAME TRACKER

| Frame | Shot | Scene | Beat | Status |
|---|---|---|---|---|
| F01 | S01 | 1 | Wide establishing — Christina enters, greets Jan | ✅ |
| F02 | S01 | 1 | Jan sighs — "Barely..." | ✅ |
| F03 | S02 | 1 | Christina pitches — "I have an idea..." | ✅ |
| F04 | S02 | 1 | Jan — "I'm listening." | ✅ |
| F05 | S02 | 1 | Christina explains breakfast-meeting concept | ✅ |
| F06a | S03 | 1 | Jan enthused, steepled fingers | ✅ |
| F06b | S03 | 1 | Jan gesturing, MBA name-drop | ✅ |
| F07 | S04 | 1 | Christina deadpan — "Diminishing returns..." | ✅ |
| F08 | S05 | 1 | Jan — "Great. Make it so." | ✅ |
| F09 | S05 | 1 | Christina confused — "I am sorry, what?" | ✅ |
| F10 | S05 | 1 | Jan — Star Trek reference | ✅ |
| F11 | S05 | 1 | Christina — "Shockingly no." | ✅ |
| F12 | S06 | 1 | Jan dismisses — "Fine, just make it happen..." | ✅ |
| F13 | S06 | 1 | Christina — "poorly rehearsed presentations?" | ✅ |
| F14 | S07 | 1 | Jan offended — "MBA from the University of --" | ✅ |
| F15 | S07 | 1 | Christina cuts in — "Made Up Place?" | ✅ |
| F16 | S07 | 1 | Jan screams — "GET OUT NOW YOU STUPID COW!" | ✅ |
| F17 | S08 | 1 | Christina exits calmly, door shuts | ✅ |
| F18 | S09 | 1 | Jan unbuttons shirt, flustered/sweating | ⬜ |
| F19 | S09 | 1 | Jan removes shirt, arrow revealed | ⬜ |
| F20 | S10 | 1 | Sharon enters unannounced — Jan reacts | ✅ |
| F21 | S11 | 1 | Sharon glances at the arrow | ⬜ |
| F22 | S11 | 1 | Jan frozen, mortified | ⬜ |
| F23 | S12 | 1 | Sharon — "breakfast meetings now." | ⬜ |
| F24 | S13 | 1 | Jan brushes her off | ⬜ |
| F25 | S13 | 1 | Sharon — "I have needs too Jan..." | ⬜ |
| F26a | S14 | 1 | Jan yanks blinds shut | ⬜ |
| F26b | S14 | 1 | Jan locks the door | ⬜ |
| F27 | S15 | 2 | Chris & Rick establishing 2-shot | ⬜ |
| F28 | S16 | 2 | Chris — "don't even try to hide it..." | ⬜ |
| F29 | S16 | 2 | Rick flat — "Give it another five minutes." | ⬜ |
| F30 | S17 | 2 | Sharon walks past, dishevelled | ⬜ |
| F31 | S18 | 2 | Jan emerges, claps hands | ⬜ |
| F32 | S19 | 2 | Chris — "Does Sharon get a pass?" | ⬜ |
| F33 | S19 | 2 | Jan — "personal reasons." | ⬜ |
| F34 | S19 | 2 | Crowd sniggers | ⬜ |
| F35 | S20 | 2 | Jan shouts — "SHUT UP!... new project required" | ⬜ |
| F36 | S21 | 2 | Rick — "isn't it ongoing?... completely failing." | ⬜ |
| F37a | S22 | 2 | Jan justifies previous project | ⬜ |
| F37b | S22 | 2 | Jan names it — "Project Inception" | ⬜ |
| F38 | S23 | 2 | Chris — "You're dreaming Jan!" | ⬜ |
| F39 | S23 | 2 | Jan — "What?!" | ⬜ |
| F40 | S23 | 2 | Chris — "film about dreams Jan." | ⬜ |
| F41 | S23 | 2 | Jan flustered backpedal | ⬜ |
| F42 | S24 | 2 | INSERT — 1,000 "PROJECT INCEPTION" stress balls/pens/tees | ⬜ |
| F43 | S25 | 2 | Chris — "Will there be a lead?" | ⬜ |
| F44 | S25 | 2 | Jan — "filled... by me." | ⬜ |
| F45 | S25 | 2 | Crowd groans | ⬜ |
| F46 | S26 | 2 | Jan — "£50k to my salary... GET BACK TO WORK!" | ⬜ |
| F47 | S27 | 3 | Canteen establishing, pastries prepped | ⬜ |
| F48 | S28 | 3 | Last pastry claimed, tray empty | ⬜ |
| F49 | S29 | 3 | Jan strides into canteen | ⬜ |
| F50 | S29 | 3 | Jan — "any more pain au chocolat?" | ⬜ |
| F51 | S29 | 3 | Canteen Worker — "Sorry, all gone." | ⬜ |
| F52 | S30 | 3 | Jan — "OH THAT IS IT!" | ⬜ |
| F53 | S31 | 3 | Jan sweeps plates off counter | ⬜ |
| F54 | S31 | 3 | Plates shattered, crowd frozen | ⬜ |
| F55 | S32 | 3 | Jan screams — "I HAVE AN MBA..." | ⬜ |
| F56 | S33 | 3 | Chair hurled through window | ⬜ |
| F57 | S34 | 3 | Jan reaches for 2nd chair, Rick raises taser | ⬜ |
| F58 | S34 | 3 | INSERT — taser POP-CRACKLE flash | ⬜ |
| F59 | S34 | 3 | Jan slumps face-down, unconscious | ⬜ |
| F60 | S35 | 3 | Chris crouches — "Have you killed him?" | ⬜ |
| F61 | S35 | 3 | Rick stows taser, answers calmly | ⬜ |

> Update Status: ⬜ PENDING → ✅ APPROVED → ❌ REJECTED → 🔄 REGENERATING

---
---

# SCENE 1 — INT. JAN'S OFFICE — DAY
**Scene attachment (all frames):** `@office` → `location-refs/jan_office_location_sheet.jpg`

---

### S01 — Wide Establishing, Greeting
**Attach:** `@jan`, `@christina`, `@office`

**F01**
```
Wide still. @christina enters and stands opposite @jan's desk, mid-greeting, relaxed and professional. @jan looks up from his desk toward her, in @office. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Christina:** "Morning Jan. Survive the weekend?"

**F02**
```
Same framing, slightly closer on @jan. He gives a small sigh, leaning back in his chair with a put-upon expression. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Jan (sighing):** "Barely. Another day dealing with these morons who cannot understand the discipline and brilliance it takes to run a place like this."

**Continuity:** Jan shirt buttoned, composed. Christina composed.

---

### S02 — Christina Pitches the Idea
**Attach:** `@christina`, `@jan`

**F03**
```
Medium close-up on @christina, upright and businesslike, mid-pitch, tablet in hand. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Christina:** "I see. Well, I might be able to help with that. I have an idea to help us communicate better with the whole department."

**F04**
```
Medium close-up on @jan, leaning forward slightly, genuinely curious. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Jan:** "I'm listening."

**F05**
```
Medium close-up on @christina, explaining calmly and matter-of-factly, one hand gesturing slightly to illustrate the plan. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Christina:** "Well, every two weeks on a Friday we do a 'breakfast meeting' and offer some pastries or some other junk loaded with as much sugar as humanly possible, and we give a talk about whatever for thirty mins. We then take any questions and pretend to listen."

---

### S03 — Jan's Enthusiastic Response
**Attach:** `@jan`

**F06a**
```
Medium close-up. @jan's eyes light up, fingers steepling, chin raised — genuinely enthused and already congratulating himself. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Jan (enthused):** "I am liking the idea of this so far. Especially if we ensure that the sugar in the breakfast junk is just enough to pacify the workers' brains so as not to care what we are talking about, but not too much so as to result in no actual work being done afterwards."

**F06b**
```
Same medium close-up, slightly closer. @jan gestures with one open hand, utterly convinced of his own brilliance. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Jan (continuing):** "This is exactly the kind of strategic thinking they don't teach you unless you've got a real MBA."

**Continuity:** Shirt buttoned, not yet stressed.

---

### S04 — Christina's Deadpan Reply
**Attach:** `@christina`, `@jan`

**F07**
```
Over-the-shoulder still from behind @jan toward @christina. Her expression is completely flat and dry, delivering the line without any change in composure. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Christina (dry):** "Thought you would like it. Friday statistically is the least productive day anyway, so we could just up the sugar content as much as we like. Diminishing returns don't really apply if there were no returns to begin with."

---

### S05 — Quick Exchange: "Make It So" / Star Trek
**Attach:** `@jan`, `@christina`

**F08**
```
Medium close-up on @jan, brisk and dismissive, already moving on. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Jan:** "Great. Make it so."

**F09**
```
Medium close-up on @christina, a flicker of genuine confusion crossing her usually flat expression. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Christina:** "I am sorry, what?"

**F10**
```
Medium close-up on @jan, mildly incredulous that she doesn't get the reference. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Jan:** "You never seen Star Trek Next Generation?"

**F11**
```
Medium close-up on @christina, deadpan with heavy sarcasm, barely masking irritation. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Christina (heavy sarcasm):** "Shockingly no."

---

### S06 — Jan Dismisses Her
**Attach:** `@jan`, `@christina`

**F12**
```
Medium close-up on @jan, waving a hand toward the door, already distracted by his next task. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Jan:** "Fine, just make it happen. Start tomorrow with the first meeting. Now get out, I have got to prepare for a short presentation to the whole staff in a few mins."

**F13**
```
Medium close-up on @christina, one eyebrow raised, needling him on her way out. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Christina:** "Is this another one of your poorly rehearsed presentations?"

---

### S07 — MBA Insult, Jan Explodes
**Attach:** `@jan`, `@christina`

**F14**
```
Tight close-up on @jan, visibly offended, sitting up straighter, starting to bristle. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Jan:** "Jesus! Everyone thinks they know better than me! I am the one with the MBA from the University of --"

**F15**
```
Medium close-up on @christina, cutting him off mid-sentence with a perfectly flat, deadpan delivery. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Christina:** "Made Up Place?"

**F16**
```
Tight close-up on @jan, face fully flushed red, screaming, veins visible at the neck. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Jan (screaming, red-faced):** "GET OUT NOW YOU STUPID COW! JUST GET THAT DAMN MEETING ORGANISED!"

**Continuity:** First visible face-reddening — bridges into the sweating/shirt-off stress arc.

---

### S08 — Christina Exits Calmly
**Attach:** `@christina`

**F17**
```
Wide still. @christina walks out and shuts the glass door calmly behind her — completely unbothered, not even a flinch. [PASTE IMAGE STYLE ANCHOR HERE]
```
🔇 *(no dialogue — door click, calm exit)*

---

### S09 — Jan Removes His Shirt
**Attach:** `@jan`

**F18**
```
Medium close-up. @jan, alone now, flustered and sweating profusely, begins unbuttoning his shirt. [PASTE IMAGE STYLE ANCHOR HERE]
```
🔇 *(no dialogue)*

**F19**
```
Wide still. @jan has pulled the shirt fully off, chest bared, mid-motion dropping it. [PASTE IMAGE STYLE ANCHOR HERE]
```
🔇 *(no dialogue — silent visual gag beat)*

**Continuity:** Shirt fully OFF. Comedy peak — needs to land visually.

---

### S10 — Sharon Enters Unannounced
**Attach:** `@jan`, `@sharon`

**F20**
```
Wide still. The door has just opened — @sharon walks in without knocking. @jan, shirtless, spins toward her in alarm. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Jan:** "BLOODY HELL SHARON. KNOCK ON THE DOOR WILL YOU!"

**Continuity:** Sharon State A (composed) — arrival state.

---

### S11 — The Arrow Reveal
**Attach:** `@sharon`, `@jan`

**F21**
```
Medium close-up on @sharon, eyes flicking briefly down toward Jan's chest, expression staying completely neutral. [PASTE IMAGE STYLE ANCHOR HERE]
```
🔇 *(no dialogue — beat)*

**F22**
```
Medium close-up on @jan, frozen in mortified realisation that she's seen it. [PASTE IMAGE STYLE ANCHOR HERE]
```
🔇 *(no dialogue — reaction beat)*

**Continuity:** Sharon's expression neutral, NOT shocked/laughing. Jan's manscaped arrow (already on his identity sheet) must be visible here.

---

### S12 — Sharon States Her Business
**Attach:** `@sharon`

**F23**
```
Medium close-up on @sharon, flat and transactional, as if nothing unusual is happening. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Sharon (unbothered):** "I hear Christina is doing breakfast meetings now."

---

### S13 — Jan Brushes Her Off, Sharon Pushes Back
**Attach:** `@jan`, `@sharon`

**F24**
```
Medium close-up on @jan, flustered, trying to wave her off while still half-undressed. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Jan:** "I really don't have time for this now Sharon. I can't make any concessions for you to have some other nonsensical meeting --"

**F25**
```
Medium close-up on @sharon, flat and matter-of-fact, unmoved by his protest. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Sharon:** "Well I have needs too Jan that must be met."

---

### S14 — Jan Locks the Room Down
**Attach:** `@jan`

**F26a**
```
Medium close-up. @jan, shirtless and sweating, yanks the venetian blinds down with both hands, urgent. [PASTE IMAGE STYLE ANCHOR HERE]
```
🔇 *(no dialogue — blind mechanical slam-drop)*

**F26b**
```
Medium close-up. @jan turns and locks the office door. [PASTE IMAGE STYLE ANCHOR HERE]
```
🔇 *(no dialogue — door lock click. Cut to corridor.)*

**Continuity:** Shirt still off — last frame of Scene 1.

---
---

# SCENE 2 — INT. CORRIDOR / OPEN-PLAN FLOOR — CONTINUOUS
**Scene attachment (all frames):** `@openplan` → `location-refs/open_plan_floor_location_sheet.jpg`

---

### S15 — Chris & Rick Establishing
**Attach:** `@chris`, `@rick`, `@openplan`

**F27**
```
Wide still. @chris and @rick stand by a desk run in @openplan, relaxed, mid-conversation. [PASTE IMAGE STYLE ANCHOR HERE]
```
🔇 *(no dialogue — establishing)*

---

### S16 — The Dry Exchange
**Attach:** `@chris`, `@rick`

**F28**
```
Medium close-up on @chris, dry smirk, delivering the line to Rick. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Chris:** "Christ! They don't even try to hide it any more do they."

**F29**
```
Medium close-up on @rick, completely flat, unbothered, responding without missing a beat. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Rick (flat):** "Never have. Give it another five minutes."

---

### S17 — Sharon Walks Past, Dishevelled
**Attach:** `@sharon`, `@chris`, `@rick`

**F30**
```
Wide still. @sharon walks past @chris and @rick, dripping sweat, hair and makeup visibly dishevelled, unhurried and unbothered. They watch her go. [PASTE IMAGE STYLE ANCHOR HERE]
```
🔇 *(no dialogue — footsteps/ambient)*

**Continuity:** Sharon State B — dishevelled, sweat visible, hair/makeup mussed.

---

### S18 — Jan Emerges, Claps for Attention
**Attach:** `@jan`, `@openplan`

**F31**
```
High-angle wide still. @jan emerges onto the open-plan floor, shirt re-buttoned visibly askew, clapping his hands loudly to summon everyone. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Jan:** "Right guys, as you know --"

**Continuity:** Shirt re-buttoned askew — visible continuity from F26b.

---

### S19 — Chris Asks About Sharon
**Attach:** `@chris`, `@jan`

**F32**
```
Medium close-up on @chris, needling, half-smirking, calling out from the crowd. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Chris:** "Does Sharon get a pass on attending this?"

**F33**
```
Medium close-up on @jan, caught slightly off guard, covering quickly. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Jan:** "Err... yes she does. I have given her the rest of the day off for personal reasons."

**F34**
```
Wide still of the gathered crowd in @openplan, quiet sniggering rippling through several workers. [PASTE IMAGE STYLE ANCHOR HERE]
```
🔇 *(no dialogue — sniggering ripple)*

---

### S20 — Jan Shouts Them Down
**Attach:** `@jan`

**F35**
```
Medium close-up on @jan, flushed, snapping at the crowd, gesturing sharply. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Jan (flushed):** "SHUT UP! I am truly appalled by the lack of discipline in this place and that changes now! I have decided a new project is required to manage all the change around here."

---

### S21 — Rick's Skeptical Question
**Attach:** `@rick`

**F36**
```
Medium close-up on @rick, arms crossed, flat and pointed. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Rick:** "What happened to the last project for this, isn't it ongoing? By that I mean completely failing."

---

### S22 — Jan Announces "Project Inception"
**Attach:** `@jan`

**F37a**
```
Medium close-up on @jan, defensive and blustering, justifying himself with total conviction. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Jan:** "There's no need for the previous project as everything has been a great success even though most things were not delivered on time or within budget. I know because I see everything happening so am best placed to judge."

**F37b**
```
Same medium close-up, closer, peak self-satisfaction as he announces the name. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Jan (continuing):** "We need a new project to continue the success of the previous project. So I have decided to call the project Inception."

---

### S23 — Chris's Joke Lands
**Attach:** `@chris`, `@jan`

**F38**
```
Medium close-up on @chris, shouting out to the laughing crowd, delighted. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Chris (shouting to laughter):** "You're dreaming Jan!"

**F39**
```
Medium close-up on @jan, confused, thrown off. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Jan:** "What?!"

**F40**
```
Medium close-up on @chris, explaining with a smirk. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Chris:** "Inception is the name of a film about dreams Jan."

**F41**
```
Medium close-up on @jan, flustered, backpedalling, trying to save face. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Jan (flustered):** "Oh, well it is also the name of this project."

---

### S24 — The Merch Reveal (Sight Gag)
**Attach:** *(none — prop insert only)*

**F42**
```
Close-up insert still of a stack of branded merchandise — stress balls, pens, and t-shirts all printed with "PROJECT INCEPTION" — already boxed and ready, implying it was ordered before this meeting even happened. [PASTE IMAGE STYLE ANCHOR HERE]
```
🔇 *(no dialogue — visual sight gag; narration option: "...it is too late to change the name, as he has already ordered 1,000 stress balls, pens, and t-shirts.")*

---

### S25 — The Lead Announcement
**Attach:** `@chris`, `@jan`, `@openplan`

**F43**
```
Medium close-up on @chris, genuinely curious this time. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Chris:** "Will there be a lead for this?"

**F44**
```
Medium close-up on @jan, chin raised, savouring the moment. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Jan:** "At last something sensible is asked. Yes there will. However, it is with regret that I have to inform you all that the position has already been filled... by me."

**F45**
```
Wide still of the crowd in @openplan, a collective groan rippling through them. [PASTE IMAGE STYLE ANCHOR HERE]
```
🔇 *(no dialogue — groans)*

---

### S26 — Jan's Closing Rally
**Attach:** `@jan`

**F46**
```
Medium close-up on @jan, defiant, sweating, jabbing a finger for emphasis before turning away. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Jan:** "Yes groan all you like, but I am the one with the most talent and skills to deliver this. It will add £50k to my salary as I simply add this role into my duties. I will let you know when more information is available, now GET BACK TO WORK!"

**Continuity:** End of Scene 2. Time-cut card to follow: "NEXT MORNING."

---
---

# SCENE 3 — INT. STAFF RESTAURANT / CANTEEN — NEXT MORNING
**Scene attachment (all frames):** `@canteen` → `location-refs/canteen_location_sheet.jpg`

---

### S27 — Canteen Establishing
**Attach:** `@canteen` *(no canteen-worker reference sheet — describe minimally, see legend note above)*

**F47**
```
Wide still. Morning canteen, workers seated eating pastries. Canteen staff behind the counter, having prepared a high-sugar batch of pain au chocolat. High demand visible — trays being worked through quickly. [PASTE IMAGE STYLE ANCHOR HERE]
```
🔇 *(no dialogue — cheerful ambient)*

---

### S28 — Last Pastry Claimed
**Attach:** `@canteen`

**F48**
```
Medium close-up/insert still. The tray is now empty, just crumbs — the last pastry has been claimed moments before Jan enters. [PASTE IMAGE STYLE ANCHOR HERE]
```
🔇 *(no dialogue)*

**Continuity:** Empty tray is plot-critical — must be clearly visible.

---

### S29 — Jan Arrives, Asks for Pastries
**Attach:** `@jan`, `@canteen` *(canteen worker: no reference sheet — describe minimally)*

**F49**
```
Handheld tracking still. @jan strides purposefully into the canteen, confident, full suit on. [PASTE IMAGE STYLE ANCHOR HERE]
```
🔇 *(no dialogue — confident footsteps)*

**F50**
```
Handheld medium close-up. @jan reaches the counter, looking around for the pastry tray. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Jan:** "Is there any more pain au chocolat?"

**F51**
```
Medium close-up on a canteen worker in a beige apron behind the counter, apologetic. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Canteen Worker:** "Sorry, all gone."

**Continuity:** Full suit on, rage building from 0%.

---

### S30 — Jan's Rage Trigger
**Attach:** `@jan`

**F52**
```
Tight close-up. @jan's face has gone deep red, a neck vein bulging visibly, expression tipping fully into fury. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Jan (veins bulging):** "OH THAT IS IT!"

---

### S31 — Plates Swept to the Floor
**Attach:** `@jan`

**F53**
```
Wide static still. @jan grabs plates from the counter with both hands, sweeping them violently onto the floor mid-motion. [PASTE IMAGE STYLE ANCHOR HERE]
```
🔇 *(no dialogue — CRASH, china shattering)*

**F54**
```
Wide static still, same angle. China lies shattered across the floor. The entire canteen has gone silent, everyone frozen, staring. [PASTE IMAGE STYLE ANCHOR HERE]
```
🔇 *(no dialogue — dead silence)*

---

### S32 — Jan's Screaming Rant
**Attach:** `@jan`

**F55**
```
Medium close-up/wide still. @jan, deep crimson, sweat-soaked, screaming at full volume, arms wide. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Jan (screaming):** "I HAVE HAD IT WITH THIS PLACE! I HAVE AN MBA, NOBODY APPRECIATES MY IMMENSE TALENT!"

---

### S33 — Chair Through the Window
**Attach:** `@jan`

**F56**
```
Wide static still. @jan hurls a heavy meeting chair into the nearest floor-to-ceiling window — glass mid-shatter around the impact. [PASTE IMAGE STYLE ANCHOR HERE]
```
🔇 *(no dialogue — GLASS SHATTERS)*

**Continuity:** The plate-smash and chair-through-window are the physical comedy climax — must read as shocking.

---

### S34 — The Taser
**Attach:** `@jan`, `@rick`

**F57**
```
Wide static still. @jan turns to grab a second chair. Behind him, @rick has stepped forward, calm, raising a small prop taser toward Jan's back. [PASTE IMAGE STYLE ANCHOR HERE]
```
🔇 *(no dialogue — tense beat)*

**F58**
```
Extreme close-up insert still of the prop taser firing — a brief blue-white electric arc crackle, clearly toy-like/prop quality, comedic not threatening. [PASTE IMAGE STYLE ANCHOR HERE]
```
🔇 *(no dialogue — POP-CRACKLE)*

**F59**
```
Wide static still. @jan has frozen, dropped the chair, and slumped face-first onto the floor, motionless, surrounded by broken china. @rick stands calmly behind him, taser still in hand. [PASTE IMAGE STYLE ANCHOR HERE]
```
🔇 *(no dialogue — single heavy THUD, then silence)*

**Continuity:** Taser prop must read as clearly non-functional/toy-like. Rick's expression flat calm throughout.

---

### S35 — Aftermath (FINAL SHOT)
**Attach:** `@chris`, `@rick`, `@jan`

**F60**
```
Medium two-shot still. @chris crouches down next to the unconscious @jan, looking up at @rick, expression somewhere between concerned and amused. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Chris (crouching down):** "Have you killed him?"

**F61**
```
Same medium two-shot. @rick calmly and methodically stows the prop taser away, expression completely flat and unbothered. [PASTE IMAGE STYLE ANCHOR HERE]
```
💬 **Rick (calmly stowing Taser):** "No relax, he will be out for a while. I knew this Taser would come in useful one day in this place. I think we need the police here..."

**Continuity:** FINAL SHOT. Chris's expression should land the comedy. Rick's flat calm is the punchline. Broken china, cracked window visible in frame.

---
---

## ✂️ POST-PRODUCTION / STITCH ASSEMBLY ORDER

```
F01→F02→F03→F04→F05→F06a→F06b→F07→F08→F09→F10→F11→F12→F13→F14→F15→F16→F17→F18→F19→F20→F21→F22→F23→F24→F25→F26a→F26b
    [SCENE 1 COMPLETE — cut on blinds/lock]
F27→F28→F29→F30→F31→F32→F33→F34→F35→F36→F37a→F37b→F38→F39→F40→F41→F42→F43→F44→F45→F46
    [SCENE 2 COMPLETE — TIME CUT CARD: "NEXT MORNING"]
F47→F48→F49→F50→F51→F52→F53→F54→F55→F56→F57→F58→F59→F60→F61
    [SCENE 3 COMPLETE — FADE OUT]
```

**Viewer**: open `storyboard_slideshow.html` in Chrome to browse scene-by-scene with speech bubbles. It looks for images at `storyboard-frames/<FRAME ID>.jpg` and shows a placeholder until each one exists.

**Reference docs**: `character-bible.html`, `location-bible.html`, `CTS_Featurette_Episode.fountain`
**Superseded**: `featurette_prompt_engine.md`, `featurette_shot_list.md` (Flow/video-prompt attempt)
**TTS voice files**: `qwen3_tts_voice_prompts.json`
