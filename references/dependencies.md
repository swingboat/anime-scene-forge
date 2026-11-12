# 技术与依赖

## 核心与条件依赖

| 层 | 用途 | 依赖与选择 |
|---|---|---|
| Agent | 理解需求、写提示词/代码、操作文件与运行命令 | 支持Agent Skills或能读SKILL.md的编码Agent；不强制MCP或某家API |
| 原画 | 人物与场景一致性、机位参考 | 宿主内置图像工具、已接入图像服务或用户提供的原画。Claude Code不能被假定具有Codex内置图像生成能力 |
| 连续表演 | I2V及音频驱动的讲话表演 | 适配器必须满足backend-contract.md；本包可选MLX参考实现 |
| 声音 | 角色对白、环境、配乐、音效 | 用户音频或所选TTS；可见对白要先定声音。Qwen3-TTS VoiceDesign为可选本地参考，不是所有任务的必装依赖 |
| 剪辑与导出 | 时间轴、字幕、音效、MP4、可编辑工程 | Node.js 22+、npm、Remotion/React/TypeScript；系统ffmpeg/ffprobe、可用Chrome或工程内浏览器 |
| 工程辅助 | 独立路径、选片、驱动WAV、检查和ZIP | Python 3.10+标准库；本包核心脚本不依赖MLX/Numpy/Pillow |
| 内容检查 | 对白文字辅助转写 | 可选ASR；正确转写不能证明嘴型正确 |
| 画面与播放检查 | 看原画、逐帧图、实际1倍速播放 | 可用的图像查看/视频播放能力；有浏览器工具时操作Studio或成片页 |

模板固定 Remotion及其配套包4.0.541、React/React DOM19.3.1、TypeScript5.9.3。它们是本项目经验的版本快照，不宣称是最新或所有机器的最低版本。本次模板验证的实际版本写入validation.md；升级时同步Remotion包版本并重新跑模板测试。

需要中文或其他特定字形时，将字体及许可复制/下载到当前视频的public内，设置production.json的fontFile。不能把本机系统字体存在当作其他机器也能复现的依据。Skill包不附带模型、字体、角色图、影片或密钥。

## Apple Silicon参考环境

视频：Python3.13、uv、git、MLX0.32.4、mlx-lm0.32.2、Gemma3与LTX-2.3 q4。模型文件约26.6GiB，环境与下载中间文件另需空间。实际机器是M3 Pro、18GB统一内存，使用顺序加载/逐块读取/提示词缓存；这不是对16GB或其他设备的最低配置保证。

可选语音：独立.venv-tts，mlx-audio0.6.5与Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16，权重与tokenizer约4.52GB十进制。可选Qwen3-ASR-0.6B-4bit约0.71GB。下载前读取固定清单并检查实际磁盘余量，不自动给未选择的后端安装模型。

MLX不适用于NVIDIA/Windows。其他环境可以沿用相同分镜、资产约定、Remotion工程与检查方法，但需要选择实际可用的视频/语音后端。API后端的网络、账户和费用取决于已选择的服务；Skill不会创建账户或自带额度。
