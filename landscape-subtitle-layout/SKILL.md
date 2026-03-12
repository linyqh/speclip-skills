---
name: landscape-subtitle-layout
description: 横屏视频字幕位置与参数配置 skill。适用于 16:9 或其他横屏视频的字幕烧录、ASS 样式调整、底部安全区控制，以及“字幕太高/太低/太贴边/太挤”这类字幕排版请求。
---

# 横屏视频字幕位置与参数

用于 **横屏视频** 的字幕排版与烧录决策。重点不是“随便给一个字幕命令”，而是稳定回答：字幕应该放多高、字号多大、左右边距多少、两行怎么控、什么时候该抬高字幕避开片尾条或 UI。

## 什么时候用

- 用户明确说是 **横屏 / 16:9 / landscape** 视频
- 用户要调字幕位置：**再低一点 / 再高一点 / 别挡画面 / 别贴底边**
- 用户要烧录字幕，且希望给出 **ASS 参数** 而不是只给一个笼统 FFmpeg 命令
- 任务涉及 `.srt → .ass → FFmpeg burn-in`

如果是竖屏 / 9:16，请改用 `portrait-subtitle-layout`。

## 默认基准

以 **1920x1080** 横屏为基准，默认采用 **底部居中** 字幕：

- `Alignment = 2`（bottom-center）
- `FontSize = 90`
- `MarginV = 60`
- `MarginL = 48`
- `MarginR = 48`
- `Outline = 2`
- `Shadow = 1`
- `WrapStyle = 0`
- `MaxLineLength = 18`
- 目标：**最多两行**，优先稳读，不靠缩字号硬塞

这套参数与 Speclip 当前内置横屏字幕基线保持一致，适合访谈、剧情、解说、课程、屏录讲解等大多数横屏场景。

## 缩放公式

如果分辨率不是 1920x1080，按下面规则缩放：

```text
fontSize = clamp(round(90 * H / 1080), 54, 180)
marginV  = clamp(round(60 * H / 1080), 40, 120)
marginL  = clamp(round(48 * W / 1920), 32, 120)
marginR  = clamp(round(48 * W / 1920), 32, 120)
outline  = clamp(round(2 * H / 1080), 2, 4)
shadow   = clamp(round(1 * H / 1080), 1, 2)
```

其中：

- `W` = 视频宽度
- `H` = 视频高度

## 位置调整规则

### 1) 默认横屏位置

- 优先保持 `Alignment = 2`
- 常规内容用 `MarginV = 60`
- 这是“靠下但不贴底”的安全值

### 2) 用户说“字幕再低一点”

优先把 `MarginV` 调到：

- `40–55`：更贴近传统电影/访谈字幕区
- 不建议低于 `40`，否则容易贴边、压黑边、压播放器控件

### 3) 用户说“字幕再高一点”

优先把 `MarginV` 调到：

- `80–100`：轻度上移
- `100–120`：明显上移，适合底部有 banner、logo、章节条、双语第二轨

### 4) 左右太挤 / 英文长句太容易贴边

优先处理顺序：

1. 先增大 `MarginL / MarginR`
2. 再缩短每行长度
3. 最后才缩字号

推荐区间：

- 常规：`48`
- 更稳妥：`56–72`
- 超高分辨率或双语：`72–96`

### 5) 行太长、读起来累

- 默认 `MaxLineLength = 18`
- 节奏快、口语短句：保持 `18`
- 英文长句或双语：可放宽到 `20`
- 画面信息密集：宁可拆句，也不要把字号压得太小

## ASS 建议参数

标准样式行可直接按下面结构生成：

```text
Style: Default,PingFang SC,90,&H00FFFFFF,&H000000FF,&H00000000,&H66000000,-1,0,0,0,100,100,0,0,1,2,1,2,48,48,60,1
```

字段重点：

- `Outline = 2`
- `Shadow = 1`
- `Alignment = 2`
- `MarginL = 48`
- `MarginR = 48`
- `MarginV = 60`

如果平台不是 macOS，可换成更合适的字体，但保持同级别字重和可读性。

## 推荐工作流

1. 先拿到 `.srt`
2. 优先转成 `.ass`
3. 按横屏参数修改样式
4. 再用 FFmpeg 烧录

不要在最终烧录流程里直接把 `.srt` 当作唯一排版来源；需要稳定位置控制时，优先 `.ass`。

## FFmpeg 烧录示例

```bash
ffmpeg -y -i "IN.mp4" -vf "subtitles='SUB.ass'" \
  -c:v libx264 -preset medium -crf 19 \
  -c:a aac -b:a 128k -map 0:v:0 -map 0:a? -movflags +faststart "OUT.mp4"
```

## 常见决策

### 电影感 / 访谈感

- `Alignment = 2`
- `MarginV = 40–55`
- `FontSize` 不要过大

### 教程 / 屏录 / 底部有控件

- `Alignment = 2`
- `MarginV = 80–120`
- `MarginL/R = 56–72`

### 双语字幕

- 先提高 `MarginV`
- 再扩大 `MarginL/R`
- 保持两行内可读，避免整块字幕压太满

## 输出要求

使用这个 skill 时，最终回答应包含：

1. 当前判定为横屏的依据（分辨率或用户说明）
2. 最终采用的字幕参数
3. 若有调整，说明为什么上移 / 下移 / 放宽边距
4. 可直接使用的 `.ass` 样式或 FFmpeg 命令
5. 输出路径或建议输出文件名
