---
name: drama-explainer
description: 短剧解说视频制作工作流。将短剧原片制作成“解说配音 + 原片高代入感台词/表演”交替穿插的二创视频。核心功能：(1) ASR 提取对话字幕，(2) 全片视觉分析画面内容，(3) 校验剧情与人物关系，(4) 将已确认文案拆分为最终剪辑脚本（区分“解说配音”与“播放原片”），(5) 仅对解说配音段生成 TTS，(6) 批量匹配画面时间段并按段渲染，(7) 可选进入字幕分支并按横屏/竖屏选择对应字幕方案。触发场景：用户请求制作短剧解说成片、剧情解说二创、影视解说剪辑等类似内容。
---

# 短剧解说工作流

## 核心原则


- **视觉优先理解剧情**：仅靠对话无法完整理解短剧，必须结合画面分析，才能为后续文案导入和画面匹配提供准确依据
- **多源独立处理**：用户提供多个原片视频时，**不合并**，逐个独立执行 ASR、mediainfo、视觉分析
- **校验先行**：视觉分析完成后，必须先校验剧情走向和人物关系，再进入文案导入与配音阶段
- **人物关系建档**：人物关系独立存储为 `characters.md`，作为后续文案审核和画面匹配的统一参考
- **文案外置**：解说文案创作已拆分到 `drama-script-writer`，本 skill 接收用户已确认的文案稿 / `voiceover.md` / 表格稿，并在步骤 5 整理成最终剪辑脚本
- **最终剪辑脚本先行**：步骤 5 必须先把“文案稿”整理成 `final_script.md`，显式标出每段是“解说配音”还是“播放原片”
- **原片台词优先**：凡是原片中已有表演力度、情绪张力或记忆点的台词，优先标记为“播放原片”，不要再让 TTS 复读一遍
- **动态穿插节奏**：根据剧情节点动态决定每段解说和原片的时长，非固定比例
- **按剧情时序匹配**：解说画面从当前剧情进度提取，不跨时间线
- **音量控制**：`解说配音` 段使用原片静音画面并叠加 TTS，`播放原片` 段保留原声
- **禁止凭空估算画面时间段**：画面匹配必须通过 `doubao-chat` subagent 基于视觉模型确定，禁止根据对话时间戳或剧情推测来猜测
- **时间不重叠（强制约束）**：同一 `source_index` 下所有最终使用的 `video` 时间段绝对不能重叠。生成 `scene_matching.json` 后必须逐项验证无冲突

## 工具清单

| 阶段 | 工具 | 用途 |
|------|------|------|
| 提问 | `question` | 与用户交互确认 |
| 分析 | `qwenasr` | 提取原片对话字幕和时间戳 |
| 分析 | `mediainfo` | 获取视频元数据 |
| 视觉 | `doubaovision` | **全片视觉分析**，理解整体剧情和画面内容 |
| 匹配 | `doubao-chat` subagent | 多轮对话**精确匹配**解说文案与原片画面时间段 |
| 生成 | `voiceover` | 解说文案转音频 |
| 剪辑 | `trimvideo` | 截取视频片段 |
| 合成 | `FFmpeg` | 多片段拼接渲染 |

## 项目目录结构

