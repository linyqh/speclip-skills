<p align="center">
  <a href="https://www.speclip.com">
    <img src="https://www.speclip.com/logo.svg" alt="Speclip Logo" width="120" />
  </a>
</p>

<h1 align="center">Speclip Skills</h1>

<p align="center">
  <strong>面向真实视频生产流程的开源 Agent Skills</strong>
</p>

<p align="center">
  把可复用的视频制作方法，变成 AI 可执行的工作流。
</p>

<p align="center">
  <a href="./README.md">English</a> ·
  <a href="https://www.speclip.com">官网</a> ·
  <a href="#精选-skills">精选 Skills</a> ·
  <a href="#快速开始">快速开始</a> ·
  <a href="#为什么还需要-speclip">为什么还需要 Speclip</a> ·
  <a href="#常见问题">常见问题</a>
</p>

---

## 你可以用它做什么

这个仓库包含一组面向**视频创作、视频剪辑与工作流自动化**的开源 Agent Skills。

你可以用这些 skills，把 AI 从“只会提建议的助手”变成“理解流程、按方法执行”的视频 Agent。

有了这个仓库中的 skills，你可以：

- 制作短剧解说类视频
- 复用结构化的视频工作流
- 复用可靠的 FFmpeg 生产实践
- 为重复性任务封装自己的垂直技能

> **本仓库开源内容：** skill definitions、workflow instructions、helper scripts、references  
> **完整执行仍需 Speclip：** runtime、built-in video tools、desktop / CLI workflow environment

---

## 为什么有这个仓库

Speclip 主产品本身**不开源**。

但优秀视频生产背后的**工作流层**，是可以开源的。

这个仓库就是用来开源这些可以复用的 skills、结构化工作流、辅助脚本和领域知识，让创作者、团队、开发者都可以直接学习、复用、扩展。

如果你希望把这些工作流真正跑起来，完成端到端的视频生产执行，请下载 Speclip。

> **下载试用 Speclip：** https://www.speclip.com

---

## 精选 Skills

### 🎬 `drama-explainer`

**把短剧原片转成“解说 + 原片穿插”的二创视频工作流。**

这是一个非常适合中文视频平台的热门内容形态工作流，适用于抖音、B 站、快手等平台的短剧解说与剧情复盘内容。

**它能帮你做什么：**

- 带说话人区分的对话转写
- 剧情与场景理解
- 解说文案生成
- 解说与片段精准匹配
- 最终渲染与成片指导

**内含：**

- 10 种解说风格
- 结构化参考文档
- 渲染说明
- 片段匹配指南

### 🛠️ `ffmpeg-best-practice`

**面向 Agent 与高级用户的生产级 FFmpeg 实战手册。**

当你需要更稳定地处理拼接、导出、字幕烧录、音频混合、VFR/CFR 规范化等问题时，这个 skill 可以帮你减少踩坑。

**适合场景：**

- 成片导出与交付
- 拼接与合成
- 字幕烧录
- 配音与 BGM 混音
- 复杂源素材的稳健处理

### 🖥️ `landscape-subtitle-layout`

**横屏视频的字幕位置与 ASS 参数配置 skill。**

当你需要为 16:9 内容稳定设置底部居中字幕、边距、字号、安全区，并且要明确回答“字幕再高一点/再低一点”这类问题时，用这个 skill。

**适合场景：**

- 访谈与解说视频
- 教程 / 屏录导出
- `.ass` 字幕烧录
- 横屏字幕位置微调

### 📱 `portrait-subtitle-layout`

**竖屏视频的字幕位置与 ASS 参数配置 skill。**

当你需要为 9:16 短视频设置字幕位置，并避让人脸、底部 CTA、商品卡和平台 UI 时，用这个 skill。

**适合场景：**

- 抖音 / Reels / Shorts 导出
- 口播字幕
- 竖屏剧情解说
- 底部安全区控制

### 🧱 `skill-creator`

**用规范结构创建你自己的 Agent Skill。**

这是一个用来创建新 skill 的元技能，帮助你用更合理的结构组织说明、引用资料、校验脚本和打包流程。

**适合人群：**

- AI 工作流搭建者
- 想沉淀视频方法的视频团队
- 想把领域流程打包成 skill 的开发者

