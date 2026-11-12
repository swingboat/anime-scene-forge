# 手绘动画电影风 · 三秒短测

用于体验`handpainted-film`及检验新原画在连续运动中能否保持画感。可复制：

```text
使用 $anime-scene-forge，制作一个3秒的手绘动画电影风样片，style选择handpainted-film。
原创乡间山坡场景：栗棕短发少女穿米白衬衣、砖红裙，面向田野感受轻风，轻微抬头后闭口微笑，头发、衣角与前景草木顺风轻动。
16:9，1280×720，24fps，72帧，一个连续镜头；画面保留细腻水粉背景、自然午后光和清楚的人物线稿。
无对白、无字幕；用轻微环境风声营造空间感。
在examples下新建独立子目录，先做完整场景原画，再真实连续I2V。不要用静图平移替代动画。
检查全部帧和1倍速表现，记录画风、人物/背景稳定性及实际动作与要求的偏差，交付MP4和独立工程。
```

初始化参数示例：

```sh
python3 <skill-dir>/scripts/init_project.py --workspace <workspace> --id hillside-breeze --seconds 3 --style handpainted-film --profile mlx
```

`--profile`按实际环境选择，风格参数不等于模型能力。真实短测观察到多次闭眼与后半段人物横移，因此这类问题要写入候选记录；新任务是否可用由实际审看决定，不直接沿用历史审批。详细风格配置与提示词组合见[风格说明](../../../references/styles.md)。
