# Audio selection and synchronization — do not silently mismatch scripts

## DEFAULT when you already have voiceover from yesterday
The existing ElevenLabs narration completed successfully and is **68.4 seconds** according to the generation record. Its **exact submitted script** is `docs/VOICEOVER_V1_ALREADY_GENERATED.txt`. The project pack does **NOT** contain a copy of its audio; the owner downloads it and places it in `assets/audio/`.

- If `assets/audio/voiceover_v2.wav` or `.mp3` exists: use it and align `docs/VOICEOVER_V2_RECOMMENDED.txt`.
- Else if `assets/audio/voiceover.wav` or `.mp3` or `assets/audio/voiceover_original.*` exists: use that original audio and align `docs/VOICEOVER_V1_ALREADY_GENERATED.txt`.
- If there are multiple candidates without a clearly named v2, do not guess: report selection and use only a deterministic priority, leaving originals untouched.
- NEVER overlay V2 subtitles onto V1 speech. Both narrations have different word order and different key facts.
- If the user wants maximum construction detail, the recommended V2 narration is better. But **generating V2 is an optional manual step** and requires ElevenLabs credits. Do not call APIs to create it, and do not block editing with V1.
- Keep natural spoken durations: V1 is 68.4 s; V2 is a draft of 172 words and its duration is **unknown until actually generated**. Do not fabricate a 70-second result.

## Alignment method
1. Use voiceover as timeline master. Probe actual length via ffprobe.
2. Use local word alignment if available without paid APIs; otherwise manually mark phrase start/end against waveform.
3. `docs/STORYBOARD_V2.csv` carries both audio cue sets (`v1_audio_cue` and `v2_audio_cue`). They are **search anchors, not subtitles or verified timestamps**.
4. Map engineering visuals to narrative phrases, cutting/rearranging/reusing footage as needed. `6 seconds` is per Flow source clip, NOT locked final screen time.
5. If narration exceeds 72 seconds after trims, use licensed stills or controlled diagrams; do not duplicate video via obvious loops or falsely claim footage length.

## Recommended narration delivery
Natural American English, documentary curiosity, bright/calm energetic, rhythm ~145–160 WPM; stress `self-climbing formwork`, `sixty-four hydraulic translators`, `eighteen launches`. Short dramatic emphasis on `Again. And again.` No applause, voices or music baked into exported narration.
