# 🎬 SCENE 4 — THE NEXT DAY

> Four sluglines in `CTS_Featurette_Episode.fountain` (added 2026-09-05, after the Scene 3
> `FADE OUT.`): `INT. JAN'S OFFICE - THE NEXT DAY` → `INT. OPEN-PLAN FLOOR - CONTINUOUS` →
> `INT. HR BREAKOUT ROOM - LATER` → `INT. STAFF CANTEEN - THAT AFTERNOON`. One continuous
> day (day 3 of the story), unlike Scene 3's day jump. Companion to `SCENE3_SHOT_LIST.md`,
> same method, same 2.75 words/sec, 15s ceiling per `.agents/rules/clip_duration_rules.md`.

**51 shots, ~6m40s total runtime estimate.** That's roughly 5x Scene 3 — this scene has a
lot more dialogue by design (four locations, five-plus speaking parts). Flagging the count
up front so it can be trimmed before any generation starts if it's more than wanted.

## Cast — one new character needed

| Who | Status |
|---|---|
| Jan, Christina, Chris, Rick, Sharon, Maureen | Existing refs, no new work |
| **DEBBIE VANCE** (45, HR lanyard, relentless deadpan positivity) | **NEW** — needs a full reference sheet before any HR-breakout-room shot can be generated, same pipeline as Maureen/Sharon got (`generate-cast-refs.js` pattern) |

Wardrobe: Jan is in **DAY 3 WARDROBE** — the same too-tight navy suit jacket (silhouette
stays recognisable, per the Scene 3 decision) over the SAME pale-blue-shirt-plus-dark-red-tie
combo from Scene 3 (he was unconscious in it, nobody re-dressed him), now visibly creased and
re-buttoned wrong, plus a large white foam neck brace. Beat 4 (that afternoon) swaps the brace
for a smaller, "more dignified" version — note this as a mid-scene prop change, not a full
wardrobe reset. Christina, Chris, Rick, Sharon, Maureen: unchanged from their established looks.

## Locations — reuse three, repurpose one, no new location build

| Location in scene | Asset | Plan |
|---|---|---|
| Jan's office | `location-refs/higgsfield/coverage/jan_office/` | Reuse `jan_office_master_wide` / `jan_office_desk_front` directly |
| Open-plan floor | `location-refs/higgsfield/coverage/jan_office_corridor/jan_office_corridor_master_wide.png` | Reuse (same anchor as Scene 2). **New prop-populated angle needed**: Rick's desk with the drawer visible, and the delivery trolley — compose as character-populated plates the way `SCENE2_PLATE_SHOT_LIST.md` did, not raw coverage |
| HR breakout room | `location-refs/higgsfield/coverage/goldfish_meeting_room/` | **Repurpose**, don't build new. This is the small glass "goldfish bowl" meeting room already in the bible (distinct from Jan's office). Add folding chairs facing a wheeled TV/DVD combo unit as a set-dressing addition to `goldfish_meeting_room_master_wide`, same pattern as the venetian blinds added to Location 05 |
| Canteen | `location-refs/higgsfield/coverage/staff_canteen/` | Reuse, but **continuity must carry forward from Scene 3's end state**: the window is now boarded with plywood and a hand-written "DO NOT LEAN ON WINDOW (NEW)" sign — NOT the shattered-glass state from `s3_06`/`s3_07b`. China stacks are back to normal (new plates, day's passed). Maureen is back behind the counter, same wardrobe |

## Continuity state to carry through the scene

