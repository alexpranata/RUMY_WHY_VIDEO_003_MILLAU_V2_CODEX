"""Word-at-a-time captions and verified pixel-following attention animations. No source changes."""
from pathlib import Path
import subprocess,json,re,math,shutil,hashlib
from PIL import ImageFont
R=Path(__file__).resolve().parents[3];W=R/'output/work/kinetic';P=R/'output/reports';F=R/'output/final'
source=json.loads((P/'source_hashes.json').read_text())
for p,h in source.items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h,p
words=[x for x in json.loads((P/'vo_word_alignment.json').read_text()) if not x['word'].startswith(('<','['))]
tokens=(R/'docs/VOICEOVER_V2_RECOMMENDED.txt').read_text().split(); captions=[];wi=0;i=0
# Numeric display preserves spoken meaning. Multi-word numbers are a single readable numeric token.
substitutions=[(['eleven','hundred','twenty-five'],'1,125'),(['two','thousand','four.'],'2004.'),(['eight-hundred-foot'],'800-foot'),(['Sixty-four'],'64'),(['seven'],'7'),(['thirteen'],'13'),(['eighteen'],'18')]
while i<len(tokens):
 display=tokens[i];consumed=1
 for phrase,replacement in substitutions:
  if [x.lower() for x in tokens[i:i+len(phrase)]]==[x.lower() for x in phrase]:display=replacement;consumed=len(phrase);break
 original=' '.join(tokens[i:i+consumed]);n=len(re.findall(r"[a-z]+(?:'[a-z]+)?",original.lower()))
 a=words[wi]['start'];b=words[wi+n-1]['end'];captions.append({'spoken':original,'display':display.upper(),'start':a,'spoken_end':b});wi+=n;i+=consumed
assert wi==len(words),(wi,len(words))
keywords={'ENGINEERS','BUILD','CONCRETE','PIER','MILLAU','VIADUCT','DRILLED','FOUNDATION','BEDROCK','HOLLOW','PIERS','SELF-CLIMBING','FORMWORK','STRENGTH','RAISED','AGAIN','STEEL','ROADWAY','ASSEMBLED','DECK','LAND','SIDES','HYDRAULIC','TRANSLATORS','PUSHED','TEMPORARY','RED','TOWERS','CABLES','LAUNCHING','MET','PYLONS','COMPLETE','SKY'}
for idx,c in enumerate(captions):
 start_frame=round(c['start']*30);next_frame=round(captions[idx+1]['start']*30) if idx+1<len(captions) else 1929
 end_frame=min(next_frame,max(start_frame+1,round((c['spoken_end']+.09)*30)));assert end_frame>start_frame,c
 c.update(start_frame=start_frame,end_frame=end_frame,highlight=bool(re.search(r'\d',c['display']) or c['display'].strip('.,?!') in keywords))
