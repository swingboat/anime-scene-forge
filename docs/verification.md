# 本仓库验证记录

## v0.4.1 · 2026-11-12

- 按当前分发要求，将示例统一放在examples/prompts/classic-anime、handpainted-film和shared；新旧入口的Markdown链接均由打包资源测试核对。
- 两种style分别提供完整请求、原画和连续视频场景提示词；classic-anime另有配音JSON，handpainted-film加入海边花山滑板方案与关键动作短测提示词。滑板方案尚未制作。
- 构建器仅将examples/prompts中的Markdown/TXT/JSON纳入包，不递归其他视频目录；增加媒体文件误放时拒绝打包的回归测试。
- `python3 -m unittest discover -s tests -v`：17项通过。运行时未修改，不重复GPU推理或影片导出smoke；之前36项导出检查仍作为v0.4.0记录。
- 交付版本化ZIP、通用名称ZIP及SHA256校验文件。解压后使用整个anime-scene-forge目录；包内不附带模型、原画、音频、影片或历史验收。
- 最终ZIP审计5项通过：单顶层目录/CRC、仅精选文本示例、53个相对Markdown链接全部可解析，以及两种style从解包目录独立初始化、规划校验、原画提示词组合与MLX视频dry-run。没有导入模型或执行推理；报告在`.dist/validation-v0.4.1.json`。

## v0.4.0 · 2026-11-12

- 增加style参数、两套完整profile、本片原画提示词组合工具、MLX实际有效提示词/风格哈希记录、过期生成/风格审看拒绝和导出profile指纹。profile与模型后端独立，不迁移历史影片。
- `python3 -m unittest discover -s tests -v`：16项回归通过，包括handpainted实际dry-run、分发包携带两套profile、非法/不匹配/缺失配置拒绝、无style旧工程兼容。
- `python3 scripts/test_pipeline.py --id pipeline-smoke-v040-20261112 --render`：独立工程36项smoke通过，覆盖新profile拦截、实际MP4导出/完整解码/精确容器时长与ZIP。
- Skill Creator结构校验通过。真实风格样片工程：`examples/hillside-breeze-3s-20261112/`，过程与检查单独记录；smoke通过不表示样片艺术通过。
- 真实handpainted-film单人样片已完成连续I2V：73帧源采用72帧/3秒，生成395.89秒；全部72帧全画面/脸部查看，浏览器1倍速播放至结束。保留多次闭眼和人物横移的观察；原声听感与用户艺术验收仍待确认，样片不证明精确动作控制。

## v0.3.0 · 2026-11-11

本次为本地分发包准备。环境仍为macOS arm64、M3 Pro/18GiB；使用本仓库的源码和独立新建工程，没有同步全局安装或发布远程仓库。

- `python3 -m unittest discover -s tests -v`：12项回归通过。新增分发包内示例/链接/配音配置自洽、AAC尾部修整后画面逐帧一致与语音时点保持、无声导出检查幂等。
- `python3 scripts/test_pipeline.py --id pipeline-smoke-v030-20261111 --render`：34项技术测试通过。新工程位于`examples/pipeline-smoke-v030-20261111/`，独立锁定依赖、缓存、媒体和日志；实际执行候选/正式导出、0.5秒容器检查、完整解码、修改导出辅助脚本后的旧成片拒绝与ZIP校验。
- Skill Creator `quick_validate.py`通过。分发资源测试遍历ZIP中Markdown相对链接，所有目标随包存在；解包后能独立初始化工程。
- 增加可复制的20秒完整请求、12秒入门请求和口型修复请求，以及真实制作层提示词与配音JSON。它们在references内分发；本地视频试验目录不打包。
- 《明天，我也在》真实制作工程使用本机MLX/LTX-2.3 q4/Qwen3-TTS和imagegen，实际生成7个完整候选采用5个、拒绝2个，另1次主动中止，累计视频进程墙钟约55.31分钟；20秒/480帧，内部逐帧、1倍速及技术检查通过，最终混音相关性约0.999962、0采样偏移。无法直接试听，用户艺术验收未自动推定。详细记录在该片工程的制作文档内；此处不附带影片、模型或审批。
- 从真实工程回写OffthreadVideo/Html5Audio预览、Scenes稳定包装组件与AAC尾部修整。新版模板的smoke是技术测试，不把合成图案或脉冲音频当作动漫表演验收。

未验证边界：Claude Code应用内完整生产、Windows/Linux、CUDA/云端、新机器MLX以及多人重叠对白。格式兼容、后端可用、技术检查、内部视觉和用户验收分别表述。

## v0.2.0历史记录

日期：2026-11-11。环境：macOS arm64、M3 Pro/18GiB，Python3.13.4、Node24.13.1、npm11.8.0、FFmpeg7.1.1。

### 已执行

- Skill Creator `quick_validate.py`：通过。
- `python3 -m unittest discover -s tests -v`：9项回归，覆盖初始化的精确帧数/不覆盖/非法参数/路径隔离、可搬移MLX工程、分发包解包后初始化、公共锁文件和脚本语法。
- `python3 scripts/test_pipeline.py --id pipeline-smoke-20261111 --render`：32项技术测试通过。测试工程位于 `examples/pipeline-smoke-20261111/`，有自己的依赖、缓存、素材、源码和日志，没有借用旧视频环境。
- 模板与样例锁文件的295个tarball地址改为公共npm，版本和integrity不变；以公共registry配置重新安装、重新导出和检查。
- 实际导出候选与最终H.264/AAC，1280×720、24fps、12帧、0.5秒；FFmpeg全片解码通过。ZIP CRC及包内成片哈希一致。
- Skill分发包包含运行需要的模板、锁文件、适配器与references；不含examples、仓库文档、tests、模型、缓存或node_modules。解包后可以独立初始化新工程。

### 本次新增的行为检查

1. 匹配实际驱动的A2V记录、源候选和采用片段时可以进入draft检查。
2. 另一份路径不同的候选不能借用原A2V记录，即使文件内容相同。
3. 非零源帧选片需要生成前通过 `--source-start` 补足驱动偏移；改变选片起点会被拒绝。
4. 采用片段与selection记录的路径/哈希不同、旧视觉记录、修改音轨或对白起点、缺失来源时拒绝最终通过。

真实JSON和逐项日志在样例的 `outputs/checks/skill-smoke-report.json`、`export.json`、`package.json`。它们是本地输出，默认不进Git。Git保留样例源码、提示词和来源记录；媒体/环境在本机，重跑用新 `--id`。

### 未验证与声明边界

本次使用合成测试图案与脉冲音频，A2V记录和review明确标记为synthetic，仅覆盖工程机制正负分支。没有为了本轮初始化运行GPU视频/语音推理，没有重看旧动漫，也没有声明新的动漫口型、人物表演或声音相似度已验收。

MLX安装器仅执行计划与命令dry-run；真实推理经验来自历史20/30秒工程。Claude Code应用内完整流程、新机MLX环境、Windows/Linux、CUDA/云端、多人重叠对白仍待实测。格式兼容、技术检查通过、艺术质量和用户验收分别记录。
