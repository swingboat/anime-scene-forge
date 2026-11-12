"""Compare exported AAC timing with the original, unaltered dialogue mix."""
import project_env
import subprocess, wave, json
import numpy as np
from scipy.signal import correlate, correlation_lags
from project_ops import ROOT, load, emit, sha

def read(path):
    with wave.open(str(path),'rb') as w:
        assert w.getframerate()==48000 and w.getnchannels()==2
        return np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(np.float64).reshape(-1,2)/32768

data=load();rate=48000;n=data['format']['durationFrames']*rate//data['format']['fps']
expected=np.zeros((n,2));events=[];frame=0
for shot in data['shots']:
    d=shot.get('dialogue')
    if d:
        voice=read(ROOT/'public'/d['file']);start=(frame+d['fromFrame'])*rate//24
        expected[start:start+len(voice)] += voice
        events.append({'shot':shot['id'],'seconds':start/rate,'endSeconds':(start+len(voice))/rate})
    frame+=shot['frames']
if data.get('background'):
    b=data['background'];bed=read(ROOT/'public'/b['file']);expected[:min(n,len(bed))]+=bed[:n]*b['volume']
decoded=ROOT/'.cache/tmp/final-audio.f32'
subprocess.run(['ffmpeg','-y','-v','error','-i',str(ROOT/'outputs/final.mp4'),'-vn','-ar','48000','-ac','2','-f','f32le',str(decoded)],check=True)
actual=np.fromfile(decoded,dtype='<f4').astype(np.float64).reshape(-1,2)[:n]
length=min(len(actual),n);ref=expected[:length].mean(axis=1);out=actual[:length].mean(axis=1)
cross=correlate(out,ref,mode='full',method='fft');lags=correlation_lags(len(out),len(ref),mode='full')
within=np.flatnonzero(abs(lags)<=4800);lag=int(lags[within[np.argmax(cross[within])]])
if lag>0: out=out[lag:];ref=ref[:-lag]
elif lag<0: out=out[:lag];ref=ref[-lag:]
correlation=float(np.corrcoef(ref,out)[0,1])
result={'status':'pass' if abs(lag)<=240 and correlation>.98 else 'investigate',
        'scope':'Encoded audio placement and sample-envelope comparison. Does not verify voice quality or phoneme lip sync.',
        'fileSha256':sha(ROOT/'outputs/final.mp4'),'sampleRate':rate,'lagSamples':lag,'lagMs':lag/rate*1000,
        'correlation':correlation,'peak':float(abs(actual).max()),'rmsDbfs':float(20*np.log10(np.sqrt(np.mean(actual**2)))),
        'dialogueWindows':events}
emit(ROOT/'outputs/checks/audio-mix.json',result)
print(json.dumps(result,ensure_ascii=False,indent=2))
assert result['status']=='pass', 'Investigate exported audio timing'
