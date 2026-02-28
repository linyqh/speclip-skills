---
name: drama-explainer
description: 短剧解说视频制作工作流。将短剧原片制作成"解说 + 原片交替穿插"的二创视频。核心功能：(1) ASR 提取对话字幕，(2) 全片视觉分析画面内容，(3) 校验剧情与人物关系，(4) 结合对话 + 视觉撰写解说文案并生成配音，(5) 批量匹配画面时间段，(6) 解说画面静音、原片片段保留原声，交替穿插剪辑。触发场景：用户请求制作短剧解说、剧情解说、影视二创、影视解说等类似内容。
---

# 短剧解说工作流

## 解说风格

共 10 种解说风格可选，用户可通过风格名称或编号指定。未指定时默认使用 `1 默认风格`。

| ID | 风格 | 一句话描述 |
|----|------|-----------|
| 1 | 默认风格 | 冷静客观，最吸引人的部分前置，偏口语化 |
| 2 | 口语化叙述 | 接地气表达，直接切入正题，不排比不总结 |
| 3 | 高能白话 | 兄弟聊天口气，全程高能，"我靠/绝了"式表达 |
| 4 | 引导式开头 | 情感共鸣切入，直击大众痛点 |
| 5 | 吐槽式开头 | 毒舌吐槽+玩梗，朋友聊天式幽默 |
| 6 | 深度解析 | 专业影评人，开场白→剧情解析→主题升华 |
| 7 | 慢节奏 | 温暖舒缓，聚焦情感共鸣与人性美好 |
| 8 | 电影解密师 | 抛论点→证据链→逻辑闭环，侦探式解构 |
| 9 | 影视解说 | 爆款钩子结构，3秒抓住注意力，悬念+反转 |
| 10 | 短剧漫剧 | 句句爆点，高能反转+情绪冲突+悬念钩子 |

各风格的人设、语气、开头策略、示例详见 `references/styles/` 目录下的独立文件：

| 文件 | 风格 |
|------|------|
| [01-默认风格.md](references/styles/01-默认风格.md) | 冷静客观，高信息密度 |
| [02-口语化叙述.md](references/styles/02-口语化叙述.md) | 接地气表达 |
| [03-高能白话.md](references/styles/03-高能白话.md) | 兄弟聊天口气 |
| [04-引导式开头.md](references/styles/04-引导式开头.md) | 情感共鸣切入 |
| [05-吐槽式开头.md](references/styles/05-吐槽式开头.md) | 毒舌吐槽+玩梗 |
| [06-深度解析.md](references/styles/06-深度解析.md) | 专业影评人 |
| [07-慢节奏.md](references/styles/07-慢节奏.md) | 温暖舒缓治愈 |
| [08-电影解密师.md](references/styles/08-电影解密师.md) | 侦探式解构 |
| [09-影视解说.md](references/styles/09-影视解说.md) | 爆款钩子结构（含100条案例） |
| [10-短剧漫剧.md](references/styles/10-短剧漫剧.md) | 高能反转短剧风（含100条案例） |

**风格选择指引**：
- 温情/治愈类 → 7 慢节奏
- 搞笑/吐槽类 → 5 吐槽式 或 3 高能白话
- 悬疑/烧脑片 → 8 电影解密师
- 短剧/网剧 → 10 短剧漫剧
- 通用影视解说 → 9 影视解说 或 1 默认风格

## 核心原则

- **视觉优先理解剧情**：仅靠对话无法完整理解短剧，必须结合画面分析才能写出准确的解说文案
- **多源独立处理**：用户提供多个原片视频时，**不合并**，逐个独立执行 ASR、mediainfo、视觉分析
- **校验先行**：视觉分析完成后，必须经过校验步骤验证剧情走向、人物关系的准确性，再进入文案撰写
- **人物关系建档**：人物关系独立存储为 `characters.md`，作为文案撰写的核心参考，防止偏题
- **动态穿插节奏**：根据剧情节点动态决定每段解说和原片的时长，非固定比例
- **按剧情时序匹配**：解说画面从当前剧情进度提取，不跨时间线
- **音量控制**：解说片段使用原片静音画面，原片片段保留原声
- **代入感为核心**：文案描述观众能在画面中看到的真实内容，不凭空编造
- **禁止凭空估算画面时间段**：画面匹配必须通过 `doubao-chat` subagent 基于视觉模型确定，禁止根据对话时间戳或剧情推测来猜测
- **时间不重叠（强制约束）**：`vo_video` 和 `orig_video` 的时间段绝对不能重叠。生成 `scene_matching.json` 后必须使用 `drama_helper.py verify` 验证

