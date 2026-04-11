# short-drama-video

短剧解说相关 skills 的专用目录。

这个目录集中收纳了当前仓库里直接面向“短剧解说视频制作”的核心 skills，避免它们散落在仓库根目录，方便单独浏览、安装和维护。

## 共享标准

这个目录下所有短剧解说 skill 共同遵守两份共享参考：

- `references/excellent-short-drama-commentary-playbook.md`
- `references/skill-stack.md`

它们定义了优秀短剧解说的共同质量标准、节奏红线和 3 个核心 skill 的分工关系。

## 已收纳的核心 skills

- `drama-explainer/`
  - 面向完整短剧解说成片流程
  - 负责剧情理解、戏眼检索、分镜、VO、匹配、渲染交接
- `drama-script-writer/`
  - 面向短剧解说文案撰写
  - 负责根据字幕 / 梗概 / 角色关系产出逐行解说稿
- `short-drama-commentary/`
  - 面向结构拆解与原片/解说穿插规划
  - 负责分析优秀样本、设计 beat sheet、插片计划和混排脚本

## 推荐使用顺序

1. `short-drama-commentary/`：先定结构和原片/解说穿插策略
2. `drama-script-writer/`：再写纯解说稿或逐段口播稿
3. `drama-explainer/`：最后进入完整成片流程

## 仍然推荐配合的通用 skills

这些也常用于短剧解说视频制作，但它们是跨场景通用能力，所以仍保留在仓库根目录：

- `ffmpeg-best-practice/`
- `portrait-subtitle-layout/`
- `landscape-subtitle-layout/`

## 安装示例

```bash
claude install-skill ./short-drama-video/short-drama-commentary
claude install-skill ./short-drama-video/drama-script-writer
claude install-skill ./short-drama-video/drama-explainer
```
