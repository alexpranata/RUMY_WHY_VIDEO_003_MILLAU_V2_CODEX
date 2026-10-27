from pathlib import Path
import json,csv,re,hashlib
R=Path(__file__).resolve().parents[2];P=R/'output/reports'
rows=[
('S01','2/3/3/3/3','4/5/3/4/4','V2','Active pier construction, bucket/crane and workers replace a finished-bridge flyover. Pier scale is illustrative; no image-anchored measuring line.'),
('S02','1/3/3/3/4','2/5/3/3/4','V2','Brighter valley and blue sky. Bridge appears progressively, so use as location/finished-context illustration, not construction order or surveyed geography.'),
('S03','1/3/3/3/4','4/5/3/4/4','V2 for drilling; original for valley context','V2 shows drill and underground shafts. Cutaway depth/shafts are conceptual. Original has useful valley/pier context, not drilling.'),
('S04','2/3/3/3/4','3/5/3/3/4','V2','Cutaway illustrates a cap and shafts; exact shaft geometry not validated. No dimensions drawn over it.'),
('S05','2/3/3/3/4','3/5/3/3/4','V2 plus explanatory diagram','Red guarded formwork is visible. Three samples do not prove a complete hydraulic climb cycle; explain pour/strength/climb with schematic.'),
('S06','2/3/2/3/4','2/5/1/3/3','Neither for growth; original schematic','Original is deck construction, not pier growth. V2 upper formwork/segments separate in samples; unsuitable as evidence of climbing. New staged schematic replaces it.'),
('S07','3/3/3/3/4','4/5/3/4/3','V2','V2 shows steel assembly and welding on land. Original is support/launch hardware. V2 generated top-left text covered by opaque brand panel.'),
('S08','2/3/3/3/4','4/5/2/4/4','V2 with schematic','Original is broad launch context. V2 is a useful ram closeup, not a verified translator drawing. On-screen schematic explains direction without tracking.'),
('S09','3/3/2/3/4','3/5/2/4/4','V2 early 0.1–2.6s plus schematic','Early V2 shows red support towers. Later V2 adds several completed pylons and changing deck geometry; excluded. Diagram explains two leading launch pylons.'),
('S10','4/3/3/4/4','2/5/2/4/4','Original preferred; closure schematic','Original frames show two deck noses and guarded gap. V2 camera travels along open box girders instead of demonstrating closure. Both are CGI, not proof of millimetric fit.'),
('S11','1/3/3/3/4','4/5/2/4/4','V2 early section','Original is completed bridge. V2 shows an inclined mast and raising equipment. Rigging/base detail unverified; do not claim a validated hinge mechanism or attached final stays.'),
('S12','1/3/3/3/4','2/5/3/4/4','V2','Clear vivid completed-bridge payoff; no red temporary towers in sampled frames. Exact topology and stay count not independently validated.')]
text='''# Best-take selection — V2\n\nEvidence: all 24 actual source files were probed; three decoded frames per take (0.4s, midpoint, end minus 0.4s) were inspected in contact sheets. This is sampled visual review, not uninterrupted playback or verified motion tracking. Scores are provisional editorial judgments, not engineering certification.\n\nScore order (0–5): visible process / brightness / geometry plausibility / purposeful camera evidence / safe material and overlay space. Weights for process, geometry, brightness, camera, space are 35/25/20/15/5%. Camera and safety cannot be fully established from three frames.\n\n| Scene | Original | V2 | Selection | Observed reason / required improvement |\n|---|---|---|---|---|\n'''
for row in rows:text+='| '+' | '.join(row)+' |\n'
text+='\nPriority for optional owner improvement: S06 physically continuous climbing cycle; S08 verified translator geometry; S09 coherent supported launch with only leading pylons; S10 clear approach/closure; S11 coherent raising rigging. S05 should visibly show a controlled climb. No regeneration was requested or performed. All source files remain untouched.\n'
(P/'shot_selection.md').write_text(text)
words=json.loads((P/'vo_word_alignment.json').read_text())
path=P/'timeline_alignment.csv';data=list(csv.DictReader(path.open()));fields=list(data[0])+['actual_audio_cue','alignment_method']
for row in data:
 a=float(row['timeline_in_s']);b=float(row['timeline_out_s']);ws=[re.sub(r'\(\d+\)$','',w['word']) for w in words if a<=w['start']<b and not w['word'].startswith(('<','['))]
 row['actual_audio_cue']=' '.join(ws);row['alignment_method']='PocketSphinx 5.0.4 forced alignment on decoded 16 kHz PCM; provisional, listen review pending'
with path.open('w') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(data)
# Standard SRT sidecar for owner inspection (render uses same ASS captions).
ass=(R/'output/work/finish.ass').read_text();entries=[]
def st(s):
 h,m,sec=s.split(':');val=float(sec);return f'{int(h):02}:{int(m):02}:{int(val):02},{round((val%1)*1000):03}'
for line in ass.splitlines():
 if line.startswith('Dialogue: 5,'):
  p=line.split(',',9);text=re.sub(r'\{[^}]*\}','',p[9]).replace('\\N','\n');entries.append(f'{len(entries)+1}\n{st(p[1])} --> {st(p[2])}\n{text}\n')
(R/'output/final/captions_V2.srt').write_text('\n'.join(entries))
print('Wrote shot selection, cue-enriched timeline, caption sidecar')
