# 步骤 9-11：渲染、拼接与交接

## 基本原则

- 最终渲染只读取 `scripts/storyboard.json`
- 不读取 `final_script.md` 作为程序输入
- 不使用 `rendervideo` 做最终混合渲染

## 步骤 9：逐段渲染

输入前提：
- `scripts/storyboard.json`
- `audio/*.mp3`（仅 `mode = voiceover` 段存在）

### 阶段 A：逐段截取

```bash
trimvideo(input_path=<segment.source_path>, start=<segment.start>, end=<segment.end>, \
          output_path=<项目名>/clips/raw/clip_015.mp4)
```

要求：
- 一切路径和时间从 `storyboard.json` 读取
- 多源时直接读 `source_path`

### 阶段 B：标准化与音频合成

参数来源：从 `mediainfo.json` 或 `state.json.media.sources[*]` 读取 `SRC_RES` 和 `SRC_FPS`。

**`mode = voiceover`**：
- 使用原片画面
- 静音原片音频
- 叠加 TTS

**`mode = original`**：
- 保留原片视频和原声
- 若无音轨，用 `anullsrc`

### 产出

- `clips/raw/clip_*.mp4`
- `clips/merged/merged_*.mp4`

回写：
- `storyboard.json.segments[].status = "merged"`

## 步骤 10：最终拼接

使用 concat demuxer 拼接 `clips/merged/`：

```bash
ffmpeg -y -f concat -safe 0 -i <项目名>/filelist.txt \
  -c copy \
  -movflags +faststart \
  <项目名>/output/output.mp4
```

回写：
- `storyboard.json.output.final_video`
- 对应 segment 最终状态

## 步骤 11：字幕交接（可选）

若用户需要字幕，交接以下输入给后续字幕 skill：
- `output/output.mp4`
- `scripts/final_script.md`
- `scripts/storyboard.json`
- 用户的字幕样式要求
