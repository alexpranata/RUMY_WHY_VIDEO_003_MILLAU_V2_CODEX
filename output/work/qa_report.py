from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[2];P=R/'output/reports';F=R/'output/final';v=json.loads((P/'final_validation.json').read_text());m=json.loads((P/'final_ffprobe.json').read_text());q=v['loudness']
report=f'''# RUMY WHY 003 — Millau V2 QA

Date: 27 October 2026 (Asia/Jakarta).

**Release decision: REVIEW REQUIRED. Final PASS is withheld.**

A real export exists and has passed the technical checks listed below. Final uninterrupted motion review, subjective audio playback and listening against the burned-in captions remain outstanding. This execution interface supplied decoding and local speech-recognition evidence, but no dependable way to perform a subjective listening review. No claim of having listened to the complete final program is made. Do not publish this as a fully approved final until those checks are completed.

## Delivered files

- `output/final/RUMY_WHY_003_MILLAU_FINAL.mp4` — composed export with owner narration, English burned-in captions, screen-space labels and schematic animation.
- `output/draft/RUMY_WHY_003_V2_ROUGHCUT.mp4` — pre-polish assembly using the same selection and timing. Schematic intervals are plain background placeholders here; use the composed export to review the explanatory animation.
- `output/final/captions_V2.srt` — matching English caption sidecar.
- `output/final/review_frames/` — actual decoded export frames and contact sheet.
- `output/reports/asset_audit.json`, `shot_selection.md`, `timeline_alignment.csv` — source inventory, comparative choices and real-narration cue map.
- `output/reports/vo_word_alignment.json` — acoustic word timings, not storyboard estimates.
- `output/work/produce_v2.py`, `align.py`, `write_reports.py`, `verify_v2.py` — reproducible local editing/alignment/QA helpers, not changes to application source.

## Actual measured media

| Property | Measured result |
|---|---|
| Container / video / audio duration | {v['container_duration']} / {v['video_duration']} / {v['audio_duration']} s |
| Video | H.264, 1080 × 1920, yuv420p, 30/1 fps |
| Actual decoded frames | {v['frames']} |
| Audio | AAC, 48 kHz, owner mono narration, 192 kb/s target |
| Caption events | {v['caption_events']}; at most two explicit lines; full script text verified by producer assertion |
| Final measured loudness | {q['input_i']} LUFS integrated |
| Final measured true peak | {q['input_tp']} dBTP |
| Final measured loudness range | {q['input_lra']} LU |
| Full decode | Exit {v['decode_exit']}; all video/audio decoded to null |
| Black detection | {len(v['black_segments'])} segments at threshold 0.02 / minimum 0.1s |
| Source integrity | All {v['source_files_verified']} original asset files unchanged by SHA-256 |

Final MP4 SHA-256: `{v['sha256']}`.

Evidence: `final_ffprobe.json`, `final_validation.json`, `final_decode_audio_qc.log`, `source_hashes.json`, `source_integrity.json`. The final-audio loudness numbers above are the **input** measurement from the QC analysis of the exported AAC; the second normalization output in the diagnostic log was discarded, not used as the reported measurement.

## Narration and alignment

Only `assets/audio/voiceover_v2.mp3` is present. Its probed MP3 duration is 64.287347s, not the owner's earlier V1 generation duration of 68.4s. Existing V1 audio was not present and was not synthesized. Local unconstrained PocketSphinx recognition follows the V2 narrative (climbing forms, thirteen-foot lift, remaining pylons, ending “They pushed it there”), with normal recognizer substitutions documented verbatim in `vo_recognition.txt`. This supports the V2 selection; it is not perfect transcription or a substitute for hearing the original.

Caption wording comes only from `docs/VOICEOVER_V2_RECOMMENDED.txt`; no recognizer errors were copied into captions. Pocketsphinx 5.0.4 forced alignment used the actual decoded 16 kHz waveform, with explicit pronunciations for missing formwork/Tarn/tensioned dictionary words. Timing remains provisional until listening review; no timing-accuracy guarantee is made. The cue CSV includes actual aligned words at each edit. Export duration is frame-quantized to 64.3s, without time-stretching narration or forcing a 72s target.

The VO was loudness-normalized with controlled true peak. There is no added music/SFX because no licensed audio files were supplied, and no Flow-clip sound was used. No speech was synthesized and no paid media APIs, external footage downloads or Google Flow logins were used.

## Visual and engineering review

The audit executed `python3 scripts/check_assets.py` before editing. All 24 actual clips were probed and three frames per take inspected (early/middle/late); source contact sheets are retained. This establishes sampled visual evidence, not continuous motion certification. Several V2 sources run 8 seconds, rather than the nominal 6 seconds. No source is slowed or looped; ordinary conversion to the output 30fps grid is used.

Most V2 takes are visibly brighter and more explanatory than the originals. Original S03 is retained for valley/pier context, and original S10 is preferred for the visible guarded closure gap. S06 V2 shows separated formwork/segments in sampled frames; its misleading growth footage is excluded and replaced by a staged, explicitly schematic hollow-pier/climbing illustration. S05's formwork is visible but a complete physical climb cycle is not verified; the scheme clarifies gain strength/climb/repeat. Later S09 V2 frames have questionable multiple-pylon/deck evolution; only its early 0.1–2.6s range is used, with a separate two-front launch-support schematic. S10 V2 is excluded because its open-girder camera path is weaker evidence of deck closure. S11 V2 early mast-raising footage is retained as CGI; its detailed rigging geometry is not certified. See every scene's scored selection and limitations in `shot_selection.md`.

Reviewed final samples cover hook, location, drilling, foundation, formwork, staged climb, ground assembly, hydraulic closeup, launch supports, closure, mast raising, completed bridge and ending. Captions are positioned in the upper safe zone, deliberately above the diagrams and technical labels; this differs from the suggested lower placement to preserve that hierarchy and keep mechanisms visible. White captions use a restrained dark outline. Fixed-position labels and graphics use brand yellow #FFD400 and white type. No unverified motion tracking or geometry-anchored measurement is claimed. All engineering overlays derive from the repository's verified-facts document, not measurements of generated footage.

Construction order is foundations → hollow piers/formwork → steel assembled on both sides → incremental launch with red temporary supports and two leading stayed pylons (schematic) → deck closure → five remaining pylons → completion. The 245m pier and 343m maximum structural height are explicitly distinguished. The 4m/three-days rise is labeled conceptual time-lapse, never an instantaneous real-time cure. The 64-translator total is project-wide and the ~60cm cycle is schematic. Closure is dated 28 May 2004. No label asserts a single simultaneous 36,000t push. The final sampled payoff has no temporary red towers. Exact seven-pylon/stay topology of the AI source has not been independently established; the imagery is labeled CGI reconstruction throughout.

## Outstanding release checks and limits

1. Play the full 64.3s exported MP4 with sound: verify owner VO identity, clarity, no clicks/harshness, all spoken words, the ending and caption synchronization. Adjust any local forced-alignment errors if heard.
2. Review continuous motion at full and phone scale, particularly S03 cutaway geometry, S05 climbing action, S08 mechanism, early S09 support continuity, S10 closure and S11 raising rigging. Sampled review cannot rule out intermediate morphing or unsafe geometry.
3. Final hero-shot geometry is illustrative, not a validated reconstruction. Any obvious geometry defect found in playback must be trimmed, schematically replaced or replaced with an improved owner-supplied take. No regeneration is required or performed automatically.
4. Rights clearance rests on the owner-provided source provenance. No third-party stock or reference footage was added.

The final MP4 is a review export at the requested delivery path. It must not be described as final PASS while the listening and uninterrupted-motion checks remain pending.

## Reuse and environment

The existing checkout is already isolated; do not create a worktree. Local helpers live under output/work and never write into assets. The rendering helper overwrites generated output paths when deliberately rerun; preserve wanted output versions first. `--reuse-parts` is only for this unchanged edit and verifies source hashes and expected frame counts; omit it if changing timeline or source choices.

Run from the repository root with `/workspace/millau-tools/bin/python`: `output/work/align.py` (after 16kHz PCM decode), `output/work/produce_v2.py`, `output/work/write_reports.py`, then `output/work/verify_v2.py`. Read each helper before adapting a different VO: the current producer intentionally contains this edit's 64.3s timeline. FFmpeg and ffprobe are present; local Python packages are PocketSphinx 5.0.4 and Pillow 12.3.0. The nonfatal fontconfig cache warning did not prevent caption rendering; reviewed frames confirm the text is present.

Reusable install_script and start_skill fields were saved successfully in the environment draft. Saving does not publish: review and save the environment settings and then publish the environment to retain this prepared state for future tasks. Fresh-task restoration has not been independently tested. No Git push of these generated outputs was performed in this editing pass; tracked project and asset files remain unchanged.
'''
(F/'QA_V2.md').write_text(report)
print('QA_V2.md written; REVIEW REQUIRED, not final PASS')