## 工具清单

| 阶段 | 工具 | 用途 |
|------|------|------|
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
│   ├── characters.md        # ⭐ 人物档案（步骤4产出，独立文件）
│   └── scene_matching.json  # 画面匹配结果
├── scripts/                 # 步骤5产出：解说文案
│   └── voiceover.md         # 解说文案（Markdown表格）
├── audio/                   # 步骤6产出：配音音频
│   ├── vo_01.mp3
│   └── ...
├── clips/                   # 步骤7-8产出：视频片段
│   ├── voiceover/           # 解说画面（静音截取）
│   ├── original/            # 原片片段（保留原声）
│   └── merged/              # 合并后片段（解说画面+配音）
├── output/                  # 步骤9产出：最终成片
│   └── output.mp4
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
| `voiceover.md` | 解说文案（Markdown 表格格式） |
| `visual_analysis.json` | 全片视觉描述（summary + scenes） |
| `scene_matching.json` | 画面匹配结果（vo_video + orig_video + match_reason） |
| `state.json` | 项目状态跟踪（进度/片段/已用时间段） |

## 工作流程

### 步骤 0：项目初始化

```bash
# 单个原片
python scripts/drama_helper.py init --project-dir <项目名> --source <原片路径> [--style <风格ID>]

# 多个原片（不合并，逐个独立处理）
python scripts/drama_helper.py init --project-dir <项目名> --source <原片1> <原片2> [<原片3> ...] [--style <风格ID>]
```

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

> **此步骤是确保后续文案不偏题的关键环节。**

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

**状态更新**：`steps.4_verification = "completed"`

### 步骤 5：撰写解说文案

结合「对话时间轴」、「视觉描述」和「人物档案」三个维度撰写解说文案。

**输入**：`transcript.json` + `plot_analysis.md`（校验确认版）+ `visual_analysis.json` + `characters.md` + 对应风格文件

**撰写规则**：
- 严格遵循所选风格的人设、语气和开头策略（默认 1）
- 每段文案控制在 8-15 秒（约 30-60 字），结尾过渡到下一画面
- 文案必须描述画面中真实发生的事，视觉信息融入叙述
- 对话无法传达的情绪由文案补充
- **人物称呼必须与 `characters.md` 一致**，不要出现歧义或前后不一致的称呼
- **人物关系描述必须与 `characters.md` 一致**，防止偏题
- **避免台词重复**：不要复述原片台词（否则观众听两遍），用 `【播放原片】` 标记替代需要播放原声的部分

> **多源时**：解说文案中每段需标注 `source_index`（从 1 开始），指明该段画面来自哪个原片。

**产出**：`voiceover.md`
**状态更新**：`steps.5_script = "completed"`

### 步骤 6：生成解说音频

```
voiceover(text=<文案>, provider=free, speed=1.0, output_path=<项目名>/audio/vo_01.mp3)
```

逐段生成，记录实际音频时长，更新 `voiceover.md` 和 `state.json`。

**产出**：`vo_01.mp3`, `vo_02.mp3`, ...
**状态更新**：`steps.6_audio = "completed"`，`segments[].vo_duration` 填充实际时长

### 步骤 7：画面匹配（必须使用 doubao-chat subagent）

> **必须调用 `doubao-chat` subagent 完成画面匹配，禁止手动估算时间段。**

通过 `doubao-chat` subagent 与豆包视觉模型多轮对话，逐段匹配每段文案对应的画面时间段。匹配完成后**必须运行 `drama_helper.py verify` 验证时间不重叠**。

