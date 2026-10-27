# Agent instructions — Video 003 (V2), RUMY WHY

## Hard constraints
- User generates ALL source videos manually in Google Flow, 6 sec each; no paid video APIs, no Flow login or scraping.
- User generates VO manually via ElevenLabs; do not spend credits, call APIs or silently synthesize new speech.
- Do NOT overwrite, move or delete any file in `assets/`. Source immutable. Existing `S01.mp4`–`S12.mp4` already made by owner. New clips named `SXX_v2.mp4` preferred if present, but keep originals.
- Keep animated engineering documentary look. Bright noon sunlight / high visibility / vivid realistic vegetation, clean limestone + red supports, not bleak gray mood or fog.
- Only claim facts sourced in `docs/RESEARCH_VERIFIED.md`. CGI reconstruction not archive/historical proof; no nonlicensed historical photos.
- YouTube Short deliverable: 9:16, 1080x1920, 30fps, H.264/AAC, target ~70s but conform to actual narration. Use no stretch video/audio tricks to hit arbitrary duration.
- Yellow #FFD400 specifically for ARROWS, lines, measurement guides, callouts, highlight circles. White text, consistent RUMY WHY identity. Captions must be above diagrams/technical overlays, within short safe area.
- Graphics should be motion tracked ONLY after verified tracking. When geometry is unreliable use fixed-position callouts or schematic overlays; do not pretend AI footage proves measurements.

## Required first steps
1. Read README and all docs including style reference analysis, VO options, storyboard, flow prompts, QA.
2. `python3 scripts/check_assets.py`; ffprobe and review real footage.
3. Determine exactly what VO version was downloaded from file naming and audible words; do not assume V2 if filename ambiguous. Actual completed V1 generation duration 68.4s.
4. Select best footage per scene: v2 preferred only when actually visually better; no forced regen. Create `output/reports/shot_selection.md` with score (visible process, brightness, correct geometry, camera, safe materials).
5. Realign timeline using voiceover actual word timing/waveform; footage raw clips all 6s (may trim <6 or cut within scene).
6. Build visual overlays. Core priorities: step-by-step 4m pier growth using self-climbing formwork; drilling foundations; hydraulic translator 60cm cycle; temp red steel launch supports; two ends meet; pylon raised from horizontal after bridge closure. If Flow clip misrepresents geometry, replace misleading frames with schematic or safe visual.
7. Mix VO as main audio. Use SFX/music only if user supplied rights-cleared assets; never use unlicensed internet grabs. Do not use audio from generated Flow clips unless clear and intentional.
8. Export and inspect with ffprobe, audio QC and contact sheet before declaring complete. Deliver QA file describing remaining problems honestly.

## Narration mismatch protection
- `voiceover_v2.*` => subtitle from `docs/VOICEOVER_V2_RECOMMENDED.txt` only.
- `voiceover.*` or `voiceover_original.*` => subtitle from `docs/VOICEOVER_V1_ALREADY_GENERATED.txt` only, unless actual listened audio proves otherwise; note discrepancy.
- Ambiguous or absent audio => render only silent proof / prep, and report.

## Fact traps
- 343m = STRUCTURAL HEIGHT TO MAST TOP; 245m = HIGHEST MAIN CONCRETE PIER.
- Total 36,000 tonne steel deck NOT shoved as one 36,000 tonne load in a single operation.
- Two leading stay-supported pylons used during launch; remaining FIVE after closure.
- 64 hydraulic translators across support system; 18 launching operations; full deck gradually from north and south, May 28 2004 deck meeting.
- Climbing formwork ≈4m per three days, not 4m each 6-second real-time shot; label CGI time-lapse as illustration.
- No premature finished seven-pylon construction stage, no floating steel deck/colliding halves.

## Final targets
- `output/final/RUMY_WHY_003_MILLAU_FINAL.mp4`
- `output/final/QA_V2.md`
- `output/final/review_frames/*`
- `output/reports/asset_audit.json`, `shot_selection.md`, `timeline_alignment.csv`
- If missing media: report accurately. NEVER claim render or QA complete without real files and inspection.
