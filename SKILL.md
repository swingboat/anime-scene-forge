---
name: anime-scene-forge
description: "Create or repair short 2D anime narrative videos with consistent characters, continuous acting, dialogue-driven lips and expressions, captions and Remotion delivery. 适用于少角色的日常互动、鼓励、情绪反应和简单动作；不用于纯轮播、通用动态图表或保证复杂比赛与精确原声复刻。"
metadata:
  version: "0.4.1"
---

# 漫声片场 · Anime Scene Forge

把角色、场景、声音和表演做成一段可独立预览、检查和导出的二维动漫短片。先确定用户要的内容与交付形式；明确要求优先于本 Skill 的默认路线。

## 直接试用

需要可复制的完整请求时，打开随包的[风格提示词示例](examples/prompts/README.md)：`classic-anime/`包含20秒双人故事、12秒短对白、原画/视频场景提示词和配音配置；`handpainted-film/`包含3秒山坡微风与12秒海边花山滑板、原画/视频及滑行短测提示词。已有影片修复见[对白口型修复](examples/prompts/shared/repair-lipsync.md)。只阅读与当前任务有关的示例；角色、场景和镜头数量都是示例选择，不是固定要求。

## 选择任务与后端

- 优先处理约10–60秒、1–3个主要角色、以对白/情绪/简单动作为主的短叙事；已验证的成片案例为20和30秒。长时长、复杂接触和高速运动需要先验证关键动作。具体边界见 [scope.md](references/scope.md)。
- 阅读 [dependencies.md](references/dependencies.md)，把“Agent 能读这个 Skill”和“当前环境能运行某个生成后端”分开。核心指令不依赖某个 Agent 的工具名、MCP 或 API 密钥。
- 盘点图像生成或参考原画、语音来源、连续视频生成、命令执行、图片查看与视频播放能力。运行 `python3 <skill-dir>/scripts/doctor.py --workspace <workspace>` 辅助检查；宿主的图像/浏览器工具仍由 Agent 自己发现。
- 本包提供已验证路线的 Apple Silicon / MLX 适配器；阅读 [mlx-profile.md](references/mlx-profile.md) 后使用。其他后端按 [backend-contract.md](references/backend-contract.md) 接入，不能宣称未经测试的 CUDA/云端实现已可用。缺少能力时继续完成不依赖它的分镜、提示词和工程；明确指出缺少的工具或授权。

## 建立当前视频的独立工程

先建立 `examples/<video-id>/`，一个视频一个子目录，在该目录进行后续安装、生成和导出。可运行：

```sh
python3 <skill-dir>/scripts/init_project.py --workspace <workspace> --id <video-id> --seconds 30 --style classic-anime
```

默认集合为 `examples/`。用户已有工作区采用其他集合时用 `--collection <目录名>` 显式选择，例如 `--collection videos`；尊重本次指定的位置。

`--style`支持`classic-anime`（默认，经典日系动画风）和`handpainted-film`（手绘动画电影风）。制作前读本片`docs/style.json`，按其原画、视频、声音和检查方向执行；具体用法见[styles.md](references/styles.md)。风格与生成后端`--profile`独立，用户的具体美术要求优先。

初始化器复制独立的 Remotion 工程与辅助脚本。所有资源、锁文件、虚拟环境、下载模型、缓存、临时文件和输出留在本视频目录。复用素材时复制为本地文件；视频运行时不读取其他视频目录或已安装 Skill 的文件。`node_modules`、模型和虚拟环境不进入交付ZIP。

用 `production.json` 描述镜头、帧数、素材和声音；`docs/brief.md` 写清人物、场景、参考来源、风格、时长、语言、对白模式和交付要求。根据故事修改默认分段，不把初始化器的等长分段当成分镜。若用户已有工程，先检查其约定再修改，不初始化覆盖它。

## 制作与迭代

1. **统一视觉身份。** 固定造型、完整场景、透视、线条、色彩、光向和角色间距；使用当前可用的图像工具或合适的已提供原画。角色、配角和观众都纳入场景设计。保留提示词、参考来源和输入哈希。
2. **先确定可见对白的声音。** 确定文本、声线、情绪和正常语速，用实际角色音轨驱动画面。画外旁白、无对白和不需要对嘴的角色按其叙事需要处理。详见 [dialogue-and-qa.md](references/dialogue-and-qa.md)。
3. **先做2–4秒关键表演。** 用整幅场景连续图生视频；讲话镜头用含真实静音时段的独立对白驱动。一个镜头围绕一个主要动作，明确说话者、倾听者及其他人的反应。单人镜头谨慎命名画外人物，避免引入额外角色。
4. **检查后再扩展。** 查看完整画面和逐帧脸部、手脚、握持、关键接触与正常速度表现；核对说话前、停顿与说完后的嘴部、眉眼和视线。短样片是内部检查，不新增逐镜头向用户确认的流程。
5. **有依据地重试。** 保留失败候选，每次调整原画、约束、提示词或机位。提前张嘴、转头变形可用干净的闭口/收尾参考后重做；核心人体或物体错误不能靠边缘裁切解决。同类错误重复出现时改变方案，结合任务已有时间/费用约束，避免无界重试。
6. **按1倍速选片与合成。** 记录连续源帧范围；慢动作只用于用户要求或明确表达目的。素材不足补有叙事作用的镜头。固定数量、轨迹和接触明确的物体可用匹配画风的程序合成，重新校准遮挡和声音。重生成动作后以采用画面重标拍手等事件。

在当前视频内执行 `npm run dev`，通过可用的浏览器/播放器展示工程并检查。可用 `python3 scripts/project_ops.py sheet <shot-id>` 生成逐帧检查图。只有实际做过视觉检查后，才填写 `docs/reviews/` 记录（含本片`styleSha256`与风格检查观察）并将镜头标为 `approved`；脚本生成成功不等于视觉通过。

## 完成交付

- 需要审核成片时先用 `npm run render:draft` 输出候选；按1倍速播放并检查关键动作与交接。最终导出使用 `npm run render`，它拒绝缺少素材、对白驱动不一致或没有对应视觉记录的镜头。
- 运行 `npm run check`，核对锁定依赖、路径隔离、时长、帧数、音视频解码、音轨位置和文件哈希。技术分数不代替逐音素口型与表情的视觉检查；工具不能听音时如实记录。
- 按用户要求提供预览、MP4或工程包；需要工程包时运行 `npm run package`。README 给出独立安装、预览、修改声音/素材/时间轴、检查和导出的命令。
- 在本片 `docs/production-method.md` 记录实际后端/版本、失败候选、修正、耗时、检查范围和限制。分别表述“已制作”“内部检查通过”和“用户已验收”。

迁移到其他 Agent 的安装位置与能力映射见 [portability.md](references/portability.md)。本包的测试范围和未验证部分见 [validation.md](references/validation.md)。
