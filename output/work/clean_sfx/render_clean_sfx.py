"""Owner revision: remove object overlays, retain word highlights, add optional source-clip texture SFX."""
from pathlib import Path
import subprocess,json,hashlib,math,struct,shutil
R=Path(__file__).resolve().parents[3];W=R/'output/work/clean_sfx';F=R/'output/final';P=R/'output/reports'
for p,h in json.loads((P/'source_hashes.json').read_text()).items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h,p
# Keep only the existing word captions, including approved word/number highlighting.
text=(R/'output/work/kinetic/word_highlights.ass').read_text();header=text.split('[Events]')[0]
header='\n'.join(x for x in header.splitlines() if not x.startswith('Style: Graphic,'))+'\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
caps=[x for x in text.splitlines() if x.startswith('Dialogue: 5,')];assert len(caps)==168 and all(r'\p1' not in x for x in caps)
ass=W/'word_only.ass';ass.write_text(header+'\n'.join(caps)+'\n')
rough=R/'output/draft/RUMY_WHY_003_V2_ROUGHCUT.mp4';clean=F/'RUMY_WHY_003_MILLAU_WORDS.mp4'
af='loudnorm=I=-16:TP=-1.5:LRA=9:measured_I=-23.48:measured_TP=-2.52:measured_LRA=3.30:measured_thresh=-33.87:offset=0.81:linear=false'
subprocess.run(['ffmpeg','-v','warning','-nostdin','-y','-i',str(rough),'-vf',f'ass={ass}','-af',af,'-ar','48000','-c:v','libx264','-threads','3','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','192k','-t','64.3','-movflags','+faststart',str(clean)],check=True)
# Only owner-provided source audio; no external downloads, billed APIs or new narration.
# Short processed texture cues, with the speech-heavy middle band removed; not a claim of authentic location recording.
cues=[('formwork','S05_v2.mp4',1.1,18.7,1.1),('steel_assembly','S07_v2.mp4',2.25,35.3,2.1),('translator','S08_v2.mp4',1.0,39.6,3.0),('raising','S11_v2.mp4',.6,55.2,2.5)]
manifest=[];stems=[]
for idx,(name,clip,offset,start,duration) in enumerate(cues):
 filtered=W/f'{name}_filtered.wav'
 # Preserve mechanical low rumble and high texture, strongly suppress possible incidental vocal intelligibility.
 filters=f'highpass=f=90,lowpass=f=6500,bandreject=f=1500:width_type=o:width=3,afade=t=in:st=0:d=0.10,afade=t=out:st={duration-.18}:d=0.18'
 subprocess.run(['ffmpeg','-v','error','-nostdin','-y','-ss',str(offset),'-i',str(R/'assets/video'/clip),'-t',str(duration),'-vn','-ac','1','-ar','48000','-af',filters,str(filtered)],check=True)
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(filtered),'-f','s16le','-'])
 values=struct.unpack('<'+'h'*(len(raw)//2),raw);rms=math.sqrt(sum(v*v for v in values)/len(values));peak=max(abs(v) for v in values)
 db=20*math.log10(max(rms,1e-9)/32768);pk=20*math.log10(max(peak,1e-9)/32768)
 # At least ~16 LU below narration on average, with peaks capped near -19 dBFS.
 gain=min(-32-db,-19-pk);stem=W/f'{name}.wav'
 subprocess.run(['ffmpeg','-v','error','-nostdin','-y','-i',str(filtered),'-af',f'volume={gain:.3f}dB',str(stem)],check=True);stems.append(stem)
 manifest.append({'name':name,'source':'assets/video/'+clip,'source_in_s':offset,'timeline_in_s':start,'duration_s':duration,'processing':filters,'gain_db':round(gain,3),'expected_rms_dbfs':round(db+gain,2),'expected_peak_dbfs':round(pk+gain,2),'provenance':'owner-provided Flow clip, reused in matching scene','subjective_listening':'pending; processed texture candidate, not certified field recording'})
(P/'sfx_selection.json').write_text(json.dumps(manifest,indent=2))
args=['ffmpeg','-v','warning','-nostdin','-y','-i',str(clean)]
for stem in stems:args+=['-i',str(stem)]
filters=[]
for i,c in enumerate(manifest,1):filters.append(f'[{i}:a]adelay={round(c["timeline_in_s"]*1000)}:all=1[s{i}]')
# SFX are quiet and only in four short windows; VO remains the lead. No audio time stretching.
filters.append('[0:a]'+''.join(f'[s{i}]' for i in range(1,5))+'amix=inputs=5:duration=first:normalize=0,alimiter=limit=0.8414:attack=5:release=60:level=false:latency=true[mix]')
final=F/'RUMY_WHY_003_MILLAU_WORDS_SFX.mp4'
args+=['-filter_complex',';'.join(filters),'-map','0:v','-map','[mix]','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t','64.3','-movflags','+faststart',str(final)]
subprocess.run(args,check=True);shutil.copy2(final,F/'RUMY_WHY_003_MILLAU_FINAL.mp4')
print('Word-only version and optional source-texture SFX version exported; subjective listening remains pending.',flush=True)
