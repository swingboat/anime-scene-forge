#!/usr/bin/env python3
"""Build a portable Skill ZIP with curated text prompts, excluding video projects."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NAME = 'anime-scene-forge'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / '.dist' / f'{NAME}.zip')
    args = parser.parse_args()
    target = args.output.absolute()
    files = [ROOT / 'SKILL.md']
    for directory in ['agents', 'references', 'assets', 'scripts']:
        for path in (ROOT / directory).rglob('*'):
            if path.is_symlink():
                parser.error(f'Symlinks cannot be distributed: {path}')
            if path.is_file() and not any(part in ['__pycache__', 'node_modules', '.cache', '.venv', '.venv-tts', '.git', 'outputs'] for part in path.relative_to(ROOT).parts) and path.suffix != '.pyc':
                if path.name != 'build_skill.py':
                    files.append(path)
    # Never walk all of examples/: it contains independent video projects/models.
    prompts = ROOT / 'examples/prompts'
    if not prompts.is_dir() or prompts.is_symlink():
        parser.error('Missing regular examples/prompts library')
    for path in prompts.rglob('*'):
        if path.is_symlink():
            parser.error(f'Symlinks cannot be distributed: {path}')
        if path.is_file():
            if path.suffix not in {'.md', '.txt', '.json'}:
                parser.error(f'Only text prompt resources are allowed in examples/prompts: {path}')
            files.append(path)
    if target in files:
        parser.error('Output would overwrite a source file')
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in sorted(set(files)):
            archive.write(path, (Path(NAME) / path.relative_to(ROOT)).as_posix())
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None:
            raise SystemExit('ZIP CRC check failed')
        for path in files:
            if archive.read((Path(NAME) / path.relative_to(ROOT)).as_posix()) != path.read_bytes():
                raise SystemExit(f'Archive differs from source: {path}')
    print(json.dumps(dict(file=str(target), files=len(files), bytes=target.stat().st_size,
                          sha256=hashlib.sha256(target.read_bytes()).hexdigest(), crc='passed'),
                     indent=2))


if __name__ == '__main__':
    main()
