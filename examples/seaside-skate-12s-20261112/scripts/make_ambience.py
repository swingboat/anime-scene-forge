"""Deterministic original environmental sound design; no recordings or music."""
import project_env
import hashlib
import json
import wave
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RATE, SECONDS = 48000, 12
WIND_GAIN, SURF_GAIN, WHEEL_GAIN = 0.010, 0.009, 0.024
rng = np.random.default_rng(61112)
t = np.arange(RATE * SECONDS) / RATE
freq = np.fft.rfftfreq(len(t), 1 / RATE)


def noise(low, high, slope=0):
    spectrum = np.fft.rfft(rng.standard_normal(len(t)))
    shape = (1 - np.exp(-(freq / low) ** 4)) * np.exp(-(freq / high) ** 4)
    shape *= np.maximum(freq, 1) ** slope
    signal = np.fft.irfft(spectrum * shape, n=len(t))
    return signal / np.sqrt(np.mean(signal * signal))


def envelope(points):
    return np.interp(t, [p[0] for p in points], [p[1] for p in points])


fade = np.minimum(t / 0.18, 1) * np.minimum((SECONDS - t) / 0.55, 1)
wind_swell = 0.82 + 0.12 * np.sin(t * 0.72) + 0.06 * np.sin(t * 1.53 + 1.8)
wind = np.column_stack([noise(75, 1800, -0.40), noise(75, 1800, -0.40)])
wind *= (WIND_GAIN * wind_swell * fade)[:, None]

# Broad, unhurried distant surf: low water body and softer high foam.
surf_swell = envelope([(0, .45), (1.7, .9), (3.8, .35), (6.2, 1), (8.1, .4), (10.5, .8), (12, .5)])
surf = np.column_stack([.85 * noise(50, 650, -.35) + .20 * noise(600, 3500, -.1) for _ in range(2)])
surf *= (SURF_GAIN * surf_swell * fade)[:, None]

# Continuous wheel texture follows camera distance; no kick or landing sounds.
distance = envelope([(0, .25), (3.7, .42), (4, 1), (7.8, 1), (8, .65), (10, .38), (12, .12)])
grain = noise(100, 4200, -.32)
roughness = .88 + .05 * np.sin(2 * np.pi * 8.3 * t) + .07 * np.sin(2 * np.pi * 13.71 * t + .4)
roll = grain * roughness + .10 * np.sin(2 * np.pi * (73 * t + .09 * np.sin(t * .7)))
pan = envelope([(0, -.62), (3.99, .12), (4, -.08), (7.99, -.08), (8, -.12), (12, .38)])
wheel = np.column_stack([roll * np.sqrt((1 - pan) / 2), roll * np.sqrt((1 + pan) / 2)])
wheel *= (WHEEL_GAIN * distance * fade)[:, None]

folder = ROOT / 'public/audio'
folder.mkdir(parents=True, exist_ok=True)
records = []
for name, data in [('wind', wind), ('distant-surf', surf), ('skateboard-asphalt', wheel), ('coastal-mix', wind + surf + wheel)]:
    path = folder / f'{name}.wav'
    with wave.open(str(path), 'wb') as stream:
        stream.setparams((2, 2, RATE, 0, 'NONE', 'not compressed'))
        stream.writeframes((np.clip(data, -1, 1) * 32767).astype('<i2').tobytes())
    records.append({'file': path.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'peak': float(np.max(np.abs(data))), 'rms': float(np.sqrt(np.mean(data * data)))})
report = {'method': 'Original procedural filtered-noise environmental sound design, not field recordings', 'seed': 61112, 'rate': RATE, 'channels': 2, 'duration': SECONDS, 'music': False, 'dialogue': False, 'listeningReviewed': False, 'files': records}
(ROOT / 'docs/generation/audio.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(report, indent=2))
