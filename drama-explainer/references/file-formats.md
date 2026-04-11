# 文件格式规范与质量约束

本文档定义 `drama-explainer` 中关键文件的结构、字段语义、质量约束和常见错误。

## 多源文件命名规则

当用户提供多个原片视频时，按源文件顺序编号。单个原片时使用不带编号的文件名。

| 文件类型 | 单源 | 多源 |
|---------|------|------|
| ASR 转录 | `transcript.json` | `transcript_01.json`, `transcript_02.json`, ... |
| 视频元数据 | `mediainfo.json` | `mediainfo_01.json`, `mediainfo_02.json`, ... |
| 视觉描述 | `visual_analysis.json` | `visual_analysis_01.json`, `visual_analysis_02.json`, ... |
| 剧情分析 | `plot_analysis.md` | `plot_analysis.md` |
| 人物档案 | `characters.md` | `characters.md` |
| 检索候选快照 | `retrieval_candidates.json` | `retrieval_candidates.json` |
| 原始文案 | `draft_script.md` | `draft_script.md` |
| 分镜主数据 | `storyboard.json` | `storyboard.json` |
| 匹配快照 | `scene_matching.json` | `scene_matching.json` |

## `draft_script.md`

作用：只把故事讲顺，为步骤 6 提供删改底稿。

### 正例特点
- 读起来顺
- 情绪线完整
- 人物称呼一致
- 不提前拆 `mode`

### 反例特点
- 提前写时间戳
- 提前决定全部 `original` / `voiceover`
- 用万能包装句代替人物处境
- 读起来像短视频成片，而不是底稿

## `storyboard.json`

这是唯一真相源。所有音频、匹配、裁切、拼接都只读取它。

### 推荐结构

```json
{
  "version": "1.0",
  "project": {
    "name": "jljw2_drama_explainer",
    "title": "她最狼狈那天被求婚，他却在婚宴上当众护到底",
    "created_at": "2026-03-13T12:00:00Z"
  },
  "sources": [
    {
      "source_index": 1,
      "source_path": "/abs/path/1.mp4",
      "subtitle_path": "/abs/path/1.srt",
      "transcript_path": "analysis/transcript_01.json",
      "duration_sec": 182.4
    }
  ],
  "draft_script_path": "scripts/draft_script.md",
  "segments": [
    {
      "id": "seg_01",
      "title": "开场钩子",
      "mode": "voiceover",
      "source_index": 1,
      "source_path": "/abs/path/1.mp4",
      "start": null,
      "end": null,
      "text": "洪灾刚过，她硬闯医务室救人，转头却被家里逼着改嫁。",
      "text_raw": null,
      "mute_original": true,
      "audio_file": null,
      "audio_duration_sec": null,
      "status": "scripted",
      "notes": "hook_preposed=true；用后文最强处境做开场，VO 负责立题"
    },
    {
      "id": "seg_02",
      "title": "怒斥领导命金贵",
      "mode": "original",
      "source_index": 1,
      "source_path": "/abs/path/1.mp4",
      "start": "00:00:50.580",
      "end": "00:00:56.900",
      "text": "你检查个铲铲呐，再检查都好球了。国家领导现在的身体叫金贵，我们那些工人的命都不值钱呐。",
      "text_raw": "你检查个铲铲呐，再检查都好球了。国家领导现在的身体叫金贵，我们那些工人的命都不值钱呐。",
      "mute_original": false,
      "audio_file": null,
      "audio_duration_sec": null,
      "status": "scripted",
      "notes": "必须保留原声：这句最能立住蔡小燕的脾气和立场"
    }
  ],
  "output": {
    "final_video": null
  }
}
```

> 注意：向量索引本身属于工具运行时状态，不写入 `storyboard.json`。如需保留检索证据，请写到 `analysis/retrieval_candidates.json`。

### 顶层字段说明

- `version`：schema 版本号
- `project.name`：项目名
- `project.title`：成片标题或工作标题
- `project.created_at`：ISO 8601 时间戳
- `sources`：原视频信息列表
- `draft_script_path`：对应初稿路径
- `segments`：最终分镜时间线
- `output.final_video`：最终成片路径

### `sources[]` 字段说明

- `source_index`：素材编号，从 `1` 开始
- `source_path`：素材绝对路径
- `subtitle_path`：字幕路径，用于台词锚定
- `transcript_path`：transcript 路径
- `duration_sec`：素材总时长，单位秒

### `segments[]` 字段说明

- `id`：片段唯一标识
- `title`：供人工审查的短标题
- `mode`：只允许 `voiceover` 或 `original`
- `source_index`：对应 `sources[].source_index`
- `source_path`：冗余保存，便于人工审查和调试
- `start` / `end`：使用时间范围；`original` 在步骤 6 就必须有值，`voiceover` 在步骤 8 匹配后回填
- `text`：最终展示文本
- `text_raw`：原始字幕 / ASR 文本；`original` 段应保留，`voiceover` 固定为 `null`
- `mute_original`：`voiceover = true`，`original = false`
- `audio_file`：对应配音文件，仅 `voiceover` 段回填
- `audio_duration_sec`：对应配音时长，仅 `voiceover` 段回填
- `status`：建议使用 `scripted` / `audio_ready` / `matched` / `merged` / `rendered`
- `notes`：必须写一句解释，说明为何保留原声或为何这里必须 VO；如有时间回跳，写 `hook_preposed=true`

