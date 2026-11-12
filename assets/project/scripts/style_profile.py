"""Project-local style directions shared by artwork preparation and video generation."""
import project_env
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STYLE_IDS = ('classic-anime', 'handpainted-film')


def load_style(production=None):
    data = production if production is not None else json.loads((ROOT / 'production.json').read_text())
    if 'style' not in data:
        return None  # Existing projects keep their original prompts and look.
    if data['style'] not in STYLE_IDS:
        raise ValueError('Unknown style; use classic-anime or handpainted-film')
    path = ROOT / 'docs/style.json'
    if path.is_symlink() or not path.resolve().is_relative_to(ROOT):
        raise ValueError('Style profile must be a project-local regular file')
    profile = json.loads(path.read_text())
    if profile.get('schemaVersion') != 1 or profile.get('id') != data['style']:
        raise ValueError('Style profile does not match production.style')
    for field in ('name', 'imagePrompt', 'videoPrompt', 'soundDirection'):
        if not isinstance(profile.get(field), str) or not profile[field].strip():
            raise ValueError(f'Incomplete style profile: {field}')
    checks = profile.get('reviewChecks')
    if not isinstance(checks, list) or not checks or not all(isinstance(c, str) and c.strip() for c in checks):
        raise ValueError('Style profile needs meaningful reviewChecks')
    return profile


def compose_prompt(scene, kind, production=None):
    if kind not in ('image', 'video'):
        raise ValueError('Prompt kind must be image or video')
    if not isinstance(scene, str) or not scene.strip():
        raise ValueError('Scene prompt is empty')
    profile = load_style(production)
    if not profile:
        return scene.strip()
    return profile[kind + 'Prompt'].strip() + '\n\nScene-specific direction (explicit scene choices take priority):\n' + scene.strip()


def style_provenance(production=None):
    profile = load_style(production)
    if not profile:
        return {}
    return {'style': profile['id'], 'styleSha256': hashlib.sha256((ROOT / 'docs/style.json').read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kind', choices=['image', 'video'], required=True)
    parser.add_argument('--scene', type=Path, required=True, help='Project-local scene prompt text file')
    parser.add_argument('--output', type=Path, help='Optional new project-local effective prompt file')
    args = parser.parse_args()
    def inside(path):
        candidate = ROOT / path
        if not candidate.resolve().is_relative_to(ROOT) or candidate.is_symlink():
            parser.error('Prompt files must stay inside this project')
        return candidate
    prompt = compose_prompt(inside(args.scene).read_text(), args.kind)
    if args.output:
        target = inside(args.output)
        if target.exists():
            parser.error('Preserving existing prompt; use a new output name')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(prompt + '\n')
    print(prompt)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, FileNotFoundError) as error:
        raise SystemExit(str(error))
