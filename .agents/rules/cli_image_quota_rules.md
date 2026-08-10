# 🖼️ CLI IMAGE GENERATION QUOTA & WORKFLOW RULES

## 1. CLI Tool Limits (`generate_image`)
- **Capacity Ceiling:** Maximum **12 image generations** per rolling **4-hour window**.
- **Enforcement:** If a `429 RESOURCE_EXHAUSTED` error is received from `cloudcode-pa.googleapis.com`, stop CLI generations immediately and notify the user of the exact reset timestamp.
- **Tracking:** Maintain a count of generated images per session so the user is warned when approaching 10/12 images.

## 2. Session Consistency & AI Studio Workflow
- **Single-Session Consistency:** For multi-frame storyboards (e.g. 64 frames), recommended primary workflow is **Google AI Studio** (`aistudio.google.com`) using personal subscription quota to maintain character memory within a single continuous chat thread.
- **Character Tags:** All prompts must include explicit `@tag` character names (`@jan`, `@christina`, `@sharon`, `@chris`, `@rick`) and physical anchors.
- **Output Storage:** Save all generated frames into `circle_the_square/storyboard-frames/Fxx.jpg` to feed `storyboard_slideshow.html`.
