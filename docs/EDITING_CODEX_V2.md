# Edit & motion graphics spec — YouTube Shorts

## Story and rhythm
- User wants a visual **engineering-process** story, not an aesthetically pleasing bridge slideshow.
- Alternate 2–4 second *detail* (workers/mechanical operation) with 4–6 second *context* (tower relative to valley/launch across gap).
- Prefer cut on physical action, specific VO beats, engineering narrative shifts; speed ramps only on footage with sufficient temporal clarity.
- Each source clip is 6s maximum. Final video need NOT have 12 equal 6s scenes. Use additional controllable explanation graphics rather than visual loops or forced slow motion when VO continues.
- Do not simply apply a generic zoom overlay to every scene; S05 hydraulic form climbing and S08 translation mechanics need intelligible time/space.

## Color grade
- Make the source material brighter and less gray: neutral clean Rec.709, luminous green terrain and blue sky with natural saturation. Avoid crushed blacks, dull muddy olive palette, overly warm orange sky, overblown white forms and fake fog.
- Suggest baseline candidate ONLY, adjust visually: exposure +0.15–0.4 stops, midtones gently up, vibrance +5 to +12%, local contrast moderate, preserve white cloud/sky details; per-shot corrections for consistency.
- If a clip is genuinely too dark, re-render or replace instead of extreme gamma boosting and banding.

## Graphics system
- Brand yellow `#FFD400` for arrows, braces, measuring lines, highlights and circles.
- White technical labels with dark soft backplate/shadow, 1080x1920 at 30fps.
- Max 1–2 fact labels at once; type hierarchy: number -> unit -> short context.
- Use only sourced facts from RESEARCH_VERIFIED. High structural height `343 M / 1,125 FT` at tip of tallest pylon, tallest CONCRETE pier `245 M / 804 FT` distinct. 4 m / 3 DAYS represents historical formwork rise, and 60 CM/CYCLE describes hydraulic translator operation; never use an onscreen measuring line anchored to hallucinated AI geometry.
- First show `PIER = 804 FT`, then quick climbing-formwork inset (a *diagram*, not a photo simulation), then steel deck translator diagram showing force/path. Do not display exact angles or technical force distribution without a legitimate diagram.
- Stable on-screen graphic anchoring preferred. If motion tracking cannot be verified, label diagram as SCHEMATIC and use screen-space annotation. No invented point tracking.

## Subtitle safe area and Shorts UI
- Dynamic subtitle 2 lines maximum, no word-by-word flashing that competes with mechanisms. Start around 70-76% canvas height; prevent overlap with important machines, lower UI and yellow arrows. Manually inspect on phone-scale preview.
- Captions white, with restrained black outline/shadow; optional yellow on critical number/verb only. Absolutely no text baked into Google Flow input clips.
- Technical labels positioned to side on open sky / flat terrain; subtitle should be top layer in composite.

## Audio
- Voiceover loud and upfront, consistent; high-pass low frequencies ~70-90Hz as needed. Peak safety (avoid clipping); inspect integrated loudness rather than enforce loudness blindly.
- Optional light tool SFX (hydraulic actuator, welder, crane) only if sourced/licensed. Music must be owner provided and rights cleared; lower under speech. No generated footage audio if distracting.
- End with brief music/sfx tail only if it fits actual VO; avoid silently stretching.

## Construction timeline notes
- CGI formwork stage must communicate a safe controlled lift, not unsupported workers or magical rapid concrete hardening.
- Show two launch fronts, red temporary supports, front stay-assisted pylons, only then 5 remaining pylons after bridge meets.
- In final reveal remove temporary red towers and cranes.

## Output
- Draft: `output/draft/RUMY_WHY_003_V2_ROUGHCUT.mp4`
- Final: `output/final/RUMY_WHY_003_MILLAU_FINAL.mp4` 1080x1920/30fps/H264/AAC; final cut determined by narration.
- QA: `output/final/QA_V2.md` with actual code commands/media metrics, manual visuals, remaining issues, color consistency, overlays provenance, audio and subtitle match.
- Review frames for at least S01/S03/S05/S06/S08/S09/S10/S11/S12 at `output/final/review_frames`.
