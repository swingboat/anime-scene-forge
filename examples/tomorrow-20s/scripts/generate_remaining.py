"""Serial local generation and QA sheets. Does not assign visual approval."""
import project_env
import argparse, subprocess, json, sys
from project_ops import ROOT, load

p=argparse.ArgumentParser();p.add_argument('shots',nargs='+');p.add_argument('--take',default='v1')
a=p.parse_args()
for shot_id in a.shots:
    shot=next(s for s in load()['shots'] if s['id']==shot_id)
    print(json.dumps({'shot':shot_id,'stage':'generating'},ensure_ascii=False),flush=True)
    command=[str(ROOT/'.venv/bin/python'),'scripts/run_mlx.py',shot_id,
        '--mode','a2v','--image','public/'+shot['art'],'--prompt',f'docs/prompts/{shot_id}.txt',
        '--take',a.take,'--frames','97','--seed',str(11210+int(shot_id[-2:]))]
    anchors=ROOT/f'docs/prompts/{shot_id}-anchors.json'
    if anchors.exists():command += ['--anchors',anchors.relative_to(ROOT).as_posix()]
    subprocess.run(command,cwd=ROOT,check=True)
    subprocess.run([sys.executable,'scripts/project_ops.py','select',shot_id,
        '--source',f'public/candidates/{shot_id}-{a.take}.mp4','--take',a.take,
        '--generation',f'docs/generation/{shot_id}-{a.take}.json'],cwd=ROOT,check=True)
    subprocess.run([str(ROOT/'.venv/bin/python'),'scripts/review_frames.py',shot_id],cwd=ROOT,check=True)
    print(json.dumps({'shot':shot_id,'stage':'ready-for-visual-review'},ensure_ascii=False),flush=True)
