# 漫声片场开发约定

本仓库是 anime-scene-forge 的开发源码，以根目录 `SKILL.md` 为制作入口。
开始改动前阅读 `docs/requirements.md`；追溯依据见 `docs/conversation-review.md`。

- Skill 的通用指令放 `SKILL.md`，按需说明放 `references/`，可复制运行时放 `assets/`，维护与初始化工具放 `scripts/`。
- 每个测试视频创建 `examples/<video-id>/`，一个视频一个子目录。使用 `scripts/init_project.py`；禁止覆盖已有工程。
- 当前视频自己的源码、依赖、模型、素材、缓存、日志和输出全部放在该子目录。运行时不能依赖另一个视频、根目录的 node_modules 或已安装 Skill；复用时复制独立文件，不使用软/硬链接。
- 在视频目录运行安装、生成、预览、检查与导出。系统工具可复用；工具无法配置的临时输出及时归档，记录真实限制。
- 可见对白先定声音、情绪及自然语速，再用同一音轨驱动连续表演。先验证2–4秒关键片段；技术测试不替代逐帧与1倍速视觉检查，不自动填写艺术审批。
- 区分已制作、内部检查通过、用户验收。不要把历史作品验收当成本模板或其他宿主已完整验证。
- 根目录和模板的脚本有改动时，运行 `python3 -m unittest discover -s tests -v`。影响剪辑/音轨/导出时，按 README 在独立 example 运行完整 smoke 流程。
- `examples/prompts/<style>/`是随Skill分发的纯文本提示词库；`examples/<video-id>/`是本地视频试验工程，不进入分发包。构建器只允许examples/prompts中的Markdown、TXT和JSON，不能递归打包整个examples。用 `scripts/build_skill.py` 构建分发包。不要自动同步全局安装、下载模型或发布远程仓库。
