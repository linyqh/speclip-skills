<p align="center">
  <a href="https://www.speclip.com">
    <img src="https://www.speclip.com/logo.svg" alt="Speclip Logo" width="120" />
  </a>
</p>

<h1 align="center">Speclip Skills: Open-Source AI Video Workflows, FFmpeg, Subtitle Layout, and Video Editing Agent Skills</h1>

<p align="center">
  <strong>An open-source repository of reusable skills for real video production workflows.</strong>
</p>

<p align="center">
  <a href="./README.md">中文 README</a> ·
  <a href="https://www.speclip.com">Website</a> ·
  <a href="#quick-start">Quick Start</a> ·
  <a href="#choose-a-skill">Choose a Skill</a> ·
  <a href="#faq">FAQ</a> ·
  <a href="#help">Help</a>
</p>

> `Speclip Skills` currently includes `7` reusable skills for AI video workflows, video editing automation, FFmpeg usage, subtitle layout, short-drama commentary, and talking-head editing.

---

<a id="overview"></a>

## Overview

This repository is not a loose prompt collection. It packages repeatable video production methods into structured skills that are easier to reuse, maintain, and adapt.

If you are searching for topics like these, this repository is relevant:

- `AI video workflow`
- `video editing agent skills`
- `FFmpeg best practice`
- `subtitle layout for portrait video`
- `short drama commentary workflow`
- `talking head editing workflow`

Each skill typically includes:

- trigger conditions
- step-by-step workflow guidance
- output formats and constraints
- references
- helper scripts or evaluation materials

---

<a id="quick-facts"></a>

## Repository Snapshot

- `7` indexed skills in [`skills.json`](./skills.json)
- `3` content and editing skills: `drama-explainer`, `drama-script-writer`, `talking-head-editor`
- `3` execution and layout skills: `ffmpeg-best-practice`, `landscape-subtitle-layout`, `portrait-subtitle-layout`
- `1` meta-skill: `skill-creator`
- Primary README is Chinese; English docs live in this file
- The repository open-sources the workflow layer; Speclip provides the full execution environment

---

<a id="choose-a-skill"></a>

## Choose a Skill

| If you want to... | Use this skill | Typical output |
| --- | --- | --- |
| Turn raw short-drama footage into commentary videos | `drama-explainer` | plot understanding, narration structure, clip matching, rendering guidance |
| Write commentary scripts from subtitles or plot notes | `drama-script-writer` | script draft, narrative structure, emotional framing |
| Clean up a talking-head video | `talking-head-editor` | rough-cut suggestions, filler removal, jump-cut rules |
| Generate stable FFmpeg commands | `ffmpeg-best-practice` | export, stitching, audio mixing, subtitle burn-in commands |
| Adjust subtitle layout for 16:9 video | `landscape-subtitle-layout` | ASS parameters, safe-area guidance, subtitle positioning |
| Adjust subtitle layout for 9:16 video | `portrait-subtitle-layout` | vertical subtitle layout, bottom UI avoidance, safe-area control |
| Create your own reusable skill | `skill-creator` | skill structure, docs, references, script organization |

Natural-language examples:

- "Help me turn this short drama into a commentary video."
- "Help me write a commentary script from these subtitles."
- "Help me clean pauses and filler words from this talking-head video."
- "Help me write a stable ffmpeg command to stitch three clips together and burn in subtitles."
- "Help me move subtitles higher in this 9:16 video to avoid bottom UI."

---

<a id="skills"></a>

## Skills Included

### `drama-explainer`

Turn raw short-drama footage into commentary-driven recap videos with scene understanding, narration planning, clip matching, and rendering guidance.

### `drama-script-writer`

Write commentary scripts for short dramas, suspense clips, and story-driven video content from subtitles, synopses, or relationship notes.

### `talking-head-editor`

Refine talking-head videos by identifying pauses, filler words, weak lines, and rough-cut opportunities from transcripts or review notes.

### `ffmpeg-best-practice`

Use production-grade FFmpeg patterns for exporting, stitching, subtitle burn-in, audio mixing, and compatibility handling.

### `landscape-subtitle-layout`

Define stable subtitle placement and ASS defaults for 16:9 landscape videos.

### `portrait-subtitle-layout`

Handle subtitle layout for 9:16 vertical videos while avoiding bottom UI, CTA bars, and face overlap.

### `skill-creator`

Create new reusable skills with better structure, references, helper scripts, and packaging conventions.

---

<a id="quick-start"></a>

## Quick Start

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd speclip-skills
```

### 2. Install a skill

```bash
claude install-skill ./drama-explainer
```

Common options:

```bash
claude install-skill ./drama-script-writer
claude install-skill ./talking-head-editor
claude install-skill ./ffmpeg-best-practice
claude install-skill ./landscape-subtitle-layout
claude install-skill ./portrait-subtitle-layout
claude install-skill ./skill-creator
```

### 3. Run a real task

```text
Help me turn this short drama into a commentary video.
```

```text
Help me clean pauses, filler words, and weak lines from this talking-head video.
```

```text
Help me write a stable ffmpeg command to stitch three clips together and burn in subtitles.
```

```text
Help me move subtitles higher in this 9:16 video to avoid bottom UI.
```

### 4. Use `skills.json` as the index

[`skills.json`](./skills.json) maps skill names, descriptions, and file paths for search, routing, automation, and secondary tooling.

---

<a id="open-source-boundary"></a>

## Open-Source Boundary

This repository open-sources the workflow layer:

- skill definitions
- workflow instructions
- helper scripts
- references

Speclip provides the full runtime for end-to-end execution.

That means:

- you can still use these skills as workflow templates, knowledge assets, or packaging examples
- if you want the full video-processing runtime, Speclip is the more complete environment

---

<a id="faq"></a>

## FAQ

### Is Speclip open source?

No. Speclip itself is not open source.

This repository open-sources the reusable skills layer: workflow definitions, references, helper scripts, and execution patterns.

### Can I use these skills without Speclip?

Yes. You can use them as references, workflow templates, or examples of how to package domain-specific skills.

For end-to-end execution, they work best with Speclip.

### Which skill should I start with?

Recommended order:

1. `drama-explainer`
2. `ffmpeg-best-practice`
3. `portrait-subtitle-layout` or `landscape-subtitle-layout`
4. `talking-head-editor`
5. `skill-creator`

### Can I create my own skills?

Yes. Start with `skill-creator`.

---

<a id="help"></a>

## Help

- Learn more about Speclip: https://www.speclip.com
- Browse all indexed skills: [`skills.json`](./skills.json)
- Read the primary Chinese README: [`README.md`](./README.md)
- Contribute a new skill, example, or helper script through issues or pull requests

---

## Links

- Website: https://www.speclip.com
- Download Speclip: https://www.speclip.com
- Skills Index: [`skills.json`](./skills.json)
- Primary Chinese README: [`README.md`](./README.md)

---

<p align="center">
  Built by the <a href="https://www.speclip.com">Speclip</a> team
</p>