assert all(x['end_frame']<=y['start_frame'] for x,y in zip(captions,captions[1:]))
header='''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Word,DejaVu Sans,88,&H00FFFFFF,&H00FFFFFF,&H00161616,&H80000000,-1,0,0,0,100,100,0,0,1,4,2,5,80,130,0,1
Style: Graphic,DejaVu Sans,24,&H0000D4FF,&H0000D4FF,&H0000D4FF,&H80000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
def ts(t):return f'{int(t//3600)}:{int(t%3600//60):02}:{t%60:05.2f}'
events=[]
def event(layer,a,b,style,txt):events.append(f'Dialogue: {layer},{ts(a)},{ts(b)},{style},,0,0,0,,{txt}')
for c in captions:
 text=c['display'];key=c['highlight'];size=110 if re.search(r'\d',text) else (96 if key else 88)
 font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',size)
 while font.getlength(text)*1.1>850:size-=2;font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',size)
 color='00D4FF' if key else 'FFFFFF';pop=112 if key else 105
 a=c['start_frame']/30;b=c['end_frame']/30;ms=min(90,max(20,int((b-a)*650)))
 txt=r'{\q2\an5\pos(515,1370)\fs'+str(size)+r'\1c&H'+color+r'&\fscx'+str(pop)+r'\fscy'+str(pop)+rf'\t(0,{ms},\fscx100\fscy100)'+'}'+text
 event(5,a,b,'Word',txt)
tracks=json.loads((P/'object_tracks.json').read_text())
# Optical-flow targets were visually checked at start/mid/end. Drill tracking failed visual verification and was omitted.
def shape(a,b,path,fill=False):
 # ASS closes open contour borders. Convert the intended open polyline into a
 # narrow filled ribbon so arcs stay open and corner brackets do not become triangles.
 if not fill:
  nums=[float(x) for x in re.findall(r'-?\d+(?:\.\d+)?',path)];pts=list(zip(nums[::2],nums[1::2]));left=[];right=[]
  for i,(x,y) in enumerate(pts):
   before=pts[max(0,i-1)];after=pts[min(len(pts)-1,i+1)];dx=after[0]-before[0];dy=after[1]-before[1];length=max(.001,math.hypot(dx,dy));nx=-dy/length*2.5;ny=dx/length*2.5;left.append((x+nx,y+ny));right.append((x-nx,y-ny))
  polygon=left+right[::-1];path='m '+point(*polygon[0])+' l '+' '.join(point(*p) for p in polygon[1:])+' '+point(*polygon[0])
 tags=r'{\an7\pos(0,0)\shad1\4c&H181818&\1c&H00D4FF&\3c&H181818&\bord0.6\1a&H00&\p1}'
 event(1,a,b,'Graphic',tags+path)
def point(x,y):return f'{x:.1f} {y:.1f}'
for track in tracks:
 name=track['object'];radius={'formwork_jack':88,'translator':170,'red_support':105,'mast_tip':90}[name]
 for row in track['samples']:
  a=row['frame']/30;b=(row['frame']+1)/30;t=a-track['start'];cx=row['cx'];cy=row['cy'];pulse=1+.065*math.sin(t*2*math.pi/1.1);rr=radius*pulse
  if name=='translator':
   # Breathing corner brackets frame the ram; no fake force direction or dimensions.
   ww=295*pulse;hh=115*pulse;L=44
   for dx,dy in [(-1,-1),(1,-1),(-1,1),(1,1)]:
    x=cx+dx*ww;y=cy+dy*hh
    shape(a,b,'m '+point(x-dx*L,y)+' l '+point(x,y)+' '+point(x,y-dy*L))
  else:
   # Rotating broken halo highlights a real object without replacing/morphing it.
   for offset in [0,math.pi]:
    angles=[offset+t*1.2+j*math.pi*.78/20 for j in range(21)]
    path='m '+point(cx+rr*math.cos(angles[0]),cy+rr*math.sin(angles[0]))+' l '+' '.join(point(cx+rr*math.cos(q),cy+rr*math.sin(q)) for q in angles[1:]);shape(a,b,path)
  # Short attention arrow approaches the selected object's edge, following its pixel center.
  ex=cx+rr*.72;ey=cy-rr*.72;gap=70+12*math.sin(t*5);sx=ex+gap;sy=ey-gap
  shape(a,b,'m '+point(sx,sy)+' l '+point(ex,ey))
  shape(a,b,'m '+point(ex,ey)+' l '+point(ex+28,ey-7)+' '+point(ex+7,ey-28)+' '+point(ex,ey),True)
ass=W/'word_highlights.ass';ass.write_text(header+'\n'.join(events)+'\n');(P/'word_caption_map.json').write_text(json.dumps(captions,indent=2))
def srt_ts(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
srt='\n'.join(f"{i+1}\n{srt_ts(c['start_frame']/30)} --> {srt_ts(c['end_frame']/30)}\n{c['display']}\n" for i,c in enumerate(captions))
(F/'captions_WORD.srt').write_text(srt);(F/'captions_V2.srt').write_text(srt)
print('Word captions:',len(captions),'highlighted:',sum(c['highlight'] for c in captions),'tracked objects:',len(tracks),flush=True)
# Raw assembly is unchanged; re-render directly from it, never from an export with old captions burned in.
rough=R/'output/draft/RUMY_WHY_003_V2_ROUGHCUT.mp4'
af='loudnorm=I=-16:TP=-1.5:LRA=9:measured_I=-23.48:measured_TP=-2.52:measured_LRA=3.30:measured_thresh=-33.87:offset=0.81:linear=false'
final=F/'RUMY_WHY_003_MILLAU_HIGHLIGHT.mp4'
subprocess.run(['ffmpeg','-v','warning','-nostdin','-y','-i',str(rough),'-vf',f'ass={ass}','-af',af,'-ar','48000','-c:v','libx264','-threads','3','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','192k','-t','64.3','-movflags','+faststart',str(final)],check=True)
shutil.copy2(final,F/'RUMY_WHY_003_MILLAU_FINAL.mp4');print('Highlight export written; QC pending.',flush=True)
