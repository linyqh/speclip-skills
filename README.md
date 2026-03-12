<p align="center">
  <a href="https://www.speclip.com">
    <img src="https://www.speclip.com/logo.svg" alt="Speclip Logo" width="120" />
  </a>
</p>

<h1 align="center">Speclip Skills</h1>

<p align="center">
  <strong>Open-source agent skills for real video production workflows</strong>
</p>

<p align="center">
  Turn repeatable editing methods into reusable AI workflows.
</p>

<p align="center">
  <a href="./README.zh.md">中文说明</a> ·
  <a href="https://www.speclip.com">Website</a> ·
  <a href="#featured-skills">Featured Skills</a> ·
  <a href="#quick-start">Quick Start</a> ·
  <a href="#why-speclip">Why Speclip</a> ·
  <a href="#faq">FAQ</a>
</p>

---

## What You Can Do

This repository contains **open-source agent skills** for video creation, editing, and workflow automation.

You can use these skills to turn AI from a generic assistant into a workflow-aware video agent that follows structured methods instead of giving generic suggestions.

With the skills in this repo, you can:

- create commentary-style short drama videos
- reuse structured video workflows
- apply production-ready FFmpeg best practices
- create your own vertical skills for repeatable tasks

> **Open source in this repo:** skill definitions, workflow instructions, helper scripts, references  
> **Requires Speclip for full execution:** runtime, built-in video tools, desktop / CLI workflow environment

---

## Why This Repo Exists

Speclip itself is not open source.

But the **workflow layer** behind great video production can be.

This repo is where we open-source reusable skills, structured workflows, helper scripts, and domain references — so creators and teams can study them, adapt them, and build on top of them.

If you want the full environment to run these workflows end-to-end, download Speclip.

> **Try Speclip:** https://www.speclip.com

---

## Featured Skills

### 🎬 `drama-explainer`

**Turn raw short-drama footage into commentary videos.**

A production workflow for one of the most popular formats on Chinese video platforms, especially Douyin, Bilibili, and Kuaishou.

**What it helps with:**

- dialogue transcription with speaker separation
- scene and plot understanding
- commentary script generation
- commentary-to-scene matching
- final rendering guidance

**Included:**

- 10 commentary styles
- structured references
- rendering guidance
- scene matching guidance

### 🛠️ `ffmpeg-best-practice`

**A production-ready FFmpeg playbook for agents and power users.**

Use this skill when you need reliable FFmpeg command construction for real editing workflows instead of trial-and-error.

**Best for:**

- export and delivery
- concatenation and compositing
- subtitle burn-in
- voiceover + BGM mixing
- mixed media reliability

### 🖥️ `landscape-subtitle-layout`

**Subtitle positioning and ASS parameters for landscape videos.**

Use this skill when you need stable subtitle placement for 16:9 content and want exact defaults for bottom-center alignment, margins, font sizing, and safe-area adjustments.

**Best for:**

- interview and commentary videos
- tutorial or screen-recorded exports
- subtitle burn-in with `.ass`
- “move subtitles higher/lower” requests

### 📱 `portrait-subtitle-layout`

**Subtitle positioning and ASS parameters for portrait videos.**

Use this skill when you need subtitle layouts for 9:16 shorts and want to avoid faces, CTA bars, product cards, and platform UI near the bottom.

**Best for:**

- Douyin / Reels / Shorts exports
- talking-head subtitles
- vertical commentary videos
- bottom safe-area control

### 🧱 `skill-creator`

**Create your own agent skills with a proper structure.**

A meta-skill for building new skills with progressive disclosure, bundled references, validation helpers, and packaging scripts.

**Best for:**

- AI workflow builders
- video teams creating reusable methods
- developers packaging domain workflows

---

## Quick Start

### 1. Clone this repo

```bash
git clone <your-repo-url>
cd speclip-skills
```

### 2. Install a skill

```bash
claude install-skill ./drama-explainer
```

Or install another skill:

```bash
claude install-skill ./ffmpeg-best-practice
claude install-skill ./landscape-subtitle-layout
claude install-skill ./portrait-subtitle-layout
claude install-skill ./skill-creator
```

### 3. Run a task

Example prompts:

```text
Help me turn this short drama into a commentary video.
```

```text
Help me add subtitles, voiceover, and background music to this video.
```

```text
Help me write a stable ffmpeg command to stitch three clips together and burn in subtitles.
```

```text
Create a new skill for product demo video workflows.
```

---

## What Makes These Skills Different

Most AI assistants can describe a workflow.

These skills help AI agents **follow one**.

Each skill can include:

- step-by-step execution guidance
- domain references
- output formats and constraints
- helper scripts
- production-specific best practices

Instead of starting from scratch every time, you get a reusable workflow that can be improved over time.

---

## Who This Repo Is For

This repo is useful if you are:

- a creator making repeatable video formats
- an editor building reusable workflows
- a content team standardizing output
- an AI workflow builder
- a developer exploring agent-based media automation

---

## Project Structure

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

## Why Speclip

This repo gives you the **open-source workflow layer**.

Speclip gives you the **full runtime** to execute those workflows end-to-end.

With Speclip, you get:

- a desktop app for AI-assisted video workflows
- a CLI for power users and automation
- built-in video tools
- model/provider flexibility
- a better environment for real execution

If this repo shows you the methods, Speclip helps you run them.

> **Download Speclip:** https://www.speclip.com

---

## Suggested First Path

If you're new here, start with this path:

1. browse `drama-explainer`
2. read the workflow and references
3. install the skill
4. try a real prompt
5. explore `skill-creator`
6. use Speclip for full execution

---

## FAQ

### Is Speclip open source?

No. Speclip itself is not open source.

This repository open-sources the **skills layer**: workflow definitions, references, helper scripts, and reusable execution patterns.

### Can I use these skills without Speclip?

Some parts are useful as references or workflow patterns on their own.

But for end-to-end video execution, these skills are designed to work best with Speclip.

### Can I use these skills with Claude Code?

Yes, where the runtime supports skill-style workflows.

### Can I create my own skills?

Yes. Start with `skill-creator`.

---

## Contributing

Contributions are welcome.

We especially welcome:

- new vertical workflow skills
- stronger references and examples
- helper scripts
- better packaging and validation

---

## Links

- Website: https://www.speclip.com
- Download Speclip: https://www.speclip.com
- Repository Skills Index: `skills.json`
- Chinese README: `README.zh.md`

---

<p align="center">
  Built by the <a href="https://www.speclip.com">Speclip</a> team
</p>
