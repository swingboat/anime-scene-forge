# handpainted-film · 手绘动画电影风

细腻水粉/水彩背景、自然光与空间层次、克制的人物表演，以及相互连贯的头发、衣物和草木运动。

- [《风起山坡》3秒完整请求](hillside-breeze-3s.md)：基于真实风格短测整理。原片有多次闭眼和人物横移，限制已记录；新任务须重新审看。
- [《海风里的滑板》12秒完整请求](coastal-skateboard-12s.md)：对应临海花山、柏油路和小女孩滑板场景；此方案尚未制作，须先验证脚/滑板/地面接触。
- [山坡原画场景提示词](scene-image.txt)与[连续视频场景提示词](scene-video.txt)：供Agent组合后端输入。
- [滑板关键动作提示词](skateboard-test-video.txt)：用于2–4秒滑行短测，不能替代真实动作检查。

初始化命令（替换路径和视频ID）：

```sh
python3 <skill-dir>/scripts/init_project.py --workspace <workspace> --id hillside-story --seconds 3 --style handpainted-film
```

本地MLX需加`--profile mlx`并具备相应硬件与环境。先检查手绘纹理是否抖动、背景是否漂移、人物身份和物体接触是否稳定，再扩展时长。导演或电影参考可写在当前影片的brief中，不是通用style必须绑定的内容。
