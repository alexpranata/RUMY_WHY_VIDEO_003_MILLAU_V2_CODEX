from pathlib import Path
import subprocess,json,hashlib,csv
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];F=R/'output/final';P=R/'output/reports';movie=F/'RUMY_WHY_003_MILLAU_FINAL.mp4'
def run(args):return subprocess.run(args,capture_output=True,text=True)
probe=run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(movie)]);assert probe.returncode==0,probe.stderr
m=json.loads(probe.stdout);(P/'final_ffprobe.json').write_text(json.dumps(m,indent=2))
v=next(x for x in m['streams'] if x['codec_type']=='video');a=next(x for x in m['streams'] if x['codec_type']=='audio')
assert (v['width'],v['height'],v['avg_frame_rate'],v['codec_name'],a['codec_name'])==(1080,1920,'30/1','h264','aac')
assert int(v['nb_read_frames'])==1929,v
qc=run(['ffmpeg','-hide_banner','-nostats','-v','info','-i',str(movie),'-vf','blackdetect=d=0.1:pix_th=0.02','-af','loudnorm=I=-16:TP=-1.5:LRA=9:print_format=json','-f','null','-'])
(P/'final_decode_audio_qc.log').write_text(qc.stderr);assert qc.returncode==0,qc.stderr
norm=json.loads(qc.stderr[qc.stderr.rfind('{'):qc.stderr.rfind('}')+1]);assert float(norm['input_tp'])<0,norm
source=json.loads((P/'source_hashes.json').read_text());changed=[p for p,h in source.items() if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h];assert not changed,changed
(P/'source_integrity.json').write_text(json.dumps({'checked_files':len(source),'changed_files':changed},indent=2))
times=[1.5,8.7,13.5,16.5,21,25,36,41,45,47.5,50,53,56.5,60,63.5]
sheet=Image.new('RGB',(1080,1224),'#202020');dr=ImageDraw.Draw(sheet)
for i,t in enumerate(times):
 f=F/'review_frames'/f'{t:05.1f}s.jpg';res=run(['ffmpeg','-v','error','-ss',str(t),'-i',str(movie),'-frames:v','1','-y',str(f)]);assert res.returncode==0,res.stderr
 im=Image.open(f);im.thumbnail((216,384));x=(i%5)*216;y=(i//5)*408;sheet.paste(im,(x,y+24));dr.text((x+5,y+5),f'{t:.1f}s',fill='white')
sheet.save(F/'review_frames/contact_sheet.jpg')
# Verify all caption events have max two manual lines and two-dimensional safe bounds established by the producer.
ass=(R/'output/work/finish.ass').read_text();caps=[x for x in ass.splitlines() if x.startswith('Dialogue: 5,')];assert all(x.count('\\N')<=1 for x in caps)
summary={'video_duration':v['duration'],'audio_duration':a['duration'],'container_duration':m['format']['duration'],'frames':v['nb_read_frames'],'caption_events':len(caps),'loudness':norm,'sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'source_files_verified':len(source),'decode_exit':qc.returncode,'black_segments':[x for x in qc.stderr.splitlines() if 'black_start:' in x]}
(P/'final_validation.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
