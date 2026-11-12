# Agent兼容与安装

本包使用Agent Skills的目录结构：SKILL.md（name/description及正文）、按需references、Python脚本和可复制模板。没有Claude专用的allowed-tools/context/fork字段，也没有必须存在的Codex工具名称。agents/openai.yaml只提供可忽略的UI元数据。

## 安装同一个文件夹

| 宿主 | 官方本地目录示例 | 调用示例 |
|---|---|---|
| Codex | 用户级~/.agents/skills/anime-scene-forge/；项目级.agents/skills/anime-scene-forge/ | 使用$anime-scene-forge |
| Claude Code | 用户级~/.claude/skills/anime-scene-forge/；项目级.claude/skills/anime-scene-forge/ | /anime-scene-forge |
| 其他兼容Agent | 该宿主文档中的Skills目录 | 按宿主名称调用或明确让Agent读取SKILL.md |

本包是可独立维护的技能源码。原v0.1曾放在创作者的~/.codex/skills，当前开发版本由源码仓库维护；不要据此推断所有Codex版本都自动扫描创作位置。开发时可明确让Agent读取当前仓库的SKILL.md；分发时按目标宿主支持的目录安装ZIP中的整个anime-scene-forge文件夹。不要只复制SKILL.md而丢掉脚本与资源。不同宿主的账户云同步/沙箱与本地技能发现范围可能不同。

路径参数中的<skill-dir>由Agent根据本次读到的SKILL.md真实位置解析，不使用宿主专属变量。初始化后模板与适配器复制进视频工程，运行时不依赖安装目录。本包不修改其他Agent配置，也不创建/发送账户凭证。

示例里的python3指Python3.10+解释器；Windows可用python或py -3运行这些脚本。Node包装器会寻找python/python3，必要时将PYTHON_BIN设为实际解释器路径。清单中的文件路径统一使用正斜杠，ZIP成员也使用跨平台路径格式。

## 能力不等于宿主名称

Codex、Claude Code都可理解指令、编辑文件和调用可用命令，但图像生成、GPU、声音与浏览器权限由实际环境提供。Claude Code可通过已接入服务、CLI或现成原画完成图像阶段；不假设它自带另一个宿主的图像工具。MLX需要Apple Silicon，与使用哪个Agent无关。

兼容声明：格式与核心脚本按通用接口设计；本次实际执行测试在Codex宿主的macOS环境完成，未运行Claude Code应用内的完整生产测试。Agent兼容与后端硬件验证分别记录。

核对日期：2026-11-11。官方依据：[Agent Skills规范](https://agentskills.io/specification)、[Codex本地技能目录](https://learn.chatgpt.com/docs/build-skills)、[Claude Code技能目录](https://code.claude.com/docs/en/skills)。以上只支撑格式与发现路径，不保证图像/视频后端可用。
