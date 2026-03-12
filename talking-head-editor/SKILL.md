---
name: talking-head-editor
description: >
  口播 / talking-head 视频精剪 skill。适用于单人出镜口播、采访、自述、
  课程讲解、播客切条等以 A-roll 说话为主的视频。Use when the user asks
  for “剪口播”, “删停顿”, “去废话”, “删语气词”, “jump cut”, “按字幕精剪”,
  “根据 transcript 粗剪”, “采访精剪”, “单人口播提速”, or “把这段 talking
  head 剪紧凑”.
---

# Talking Head Editor

Use this skill to turn transcript-driven talking-head footage into a clean rough-cut plan. Prefer sentence-level transcript editing over scene-based montage logic. If the task also requires executable FFmpeg commands or delivery-safe export settings, read `../ffmpeg-best-practice/SKILL.md` alongside this skill.

## Scope

- Remove long pauses, filler words, false starts, repeated phrases, and obvious tangents.
- Preserve the speaker's meaning, rhythm, and necessary breathing room.
- Produce sentence-level keep/delete decisions and merged cut ranges.
- Call out jump-cut risks, subtitle strategy, and export notes.
- Focus this first version on edit planning and execution specs, not automatic face tracking, B-roll retrieval, or template animation.

## Required Inputs

Start once at least one of these exists:

- `srt`, `vtt`, or transcript with timestamps
- Review notes that mark lines to keep/remove
- Source media plus a request to first create sentence-level timestamps

If the user only provides raw video without timestamps, first obtain or generate sentence-level timestamps before promising exact cut ranges.

## Default Workflow

1. Decide the pacing preset: `clean`, `creator`, or `viral`.
2. Read `references/workflow.md` for the end-to-end editing sequence.
3. Read `references/edit-rules.md` when deciding what to delete, what to keep, how much handle to preserve, and how aggressively to merge.
4. Read `references/file-formats.md` when returning structured outputs like `edit_decision.json`, merged segment tables, or subtitle plans.
5. Produce three layers of output:
   - editorial summary
   - sentence-level keep/delete decisions
   - merged execution segments with start/end timestamps
6. If the user asks for commands, hand the merged segments to the FFmpeg workflow instead of improvising export parameters.

## Pacing Presets

- `clean`: conservative cleanup; remove only obvious dead air, major stumbles, and duplicate starts.
- `creator`: default creator pass; tighten intros, trim fillers, and compress weak transitions.
- `viral`: aggressive density; short pauses, hard trims, stronger subtitle emphasis, and more visible jump cuts.

## Output Contract

Always return:

- chosen pacing preset and assumptions
- sentence-level keep/remove decisions for any ambiguous lines
- merged cut segments with `start`, `end`, and short rationale
- subtitle notes and jump-cut mitigation notes
- export or render notes if the user asks for final delivery

## Guardrails

- Do not cut inside a word, plosive, or audible breath unless a cover strategy is explicitly available.
- Prefer sentence boundaries over arbitrary silence boundaries.
- Merge nearby kept segments when semantic continuity is strong and the gap is below the preset threshold.
- Flag places that likely need punch-in, cutaway, B-roll, waveform mask, or subtitle emphasis to hide jump cuts.
- If the transcript quality is weak, say so explicitly and lower timestamp confidence.

## References

- End-to-end sequence: `references/workflow.md`
- Keep/remove heuristics and pacing rules: `references/edit-rules.md`
- Structured outputs and JSON/table schemas: `references/file-formats.md`
