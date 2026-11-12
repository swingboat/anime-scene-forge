"""Original procedural wind/grass ambience, no borrowed soundtrack."""
import project_env
import array,hashlib,json,math,random,sys,wave
from project_ops import ROOT,emit,load,save
rate=48000;seconds=3;frames=rate*seconds
random.seed(11212);samples=array.array('h');left_low=right_low=0.0;left_slow=right_slow=0.0
for i in range(frames):
 t=i/rate;fade=min(1,t/.18,(seconds-t)/.22);gust=.65+.18*math.sin(2*math.pi*.27*t)+.12*math.sin(2*math.pi*.8*t+.4)
 left_raw=random.uniform(-1,1);right_raw=.75*left_raw+.25*random.uniform(-1,1)
 left_low=.94*left_low+.06*left_raw;right_low=.94*right_low+.06*right_raw
 left_slow=.995*left_slow+.005*left_raw;right_slow=.995*right_slow+.005*right_raw
 for low,slow,raw in [(left_low,left_slow,left_raw),(right_low,right_slow,right_raw)]:
  value=(.8*low+.5*slow+.018*raw)*gust*max(0,fade)*.16
  samples.append(max(-32768,min(32767,int(value*32767))))
if sys.byteorder!='little':samples.byteswap()
file=ROOT/'public/audio/hillside-wind.wav'
with wave.open(str(file),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(rate);f.writeframes(samples.tobytes())
data=load();data['background']={'file':'audio/hillside-wind.wav','volume':.8};save(data)
emit(ROOT/'docs/generation/ambience.json',{'source':'original procedural filtered noise','script':'scripts/make_ambience.py','seed':11212,'file':file.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'seconds':seconds,'sampleRate':rate,'channels':2,'type':'wind/grass-like ambience, no dialogue or music','listeningLimitation':'Agent cannot directly audition audio; user listening remains pending.'})
print(file)
