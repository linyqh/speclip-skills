<p align="center">
  <a href="https://www.speclip.com">
    <img src="https://www.speclip.com/logo.svg" alt="Speclip Logo" width="120" />
  </a>
</p>

<h1 align="center">Speclip Skills</h1>

<p align="center">
  <strong>Open-source agent skills for <a href="https://www.speclip.com">Speclip</a> — the AI-powered video editor</strong>
</p>

<p align="center">
  <a href="https://www.speclip.com">Website</a> ·
  <a href="#available-skills">Skills</a> ·
  <a href="#quick-start">Quick Start</a> ·
  <a href="#creating-your-own-skill">Create a Skill</a>
</p>

---

## What is Speclip?

[**Speclip**](https://www.speclip.com) is an AI-driven video editing tool that automates complex editing workflows through conversational AI. It provides:

- **CLI** — Interactive terminal UI with AI agent orchestration
- **Desktop App** — Cross-platform native application (macOS / Windows / Linux) built with Tauri + React
- **JavaScript SDK** — Client/Server interfaces for third-party integration

### Key Features

| Feature | Description |
|---------|-------------|
| AI Agent Orchestration | Multiple AI agents analyze, plan, and execute editing tasks |
| Speech-to-Text | Transcription with speaker diarization and SRT generation |
| Multi-track Compositing | Combine clips, voiceovers, background music, and stock footage |
| Synthetic Voiceover | AI-generated narration from text |
| Stock Footage Search | Integrated Pexels library |
| 15+ AI Providers | Anthropic, OpenAI, Google, Azure, Groq, Mistral, and more |

> **Free Early Access** — [Download Speclip](https://www.speclip.com) and start editing with AI today.

---

## What is This Repo?

This repository contains **open-source agent skills** that extend Speclip (and [Claude Code](https://docs.anthropic.com/en/docs/claude-code)) with specialized workflows for video production tasks.

Skills are modular, self-contained packages that transform a general-purpose AI agent into a domain-specific expert. Each skill bundles:

- Procedural workflows (step-by-step instructions)
- Reference documentation (domain knowledge, schemas)
- Scripts (automation helpers)

## Available Skills

### 🎬 drama-explainer

**AI-powered short drama commentary video production workflow.**

Transforms raw drama footage into "commentary + original footage interleaved" derivative videos — a hugely popular format on Chinese video platforms (Douyin, Bilibili, Kuaishou).

**What it does:**

1. **ASR Extraction** — Transcribes dialogue with speaker diarization
2. **Visual Analysis** — Understands plot, characters, and scenes from video frames
3. **Cross-validation** — Verifies character relationships and plot accuracy
4. **Commentary Script** — Writes narration combining dialogue + visual context
5. **Scene Matching** — Precisely maps commentary to original footage timestamps
6. **Automated Editing** — Renders final video with commentary voiceover interleaved with original audio

**10 commentary styles** included — from casual conversational to professional film critic, covering comedy, suspense, romance, and more.

### 🛠️ skill-creator

**Guide for creating new agent skills.**

A meta-skill that helps you create effective skills with proper structure, progressive disclosure, and bundled resources. Includes:

- Skill anatomy and design principles
- Initialization scripts (`init_skill.py`)
- Packaging and validation tools (`package_skill.py`)
- Best practices for context window management

## Quick Start

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI installed
- [Speclip](https://www.speclip.com) installed (for video editing skills)

### Install a Skill

```bash
# Install the drama-explainer skill
claude install-skill /path/to/speclip-skills/drama-explainer

# Or install from this repo
git clone https://github.com/user/speclip-skills.git
claude install-skill ./speclip-skills/drama-explainer
```

### Use a Skill

Once installed, skills activate automatically when relevant. For example:

```
> 帮我把这个短剧做成解说视频

# The drama-explainer skill activates and guides you through the full workflow
```

## Creating Your Own Skill

Use the `skill-creator` skill to bootstrap new skills:

```
skill-name/
├── SKILL.md              # Required: frontmatter + instructions
├── scripts/              # Optional: automation scripts
├── references/           # Optional: domain knowledge docs
└── assets/               # Optional: templates, images, fonts
```

**Key principles:**

- **Concise is key** — Only include what the AI doesn't already know
- **Progressive disclosure** — Metadata → SKILL.md body → references (loaded on demand)
- **Appropriate freedom** — Match specificity to task fragility

See the [skill-creator SKILL.md](skill-creator/SKILL.md) for the full guide.

## Project Structure

```
speclip-skills/
├── drama-explainer/           # Short drama commentary video skill
│   ├── SKILL.md               # Core workflow (10 styles, 9-step pipeline)
│   └── references/
│       ├── styles/            # 10 commentary style definitions
│       ├── file-formats.md    # Output file format specifications
│       ├── rendering.md       # FFmpeg rendering guide
│       └── scene-matching-guide.md
├── skill-creator/             # Skill creation guide
│   ├── SKILL.md               # English version
│   ├── SKILL-zh.md            # Chinese version
│   └── scripts/
│       ├── init_skill.py      # Scaffold new skills
│       ├── package_skill.py   # Package for distribution
│       └── quick_validate.py  # Validate skill structure
└── README.md
```

## Tech Stack

This skills repo works with:

| Component | Technology |
|-----------|-----------|
| AI Agent Runtime | [Speclip](https://www.speclip.com) / [Claude Code](https://docs.anthropic.com/en/docs/claude-code) |
| Video Processing | FFmpeg |
| Speech Recognition | Qwen ASR (via Speclip) |
| Visual Understanding | Doubao Vision (via Speclip) |
| Voiceover Generation | TTS providers (via Speclip) |
| Language | Python (scripts), Markdown (instructions) |

## Contributing

Contributions are welcome! To add a new skill:

1. Fork this repository
2. Create your skill using `skill-creator`
3. Test with real tasks
4. Submit a pull request

## License

This project is open source. See individual skill directories for specific licensing.

## Links

- [Speclip Official Website](https://www.speclip.com)
- [Speclip Documentation](https://www.speclip.com)
- [Report Issues](https://github.com/user/speclip-skills/issues)

---

<p align="center">
  Built with ❤️ by the <a href="https://www.speclip.com">Speclip</a> team
</p>
