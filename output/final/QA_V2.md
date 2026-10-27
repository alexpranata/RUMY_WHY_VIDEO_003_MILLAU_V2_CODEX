# Millau V2 — simplified edit QA

Owner correction: video footage, existing narration and English subtitles only. This supersedes the earlier added-graphics specification. No added banners, brand strips, technical callouts, yellow graphics or schematic scenes appear in this version. The previous graphics edit remains recoverable in Git history.

## Deliverables

- `RUMY_WHY_003_MILLAU_SIMPLE.mp4`: current simplified export.
- `RUMY_WHY_003_MILLAU_FINAL.mp4`: identical bytes at the canonical delivery path.
- `captions_V2.srt`: matching 32 caption cues; adjacent cues no longer overlap.
- `review_frames/`: actual decoded samples of the current export.
- `output/draft/RUMY_WHY_003_V2_ROUGHCUT.mp4`: current footage/narration assembly before subtitle burn-in; no diagram placeholders.
- `output/reports/timeline_alignment.csv`: current narration-aligned footage choices.

## Technical validation

| Check | Actual result |
|---|---|
| Container/video/audio duration | 64.300000 / 64.300000 / 64.300000 seconds |
| Video | 1080 × 1920, H.264, yuv420p, 30fps, 1929 decoded frames |
| Audio | Owner V2 narration, AAC, mono, 48kHz; no music/SFX or Flow clip audio |
| Integrated loudness | -16.23 LUFS |
| True peak | -1.43 dBTP |
| Full video/audio decode | Exit 0 |
| Detected black segments | 0 (0.02 threshold / 0.1s minimum) |
| Subtitle cues | 32; max two lines, white with black outline, lower safe zone |
| Asset integrity | 30 source files unchanged, SHA-256 verified |

Current MP4 SHA-256: `7a4255b51f9194bc47c39746376141115bc00d077333e550bb3a1cf853b83d33`.

Measurements are retained in `final_ffprobe.json`, `final_validation.json` and `final_decode_audio_qc.log`. Loudness values above measure the actual encoded AAC, not the hypothetical normalized output of the diagnostic filter.

## Editing choices and limits

The provided V2 MP3 measures 64.287347s; the export follows it at a 64.3s frame boundary. No narration synthesis, voice replacement, time stretching or video loops were used. Caption words are exactly from the V2 script; existing acoustic forced-alignment times are retained, with overlaps removed. These are still provisional timings pending listening review.

Original S05 formwork footage now fills 23.0–28.4s instead of the climbing schematic. It shows the pier/formwork context but does not prove a complete physical climbing cycle. Original S08 support footage replaces the launch schematic at 43.8–46.2s. Original S09 and S10 show closure context/detail at 48.7–54.9s. Poor separated-formwork S06 V2 and later problematic S09 V2 footage remain excluded. New cuts use source footage at natural speed; technical geometry is illustrative CGI, not verified construction documentation.

Only S07 has a framing adjustment: 160 source pixels cropped from the top, then aspect-preserving scale/fill, to remove a title already baked into the owner-supplied clip. No replacement text strip was added. Other footage fills the vertical frame. No blanket dark grade is applied.

Reviewed decoded frames cover the hook, valley, drilling, pier, formwork, former schematic intervals, steel assembly, translator, red supports, closure, raising mast and final bridge. The final contact sheet represents this simplified edit, not the previous graphic version.

## Review status

**REVIEW REQUIRED — no final PASS claim.** Technical decode and sampled frame review are complete. Uninterrupted motion and subjective listening/caption-sync review remain necessary before release. This execution interface provides local decoding and recognition, but not dependable subjective playback. Existing local recognition supports selection of V2 narration and does not constitute a full listening review. Source CGI geometry and intermediate morphing are not certified by sampled frames.

## Reproduce

Read `AGENTS.md` and this latest owner correction; preserve every asset. Use the existing isolated checkout; no worktree is needed. Run `/workspace/millau-tools/bin/python output/work/produce_simple.py` from the repository root to rebuild (it overwrites generated outputs only), then `output/work/verify_v2.py` and `output/work/qa_report.py` with the same interpreter. Check the actual narration before adapting the hardcoded 64.3s edit for any future audio.

`output/work/simple/subtitles.ass` contains only subtitle events. `produce_v2.py` and `write_reports.py` are archived helpers for the superseded graphic edit; do not use them for the current simple style. The earlier environment startup instructions also reference that archived edit; follow this correction and `produce_simple.py` instead. FFmpeg/ffprobe, Pillow 12.3.0 and existing PocketSphinx 5.0.4 alignment evidence are used. The harmless fontconfig cache warning did not prevent subtitle rendering.
