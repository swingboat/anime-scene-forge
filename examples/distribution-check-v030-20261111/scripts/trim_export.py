"""Trim only AAC encoder tail beyond the exact composition duration."""
import project_env
import argparse, datetime, json, subprocess
from project_ops import ROOT, local, load, sha, probe, emit, require

p=argparse.ArgumentParser();p.add_argument('file');a=p.parse_args()
file=local(a.file);data=load();seconds=data['format']['durationFrames']/data['format']['fps']
meta=probe(file);audio=next((s for s in meta['streams'] if s['codec_type']=='audio'),None)
record={'file':a.file,'targetSeconds':seconds,'inputSha256':sha(file),'videoReencoded':False}
if audio and float(audio['duration'])>seconds+.002:
    temp=ROOT/'.cache/tmp'/f'{file.stem}-exact.mp4'
    subprocess.run(['ffmpeg','-y','-v','error','-i',str(file),'-map','0:v:0','-map','0:a:0',
        '-c:v','copy','-af',f'atrim=end={seconds:.9f},asetpts=PTS-STARTPTS',
        '-c:a','aac','-b:a','320k','-ar','48000','-t',f'{seconds:.9f}',
        '-movflags','+faststart',str(temp)],check=True)
    check=probe(temp);require(abs(float(check['format']['duration'])-seconds)<.001,'Exact duration trim failed')
    folder=ROOT/'outputs/intermediate';folder.mkdir(exist_ok=True)
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    original=folder/f'{file.stem}-remotion-{stamp}.mp4';file.replace(original);temp.replace(file)
    record.update(original=original.relative_to(ROOT).as_posix(),trimmedAudioTailSeconds=float(audio['duration'])-seconds,
                  processing='Video stream copy; AAC audio trim to exact composition duration and reencode at320kbps. No speech tempo or placement change.')
else: record['processing']='No duration correction required.'
record['outputSha256']=sha(file);emit(ROOT/f'outputs/checks/{file.stem}-audio-tail.json',record)
print(json.dumps(record,indent=2))
