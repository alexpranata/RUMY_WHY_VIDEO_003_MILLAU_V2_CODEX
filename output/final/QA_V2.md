# Millau V2 — no object graphics, optional matching SFX

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
| formwork | assets/video/S05_v2.mp4 | 1.10s | 18.70–19.80s | -37.32 |
| steel_assembly | assets/video/S07_v2.mp4 | 2.25s | 35.30–37.40s | -36.28 |
| translator | assets/video/S08_v2.mp4 | 1.00s | 39.60–42.60s | -35.81 |
| raising | assets/video/S11_v2.mp4 | 0.60s | 55.20–57.70s | -32.0 |

Each cue is aligned using the same source offset as its video shot. High/low-pass filtering, a broad mid-band rejection, short fades and conservative gain retain low mechanical/high-frequency texture while suppressing possible incidental vocal content. Effects are deliberately quiet below the narration, with individual peaks capped near -19 dBFS. A latency-compensated limiter protects the combined mix. The VO itself is not filtered this way or time-stretched.

Subjective listening is still pending. Local speech-recognition checks on raw source sounds were inconclusive; they are not proof of dialogue absence, music absence or effect suitability. This is a review mix, not a claim that embedded sounds were human-listened and certified. Use the supplied no-SFX version if any texture distracts from the narration. Provenance and exact processing are retained in sfx_selection.json.

Waveform comparison against the no-SFX version confirms actual additions in the four cue windows; the difference outside padded cue windows is -65.31 dBFS, predominantly AAC generation noise. The two versions have identical compressed video bitstreams, so only audio differs. See sfx_mix_validation.json.

## Actual measured validation

| Check | Measured result |
|---|---|
| Container / video / audio duration | 64.300000 / 64.300000 / 64.300000 seconds |
| Video | H.264, 1080×1920, yuv420p, 30fps, 1929 decoded frames |
| Audio | AAC, mono, 48kHz; existing owner V2 narration plus source-texture cues |
| Integrated loudness | -16.23 LUFS |
| True peak | -1.46 dBTP |
| Full video/audio decode | Exit 0 |
| Black segments | 0 at 0.02 threshold / 0.1s minimum |
| Captions | 168 single tokens, 53 emphasized, nonoverlapping frame intervals |
| Object overlay events | 0, checked against rendered ASS source |
| Source integrity | 30 asset files unchanged by SHA-256 |

Current SFX export SHA-256: `59a49e3d239a39bd1b548c384cac1d5301932d7cda8f39fe486e9b819516d151`.

The master narration is still the actual 64.287347s V2 MP3; the export follows it at a 64.3s frame boundary. Sampled output inspection covers the formwork, translator, supports and mast where graphics used to appear, plus figures/keywords and closing shots. No new banner or diagram was introduced.

## Review status

**REVIEW REQUIRED — no final PASS claim.** Decode, source integrity, metrics, subtitle assertions and sampled frames are checked. Full listening and uninterrupted motion/caption-sync review remain pending because this execution interface does not provide dependable subjective playback. The SFX version is intentionally offered alongside a no-SFX fallback. Local word alignment and CGI geometry retain the previously documented limitations.

## Reproduce

Use the existing isolated checkout; no worktree. Preserve all assets. With the existing raw assembly and previous word timing evidence present, run `/workspace/millau-tools/bin/python output/work/clean_sfx/render_clean_sfx.py`, then output/work/verify_v2.py and this write_clean_qa.py helper. FFmpeg/ffprobe and Pillow are used; no API is called. The helper intentionally overwrites generated outputs, never assets. Older workflow helpers and environment startup instructions describe prior edits; follow this latest owner correction.
