# drama-explainer

一个面向短剧二创的“解说配音 + 原片高张力片段穿插”成片技能。

当前工作流已升级为：**向量检索先召回候选戏眼，再由编辑流程决定保留哪些原声与 VO；`doubaovision` 默认只做定向视觉复核，不再与检索重复扫片。**

## 适用场景

当用户要做这些事情时，应优先使用它：
- 短剧解说成片
- 狗血短剧混剪解说
- 情绪冲突型剧情二创
- 从多段短剧原片提炼出“保留戏眼 + VO 串联”的成片

它不适合：
- 普通剧情总结
- 纯影评
- 只改写文案
- 纯字幕烧录
- 普通视频剪切

## 关键产物

- `analysis/plot_analysis.md`
- `analysis/characters.md`
- `analysis/retrieval_candidates.json`（可选）
- `scripts/draft_script.md`
- `scripts/storyboard.json`
- `scripts/final_script.md`
- `scripts/voiceover.md`
- `output/output.mp4`

## 设计原则

- `storyboard.json` 是唯一真相源
- 先用 `videoindex` / `videosearch` 召回候选片段，再做人类可审查的编辑决策
- `doubaovision` 默认只在候选歧义、字幕不足、无台词强表演等场景介入
- 步骤 5 只把故事讲顺
- 步骤 6 才做真正的编辑决策
- 优先保留最有戏的原片，而不是最完整的原片
- VO 只负责铺垫、跳转、补信息，不复述原片

## 相关文件

- `short-drama-video/drama-explainer/SKILL.md`
- `short-drama-video/drama-explainer/references/file-formats.md`
- `short-drama-video/drama-explainer/references/scene-matching-guide.md`
- `short-drama-video/drama-explainer/references/rendering.md`
- `short-drama-video/drama-explainer/evals/evals.json`
- `short-drama-video/drama-explainer/evals/review-rubric.md`
- `short-drama-video/drama-explainer/references/dramatic-editor-guide.md`
