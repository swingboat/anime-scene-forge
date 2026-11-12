#!/usr/bin/env python3
"""Maintainer-only technical fixture. No model downloads, API calls or GPU inference.

Requires a fresh half-second project explicitly marked as a smoke fixture.
The synthetic review record exercises export gates; it is not artistic approval.
"""
import argparse,array,hashlib,json,math,os,subprocess,sys,wave
from pathlib import Path

def main():
    p=argparse.ArgumentParser();p.add_argument('--project',type=Path,required=True);p.add_argument('--render',action='store_true');a=p.parse_args()
    root=a.project.resolve();marker=root/'.skill-smoke-fixture'
    if not marker.is_file() or marker.read_text().strip()!='anime-scene-forge:test-fixture:v1':raise SystemExit('Refusing to mutate a project without the dedicated smoke-fixture marker')
    data=json.loads((root/'production.json').read_text())
    if data['format']['durationFrames']!=12 or data['format']['fps']!=24 or len(data['shots'])!=1:raise SystemExit('Use a fresh 0.5s /24fps fixture project')
    env={**os.environ,'TMPDIR':str(root/'.cache/tmp'),'TMP':str(root/'.cache/tmp'),'TEMP':str(root/'.cache/tmp'),'PYTHONDONTWRITEBYTECODE':'1','npm_config_cache':str(root/'.cache/npm')}
    report=[]
    def run(name,args,ok=True):
        r=subprocess.run(args,cwd=root,env=env,capture_output=True,text=True)
        (root/f'outputs/checks/{name}.log').write_text(r.stdout+r.stderr)
        if (r.returncode==0)!=ok:raise RuntimeError(f'{name}: unexpected status {r.returncode}\n{r.stdout}\n{r.stderr}')
        report.append({'case':name,'expected':'success' if ok else 'rejection','passed':True});return r
    def save(): (root/'production.json').write_text(json.dumps(data,indent=2)+'\n')
    py=sys.executable;ops=[py,'scripts/project_ops.py']
    run('initial-source',[*ops,'validate','--stage','scaffold'])
    run('pending-export-rejected',[*ops,'validate'],ok=False)
    if (root/'scripts/setup_mlx.py').is_file():
        run('video-setup-plan',[py,'scripts/setup_mlx.py','video','--plan'])
        run('voice-setup-plan',[py,'scripts/setup_mlx.py','voice','--plan'])
    run('source-fixture',['ffmpeg','-y','-v','error','-f','lavfi','-i','testsrc2=size=1280x720:rate=24','-frames:v','17','-an','-c:v','libx264','-pix_fmt','yuv420p','public/candidates/smoke-source.mp4'])
    run('art-fixture',['ffmpeg','-y','-v','error','-i','public/candidates/smoke-source.mp4','-frames:v','1','-update','1','public/art/smoke.png'])
    samples=array.array('h')
    for i in range(9600):
        t=i/48000;envelope=math.sin(math.pi*i/9600)**2*(.5+.5*math.sin(2*math.pi*7*t))
        v=int(6000*envelope*math.sin(2*math.pi*440*t));samples.extend([v,v])
    if sys.byteorder!='little':samples.byteswap()
    voice=root/'public/audio/voices/smoke.wav'
    with wave.open(str(voice),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(48000);f.writeframes(samples.tobytes())
    shot=data['shots'][0];shot['caption']={'text':'Technical fixture','startFrame':0,'endFrame':12};shot['art']='art/smoke.png'
    shot['dialogue']={'text':'Synthetic test pulse, not speech','file':None,'sync':'voiceover','fromFrame':3};save()
    run('voice-overflow-rejected',[*ops,'pad-voice','scene-01','--voice','public/audio/voices/smoke.wav','--from-frame','12','--source-frames','17','--take','invalid'],ok=False)
    run('pad-voice',[*ops,'pad-voice','scene-01','--voice','public/audio/voices/smoke.wav','--from-frame','3','--source-frames','17','--take','v1'])
    data=json.loads((root/'production.json').read_text());shot=data['shots'][0]
    run('select-native-nonzero-start',[*ops,'select','scene-01','--source','public/candidates/smoke-source.mp4','--start','2','--take','v1'])
    data=json.loads((root/'production.json').read_text());shot=data['shots'][0]
    run('unreviewed-export-rejected',[*ops,'validate'],ok=False)
    baseline=voice.read_bytes();changed=bytearray(baseline);changed[-1]^=1;voice.write_bytes(changed)
    run('changed-voice-rejected',[*ops,'validate','--stage','draft'],ok=False);voice.write_bytes(baseline)
    shot['dialogue']['fromFrame']=4;save();run('changed-timing-rejected',[*ops,'validate','--stage','draft'],ok=False)
    shot['dialogue']['fromFrame']=3;shot['dialogue']['sync']='on-screen';save()
    run('missing-a2v-rejected',[*ops,'validate','--stage','draft'],ok=False);shot['dialogue']['sync']='voiceover'
    shot['art']='../outside.png';save();run('asset-escape-rejected',[*ops,'validate','--stage','scaffold'],ok=False);shot['art']='art/smoke.png'
    data['format']['fps']=30;save();run('fps-mismatch-rejected',[*ops,'validate','--stage','draft'],ok=False);data['format']['fps']=24;save()
    prompt=root/'docs/prompts/smoke.txt';prompt.write_text('Technical dry-run fixture only; no character generation requested.\n')
    run('pad-a2v-nonzero-start',[*ops,'pad-voice','scene-01','--voice','public/audio/voices/smoke.wav','--from-frame','3','--source-frames','17','--source-start','2','--take','a2v'])
    data=json.loads((root/'production.json').read_text());shot=data['shots'][0]
    source=root/'public/candidates/smoke-source.mp4'
    generation=root/'docs/generation/smoke-synthetic-a2v.json'
    gen={'mode':'a2v','backend':'synthetic-technical-fixture-no-inference','audioSha256':shot['dialogue']['driverSha256'],'output':'public/candidates/smoke-source.mp4','outputSha256':hashlib.sha256(source.read_bytes()).hexdigest()}
    if data.get('style'):gen.update(style=data['style'],styleSha256=hashlib.sha256((root/'docs/style.json').read_bytes()).hexdigest())
    generation.write_text(json.dumps(gen,indent=2))
    shot['dialogue']['sync']='on-screen';shot['generation']='docs/generation/smoke-synthetic-a2v.json';save()
    run('matching-a2v-provenance',[*ops,'validate','--stage','draft'])
    if data.get('style'):
        profile=root/'docs/style.json';baseline_profile=profile.read_bytes();profile.write_bytes(baseline_profile+b'\n')
        run('changed-generation-style-rejected',[*ops,'validate','--stage','draft'],ok=False);profile.write_bytes(baseline_profile)
    run('a2v-selection-shift-rejected',[*ops,'select','scene-01','--source','public/candidates/smoke-source.mp4','--start','1','--take','bad-shift','--generation','docs/generation/smoke-synthetic-a2v.json'],ok=False)
    other=root/'public/candidates/smoke-other.mp4';other.write_bytes(source.read_bytes())
    gen['output']='public/candidates/smoke-other.mp4';generation.write_text(json.dumps(gen))
    run('unrelated-a2v-source-rejected',[*ops,'validate','--stage','draft'],ok=False)
    gen['output']='public/candidates/smoke-source.mp4';generation.write_text(json.dumps(gen,indent=2))
    selection=root/shot['selection'];sel=json.loads(selection.read_text());sel['startFrame']=1;selection.write_text(json.dumps(sel))
    run('a2v-timeline-shift-rejected',[*ops,'validate','--stage','draft'],ok=False)
    sel['startFrame']=2;sel['outputSha256']='0'*64;selection.write_text(json.dumps(sel))
    run('replaced-selection-rejected',[*ops,'validate','--stage','draft'],ok=False)
    sel['outputSha256']=hashlib.sha256((root/'public'/shot['clip']).read_bytes()).hexdigest();selection.write_text(json.dumps(sel,indent=2))
    if (root/'scripts/run_mlx.py').is_file():
        dry=run('mlx-dry-run',[py,'scripts/run_mlx.py','scene-01','--mode','a2v','--image','public/art/smoke.png','--prompt','docs/prompts/smoke.txt','--take','dry','--frames','17','--dry-run'])
        assert json.loads(dry.stdout)['executed'] is False and not (root/'docs/generation/scene-01-dry.json').exists()
    run('frame-sheet',[*ops,'sheet','scene-01']);run('cropped-frame-sheet',[*ops,'sheet','scene-01','--crop','20','20','400','300','--label','region'])
    clip=root/'public'/shot['clip'];clip_sha=hashlib.sha256(clip.read_bytes()).hexdigest()
    review=root/'docs/reviews/smoke-fixture.json'
    rv={'clipSha256':'0'*64,'visualReviewed':True,'normalSpeedReviewed':True,'reviewer':'automated-test-fixture','observations':'Synthetic approval input used only to exercise technical gates; not a production or user review.','limitations':'No anime character, lip sync or artistic quality is certified.'}
    if data.get('style'):rv['styleSha256']=hashlib.sha256((root/'docs/style.json').read_bytes()).hexdigest()
    review.write_text(json.dumps(rv,indent=2));shot.update(status='approved',review='docs/reviews/smoke-fixture.json');save()
    run('stale-review-rejected',[*ops,'validate'],ok=False)
    rv['clipSha256']=clip_sha
    if data.get('style'):
        original_style=rv['styleSha256'];rv['styleSha256']='0'*64;review.write_text(json.dumps(rv))
        run('stale-style-review-rejected',[*ops,'validate'],ok=False);rv['styleSha256']=original_style
    review.write_text(json.dumps(rv,indent=2));run('valid-fixture',[*ops,'validate'])
    if a.render:
        run('typescript',['node','scripts/run.mjs','source-check'])
        run('render-draft',['node','scripts/run.mjs','render-draft']);run('render-final',['node','scripts/run.mjs','render'])
        run('final-check',['node','scripts/run.mjs','check'])
        exported=json.loads((root/'outputs/checks/export.json').read_text())
        if abs(exported['containerDuration']-.5)>=.002:raise RuntimeError('Container exceeds the exact fixture duration')
        run('exact-container-duration',['ffprobe','-v','error','-show_entries','format=duration','-of','json','outputs/final.mp4'])
        helper=root/'scripts/trim_export.py';original_helper=helper.read_bytes();helper.write_bytes(original_helper+b'\n# changed after export\n')
        run('stale-render-helper-rejected',[*ops,'verify-export'],ok=False);helper.write_bytes(original_helper)
        before=data['title'];data['title']='Changed after export';save();run('stale-export-rejected',[*ops,'verify-export'],ok=False);data['title']=before;save()
        run('package-fixture',['node','scripts/run.mjs','package'])
    summary={'status':'passed','scope':'Technical fixture and command guards only; no generated performance, host-agent integration or GPU model inference certified.','rendered':a.render,'cases':report}
    (root/'outputs/checks/skill-smoke-report.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
