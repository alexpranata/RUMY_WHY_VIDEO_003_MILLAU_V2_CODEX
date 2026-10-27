#!/usr/bin/env python3
"""Produce a simple proof-of-assembly; not a polished video. No text/motion-graphics/purchased media.
  Uses selected v2 or original per scene; never mutates source assets.
  Uses ffmpeg + ffprobe in PATH. For long VO above sum of clip lengths, refuses to pad unrealistically.
"""
import pathlib, subprocess, json, shutil, sys
R=pathlib.Path(__file__).resolve().parents[1]
V=R/'assets'/'video'; A=R/'assets'/'audio'; OUT=R/'output'/'draft'/'RUMY_WHY_003_V2_ROUGHCUT.mp4'

def probe_dur(p):
 return float(json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-of','json',str(p)]))['format']['duration'])

def main():
 for tool in ('ffmpeg','ffprobe'):
  if not shutil.which(tool):print('Missing dependency:',tool);return 3
 clips=[]
 for i in range(1,13):
  stem=f'S{i:02d}';v2=V/(stem+'_v2.mp4');v1=V/(stem+'.mp4')
  clip=v2 if v2.is_file() else v1
  if not clip.is_file():print('Missing scene',stem,'Stop without generating anything.');return 2
  clips.append(clip)
 voices=[A/n for n in ['voiceover_v2.wav','voiceover_v2.mp3','voiceover.wav','voiceover.mp3','voiceover_original.wav','voiceover_original.mp3'] if (A/n).is_file()]
 if not voices:print('Missing voiceover. No silent fake final.');return 2
 voice=voices[0];vo_dur=probe_dur(voice);durations=[probe_dur(c) for c in clips]
 if any(d<1.5 for d in durations): print('A clip is unexpectedly short; abort.'); return 2
 # Approximately equal durations for baseline only; Codex must re-time from narration before FINAL render.
 available=sum(durations)
 if vo_dur>available-0.15:
  print(f'Voice {vo_dur:.2f}s longer than available raw {available:.2f}s: no forced loops or fabricated frames.')
  return 2
 target=[min(d-0.04,vo_dur/len(clips)) for d in durations]
 # Distribute remaining duration within available real footage capacity.
 remainder=vo_dur-sum(target)
 if remainder>0:
  for i in range(len(target)):
   extra=min(max(durations[i]-0.04-target[i],0),remainder)
   target[i]+=extra;remainder-=extra
   if remainder<=.001:break
 if remainder>0.05:
  print('Could not allocate target duration without freezing; abort.');return 2
 OUT.parent.mkdir(parents=True,exist_ok=True)
 # Build single ffmpeg filtergraph with scaled/cropped source, loud original clips discarded, audio supplied separately.
 args=['ffmpeg','-hide_banner','-loglevel','warning','-y']
 for p in clips:args+=['-i',str(p)]
 args+=['-i',str(voice)]
 filt=[]
 for i,t in enumerate(target):
  filt.append(f'[{i}:v]trim=duration={t:.4f},setpts=PTS-STARTPTS,fps=30,scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1,format=yuv420p[v{i}]')
 filt.append(''.join(f'[v{i}]' for i in range(12))+'concat=n=12:v=1:a=0[v]')
 args+=['-filter_complex',';'.join(filt),'-map','[v]','-map','12:a:0','-c:v','libx264','-preset','veryfast','-crf','21','-r','30',
        '-c:a','aac','-b:a','192k','-movflags','+faststart','-shortest',str(OUT)]
 print('Rendering roughcut from 12 source clips, VO',f'{vo_dur:.2f}s','target segments',target)
 res=subprocess.run(args)
 if res.returncode==0:print('Roughcut saved:',OUT,'-- NO CAPTIONS/GRAPHICS: Codex must polish and QA.')
 return res.returncode

if __name__=='__main__':sys.exit(main())
