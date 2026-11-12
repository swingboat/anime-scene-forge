"""One-time APFS model materialization; inference never reads the source project."""
import project_env
import argparse,json,subprocess,time
from project_ops import ROOT,emit
from pathlib import Path
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source-models',type=Path,required=True)
args=parser.parse_args()
source=args.source_models.resolve()
records=[]
for relative in ['.cache/models']:
 old=source;new=ROOT/relative
 if new.exists():raise SystemExit(f'Preserving existing destination: {new}')
 new.parent.mkdir(parents=True,exist_ok=True)
 start=time.monotonic()
 subprocess.run(['/bin/cp','-cR',str(old),str(new)],check=True)
 files=[p for p in new.rglob('*') if p.is_file()]
 for p in files:
  if p.is_symlink() or p.stat().st_nlink!=1:raise SystemExit(f'Non-independent file: {p}')
  original=old/p.relative_to(new)
  if (p.stat().st_dev,p.stat().st_ino)==(original.stat().st_dev,original.stat().st_ino):raise SystemExit('Inode unexpectedly shared')
 records.append({'source':str(old),'copy':new.relative_to(ROOT).as_posix(),'files':len(files),'bytes':sum(p.stat().st_size for p in files),'independentInodes':True,'method':'APFS clonefile via cp -cR','wallSeconds':round(time.monotonic()-start,2)})
emit(ROOT/'outputs/checks/environment-materialization.json',{'copies':records,'downloadedModels':False,'note':'Only one-time preparation reads source; generation uses project-local model paths.'})
print(json.dumps(records,indent=2))
