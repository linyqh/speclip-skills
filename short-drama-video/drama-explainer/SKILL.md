---
name: drama-explainer
description: 制作“解说配音 + 原片高张力片段穿插”的短剧解说成片技能。适用于短剧二创、剧情解说、狗血短剧混剪、情绪冲突型剧情拆解、影视解说口播成片等场景；当用户希望从短剧原片直接产出可剪辑脚本、解说配音、分镜数据和最终成片时应触发。尤其适合“保留原片最有戏的台词和表演，再用解说串联剧情”的任务。不要在普通剧情总结、影评、纯文案改写、纯字幕烧录、普通视频剪切中使用本技能。
---

# 短剧解说工作流

## 核心定位

这个 skill 不是“把剧情讲清楚”就结束的摘要器，而是一个**短剧解说成片编辑器**。

它的核心任务是：
- 先正确理解剧情、人物和情绪链条
- 再从原片里挑出**最有表演张力、最有羞辱感、最有反击快感、最能立住人物**的原台词
- 最后用克制的解说把这些高张力片段串成一条节奏清晰、代入感强的成片时间线

如果最终结果只是“信息对了，但不好看、不够狠、没记忆点”，那就是失败。

## 成功标准

只有同时满足以下条件，才算成功：

1. **剧情准确**：人物关系、关键事件、时序推进准确
2. **戏眼命中**：真正最有戏的原片段被优先保留，而不是只选“能说明剧情”的台词
3. **解说克制**：解说只负责铺垫、转场、补信息，不复述原片已经说清楚的内容
4. **情绪完整**：成片保留关键情绪链条，例如：羞辱 → 反抗 → 落难 → 安慰 → 反转 → 站队
5. **结构可执行**：`storyboard.json` 可直接用于配音、匹配、裁切、拼接

## 失败信号

出现以下任一情况，都说明 skill 执行失败，需要返工：

- VO 文案充满空泛短视频腔，比如“命运”“站稳”“移不开眼”这类万能包装词，但缺少人物感
- 选中了“能讲明白剧情”的原片，却漏掉了真正最有表演张力的片段
- 只保留结果，不保留羞辱、反抗、护子、护妻、转折等关键戏眼
- `original` 段的 `text` 写成摘要标签，而不是真正要展示的台词
- 同一 source 时间乱跳却没有明确钩子前置策略
- `voiceover` 紧挨着复述 `original` 刚说完的信息，造成“台词听两遍”

## 核心原则

- **检索优先定位戏眼，视觉复核补足表演信息**：先用 `videoindex` / `videosearch` 缩小范围，再用视觉判断补足 transcript 看不见的表演强度
- **校验先行**：人物关系和剧情理解未经校验，不得进入文案步骤
- **文案分两步处理**：步骤 5 只写顺 `draft_script.md`；步骤 6 才做剪辑化编辑
- **`storyboard.json` 为唯一真相源**：步骤 6 开始，所有分镜、音频、时间和输出状态都只回写它
- **原片戏眼优先**：优先保留最有戏的原片，不优先保留最“完整”的原片
- **向量检索先召回，人工再定稿**：先用 `videoindex` / `videosearch` 缩小候选戏眼范围，再结合 transcript 与定向视觉复核做最终编辑判断
- **VO 必须克制**：VO 不能抢原片的戏，不能把原片最强台词提前讲掉
- **按情绪推进，不只按信息推进**：一条成片线必须同时考虑剧情信息和情绪抬升
- **时间不重叠**：同一 `source_index` 下所有最终使用时间段不能重叠
- **渲染只读 `storyboard.json`**：裁切、拼接、交接都不再依赖别的片段真相文件

## 工具清单

| 阶段 | 工具 | 用途 |
|------|------|------|
| 分析 | `qwenasr` | 提取原片对话字幕和时间戳 |
| 分析 | `mediainfo` | 获取视频元数据 |
| 检索 | `videoindex` | 为原片建立向量索引，供后续戏眼召回和画面匹配使用 |
| 检索 | `videosearch` | 用自然语言召回高张力候选片段，缩小编辑搜索范围 |
| 视觉 | `doubaovision` | 对候选片段、疑难节点或弱字幕段做视觉复核；只有在必要时才上升到全片分析 |
| 编辑 | subagent / TaskTool | 为步骤 6 派发专门的 dramatic editor 子任务 |
| 匹配 | `videosearch` + 视觉复核 | 为 `voiceover` 段匹配能承载情绪的画面，必要时再做视觉复核 |
| 生成 | `voiceover` | 生成解说音频 |
| 剪辑 | `trimvideo` | 按分镜截取原片 |
| 合成 | `FFmpeg` | 标准化、拼接、输出最终成片 |