```
<项目名>/
├── analysis/                # 步骤1-4产出：分析与校验结果
│   ├── transcript.json      # ASR转录（单源）
│   ├── transcript_01.json   # ASR转录（多源时按序编号）
│   ├── transcript_02.json
│   ├── mediainfo.json       # 视频元数据（单源）
│   ├── mediainfo_01.json    # 视频元数据（多源时按序编号）
│   ├── mediainfo_02.json
│   ├── plot_analysis.md     # 剧情分析文档（三阶段更新：初步→视觉融合→校验确认）
│   ├── visual_analysis.json # 视觉描述（单源）
│   ├── visual_analysis_01.json # 视觉描述（多源时按序编号）
│   ├── visual_analysis_02.json
│   ├── characters.md        # 人物档案（步骤4产出，独立文件）
│   └── scene_matching.json  # 画面匹配结果
├── scripts/                 # 步骤5产出：最终剪辑脚本 + TTS 文案
│   ├── final_script.md      # 最终剪辑脚本（逐段标明“解说配音 / 播放原片”）
│   └── voiceover.md         # 仅保留需生成 TTS 的文案
├── audio/                   # 步骤6产出：仅为“解说配音”段生成的配音音频
│   ├── vo_01.mp3
│   └── ...
├── clips/                   # 步骤7-8产出：逐段视频片段
│   ├── raw/                 # 按最终脚本逐段截取的原始片段
│   └── merged/              # 标准化后片段（每段一个 merged_XXX.mp4）
├── output/                  # 步骤9-10产出：最终成片 / 字幕版
│   ├── output.mp4
│   └── output_subtitled.mp4 # 可选，用户需要字幕时产出
└── state.json               # 项目状态文件
```

> **多源文件命名规则**：单个原片时使用不带编号的文件名（如 `transcript.json`）；多个原片时按源文件顺序编号（如 `transcript_01.json`、`transcript_02.json`）。

## 文件格式规范

所有产出文件的 JSON/Markdown 结构定义详见 [references/file-formats.md](references/file-formats.md)，包含：

| 文件 | 说明 |
|------|------|
| `transcript.json` | ASR 转录，含说话人标识（A/B/C...） |
| `mediainfo.json` | 视频元数据（时长/分辨率/帧率等） |
| `plot_analysis.md` | 剧情分析（初步版 → 视觉融合版 → 校验确认版，三阶段更新） |
| `characters.md` | **人物档案**（人物列表 + 关系图 + 关系变化） |
| `final_script.md` | **最终剪辑脚本**（逐段标明是解说配音还是播放原片） |
| `voiceover.md` | 仅保留需要生成 TTS 的解说文案 |
| `visual_analysis.json` | 全片视觉描述（summary + scenes） |
| `scene_matching.json` | 画面匹配结果（逐段 `play_mode` + `video` + match_reason） |
| `state.json` | 项目状态跟踪（进度/片段/已用时间段） |

## 工作流程

### 步骤 0：项目初始化

本 skill 不负责从零撰写解说文案；开始前先确认用户是否已经准备好文案稿、`voiceover.md` 或等价的分段解说稿。

- 若用户**已经提供文案**：直接初始化项目并继续。
- 若用户**还没有文案**：暂停本流程，先使用 `drama-script-writer` 完成文案创作或让用户手动提供。

1. 创建项目目录结构：
```bash
mkdir -p <项目名>/{analysis,scripts,audio,clips/raw,clips/merged,output}
```

2. 写入 `<项目名>/state.json` 初始状态（格式详见 [references/file-formats.md](references/file-formats.md)）：
   - `project.sources`：原片绝对路径数组
   - `progress.steps`：所有步骤设为 `"pending"`
   - `segments`：空数组
   - `used_time_ranges`：按源文件数量初始化空数组

**产出**：项目目录结构 + `state.json`（所有步骤 `pending`）

### 步骤 1：分析原片

对每个原片**独立**执行 ASR 和 mediainfo：

```
# 单源
qwenasr(input_path=<原片>) → <项目名>/analysis/transcript.json
mediainfo(path=<原片>) → <项目名>/analysis/mediainfo.json

# 多源：逐个处理，按顺序编号
qwenasr(input_path=<原片1>) → <项目名>/analysis/transcript_01.json
mediainfo(path=<原片1>) → <项目名>/analysis/mediainfo_01.json
qwenasr(input_path=<原片2>) → <项目名>/analysis/transcript_02.json
mediainfo(path=<原片2>) → <项目名>/analysis/mediainfo_02.json
...
```

ASR 输出的 SRT 已包含说话人标识（`[Speaker N]` 前缀），构建 `transcript.json` 时需解析前缀并映射为角色标识（A/B/C...）。

> **多源注意**：不同视频中的同一角色可能被 ASR 识别为不同的 Speaker 编号。此时在步骤 4（校验）中统一修正。

