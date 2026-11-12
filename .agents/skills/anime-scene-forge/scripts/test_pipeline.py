#!/usr/bin/env python3
"""Create a fresh examples/ fixture and run technical checks; never run model inference."""
import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--id', default='pipeline-smoke-' + datetime.now().strftime('%Y%m%d-%H%M%S'))
    parser.add_argument('--render', action='store_true', help='Install local locked npm dependencies, render and package')
    args = parser.parse_args()
    result = subprocess.run([sys.executable, str(ROOT / 'scripts/init_project.py'),
                             '--workspace', str(ROOT), '--id', args.id, '--seconds', '0.5',
                             '--profile', 'mlx', '--title', 'Technical pipeline fixture'],
                            text=True, capture_output=True)
    if result.returncode:
        raise SystemExit(result.stderr)
    project = Path(json.loads(result.stdout)['project'])
    (project / '.skill-smoke-fixture').write_text('anime-scene-forge:test-fixture:v1\n')
    # Keep the fixture runner and all generated logs in this standalone video.
    shutil.copy2(ROOT / 'scripts/smoke_test.py', project / 'scripts/smoke_test.py')
    env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'UV_LINK_MODE': 'copy'}
    for key, folder in [('TMPDIR', '.cache/tmp'), ('TMP', '.cache/tmp'), ('TEMP', '.cache/tmp'),
                        ('npm_config_cache', '.cache/npm'), ('XDG_CACHE_HOME', '.cache')]:
        env[key] = str(project / folder)
    if args.render:
        with (project / 'outputs/checks/npm-install.log').open('w') as log:
            install = subprocess.run(['npm', 'ci', '--cache', '.cache/npm', '--no-audit', '--no-fund'],
                                     cwd=project, env=env, stdout=log, stderr=subprocess.STDOUT)
        if install.returncode:
            raise SystemExit(f'npm ci failed; see {project}/outputs/checks/npm-install.log')
    command = [sys.executable, 'scripts/smoke_test.py', '--project', str(project)]
    if args.render:
        command.append('--render')
    result = subprocess.run(command, cwd=project, env=env, text=True, capture_output=True)
    (project / 'outputs/checks/pipeline.log').write_text(result.stdout + result.stderr)
    if result.returncode:
        raise SystemExit(f'Pipeline failed; see {project}/outputs/checks/pipeline.log\n{result.stderr}')
    report = json.loads(result.stdout)
    print(json.dumps(dict(project=str(project), status=report['status'], cases=len(report['cases']),
                          rendered=report['rendered'], scope=report['scope']), indent=2))


if __name__ == '__main__':
    main()
