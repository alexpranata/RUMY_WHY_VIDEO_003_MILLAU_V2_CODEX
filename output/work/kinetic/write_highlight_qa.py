from pathlib import Path
import json,csv,hashlib,shutil
R=Path(__file__).resolve().parents[3];P=R/'output/reports';F=R/'output/final';W=R/'output/work/kinetic'
v=json.loads((P/'final_validation.json').read_text());words=json.loads((P/'word_caption_map.json').read_text());tracks=json.loads((P/'object_tracks.json').read_text());q=v['loudness']
assert hashlib.sha256((F/'RUMY_WHY_003_MILLAU_HIGHLIGHT.mp4').read_bytes()).hexdigest()==v['sha256']
assert all(a['end_frame']<=b['start_frame'] for a,b in zip(words,words[1:]))
assert all(' ' not in x['display'] for x in words)
shutil.copy2(W/'tracked_objects_review.jpg',P/'tracked_objects_review.jpg')
track_table='\n'.join(f"| {t['object']} | {t['start']}–{t['end']}s | {len(t['samples'])} | {min(x['points'] for x in t['samples'])} | {max(x['median_fb_error_halfres_px'] for x in t['samples']):.4f} |" for t in tracks)
(F/'QA_V2.md').write_text(f'''# Millau V2 — word highlights and object animation

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

{len(words)} sequential single-token caption events, with {sum(w['highlight'] for w in words)} highlighted terms/numbers. Only one token is visible at a time; frame-based intervals are nonoverlapping. Hyphenated compounds remain single tokens. Spoken multi-word numbers may display as one numeric token: `800-FOOT`, `1,125`, `7`, `13`, `64`, `18`, `2004`. The numeric forms preserve the narration's meaning; “800-foot” is the rounded opening phrase from V2, not a substituted exact 804-foot measurement.

White words alternate with brand-yellow #FFD400 keywords/numbers. Keywords and figures have a restrained scale-pop animation. Captions are larger than the previous sentence version, remain within the lower safe zone, and are composited above the object overlay layer. Caption wording is derived from the V2 owner script and the existing actual-audio acoustic alignment, never synthesized narration or invented timestamps. Timing is rounded to the actual 30fps output grid.

Four short attention animations follow real object pixel positions: pulsing/rotating open halos around the formwork jack, red support and mast tip; breathing corner brackets around the translator piston; short yellow pointers approach these targets. The graphics highlight existing pixels without moving or morphing the equipment itself. These are attention cues, not technical force arrows, measured dimensions, physical motion simulations or engineering certification.

## Tracking verification

Tracking uses OpenCV 4.12.0.88 pyramidal KLT at 540×960, ROI-limited features, forward/backward rejection below 1.5 half-resolution pixels, robust median translation and feature reseeding. Tracking stays within selected short clips, never across scene cuts. Original-ROI and sample coordinates are retained.

| Object | Timeline window | Tracked frames | Minimum retained points | Maximum median FB error, half-res px |
|---|---|---|---|---|
{track_table}

Start/middle/end overlays for these four targets were visually checked against the real assembly. A drill track passed some numeric checks but drifted away from the drill on visual review; it was rejected and is absent from the export. Pixel tracking includes camera motion and does not validate the underlying CGI mechanism. Sampled checks are not uninterrupted tracking certification.

## Actual media validation

| Check | Measured result |
|---|---|
| Container/video/audio duration | {v['container_duration']} / {v['video_duration']} / {v['audio_duration']} seconds |
| Video | H.264, 1080×1920, yuv420p, 30fps, {v['frames']} decoded frames |
| Narration | Existing owner V2 MP3; AAC export, mono, 48kHz |
| Integrated loudness | {q['input_i']} LUFS |
| True peak | {q['input_tp']} dBTP |
| Complete video/audio decode | Exit {v['decode_exit']} |
| Detected black segments | {len(v['black_segments'])} (0.02 threshold / 0.1s minimum) |
| Source integrity | {v['source_files_verified']} files unchanged, verified by SHA-256 |

Latest MP4 SHA-256: `{v['sha256']}`.

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
''')
# Annotate the existing exact source timeline without changing its cuts.
p=P/'timeline_alignment.csv';rows=list(csv.DictReader(p.open()));fields=list(rows[0])
for row in rows:
 base=row['adjustments'].replace('Cut only; no graphics','Natural-speed footage; per-word highlighted captions')
 base=base.split('; tracked attention:')[0]
 a=float(row['timeline_in_s']);b=float(row['timeline_out_s']);active=[t['object'] for t in tracks if a<t['end'] and b>t['start']]
 row['adjustments']=base+('; tracked attention: '+', '.join(active) if active else '')
with p.open('w') as f:
 writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)
p=P/'shot_selection.md';s=p.read_text();marker='<!-- CURRENT HIGHLIGHT EDIT -->\n'
if not s.startswith(marker):p.write_text(marker+'# Current highlight edit\n\nLatest update retains the simple edit’s source selections and chronology. Captions now appear one token at a time with keyword/number highlighting. Four verified short object tracks drive attention halos/brackets/pointers; no large banners or schematic replacements. Current source intervals and object windows are in timeline_alignment.csv and object_tracks.json. Earlier style directions below are historical.\n\n'+s)
print('Highlight QA and timeline annotations written.')
