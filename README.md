<p align="center">
  <a href="https://www.speclip.com">
    <img src="https://www.speclip.com/logo.svg" alt="Speclip Logo" width="120" />
  </a>
</p>

<h1 align="center">Speclip Skills：开源 AI 视频工作流、FFmpeg、字幕布局与视频剪辑 Agent Skills</h1>

<p align="center">
  <strong>一个面向真实视频生产的开源 Skills 仓库，覆盖短剧解说、口播精剪、FFmpeg 命令、横竖屏字幕布局和新 Skill 封装。</strong>
</p>

<p align="center">
  <a href="./README.en.md">English</a> ·
  <a href="https://www.speclip.com">Speclip 官网</a> ·
  <a href="#quick-start">快速开始</a> ·
  <a href="#choose-a-skill">如何选 Skill</a> ·
  <a href="#faq">常见问题</a> ·
  <a href="#help">获取帮助</a>
</p>

> `Speclip Skills` 是一个开源仓库，当前收录 `8` 个可复用的 AI 视频工作流 Skills，适合做 AI video workflow、video editing automation、FFmpeg best practice、subtitle layout、short drama commentary 和 talking-head editing。

---

<a id="overview"></a>

## 概览

这个仓库不是泛化提示词集合，而是把视频生产里的高频任务整理成可复用、可维护、可扩展的结构化工作流。

如果你在找下面这些方向，这个仓库就是相关入口：

- `AI video workflow`
- `video editing agent skills`
- `FFmpeg best practice`
- `subtitle layout for portrait video`
- `short drama commentary workflow`
- `talking head editing workflow`

你可以把仓库里的每个 Skill 理解为一套可执行说明，通常包含：

- 触发条件
- 步骤化工作流
- 输出格式和约束
- 参考资料
- 辅助脚本或评测材料

---

<a id="quick-facts"></a>

## 仓库快照

- `8` 个已收录 Skills，索引见 [`skills.json`](./skills.json)
- `4` 个内容 / 剪辑向 Skills：`drama-explainer`、`short-drama-commentary`、`drama-script-writer`、`talking-head-editor`
- `3` 个执行 / 布局向 Skills：`ffmpeg-best-practice`、`landscape-subtitle-layout`、`portrait-subtitle-layout`
- `1` 个元技能：`skill-creator`
- 主 README 为中文，英文入口见 [`README.en.md`](./README.en.md)
- 本仓库开源的是工作流层，完整运行环境由 Speclip 提供

---

<a id="problems"></a>

## 你可以用它解决什么问题

这个仓库主要解决的是“AI 知道视频怎么做，但不知道怎么稳定落地”的问题。

典型使用场景包括：

- 把短剧原片转成解说类二创视频
- 根据字幕或剧情梗概写解说文案
- 根据 transcript 清理口播停顿、废话和口头禅
- 生成更稳的 FFmpeg 拼接、导出、混音、字幕烧录命令
- 为 16:9 或 9:16 视频设置更合理的字幕位置和安全区
- 把团队内部的视频生产方法封装成新 Skill

---

<a id="choose-a-skill"></a>

## 如何选 Skill

| 如果你想解决的问题 | 使用哪个 Skill | 典型输出 |
| --- | --- | --- |
| 拆解优秀短剧解说字幕、规划原片/解说穿插 | `short-drama-commentary` | 结构判断、插片计划、beat sheet、混排脚本 |
| 把短剧原片做成解说视频 | `drama-explainer` | 剧情理解、解说结构、片段匹配、成片指导 |
| 根据字幕或剧情梗概写解说稿 | `drama-script-writer` | 解说文案、叙事结构、情绪冲突表达 |
| 精剪口播视频 | `talking-head-editor` | 粗剪建议、停顿清理、jump cut 处理规则 |
| 稳定生成 FFmpeg 命令 | `ffmpeg-best-practice` | 导出、拼接、混音、字幕烧录命令 |
| 调整横屏字幕位置 | `landscape-subtitle-layout` | 16:9 字幕布局、ASS 参数、安全区建议 |
| 调整竖屏字幕位置 | `portrait-subtitle-layout` | 9:16 字幕布局、底部 UI 避让、安全区控制 |
| 创建你自己的 Skill | `skill-creator` | Skill 结构、说明文档、参考资料、脚本组织方式 |

如果你更习惯按搜索意图判断，可以直接参考下面这些自然语言任务：

