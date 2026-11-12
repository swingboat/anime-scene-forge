# 《明天，我也在》：制作层提示词与实际经验

这是给执行 Agent 的可选参考。用户可以只复制[完整制作请求](tomorrow-20s.md)，不必自行编写下面的后端提示词。这里的模型、声音设计与 guide 时点属于一次实际任务，不能当作所有任务的固定配置。

## 原画：先定场景，再派生近景

主场景提示词示例：

```text
An original Japanese 2D hand-drawn anime film keyframe, landscape 16:9.
After school in a quiet empty classroom, soft sunset light from the windows on the left.
Two teenage friends sit at adjacent wooden desks, visible from the waist up.
On the left, Xiaxia has a black shoulder-length bob, dark brown eyes, a light blue knit cardigan and a cream top. She looks down, mouth closed, quietly disappointed, hands resting naturally on her desk.
On the right, A-Qing has a dark chestnut high ponytail, amber-brown eyes and a white collared blouse. She looks kindly toward Xiaxia, lips closed, calmly listening.
Clean fine linework, restrained expressions, flat-shaded faces, a soft painted background, muted blue shadows and warm gold light. Stable anatomy, no extra people, no lettering or panels.
```

近景沿用主图作身份与环境参考，而不是重新独立设计。提示词明确要哪一个人、看向哪侧、同一个座位和光向，保留嘴部可见和适当头顶空间。例如阿晴：

```text
Use the established two-shot as a strict identity and environment reference.
A single close-up of A-Qing, the high-ponytail girl from the right-side desk.
Keep her exact facial identity, brown high ponytail, amber eyes, white blouse, seated position and sunset shading. Her face remains three-quarter toward screen left, looking at her offscreen friend, with a calm closed-mouth smile. Same classroom and linework, no other person visible.
```

## 配音：角色配置与情绪分别保存

可以把[dialogue-example.json](dialogue-example.json)复制到新视频的`docs/dialogue.json`，再按所选语音后端使用或改写。它包含两种声线描述、固定seed、五句原文及逐句情绪。相同seed有助于重现一次配置，不保证每次或每个模型的声线完全一致。

本次实际原速五句约3.44/2.48/1.60/2.40/2.56秒。新模型或新声线需要重新测量，不复用这些时长。文字辅助转写只核对台词，不能证明听感与口型通过。

## A2V：描述表演，让实际音轨承载对白

下面是本次承诺近景采用版的实际画面提示词；对白全文另存在音频和对白配置中：

```text
A continuous cinematic four-second Japanese 2D hand-drawn anime close-up of the same seated teenage girl, dark chestnut high ponytail, amber eyes, white collared blouse. Same classroom, warm sunset from the left, fixed camera, normal speed. She looks gently toward screen left and makes a quiet reassuring promise in Mandarin, matching the supplied audio precisely with small natural opening and closing lip movements. She keeps her lips closed during the initial silence and the sentence pause. One tiny confident nod, stable eyes, calm affectionate expression. When the audio ends, her lips close into a restrained smile while she breathes naturally. Preserve the original face and hairstyle. Clean unlettered image throughout, with a plain blouse and background. Only one person.
```

本次首版将完整台词写入较长画面提示词，出现了无关英文样文字；简化表演描述并保留实际音轨，重做后消失。这是对该候选的修正，不是禁止其他后端在提示词中写对白。

开口约束使用实际波形与逐帧画面决定。本次承诺镜语音第8帧附近开始，闭口guide放在第6帧，另在第72帧约束收尾；鼓励镜首版提前约0.29秒开口，重做时把guide放到两段语音前。换句子、声音、起点或源帧范围后，必须重新标定，不能照抄这些帧号。

告别镜的起始参考提取自本片前一镜的闭口期待画面，再生成微笑收尾参考，最后重新A2V生成连续画面。参考帧不是拿来冻结或循环补时的片段。

## 检查与交付边界

本次7个完整候选采用5个、拒绝2个，另1次主动中止；视频进程累计约55.31分钟。完成了逐帧、1倍速及技术检查，代理无法直接试听，用户艺术验收仍待确认。这些数字只说明本次任务，不是新任务的速度或质量承诺。

原画、WAV、模型、原始候选与成片属于制作工程，不随 Skill 包分发。其他使用者按自己的后端重新生成并检查。
