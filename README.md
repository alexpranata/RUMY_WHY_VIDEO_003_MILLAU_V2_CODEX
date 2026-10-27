# RUMY WHY — Video 003: Millau Viaduct V2

**Ready-to-use Codex production project**, updated for owner feedback on 27 Oct 2026. Focus: BRIGHT vivid 3D documentary graphics with observable engineering actions, not generic flyover/zoom. Google Flow creates footage **manually**, six seconds per clip. Codex only edits assets that exist locally.

## Existing assets are preserved — VERY IMPORTANT
The owner **already generated `S01.mp4` through `S12.mp4`** in the earlier project. DO NOT DELETE or rewrite them. This fresh V2 archive has no source video assets; it is a documentation + tooling package. If updating your existing folder, merge `AGENTS.md`, `CODEX_START_PROMPT.md`, `docs/` and `scripts/` into that workspace. Leave its `assets/video/` and `assets/audio/` intact.

- Existing: `assets/video/S01.mp4` ... `S12.mp4` (6s per original source)
- Better replacement, only when manually generated: `assets/video/S05_v2.mp4`, etc.
- Keep old files as fallback. Editing preference = **v2 replacement when present**, otherwise original.
- Existing ElevenLabs original narration finished at **68.4 seconds**. If already downloaded to workspace, keep it. Its exact original script is `docs/VOICEOVER_V1_ALREADY_GENERATED.txt`.
- Recommended improved narration: `docs/VOICEOVER_V2_RECOMMENDED.txt` (172 words). Audio for V2 is **not** part of this package and has **not** been generated; generate manually only if you want to spend additional credits. When provided as `assets/audio/voiceover_v2.wav` or `voiceover_v2.mp3`, Codex should use it.

## Start here
1. Read `CODEX_START_PROMPT.md` then `AGENTS.md` and the docs.
2. Run `python3 scripts/check_assets.py` from the repository root.
3. Put existing S01–S12 in `assets/video/` and one voiceover in `assets/audio/` if not present.
4. Use `docs/GOOGLE_FLOW_V2_COPY_PASTE.md` to generate **only poor scenes** in Flow, separately, saving to `SXX_v2.mp4`.
5. Codex audits visuals before editing, selects best takes, synchronizes actual narration, creates informative yellow overlays and review frames, then renders quality-controlled final Short.
6. `python3 scripts/render_roughcut.py` can render a **plain footage+VO assembly preview** if enough assets exist. It is not the polished final video. This script deliberately does not fabricate AI scenes or captions and does not modify sources.

## Core deliverables
- `output/draft/` — assembly rough cut, review captures
- `output/final/RUMY_WHY_003_MILLAU_FINAL.mp4` — edited, captions, color, graphics, music only if licensed, voiceover
- `output/final/QA_V2.md` — factual + media technical QA, actual output duration, review notes, warnings
- `output/final/review_frames/` — still frames of each engineering stage

## Audio selection caution
Older *generated* script and improved V2 script differ. NEVER subtitle the older 68.4s audio with the new words. Automatic selection requirements in `docs/VOICEOVER_DECISION.md`.

## Key technical facts
Seven concrete piers; 245m highest pier; 343m highest complete structure (top pylon); self-climbing forms ~4m / 3days; steel deck made on land on two ends; 64 hydraulic translators, 18 launch operations; red temporary towers, two early launch-support pylons and five later pylons; meeting 28 May 2004. All graphics must be fact checked against `docs/RESEARCH_VERIFIED.md`.

## No paid APIs, no rights-uncleared references
No use of paid video/TTS generation APIs; user generates in Google Flow/ElevenLabs manually. Mississippi reference clip guides aesthetic only; NEVER included in final footage. Do not use internet/stock archival images in final without license.