**产出**：`transcript.json` / `transcript_01.json` + `mediainfo.json` / `mediainfo_01.json`
**状态更新**：`steps.1_analysis = "completed"`，`media` 字段填充

### 步骤 2：初步剧情分析

根据 ASR 转录内容（如有多源则综合所有转录），识别故事背景、人物关系、剧情线划分（开场→冲突→转折→高潮→结局）。

> **多源时**：按视频顺序拼接理解，注意不同视频间的剧情衔接。标注每段剧情来自哪个源文件。

**产出**：`plot_analysis.md`（初步版本，基于对话）
**状态更新**：`steps.2_plot_analysis = "completed"`

### 步骤 3：视觉分析（每个原片 1 次调用）

步骤 3 只负责理解全片剧情，**不进行精确画面匹配**（精确匹配由步骤 7 完成）。

对**每个**原片视频调用 **1 次** `doubaovision`：

```
doubaovision(
  file_path=<原片>,
  fps=0.5,
  max_tokens=4096,
  prompt="请详细描述这个视频的完整内容。
请包括：
1. 故事背景和类型
2. 主要人物的外貌、服装、性格特征
3. 场景环境
4. 剧情发展脉络（开场→冲突→转折→高潮→结局）
5. 关键视觉细节（表情变化、肢体语言、重要道具）
6. 情绪氛围和镜头语言
请按时间顺序描述，标注每个场景的时间段。"
)
```

- `fps=0.5`：2-3 分钟视频约采样 60-90 帧，足够理解剧情
- **每个视频只调用 1 次**，无论时长多少

**产出**：`visual_analysis.json` / `visual_analysis_01.json`, `visual_analysis_02.json`
**状态更新**：`steps.3_visual_analysis = "completed"`

### 步骤 4：校验与人物建档

> **此步骤会为后续文案审核、配音和画面匹配建立统一剧情基线。**

将步骤 2（对话分析）和步骤 3（视觉分析）的结果进行**交叉校验**，修正不准确的信息，并产出独立的人物档案文件。

**输入**：`plot_analysis.md`（初步版）+ `visual_analysis.json` + 所有 `transcript.json`

**校验清单**：

| 校验项 | 具体操作 |
|--------|---------|
| **人物身份匹配** | 将 Speaker A/B/C 与视觉分析中识别的人物外貌对应。确认每个 Speaker 是谁（姓名/称呼、外貌、身份） |
| **人物关系准确性** | 交叉验证对话中暗示的关系（称呼、语气）与视觉中的互动（肢体语言、距离、表情）是否一致 |
| **故事背景** | 对话中的背景线索（地点、时代、职业）与视觉场景是否吻合 |
| **剧情走向** | 对话推断的剧情线与视觉呈现的实际画面是否匹配，是否存在仅靠对话无法理解的情节 |
| **多源连贯性** | （多源时）不同视频间的角色是否同一人，剧情是否连贯衔接 |

**工作流程**：

1. **逐项对比**：将 `plot_analysis.md` 中的每个要素与 `visual_analysis.json` 对照
2. **修正差异**：发现不一致时，以视觉分析为准修正（画面是真实的，对话推断可能有误）
3. **产出 `characters.md`**：将确认后的人物信息独立建档（格式详见 [references/file-formats.md](references/file-formats.md)）
4. **更新 `plot_analysis.md`**：融合视觉信息后覆盖为「校验确认版」

**产出**：
- `characters.md`（人物档案，**独立文件**）
- `plot_analysis.md`（校验确认版，覆盖初步版本）

**⛔ STOP — 产出完成后必须停下，等用户确认后才能进入步骤 5。不要跳过。**

1. 先向用户输出以下摘要信息：
   - 人物列表（姓名、身份、彼此关系，每人一行）
   - 核心剧情走向（一句话概括每个阶段：开场→冲突→转折→高潮→结局）
