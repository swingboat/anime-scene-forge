"""Make numbered review pages; no visual approval is assigned."""
import project_env
from PIL import Image,ImageDraw
from project_ops import ROOT
source=ROOT/'outputs/checks/scene-01/full'
files=sorted(source.glob('frame-*.png'))
if not files:raise SystemExit('Run project_ops.py sheet scene-01 first')
for kind,crop in [('full',None),('face',(680,0,1240,440))]:
 for offset in range(0,len(files),12):
  page=Image.new('RGB',(1280,630),'#151b22');draw=ImageDraw.Draw(page)
  for j,path in enumerate(files[offset:offset+12]):
   picture=Image.open(path).convert('RGB')
   if crop:picture=picture.crop(crop)
   picture.thumbnail((320,180))
   x=(j%4)*320;y=(j//4)*210
   page.paste(picture,(x+(320-picture.width)//2,y+25+(180-picture.height)//2))
   draw.text((x+8,y+6),f'{kind} / frame {offset+j:02d}',fill='white')
  target=ROOT/f'docs/reviews/{kind}-{offset//12+1:02d}.jpg'
  page.save(target,quality=92)
  print(target)
