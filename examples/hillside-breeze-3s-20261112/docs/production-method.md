# 《风起山坡》实际制作记录

日期：2026-11-12。状态：已制作，内部逐帧/播放与技术检查通过，用户艺术验收未确认。风格：handpainted-film。

## 成片

- H.264/AAC，1280×720，24fps，72帧，3.000秒；音视频及容器时长检查通过，完整解码通过。
- 原生连续I2V源为1024×576、24fps、73帧，采用源0–71帧，1倍速，无裁切、冻结、循环、倒放或变速补时。Remotion按原画幅放大交付。
- 最终文件：outputs/final.mp4，SHA256：d33bc3009006141f53a49f43f1d58e8d23fa906c0aa3ef030cf88fb2aa6ebc91。
- 全部源码、素材、独立模型、环境、缓存和日志在本目录。工程ZIP由npm run package生成，排除可重建依赖、模型与缓存。

## 风格参数与实际后端

本片由初始化器使用--style handpainted-film --profile mlx建立。docs/style.json包含原画、视频、声音和检查方向；run_mlx.py实际前置videoPrompt，生成记录保存完整有效提示词及风格/输入/输出哈希。

原画通过内置imagegen生成，未提供既有影片帧或角色。用户要求的宫崎骏电影视觉方向只用于本片原画提示词；通用profile不绑定导演或影片。工具没有暴露具体图像模型版本。实际原画调用提示词为docs/prompts/scene-01-image-tool.txt，归档原图和技术归一化输入均在public/art。宿主要求保留generated_images内原件，运行只使用本片副本，不宣称工具内部缓存已隔离。

连续视频：LTX-2.3 q4，MLX0.32.4/mlx-lm0.32.2，LTX-2-MLX提交747b30ef10e92a011e85b2aa0f6c4ee86ced5218，Gemma3-12b q4。代码/模型修订见docs/mlx-profile.json。M3 Pro/18GiB，Python3.13.9；默认float32、11GiB MLX额度、缓存0，Gemma与连接器顺序加载、提示词缓存及DiT逐块读取。一个GPU任务。

本片模型通过APFS clonefile复制已有本机模型为独立inode文件，没有软/硬链接，没有下载新权重；固定源码重新克隆，.venv重新安装，不读取其他视频的虚拟环境。来源与文件大小/inode检查见outputs/checks/environment-materialization.json。prepare_environment.py为通用显式源目录导入工具，生成时不依赖该来源。npm也在本片独立安装。

## 候选与真实观察

仅生成一个候选scene-01-v1，推理流水线墙钟395.89秒（约6.60分钟），包含文本编码、两阶段去噪、解码与封装，不包括原画、环境准备、审看及导出。

已查看编号full-01至06、face-01至06，覆盖全部72帧的完整画面和脸部。人物栗棕短发、米白衬衣、砖红裙和脸型可辨认一致，水粉背景、暖光与田野层次统一，未见额外人物/文字或明显核心人体错误。头发与前景草木有连续风动，脸部有闭眼与轻微转动。候选在IAB以1倍速、不静音播放至3秒结束，媒体错误为空；候选与最终MP4字节SHA256相同；正式MP4也已在IAB以1倍速、不静音播放至3秒结束，媒体错误为空，见docs/reviews/final-playback.json。

实际表现偏离brief：有多次闭眼，后半段人物向右侧移动，构图不满足严格固定意图，背景细笔触有轻微形变。这些限制保留在review中；作为手绘画风与少量连续运动短测采用，不宣称精确控制镜头/眨眼次数通过，也不由此承诺复杂动作、多人或长片同样稳定。

视觉记录绑定采用片段与style SHA256，技术检查和艺术判断分开。用户验收未自动推定。

## 声音与交付

无对白、无字幕、无配乐。本片脚本make_ambience.py用固定seed合成48kHz立体声PCM16风/草木声，随影片混音。没有使用原电影音乐或原声。代理无法直接试听，环境声自然度和混音听感由用户判断；浏览器不静音播放不等于人耳听感验收。

Remotion初始AAC约8ms尾部填充由本片trim_export.py处理，复制视频码流、仅修整AAC尾部至严格3.000秒，无画面或语速变更。原始导出保留在outputs/intermediate。

独立预览：npm run dev；播放器docs/reviews/player.html（通过本片HTTP服务打开）；制作与检查命令见README。原画、提示词、候选、选片、review和制作记录都属于本片，不随Skill分发包携带。
