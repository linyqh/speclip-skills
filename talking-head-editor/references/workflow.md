# Talking-Head Editing Workflow

Use this file for end-to-end requests such as “帮我剪一条更紧凑的口播”, “按字幕粗剪”, or “给我一份可执行的口播剪辑方案”.

## 1. Choose the editing mode

- `transcript-first`: Use when `srt`/`vtt`/timestamped transcript already exists. This is the default.
- `notes-first`: Use when the user marked sentences manually but did not provide formal subtitle files.
- `asr-first`: Use when only raw media exists. The first deliverable is sentence-level timestamps, not final cuts.

## 2. Normalize the source material

Build a sentence list with these minimum fields:

- `sentence_id`
- `start`
- `end`
- `text`
- `speaker` when available
- `confidence` when available

If the source contains `<No Speech>` or similar markers, keep them as silence candidates instead of deleting them immediately.

## 3. Label each sentence

Use one of these labels:

- `keep`
- `trim`
- `delete`
- `review`

Common reasons:

- `hook`
- `core_point`
- `example`
- `duplicate`
- `false_start`
- `filler`
- `long_pause`
- `off_topic`
- `bad_take`
- `needs_cover`

## 4. Convert labels into cut ranges

- `keep`: keep the full sentence with preset padding.
- `trim`: keep the sentence but tighten its head/tail.
- `delete`: remove the sentence and collapse the gap.
- `review`: keep temporarily and mark for manual confirmation.

When one kept sentence ends very close to the next kept sentence, merge them into a single execution segment.

## 5. Review jump-cut risk

Flag segments that likely need cover when:

- two consecutive kept segments come from the same framing with a visible head snap
- a sentence begins mid-mouth shape after a hard trim
- the speaker's hand position changes abruptly
- the audio sounds natural but the visual discontinuity is obvious

Typical cover options:

- punch-in 103%–108%
- short cutaway or B-roll
- subtitle emphasis burst
- waveform / screenshot / slide insert

## 6. Produce deliverables

Return, in order:

1. editing goal and pacing preset
2. sentence-level decision list
3. merged execution segments
4. jump-cut mitigation notes
5. subtitle plan
6. export notes if requested

## 7. Confidence rules

- `high`: timestamps come from sentence-level subtitles or reviewed transcript
- `medium`: timestamps come from ASR but text is mostly clean
- `low`: timestamps come from noisy ASR, diarization is unclear, or large sections need manual review

If confidence is `low`, do not over-specify exact frame-accurate cuts.
