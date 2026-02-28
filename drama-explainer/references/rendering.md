# 步骤 8-9：截取视频、合并与渲染

## 步骤 8：截取视频与合并

### 阶段 A：批量截取视频片段

根据 `scene_matching.json` 的匹配结果，逐段截取解说画面和原片片段：

```
# 解说画面（静音，时长 = 音频时长）
# 多源时根据 source_index 选择对应原片
trimvideo(input_path=<原片[source_index]>, start=<vo_video.start>, end=<vo_video.end>,
          output_path=<项目名>/clips/voiceover/clip_vo_01.mp4)

# 原片片段（保留原声，时长灵活）
trimvideo(input_path=<原片[source_index]>, start=<orig_video.start>, end=<orig_video.end>,
          output_path=<项目名>/clips/original/clip_orig_01.mp4)
```

> **多源时**：每个 segment 的 `source_index` 指明从哪个原片截取。从 `state.json` 的 `project.sources` 数组中取对应路径。

### 阶段 B：合并解说片段

将每个解说画面与对应配音合并为独立文件：

```bash
# 解说片段：用配音替换原声
ffmpeg -y -i <项目名>/clips/voiceover/clip_vo_01.mp4 \
  -i <项目名>/audio/vo_01.mp3 \
  -c:v copy -c:a aac -map 0:v -map 1:a -shortest \
  <项目名>/clips/merged/merged_vo_01.mp4

# 原片片段：保留原声，无需处理
```

**产出**：
- `<项目名>/clips/voiceover/clip_vo_*.mp4` — 解说画面片段
- `<项目名>/clips/original/clip_orig_*.mp4` — 原片片段
- `<项目名>/clips/merged/merged_vo_*.mp4` — 合并后的解说片段

**状态更新**：`steps.8_clips = "completed"`，`segments[].status = "merged"`

## 步骤 9：渲染输出

**重要**：不要使用 `adelay` + `amix` 方式，会导致后半部分音画不同步。

正确方法是 **先合并单个片段，再统一拼接**：

```bash
ffmpeg -y \
  -i <项目名>/clips/merged/merged_vo_01.mp4 \
  -i <项目名>/clips/original/clip_orig_01.mp4 \
  -i <项目名>/clips/merged/merged_vo_02.mp4 \
  -i <项目名>/clips/original/clip_orig_02.mp4 \
  ... \
  -filter_complex "\
    [0:v]fps=25,format=yuv420p[v0]; \
    [0:a]aformat=sample_rates=44100:channel_layouts=stereo[a0]; \
    [1:v]fps=25,format=yuv420p[v1]; \
    [1:a]aformat=sample_rates=44100:channel_layouts=stereo[a1]; \
    ... \
    [v0][a0][v1][a1]...concat=n=12:v=1:a=1[outv][outa] \
  " \
  -map "[outv]" -map "[outa]" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k \
  <项目名>/output/output.mp4
```

**关键点**：
1. **先合并后拼接**：每个解说片段先与配音合并，避免多轨道同步问题
2. **统一音频格式**：所有音频转换为 `44100Hz stereo`，避免格式不兼容
3. **使用 concat filter**：一次性拼接视频和音频，确保同步精确

**产出**：
- `<项目名>/output/output.mp4` — 最终成片

**状态更新**：`steps.9_render = "completed"`