- “帮我把这个短剧做成解说视频”
- “帮我根据字幕写一版剧情解说稿”
- “帮我清理这段口播里的停顿和口头禅”
- “帮我写一个稳定的 ffmpeg 命令，把三段素材拼起来并烧录字幕”
- “帮我把 9:16 视频字幕往上提一点，避开底部 UI”
- “帮我创建一个新的 product demo video skill”

---

<a id="skills"></a>

## Skills 列表

### `short-drama-commentary`

字幕优先的短剧解说结构设计 Skill。适合拆解优秀短剧解说字幕，学习“什么时候插原片、什么时候用解说压缩”，或直接根据原剧字幕产出插片计划和混排脚本。

适合处理：

- 优秀短剧解说样本拆解
- 原片 / 解说穿插结构设计
- beat sheet 与插片计划表
- 混排脚本与节奏提纯

### `drama-explainer`

把短剧原片转换成“解说 + 原片穿插”的二创视频工作流，适用于抖音、B 站、快手等平台的剧情解说、剧情复盘和冲突向内容。

适合处理：

- 角色分离转写
- 剧情与场景理解
- 解说词生成
- VO 与画面片段匹配
- 最终成片渲染指导

### `drama-script-writer`

面向短剧、影视、悬疑剧情视频的解说文案创作 Skill。可根据字幕、剧情梗概、人物关系或视觉笔记撰写解说稿。

适合处理：

- 解说文案创作
- 剧情梳理
- 人物关系提炼
- 情绪冲突型叙事表达

### `talking-head-editor`

面向口播 / talking-head 视频的精剪 Skill。根据字幕、逐句 transcript 或审片笔记生成粗剪方案、停顿清理建议和导出要求。

适合处理：

- 删除停顿和废话
- 清理口头禅
- jump cut 编辑建议
- 口播视频粗剪流程

### `ffmpeg-best-practice`

生产级 FFmpeg 工作流 Skill，适合稳定生成视频压缩、导出、拼接、混音和字幕处理命令，而不是靠试错写命令。

适合处理：

- MP4 导出与交付
- 素材拼接和合成
- 语音 + BGM 混音
- 字幕烧录
- VFR / CFR 与兼容性问题

### `landscape-subtitle-layout`

横屏视频字幕位置与 ASS 参数配置 Skill，适用于 16:9 视频的底部居中字幕布局、安全区、字号和边距调整。

适合处理：

- 横屏教程和访谈视频
- `.ass` 字幕烧录
- 字幕上下位置微调
- 安全区与边距控制

### `portrait-subtitle-layout`

竖屏视频字幕位置与 ASS 参数配置 Skill，适用于 9:16 短视频字幕布局，并考虑底部 CTA、商品卡、平台 UI 和人物避让。

适合处理：

- 抖音 / Reels / Shorts 字幕布局
- 口播字幕安全区
- 竖屏剧情解说字幕
- 底部遮挡风险控制

### `skill-creator`

用于创建新 Skill 的元技能，帮助你把领域方法打包成结构化说明、参考资料、辅助脚本和可维护的目录结构。

适合处理：

- 新 Skill 设计
- Skill 文档组织
- 参考资料打包
- Skill 校验与迭代

---

<a id="quick-start"></a>

## 快速开始

### 1. 克隆仓库

```bash
git clone <your-repo-url>
cd speclip-skills
```

### 2. 安装一个 Skill

```bash
claude install-skill ./short-drama-video/drama-explainer
```

常用安装示例：

```bash
claude install-skill ./short-drama-video/short-drama-commentary
claude install-skill ./short-drama-video/drama-script-writer
claude install-skill ./talking-head-editor
claude install-skill ./ffmpeg-best-practice
claude install-skill ./landscape-subtitle-layout
claude install-skill ./portrait-subtitle-layout
claude install-skill ./skill-creator
```

### 3. 用真实任务触发

```text
帮我把这个短剧做成解说视频
```

```text
帮我根据字幕写一版狗血短剧解说稿
```

```text
帮我清理这段口播里的停顿、废话和口头禅
```

```text
帮我写一个稳定的 ffmpeg 命令，把三段素材拼起来并烧录字幕
```

```text
帮我把 9:16 视频的字幕往上提一点，避开底部 UI
```

### 4. 用 `skills.json` 做自动化索引

