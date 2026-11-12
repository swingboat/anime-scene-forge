"""Produce numbered QA sheets, including every frame and audio activity.

This only creates inspection artifacts, never edits production artwork/video.
"""
import project_env
import argparse, json, subprocess, wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from project_ops import ROOT, sha

p=argparse.ArgumentParser();p.add_argument('shot');p.add_argument('--face',nargs=4,type=int);p.add_argument('--listener',nargs=4,type=int)
a=p.parse_args();data=json.loads((ROOT/'production.json').read_text())
shot=next(s for s in data['shots'] if s['id']==a.shot)
source=ROOT/'public'/shot['clip'];folder=ROOT/'outputs/checks'/a.shot/sha(source)[:10]/'frames'
folder.mkdir(parents=True,exist_ok=True)
if not all((folder/f'{i+1:03d}.png').is_file() for i in range(shot['frames'])):
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(source),str(folder/'%03d.png')],check=True)
driver=ROOT/'public'/shot['dialogue']['driverFile']
with wave.open(str(driver),'rb') as w:
    audio=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float).reshape(-1,2)/32768
activity=[float(np.sqrt(np.mean(audio[i*2000:(i+1)*2000]**2))) for i in range(96)]
def sheet(name,indices,crop=None):
    width=256;img_h=144 if not crop else 192;height=img_h+30;cols=6
    out=Image.new('RGB',(cols*width,int(np.ceil(len(indices)/cols))*height),(20,23,27));draw=ImageDraw.Draw(out)
    for cell,i in enumerate(indices):
        frame=Image.open(folder/f'{i+1:03d}.png').convert('RGB')
        if crop:
            x,y,w,h=crop;frame=frame.crop((x,y,x+w,y+h))
        frame=frame.resize((width,img_h),Image.Resampling.LANCZOS)
        x=(cell%cols)*width;y=(cell//cols)*height
        out.paste(frame,(x,y));draw.text((x+5,y+img_h+3),f'f{i:02d}  {i/24:.3f}s  RMS {activity[i]:.3f}',fill='white')
        draw.rectangle((x,y+height-3,x+int(width*min(1,activity[i]/.15)),y+height-1),fill=(100,210,180))
    target=folder.parent/(name+'.jpg');out.save(target,quality=93)
    return str(target.relative_to(ROOT))
files=[sheet('overview-every-fourth',list(range(0,96,4))),sheet('all-frames',list(range(96)))]
if a.face:files.append(sheet('face-all-frames',list(range(96)),a.face))
if a.listener:files.append(sheet('listener-all-frames',list(range(96)),a.listener))
record={'clipSha256':sha(source),'driverSha256':sha(driver),'files':files,'frameRms':activity,
        'scope':'Actual frames and signal activity for human/agent inspection; no automatic visual approval.'}
(folder.parent/'sheet-index.json').write_text(json.dumps(record,indent=2))
print(json.dumps(files,indent=2))
