# 已验证经验的MLX参考适配器

选择此后端时用init_project.py的`--profile mlx`。它把独立脚本、两套冻结Python依赖和`docs/mlx-profile.json`复制到当前视频目录；不引用原视频或Skill安装位置。

## 安装范围与版本

- macOS Apple Silicon，历史验证机M3 Pro/18GB；Python3.13。
- MLX0.32.4、mlx-lm0.32.2；LTX-2-MLX提交`747b30ef10e92a011e85b2aa0f6c4ee86ced5218`。
- 视频：dgrauet/ltx-2.3-mlx-q4，修订`f306259444116d71927188af2fbbf7fdc1a8089a`。
- 文本编码：mlx-community/gemma-3-12b-it-4bit，修订`86cc6a8dedbc456dd0e4af01a9d09f396f77e558`。
- 可选声音：Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16，修订`7d3824abff87e49756bb0f83fb5411de75d160c4`，mlx-audio0.6.5。ASR快照只作可选参考，本包未提供自动ASR验收器。

文件清单、尺寸和目标相对路径以复制后的profile为准。模型不打包；本包也不把原影片的画面质量视为新硬件或新包装器已经端到端通过。

在当前视频目录运行：

```sh
python3 scripts/setup_mlx.py video --plan
python3 scripts/setup_mlx.py video --download
# 只在选择本地TTS时安装：
python3 scripts/setup_mlx.py voice --plan
python3 scripts/setup_mlx.py voice --download
```

没有`--download`时只建立相应本地环境；`--plan`只输出估算，不安装和下载。视频模型约26.6GiB，语音另约4.52GB十进制，还需环境、缓存与输出空间。先盘点当前可用磁盘和已有授权，不自动为未选路线下载大模型。

## 内存与任务

ltx_entry.py使用默认float32计算、q4权重、11GiB MLX额度、缓存额度0；Gemma与连接器顺序加载，提示词NPZ缓存，DiT逐块读取。lowram_prompt.py依赖上述固定提交，升级时需重新校验。历史float16试跑遇到Metal错误，不能据此推广所有设备，也不把改精度当成无须短测的优化。

gpu_lock.py只串行当前项目的推理；Agent还要确保同机其他项目没有同时运行视频/TTS/ASR推理。不要停止不属于当前任务的进程。环境、缓存、托管Python和模型都位于当前项目，依赖安装使用复制模式而非共享其他视频环境。

## 可选角色声音

建立本项目`docs/dialogue.json`：

```json
{"language":"Chinese","characters":{"lead":{"seed":42,"description":"年轻、温暖、清楚自然的角色声音"}},"lines":[{"id":"scene-01","character":"lead","text":"我们再试一次吧。","emotion":"耐心鼓励，轻松而真诚"}]}
```

使用用户实际选择的语言/风格。然后：

```sh
.venv-tts/bin/python scripts/synthesize_mlx.py --take v1
ffmpeg -i public/audio/voices/scene-01-v1-raw.wav -ar 48000 -ac 2 -c:a pcm_s16le public/audio/voices/scene-01-v1.wav
```

先核对音色、文字、语速和情绪；过长则改句或重录。设置production.json该镜头的dialogue（含text、sync、fromFrame、file），再用project_ops.py pad-voice保存原速输入。字体、角色图和音乐单独按用户需求准备。

## 连续生成

保存实际提示词到本项目docs/prompts。示例：

```sh
.venv/bin/python scripts/run_mlx.py scene-01 --mode a2v --image public/art/scene-01.png --prompt docs/prompts/scene-01.txt --take v1 --frames 97
python3 scripts/project_ops.py select scene-01 --source public/candidates/scene-01-v1.mp4 --start 0 --take v1 --generation docs/generation/scene-01-v1.json
python3 scripts/project_ops.py sheet scene-01
```

无可见对白镜头用`--mode i2v`。可先加`--dry-run`检查命令和输入元数据，使用普通Python即可；这不运行模型，也不证明画面效果。frames采用8k+1且覆盖选片时长；此参考路线使用24fps、长宽为64的倍数，历史原生尺寸1024×576。

追加参考通过`--anchors docs/prompts/scene-01-anchors.json`提供数组：`[{"image":"public/art/closed.png","frame":17,"strength":1.0,"binding":"guide"}]`。按实际台词选择时点；不是固定嘴型修补算法。候选保留版本，逐帧/1倍速检查后再标记approved。

上游将a2v --distilled标为实验性功能。历史中文对白修复中既有可用结果，也有提前张嘴和脸部变形的失败候选；不能把某次成功扩展为任意角色、语言和台词的保证。

资料：[固定MLX代码](https://github.com/dgrauet/ltx-2-mlx/tree/747b30ef10e92a011e85b2aa0f6c4ee86ced5218)、[LTX官方项目](https://github.com/Lightricks/LTX-2)、[MLX Audio](https://github.com/Blaizzy/mlx-audio)。本包依据历史实做快照固定版本，不跟随上游main自动升级。
