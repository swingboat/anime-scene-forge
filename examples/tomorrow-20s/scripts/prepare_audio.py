"""Adopt unchanged-speed speech and write an original quiet piano/room bed."""
import project_env
import json, subprocess, wave
from pathlib import Path
import numpy as np
from project_ops import ROOT, sha, emit

RATE = 48000

def write(path, x):
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(RATE)
        w.writeframes((np.clip(x, -.99, .99)*32767).astype('<i2').tobytes())

def main():
    data = json.loads((ROOT/'production.json').read_text())
    offsets = [6, 9, 12, 8, 10]
    metrics = []
    for shot, offset in zip(data['shots'], offsets):
        source = ROOT/f'public/audio/voices/{shot["id"]}-v1-raw.wav'
        target = ROOT/f'public/audio/voices/{shot["id"]}-v1.wav'
        # Constant gain and sample-rate conversion only: no time stretch or cuts.
        if not target.exists():
            subprocess.run(['ffmpeg', '-v', 'error', '-n', '-i', str(source),
                            '-af', 'volume=1.35', '-ar', '48000', '-ac', '2',
                            '-c:a', 'pcm_s16le', str(target)], check=True)
        with wave.open(str(target), 'rb') as w:
            seconds = w.getnframes()/w.getframerate()
        shot['dialogue'].update(file=target.relative_to(ROOT/'public').as_posix(),fromFrame=offset)
        shot['caption'].update(startFrame=offset,endFrame=min(96,offset+int(np.ceil(seconds*24))+3))
        metrics.append({'shot':shot['id'],'seconds':seconds,'fromFrame':offset,
                        'speed':1,'gain':1.35,'sourceSha256':sha(source),'sha256':sha(target)})
    n = RATE*20
    piano = np.zeros((n, 2), np.float64)
    rng = np.random.default_rng(112120)
    score = []
    def note(start, midi, velocity=.3, duration=3.0):
        count = min(int(duration*RATE), n-int(start*RATE))
        if count <= 0: return
        t = np.arange(count)/RATE
        freq = 440*2**((midi-69)/12)
        sound = np.zeros(count)
        # Decaying, slightly inharmonic struck strings, with a quiet hammer transient.
        for partial in range(1, 13):
            decay = (2.1 if midi < 60 else 1.55)/(partial**.38)
            f = freq*partial*np.sqrt(1+.00016*partial**2)
            sound += (1/partial**1.9)*np.exp(-t/decay)*np.sin(2*np.pi*f*t)
            sound += .13/partial**2*np.exp(-t/(decay*.85))*np.sin(2*np.pi*f*1.0012*t)
        sound *= (1-np.exp(-t/.004))*np.minimum(1,(duration-t)/.12)
        sound += rng.standard_normal(count)*.012*np.exp(-t/.012)
        sound *= velocity*.105
        pan = np.clip((midi-60)/44,-.35,.35)
        stereo = np.column_stack((sound*np.sqrt((1-pan)/2),sound*np.sqrt((1+pan)/2)))
        begin = int(start*RATE);piano[begin:begin+count] += stereo
        score.append({'seconds':start,'midi':midi,'velocity':velocity})
    # Original five-bar phrase: Cmaj7 / Am9 / Fmaj7 / Gsus / C6.
    chords = [(48,[64,67,71,76]),(45,[60,64,69,71]),(41,[60,64,69,72]),
              (43,[62,67,69,74]),(48,[64,67,69,72])]
    for bar,(bass,upper) in enumerate(chords):
        base = bar*4+.12
        note(base,bass,.48,4.0)
        for step,index in enumerate([0,1,2,1,3]):
            note(base+.34+step*.66,upper[index],.28 if step%2 else .34,2.9)
    # Short diffuse room reflections; no looping audio.
    dry = piano.copy()
    for delay,gain in [(.073,.15),(.119,.11),(.211,.075),(.337,.04)]:
        d = int(delay*RATE);piano[d:] += dry[:-d,::-1]*gain
    tt = np.arange(n)/RATE
    noise = rng.standard_normal(n)
    room = np.convolve(noise,np.ones(65)/65,mode='same')*.02
    room += .00009*np.sin(2*np.pi*100*tt)
    ambient = np.column_stack((room,np.roll(room,157)))
    # Near inaudible outside bird phrases, well behind the dialogue.
    for start in [3.4,7.45,11.5,18.55]:
        count = int(.24*RATE);t=np.arange(count)/RATE
        bird = .00065*np.sin(2*np.pi*(2450*t+1250*t*t))*np.sin(np.pi*t/.24)**2
        b=int(start*RATE);ambient[b:b+count] += bird[:,None]*np.array([.8,.5])
    fade = np.minimum(1,tt/.7)*np.minimum(1,(20-tt)/.85)
    piano *= fade[:,None];ambient *= fade[:,None]
    write(ROOT/'public/audio/piano-original.wav',piano)
    write(ROOT/'public/audio/classroom-ambience.wav',ambient)
    bed = piano+ambient
    write(ROOT/'public/audio/bed.wav',bed)
    data['fontFile'] = 'fonts/NotoSansSC.ttf'
    data['background'] = {'file':'audio/bed.wav','volume':.85}
    (ROOT/'production.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    emit(ROOT/'docs/generation/audio-adoption.json',{'voices':metrics,'processing':'No speed changes, no voice cuts; gain and 24kHz to 48kHz stereo conversion only.',
         'music':'Original additive struck-string piano synthesis, five bars, no external recording.','score':score,
         'pianoRmsDbfs':float(20*np.log10(np.sqrt(np.mean(piano**2)))),'roomRmsDbfs':float(20*np.log10(np.sqrt(np.mean(ambient**2))))})
    print(json.dumps(metrics,indent=2))

if __name__ == '__main__': main()
