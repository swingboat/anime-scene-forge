"""Observable initialization/isolation and distribution behavior, no model downloads."""
import ast
import array
import hashlib
import json
import os
import math
import posixpath
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
import wave
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
ENV = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}


class SkillTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='.test-', dir=ROOT / 'examples')
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name)

    def init(self, *extra, ok=True):
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/init_project.py'),
                                 '--workspace', str(self.workspace), '--id', 'test-scene', *extra],
                                env=ENV, text=True, capture_output=True)
        self.assertEqual(result.returncode == 0, ok, result.stdout + result.stderr)
        return result

    def test_default_examples_and_exact_frames(self):
        result = json.loads(self.init('--seconds', '30').stdout)
        project = self.workspace / 'examples/test-scene'
        self.assertEqual(result['project'], str(project))
        data = json.loads((project / 'production.json').read_text())
        self.assertEqual(data['format']['durationFrames'], 720)
        self.assertEqual(data['style'], 'classic-anime')
        self.assertEqual(json.loads((project/'docs/style.json').read_text())['id'], data['style'])
        self.assertEqual(sum(s['frames'] for s in data['shots']), 720)
        self.assertTrue(all(isinstance(s['frames'], int) for s in data['shots']))
        self.assertFalse((project / '.venv').exists())
        self.assertFalse((project / 'node_modules').exists())
        self.assertFalse((project / 'scripts/run_mlx.py').exists())
        self.assertFalse((self.workspace / 'videos').exists())
        self.assertEqual(json.loads((project / 'package-lock.json').read_text())['packages']['']['name'], 'test-scene')

    def test_preserves_existing_project(self):
        self.init()
        project = self.workspace / 'examples/test-scene'
        before = hashlib.sha256((project / 'production.json').read_bytes()).hexdigest()
        sentinel = project / 'user-notes.txt'
        sentinel.write_text('Keep this')
        self.init('--seconds', '20', ok=False)
        self.assertEqual(hashlib.sha256((project / 'production.json').read_bytes()).hexdigest(), before)
        self.assertEqual(sentinel.read_text(), 'Keep this')

    def test_handpainted_style_is_materialized_and_used_in_mlx_prompt(self):
        self.init('--seconds', '3', '--profile', 'mlx', '--style', 'handpainted-film')
        project = self.workspace/'examples/test-scene'
        data = json.loads((project/'production.json').read_text())
        profile = json.loads((project/'docs/style.json').read_text())
        self.assertEqual(data['style'], 'handpainted-film')
        self.assertEqual(profile['id'], data['style'])
        scene = project/'docs/prompts/scene.txt'
        scene.write_text('A girl feels a light breeze. No dialogue.')
        # Dry-run hashes this stand-in but never decodes it or imports a model.
        (project/'public/art/test.png').write_bytes(b'cpu-only-placeholder')
        image = subprocess.run([sys.executable, 'scripts/style_profile.py', '--kind', 'image',
                                '--scene', 'docs/prompts/scene.txt'], cwd=project, env=ENV, text=True, capture_output=True)
        self.assertEqual(image.returncode, 0, image.stderr)
        self.assertIn(profile['imagePrompt'], image.stdout)
        result = subprocess.run([sys.executable, 'scripts/run_mlx.py', 'scene-01', '--mode', 'i2v',
                                 '--image', 'public/art/test.png', '--prompt', 'docs/prompts/scene.txt',
                                 '--frames', '73', '--take', 'dry', '--dry-run'],
                                cwd=project, env=ENV, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        dry = json.loads(result.stdout)
        self.assertFalse(dry['executed'])
        self.assertEqual(dry['record']['style'], data['style'])
        self.assertEqual(dry['record']['styleSha256'], hashlib.sha256((project/'docs/style.json').read_bytes()).hexdigest())
        self.assertIn(profile['videoPrompt'], dry['record']['prompt'])
        self.assertIn(scene.read_text(), dry['record']['prompt'])
        self.assertIn(dry['record']['prompt'], dry['command'])
        self.assertFalse((project/'docs/generation/scene-01-dry.json').exists())

    def test_unknown_style_rejected_before_creating_project(self):
        self.init('--style', 'unknown-style', ok=False)
        self.assertEqual(list(self.workspace.iterdir()), [])

    def test_style_mismatch_and_missing_profile_rejected(self):
        self.init('--seconds', '.5')
        project = self.workspace/'examples/test-scene'
        path = project/'docs/style.json'
        profile = json.loads(path.read_text())
        profile['id'] = 'handpainted-film'
        path.write_text(json.dumps(profile))
        command = [sys.executable, 'scripts/project_ops.py', 'validate', '--stage', 'scaffold']
        result = subprocess.run(command, cwd=project, env=ENV, text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('does not match', result.stderr)
        path.unlink()
        result = subprocess.run(command, cwd=project, env=ENV, text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)

    def test_legacy_project_without_style_keeps_original_prompt(self):
        self.init('--seconds', '.5')
        project = self.workspace/'examples/test-scene'
        path = project/'production.json'
        data = json.loads(path.read_text());data.pop('style');path.write_text(json.dumps(data))
        (project/'docs/style.json').unlink()
        (project/'docs/prompts/scene.txt').write_text('Keep this original prompt.')
        result = subprocess.run([sys.executable, 'scripts/style_profile.py', '--kind', 'video',
                                 '--scene', 'docs/prompts/scene.txt'], cwd=project, env=ENV, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), 'Keep this original prompt.')

    def test_rejects_invalid_duration_and_format_without_files(self):
        for args in [('--seconds', 'NaN'), ('--seconds', '0'), ('--seconds', '-1'),
                     ('--seconds', '0.1'), ('--fps', '0'), ('--width', '1279'),
                     ('--seconds', '1/0')]:
            with self.subTest(args=args):
                self.init(*args, ok=False)
        self.assertEqual(list(self.workspace.iterdir()), [])

    def test_explicit_legacy_collection(self):
        self.init('--collection', 'videos', '--seconds', '0.5')
        self.assertTrue((self.workspace / 'videos/test-scene/production.json').is_file())

    def test_rejects_collection_escape_and_symlinks(self):
        self.init('--collection', '../outside', ok=False)
        outside = self.workspace / 'outside'
        outside.mkdir()
        link = self.workspace / 'examples'
        link.symlink_to(outside, target_is_directory=True)
        self.init(ok=False)
        self.assertEqual(list(outside.iterdir()), [])

    def test_mlx_project_is_relocatable_and_self_contained(self):
        self.init('--profile', 'mlx', '--seconds', '0.5')
        project = self.workspace / 'examples/test-scene'
        moved = self.workspace / 'standalone'
        shutil.move(project, moved)
        self.assertTrue((moved / 'docs/mlx-profile.json').is_file())
        self.assertTrue((moved / 'requirements-tts.txt').is_file())
        for args in [['scripts/project_ops.py', 'validate', '--stage', 'scaffold'],
                     ['scripts/setup_mlx.py', 'video', '--plan'],
                     ['scripts/setup_mlx.py', 'voice', '--plan']]:
            result = subprocess.run([sys.executable, *args], cwd=moved, env=ENV, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn(str(ROOT), result.stdout)
        self.assertFalse((moved / '.venv').exists())
        for path in moved.rglob('*'):
            self.assertFalse(path.is_symlink())
            if path.is_file():
                self.assertEqual(path.stat().st_nlink, 1)

    def test_distribution_contains_runtime_and_curated_prompts_without_video_projects(self):
        target = self.workspace / 'skill.zip'
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/build_skill.py'), '--output', str(target)],
                                env=ENV, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        with zipfile.ZipFile(target) as archive:
            names = archive.namelist()
            self.assertIn('anime-scene-forge/SKILL.md', names)
            self.assertIn('anime-scene-forge/assets/project/package-lock.json', names)
            self.assertIn('anime-scene-forge/assets/mlx/scripts/run_mlx.py', names)
            self.assertIn('anime-scene-forge/assets/styles/classic-anime.json', names)
            self.assertIn('anime-scene-forge/assets/styles/handpainted-film.json', names)
            self.assertFalse(any('/tests/' in n or '/.git/' in n for n in names))
            examples = [n for n in names if '/examples/' in n]
            self.assertTrue(examples)
            self.assertTrue(all(n.startswith('anime-scene-forge/examples/prompts/') for n in examples))
            self.assertTrue(all(Path(n).suffix in {'.md','.txt','.json'} for n in examples))
            extracted = self.workspace / 'unpacked'
            archive.extractall(extracted)
        run = subprocess.run([sys.executable, str(extracted / 'anime-scene-forge/scripts/init_project.py'),
                              '--workspace', str(self.workspace), '--id', 'from-zip', '--seconds', '0.5', '--style', 'handpainted-film'],
                             env=ENV, text=True, capture_output=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue((self.workspace / 'examples/from-zip/scripts/project_ops.py').is_file())
        self.assertEqual(json.loads((self.workspace/'examples/from-zip/production.json').read_text())['style'], 'handpainted-film')

    def test_python_sources_parse(self):
        for directory in ['scripts', 'assets']:
            for path in (ROOT / directory).rglob('*.py'):
                with self.subTest(path=path):
                    ast.parse(path.read_text())

    def test_distributed_prompt_resources_are_discoverable_and_self_contained(self):
        target = self.workspace / 'skill.zip'
        subprocess.run([sys.executable, str(ROOT / 'scripts/build_skill.py'), '--output', str(target)],
                       env=ENV, check=True, capture_output=True)
        with zipfile.ZipFile(target) as archive:
            names = set(archive.namelist())
            self.assertIn('anime-scene-forge/references/prompt-examples.md', names)
            self.assertIn('anime-scene-forge/examples/prompts/README.md', names)
            for style in ['classic-anime','handpainted-film']:
                prefix=f'anime-scene-forge/examples/prompts/{style}/'
                self.assertIn(prefix+'README.md', names)
                self.assertIn(prefix+'scene-image.txt', names)
                self.assertIn(prefix+'scene-video.txt', names)
                self.assertTrue(any(n.startswith(prefix) and n.endswith('.md') and n!=prefix+'README.md' for n in names))
            self.assertIn('anime-scene-forge/examples/prompts/handpainted-film/coastal-skateboard-12s.md', names)
            for name in [n for n in names if n.endswith('.md')]:
                body = archive.read(name).decode('utf-8')
                for destination in re.findall(r'\[[^\]]*\]\(([^)]+)\)', body):
                    destination = unquote(destination.split('#', 1)[0].strip('<>'))
                    if not destination or re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', destination):
                        continue
                    linked = posixpath.normpath(posixpath.join(posixpath.dirname(name), destination))
                    self.assertIn(linked, names, f'{name} references missing {destination}')
            dialogue = json.loads(archive.read('anime-scene-forge/examples/prompts/classic-anime/dialogue-example.json'))
            self.assertTrue(dialogue['characters'])
            self.assertEqual(len({line['id'] for line in dialogue['lines']}), len(dialogue['lines']))
            for line in dialogue['lines']:
                self.assertIn(line['character'], dialogue['characters'])
                self.assertTrue(line['text'].strip())
                self.assertTrue(line['emotion'].strip())

    def test_distribution_rejects_media_in_prompt_library(self):
        isolated=self.workspace/'isolated-skill'
        isolated.mkdir()
        shutil.copy2(ROOT/'SKILL.md',isolated/'SKILL.md')
        for directory in ['agents','references','assets','scripts','examples/prompts']:
            shutil.copytree(ROOT/directory,isolated/directory,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        (isolated/'examples/prompts/unintended-movie.mp4').write_bytes(b'media must not enter the skill')
        archive=self.workspace/'invalid.zip'
        result=subprocess.run([sys.executable,str(isolated/'scripts/build_skill.py'),'--output',str(archive)],env=ENV,text=True,capture_output=True)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('Only text prompt resources',result.stderr)
        self.assertFalse(archive.exists())

    def media_command(self, *args, cwd):
        return subprocess.run(list(args), cwd=cwd, env=ENV, check=True, capture_output=True)

    def test_audio_tail_trim_preserves_pictures_and_speech_placement(self):
        self.init('--seconds', '0.5')
        project = self.workspace / 'examples/test-scene'
        self.media_command('ffmpeg', '-y', '-v', 'error', '-f', 'lavfi', '-i',
                           'testsrc2=size=64x64:rate=24', '-frames:v', '12', '-an',
                           '-c:v', 'libx264', 'outputs/pictures.mp4', cwd=project)
        samples = array.array('h')
        for i in range(28800):
            value = int(6000*math.sin(2*math.pi*440*i/48000)) if 6000 <= i < 15600 else 0
            samples.extend([value, value])
        if sys.byteorder != 'little': samples.byteswap()
        with wave.open(str(project/'outputs/tone.wav'), 'wb') as stream:
            stream.setnchannels(2); stream.setsampwidth(2); stream.setframerate(48000)
            stream.writeframes(samples.tobytes())
        self.media_command('ffmpeg', '-y', '-v', 'error', '-i', 'outputs/pictures.mp4',
                           '-i', 'outputs/tone.wav', '-map', '0:v:0', '-map', '1:a:0',
                           '-c:v', 'copy', '-c:a', 'aac', 'outputs/tail.mp4', cwd=project)
        def pixels():
            result = self.media_command('ffmpeg', '-v', 'error', '-i', 'outputs/tail.mp4',
                                        '-map', '0:v:0', '-f', 'framemd5', '-', cwd=project)
            return [line.rsplit(b',', 1)[-1].strip() for line in result.stdout.splitlines() if not line.startswith(b'#')]
        def audio():
            result = self.media_command('ffmpeg', '-v', 'error', '-i', 'outputs/tail.mp4',
                                        '-map', '0:a:0', '-t', '0.5', '-ac', '1', '-ar', '48000', '-f', 's16le', '-', cwd=project)
            values = array.array('h'); values.frombytes(result.stdout)
            if sys.byteorder != 'little': values.byteswap()
            return values
        before_pixels, before_audio = pixels(), audio()
        self.media_command(sys.executable, 'scripts/trim_export.py', 'outputs/tail.mp4', cwd=project)
        meta = json.loads(self.media_command('ffprobe', '-v', 'error', '-show_format', '-show_streams',
                                             '-of', 'json', 'outputs/tail.mp4', cwd=project).stdout)
        self.assertAlmostEqual(float(meta['format']['duration']), .5, places=3)
        self.assertEqual(pixels(), before_pixels)
        after_audio = audio()
        self.assertEqual(len(before_audio), len(after_audio))
        correlation = sum(x*y for x,y in zip(before_audio,after_audio))/math.sqrt(sum(x*x for x in before_audio)*sum(y*y for y in after_audio))
        self.assertGreater(correlation, .99)
        first_before = next(i for i,v in enumerate(before_audio) if abs(v)>1000)
        first_after = next(i for i,v in enumerate(after_audio) if abs(v)>1000)
        self.assertLessEqual(abs(first_after-first_before), 24)
        record = json.loads((project/'outputs/checks/tail-audio-tail.json').read_text())
        self.assertTrue((project/record['original']).is_file())

    def test_silent_export_tail_check_is_idempotent(self):
        self.init('--seconds', '0.5')
        project = self.workspace / 'examples/test-scene'
        self.media_command('ffmpeg', '-y', '-v', 'error', '-f', 'lavfi', '-i',
                           'testsrc2=size=64x64:rate=24', '-frames:v', '12', '-an',
                           '-c:v', 'libx264', 'outputs/silent.mp4', cwd=project)
        before = (project/'outputs/silent.mp4').read_bytes()
        for _ in range(2):
            self.media_command(sys.executable, 'scripts/trim_export.py', 'outputs/silent.mp4', cwd=project)
        self.assertEqual((project/'outputs/silent.mp4').read_bytes(), before)

    def test_lockfile_uses_public_registry_and_matches_manifest(self):
        lock = json.loads((ROOT / 'assets/project/package-lock.json').read_text())
        manifest = json.loads((ROOT / 'assets/project/package.json').read_text())
        for section in ['dependencies', 'devDependencies']:
            self.assertEqual(lock['packages'][''][section], manifest[section])
        for package in lock['packages'].values():
            if package.get('resolved'):
                self.assertTrue(package['resolved'].startswith('https://registry.npmjs.org/'))
                self.assertTrue(package.get('integrity'))


if __name__ == '__main__':
    unittest.main()