2. 然后调用 `AskUserQuestion` 工具：
   - question: `"以上人物关系和剧情理解是否正确？"`
   - header: `"剧情校验"`
   - options:
     - `"确认无误"` — 人物关系和剧情理解正确，继续导入文案
     - `"需要修正"` — 有错误需要修改，我会在下方说明具体问题
3. 用户选择「需要修正」时，根据反馈修正 `characters.md` 和 `plot_analysis.md`，修正后**重新展示并再次提问**，直到用户选择「确认无误」。

**状态更新**：用户确认后 `steps.4_verification = "completed"`

### 步骤 5：导入并确认解说文案

本 skill 不负责从零创作文案，但**必须**把用户提供的文案整理成“最终可执行剪辑脚本”。

**输入**：用户提供的 `voiceover.md`、表格稿、纯文本分段稿，或由 `drama-script-writer` 产出的最终文案

**本步骤必须同时产出 2 份文件**：
1. `scripts/final_script.md`：最终剪辑脚本，逐段标明 `play_mode`
   - `解说配音`：需要生成 TTS
   - `播放原片`：直接使用原片音画或至少保留原声，不生成 TTS
2. `scripts/voiceover.md`：**仅保留 `play_mode=解说配音` 的段落**，供步骤 6 生成配音

**拆分规则（关键）**：
- 每段先判断它属于“解说配音”还是“播放原片”，不要把二者混在一段里
- **人物称呼必须与 `characters.md` 一致**，不要出现歧义或前后不一致的称呼
- **人物关系描述必须与 `characters.md` 一致**，防止偏题
- 涉及画面动作、情绪、关系的表述不能与 `plot_analysis.md` 和 `visual_analysis.json` 冲突
- **原片中已存在的高张力台词，优先改为 `播放原片`**，不要在 TTS 里重复朗读一遍
- 出现以下情况时，必须优先拆成“铺垫解说 + 原片台词”两段：
  - 文案里出现引号、冒号、破折号引出原话
  - 文案在描述“某人当着全家人的面说/骂/喊/质问/摊牌”等，且原片中确有对应对白
  - 原片表演本身比复述更有代入感
- **多源时**：每段需标注 `source_index`（从 1 开始），指明该段画面来自哪个原片

**示例（必须按这种思路拆）**：

```markdown
| 段落 | 播放方式 | 文案/台词 | 对应视频 | 预估时长 | 备注 |
|------|----------|-----------|---------|---------|------|
| 15 | 解说配音 | 回到娘家，怀孕的嫂子当着全家人的面说—— | 1 | 4秒 | 用解说铺垫冲突 |
| 16 | 播放原片 | 房子这么小，小姑子带个拖油瓶回来，挤得我胎都不稳了。 | 1 | 6秒 | 直接使用原片表演和原声，不生成 TTS |
```

**产出**：`final_script.md` + `voiceover.md`

**⛔ STOP — 文案整理完成后必须停下，等用户确认后才能进入步骤 6。不要跳过。**

1. 向用户展示整理后的 `final_script.md`，并说明：总段数、其中 `解说配音` 段数、`播放原片` 段数、预估总时长。
2. 同时展示派生后的 `voiceover.md`，让用户确认哪些段会生成 TTS、哪些段会直接播放原片。
3. 若用户要求改写语气、重写段落或补全缺失内容，停止本 skill 的后续步骤，改用 `drama-script-writer` 处理文案。
4. 用户确认无误后，再进入配音阶段。

**状态更新**：用户确认满意后 `steps.5_script = "completed"`

### 步骤 6：生成解说音频

```
voiceover(text=<文案>, provider=free, speed=1.0, output_path=<项目名>/audio/vo_01.mp3)
```

仅对 `final_script.md` 中 `play_mode = 解说配音` 的段落逐段生成，`播放原片` 段**跳过**，不要生成空音频。

- `voiceover.md` 中每一行必须保留 `final_segment` 字段，便于回写到最终脚本
- 记录实际音频时长，回填到 `voiceover.md`、`final_script.md` 和 `state.json`
- `播放原片` 段在 `state.json` 中标记 `needs_tts = false`

