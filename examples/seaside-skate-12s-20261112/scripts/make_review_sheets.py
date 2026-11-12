"""Review every frame in readable batches, with frame numbers and detail crops."""
import project_env
import argparse
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('shot')
parser.add_argument('--source')
parser.add_argument('--crop', nargs=4, type=int)
parser.add_argument('--label', default='full')
parser.add_argument('--drift-x', type=float, default=0)
args = parser.parse_args()
data = json.loads((ROOT / 'production.json').read_text())
shot = next(s for s in data['shots'] if s['id'] == args.shot)
source = ROOT / args.source if args.source else ROOT / 'public' / shot['clip']
folder = ROOT / 'outputs/checks' / args.shot / 'frames'
folder.mkdir(parents=True, exist_ok=True)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(source), '-frames:v', str(shot['frames']), str(folder / '%04d.png')], check=True)
frames = sorted(folder.glob('*.png'))
out = ROOT / 'docs/reviews' / args.shot
out.mkdir(parents=True, exist_ok=True)
for batch in range(0, len(frames), 12):
    sheet = Image.new('RGB', (1280, 4 * 202), '#19232b')
    draw = ImageDraw.Draw(sheet)
    for i, path in enumerate(frames[batch:batch + 12]):
        im = Image.open(path).convert('RGB')
        if args.crop:
            x0, y0, w0, h0 = args.crop
            x0 += round((batch+i)*args.drift_x)
            im = im.crop((x0, y0, x0+w0, y0+h0))
        im.thumbnail((426, 176))
        x, y = (i % 3) * 426, (i // 3) * 202
        sheet.paste(im, (x, y + 24))
        draw.text((x + 8, y + 5), f'{args.shot} frame {batch+i:03d}  {(batch+i)/24:.3f}s', fill='white')
    sheet.save(out / f'{args.label}-{batch//12+1:02d}.jpg', quality=92)
print(out)
