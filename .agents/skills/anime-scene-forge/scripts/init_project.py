#!/usr/bin/env python3
"""Copy a standalone video into examples/; never install or download implicitly."""
import argparse,json,math,re,shutil
from fractions import Fraction
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--workspace',type=Path,default=Path.cwd());p.add_argument('--id',required=True)
    p.add_argument('--collection',default='examples',help='Workspace-relative collection directory (default: examples)')
    p.add_argument('--seconds',default='30');p.add_argument('--fps',type=int,default=24)
    p.add_argument('--width',type=int,default=1280);p.add_argument('--height',type=int,default=720)
    p.add_argument('--title',default='Anime narrative scene')
    p.add_argument('--style',choices=['classic-anime','handpainted-film'],default='classic-anime',help='Visual/acting/sound direction (default: classic-anime)')
    p.add_argument('--profile',choices=['external','mlx'],default='external');a=p.parse_args()
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',a.id):p.error('id must use lowercase letters, digits and hyphens')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',a.collection):p.error('collection must use lowercase letters, digits and hyphens')
    try:frames=Fraction(a.seconds)*a.fps
    except (ValueError,ZeroDivisionError):p.error('seconds must be a finite positive number')
    if frames.denominator!=1 or frames<=0 or a.fps<=0 or min(a.width,a.height)<=0 or a.width%2 or a.height%2:
        p.error('Use positive dimensions/fps and a duration containing an integer number of frames; dimensions must be even')
    base=a.workspace.resolve();videos=base/a.collection
    if not base.is_dir():p.error('workspace must be an existing directory')
    if videos.is_symlink() or not videos.resolve().is_relative_to(base):p.error('collection must be a real directory inside the workspace')
    if videos.exists() and not videos.is_dir():p.error('collection must be a directory')
    target=videos/a.id
    if target.exists() or target.is_symlink():p.error(f'Preserving existing destination: {target}')
    videos.mkdir(parents=True,exist_ok=True)
    assets=Path(__file__).resolve().parents[1]/'assets'
    style=json.loads((assets/'styles'/f'{a.style}.json').read_text())
    shutil.copytree(assets/'project',target)
    if a.profile=='mlx':shutil.copytree(assets/'mlx',target,dirs_exist_ok=True)
    for directory in ['public/art','public/candidates','public/video','public/audio/voices','public/audio/drivers','public/fonts','docs/prompts','docs/reviews','docs/generation','docs/selections','.cache/npm','.cache/tmp','outputs/checks']:
        (target/directory).mkdir(parents=True,exist_ok=True)
    shutil.copy2(assets/'styles'/f'{a.style}.json',target/'docs/style.json')
    count=math.ceil(int(frames)/(4*a.fps));each,extra=divmod(int(frames),count)
    shots=[{'id':f'scene-{i+1:02d}','frames':each+int(i<extra),'action':'','art':None,'clip':None,'status':'pending','review':None,'selection':None,'generation':None,'caption':None,'dialogue':None} for i in range(count)]
    data={'schemaVersion':1,'title':a.title,'style':a.style,'format':{'width':a.width,'height':a.height,'fps':a.fps,'durationFrames':int(frames)},'fontFile':None,'background':None,'sfx':[],'shots':shots}
    (target/'production.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    for name in ['package.json','package-lock.json']:
        path=target/name;data=json.loads(path.read_text());data['name']=a.id
        if 'packages' in data:data['packages']['']['name']=a.id
        path.write_text(json.dumps(data,indent=2)+'\n')
    brief=f'# {a.title}\n\n状态：制作规划，未生成成片。\n\n- 时长：{a.seconds}秒，{a.fps}fps，{int(frames)}帧。\n- 画幅：{a.width}×{a.height}。\n- 角色、造型、场景与参考来源：待按用户要求填写。\n- 故事与动作：按叙事修改production.json中的默认等长分段。\n- 对白模式、语言、声线与情绪：待按用户要求填写。\n- 图像与生成后端：{a.profile}；实际能力、版本和预算需记录。\n- 交付：按用户要求提供预览、MP4和独立工程。\n'
    (target/'docs/brief.md').write_text(brief)
    with (target/'docs/brief.md').open('a') as f:
        f.write(f'\n## 风格\n\n- {style["name"]}（{a.style}），完整方向保存在 docs/style.json。\n- 原画和视频按该配置组织提示词；声音按 soundDirection 设计，视觉检查覆盖 reviewChecks。\n- 风格选择不自动增加角色、对白、配乐或镜头。\n')
    (target/'docs/production-method.md').write_text('# 实际制作记录\n\n状态：尚未制作。完成后记录真实版本、候选、失败、修正、检查、耗时与限制。\n')
    print(json.dumps({'project':str(target),'profile':a.profile,'style':a.style,'frames':int(frames),'shots':count,'installed_dependencies':False,'downloaded_models':False},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
