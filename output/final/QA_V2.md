# Millau V2 — word highlights and object animation

Latest owner direction: retain video and owner narration, show subtitles one word at a time, highlight important terms/numbers, and add relevant object animations. This supersedes the earlier simple edit's ban on all overlays. No large title banners, information panels or standalone diagrams were reintroduced. Original assets are untouched.

## Current deliverables

- `RUMY_WHY_003_MILLAU_HIGHLIGHT.mp4`: latest version.
- `RUMY_WHY_003_MILLAU_FINAL.mp4`: identical canonical copy.
- `captions_WORD.srt` and `captions_V2.srt`: current single-token captions.
- `RUMY_WHY_003_MILLAU_SIMPLE.mp4`: preserved previous simple version, not the latest export.
- `review_frames/contact_sheet.jpg`: decoded samples from the latest highlight export.
- `output/reports/word_caption_map.json`: original spoken words, displayed text, source audio times and output frame boundaries.
- `output/reports/object_tracks.json`, `tracked_objects_review.jpg`: pixel tracking and manually reviewed start/middle/end evidence on the raw assembly.

## Subtitle and animation treatment

168 sequential single-token caption events, with 53 highlighted terms/numbers. Only one token is visible at a time; frame-based intervals are nonoverlapping. Hyphenated compounds remain single tokens. Spoken multi-word numbers may display as one numeric token: `800-FOOT`, `1,125`, `7`, `13`, `64`, `18`, `2004`. The numeric forms preserve the narration's meaning; “800-foot” is the rounded opening phrase from V2, not a substituted exact 804-foot measurement.

White words alternate with brand-yellow #FFD400 keywords/numbers. Keywords and figures have a restrained scale-pop animation. Captions are larger than the previous sentence version, remain within the lower safe zone, and are composited above the object overlay layer. Caption wording is derived from the V2 owner script and the existing actual-audio acoustic alignment, never synthesized narration or invented timestamps. Timing is rounded to the actual 30fps output grid.

Four short attention animations follow real object pixel positions: pulsing/rotating open halos around the formwork jack, red support and mast tip; breathing corner brackets around the translator piston; short yellow pointers approach these targets. The graphics highlight existing pixels without moving or morphing the equipment itself. These are attention cues, not technical force arrows, measured dimensions, physical motion simulations or engineering certification.

## Tracking verification

Tracking uses OpenCV 4.12.0.88 pyramidal KLT at 540×960, ROI-limited features, forward/backward rejection below 1.5 half-resolution pixels, robust median translation and feature reseeding. Tracking stays within selected short clips, never across scene cuts. Original-ROI and sample coordinates are retained.

| Object | Timeline window | Tracked frames | Minimum retained points | Maximum median FB error, half-res px |
|---|---|---|---|---|
| formwork_jack | 18.5–20.0s | 45 | 58 | 0.0102 |
| translator | 39.3–42.4s | 93 | 95 | 0.0042 |
| red_support | 43.9–45.8s | 57 | 100 | 0.0032 |
| mast_tip | 55.2–57.8s | 78 | 23 | 0.0037 |

Start/middle/end overlays for these four targets were visually checked against the real assembly. A drill track passed some numeric checks but drifted away from the drill on visual review; it was rejected and is absent from the export. Pixel tracking includes camera motion and does not validate the underlying CGI mechanism. Sampled checks are not uninterrupted tracking certification.

## Actual media validation

| Check | Measured result |
|---|---|
| Container/video/audio duration | 64.300000 / 64.300000 / 64.300000 seconds |
| Video | H.264, 1080×1920, yuv420p, 30fps, 1929 decoded frames |
| Narration | Existing owner V2 MP3; AAC export, mono, 48kHz |
| Integrated loudness | -16.23 LUFS |
| True peak | -1.43 dBTP |
| Complete video/audio decode | Exit 0 |
| Detected black segments | 0 (0.02 threshold / 0.1s minimum) |
| Source integrity | 30 files unchanged, verified by SHA-256 |

Latest MP4 SHA-256: `b5a557d677c520d72e645be2efe70fdc32ca5b2d22f87e15f1ee0222d1ae8a17`.

The same 64.287347s V2 narration dictates the 64.3s export. Source selection, cuts, chronology and natural speed from the simple edit are retained; the raw rough cut is unchanged. Only S07 retains the previously documented source-top crop to remove baked-in title text. No new music/SFX, source-clip audio, TTS, paid API generation, Flow login or replacement footage were used.

Source geometry limitations remain: S05 gives formwork context without proving a complete climb; the CGI translator is not a validated hydraulic drawing; launch and mast rigging geometry remain illustrative. The source scene comparison and current source intervals are in shot_selection.md and timeline_alignment.csv.

## Review status

**REVIEW REQUIRED — no final PASS claim.** Decoding, metrics, one-token/no-overlap assertions, source integrity and sampled frame inspection were completed. Full subjective audio/caption-sync and uninterrupted motion review remain pending; this interface does not provide dependable subjective listening. In particular, very short function words follow the narration's rapid cadence and should be reviewed at normal playback speed. Actual forced alignment is provisional, not a promise of human-verified word timing.

## Reproduce this version

Use the existing isolated checkout, no worktree. Preserve every file in assets. The raw assembly under output/draft must match the current simple timeline. Install local Python dependencies if needed: Pillow==12.3.0, opencv-python-headless==4.12.0.88 and numpy==2.2.6. Existing alignment evidence was made with PocketSphinx==5.0.4.

Run with `/workspace/millau-tools/bin/python`, from the repository root:

1. `output/work/kinetic/track_objects.py`
2. Visually verify generated tracking_candidates/tracked_objects_review evidence; reject tracks that leave the intended object even if numeric checks pass.
3. `output/work/kinetic/render_highlight.py`
4. `output/work/verify_v2.py`
5. `output/work/kinetic/write_highlight_qa.py`

The helpers overwrite generated outputs only. The old produce_v2.py / write_reports.py / produce_simple.py / qa_report.py and earlier environment startup instructions describe superseded edit versions. They are not the current highlight workflow. The fontconfig cache warning was nonfatal; sampled export frames confirm text rendering.