## `storyboard.json` 质量规则

### 强制规则

- `original.text` 必须是真实展示台词，不能是摘要标签
- `original` 段必须保留 `text_raw`
- `voiceover` 不得复述紧邻 `original` 刚说清楚的内容
- 若同一 source 出现时间回跳，`notes` 必须标明 `hook_preposed=true`
- 全部最终渲染逻辑只读取 `storyboard.json`

### 编辑规则

- 优先保留“最有戏”的原片，不优先保留“最完整”的原片
- `voiceover` 只负责铺垫、转场、补信息
- 情绪链条必须完整，不能只留结果
- 钩子必须来自后文真正最强的一段戏，而不是泛泛总结

## `storyboard.json` 常见负例

### 负例 1：摘要冒充台词

```json
{
  "mode": "original",
  "text": "婆婆羞辱儿媳",
  "text_raw": "我儿放到那么多条件好的、长得贵的女娃儿不要。可以找个二婚的。"
}
```

问题：`text` 不是最终展示台词，而是摘要标签。

### 负例 2：VO 套话过重

```json
{
  "mode": "voiceover",
  "text": "命运的齿轮在这一刻开始转动，她终于站稳了人生。"
}
```

问题：空泛、模板化、没有人物感。

### 负例 3：时间回跳无说明

```json
[
  {"id": "seg_01", "source_index": 1, "start": "00:03:10.000", "end": "00:03:18.000", "notes": ""},
  {"id": "seg_02", "source_index": 1, "start": "00:00:50.000", "end": "00:00:56.000", "notes": ""}
]
```

问题：同源内发生明显回跳，但没有标记是钩子前置。

## `retrieval_candidates.json`

这是步骤 3.5 的**可选检索候选快照**，用于记录向量检索召回过哪些高张力候选，帮助步骤 6 / 8 回放检索依据。

它不是新的真相源；最终入选片段仍以 `storyboard.json` 为准。

### 推荐结构

```json
{
  "version": "1.0",
  "generated_at": "2026-03-13T12:20:00Z",
  "queries": [
    {
      "label": "羞辱",
      "query": "婆家当众羞辱儿媳，语气刻薄，围观压力强",
      "results": [
        {
          "source_index": 1,
          "start": "00:00:50.580",
          "end": "00:00:56.900",
          "score": 0.8731,
          "reason": "台词和围观氛围都强，适合作为羞辱戏眼候选"
        }
      ]
    }
  ]
}
```

### 字段说明

- `label`：候选类别，如 `羞辱` / `反抗` / `护子` / `安慰` / `站队`
- `query`：实际用于 `videosearch` 的自然语言检索语句
- `results[].source_index`：命中的素材编号
- `results[].start` / `results[].end`：命中的候选时间范围
- `results[].score`：相似度分数，用于排序参考
- `results[].reason`：为什么这条结果值得进入后续人工筛选

### 质量规则

- 每类关键情绪至少保留 1 组有效候选
- 不要只保存“语义相关但没戏”的说明性镜头
- 候选不足时，优先改写 query 再检索，不要直接跳过关键情绪节点

## `final_script.md`

这是从 `storyboard.json` 派生的**人类审查稿**，不再是程序输入。

建议格式：

```markdown
# final_script

## segment seg_01
- mode: voiceover
- source: 1.mp4
- start: null
- end: null
- text: 洪灾刚过，她硬闯医务室救人，转头却被家里逼着改嫁。
- notes: hook_preposed=true；用后文最强处境做开场

## segment seg_02
- mode: original
- source: 1.mp4
- start: 00:00:50.580
- end: 00:00:56.900
- text: 你检查个铲铲呐，再检查都好球了。国家领导现在的身体叫金贵，我们那些工人的命都不值钱呐。
- notes: 必须保留原声；这句最能立住人物
```

## `voiceover.md`

这是从 `storyboard.json` 中筛选出 `mode = voiceover` 的段落后得到的派生文件。

```markdown
# Voiceover

- VO01 | storyboard_segment=seg_01 | 洪灾刚过，她硬闯医务室救人，转头却被家里逼着改嫁。
```

## `scene_matching.json`

这是步骤 8 的可选审查快照，不是新的真相源。

如果生成，必须和 `storyboard.json` 保持一致，只用于人工复核匹配质量。

## `state.json`

只保存：
- `project`
- `progress`
- `media`
- `last_error`

不再保存：
- `segments`
- `used_time_ranges`
- 任何片段级真相字段
