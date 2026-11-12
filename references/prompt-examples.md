# 可直接复制的提示词示例

完整提示词已按style整理在随包的[examples/prompts](../examples/prompts/README.md)。安装Skill并准备好可用的图像、语音和视频后端后，复制对应示例中的「可复制请求」整段给Agent。示例不自带模型、音色、原画或成片；实际耗时和效果取决于后端。能力与安装说明见[dependencies.md](dependencies.md)和[portability.md](portability.md)。

| 想做什么 | 示例 |
|---|---|
| classic-anime双人情绪短片 | [《明天，我也在》：20秒、5镜、普通话](../examples/prompts/classic-anime/tomorrow-20s.md) |
| classic-anime短对白 | [《这一题，我们慢慢来》：12秒、3镜](../examples/prompts/classic-anime/small-step-12s.md) |
| 任意风格的可见对白修复 | [保留配音、重做口型和表情](../examples/prompts/shared/repair-lipsync.md) |
| handpainted-film背景与细微运动 | [3秒山坡微风](../examples/prompts/handpainted-film/hillside-breeze-3s.md) |
| handpainted-film花山、大海与滑板 | [12秒海风里的滑板](../examples/prompts/handpainted-film/coastal-skateboard-12s.md) |

Codex 可使用 `$anime-scene-forge`，其他宿主用其支持的调用方式，或明确让 Agent 读取已安装目录的 `SKILL.md`。工程目录已经存在时换一个新名称，修复任务则检查并保留现有工程。

改写故事时，优先替换片名、角色造型、场景、台词与情绪，再核对时长和帧数。保留声音先行、实际音轨驱动、2–4秒短测、原速选片和检查记录等制作约束。

需要了解Agent如何拆分原画、配音和连续表演时，再看[《明天，我也在》的制作层经验](../examples/prompts/classic-anime/production-notes.md)。它引用真实制作经验，不能直接复用旧片帧号或当作新片验收。原references/prompt-examples中的Markdown入口保留为跳转，完整内容统一维护在examples/prompts。