- **Jan's neck brace**: large/foam in Beats 1–3, swapped for a smaller one entering Beat 4. Never absent.
- **The Incident Reflection Form**: introduced in Beat 1 (Jan's copy), reappears in Beat 2 as
  the mass hand-out Nina distributes — same prop design both times.
- **PROJECT INCEPTION 2 merch**: first seen as sealed delivery boxes in Beat 2 (Rick/Chris
  reaction only, Jan doesn't see it happen), then opened and in active use (tote bags, mugs,
  banner) in Beat 4. The boxes must visibly match the merch later deployed.
- **The canteen window**: boarded/plywood throughout Beat 4, consistent with Scene 3's final
  state. It must NOT read as freshly broken or as fully repaired glass.
- **Rick's weapons drawer**: established in Beat 2 as bear spray, zip ties, a second taser, a
  flare gun. Not referenced again, but keep the drawer prop design available in case a later
  scene calls back to it.

## Chaining flags — these pairs MUST use `--start-image`, not independent stills

Per `location_continuity_rules.md` ("never let a still-speaking character warp mid-line"),
these are one continuous scripted speech split only by the duration cap:

- `s4_09` → `s4_10` (Jan's "risk management" speech, split mid-thought at "risk management." /
  "I invented it. Well -- not invented.")
- `s4_18` → `s4_19` (Debbie's opening line interrupted by Jan's "Unrelated events." and resumed
  — chain the resume off the interruption shot's last frame, don't re-seed from a fresh plate)

## Beat 1 — INT. JAN'S OFFICE - THE NEXT DAY (15 shots, ~2m07s)

| # | Slug | Line(s) | Words | Est. |
|---|---|---|---|---|
| 1 | `s4_01_neckbrace_establish` | Establishing: Jan alone, neck brace, squeezing stress ball; Christina enters | 0 | ~4s |
| 2 | `s4_02_alive_then` | CHRISTINA "You're alive then. Shame." / JAN "It takes more than eight thousand volts... if you think about it." | 37 | ~13.5s |
| 3 | `s4_03_forty_witnesses` | CHRISTINA "Rick tasered you in front of forty witnesses... extractor fan." / JAN "Yes, well. Nolan films are famously misunderstood on first viewing." | 36 | ~13.1s |
| 4 | `s4_04_crumb_ratio` | CHRISTINA "It wasn't a film, Jan... pain au chocolat crumbs." / JAN "Did I get a good crumb-to-face ratio? I don't remember that part." | 35 | ~12.7s |
| 5 | `s4_05_for_the_file` | CHRISTINA "Ninety percent coverage. HR has photos. For the file." / JAN "There's a FILE?!" | 13 | ~4.7s |
| 6 | `s4_06_keynote_offer` | CHRISTINA "There's several. Legal opened one... offering us a keynote." | 29 | ~10.5s |
| 7 | `s4_07_book_him` | JAN "Book him." / CHRISTINA "Jan." / JAN "BOOK. HIM. If a man on the internet... to argue." | 25 | ~9.1s |
| 8 | `s4_08_own_facilities` | CHRISTINA "There's also the small matter of you being tasered by your own Head of Facilities." | 14 | ~5.1s |
| 9 | `s4_09_risk_management` | JAN "Rick was well within his rights... I invented it. Well -- not invented." **[chain source]** | 35 | ~12.7s |
| 10 | `s4_10_studied_mba` | JAN cont. "Studied. At my MBA." **[chained from #9's last frame]** | 11 | ~4s |
| 11 | `s4_11_made_up_place` | CHRISTINA "The University of Made Up Place." / JAN "Buckinghamshire College of Advanced Enterprise Studies." / CHRISTINA "Which closed in 2011." / JAN "Which closed WELL. With dignity. Unlike this canteen window." | 24 | ~8.7s |
| 12 | `s4_12_incident_form` | CHRISTINA (leaving) "Speaking of which -- HR needs you to complete an Incident Reflection Form before you're cleared to re-enter any room with furniture in it." | 24 | ~8.7s |
| 13 | `s4_13_give_it_here` | JAN "Fine. Give it here." / CHRISTINA "It's fourteen pages." / JAN "FOURTEEN?! For a taser?!" | 12 | ~4.4s |
| 14 | `s4_14_relationship_authority` | CHRISTINA "Page one is the taser... 'relationship with authority,' prompted by page one." | 21 | ~7.6s |
| 15 | `s4_15_coversheet_memo` | JAN "This is worse than the coversheet memo." / CHRISTINA "Everything is worse than the coversheet memo, Jan. That's why we keep sending it." | 22 | ~8s |

## Beat 2 — INT. OPEN-PLAN FLOOR - CONTINUOUS (12 shots, ~1m36s)

| # | Slug | Line(s) | Words | Est. |
|---|---|---|---|---|
| 16 | `s4_16_maintenance_establish` | Establishing: Chris & Rick by the desk run, maintenance man taping cardboard over the canteen window visible through the partition | 0 | ~4s |
| 17 | `s4_17_hero_now` | CHRIS "So. You're a hero now." / RICK "I'm a man who keeps a taser in his desk. The company decided which noun to use." | 23 | ~8.4s |
| 18 | `s4_18_proportionate` | CHRIS "HR called it 'a proportionate use of de-escalation equipment'... best thing I've seen since the Christmas party." / RICK "There's more where that came from." | 27 | ~9.8s |
| 19 | `s4_19_bear_spray` | CHRIS "More tasers?" / RICK opens drawer "Bear spray. Zip ties. A second taser... A flare gun I'm not licensed for." | 24 | ~8.7s |
| 20 | `s4_20_flare_gun` | CHRIS "Why do you have a flare gun in an office building?" / RICK closes drawer "Because one day someone's going to ask me that question... intend to be ready." | 35 | ~12.7s |
| 21 | `s4_21_nina_forms` | Establishing: Nina passes with a stack of forms, repeating "Incident Reflection Forms!" down the row | 0 | ~4s |
| 22 | `s4_22_not_filling_in` | CHRIS "I'm not filling this in." / RICK "You have to." / CHRIS "I watched a man get electrocuted over pastries, Rick... correct outcome, wrong voltage, should've been higher." | 37 | ~13.5s |
| 23 | `s4_23_inception2_boxes` | Action: Chris drops the form unsigned into recycling; delivery man wheels in boxes marked PROJECT INCEPTION 2: THE RECKONING | 0 | ~4.5s |
| 24 | `s4_24_ordered_more` | RICK "He ordered more." / CHRIS "He ordered more." / RICK "Before or after the taser?" / CHRIS "Tracking number says the order went through while he was unconscious on the canteen floor." | 25 | ~9.1s |
| 25 | `s4_25_card_details` | RICK "Christina must have his card details memorised at this point." / CHRIS "Christina IS his card details at this point." | 19 | ~6.9s |
| 26 | `s4_26_mine_was_easy` | Action: Sharon walks past with her completed form, heart dotting the "i" / SHARON "Mine was easy. I wasn't even in the room." | 9 | ~7s |
| 27 | `s4_27_barely` | CHRIS "No. No, you were absolutely in a room." / RICK "Different room. Timing's the only thing keeping HR out of it." / CHRIS "Barely." | 21 | ~7.6s |

## Beat 3 — INT. HR BREAKOUT ROOM - LATER (11 shots, ~1m28s)

| # | Slug | Line(s) | Words | Est. |
|---|---|---|---|---|
| 28 | `s4_28_room_establish` | Establishing: laminated "MANDATORY: RESPECT AT WORK REFRESHER" sign, folding chairs facing the wheeled TV/DVD combo, Debbie standing, Jan and Sharon in the front row sharing a bag of crisps | 0 | ~5s |
| 29 | `s4_29_recent_events` | DEBBIE "Right! Thank you all for making time for this. As you know, following recent events --" / JAN (loudly) "Unrelated events." **[chain source]** | 19 | ~6.9s |
| 30 | `s4_30_just_a_formality` | DEBBIE cont. "-- following recent, unrelated events, Head Office has asked every department to complete the refresher... feeling very good about our culture." **[chained from #29's last frame]** | 38 | ~13.8s |
| 31 | `s4_31_tv_insert_gary` | Insert/cutaway: old training video plays on the TV. VIDEO NARRATOR (V.O.) "Welcome to 'Boundaries: Working Better Together.' Let's meet Gary, who has made an inappropriate comment to a colleague..." | 18 | ~6.5s |
| 32 | `s4_32_gary_idiot` | JAN (stage-whisper) "This Gary sounds like an idiot." / SHARON (not whispering) "Gary sounds like every man I've ever managed." / JAN "HA! Managed. Good one." + high-five | 18 | ~6.5s |
| 33 | `s4_33_question_one` | DEBBIE (deadpan) "Question one. 'Is it appropriate to lock your office door during working hours with a colleague inside?'" | 17 | ~6.2s |
| 34 | `s4_34_depends_on_context` | JAN "Depends entirely on the fire code." / DEBBIE "It's multiple choice, Jan." / JAN "Then it's C. Always C. C is 'depends on context,' I've read ahead." | 24 | ~8.7s |
| 35 | `s4_35_perfect_moving_on` | DEBBIE "There is no C. There's A, 'yes,' and B, 'no.'" / JAN (long pause) "...B?" / DEBBIE "Perfect. Moving on." | 14 | ~5.1s |
| 36 | `s4_36_fire_drill` | SHARON "This is the most action this room's seen since the fire drill." / DEBBIE "The fire drill was also about you, Sharon." / SHARON "Was it?" | 23 | ~8.4s |
| 37 | `s4_37_enfield_protocol` | DEBBIE "You set off the alarm on your way out of Jan's office. Twice... It's called the Enfield Protocol." | 33 | ~12s |
| 38 | `s4_38_form_of_love` | JAN (beaming) "They named a protocol after you. That's more than they ever gave me." / SHARON "They gave you a form, love." / JAN "Fourteen pages of form." | 24 | ~8.7s |

## Beat 4 — INT. STAFF CANTEEN - THAT AFTERNOON (13 shots, ~1m29s)

| # | Slug | Line(s) | Words | Est. |
|---|---|---|---|---|
| 39 | `s4_39_canteen_wary` | Establishing: plywood-boarded window, "DO NOT LEAN ON WINDOW (NEW)" sign, staff eating warily, Maureen restocking pastries reluctantly | 0 | ~4s |
| 40 | `s4_40_jan_enters_merch` | Action: Jan enters (smaller neck brace), Christina wheeling the PROJECT INCEPTION 2 merch trolley — tote bags, mugs, "DEEPER THIS TIME" banner | 0 | ~4s |
| 41 | `s4_41_bold_new_name` | JAN "Right, everyone! In light of yesterday's, ah, learning opportunity... I am relaunching the initiative under a bold new name." | 34 | ~12.4s |
| 42 | `s4_42_the_reckoning` | CHRIS "Please don't say Inception 2." / JAN "Inception 2: The Reckoning." + groans; Maureen freezes, tongs mid-air | 9 | ~6s |
| 43 | `s4_43_lawyers_weapon` | CHRISTINA (through her teeth) "We talked about this. The lawyers specifically said do not use the word 'reckoning' near an incident involving a weapon." | 20 | ~7.3s |
| 44 | `s4_44_trust_fall` | JAN "Everyone gets a tote bag! Everyone gets a mug!... a 'trust fall' exercise, right here, right now, in this very canteen." | 37 | ~13.5s |
| 45 | `s4_45_not_near_pastries` | MAUREEN "Not near the pastries." / JAN "Especially near the pastries! That's where the ENERGY is, Maureen!" | 15 | ~5.5s |
| 46 | `s4_46_tray_crash` | Action: Jan hurls a stress ball, knocks the tray from Maureen's hands, CRASH | 0 | ~4s |
| 47 | `s4_47_frozen_stare` | Action: total silence, everyone stares at the wreckage, then at Jan, then at Rick standing in the doorway with his own tray | 0 | ~4s |
| 48 | `s4_48_ninety_seconds` | RICK "Same time as yesterday?" / CHRIS "Give it about ninety seconds." + Jan picks up a second stress ball | 10 | ~5s |
| 49 | `s4_49_catch_the_next_one` | JAN (arms wide) "WHO WANTS TO CATCH THE NEXT ONE?!" + reaction cutaways: Christina's hands over her face, Sharon filing her nails, Rick reaching for his phone | 7 | ~5s |
| 50 | `s4_50_stress_balls_staff` | RICK (reading his phone) "Well. Good news is the local paper's run the story already... 'EXINC CEO STRESS BALLS STAFF AFTER TASER INCIDENT.'" | 24 | ~8.7s |
| 51 | `s4_51_more_stress_balls` | JAN "We're in the PAPER?!" / CHRISTINA "That is not the takeaway, Jan." / JAN "Get the marketing team on the phone. We need more stress balls." | 25 | ~9.1s |

## Known risks

1. **Debbie Vance has no reference sheet yet.** Nothing in Beat 3 can be generated until
   she's built — same process used for Maureen/Sharon.
2. **The stress-ball-hits-tray beat (`s4_46`) is a physics/impact moment**, same class of
   problem as Scene 3's shattering glass and china. Follow the same fix: generate the
   *before* (`s4_45`) and *after* (`s4_47`) states cleanly and let MiniMax H3's keyframe
   mode render the impact between them, rather than asking a still model for the moment of
   impact itself.
3. **New prop-populated open-plan angle needed** (Rick's desk with the drawer, the delivery
   trolley) — this is not existing `jan_office_corridor` coverage, it needs compositing the
   way `SCENE2_PLATE_SHOT_LIST.md` built character-populated plates rather than pulling from
   the empty-set coverage folder.
4. **Content filtering**: Beat 3's "lock your office door" HR-video line and Beat 1's taser
   aftermath discussion are dialogue-only, not depicted, so should be lower flagging risk
   than Scene 3's actual violence — but the stress-ball impact in Beat 4 is a physical
   comedy/property-damage beat like Scene 3's chair-through-window and may get the same
   false-positive treatment. Expect a possible re-roll.
5. **`s4_30` and `s4_19` (Debbie's opening line) is a genuinely large single-shot word count
   (38 words, 13.8s)** — closest to the cap of anything in this scene. If Higgsfield/fal
   render quality degrades on longer single-take lines, this is the first candidate to split
   further (natural break after "complete the refresher.").
