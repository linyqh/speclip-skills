# 步骤 7：画面匹配详细指南

## 阶段 A：派发 doubao-chat subagent

构造 subagent 任务 prompt，必须包含以下信息：
1. 视频文件路径（subagent 需要在首轮调用 `doubao-chat` 工具时传入）
2. ASR 时间轴摘要（从 `transcript.json` 提取关键对话和时间点）
3. 全部解说文案及实际音频时长（从 `voiceover.md` 提取）
4. 匹配规则和输出格式要求

**调用方式**：使用 TaskTool 派发 subagent，`subagent_type` 为 `"doubao-chat"`。

```
TaskTool(
  subagent_type="doubao-chat",
  description="匹配解说文案与原片画面时间段",
  prompt="请为以下短剧解说文案匹配原片画面时间段。

⚠️ 重要：首次调用 doubao-chat 工具时，必须传入 file_path 参数上传视频：
doubao-chat(file_path=\"<原片的绝对路径>\", prompt=\"...\")
后续追问使用返回的 session_id 继续对话，不需要再传 file_path。

## 对话时间轴（ASR 转录摘要）
{从 transcript.json 提取的关键对话和时间点}

## 解说文案
| 序号 | 文案 | 音频时长 | 对应剧情时间范围 |
|------|------|----------|-----------------|
| 1    | ...  | 10.5s    | 00:15-00:45     |
| 2    | ...  | 8.2s     | 00:45-01:20     |
...

## 匹配规则
1. 每段解说需要两个画面：「解说画面」和紧随其后的「原片片段」
2. 解说画面：时长必须精确等于该段音频时长，画面内容要与文案描述匹配
3. 原片片段：时长不做硬性要求，选择能给观众代入感的片段，确保观感连贯
4. **⚠️ 所有画面时间段不能重叠（不能重复使用同一段画面）**
   - `vo_video` 和 `orig_video` 不能重叠（同一片段内的解说和原片）
   - 相邻片段的画面也不能重叠
   - 规则：对于每段，必须满足 `vo_video.end <= orig_video.start` 或 `orig_video.end <= vo_video.start`
5. 整体按剧情时序推进，不跨时间线

## 工作方式
1. 先向豆包提问视频的整体画面概况和关键时间节点
2. 然后逐段（或分批）提问每段文案对应的最佳画面时间段
3. 如果某段匹配不确定，追问该时间段附近的具体画面内容
4. 最终输出完整的匹配 JSON

> **多源时**：对每个原片独立调用 doubao-chat subagent。每段文案已通过 voiceover.md 中的"源文件"列标注了来自哪个原片，subagent 只需在对应视频中匹配画面。

## 输出格式
最终请输出 JSON 数组：
[
  {
    \"segment\": 1,
    \"source_index\": 1,
    \"vo_video\": {\"start\": 15.0, \"end\": 25.5},
    \"orig_video\": {\"start\": 25.5, \"end\": 35.0},
    \"match_reason\": \"画面中男主推门进入办公室，与文案描述吻合\"
  }
]

> `source_index` 标注该段画面来自哪个原片（编号从 1 开始）。单源时可省略或固定为 1。"
)
```

## 阶段 B：校验匹配结果

从 subagent 返回的结果中提取 JSON，逐项校验：

| 校验项 | 处理方式 |
|--------|---------|
| JSON 解析失败 | 从返回文本中提取 JSON 块，去除 markdown 包裹 |
| 解说画面时长 ≠ 音频时长 | 强制修正 `vo_video.end = vo_video.start + vo_duration` |
| **时间段重叠** | **逐项验证无冲突（见下方规则）**，冲突时向后偏移冲突段 |
| 时间超出视频总时长 | 裁剪到视频末尾，报告警告 |
| 缺少某段匹配 | 回退到 ASR 时间轴，按对应剧情时间顺序分配 |

**⚠️ 强制验证步骤**：逐项检查以下规则，全部通过才能继续：

1. **同一片段内**：每个 segment 的 `vo_video` 和 `orig_video` 不能重叠（即 `vo_video.end <= orig_video.start` 或 `orig_video.end <= vo_video.start`）
2. **同源全局**：同一 `source_index` 下的所有时间段（所有 segment 的 vo_video + orig_video）按 start 排序后，前一段的 end 不能超过后一段的 start
3. **时间边界**：所有时间段的 start >= 0 且 end <= 该源视频总时长

发现冲突时：向后偏移冲突段的起始时间，修正后重新验证。

校验通过后，将结果写入 `<项目名>/analysis/scene_matching.json`。

**产出**：
- `<项目名>/analysis/scene_matching.json` — 批量匹配结果

**状态更新**：`steps.7_matching = "completed"`，`segments[].vo_video` 和 `orig_video` 填充，`used_time_ranges` 更新
