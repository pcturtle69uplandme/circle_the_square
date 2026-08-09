"""Generate all 9 Master Location Spec Sheets for Circle the Square.
"""

import os
import sys
import subprocess
from pathlib import Path

AI_DIR = Path(r"C:\ai\AI")
OUT_DIR = Path(r"C:\kontitemp\ai\circle_the_square\location-refs")
OUT_DIR.mkdir(parents=True, exist_ok=True)

LOCATIONS = [
    {
        "id": "01",
        "name": "Exterior Forecourt & Main Entrance",
        "file_prefix": "01_exterior_forecourt_location_sheet",
        "prompt": (
            "Comprehensive master location identity and set reference sheet for Location #1 Exterior Forecourt & Main Entrance of Prism HQ from the series 'Circle the Square', formatted in a clean white multi-panel model sheet grid layout matching professional film production reference sheets. "
            "LEFT PANEL: Bold header 'LOCATION #1 | EXTERIOR FORECOURT & TOWER'. Sections for 'LOCATION CORE' (Function: Establishing / Cold Open, Real basis: Entrance plaza & tower, Exterior ground level), 'ATMOSPHERE & PALETTE' (Mood: Institutional, corporate, calm dusk hero look), and 'COLOR PALETTE' swatches (#D9C3A0 sand brick, #E7E2D6 precast concrete, #2B3038 bronze framing, #16294A dusk sky, #F2A34D amber lantern glow). "
            "TOP CENTER: 'MAIN SET & PERSPECTIVE ELEVATIONS' with 4 set views (Wide Symmetrical Dusk Approach, 3/4 Tower Perspective, Ground Elevation, Night Entrance View) showing the cream brick building, link bridge, revolving doors, and 39m tower topped with an amber glowing glass lantern. "
            "TOP RIGHT: 'ARCHITECTURAL & LIGHTING GRID' with 6 close-up details (Brick texture, Bronze glazing fins, Revolving doors, Tower lantern close-up, Ground uplighters, Landscaped benches). "
            "BOTTOM CENTER: 'SET DRESSING & PRACTICALS' (Picnic benches, low hedge planters, ground uplighters, Prism entrance signage). "
            "BOTTOM RIGHT PANEL: 'CINEMATIC SHOT IN CONTEXT' showing a 35mm film-still of a single figure walking toward the glowing amber entrance at dusk. Clean white layout, highly detailed photorealistic concept sheet."
        )
    },
    {
        "id": "02",
        "name": "Reception & Atrium Lobby",
        "file_prefix": "02_reception_atrium_location_sheet",
        "prompt": (
            "Comprehensive master location identity and set reference sheet for Location #2 Reception & Double-Height Atrium of Prism HQ from the series 'Circle the Square', formatted in a clean white multi-panel model sheet grid layout matching professional film production reference sheets. "
            "LEFT PANEL: Bold header 'LOCATION #2 | RECEPTION & ATRIUM LOBBY'. Sections for 'LOCATION CORE' (Function: Badge access checkpoint / Arrivals, Real basis: Double-height lobby & link building, Ground floor & mezzanine), 'ATMOSPHERE & PALETTE' (Mood: Corporate formal, impressive security checkpoint), and 'COLOR PALETTE' swatches (#E7E3D6 floor tile, #9C958A concrete column, #B8C4C4 turnstile glass, #2C3A5C glazed brick pier, #B98A55 oak stair tread). "
            "TOP CENTER: 'MAIN SET & PERSPECTIVE ELEVATIONS' with 4 set views (Ground Master Wide with Turnstiles, Elevated Mezzanine View, Reception Desk Angle, Staircase Perspective) showing the double-height atrium, bank of glass paddle turnstiles, faceted amber reception desk, and concrete/oak staircase. "
            "TOP RIGHT: 'ARCHITECTURAL & LIGHTING GRID' with 6 close-up details (Glass paddle gates, Faceted desk finish, Mirrored ceiling soffit, Glazed brick piers, Backlit feature wall with Prism logo, Oak stair treads). "
            "BOTTOM CENTER: 'SET DRESSING & PRACTICALS' (Visitor sign-in tablet, desk phones, black leather sofa seating, queue barriers). "
            "BOTTOM RIGHT PANEL: 'CINEMATIC SHOT IN CONTEXT' showing a 35mm film-still of a character presenting a burnt orange lanyard badge at the glass turnstile gates. Clean white layout, highly detailed photorealistic concept sheet."
        )
    },
    {
        "id": "03",
        "name": "Staff Restaurant / Canteen",
        "file_prefix": "03_canteen_location_sheet",
        "prompt": (
            "Comprehensive master location identity and set reference sheet for Location #3 Staff Restaurant and Canteen of Prism HQ from the series 'Circle the Square', formatted in a clean white multi-panel model sheet grid layout matching professional film production reference sheets. "
            "LEFT PANEL: Bold header 'LOCATION #3 | STAFF RESTAURANT / CANTEEN'. Sections for 'LOCATION CORE' (Function: Canteen meltdown climax / Pastry beat, Real basis: Servery & dining hall, Ground floor & mezzanine), 'ATMOSPHERE & PALETTE' (Mood: Everyday institutional canteen, ordinariness contrasting Jan's meltdown), and 'COLOR PALETTE' swatches (#E7E3D6 floor tile, #1C1C1C servery counter, #F2F0EA subway tile, #B98A55 oak canopy, #E8B800 yellow accent). "
            "TOP CENTER: 'MAIN SET & PERSPECTIVE ELEVATIONS' with 4 set views (Servery Counter Master Wide, Ground Floor Seating Area, Mezzanine Dining View, Open Action Floor for Meltdown) showing the oak slat canopy, black counters, white subway tiles, and dining tables. "
            "TOP RIGHT: 'ARCHITECTURAL & LIGHTING GRID' with 6 close-up details (Black counter sneeze guards, Oak ceiling slats, White subway tile splashback, Digital menu screens, Pay point floor sign, Yellow gloss accent wall). "
            "BOTTOM CENTER: 'SET DRESSING & PRACTICALS' (Pastry tray with 'Sorry All Gone' sign, cutlery bins, condiment station, round oak communal table). "
            "BOTTOM RIGHT PANEL: 'CINEMATIC SHOT IN CONTEXT' showing a 35mm film-still of the dramatic canteen meltdown scene with plates swept on the floor and a shattered window background. Clean white layout, highly detailed photorealistic concept sheet."
        )
    },
    {
        "id": "04",
        "name": "Open-Plan Office Floor",
        "file_prefix": "04_open_plan_office_location_sheet",
        "prompt": (
            "Comprehensive master location identity and set reference sheet for Location #4 Open-Plan Office Floor of Prism HQ from the series 'Circle the Square', formatted in a clean white multi-panel model sheet grid layout matching professional film production reference sheets. "
            "LEFT PANEL: Bold header 'LOCATION #4 | OPEN-PLAN OFFICE FLOOR'. Sections for 'LOCATION CORE' (Function: Staff gather-round / Project Inception zone, Real basis: Upper office desking wing, Upper floor), 'ATMOSPHERE & PALETTE' (Mood: Contemporary open-plan office, unremarkable backdrop for comedy), and 'COLOR PALETTE' swatches (#8A8578 carpet tile, #E8E6DE white desk, #2B2B2B partition fabric, #F4F3EF ceiling, #C21F2A red zone accent). "
            "TOP CENTER: 'MAIN SET & PERSPECTIVE ELEVATIONS' with 4 set views (Desk Rows Master Wide, Gather-Round Open Desk Area, Desk Aisle View, Window Wall Elevation) showing rows of white standing desks, black dual monitors, task chairs, and zone-code concrete columns. "
            "TOP RIGHT: 'ARCHITECTURAL & LIGHTING GRID' with 6 close-up details (Suspended geometric triangle acoustic sculpture, Focus pod with frosted dots, Column zone signage 'NW1', Linear ceiling light cove, Locker bank, Desktop setup). "
            "BOTTOM CENTER: 'SET DRESSING & PRACTICALS' (Dell monitors, mesh task chairs, small desk plants, fire extinguisher stand, Prism stress ball). "
            "BOTTOM RIGHT PANEL: 'CINEMATIC SHOT IN CONTEXT' showing a 35mm film-still of staff gathered around Jan as he rants about Project Inception. Clean white layout, highly detailed photorealistic concept sheet."
        )
    },
    {
        "id": "05",
        "name": "Glass Meeting Room (Jan's Office)",
        "file_prefix": "05_glass_meeting_room_location_sheet",
        "prompt": (
            "Comprehensive master location identity and set reference sheet for Location #5 Glass Meeting Room (Jan's Office) of Prism HQ from the series 'Circle the Square', formatted in a clean white multi-panel model sheet grid layout matching professional film production reference sheets. "
            "LEFT PANEL: Bold header 'LOCATION #5 | GLASS MEETING ROOM'. Sections for 'LOCATION CORE' (Function: Pitch meeting / Blinds-closing affair beat, Real basis: Glazed meeting room off open floor, Upper floor), 'ATMOSPHERE & PALETTE' (Mood: Exposed corporate glass box, formal yet transparent), and 'COLOR PALETTE' swatches (#1A1A1A black frame, #FFFFFF frosted dot film, #F4F3EF white table, #2B2B2B mesh chair, #8A8578 carpet). "
            "TOP CENTER: 'MAIN SET & PERSPECTIVE ELEVATIONS' with 4 set views (Corridor View through Glass, Room Interior Master Wide, Table Perspective, Sliding Glass Door Angle) showing full-height glass walls, white meeting table, mesh task chairs, and window view beyond. "
            "TOP RIGHT: 'ARCHITECTURAL & LIGHTING GRID' with 6 close-up details (Frosted dot privacy film, Triangle decal motif, Black door joinery, Wall-mounted flatscreen TV, Window with tree view, Whiteboard marker surface). "
            "BOTTOM CENTER: 'SET DRESSING & PRACTICALS' (White meeting table, mesh task chairs, HDMI pop-up box, manual window blinds). "
            "BOTTOM RIGHT PANEL: 'CINEMATIC SHOT IN CONTEXT' showing a 35mm film-still of Jan closing the office blinds while Sharon watches. Clean white layout, highly detailed photorealistic concept sheet."
        )
    },
    {
        "id": "06",
        "name": "Breakout Nooks (Pitstop & Arcade)",
        "file_prefix": "06_breakout_nooks_location_sheet",
        "prompt": (
            "Comprehensive master location identity and set reference sheet for Location #6 Breakout & Kitchenette Nooks of Prism HQ from the series 'Circle the Square', formatted in a clean white multi-panel model sheet grid layout matching professional film production reference sheets. "
            "LEFT PANEL: Bold header 'LOCATION #6 | BREAKOUT & KITCHENETTE NOOKS'. Sections for 'LOCATION CORE' (Function: Informal staff-gossip beats / Break area, Real basis: Scattered themed nooks, Upper floors), 'ATMOSPHERE & PALETTE' (Mood: Playful graphic nooks, office trying hard to feel fun), and 'COLOR PALETTE' swatches (#4FBFAE teal stool, #B9AEDB lavender mural, #2E8B3D green recycling, #241E5C indigo arcade, #B98A55 oak veneer). "
            "TOP CENTER: 'MAIN SET & PERSPECTIVE ELEVATIONS' with 4 set views (Pitstop Branded Nook Wide, Kitchenette Coffee Station, Arcade & Foosball Nook, Mezzanine Overlook Angle) showing graphic wall murals, high tables, coffee kiosks, and foosball games. "
            "TOP RIGHT: 'ARCHITECTURAL & LIGHTING GRID' with 6 close-up details (Pitstop circuit graphic, Bean-to-cup coffee machine, Recycling icon panel, Pixel-art arcade mural, Foosball table, Pendant drum lights). "
            "BOTTOM CENTER: 'SET DRESSING & PRACTICALS' (Oak high table, teal stools, arcade cabinet, coffee cup recycling station). "
            "BOTTOM RIGHT PANEL: 'CINEMATIC SHOT IN CONTEXT' showing a 35mm film-still of Chris and Rick chatting near the foosball table. Clean white layout, highly detailed photorealistic concept sheet."
        )
    },
    {
        "id": "07",
        "name": "Landscaped Podium Courtyard",
        "file_prefix": "07_podium_courtyard_location_sheet",
        "prompt": (
            "Comprehensive master location identity and set reference sheet for Location #7 Landscaped Podium Courtyard of Prism HQ from the series 'Circle the Square', formatted in a clean white multi-panel model sheet grid layout matching professional film production reference sheets. "
            "LEFT PANEL: Bold header 'LOCATION #7 | LANDSCAPED PODIUM COURTYARD'. Sections for 'LOCATION CORE' (Function: Quiet beat / Outdoor gossip scene, Real basis: Enclosed podium courtyard, First floor level), 'ATMOSPHERE & PALETTE' (Mood: Peaceful, enclosed, building looking in on itself), and 'COLOR PALETTE' swatches (#D9C3A0 cream brick, #DCD3C0 resin gravel, #5C6B3E fern green, #C7C2B8 boulder grey). "
            "TOP CENTER: 'MAIN SET & PERSPECTIVE ELEVATIONS' with 4 set views (Enclosed Courtyard Master Wide, Elevated View from Window, Meandering Path View, Dusk Lighting View) showing the cream brick walls enclosing all four sides, gravel paths, fern beds, and boulder seats. "
            "TOP RIGHT: 'ARCHITECTURAL & LIGHTING GRID' with 6 close-up details (Cream brick punched windows, Resin gravel texture, Boulder seats, Circular water feature, Fern beds, Ground bollard uplighters). "
            "BOTTOM CENTER: 'SET DRESSING & PRACTICALS' (Smooth boulder seats, wooden bench, sunken water feature, bollard lamps). "
            "BOTTOM RIGHT PANEL: 'CINEMATIC SHOT IN CONTEXT' showing a 35mm film-still of a character sitting alone on a boulder seat at dusk. Clean white layout, highly detailed photorealistic concept sheet."
        )
    },
    {
        "id": "08",
        "name": "Corridors & Locker Bays",
        "file_prefix": "08_corridors_lockers_location_sheet",
        "prompt": (
            "Comprehensive master location identity and set reference sheet for Location #8 Corridors, Locker Bays & Washrooms of Prism HQ from the series 'Circle the Square', formatted in a clean white multi-panel model sheet grid layout matching professional film production reference sheets. "
            "LEFT PANEL: Bold header 'LOCATION #8 | CORRIDORS & LOCKER BAYS'. Sections for 'LOCATION CORE' (Function: Walk-and-talk transitions / Storage, Real basis: Circulation corridors & lockers, All floors), 'ATMOSPHERE & PALETTE' (Mood: Neutral, functional, clean office circulation), and 'COLOR PALETTE' swatches (#D8D2C4 taupe wall, #8A8578 grey carpet, #FFFFFF white lockers, #B98A55 timber fin, #2B2B2B dark tile). "
            "TOP CENTER: 'MAIN SET & PERSPECTIVE ELEVATIONS' with 4 set views (Corridor Walk-and-Talk Wide, Locker Bay Row, Abstract Ceiling Mural Junction, Washroom Trough Sink) showing white locker banks, taupe walls, linear lighting, and timber fin accents. "
            "TOP RIGHT: 'ARCHITECTURAL & LIGHTING GRID' with 6 close-up details (White key-code lockers, Zone signage 'W2-F', Fire hose cabinet, Abstract ceiling graphic, Trough sink with sensor taps, Timber doors). "
            "BOTTOM CENTER: 'SET DRESSING & PRACTICALS' (Stacked lockers, fire extinguisher stand, direction signage, bench seating). "
            "BOTTOM RIGHT PANEL: 'CINEMATIC SHOT IN CONTEXT' showing a 35mm film-still of two staff members engaged in a walk-and-talk down the locker corridor. Clean white layout, highly detailed photorealistic concept sheet."
        )
    },
    {
        "id": "09",
        "name": "Rear Staff Entrance",
        "file_prefix": "09_rear_staff_entrance_location_sheet",
        "prompt": (
            "Comprehensive master location identity and set reference sheet for Location #9 Rear / Staff-Only Entrance of Prism HQ from the series 'Circle the Square', formatted in a clean white multi-panel model sheet grid layout matching professional film production reference sheets. "
            "LEFT PANEL: Bold header 'LOCATION #9 | REAR STAFF ENTRANCE'. Sections for 'LOCATION CORE' (Function: Alternate entrance / Early arrival beat, Real basis: Secondary staff entrance, Ground floor exterior), 'ATMOSPHERE & PALETTE' (Mood: Functional, unglamorous back-of-house entrance), and 'COLOR PALETTE' swatches (#B8A98C blockwork wall, #C79A6B brick paving, #7A7A7A grey door frame, #B0381F orange accent). "
            "TOP CENTER: 'MAIN SET & PERSPECTIVE ELEVATIONS' with 4 set views (Day Exterior Approach, Dusk Illuminated Entrance, Revolving Door Detail, Interior Service Corridor Beyond) showing the painted blockwork wall, revolving glass door, and brick paving approach. "
            "TOP RIGHT: 'ARCHITECTURAL & LIGHTING GRID' with 6 close-up details (Blockwork texture, 'Staff Entrance Only' plaque, Red fire extinguisher cabinet, Alarm bell, Brick paving, Service corridor interior). "
            "BOTTOM CENTER: 'SET DRESSING & PRACTICALS' (Revolving door, staff signage, fire cabinet, bollard lighting). "
            "BOTTOM RIGHT PANEL: 'CINEMATIC SHOT IN CONTEXT' showing a 35mm film-still of a character entering through the glowing rear revolving door at dusk. Clean white layout, highly detailed photorealistic concept sheet."
        )
    }
]

if __name__ == "__main__":
    print(f"Loaded {len(LOCATIONS)} location specs for Circle the Square.")
    for loc in LOCATIONS:
        print(f"[{loc['id']}] {loc['name']} -> {loc['file_prefix']}.jpg")