**产出**：`vo_01.mp3`, `vo_02.mp3`, ...
**状态更新**：`steps.6_audio = "completed"`，`segments[].audio_duration` 填充实际时长（仅 `解说配音` 段有值）

### 步骤 7：画面匹配（必须使用 doubao-chat subagent）

> **必须调用 `doubao-chat` subagent 完成画面匹配，禁止手动估算时间段。**

通过 `doubao-chat` subagent 与豆包视觉模型多轮对话，按 `final_script.md` 的**最终段落顺序**逐段匹配每段对应的画面时间段。匹配完成后**必须验证时间不重叠**。

**匹配目标**：
- `解说配音` 段：找一段能承载该段解说的画面，`video` 时长必须覆盖该段 `audio_duration`
- `播放原片` 段：找出原片中该句台词/该段表演实际发生的时间段，保留原声，优先确保台词完整与表演完整

> **多源时**：`scene_matching.json` 中每个 segment 需包含 `source_index` 字段，指明画面来自哪个原片。对每个原片独立调用 doubao-chat subagent 完成该片的画面匹配。

详细的 subagent prompt 模板、匹配规则和校验流程见 [references/scene-matching-guide.md](references/scene-matching-guide.md)。

**产出**：`scene_matching.json`

**⚠️ 验证时间不重叠（必须执行）**：生成 `scene_matching.json` 后，逐项检查以下规则，全部通过才能继续：

1. **段落完整**：每个最终段落都必须有一条匹配结果，禁止漏段
2. **同源全局**：同一 `source_index` 下所有 `video` 时间段按 start 排序后，前一段的 end 不能超过后一段的 start
3. **时间边界**：所有时间段的 start >= 0 且 end <= 该源视频总时长
4. **音频时长保障**：每个 `解说配音` 段的 `video` 时长必须 >= `audio_duration`。不满足时执行「音频超长修复流程」（详见 [references/scene-matching-guide.md](references/scene-matching-guide.md)）：无重叠冲突则延长 `video`，有冲突则重写该段文案并重新生成音频
5. **原台词完整**：每个 `播放原片` 段必须覆盖该句关键台词或关键表演的完整起止，不能只截半句

发现冲突时：向后偏移冲突段的起始时间，修正后重新验证。

**状态更新**：`steps.7_matching = "completed"`

### 步骤 8：截取视频与标准化合并

> **⚠️ 本步骤包含 2 个阶段：阶段 A（截取）和阶段 B（标准化合并）。阶段 B 是确保音视频格式统一和解说音频不丢失的关键步骤，不可跳过。**
> **⚠️ 不要使用 `rendervideo` 工具做最终渲染，它的 timeline 格式不支持解说配音叠加，会导致成片无解说音频。必须使用 FFmpeg 手动渲染。**

> **多源时**：每个 segment 的 `source_index` 指明从哪个原片截取，从 `state.json` 的 `project.sources` 数组中取对应路径。

**阶段 A — 按最终脚本逐段截取**：根据 `scene_matching.json`，每个最终段落只截取 **1 个** 原始片段：

```
trimvideo(input_path=<原片[source_index]>, start=<video.start>, end=<video.end>,
          output_path=<项目名>/clips/raw/clip_015.mp4)
```

**阶段 B — 标准化与合并（关键步骤）**：将所有片段统一为相同的视频参数（分辨率、帧率、像素格式、音频格式），并按 `play_mode` 决定音频来源，为步骤 9 的无损拼接做准备。

> **参数来源**：从 `mediainfo.json` 读取源视频的分辨率（`SRC_RES`，如 `1920:1080`）和帧率（`SRC_FPS`，如 `30`），确保输出与原片一致。不要硬编码 fps=25。

**B1 — `解说配音` 段**：标准化视频 + 用配音替换原声：

