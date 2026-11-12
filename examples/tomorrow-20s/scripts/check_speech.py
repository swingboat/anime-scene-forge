"""Local ASR text check; explicitly not an auditory or lipsync approval."""
import project_env
import os, json
from project_ops import ROOT, emit, sha
from gpu_lock import gpu_task

os.environ['HF_HUB_OFFLINE'] = '1'
with gpu_task('speech-text-check'):
    import mlx.core as mx
    from mlx_audio.stt.utils import load_model
    mx.set_memory_limit(4*1024**3)
    model = load_model(str(ROOT/'.cache/tts-models/qwen3-asr-4bit'))
    data = json.loads((ROOT/'production.json').read_text())
    result = []
    for shot in data['shots']:
        path = ROOT/'public'/shot['dialogue']['file']
        value = model.generate(str(path), language='Chinese', max_tokens=96)
        record = {'shot':shot['id'],'expected':shot['dialogue']['text'],
                  'transcription':value.text,'sha256':sha(path)}
        result.append(record)
        print(json.dumps(record,ensure_ascii=False),flush=True)
    emit(ROOT/'outputs/checks/speech-text.json', {'backend':'Qwen3-ASR-0.6B-4bit',
         'scope':'Text verification only. Not a listening, voice quality, emotion or lip-sync score.','lines':result})