[`skills.json`](./skills.json) 提供了技能名称、说明和关联文件映射，适合做检索、自动装配、代理路由或二次封装。

---

<a id="open-source-boundary"></a>

## 开源边界

这个仓库开源的是视频 AI 工作流里的“方法层”：

- Skills 定义
- workflow instructions
- helper scripts
- references

Speclip 提供的是完整执行环境，包括更适合真实视频生产的运行时、工具链和桌面 / CLI 工作流。

这意味着：

- 你可以单独把这些 Skills 当成工作流模板、知识库或 Skill 设计参考
- 如果你要跑完整的视频处理链路，Speclip 会更完整

---

<a id="who-for"></a>

## 适合谁

这个仓库适合下面这些角色：

- 做固定视频栏目或批量内容生产的创作者
- 想把剪辑经验沉淀成流程的剪辑师
- 想规范视频产出的内容团队
- 在做 AI 视频工作流或 Agent automation 的开发者
- 想复用 FFmpeg、字幕布局、脚本生成方案的高级用户

---

<a id="structure"></a>

## 仓库结构

```text
speclip-skills/
├── short-drama-video/
│   ├── README.md
│   ├── drama-explainer/
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── evals/
│   │   └── references/
│   ├── drama-script-writer/
│   │   ├── SKILL.md
│   │   └── references/
│   └── short-drama-commentary/
│       ├── SKILL.md
│       ├── README.md
│       └── references/
├── talking-head-editor/
│   ├── SKILL.md
│   ├── agents/
│   └── references/
├── ffmpeg-best-practice/
│   ├── SKILL.md
│   └── references/
├── landscape-subtitle-layout/
│   └── SKILL.md
├── portrait-subtitle-layout/
│   └── SKILL.md
├── skill-creator/
│   ├── SKILL.md
│   ├── LICENSE.txt
│   ├── assets/
│   ├── eval-viewer/
│   ├── references/
│   └── scripts/
├── skills.json
├── README.md
└── README.en.md
```

---

<a id="faq"></a>

## 常见问题

### Speclip 是开源的吗？

不是。Speclip 主产品本身不开源。

这个仓库开源的是可复用的 Skills、工作流定义、参考资料和辅助脚本，也就是视频 AI 工作流里的“方法层”。

### 不安装 Speclip 也能用这些 Skills 吗？

可以。你可以把它们当成参考资料、工作流模板或 Skill 设计样例来使用。

如果你要跑完整的视频处理链路，Speclip 提供的运行环境会更完整。

### 这些 Skills 能用于 Claude Code 或其他 Agent 环境吗？

可以。只要你的运行环境支持按 Skill 方式组织说明、引用资料和执行流程，就可以参考和适配。

### 我应该先从哪个 Skill 开始？

如果你是第一次接触，建议按这个顺序体验：

1. `drama-explainer`
2. `ffmpeg-best-practice`
3. `portrait-subtitle-layout` 或 `landscape-subtitle-layout`
4. `talking-head-editor`
5. `skill-creator`

### 我可以创建自己的 Skill 吗？

可以，直接从 `skill-creator` 开始。

### 为什么主 README 使用中文？

因为当前最主要的实际使用场景集中在中文视频创作、短剧解说、字幕布局和视频剪辑自动化。中文主 README 更符合当前主要用户入口；英文说明保留在 [`README.en.md`](./README.en.md)。

---

<a id="help"></a>

## 获取帮助

- 想了解完整产品能力：访问 https://www.speclip.com
- 想浏览全部 Skills：查看 [`skills.json`](./skills.json)
- 想看英文说明：查看 [`README.en.md`](./README.en.md)
- 想贡献新 Skill、案例或辅助脚本：直接提交 issue 或 PR

---

<a id="contributing"></a>

## 贡献

欢迎提交 issue 和 PR。尤其欢迎下面这些方向：

- 新的视频工作流 Skill
- 更强的参考资料和案例
- 更实用的辅助脚本
- 更完善的评测与验证工具
- 更清晰的安装和使用文档

---

## 相关链接

- Speclip 官网：https://www.speclip.com
- 下载 Speclip：https://www.speclip.com
- Skills 索引：[`skills.json`](./skills.json)
- 英文 README：[`README.en.md`](./README.en.md)

---

<p align="center">
  Built by the <a href="https://www.speclip.com">Speclip</a> team
</p>
