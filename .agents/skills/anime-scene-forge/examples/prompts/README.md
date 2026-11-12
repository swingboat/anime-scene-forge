# 按风格选择提示词

这里是随 Skill 分发的纯文本示例库。复制「完整制作请求」给 Agent 即可开始；示例中的角色、故事和时长可改写。Codex使用`$anime-scene-forge`，其他宿主用其支持的调用方式，或明确让Agent阅读已安装目录的SKILL.md。

| style | 入口 | 完整制作请求 |
|---|---|---|
| classic-anime（默认） | [经典日系动画风](classic-anime/README.md) | [20秒双人情绪短片](classic-anime/tomorrow-20s.md)、[12秒短对白](classic-anime/small-step-12s.md) |
| handpainted-film | [手绘动画电影风](handpainted-film/README.md) | [3秒山坡微风短测](handpainted-film/hillside-breeze-3s.md)、[12秒海边花山滑板](handpainted-film/coastal-skateboard-12s.md) |
| 任意既有风格 | [可见对白修复](shared/repair-lipsync.md) | 保留已有配音，修复嘴型与表情 |

每个风格目录也有原画/视频的场景提示词`.txt`，用于执行Agent准备后端输入；不是要求使用者自行操作模型。classic-anime另附角色配音JSON和真实制作经验。

## 使用步骤

1. 先读对应风格的README，再复制一份完整制作请求。明确`style`；改写内容后重新核对时长、台词和镜头。
2. Agent探测实际可用的图像、声音与视频后端，在工作区的`examples/<video-id>/`新建独立工程。`prompts`保留给示例库，不用作视频ID。
3. 风格方向保存在新片`docs/style.json`。场景提示词`.txt`复制到新片`docs/prompts/`后使用；图像提示词通过`style_profile.py --kind image`组合，MLX视频包装器自动组合videoPrompt，避免重复前置。
4. 先做2–4秒关键动作/对白短测，真实审看后扩展。实际影片、模型、音频和历史审批不在示例库内。

制作能力和条件依赖见[依赖说明](../../references/dependencies.md)，参数与检查见[风格说明](../../references/styles.md)，安装位置见[兼容与安装](../../references/portability.md)。格式兼容不代表每个宿主都自带图像工具或本地GPU。