## 项目目录结构

```text
<项目名>/
├── analysis/
│   ├── transcript.json / transcript_01.json
│   ├── mediainfo.json / mediainfo_01.json
│   ├── visual_analysis.json / visual_analysis_01.json
│   ├── plot_analysis.md
│   ├── characters.md
│   ├── retrieval_candidates.json     # 可选检索候选快照
│   └── scene_matching.json          # 可选审查快照
├── scripts/
│   ├── draft_script.md
│   ├── storyboard.json              # 唯一真相源
│   ├── final_script.md              # 从 storyboard 派生的审查稿
│   └── voiceover.md                 # 从 storyboard 派生的 TTS 稿
├── audio/
├── clips/
│   ├── raw/
│   └── merged/
├── output/
│   └── output.mp4
└── state.json                       # 仅记录进度/运行状态
```

## 文件职责

| 文件 | 角色 |
|------|------|
| `draft_script.md` | 连续可读的原始解说稿，只负责把故事讲顺 |
| `storyboard.json` | 分镜主数据，记录每段模式、素材来源、时间、文案、音频策略、状态 |
| `final_script.md` | 从 `storyboard.json` 派生的人类审查稿 |
| `voiceover.md` | 从 `storyboard.json` 派生的 TTS 文案稿 |
| `retrieval_candidates.json` | 步骤 3.5 的可选检索候选快照，只用于审查和回放检索过程 |
| `scene_matching.json` | 步骤 8 的可选审查快照，不是新的真相源 |
| `state.json` | 运行状态，不保存片段真相 |

## 工作流程

### 步骤 0：项目初始化

1. 创建项目目录结构
2. 初始化 `state.json`：只保存 `project`、`progress`、`last_error`
3. 初始化 `scripts/storyboard.json`：先写空壳
   - `project.name`
   - `project.created_at`
   - `sources`
   - `draft_script_path = "scripts/draft_script.md"`
   - `segments = []`
   - `output.final_video = null`

**产出**：项目目录 + `state.json` + `scripts/storyboard.json`

### 步骤 1：分析原片

对每个原片独立执行：
- `qwenasr` → `analysis/transcript*.json`
- `mediainfo` → `analysis/mediainfo*.json`

要求：
- 多源不合并处理
- transcript 必须保留时间戳和说话人标识
- 将原片路径、字幕路径、transcript 路径、时长写入 `storyboard.json.sources[]`

**产出**：`transcript*.json`、`mediainfo*.json`

### 步骤 1.5：建立向量索引

> 在具备 `videoindex` / `videosearch` 的环境里，这一步应视为默认流程。

对全部原片执行一次 `videoindex`：
- 默认用当前项目配置的后端；若无明确要求，可优先使用默认后端
- `shot_threshold` 以可召回戏眼为先，不要一上来就设得过高
- 目标不是一步切出最终片段，而是为后续“找羞辱 / 找反击 / 找安慰 / 找站队”建立可检索底座

要求：
- 只为当前项目原片建索引，不混入无关素材
- 同一批素材只建一次索引；后续步骤直接复用
- 若用户已明确给出更适合的粒度，再调整 `shot_threshold`

**产出**：本地视频向量索引

### 步骤 2：初步剧情分析

基于全部 transcript 梳理：
- 人物关系
- 剧情阶段
- 关键冲突节点
- 疑似高张力片段

这一步只建立剧情骨架，不做最终选段决策。

**产出**：`analysis/plot_analysis.md`（初步版）

### 步骤 3：定向视觉复核（默认按需触发）

`doubaovision` 默认**不是**从头到尾扫完整部片子的必跑步骤。

优先做法是：
1. 先用 transcript 建立剧情骨架
2. 再用 `videosearch` 召回高张力候选
3. 最后只对这些情况做视觉复核：
   - 候选很多，难以判断哪段更有戏
   - transcript 能说明剧情，但看不出表演强弱
   - 需要判断无台词 / 少台词画面是否值得保留
   - 检索结果语义相关，但怀疑“有信息没戏”
   - 字幕质量差，单靠 transcript 不够可靠

只有在下面情况之一，才升级为**全片视觉分析**：
- 字幕严重缺失或 ASR 质量差
- 画面表演价值远高于对白信息
- 题材里存在大量无台词冲突、动作、眼神戏
- 已经发现检索召回明显漏掉关键戏眼，且原因来自字幕不足

复核时重点回答：
- 候选里哪一段真的更有戏
- 哪些地方只是信息说明
- 哪些片段靠表情、停顿、场面就很能打人

若执行本步骤，可产出：`visual_analysis*.json`

