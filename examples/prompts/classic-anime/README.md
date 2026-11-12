# classic-anime · 经典日系动画风

清楚线稿、赛璐璐平涂、可读的表情和有目的的简洁动作；适合日常对白、鼓励和情绪反应。

- [《明天，我也在》20秒完整请求](tomorrow-20s.md)：基于一次真实制作整理；新任务仍需重新生成和审看。
- [《这一题，我们慢慢来》12秒完整请求](small-step-12s.md)：入门对白方案，尚未制作该独立影片。
- [原画场景提示词](scene-image.txt)：双人教室原画的场景输入。
- [视频场景提示词](scene-video.txt)：一个4秒讲话近景的场景输入，实际对白由音轨承载。
- [角色配音配置](dialogue-example.json)：可复制到新片`docs/dialogue.json`改写。
- [制作层经验](production-notes.md)：实际提示词、音轨先行和口型修复经验。

初始化命令（替换路径和视频ID）：

```sh
python3 <skill-dir>/scripts/init_project.py --workspace <workspace> --id classroom-story --seconds 20 --style classic-anime
```

选择本地MLX时加`--profile mlx`；默认external只建立通用工程。新片先确定采用配音和自然语速，用实际音轨驱动讲话表演，按本片profile的reviewChecks审看。示例不附带旧音频、原画、模型或验收。
