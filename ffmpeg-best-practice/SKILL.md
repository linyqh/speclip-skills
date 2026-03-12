---
name: ffmpeg-best-practice
description: >
  Production-ready FFmpeg playbook for video editing tasks in Speclip. Use when
  the user needs robust FFmpeg command construction, multi-clip compositing,
  audio mixing, subtitle burning/muxing, VFR-to-CFR normalization, and reliable
  fallbacks for diverse source media.
---

# FFmpeg Best Practice

Use this skill when the task requires direct FFmpeg work and reliability matters more than shorthand.

## Scope

- Final exports and intermediate transcodes
- Clip trimming and concatenation
- Audio mixing (voiceover + BGM + source audio)
- Resolution/FPS normalization
- Subtitle burn-in or soft subtitle muxing
- Hardware-accelerated exports with safe fallback
- Playback/web optimization (`+faststart`)

## Trigger Phrases

- "ffmpeg 报错"
- "多段素材拼接"
- "导出最终视频"
- "加配音和背景音乐"
- "有的视频没有音轨"
- "VFR/CFR"
- "字幕烧录"

## Workflow

1. Probe input files with `ffprobe` before writing commands.
2. Detect OS and available encoders with `ffmpeg -hide_banner -encoders` before choosing a re-encode path.
3. Decide path: stream-copy vs re-encode.
4. Prefer hardware video encoding for exports when available; keep software fallback ready.
5. Handle audio presence explicitly (`a?` optional mapping or generated silence).
6. Build command with deterministic output codec/muxing.
7. Run once, inspect error, apply targeted fallback.
8. Return command, output path, and why key flags were chosen.

## Input Checklist (Required)

Run for every input:

```bash
ffprobe -v error -hide_banner -show_streams -show_format -of json "INPUT"
```

And probe encoder availability once per machine/session:

```bash
ffmpeg -hide_banner -encoders
ffmpeg -hide_banner -hwaccels
```

Check:

- Has video stream?
- Has audio stream?
- Resolution and sample aspect ratio
- Frame rate (`avg_frame_rate`, `r_frame_rate`)
- Duration
- Rotation metadata
- Container/codec compatibility with target output
- Available H.264/H.265 hardware encoders on this machine
- Whether this job really needs hardware decode, or only hardware encode

## Decision Tree

1. Need frame-accurate cuts, filters, overlays, subtitles, speed changes, or mixing?
- Yes: re-encode.
- No: stream-copy is preferred.

2. Multiple clips with exactly matching codecs/time bases/resolution?
- Yes: concat demuxer route.
- No or uncertain: concat filter route (re-encode).

3. Any input may lack audio?
- Yes: always use optional mapping (`-map 0:a?`) or create silence (`anullsrc`) where needed.

4. Target is browser/mobile/web delivery?
- Yes: prefer H.264 hardware encoder for the current OS if available; otherwise use `libx264`. Always keep `-pix_fmt yuv420p -movflags +faststart` and `-c:a aac`.

5. Source is VFR and timeline sync matters?
- Yes: normalize to CFR (`-r TARGET_FPS`, plus sync settings).

6. Are you exporting on macOS or Windows?
- macOS: prefer `h264_videotoolbox` for H.264 delivery, `hevc_videotoolbox` only when HEVC is explicitly required.
- Windows: prefer `h264_nvenc`, then `h264_qsv`, then `h264_amf`; use HEVC variants only when HEVC is explicitly required.
- Any platform / encoder unavailable: fall back to `libx264`.

## Platform Codec Policy

Default principle:

- Prioritize hardware video encoding for speed when the encoder is available.
- Do **not** require hardware decode by default. For filter-heavy graphs (subtitles, concat filter, scale/pad, overlays, audio mix), software decode + hardware encode is usually the most portable path.
- Keep audio on `aac` unless the task explicitly requires another codec.
- For browser/mobile delivery, default to H.264 + AAC in MP4.

Preferred H.264 encoder order:

- macOS: `h264_videotoolbox` -> `libx264`
- Windows: `h264_nvenc` -> `h264_qsv` -> `h264_amf` -> `libx264`

Preferred HEVC encoder order when explicitly requested:

- macOS: `hevc_videotoolbox` -> `libx265`
- Windows: `hevc_nvenc` -> `hevc_qsv` -> `hevc_amf` -> `libx265`

Quality control guidance:

- `libx264` / `libx265`: use `-crf` and `-preset`.
- `*_videotoolbox`: prefer bitrate-driven settings such as `-b:v`, `-maxrate`, `-bufsize`; avoid assuming `-crf` parity.
- `*_nvenc`: prefer `-cq` or bitrate-driven settings with a preset.
- `*_qsv` / `*_amf`: prefer bitrate-driven settings unless you have validated quality knobs for the local FFmpeg build.