### 步骤 3.5：召回高张力候选片段

基于步骤 2 的剧情骨架，用 `videosearch` 做候选召回；如步骤 3 已运行，再把视觉判断作为复核依据。

优先检索这些类型的 query：
- 羞辱 / 贬低 / 当众难堪
- 反抗 / 掀桌 / 顶嘴 / 打脸
- 护子 / 护妻 / 站队 / 公开撑腰
- 落难 / 安慰 / 心碎 / 求婚 / 反转

要求：
- 每类情绪至少改写 2-3 种 query，避免只搜一个表述
- 检索结果只是候选，不是最终入选片段
- 必须先回到 transcript 校验台词和时间；只有在表演强度、场面价值或无台词画面存在歧义时，再调用视觉复核
- 如需留审查痕迹，可导出 `analysis/retrieval_candidates.json`

**产出**：候选时间段集合（可选落盘 `analysis/retrieval_candidates.json`）

### 步骤 4：校验与人物建档

将步骤 2 与步骤 3.5 的检索结果交叉校验；若步骤 3 已运行，再一并吸收视觉修正，产出统一剧情基线：
- 修正人物身份、关系、时序和场景理解
- 产出 `characters.md`
- 覆盖更新 `plot_analysis.md`

必须向用户展示：
- 人物列表
- 剧情五段式摘要
- 可疑点 / 修正点

用户确认无误后才能进入步骤 5。

**产出**：`characters.md`、校验后的 `plot_analysis.md`

### 步骤 5：创作解说文案初稿

> 本步骤只做一件事：**把故事讲顺**。

基于 `plot_analysis.md` 和 `characters.md` 产出 `draft_script.md`。

要求：
- 可以略长，但必须顺
- 不提前拆分 `mode`
- 不提前写时间点
- 不抢戏，不硬写“爽点文案”
- 人物称呼和关键事件必须与 `characters.md` 一致

禁止：
- 直接写成最终剪辑稿
- 提前决定所有 `original` / `voiceover`
- 用夸张包装词替代真实人物状态

**产出**：`draft_script.md`

### 步骤 6：dramatic editor 子任务 — 创建最终分镜脚本

> 这是质量最高优先的核心步骤。

主代理必须先准备最小上下文包：
- `characters.md`
- `plot_analysis.md`
- `draft_script.md`
- `transcript*.json` / 对应 SRT
- 必要时补充 `visual_analysis*.json` 中的候选片段复核摘要
- 如已生成，附上 `analysis/retrieval_candidates.json`

然后派发一个专门的 **dramatic editor** 子任务。这个子任务只做三件事：
1. 挑出必须保留原声的原片段
2. 压缩和重写 VO，使其只做铺垫 / 转场 / 补信息
3. 产出完整 `storyboard.json`

dramatic editor 在筛段时必须遵守：
- **先看检索候选，再做人工筛戏**：优先消费 `videosearch` 召回结果，而不是重新盲扫全量 transcript
- **检索只负责召回，不代替判断**：最终是否入选，仍以 transcript、真实台词力度、定向视觉复核结论为准

#### dramatic editor 的硬规则

- **钩子必须真钩人**：优先从后文最强冲突、最强反转、最强羞辱、最强护短场面里抽
- **`original` 优先选最有戏的台词，不是最完整的台词**
- **必须保留关键情绪链条**：如羞辱、反抗、护子、落难、安慰、表白、站队
- **VO 只做三种功能**：铺垫、跳转、补信息
- **VO 不得复述紧邻 `original` 已说明的内容**
- **`original.text` 必须是真正要展示的台词**，不能写“婆婆羞辱儿媳”“男主公开护妻”这种摘要标签
- 摘要说明如有必要，写入 `notes`
- 同一 source 内若时间回跳，必须在 `notes` 标记 `hook_preposed=true`；否则默认按剧情顺序推进

#### 步骤 6 的失败判定

以下任一命中，必须返工：
- `original.text` 明显是摘要而不是真实台词
- 缺失最关键的羞辱 / 反抗 / 反转 / 护妻 / 护子场面
- VO 中出现空泛大词：如“命运”“站稳”“移不开眼”“退路”等万能包装词，但没有人物感
- 原片最有戏的句子被改成 VO，导致原台词没被听到
- 选段只是“能说明剧情”，而不是“最有戏”

#### `storyboard.json` 在步骤 6 的最低要求

每个 segment 至少包含：
- `id`
- `title`
- `mode`：`voiceover` / `original`
- `source_index`
- `source_path`
- `start`
- `end`
- `text`
- `text_raw`
- `mute_original`
- `status`
- `notes`