---

## 快速开始

### 1. 克隆仓库

```bash
git clone <your-repo-url>
cd speclip-skills
```

### 2. 安装一个 skill

```bash
claude install-skill ./drama-explainer
```

或安装其他 skill：

```bash
claude install-skill ./ffmpeg-best-practice
claude install-skill ./landscape-subtitle-layout
claude install-skill ./portrait-subtitle-layout
claude install-skill ./skill-creator
```

### 3. 直接开始一个任务

示例提示词：

```text
帮我把这个短剧做成解说视频
```

```text
帮我给这段视频加字幕、配音和背景音乐
```

```text
帮我写一个稳定的 ffmpeg 命令，把三段素材拼起来并烧录字幕
```

```text
Create a new skill for product demo video workflows
```

---

## 这些 Skills 有什么不一样

大多数 AI 助手都能描述工作流。

这些 skills 的价值，是让 AI Agent **真正按工作流执行**。

每个 skill 都可以包含：

- 分步骤执行指引
- 领域参考资料
- 输出格式和约束
- 辅助脚本
- 生产级最佳实践

它不是每次都从零开始临时生成，而是让你拿到一套可以持续复用、持续优化的工作流。

---

## 这个仓库适合谁

如果你属于下面这些角色，这个仓库会很有帮助：

- 做固定视频栏目或内容模板的创作者
- 想沉淀方法的剪辑师
- 想标准化视频产出的内容团队
- 正在搭建 AI 工作流的从业者
- 探索 Agent 媒体自动化的开发者

---

## 项目结构

```text
speclip-skills/
├── drama-explainer/
│   ├── SKILL.md
│   └── references/
│       ├── file-formats.md
│       ├── rendering.md
│       ├── scene-matching-guide.md
│       └── styles/
├── ffmpeg-best-practice/
│   └── SKILL.md
├── landscape-subtitle-layout/
│   └── SKILL.md
├── portrait-subtitle-layout/
│   └── SKILL.md
├── skill-creator/
│   ├── SKILL.md
│   ├── SKILL-zh.md
│   ├── references/
│   └── scripts/
├── skills.json
├── README.md
└── README.zh.md
```

---

## 为什么还需要 Speclip

这个仓库提供的是**开源工作流层**。

Speclip 提供的是把这些工作流真正端到端执行起来的**完整运行环境**。

有了 Speclip，你可以获得：

- 用于 AI 视频工作流的桌面应用
- 面向高级用户和自动化场景的 CLI
- 内置视频处理工具链
- 多模型与多 provider 灵活切换
- 更适合真实落地执行的运行环境

如果这个仓库向你展示的是“方法层”，那么 Speclip 提供的就是“真正把方法跑起来的执行环境”。

> **下载 Speclip：** https://www.speclip.com

---

## 推荐体验路径

如果你是第一次接触，推荐按这个顺序体验：

1. 先看 `drama-explainer`
2. 读工作流和参考资料
3. 安装 skill
4. 用真实提示词试一次
5. 再看 `skill-creator`
6. 最后用 Speclip 跑完整流程

---

## 常见问题

### Speclip 是开源的吗？

不是。Speclip 主产品本身不开源。

这个仓库开源的是 **skills 层**：工作流定义、参考资料、辅助脚本和可复用的执行模式。

### 不安装 Speclip 也能用这些 skills 吗？

其中一部分内容可以单独作为参考资料和工作流模板使用。

但如果你希望完成端到端的视频执行，这些 skills 最适合与 Speclip 搭配使用。

### 可以和 Claude Code 一起用吗？

可以，在支持 skill 工作流的运行环境里都可以参考和使用。

### 我可以自己创建 skill 吗？

可以，直接从 `skill-creator` 开始。

---

## 贡献

欢迎贡献。

尤其欢迎以下方向：

- 新的垂直工作流 skill
- 更强的参考资料与案例
- 更实用的辅助脚本
- 更好的打包与校验工具

---

## 相关链接

- 官网：https://www.speclip.com
- 下载 Speclip：https://www.speclip.com
- Skills 索引：`skills.json`
- 英文 README：`README.md`

---

<p align="center">
  由 <a href="https://www.speclip.com">Speclip</a> 团队构建
</p>
