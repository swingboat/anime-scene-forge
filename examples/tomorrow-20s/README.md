# 《明天，我也在》

20秒日系二维动漫短片。1280×720、24fps、480帧，中文普通话配音，五个4秒镜头。

## 预览与编辑

```sh
npm ci --cache .cache/npm
npm run dev -- --port 3310
```

打开 http://localhost:3310/Episode 。侧栏 Scenes 可单独预览五个镜头。当前机器依赖已安装；此工程有自己的 node_modules、Python环境、模型、素材和缓存。

编辑 `production.json` 修改时间轴、字幕、配乐音量；`src/Root.tsx` 负责Remotion合成。对白音轨、角色配置分别在 `public/audio/voices` 和 `docs/dialogue.json`。修改可见对白的音色、时间或文本后，需要重建driver并重新生成对应讲话画面。

## 文件

- `outputs/final.mp4`：最终20秒H.264/AAC视频。
- `outputs/review-candidate.mp4`：完整候选导出。
- `public/art`：本片原创主场景及近景原画。
- `public/candidates`：未经变速的97帧连续原始候选。
- `public/video`：各镜头从源第0帧采用96帧，放大到交付分辨率。
- `docs/prompts`、`docs/generation`、`docs/selections`、`docs/reviews`：提示词、生成来源、选片和实际检查记录。
- `docs/production-method.md`：实际使用后端、检查范围、失败/修正与限制。

## 检查与导出

```sh
npm run check:source
npm run render:draft
npm run render
npm run check
```

正式导出要求每个镜头的实际内部检查记录与采用片段哈希匹配。用户验收另行记录，不由脚本推定。

## 生成环境

系统工具：Node.js 22+、npm、Python3.13、ffmpeg/ffprobe、Chrome。当前工程使用MLX0.32.4，LTX-2.3 q4 + Gemma3 q4，以及Qwen3-TTS VoiceDesign。固定版本和模型清单见 `docs/mlx-profile.json`。本地已经保存独立模型副本，未自动下载模型。所有推理命令从本目录运行。

```sh
.venv-tts/bin/python scripts/synthesize_mlx.py --take NEW-TAKE
.venv/bin/python scripts/run_mlx.py scene-04 --mode a2v --image public/art/aqing-close.png --prompt docs/prompts/scene-04.txt --take NEW-TAKE --frames 97
```

重新合成需先配置新声音的采用/静音窗口。不要覆盖旧候选；用新take名称。不要同时启动多个GPU任务。

`public/audio/piano-original.wav`为本片原创程序钢琴，`classroom-ambience.wav`为程序生成环境声。Noto Sans SC字体随本工程复制，许可见 `docs/NOTO-OFL.txt`。图像工具的宿主默认原始输出另存于generated_images；本工程只引用已归档到public/art的副本。

正式导出会自动修整AAC编码尾部，使容器也精确为20秒；源视频码流不重编码。完整制作与内部检查记录见`docs/production-method.md`，精简证据见`docs/reviews/evidence`。声音听感与用户最终验收仍待用户复核。