额外要求：
- `original` 段在步骤 6 就必须有精确 `start/end` 和 `text_raw`
- `voiceover` 段允许先无时间，但必须有成型 `text`
- 每个 segment 的 `notes` 必须解释：为什么留原声 / 为什么此处必须 VO

#### 派生文件

步骤 6 完成后：
- 从 `storyboard.json` 派生 `final_script.md`
- 从 `storyboard.json` 里所有 `mode = voiceover` 的段落派生 `voiceover.md`

**产出**：`storyboard.json`、`final_script.md`、`voiceover.md`

### 步骤 7：生成解说音频

只对 `mode = voiceover` 的段落生成音频。

回写：
- `storyboard.json.segments[].audio_file`
- `storyboard.json.segments[].audio_duration_sec`
- `voiceover.md` 的对应音频时长

禁止：
- 给 `original` 段生成空音频
- 让 `voiceover.md` 和 `storyboard.json` 漂移

### 步骤 8：画面匹配（仅匹配 `voiceover` 段）

> 必须优先使用 `videosearch`；如果尚未建索引，先补做步骤 1.5。

这一步不再负责剧情编辑决策，只负责：
- 为所有 `voiceover` 段找能承载该段解说的画面
- 时间必须覆盖 `audio_duration_sec`
- 匹配理由必须体现**情绪承载作用**，不是只写“画面相关”

匹配要求：
- 先为每条 VO 写检索 query，再用 `videosearch` 召回候选片段
- 至少尝试 2 个不同 query；若结果偏“语义相关但没情绪”，继续改写 query
- 优先匹配有表情、动作、关系 tension 的画面
- 不要匹配纯信息说明性画面，除非别无选择
- 与同一 source 其他时间段不能重叠
- 选中时间段后，必须先回看 transcript；只有在候选冲突、画面承载力不明确或存在无台词镜头时，再做视觉复核确认不是误召回
- 匹配结果回写 `storyboard.json`
- 可选导出 `analysis/scene_matching.json` 作为审查快照

### 步骤 9：按 `storyboard.json` 逐段渲染

按 `storyboard.json` 顺序逐段：
- `trimvideo` 截取原片
- `voiceover` 段：静音原声并叠加 TTS
- `original` 段：保留原声
- 统一分辨率、帧率、像素格式、音频格式
- 输出到 `clips/merged/`

### 步骤 10：拼接输出最终成片

使用 FFmpeg concat demuxer 无损拼接 `clips/merged/*.mp4`。

回写：
- `storyboard.json.output.final_video`
- 各 segment 的最终状态

### 步骤 11：字幕确认与交接（可选）

如用户需要字幕，交接给专门字幕 skill，并携带：
- `output/output.mp4`
- `scripts/final_script.md`
- `scripts/storyboard.json`

## 质量检查清单

- [ ] `draft_script.md` 读起来顺，不是最终剪辑稿
- [ ] `storyboard.json` 是唯一真相源
- [ ] 已先用向量检索召回候选片段，再做人工筛选和定稿
- [ ] `doubaovision` 只在候选歧义、字幕不足、无台词强表演等必要场景介入；没有和检索重复扫片
- [ ] `original.text` 都是真实展示台词，不是摘要标签
- [ ] 最有戏的原片台词被优先保留
- [ ] `voiceover` 没有复述紧邻 `original` 已说清的内容
- [ ] 保留了完整情绪链条，而不是只保留结果
- [ ] 同一 source 时间顺序合理；如有回跳，`notes` 明确说明是钩子前置
- [ ] `voiceover.md` 与 `storyboard.json` 一一对应
- [ ] 裁切、拼接、交接都只读取 `storyboard.json`

## 常见问题

| 问题 | 根因 | 修正方式 |
|------|------|---------|
| 成片信息对了但不好看 | 只做了剧情摘要，没有做编辑决策 | 回到步骤 6，重挑原片戏眼 |
| 台词听了两遍 | VO 复述了原片已表达内容 | 压缩 VO，只保留铺垫和转场 |
| 原片都是真实台词但还是不够打人 | 选中了“说明剧情”的台词，而不是“最有戏”的台词 | 先补检索改写 query；若仍难判断，再做定向视觉复核，高张力优先 |
| `storyboard.json` 审不动 | `original.text` 写成摘要标签 | 改成真实展示台词，摘要写 `notes` |
| 同一 source 时间跳来跳去很乱 | 没区分钩子前置和正常顺序 | 默认按剧情顺序；只有钩子允许前置且必须标记 |
| 成片没有人物感 | VO 用了空泛短视频模板句 | 重写 VO，改成更贴人物、更贴处境的句子 |
