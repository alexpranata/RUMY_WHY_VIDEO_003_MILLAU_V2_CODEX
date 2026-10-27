from pocketsphinx import Decoder
from pathlib import Path
import wave,re,json
r=Path(__file__).resolve().parents[2]
text=(r/'docs/VOICEOVER_V2_RECOMMENDED.txt').read_text().lower(); text=re.sub(r"[^a-z\s']",' ',text);text=' '.join(text.split())
d=Decoder(samprate=16000,logfn='/dev/null')
for word,phones in {'formwork':'F AO R M W ER K','tarn':'T AA R N','tensioned':'T EH N SH AH N D'}.items(): d.add_word(word,phones,False)
d.set_align_text(text)
w=wave.open(str(r/'output/work/vo.wav'),'rb'); data=w.readframes(w.getnframes())
d.start_utt();d.process_raw(data,False,True);d.end_utt()
words=[{'word':s.word,'start':s.start_frame/100,'end':(s.end_frame+1)/100} for s in d.seg()]
(r/'output/reports/vo_word_alignment.json').write_text(json.dumps(words,indent=2))
for i,s in enumerate(words):
 if s['word'] not in ['<sil>','[SPEECH]']:
  print(f"{i:3} {s['start']:5.2f}-{s['end']:5.2f} {s['word']}")
