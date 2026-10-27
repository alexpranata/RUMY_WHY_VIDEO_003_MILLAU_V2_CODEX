from pathlib import Path
import json,csv,hashlib
R=Path(__file__).resolve().parents[3];F=R/'output/final';P=R/'output/reports';W=R/'output/work/clean_sfx'
v=json.loads((P/'final_validation.json').read_text());q=v['loudness'];cues=json.loads((P/'sfx_selection.json').read_text());mix=json.loads((P/'sfx_mix_validation.json').read_text());words=json.loads((P/'word_caption_map.json').read_text())
assert hashlib.sha256((F/'RUMY_WHY_003_MILLAU_WORDS_SFX.mp4').read_bytes()).hexdigest()==v['sha256']
ass=(W/'word_only.ass').read_text();assert r'\p1' not in ass and 'Style: Graphic,' not in ass
assert len([x for x in ass.splitlines() if x.startswith('Dialogue:')])==168
rows='\n'.join(f"| {x['name']} | {x['source']} | {x['source_in_s']:.2f}s | {x['timeline_in_s']:.2f}–{x['timeline_in_s']+x['duration_s']:.2f}s | {x['expected_rms_dbfs']} |" for x in cues)
(F/'QA_V2.md').write_text(f'''# Millau V2 — no object graphics, optional matching SFX

Latest owner correction: remove yellow object animations and add suitable sound effects if possible. Yellow arrows, halos, corner brackets and all other object drawing events are removed. The previously requested single-word subtitles and yellow keyword/number highlights are retained. The source footage, natural-speed timeline and owner V2 narration are unchanged.

## Current download versions

- `RUMY_WHY_003_MILLAU_WORDS_SFX.mp4`: current mix with four short, quiet source-audio texture cues.
- `RUMY_WHY_003_MILLAU_FINAL.mp4`: identical canonical copy of the SFX version.
- `RUMY_WHY_003_MILLAU_WORDS.mp4`: same picture and narration, without SFX, for comparison.
- `captions_WORD.srt` / `captions_V2.srt`: current 168 single-token captions.
- `review_frames/`: current decoded export frames/contact sheet, showing no object graphics.

Older SIMPLE and HIGHLIGHT files remain prior versions; HIGHLIGHT still contains the now-rejected yellow object animations. The current rendering helper is `output/work/clean_sfx/render_clean_sfx.py`.

## Sound provenance and treatment

The standalone assets/sfx folder has no sound files. Existing owner-provided Flow clips do have embedded audio, so the following short selections are reused deliberately in their matching visible scenes. No unlicensed internet audio, external downloads, music, paid synthesis or new narration was added. These are processed source textures, not a claim of authentic construction-location recording.

| Cue | Owner-provided source | Source in | Timeline window | Processed cue RMS target/result dBFS |
|---|---|---|---|---|
{rows}

Each cue is aligned using the same source offset as its video shot. High/low-pass filtering, a broad mid-band rejection, short fades and conservative gain retain low mechanical/high-frequency texture while suppressing possible incidental vocal content. Effects are deliberately quiet below the narration, with individual peaks capped near -19 dBFS. A latency-compensated limiter protects the combined mix. The VO itself is not filtered this way or time-stretched.

Subjective listening is still pending. Local speech-recognition checks on raw source sounds were inconclusive; they are not proof of dialogue absence, music absence or effect suitability. This is a review mix, not a claim that embedded sounds were human-listened and certified. Use the supplied no-SFX version if any texture distracts from the narration. Provenance and exact processing are retained in sfx_selection.json.

Waveform comparison against the no-SFX version confirms actual additions in the four cue windows; the difference outside padded cue windows is {mix['difference_outside_cue_windows_dbfs']} dBFS, predominantly AAC generation noise. The two versions have identical compressed video bitstreams, so only audio differs. See sfx_mix_validation.json.

## Actual measured validation

| Check | Measured result |
|---|---|
| Container / video / audio duration | {v['container_duration']} / {v['video_duration']} / {v['audio_duration']} seconds |
| Video | H.264, 1080×1920, yuv420p, 30fps, {v['frames']} decoded frames |
| Audio | AAC, mono, 48kHz; existing owner V2 narration plus source-texture cues |
| Integrated loudness | {q['input_i']} LUFS |
| True peak | {q['input_tp']} dBTP |
| Full video/audio decode | Exit {v['decode_exit']} |
| Black segments | {len(v['black_segments'])} at 0.02 threshold / 0.1s minimum |
| Captions | {v['caption_events']} single tokens, {sum(x['highlight'] for x in words)} emphasized, nonoverlapping frame intervals |
| Object overlay events | 0, checked against rendered ASS source |
| Source integrity | {v['source_files_verified']} asset files unchanged by SHA-256 |

Current SFX export SHA-256: `{v['sha256']}`.

The master narration is still the actual 64.287347s V2 MP3; the export follows it at a 64.3s frame boundary. Sampled output inspection covers the formwork, translator, supports and mast where graphics used to appear, plus figures/keywords and closing shots. No new banner or diagram was introduced.

## Review status

**REVIEW REQUIRED — no final PASS claim.** Decode, source integrity, metrics, subtitle assertions and sampled frames are checked. Full listening and uninterrupted motion/caption-sync review remain pending because this execution interface does not provide dependable subjective playback. The SFX version is intentionally offered alongside a no-SFX fallback. Local word alignment and CGI geometry retain the previously documented limitations.

## Reproduce

Use the existing isolated checkout; no worktree. Preserve all assets. With the existing raw assembly and previous word timing evidence present, run `/workspace/millau-tools/bin/python output/work/clean_sfx/render_clean_sfx.py`, then output/work/verify_v2.py and this write_clean_qa.py helper. FFmpeg/ffprobe and Pillow are used; no API is called. The helper intentionally overwrites generated outputs, never assets. Older workflow helpers and environment startup instructions describe prior edits; follow this latest owner correction.
''')
p=P/'timeline_alignment.csv';data=list(csv.DictReader(p.open()));fields=list(data[0])
for row in data:
 base=row['adjustments'].split('; tracked attention:')[0];a=float(row['timeline_in_s']);b=float(row['timeline_out_s']);active=[x['name'] for x in cues if a<x['timeline_in_s']+x['duration_s'] and b>x['timeline_in_s']]
 row['adjustments']=base.split('; SFX:')[0]+'; no object graphics'+('; SFX: '+','.join(active) if active else '')
with p.open('w') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(data)
p=P/'shot_selection.md';s=p.read_text();marker='<!-- CURRENT NO-OBJECT-GRAPHICS EDIT -->\n'
if not s.startswith(marker):p.write_text(marker+'# Current revision\n\nYellow object overlays are removed; highlighted per-word captions remain. Source selection and video timing are unchanged. Four quiet, processed texture cues from matching owner-provided clips are available in the SFX version, with an otherwise identical no-SFX alternative. Earlier tracking/style notes below are historical.\n\n'+s)
print('Current no-object-graphics/SFX QA written.')
