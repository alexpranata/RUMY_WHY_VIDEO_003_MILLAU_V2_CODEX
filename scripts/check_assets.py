#!/usr/bin/env python3
"""Read-only audit of existing 12 Flow clips, v2 takes, and voiceover (stdlib + ffprobe)."""
import json, subprocess, shutil, sys, pathlib, datetime
R = pathlib.Path(__file__).resolve().parents[1]
VIDEO = R/'assets'/'video'; AUDIO = R/'assets'/'audio'

def probe(p):
 if shutil.which('ffprobe') is None:
  return {'exists':True,'probe_warning':'ffprobe not available; cannot inspect media'}
 try:
  raw=subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)],stderr=subprocess.STDOUT,timeout=20)
  data=json.loads(raw)
  streams=data.get('streams',[])
  v=next((s for s in streams if s.get('codec_type')=='video'),{})
  a=next((s for s in streams if s.get('codec_type')=='audio'),{})
  return {'exists':True,'duration_s':round(float(data.get('format',{}).get('duration') or v.get('duration') or a.get('duration') or 0),2),
          'width':v.get('width'),'height':v.get('height'),'video_codec':v.get('codec_name'),
          'fps':v.get('avg_frame_rate'),'audio_codec':a.get('codec_name'),'bytes':p.stat().st_size}
 except Exception as e:return {'exists':True,'probe_error':str(e)}

files=[];miss=[]
for i in range(1,13):
 s=f'S{i:02d}'
 original=VIDEO/(s+'.mp4'); newer=VIDEO/(s+'_v2.mp4')
 if not original.is_file() and not newer.is_file():miss.append(s)
 files.append({'scene':s,'original':probe(original) if original.exists() else None,
               'replacement':probe(newer) if newer.exists() else None,
               'suggested_use':str((newer if newer.is_file() else original).relative_to(R)) if (newer.is_file() or original.is_file()) else None})

voice_order=['voiceover_v2.wav','voiceover_v2.mp3','voiceover.wav','voiceover.mp3','voiceover_original.wav','voiceover_original.mp3']
voices=[{'name':name,**probe(AUDIO/name)} for name in voice_order if (AUDIO/name).is_file()]
selected_voice=next((x['name'] for x in voices),None)
report={'generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'project_root':str(R),
        'scenes':files,'missing_scenes':miss,'found_scene_count':12-len(miss),
        'voice_candidates':voices,'selected_voice':selected_voice,'selected_script':('V2' if selected_voice and '_v2' in selected_voice else 'V1' if selected_voice else None),
        'notes':['Source files are immutable; this script never writes into assets.',
                 'Having the correct file name is not proof of quality or historical accuracy.',
                 'A V2 audio candidate may be preferred only if it matches the V2 spoken text.']}
out=R/'output'/'reports'/'asset_audit.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print('Flow scenes found:',12-len(miss),'/12; missing:',','.join(miss) if miss else 'none')
print('Voiceover:', selected_voice or 'MISSING','; script:',report['selected_script'])
for entry in files:
 used=entry['suggested_use']; v=(entry['replacement'] if entry['replacement'] else entry['original']) or {}
 print(f"{entry['scene']}: {used or 'MISSING'} -- {v.get('duration_s','?')}s {v.get('width','?')}x{v.get('height','?')}")
print('Wrote:',out)
if miss or not selected_voice:sys.exit(2)
