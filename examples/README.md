# 视频测试工作区

需要可直接复制的制作请求，先看随分发包提供的[风格提示词库](prompts/README.md)：[classic-anime](prompts/classic-anime/README.md)、[handpainted-film](prompts/handpainted-film/README.md)。`prompts/`是保留的文本示例目录，其余视频工程按下面规则独立创建。

**一个视频一个子目录**：`examples/<video-id>/`。每个子目录都是可独立安装、预览、导出和打包的 Remotion 工程；不能依赖其他视频或根目录 node_modules。

在仓库根目录新建视频：

```sh
python3 scripts/init_project.py --id school-gym-30s --seconds 30 --title "放学后的球馆" --profile mlx
```

不选本地 MLX 时省略 `--profile mlx`，使用默认 external 并按后端约定提供真实素材。初始化只复制源码，不安装依赖、不下载模型、不生成视频。

风格默认为`--style classic-anime`（经典日系动画风），可用`--style handpainted-film`选择手绘动画电影风。两种都复制完整风格配置到本片，按配置制作原画、连续表演、声音并审看。`hillside-breeze-3s-20261112/`为后者的原创三秒连续动画短测，完成情况与限制见本片制作记录。

进入 `examples/school-gym-30s/` 后按它的 README 制作。所有原画、配音、候选、模型、缓存、检查及最终 MP4/ZIP 均留在该视频目录。默认 Git 只跟踪源码和文档；大媒体 `public/`、输出、环境和缓存留在本地。

`pipeline-smoke-20261111/` 是半秒合成图案与音频的工程测试，不是动漫表演样片。其 synthetic review 只用于测试技术拦截，不能作为艺术质量认证。
