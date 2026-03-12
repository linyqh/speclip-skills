# 步骤 7：画面匹配详细指南

## 核心目标

步骤 7 不再假设“每段都必须拆成 `vo_video + orig_video` 二联结构”。

现在的唯一基准是 `scripts/final_script.md`：
- `解说配音` 段 → 匹配一段可承载 TTS 的画面
- `播放原片` 段 → 匹配原片中该句台词 / 该段表演真实发生的时间段，并保留原声

最终输出必须是**逐段时间线**，与 `final_script.md` 段落顺序一一对应。

## 阶段 A：派发 doubao-chat subagent

构造 subagent 任务 prompt，必须包含以下信息：
1. 视频文件路径（subagent 需要在首轮调用 `doubao-chat` 工具时传入）
2. ASR 时间轴摘要（从 `transcript.json` 提取关键对话和时间点）
3. `final_script.md` 全部段落，以及 `voiceover.md` 中已生成的实际音频时长
4. 匹配规则和输出格式要求

**调用方式**：使用 TaskTool 派发 subagent，`subagent_type` 为 `"doubao-chat"`。

```
TaskTool(
  subagent_type="doubao-chat",
  description="按最终剪辑脚本匹配每段原片时间段",
  prompt="请为以下短剧最终剪辑脚本匹配原片画面时间段。

⚠️ 重要：首次调用 doubao-chat 工具时，必须传入 file_path 参数上传视频：
doubao-chat(file_path=\"<原片的绝对路径>\", prompt=\"...\")
后续追问使用返回的 session_id 继续对话，不需要再传 file_path。

## 对话时间轴（ASR 转录摘要）
{从 transcript.json 提取的关键对话和时间点}

## 最终剪辑脚本
| 段落 | 播放方式 | 文案/台词 | 音频时长 |
|------|----------|-----------|----------|
| 15   | 解说配音 | 回到娘家，怀孕的嫂子当着全家人的面说—— | 4.0s |
| 16   | 播放原片 | 房子这么小，小姑子带个拖油瓶回来，挤得我胎都不稳了。 | - |
| 17   | 解说配音 | 这话不是抱怨，是驱逐令。 | 3.0s |
...

## 匹配规则
1. 输出必须与最终脚本段落顺序一一对应，每段只输出 1 个 `video` 时间段
2. `解说配音` 段：
   - 选择能承载该段 TTS 的画面
   - `video` 时长必须 >= 该段 `audio_duration`
   - 画面内容需与文案描述匹配
3. `播放原片` 段：
   - 选择原片中该句台词 / 该段表演真实发生的时间段
   - 必须覆盖完整的关键台词和关键表演，不能只截半句
   - 保留原声，不生成 TTS
4. 同一 source_index 下所有 `video` 时间段不能重叠
5. 整体按剧情时序推进，不跨时间线
6. 如果某句是否适合保留原声存在不确定，优先选择更有代入感的一侧，并在 `match_reason` 中说明

## 输出格式
最终请输出 JSON 数组：
[
  {
    \"segment\": 15,
    \"play_mode\": \"tts\",
    \"source_index\": 1,
    \"text\": \"回到娘家，怀孕的嫂子当着全家人的面说——\",
    \"audio_duration\": 4.0,
    \"video\": {\"start\": 165.0, \"end\": 169.2},
    \"match_reason\": \"娘家冲突开场画面能承载铺垫解说\"
  },
  {
    \"segment\": 16,
    \"play_mode\": \"original\",
    \"source_index\": 1,
    \"text\": \"房子这么小，小姑子带个拖油瓶回来，挤得我胎都不稳了。\",
    \"use_original_audio\": true,
    \"video\": {\"start\": 169.2, \"end\": 175.8},
    \"match_reason\": \"该时间段包含嫂子完整原话和情绪表演，适合直接播放原片\"
  }
]

> 多源时：对每个原片独立调用 doubao-chat subagent。每段文案已通过 final_script.md 中的“源文件”列标注来源，subagent 只需在对应视频中匹配。"
)
```

## 阶段 B：校验匹配结果

从 subagent 返回的结果中提取 JSON，逐项校验：

| 校验项 | 处理方式 |
|--------|---------|
| JSON 解析失败 | 从返回文本中提取 JSON 块，去除 markdown 包裹 |
| 缺少某段匹配 | 回退到 `final_script.md`，按缺失段落补齐 |
| `tts` 段时长不足 | 执行“音频超长修复流程” |
| `original` 段未覆盖完整台词 | 向前/向后扩展时间，直到完整覆盖关键台词 |
| 时间段重叠 | 按同源顺序向后偏移冲突段，修正后重新验证 |

### 音频超长修复流程

当某段 `play_mode = tts` 且 `video` 时长 < `audio_duration`，执行以下流程：

**第一步 — 尝试延长**：
- 计算目标结束时间：`needed_end = video.start + audio_duration`
- 检查 `needed_end` 是否 <= 该源视频总时长
- 检查延长后的 `[video.start, needed_end]` 是否与同一 `source_index` 下其他已使用时间段重叠
- **无冲突** → 直接延长：`video.end = needed_end`，修复完成
- **有冲突** → 进入第二步

**第二步 — 重写文案并重新生成音频**：
1. 计算该 segment 可用的最大画面时长
2. 将该 segment 标记为“需重写”，记录可用最大时长
3. 回退到步骤 5，仅重写该 segment 的解说文案，要求控制在可用时长内（按 1 秒约 4 字估算字数上限）
4. 回退到步骤 6，仅重新生成该 segment 的配音音频
5. 用新的 `audio_duration` 重新修正 `video.end = video.start + audio_duration`
6. 重新执行全部校验

> 如果重写后仍超长，重复第二步直到通过。最多重试 2 次，仍失败则报错停止并提示用户手动调整。

## 强制验证规则

全部通过才能继续：

1. **段落完整**：`final_script.md` 中每个段落在 `scene_matching.json` 中都必须恰好出现一次
2. **同源全局无重叠**：同一 `source_index` 下所有 `video` 时间段按 start 排序后，前一段的 end 不能超过后一段的 start
3. **时间边界**：所有时间段的 start >= 0 且 end <= 对应源视频总时长
4. **TTS 时长覆盖**：所有 `play_mode = tts` 的段落都满足 `video.end - video.start >= audio_duration`
5. **原台词完整**：所有 `play_mode = original` 的段落都覆盖完整台词/关键表演，`use_original_audio = true`

校验通过后，将结果写入 `<项目名>/analysis/scene_matching.json`。

**产出**：
- `<项目名>/analysis/scene_matching.json` — 逐段匹配结果

**状态更新**：`steps.7_matching = "completed"`，`segments[].video` 填充，`used_time_ranges` 更新
