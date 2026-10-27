"""Owner correction: footage + existing VO + subtitles only. Sources immutable."""
from pathlib import Path
import subprocess,json,csv,re,shutil,hashlib
R=Path(__file__).resolve().parents[2];W=R/'output/work/simple';F=R/'output/final';P=R/'output/reports';W.mkdir(exist_ok=True,parents=True)
segments=[('S01',0,6,'S01_v2.mp4',0),('S02',6,11.3,'S02_v2.mp4',.2),('S03',11.3,15.3,'S03_v2.mp4',.2),('S04',15.3,17.8,'S04_v2.mp4',.3),('S05',17.8,23,'S05_v2.mp4',.2),('S06',23,28.4,'S05.mp4',.2),('CONTEXT',28.4,33.2,'S03.mp4',.5),('S07',33.2,38.9,'S07_v2.mp4',.15),('S08',38.9,43.8,'S08_v2.mp4',.3),('SUPPORTS',43.8,46.2,'S08.mp4',1),('S09',46.2,48.7,'S09_v2.mp4',.1),('CLOSURE_WIDE',48.7,51.8,'S09.mp4',.3),('CLOSURE_DETAIL',51.8,54.9,'S10.mp4',.15),('S11',54.9,58.7,'S11_v2.mp4',.3),('S12',58.7,64.3,'S12_v2.mp4',2.3)]
source=json.loads((P/'source_hashes.json').read_text())
for p,h in source.items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h,p
# Retain the acoustically aligned captions; remove all other old ASS layers/styles.
old=(R/'output/work/finish.ass').read_text();header=old.split('[Events]')[0]
header='\n'.join(x for x in header.splitlines() if not x.startswith(('Style: Label,','Style: Small,')))+'\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
events=[]
def seconds(s):
 h,m,v=s.split(':');return int(h)*3600+int(m)*60+float(v)
def stamp(t):return f'{int(t//3600)}:{int(t%3600//60):02}:{t%60:05.2f}'
for line in old.splitlines():
 if line.startswith('Dialogue: 5,'):
  fields=line.split(',',9);fields[0]='Dialogue: 0';fields[9]=fields[9].replace(r'\pos(515,380)',r'\pos(515,1370)');events.append(fields)
for i,e in enumerate(events[:-1]):
 e[2]=stamp(min(seconds(e[2]),seconds(events[i+1][1])))
ass=W/'subtitles.ass';ass.write_text(header+'\n'.join(','.join(e) for e in events)+'\n')
assert len(events)==32
assert all(r'\p1' not in e[9] for e in events)
# SRT mirrors the new nonoverlapping burn-in timings.
def srtstamp(t):
 v=round(t*1000);return f'{v//3600000:02}:{v//60000%60:02}:{v//1000%60:02},{v%1000:03}'
srt=[]
for i,e in enumerate(events):srt.append(f"{i+1}\n{srtstamp(seconds(e[1]))} --> {srtstamp(seconds(e[2]))}\n"+re.sub(r'\{[^}]*\}','',e[9]).replace('\\N','\n')+'\n')
(F/'captions_V2.srt').write_text('\n'.join(srt))
words=json.loads((P/'vo_word_alignment.json').read_text())
with (P/'timeline_alignment.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['scene','timeline_in_s','timeline_out_s','source','source_in_s','source_out_s','actual_audio_cue','adjustments'])
 for scene,a,b,p,o in segments:
  cue=' '.join(re.sub(r'\(\d+\)$','',x['word']) for x in words if a<=x['start']<b and not x['word'].startswith(('<','[')))
  w.writerow([scene,a,b,'assets/video/'+p,o,round(o+b-a,3),cue,'Crop 160px source top to remove existing source title' if scene=='S07' else 'Cut only; no graphics'])
parts=[]
for i,(scene,a,b,p,o) in enumerate(segments):
 out=W/f'part_{i:02}.mp4';n=round((b-a)*30)
 vf=('crop=iw:ih-160:0:160,' if scene=='S07' else '')+'fps=30,scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1,format=yuv420p'
 subprocess.run(['ffmpeg','-v','error','-nostdin','-y','-threads','2','-ss',str(o),'-i',str(R/'assets/video'/p),'-an','-vf',vf,'-frames:v',str(n),'-c:v','libx264','-threads','3','-preset','veryfast','-crf','20',str(out)],check=True)
 parts.append(f"file '{out}'");print('Rendered',scene,flush=True)
(W/'parts.txt').write_text('\n'.join(parts)+'\n')
rough=R/'output/draft/RUMY_WHY_003_V2_ROUGHCUT.mp4'
subprocess.run(['ffmpeg','-v','error','-nostdin','-y','-f','concat','-safe','0','-i',str(W/'parts.txt'),'-i',str(R/'assets/audio/voiceover_v2.mp3'),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-t','64.3','-movflags','+faststart',str(rough)],check=True)
# Same owner V2 narration, same natural cadence; no synthesis or source-clip sound.
af='loudnorm=I=-16:TP=-1.5:LRA=9:measured_I=-23.48:measured_TP=-2.52:measured_LRA=3.30:measured_thresh=-33.87:offset=0.81:linear=false'
final=F/'RUMY_WHY_003_MILLAU_SIMPLE.mp4'
subprocess.run(['ffmpeg','-v','warning','-nostdin','-y','-i',str(rough),'-vf',f'ass={ass}','-af',af,'-ar','48000','-c:v','libx264','-threads','3','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','192k','-t','64.3','-movflags','+faststart',str(final)],check=True)
shutil.copy2(final,F/'RUMY_WHY_003_MILLAU_FINAL.mp4')
print('Simple export written. QA pending.',flush=True)