```bash
ffmpeg -y -i <项目名>/clips/raw/clip_015.mp4 \
  -i <项目名>/audio/vo_015.mp3 \
  -filter_complex "\
    [0:v]fps=<SRC_FPS>,scale=<SRC_RES>:force_original_aspect_ratio=decrease,\
    pad=<SRC_RES>:-1:-1,format=yuv420p[v]; \
    [1:a]aformat=sample_rates=44100:channel_layouts=stereo[a]" \
  -map "[v]" -map "[a]" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k -shortest \
  <项目名>/clips/merged/merged_015.mp4
```

**B2 — `播放原片` 段**：标准化视频 + 保留原声：

```bash
ffmpeg -y -i <项目名>/clips/raw/clip_016.mp4 \
  -filter_complex "\
    [0:v]fps=<SRC_FPS>,scale=<SRC_RES>:force_original_aspect_ratio=decrease,\
    pad=<SRC_RES>:-1:-1,format=yuv420p[v]; \
    [0:a]aformat=sample_rates=44100:channel_layouts=stereo[a]" \
  -map "[v]" -map "[a]" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k \
  <项目名>/clips/merged/merged_016.mp4
```

> 如果 `播放原片` 段没有音频轨道，用 `anullsrc` 生成静音轨：将 `[0:a]aformat=...` 替换为 `anullsrc=r=44100:cl=stereo[a]`。

**产出**：
- `clips/raw/clip_*.mp4` — 按最终脚本逐段截取的原始片段
- `clips/merged/merged_*.mp4` — **标准化后的最终片段**（每段一个文件；TTS 段含配音，原片段含原声）

**状态更新**：`steps.8_clips = "completed"`，`segments[].status = "merged"`

### 步骤 9：拼接渲染成片

> **⚠️ 拼接时只使用阶段 B 产出的 `merged_*.mp4`，不要直接使用 `clips/raw/` 中的原始截取文件。**

所有片段已在步骤 8 阶段 B 标准化为相同格式，使用 FFmpeg **concat demuxer** 无损拼接（`-c copy`，无需重新编码）。

**第一步 — 生成文件列表**：

```bash
cat > <项目名>/filelist.txt << 'EOF'
file 'clips/merged/merged_015.mp4'
file 'clips/merged/merged_016.mp4'
file 'clips/merged/merged_017.mp4'
file 'clips/merged/merged_018.mp4'
...
EOF
```

**第二步 — 无损拼接**：

```bash
ffmpeg -y -f concat -safe 0 -i <项目名>/filelist.txt \
  -c copy \
  -movflags +faststart \
  <项目名>/output/output.mp4
```

**关键点**：
- **concat demuxer + `-c copy`**：步骤 8 已统一所有片段的编解码参数，此处直接流复制，速度极快且无质量损失
- **`-movflags +faststart`**：将 MP4 元数据前置，支持网络播放时边下载边播放
- **不要使用 `adelay` + `amix`**，会导致后半部分音画不同步
- **不要使用 concat filter**：已无必要重新编码，且输入数量多时 filter_complex 会过于复杂

完整的 FFmpeg 参数细节见 [references/rendering.md](references/rendering.md)。

**产出**：`output/output.mp4` — 最终成片
**状态更新**：`steps.9_render = "completed"`

### 步骤 10：字幕确认与分支（可选）

渲染完成后，**必须先问用户要不要字幕**，不要默认跳过，也不要默认强烧。

1. 读取首个源视频或最终输出的视频尺寸：
   - `height > width` → `orientation = portrait`（竖屏）
   - `width >= height` → `orientation = landscape`（横屏）
2. 明确询问用户：是否需要给最终成片增加字幕。
3. 若用户不需要字幕：直接交付 `output/output.mp4`。
4. 若用户需要字幕：
   - 将 `orientation`、`output/output.mp4`、`scripts/final_script.md`、`analysis/scene_matching.json` 作为输入，交给后续专门的字幕 skill
   - **不要在本 skill 内拍脑袋决定字幕样式或强行硬编码字幕位置**
   - 若当前环境还没有对应字幕 skill，则停下并把上述输入信息整理给用户，等待字幕 skill 接手

