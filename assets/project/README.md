# Independent anime video project

Edit `docs/brief.md` and `production.json` before generating footage. All paths below are relative to this directory. The initial shot allocation is a timing scaffold, not a finished storyboard.

## Style

`production.json.style` selects the project-local `docs/style.json`: `classic-anime` (clean cel animation, default) or `handpainted-film` (hand-painted backgrounds, natural light and subtle environmental acting). Read `imagePrompt`, `videoPrompt`, `soundDirection` and `reviewChecks` before production. Compose an artwork prompt with `python3 scripts/style_profile.py --kind image --scene docs/prompts/scene-01-image.txt --output docs/prompts/scene-01-image-effective.txt` and pass that text to your image tool. MLX `run_mlx.py` automatically prefixes the selected video direction to its scene prompt and records the effective text/profile hashes. Keep scene files free of that automatic prefix. External backends can use `--kind video` and record the same style provenance. Changes to style need new media/reviews; existing projects without a style keep their original prompt.

## Install and preview

Requirements: Node.js 22+, npm, Python 3.10+, ffmpeg/ffprobe, Chrome or a project-local Remotion browser. Optional generation environments have separate requirements in `docs/mlx-profile.json` when installed.

```sh
npm ci --cache .cache/npm
npm run check:source
npm run dev
```

`CHROME_BIN` can point to an installed Chrome; `PYTHON_BIN` can select Python. The run wrapper sets cache/temp paths inside this project. Any extra installation/generation command must also set `TMPDIR`, `TMP`, `TEMP` and package caches inside `.cache` (use `scripts/project_env.py` for Python entrypoints). Do not share another video's virtualenv, node_modules, model paths or assets.

Edit the timeline, captions and asset paths in `production.json`; Studio hot-reloads those changes. The Scenes folder previews each shot through a stable component wrapper. The template uses OffthreadVideo/Html5Audio for preview compatibility with the tested host.

## Add media and sound

- Keep complete reference artwork in `public/art`, raw candidates in `public/candidates`, and selected clips in `public/video`. Record prompts and backend versions under `docs`. Use forward slashes for browser-facing paths on every platform.
- Set format and shot durations in `production.json`; their sum must equal `format.durationFrames`. Use the same native integer fps throughout unless a different route is explicitly designed.
- Put adopted voice WAVs in `public/audio/voices` (48 kHz PCM16). Set `dialogue` to null for silent shots; for dialogue use `text`, `file`, `fromFrame`, and `sync` (`on-screen` or `voiceover`). On-screen speech additionally needs a matching `driverFile` and A2V generation record.
- Add optional captions with local `startFrame`/`endFrame` and `text`. Copy a licensed font into `public/fonts` and set `fontFile` when exact glyph rendering matters.
- `background` is null or `{ "file": "audio/bed.wav", "volume": 0.2 }`. Duck the bed for dialogue using your audio tools. `sfx` contains `{ "file": "audio/clap.wav", "frame": 100, "volume": 0.2 }`; event frames are global.

Examples (replace identifiers and paths with real files):

```sh
python3 scripts/project_ops.py pad-voice scene-01 --voice public/audio/voices/scene-01-v1.wav --from-frame 12 --source-frames 97 --take v1
python3 scripts/project_ops.py select scene-01 --source public/candidates/scene-01-v1.mp4 --start 0 --take v1 --generation docs/generation/scene-01-v1.json
python3 scripts/project_ops.py sheet scene-01
npm run render:draft
```

`select` keeps native speed, mutes candidate audio and resets visual approval. A crop can be supplied as `--crop x y width height`; check heads, hands and objects after cropping. On a changed voice or timing, create a new versioned driver and regenerate on-screen speech. Never reuse the previous visual approval after media changes.

Selections are linked through `shot.selection` to the original source path/hash, native frame range and adopted clip hash. For on-screen speech, pass the A2V generation record to `select`. If selecting from source frame N instead of 0, prepare the voice **before generation** with `pad-voice --source-start N`, covering N + shot frames, then `select --start N`. `fromFrame` remains relative to the adopted shot; changing the crop interval afterwards requires a new driver/take.

After actual frame review and normal-speed playback, write a project-local review JSON with `clipSha256`, `styleSha256` (hash of `docs/style.json` when style is set), `visualReviewed`, `normalSpeedReviewed`, `reviewer`, `observations`, and `limitations`. Record actual observations for the profile's `reviewChecks`. Point `shot.review` to it and set `shot.status` to `approved`. Helper success does not fill this record automatically. Keep candidate and user acceptance distinct.

## Export, check, package

```sh
npm run render
npm run check
npm run package
```

Outputs: `outputs/final.mp4` and `outputs/project.zip`. The package contains this project's code, locked dependencies, media, source records and final video; reinstallable environments, models, caches and node_modules are excluded. Record actual techniques, failures, time and limitations in `docs/production-method.md`. Technical checks do not assess expression or phoneme accuracy.

If AAC encoding adds an audio tail beyond the composition, the render wrapper copies the video stream unchanged and trims/reencodes only audio at 320 kbps to the requested duration. Original renders remain in `outputs/intermediate`; before/after hashes and processing are recorded in `outputs/checks/*-audio-tail.json`. This does not change dialogue tempo or placement. Silent exports are left unchanged. Final checks cover container duration and fingerprint the render helpers as well as source/media, so changing an export helper requires a fresh render.

For portable visual evidence, place compact contact sheets or review images under `docs/reviews/` alongside authored review JSON; the project ZIP includes that directory. Full frame PNGs under `outputs/checks` remain local and can be regenerated from the included candidates.
