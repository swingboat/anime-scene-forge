# 漫声片场 · Anime Scene Forge

把角色、场景、声音与连续表演做成可编辑、可预览和可导出的二维动漫叙事短片。
适合少角色的短对白、鼓励、情绪反应和简单动作；可见角色先确定配音与情绪，再以实际音轨驱动画面。

本仓库从 video-creation 的《灌篮高手》樱木与晴子会话及 v0.1 技能源码迁入维护。[会话复核](docs/conversation-review.md)记录问题和修复，[需求](docs/requirements.md)记录当前目标与验收条件。

## 使用

让 Agent 阅读根目录 [SKILL.md](SKILL.md) 后制作视频。当前仓库开发时以此文件为准；已安装的旧版技能不会自动与源码同步。

想直接试用，打开随包的[风格提示词库](examples/prompts/README.md)：`classic-anime`有20秒故事和12秒对白；`handpainted-film`有3秒山坡微风和12秒海边花山滑板。两种风格均附原画/视频场景提示词，另有配音配置和通用口型修复请求，使用者可直接复制完整请求。

```sh
python3 scripts/doctor.py --workspace .
python3 scripts/init_project.py --id school-gym-30s --seconds 30 --title "放学后的球馆" --profile mlx --style classic-anime
cd examples/school-gym-30s
npm ci --cache .cache/npm
npm run check:source
npm run dev
```

默认初始化到 `examples/<video-id>/`，不安装依赖、不下载模型、不覆盖已有目录。无需本地 MLX 时省略 `--profile mlx`，按后端约定准备素材。已有工作区可显式用 `--collection videos`。

`--style`提供两套方向：`classic-anime`（默认，经典日系动画风）与`handpainted-film`（手绘动画电影风）。配置独立复制进本片`docs/style.json`，用于原画提示词、实际视频生成、声音设计和视觉检查；与后端参数`--profile`独立。[风格使用说明](references/styles.md)。

```sh
python3 scripts/init_project.py --id hillside-breeze --seconds 3 --style handpainted-film --profile mlx
```

随后在该视频内完善 `docs/brief.md`、`production.json`，选择实际可用的原画、语音与视频后端，按本片 README 制作。候选与采用片段分开保存，镜头先逐帧、1倍速审看，再进行正式导出：

```sh
npm run render:draft
npm run render
npm run check
npm run package
```

每个视频拥有独立源码、锁文件、素材、模型、缓存和输出。MP4 在该片 `outputs/final.mp4`，工程包在 `outputs/project.zip`。详见 [examples 规则](examples/README.md)。

## 开发与验证

根目录维护 Skill；`assets/project/` 是独立 Remotion 模板，`assets/mlx/` 是可选固定版本适配器，`references/` 是按需技术说明。修改模板后，新建视频获得新版本，已存在的视频保留自己的副本。

```sh
python3 -m unittest discover -s tests -v
python3 scripts/test_pipeline.py --render
python3 scripts/build_skill.py
```

`test_pipeline.py` 每次建立一个新的 `examples/pipeline-smoke-<时间>/`，安装该片锁定 npm 依赖，使用半秒合成图案/脉冲音频测试驱动、原速选片、来源、负向拦截、导出、解码和 ZIP；不下载模型或运行 GPU。只检查 Python/FFmpeg 路径时可省略 `--render`。需要可重复的固定名称时传 `--id`，重跑须换新目录名。

分发包输出 `.dist/anime-scene-forge.zip`，包含SKILL、元数据、references、scripts、assets和`examples/prompts/`纯文本提示词库。构建器不遍历其他视频试验目录，不携带影片、模型、环境或缓存。版本化ZIP和SHA256校验文件也可用于分发；安装整个anime-scene-forge文件夹，方法见[portability](references/portability.md)。

## 验证范围

实际执行与限制见 [本仓库验证记录](docs/verification.md)。本机已使用复制到独立工程的 MLX 适配器制作《明天，我也在》20秒短片；其内部视觉、技术检查与用户验收分别记录。v0.4.0增加风格参数，独立短测位于`examples/hillside-breeze-3s-20261112/`，以该片实际记录为准。Claude Code 应用内端到端、Windows/Linux、CUDA/云端仍未实测；工程测试不代表新动漫表演通过艺术验收。