**状态更新**：
- 用户不要字幕：`steps.10_subtitles = "skipped"`
- 用户需要字幕且已交接：`steps.10_subtitles = "completed"`

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| 导入文案与剧情不符 | 回看步骤 3 和步骤 4 的结果，按 `plot_analysis.md`、`visual_analysis.json`、`characters.md` 重新校正文案后再继续 |
| 人物称呼不一致 | 检查 `characters.md` 是否准确建档，并在 `voiceover.md` 中统一修正称呼 |
| 人物关系错误导致剧情偏题 | 步骤 4 校验不充分，需重新交叉验证对话与视觉分析 |
| 多个视频中同一角色识别为不同 Speaker | 在步骤 4 中统一修正 Speaker 映射 |
| 步骤 3 调用多次 doubaovision | 步骤 3 每个视频只需 1 次全片分析，精确匹配由步骤 7 完成 |
| 台词听了两遍，代入感差 | 步骤 5 没有先拆成 `final_script.md`。原片已有情绪张力的台词必须标记为 `播放原片`，不要再生成 TTS |
| 画面时长不足 | 步骤 7「音频超长修复流程」自动处理：无重叠冲突时延长 `video`，有冲突时自动重写该段文案并重新生成音频。禁止通过 `-shortest` 截断音频 |
| 画面时间段重叠 | 按步骤 7 的验证规则逐项检查，冲突时向后偏移起始点 |
| **成片无解说音频** | **步骤 8 阶段 B 被跳过。必须先 FFmpeg 标准化合并每个最终段落：`解说配音` 段输出 `merged_*.mp4`（含 TTS），`播放原片` 段输出 `merged_*.mp4`（含原声），步骤 9 拼接时只用 `clips/merged/` 下的文件。不要用 rendervideo 工具或 timeline.json 渲染** |
| 后半部分音画不同步 | 步骤 8 阶段 B 统一所有片段格式，步骤 9 用 concat demuxer 无损拼接 |
| 音频格式不兼容 | 步骤 8 阶段 B 用 `aformat` 滤镜统一为 `stereo/44100Hz`，步骤 9 无需再处理 |
| 最终视频没有字幕 | 步骤 10 被跳过。渲染后必须先询问用户是否需要字幕；需要时先判断横屏/竖屏，再交给对应字幕 skill |
| 衔接生硬 / 节奏拖沓 | 优先检查导入文案的分段是否过长，再调整原片片段选择 |

## 质量检查

- [ ] 步骤 4 完成校验，`characters.md` 已建档且人物关系准确
- [ ] `final_script.md` 中每段都已标明 `解说配音 / 播放原片`
- [ ] 原片已有高张力台词的段落未被 TTS 复读，已改为 `播放原片`
- [ ] `voiceover.md` 仅包含需要生成 TTS 的段落，且人物称呼与 `characters.md` 一致
- [ ] 步骤 7 通过 `doubao-chat` subagent 完成画面匹配（非手动估算）
- [ ] 导入文案的内容与视频画面实际发生的事匹配
- [ ] 步骤 3 每个视频调用 1 次 `doubaovision` 完成全片视觉理解
- [ ] 解说与原片穿插自然，无画面重复使用
- [ ] 步骤 8 阶段 B 已执行：每个最终段落都产出一个 `merged_*.mp4`，TTS 段含配音，原片段含原声，所有片段格式统一
- [ ] 步骤 9 拼接使用 `clips/merged/` 目录下的标准化文件，非 `clips/raw/`
- [ ] 所有片段分辨率、帧率与原片一致（从 mediainfo.json 读取，非硬编码）
- [ ] 音画同步，音频格式统一（44100Hz stereo），输出含 `+faststart`
- [ ] 目录结构完整，`state.json` 所有步骤 completed
- [ ] 已询问用户是否需要字幕；若需要，已根据横屏/竖屏进入对应字幕分支
- [ ] **scene_matching.json 时间冲突验证通过（步骤 7 验证规则）**
- [ ] （多源时）各源文件独立分析，未合并处理
