# 风格参数

初始化支持 `--style classic-anime`（默认）和 `--style handpainted-film`。风格独立于 `--profile mlx/external`：前者决定美术、表演及检查方向，后者选择实际生成后端。

| 参数 | 名称 | 方向 |
|---|---|---|
| classic-anime | 经典日系动画风 | 清晰线稿、赛璐璐平涂、可读的表情与简洁有目的的动作 |
| handpainted-film | 手绘动画电影风 | 水粉/水彩背景、自然光与空间深度，细微表演及与环境连贯的运动 |

可复制的完整请求和制作层场景提示词随包放在[examples/prompts](../examples/prompts/README.md)，两种style各有独立目录。

这两种是可执行的制作方向，不承诺特定导演、影片或模型效果。用户给定的具体角色、色彩、机位和故事优先。不要因为选了风格就自动增加对白、音乐、镜头或人物。导演/电影参考只属于当前影片的brief，不固化为通用参数名称。

## 从参数到制作

初始化器将选定的 `assets/styles/<style>.json` 独立复制到本片 `docs/style.json`，并在 `production.json.style` 和brief登记。完整配置包含 `imagePrompt`、`videoPrompt`、`soundDirection`、`reviewChecks`。

1. 原画：先读本片profile，准备场景提示词，用本片命令组成实际原画提示词，再交给所选图像后端：

   ```sh
   python3 scripts/style_profile.py --kind image --scene docs/prompts/scene-01-image.txt --output docs/prompts/scene-01-image-effective.txt
   ```

2. 连续视频：`run_mlx.py --prompt ...`接收**场景本身**的提示词，自动前置 `videoPrompt`。实际有效提示词、SHA256、style和profile SHA256一并进入生成记录。不要把已组合的视频提示词再输入该包装器以免重复。外部后端可用上述命令的 `--kind video` 组合提示词，并登记同样的style来源字段。
3. 声音：按 `soundDirection` 选择适合本片的环境声、对白和音乐；具体音轨仍需真正制作，不通过风格名称推断已经有声音。
4. 检查：实际审看后逐项记录 `reviewChecks` 的观察。review JSON增加本片profile的 `styleSha256`；修改profile后，旧生成/视觉记录不应继续表示新风格已通过。导出指纹也包含profile。

默认新工程采用classic-anime。没有style字段的旧工程维持原提示词，不主动迁移历史影片。已有工程转换画风需要更新配置、重做原画和对应动画并重新审看；改一个字段不会把旧片自动转换。

## 验证新画风

先做2–4秒完整场景短测，检查原画质感在人物和环境运动中是否保持。handpainted-film尤其检查笔触抖动、背景漂移、过度转头和草木/衣物的风向。静图平移或缩放不能代替连续表演测试。测试结果、候选和限制写在该片目录，不把技术smoke当作风格验收。
