# 步骤 8-9：截取视频、标准化合并与渲染

> **⚠️ 不要使用 `rendervideo` 工具做最终渲染。**
> rendervideo 的 timeline 格式不支持解说配音叠加，会导致成片无解说音频。
> 必须按照下方的 FFmpeg 流程手动渲染：先标准化合并（阶段 B），再无损拼接成片（步骤 9）。

## 步骤 8：截取视频与标准化合并

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

### 阶段 B：标准化与合并

将所有片段统一为相同的视频参数，为步骤 9 的无损拼接做准备。

> **参数来源**：从 `mediainfo.json` 读取源视频的分辨率（`SRC_RES`，如 `1920:1080`）和帧率（`SRC_FPS`，如 `30`），确保输出与原片一致。不要硬编码帧率（如 fps=25）。

**B1 — 解说片段**：标准化视频参数 + 用配音替换原声：

```bash
ffmpeg -y -i <项目名>/clips/voiceover/clip_vo_01.mp4 \
  -i <项目名>/audio/vo_01.mp3 \
  -filter_complex "\
    [0:v]fps=<SRC_FPS>,scale=<SRC_RES>:force_original_aspect_ratio=decrease,\
    pad=<SRC_RES>:-1:-1,format=yuv420p[v]; \
    [1:a]aformat=sample_rates=44100:channel_layouts=stereo[a]" \
  -map "[v]" -map "[a]" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k -shortest \
  <项目名>/clips/merged/merged_vo_01.mp4
```

**B2 — 原片片段**：标准化视频参数 + 保留原声：

```bash
ffmpeg -y -i <项目名>/clips/original/clip_orig_01.mp4 \
  -filter_complex "\
    [0:v]fps=<SRC_FPS>,scale=<SRC_RES>:force_original_aspect_ratio=decrease,\
    pad=<SRC_RES>:-1:-1,format=yuv420p[v]; \
    [0:a]aformat=sample_rates=44100:channel_layouts=stereo[a]" \
  -map "[v]" -map "[a]" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k \
  <项目名>/clips/merged/merged_orig_01.mp4
```

> 如果原片片段没有音频轨道，用 `anullsrc` 生成静音轨：将 `[0:a]aformat=...` 替换为 `anullsrc=r=44100:cl=stereo[a]`。

### 标准化参数说明

| 参数 | 作用 | 说明 |
|------|------|------|
| `fps=<SRC_FPS>` | 统一帧率 | 从 `mediainfo.json` 读取，避免硬编码 |
| `scale=<SRC_RES>` | 统一分辨率 | `force_original_aspect_ratio=decrease` 保持宽高比 |
| `pad=<SRC_RES>:-1:-1` | 填充黑边 | 分辨率不足时居中填充，确保输出尺寸一致 |
| `format=yuv420p` | 统一像素格式 | 兼容性最佳的像素格式 |
| `aformat=sample_rates=44100:channel_layouts=stereo` | 统一音频格式 | 防止 concat 时音频格式不匹配 |
| `-c:v libx264 -preset fast -crf 23` | 视频编码 | H.264 编码，质量与速度平衡 |
| `-c:a aac -b:a 128k` | 音频编码 | AAC 128kbps，标准质量 |

**产出**：
- `clips/voiceover/clip_vo_*.mp4` — 解说画面原始截取（中间产物）
- `clips/original/clip_orig_*.mp4` — 原片片段原始截取（中间产物）
- `clips/merged/merged_vo_*.mp4` — **标准化解说片段（含配音）**
- `clips/merged/merged_orig_*.mp4` — **标准化原片片段（含原声）**

**状态更新**：`steps.8_clips = "completed"`，`segments[].status = "merged"`

## 步骤 9：渲染输出

所有片段已在步骤 8 阶段 B 标准化为相同的编解码参数，使用 **concat demuxer** 无损拼接。

**第一步 — 生成文件列表**：

```bash
cat > <项目名>/filelist.txt << 'EOF'
file 'clips/merged/merged_vo_01.mp4'
file 'clips/merged/merged_orig_01.mp4'
file 'clips/merged/merged_vo_02.mp4'
file 'clips/merged/merged_orig_02.mp4'
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

### 关键点

1. **concat demuxer + `-c copy`**：步骤 8 已统一所有片段的编解码参数，此处直接流复制，速度极快且无质量损失
2. **`-movflags +faststart`**：将 MP4 元数据前置，支持网络播放时边下载边播放
3. **不要使用 `adelay` + `amix`**：会导致后半部分音画不同步
4. **不要使用 concat filter**：已无必要重新编码，且输入数量多时 filter_complex 会过于复杂
5. **不要使用 `rendervideo` 工具**：timeline 格式不支持解说配音叠加

### 为什么不用 concat filter？

| 维度 | concat filter（旧方案） | concat demuxer（当前方案） |
|------|--------------------------|---------------------------|
| 编码 | 重新编码所有视频 | `-c copy` 直接复制流 |
| 速度 | 慢（取决于视频总时长） | 秒级完成 |
| 质量 | 每次编码有微小损失 | 零损失（位精确复制） |
| 复杂度 | N 个输入需 2N 行滤镜链 | 固定 2 行命令 |
| 扩展性 | 20+ 片段时命令爆炸 | 文件列表无上限 |

> 前提：步骤 8 阶段 B 必须将所有片段标准化为**完全相同**的编解码参数（分辨率、帧率、像素格式、音频采样率、声道数）。否则 concat demuxer 会产生花屏或音画不同步。

**产出**：
- `<项目名>/output/output.mp4` — 最终成片

**状态更新**：`steps.9_render = "completed"`