> **多源时**：`scene_matching.json` 中每个 segment 需包含 `source_index` 字段，指明画面来自哪个原片。对每个原片独立调用 doubao-chat subagent 完成该片的画面匹配。

详细的 subagent prompt 模板、匹配规则和校验流程见 [references/scene-matching-guide.md](references/scene-matching-guide.md)。

**产出**：`scene_matching.json`
**状态更新**：`steps.7_matching = "completed"`

### 步骤 8-9：截取视频、合并与渲染

根据 `scene_matching.json` 截取视频片段，合并解说画面与配音，最终拼接渲染成片。

> **多源时**：根据 `source_index` 从对应的原片中截取片段。

详细的 trimvideo 调用、FFmpeg 合并命令和渲染参数见 [references/rendering.md](references/rendering.md)。

**关键点**：
- 不要使用 `adelay` + `amix`，会导致音画不同步
- 先合并单个片段，再用 `concat filter` 统一拼接
- 所有音频统一为 `44100Hz stereo`

**产出**：步骤 8 → `clips/` 目录下各片段；步骤 9 → `output/output.mp4`
**状态更新**：`steps.8_clips = "completed"` → `steps.9_render = "completed"`

## 辅助脚本

```bash
# 初始化项目（支持多个原片）
python scripts/drama_helper.py init --project-dir <项目名> --source <原片1> [<原片2> ...] [--style <风格ID>]

# 添加解说片段
python scripts/drama_helper.py add --project-dir <项目名> <序号> <时长秒> <文案>

# 分配画面
python scripts/drama_helper.py allocate_video --project-dir <项目名> <序号> [优先起始秒]
python scripts/drama_helper.py allocate_orig --project-dir <项目名> <序号> [优先起始秒]

# 生成 timeline / 查看摘要
python scripts/drama_helper.py timeline --project-dir <项目名>
python scripts/drama_helper.py summary --project-dir <项目名>

# 验证 scene_matching.json（步骤 7 后必须执行）
python scripts/drama_helper.py verify <项目名>/analysis/scene_matching.json
```

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| 文案脱离画面内容 | 必须执行步骤 3 视觉分析，确保文案基于真实画面撰写 |
| 人物称呼不一致 | 检查 `characters.md` 是否准确建档，文案必须引用 `characters.md` 中的称呼 |
| 人物关系错误导致剧情偏题 | 步骤 4 校验不充分，需重新交叉验证对话与视觉分析 |
| 多个视频中同一角色识别为不同 Speaker | 在步骤 4 中统一修正 Speaker 映射 |
| 步骤 3 调用多次 doubaovision | 步骤 3 每个视频只需 1 次全片分析，精确匹配由步骤 7 完成 |
| 画面时长不足 | 调整文案缩短音频，或选择相邻相似画面 |
| 画面时间段重叠 | 运行 `drama_helper.py verify` 验证，冲突时调整起始点 |
| 后半部分音画不同步 | 先合并单个片段，用 `concat filter` 拼接，统一音频格式 |
| 音频格式不兼容 | 用 `aformat` 滤镜统一为 `stereo/44100Hz` |
| 衔接生硬 / 节奏拖沓 | 选择情绪匹配的原片片段；精简文案，增加高潮比重 |

## 质量检查

- [ ] 步骤 4 完成校验，`characters.md` 已建档且人物关系准确
- [ ] 文案中的人物称呼与 `characters.md` 一致
- [ ] 步骤 7 通过 `doubao-chat` subagent 完成画面匹配（非手动估算）
- [ ] 文案描述内容与视频画面实际发生的事匹配
- [ ] 步骤 3 每个视频调用 1 次 `doubaovision` 完成全片视觉理解
- [ ] 解说与原片穿插自然，无画面重复使用
- [ ] 解说片段配音正确，分辨率与原片一致
- [ ] 音画同步，音频格式统一（44100Hz stereo）
- [ ] 目录结构完整，`state.json` 所有步骤 completed
- [ ] **`drama_helper.py verify` 验证通过，无时间冲突**
- [ ] （多源时）各源文件独立分析，未合并处理
