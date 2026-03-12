# 步骤 8-10：逐段渲染、拼接与字幕分支

> **⚠️ 不要使用 `rendervideo` 工具做最终渲染。**
> `rendervideo` 的 timeline 格式不适合当前工作流：它无法可靠表达“有些段落走 TTS，有些段落直接保留原片原声”的混合结构。
> 必须按照下方的 FFmpeg 流程手动渲染：先逐段标准化（步骤 8），再无损拼接成片（步骤 9），最后可选进入字幕分支（步骤 10）。

## 步骤 8：按最终脚本逐段渲染

### 输入前提

- `scripts/final_script.md`：定义最终段落顺序与 `play_mode`
- `analysis/scene_matching.json`：给出每段对应的 `video` 时间段
- `audio/vo_XXX.mp3`：仅对 `play_mode = tts` 的段落存在

### 阶段 A：逐段截取原始视频

根据 `scene_matching.json` 的匹配结果，每个最终段落只截取 **1 个** 原始片段：

```bash
trimvideo(input_path=<原片[source_index]>, start=<video.start>, end=<video.end>, \
          output_path=<项目名>/clips/raw/clip_015.mp4)
```

> **多源时**：`source_index` 指明从哪个原片截取。从 `state.json` 的 `project.sources` 数组中取对应路径。

### 阶段 B：标准化与音频合成

将所有片段统一为相同的视频参数，为步骤 9 的无损拼接做准备。

> **参数来源**：从 `mediainfo.json` 或 `state.json.media.sources[*]` 读取源视频分辨率（`SRC_RES`）和帧率（`SRC_FPS`）。不要硬编码帧率。

**B1 — `play_mode = tts`**：标准化视频 + 用配音替换原声

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

**B2 — `play_mode = original`**：标准化视频 + 保留原声

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

> 如果 `play_mode = original` 的片段没有音频轨道，用 `anullsrc` 生成静音轨：将 `[0:a]aformat=...` 替换为 `anullsrc=r=44100:cl=stereo[a]`。

### 标准化参数说明

| 参数 | 作用 | 说明 |
|------|------|------|
| `fps=<SRC_FPS>` | 统一帧率 | 从源视频读取，避免硬编码 |
| `scale=<SRC_RES>` | 统一分辨率 | `force_original_aspect_ratio=decrease` 保持宽高比 |
| `pad=<SRC_RES>:-1:-1` | 填充黑边 | 分辨率不足时居中填充，确保输出尺寸一致 |
| `format=yuv420p` | 统一像素格式 | 兼容性最佳 |
| `aformat=sample_rates=44100:channel_layouts=stereo` | 统一音频格式 | 防止 concat 时音频格式不匹配 |
| `-c:v libx264 -preset fast -crf 23` | 视频编码 | H.264 编码，质量与速度平衡 |
| `-c:a aac -b:a 128k` | 音频编码 | AAC 128kbps |

### 产出

- `clips/raw/clip_*.mp4` — 按最终脚本逐段截取的原始片段
- `clips/merged/merged_*.mp4` — 标准化后的最终片段
  - `tts` 段：视频来自原片，音频来自 TTS
  - `original` 段：视频与音频都来自原片

**状态更新**：`steps.8_clips = "completed"`，`segments[].status = "merged"`

## 步骤 9：无损拼接最终成片

所有片段已在步骤 8 标准化为相同的编解码参数，使用 **concat demuxer** 无损拼接。

### 第一步：生成文件列表

```bash
cat > <项目名>/filelist.txt << 'EOF'
file 'clips/merged/merged_015.mp4'
file 'clips/merged/merged_016.mp4'
file 'clips/merged/merged_017.mp4'
file 'clips/merged/merged_018.mp4'
...
EOF
```

### 第二步：执行拼接

```bash
ffmpeg -y -f concat -safe 0 -i <项目名>/filelist.txt \
  -c copy \
  -movflags +faststart \
  <项目名>/output/output.mp4
```

### 关键点

1. **只拼接 `clips/merged/` 下的文件**，不要直接拼接 `clips/raw/`
2. **concat demuxer + `-c copy`**：步骤 8 已统一参数，此处直接流复制，速度快且无额外质量损失
3. **`-movflags +faststart`**：支持网络播放边下边播
4. **不要使用 `adelay` + `amix`**：容易导致混合结构成片后半段不同步
5. **不要使用 concat filter**：没有必要重新编码全部片段

**产出**：
- `<项目名>/output/output.mp4` — 最终成片

**状态更新**：`steps.9_render = "completed"`

## 步骤 10：字幕确认与交接（可选）

渲染完成后，必须先问用户是否需要字幕。

### 方向判断规则

- `height > width` → `portrait`（竖屏）
- `width >= height` → `landscape`（横屏）

优先读取最终输出尺寸；如果还未读取，则使用首个源视频尺寸作为目标方向。

### 决策流程

1. 读取尺寸并得出 `orientation`
2. 询问用户是否需要字幕
3. 若用户不需要：直接交付 `output/output.mp4`
4. 若用户需要：
   - 将以下信息交给后续专门的字幕 skill
   - `orientation`
   - `<项目名>/output/output.mp4`
   - `<项目名>/scripts/final_script.md`
   - `<项目名>/analysis/scene_matching.json`
   - 用户对字幕的额外要求（如双语、关键词强调、软字幕/硬字幕）

> **注意**：当前 `drama-explainer` 只负责做字幕决策与交接，不负责内置具体字幕样式。具体烧录方案由后续字幕 skill 决定。

**状态更新**：
- 不需要字幕：`steps.10_subtitles = "skipped"`
- 需要字幕并已交接：`steps.10_subtitles = "completed"`