When portability matters more than speed, or when the chosen hardware encoder errors out, immediately fall back to `libx264`.

## Command Templates

Use variables:
- `IN`, `IN1`, `IN2`, `OUT`, `START`, `END`, `FPS`, `W`, `H`, `VO`, `BGM`, `SUB`, `VENC`, `VBITRATE`, `VMAXRATE`, `VBUFSIZE`

### 0) Encoder detection and selection

Pick the first encoder that exists in `ffmpeg -hide_banner -encoders`:

```text
macOS H.264: h264_videotoolbox -> libx264
Windows H.264: h264_nvenc -> h264_qsv -> h264_amf -> libx264
macOS HEVC: hevc_videotoolbox -> libx265
Windows HEVC: hevc_nvenc -> hevc_qsv -> hevc_amf -> libx265
```

Do not force `-hwaccel auto` unless you have verified that the full pipeline works with the required filters.

### 0.1) Hardware-accelerated web-safe export (generic pattern)

```bash
ffmpeg -y -i "IN" \
  -c:v VENC -pix_fmt yuv420p -b:v VBITRATE -maxrate VMAXRATE -bufsize VBUFSIZE \
  -c:a aac -b:a 192k -ar 48000 -ac 2 \
  -map 0:v:0 -map 0:a? -movflags +faststart "OUT"
```

Examples:

```text
macOS:   VENC=h264_videotoolbox VBITRATE=6M VMAXRATE=8M VBUFSIZE=12M
Windows: VENC=h264_nvenc        VBITRATE=6M VMAXRATE=8M VBUFSIZE=12M
Fallback: switch to template 12 (`libx264`) if the encoder is unavailable or fails.
```

### 1) Fast trim (stream copy, keyframe aligned)

```bash
ffmpeg -y -ss START -to END -i "IN" -c copy -map 0:v:0 -map 0:a? -movflags +faststart "OUT"
```

### 2) Accurate trim (re-encode, frame accurate)

```bash
ffmpeg -y -ss START -to END -i "IN" \
  -c:v libx264 -preset medium -crf 20 \
  -c:a aac -b:a 192k \
  -map 0:v:0 -map 0:a? -movflags +faststart "OUT"
```

### 3) Concat demuxer (same encoding parameters)

Create `list.txt`:

```text
file '/abs/path/clip1.mp4'
file '/abs/path/clip2.mp4'
file '/abs/path/clip3.mp4'
```

Then:

```bash
ffmpeg -y -f concat -safe 0 -i "list.txt" -c copy -movflags +faststart "OUT"
```

### 4) Concat filter (mixed sources, robust path)

```bash
ffmpeg -y -i "IN1" -i "IN2" \
  -filter_complex "[0:v]scale=W:H:force_original_aspect_ratio=decrease,pad=W:H:(ow-iw)/2:(oh-ih)/2[v0]; \
                   [1:v]scale=W:H:force_original_aspect_ratio=decrease,pad=W:H:(ow-iw)/2:(oh-ih)/2[v1]; \
                   [v0][0:a?][v1][1:a?]concat=n=2:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" \
  -c:v libx264 -preset medium -crf 21 \
  -c:a aac -b:a 192k -movflags +faststart "OUT"
```

If optional audio concat fails, use template 8 (silence pad) first.

### 5) Voiceover + BGM + source audio mix

```bash
ffmpeg -y -i "IN" -i "VO" -i "BGM" \
  -filter_complex "[2:a]volume=0.25[bgm]; \
                   [1:a]volume=1.00[vo]; \
                   [0:a?][vo][bgm]amix=inputs=3:duration=longest:dropout_transition=2[mix]" \
  -map 0:v:0 -map "[mix]" \
  -c:v copy -c:a aac -b:a 192k -movflags +faststart "OUT"
```

If source has no audio, switch `[0:a?]` to silence source (template 8).

### 6) Loudness-safe ducking (BGM under voice)

```bash
ffmpeg -y -i "VO" -i "BGM" \
  -filter_complex "[1:a]volume=0.35,sidechaincompress=threshold=0.02:ratio=8:attack=20:release=300:makeup=1[bgmduck]; \
                   [0:a][bgmduck]amix=inputs=2:duration=longest[mix]" \
  -map "[mix]" -c:a aac -b:a 192k "OUT"
```

### 7) Normalize to target canvas (portrait/landscape safe pad)

```bash
ffmpeg -y -i "IN" \
  -vf "scale=W:H:force_original_aspect_ratio=decrease,pad=W:H:(ow-iw)/2:(oh-ih)/2,setsar=1" \
  -c:v libx264 -preset medium -crf 21 \
  -c:a aac -b:a 192k -map 0:v:0 -map 0:a? -movflags +faststart "OUT"
```

