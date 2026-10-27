# Archived graphics edit helper. Owner requested footage + VO + subtitles only; use produce_simple.py instead.
from pathlib import Path
import subprocess,json,re,csv,textwrap,math
R=Path(__file__).resolve().parents[2]; W=R/'output/work'; REPORT=R/'output/reports'; F=R/'output/final'; D=R/'output/draft'
for p in [F,D,F/'review_frames']:p.mkdir(exist_ok=True,parents=True)
segments=[
('S01',0,6.0,'S01_v2.mp4',0,'PIER / 245 M · 804 FT','Highest concrete pier'),
('S02',6.0,11.3,'S02_v2.mp4',.2,'MAX STRUCTURAL HEIGHT / 343 M','To pylon top · not roadway height'),
('S03',11.3,15.3,'S03_v2.mp4',.2,'DRILLED FOUNDATIONS','Underground cutaway is schematic'),
('S04',15.3,17.8,'S04_v2.mp4',.3,'SEVEN HOLLOW CONCRETE PIERS','Foundation illustration · not to scale'),
('S05',17.8,23,'S05_v2.mp4',.2,'SELF-CLIMBING FORMWORK','Pour → gain strength → climb'),
('S06',23,28.4,None,0,'ABOUT 4 M / THREE DAYS','Conceptual time-lapse · not real-time'),
('CONTEXT',28.4,33.2,'S03.mp4',.5,'NEXT / CROSS THE VALLEY','Steel deck assembled from both sides'),
('S07',33.2,38.9,'S07_v2.mp4',.15,'ASSEMBLED ON LAND','Steel box-girder sections · two sides'),
('S08',38.9,43.8,'S08_v2.mp4',.3,'64 HYDRAULIC TRANSLATORS','Project-wide total · ~60 cm per cycle'),
('S09_DIAGRAM',43.8,46.2,None,0,'SUPPORTED THROUGH THE LAUNCH','Two fronts · leading pylon on each'),
('S09',46.2,48.7,'S09_v2.mp4',.1,'TEMPORARY RED TOWERS','Stay-assisted launch · CGI illustration'),
('S10',48.7,51.8,'S10.mp4',.15,'18 LAUNCHING OPERATIONS','Deck meeting · 28 May 2004'),
('CLOSURE',51.8,54.9,None,0,'DECK MEETING / 28 MAY 2004','Closure detail · schematic · not to scale'),
('S11',54.9,58.7,'S11_v2.mp4',.3,'FIVE REMAINING PYLONS','Raised after deck closure'),
('S12',58.7,64.3,'S12_v2.mp4',2.3,'MILLAU VIADUCT / 2004','They pushed it there.')]
# All boundaries quantized to the output frame grid. Never slow or loop a source.
segments=[(s,round(a*30)/30,round(b*30)/30,p,o,t,u) for s,a,b,p,o,t,u in segments]
with (REPORT/'timeline_alignment.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['scene','timeline_in_s','timeline_out_s','source','source_in_s','source_out_s','narration_alignment','graphics'])
 for s,a,b,p,o,t,u in segments:w.writerow([s,a,b,'SCHEMATIC' if not p else 'assets/video/'+p,o,round(o+b-a,3) if p else '', 'V2 PocketSphinx acoustic forced alignment; word JSON retained',t+' / '+u])
# Caption text is taken from owner V2 script, never recognition substitutions.
words=json.loads((REPORT/'vo_word_alignment.json').read_text()); words=[w for w in words if w['word'] not in ['<sil>','</s>','<s>','[SPEECH]']]
script=(R/'docs/VOICEOVER_V2_RECOMMENDED.txt').read_text(); tokens=script.split(); groups=[]; group=[];idx=0
phrases="How did engineers build\nan eight-hundred-foot concrete pier\nin a valley... and put a highway on top?\nFrance's Millau Viaduct reaches\neleven hundred twenty-five feet\nat its highest point.\nFirst, engineers drilled\ndeep foundation shafts into bedrock.\nThen they built seven hollow concrete piers\nusing self-climbing formwork.\nCrews poured concrete,\nwaited for it to gain strength,\nand raised the formwork roughly thirteen feet\nfor the next section.\nAgain. And again.\nBut that only solved half the problem.\nThe steel roadway still had to cross the valley.\nSo instead of lifting it into place,\ncrews assembled the steel deck on land,\non both sides.\nSixty-four hydraulic translators\npushed those sections forward in small steps.\nTemporary red towers and stay cables\nsupported the advancing decks above the gaps.\nAfter eighteen launching operations,\nthe two halves met high above the Tarn River\nin May two thousand four.\nEngineers raised the remaining steel pylons\nand tensioned the cables.\nBy December, the bridge was complete.\nThey didn't build the road in the sky.\nThey pushed it there.".splitlines()
assert " ".join(phrases)==" ".join(tokens)
for phrase in phrases:
 group=[]
 for tok in phrase.split():
  count=len(re.findall(r"[a-z]+(?:'[a-z]+)?",tok.lower()));group.append((tok,idx,idx+count-1));idx+=count
 groups.append(group)
assert idx==len(words),(idx,len(words))
header='''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,DejaVu Sans,48,&H00FFFFFF,&H00FFFFFF,&H00202020,&H90000000,-1,0,0,0,100,100,0,0,1,3,1,5,100,150,0,1
Style: Label,DejaVu Sans,40,&H00FFFFFF,&H00FFFFFF,&H00202020,&H90000000,-1,0,0,0,100,100,0,0,1,2,1,5,70,120,0,1
Style: Small,DejaVu Sans,27,&H00FFFFFF,&H00FFFFFF,&H00202020,&H90000000,0,0,0,0,100,100,0,0,1,2,0,5,70,120,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
def ts(t):
 h=int(t//3600);m=int(t%3600//60);s=t%60;return f'{h}:{m:02}:{s:05.2f}'
events=[]
def event(a,b,text,style='Label',layer=1):events.append(f'Dialogue: {layer},{ts(a)},{ts(b)},{style},,0,0,0,,{text}')
def txt(a,b,text,x,y,style='Label'):event(a,b,r'{\an5\pos('+f'{x},{y}'+r')\fad(120,120)}'+text,style)
def draw(a,b,path,color='00D4FF',alpha='00',extra=''):
 event(a,b,(r'{\an7' + ('' if r'\move' in extra else r'\pos(0,0)') + r'\bord0\shad0\1c&H'+color+r'&\1a&H'+alpha+r'&'+extra+r'\p1}'+path),'Small',0)
for g in groups:
 a=words[g[0][1]]['start'];b=words[g[-1][2]]['end']; text=' '.join(x[0] for x in g)
 from PIL import ImageFont
 font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',48)
 toks=text.split(); options=[[' '.join(toks[:j]),' '.join(toks[j:])] for j in range(1,len(toks))]
 lines=min(options,key=lambda z:max(font.getlength(x) for x in z)) if font.getlength(text)>820 and options else [text]
 assert max(font.getlength(x) for x in lines)<=850,(text,lines)
 event(a,min(64.3,b+.07),r'{\q2\an5\pos(515,380)\fad(50,70)}'+'\\N'.join(lines),'Caption',5)
# Brand and explicit reconstruction notice. Covers pre-existing generated title at upper left on S07.
draw(0,64.3,'m 0 0 l 1080 0 1080 228 0 228','141A20','00')
txt(0,64.3,'R U M Y   W H Y',280,145,'Small');txt(0,64.3,'MILLAU / ENGINEERING',710,145,'Small')
txt(0,64.3,'CGI RECONSTRUCTION · NOT ARCHIVE FOOTAGE',520,195,'Small')
for s,a,b,p,o,title,sub in segments:
 draw(a,b,'m 65 1450 l 980 1450 980 1650 65 1650','141A20','15')
 # Yellow rule grows on over 0.45s; fixed screen-space, no tracking claim.
 draw(a,b,'m 85 1470 l 950 1470 950 1476 85 1476',extra=r'\clip(85,1470,86,1476)\t(0,450,\clip(85,1470,950,1476))')
 txt(a+.12,b,title,520,1530);txt(a+.12,b,sub,520,1600,'Small')
# Conceptual concrete lift: fixed hollow cross-section, distinct hardened stages; no morphing tower footage.
a,b=23,28.4
txt(a,b,'SELF-CLIMBING / SCHEMATIC',520,650)
for i in range(4):
 y=1200-i*100; start=a+max(0,i-1)*1.0
 draw(start,b,f'm 340 {y} l 660 {y} 660 {y+90} 340 {y+90}','C9CDD0')
 draw(start,b,f'm 430 {y+15} l 570 {y+15} 570 {y+75} 430 {y+75}','24313B')
for i in range(3):
 st=a+i*1.8;en=min(st+1.8,b);y=1100-i*100
 draw(st,en,f'm 310 {y-35} l 690 {y-35} 690 {y-23} 310 {y-23}')
 draw(st,en,f'm 700 {y+25} l 710 {y+25} 710 {y-20} 725 {y-20} 705 {y-45} 685 {y-20} 700 {y-20}')
 txt(st,en,['GAIN STRENGTH','CLIMB THE FORMS','REPEAT IN STAGES'][i],520,1360,'Small')
# Translator: a restrained screen-space ram and deck show direction, not fabricated tracked dimensions.
a,b=38.9,43.8
# Lower diagram avoids pretending to track piston in the generated source.
draw(a,b,'m 130 1140 l 910 1140 910 1370 130 1370','141A20','10')
txt(a,b,'TRANSLATOR CYCLE · SCHEMATIC',520,1170,'Small')
draw(a,b,'m 250 1280 l 670 1280 670 1300 250 1300','CCCCCC')
draw(a,b,'m 400 1285 l 570 1285 570 1295 400 1295',extra=r'\t(0,2300,\fscx120)')
draw(a,b,'m 560 1240 l 780 1240 780 1225 820 1248 780 1270 780 1255 560 1255')
txt(a,b,'GRIP  →  ADVANCE  →  RESET',520,1335,'Small')
# Launch diagram: exactly one leading stay-assisted pylon on each opposing front; red temporary tower.
a,b=43.8,46.2
txt(a,b,'TWO LAUNCH FRONTS / SCHEMATIC',520,650)
for x in [190,840]: draw(a,b,f'm {x} 1000 l {x+35} 1000 {x+35} 1270 {x} 1270','CCCCCC')
for x in [350,680]:
 draw(a,b,f'm {x} 1000 l {x+12} 1000 {x+12} 1270 {x} 1270','4141D6')
 draw(a,b,f'm {x+30} 1000 l {x+42} 1000 {x+42} 1270 {x+30} 1270','4141D6')
 for y in range(1000,1250,50):draw(a,b,f'm {x} {y} l {x+42} {y+40} {x+42} {y+48} {x} {y+8}','4141D6')
for x in [380,680]:
 draw(a,b,f'm {x} 800 l {x+12} 800 {x+12} 1000 {x} 1000','DDDDDD')
 for end in [x-110,x+80]:draw(a,b,f'm {x} 825 l {end} 990 {end+3} 992 {x+3} 825','DDDDDD')
draw(a,b,'m 130 990 l 480 990 480 1015 130 1015','BBBBBB')
draw(a,b,'m 590 990 l 940 990 940 1015 590 1015','BBBBBB')
draw(a,b,'m 400 1090 l 475 1090 475 1070 510 1100 475 1130 475 1110 400 1110')
draw(a,b,'m 670 1090 l 595 1090 595 1070 560 1100 595 1130 595 1110 670 1110')
txt(a,b,'NOT TO SCALE · CABLES SHOWN CONCEPTUALLY',520,1360,'Small')
a,b=51.8,54.9
txt(a,b,'CLOSURE DETAIL / SCHEMATIC',520,650)
for x in [200,830]:draw(a,b,f'm {x} 1000 l {x+35} 1000 {x+35} 1270 {x} 1270','CCCCCC')
draw(a,b,'m 130 930 l 500 930 500 1020 130 1020','BBBBBB',extra=r'\move(0,0,35,0,0,2100)')
draw(a,b,'m 570 930 l 940 930 940 1020 570 1020','BBBBBB',extra=r'\move(0,0,-35,0,0,2100)')
txt(a,b,'TWO DECK NOSES · CONCEPTUAL MOVEMENT',520,1350,'Small')
ass=W/'finish.ass' ;ass.write_text(header+'\n'.join(events)+'\n')
# Rough cut includes corrected schematic placeholders; polish applied as a separate encode.
import sys,hashlib
reuse='--reuse-parts' in sys.argv
if reuse:
 for path,digest in json.loads((REPORT/'source_hashes.json').read_text()).items():
  assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
concat=[]
for i,(s,a,b,p,o,title,sub) in enumerate(segments):
 out=W/f'part_{i:02}.mp4';n=round((b-a)*30)
 if reuse and out.exists():
  probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=nb_frames','-of','json',str(out)]))
  assert int(probe['streams'][0]['nb_frames'])==n,(s,n)
  concat.append(f"file '{out}'");print('Reused',s,flush=True);continue
 cmd=['ffmpeg','-v','error','-nostdin','-y','-threads','2']
 if p:cmd+=['-ss',str(o),'-i',str(R/'assets/video'/p)]
 else:cmd+=['-f','lavfi','-i','color=c=0x24313B:s=1080x1920:r=30']
 cmd+=['-an','-vf','fps=30,scale=1080:1920:flags=lanczos,setsar=1,format=yuv420p','-frames:v',str(n),'-c:v','libx264','-threads','3','-preset','veryfast','-crf','20',str(out)]
 subprocess.run(cmd,check=True);concat.append(f"file '{out}'");print('Rendered',s,flush=True)
(W/'parts.txt').write_text('\n'.join(concat)+'\n')
# Save raw assembly for review; source audio from Flow is excluded.
vo=R/'assets/audio/voiceover_v2.mp3';rough=D/'RUMY_WHY_003_V2_ROUGHCUT.mp4'
subprocess.run(['ffmpeg','-v','error','-nostdin','-y','-f','concat','-safe','0','-i',str(W/'parts.txt'),'-i',str(vo),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-t','64.3','-movflags','+faststart',str(rough)],check=True)
# Dynamic loudness normalization measured on owner VO; do not time-stretch or synthesize.
af='loudnorm=I=-16:TP=-1.5:LRA=9:measured_I=-23.48:measured_TP=-2.52:measured_LRA=3.30:measured_thresh=-33.87:offset=0.81:linear=false'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','warning','-nostdin','-y','-threads','2','-i',str(rough),'-vf',f'ass={ass}','-af',af,'-ar','48000','-c:v','libx264','-threads','3','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','192k','-t','64.3','-movflags','+faststart',str(F/'RUMY_WHY_003_MILLAU_FINAL.mp4')],check=True)
print('Exported; QA not yet performed.',flush=True)
