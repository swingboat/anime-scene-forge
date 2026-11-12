"""Archive compact, authored QA evidence for the portable project package.

Copies existing evidence only; never creates or changes an approval decision.
"""
import project_env
import json, shutil
from pathlib import Path
from project_ops import ROOT, load, sha, emit

manifest=[]
for shot in load()['shots']:
    if not shot.get('review'): continue
    review_file=ROOT/shot['review'];review=json.loads(review_file.read_text())
    assert review['clipSha256']==sha(ROOT/'public'/shot['clip'])
    folder=ROOT/'outputs/checks'/shot['id']/review['clipSha256'][:10]
    target=ROOT/'docs/reviews/evidence'/shot['id'];target.mkdir(parents=True,exist_ok=True)
    for file in [*folder.glob('*.jpg'),folder/'sheet-index.json']:
        if file.is_file():
            dest=target/file.name;shutil.copy2(file,dest)
            manifest.append({'source':file.relative_to(ROOT).as_posix(),
                             'archive':dest.relative_to(ROOT).as_posix(),'sha256':sha(dest)})
    original=review.get('originalArtifacts',review.get('artifacts',[]))
    review['originalArtifacts']=original
    review['artifacts']=[m['archive'] for m in manifest if m['archive'].startswith(target.relative_to(ROOT).as_posix()+'/')]
    emit(review_file,review)
target=ROOT/'docs/reviews/technical';target.mkdir(parents=True,exist_ok=True)
for file in (ROOT/'outputs/checks').glob('*.json'):
    if file.name=='package.json':continue
    dest=target/file.name;shutil.copy2(file,dest)
    manifest.append({'source':file.relative_to(ROOT).as_posix(),'archive':dest.relative_to(ROOT).as_posix(),'sha256':sha(dest)})
pilot=ROOT/'outputs/pilot-remotion-v2.mp4'
if pilot.exists():
    dest=ROOT/'docs/reviews/evidence/pilot-remotion-v2.mp4';shutil.copy2(pilot,dest)
    manifest.append({'source':pilot.relative_to(ROOT).as_posix(),'archive':dest.relative_to(ROOT).as_posix(),'sha256':sha(dest)})
emit(ROOT/'docs/reviews/evidence-manifest.json',{'scope':'Copies of existing evidence; approval decisions unchanged.','files':manifest})
print(json.dumps({'archivedFiles':len(manifest),'approvalDecisionsChanged':False}))