### 8) Generate silence when audio missing

```bash
ffmpeg -y -i "IN" -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=48000 \
  -shortest -map 0:v:0 -map 1:a:0 \
  -c:v copy -c:a aac -b:a 128k -movflags +faststart "OUT"
```

### 9) VFR to CFR for timeline stability

```bash
ffmpeg -y -i "IN" \
  -vf "fps=FPS" -r FPS \
  -c:v libx264 -preset medium -crf 20 \
  -c:a aac -b:a 192k -map 0:v:0 -map 0:a? -movflags +faststart "OUT"
```

### 10) Burn subtitles (hard subtitles)

```bash
ffmpeg -y -i "IN" -vf "subtitles='SUB'" \
  -c:v libx264 -preset medium -crf 19 \
  -c:a aac -b:a 192k -map 0:v:0 -map 0:a? -movflags +faststart "OUT"
```

### 11) Mux soft subtitles (selectable track)

```bash
ffmpeg -y -i "IN" -i "SUB.srt" \
  -map 0:v:0 -map 0:a? -map 1:0 \
  -c:v copy -c:a copy -c:s mov_text \
  -metadata:s:s:0 language=chi -movflags +faststart "OUT"
```

### 12) Web-safe final export baseline

```bash
ffmpeg -y -i "IN" \
  -c:v libx264 -preset medium -crf 21 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -ar 48000 -ac 2 \
  -map 0:v:0 -map 0:a? -movflags +faststart "OUT"
```

Use this as the deterministic software fallback on both macOS and Windows.

## Error -> Fallback Playbook

### `matches no streams` / `Stream map ... matches no streams`

- Cause: mapped audio stream absent.
- Fix order:
1. Replace `-map 0:a` with `-map 0:a?`.
2. If downstream filter requires audio, inject silence with `anullsrc`.

### `Non-monotonous DTS` / timestamp issues

- Cause: concat/timebase mismatch.
- Fix order:
1. Re-encode concat route (template 4), avoid copy concat.
2. Add `-fflags +genpts` when needed.

### `concat` fails due to parameter mismatch

- Cause: resolution/fps/codec mismatch.
- Fix order:
1. Pre-normalize each clip to a mezzanine profile (`libx264 + aac`, same fps/resolution).
2. Then concat demuxer or concat filter.

### Hardware encoder unavailable / initialization failed

- Cause: local FFmpeg build lacks the encoder, driver unavailable, remote session/VM limitations, unsupported pixel format, or encoder-specific option mismatch.
- Fix order:
1. Retry with the next encoder in the platform priority list.
2. Remove any encoder-specific quality flags that do not apply to the new encoder.
3. Fall back to `libx264` immediately if the job is urgent or portability matters more than speed.

### Hardware decode/filter graph instability

- Cause: `-hwaccel` path does not cooperate with subtitles, scale/pad, concat filter, overlays, or mixed CPU filters.
- Fix order:
1. Drop explicit hardware decode.
2. Keep software decode + filter graph on CPU.
3. If available, still use hardware **encode** for the final output.

### Audio drift after long output

- Cause: VFR + mixed sources.
- Fix order:
1. Normalize main video to CFR first (template 9).
2. Then mix audio.

### Subtitle path parse failures

- Cause: quoting/escaping on spaces or special chars.
- Fix:
1. Use absolute path.
2. Quote path carefully in filter (`subtitles='...path...'`).

## Output Contract (Always Return)

After execution, return:

1. Exact command used (single-line and formatted block)
2. Output path
3. Why key flags were chosen (`-map 0:a?`, `+faststart`, `crf`, `fps`, `scale/pad`)
4. Any fallback applied and reason

If re-encoding, also state:

5. Which encoder was selected and why (`h264_videotoolbox`, `h264_nvenc`, `h264_qsv`, `h264_amf`, or `libx264`)
6. Whether hardware decode was intentionally avoided for filter compatibility

## Safety Constraints

- Never overwrite source media in place.
- Prefer deterministic absolute output paths.
- Use `-y` only when overwrite is explicitly intended.
- Respect external directory permissions before writing output.
- For uncertain stream topology, probe first; do not guess.

## Practical Defaults

- Video encoder priority:
  - macOS: `h264_videotoolbox`, fallback `libx264`
  - Windows: `h264_nvenc`, fallback `h264_qsv`, then `h264_amf`, then `libx264`
- Software video fallback: `libx264`, `preset=medium`, `crf=20~22`
- Hardware H.264 starting point: `-b:v 6M -maxrate 8M -bufsize 12M`
- Audio: `aac`, `192k`, `48kHz`, stereo
- Web MP4: `-pix_fmt yuv420p -movflags +faststart`
- Mixed source projects: re-encode path by default
