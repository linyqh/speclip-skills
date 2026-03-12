# Talking-Head Edit Rules

Use this file when deciding what to cut, how much handle to preserve, and how aggressive the final pacing should be.

## Remove first

Delete or tighten these before touching strong content:

- long silence
- repeated sentence starts
- obvious filler words: `嗯`, `啊`, `这个`, `就是`, `然后`, `你知道`, `怎么说呢`
- abandoned clauses and self-corrections
- digressions that do not support the main point
- retakes or duplicated examples

## Protect first

Avoid removing these unless the user explicitly wants a harsher edit:

- hook sentence
- thesis or key promise
- punchline
- emotional beat
- necessary setup for an example or transition
- intentional pause used for emphasis

## Preset rules

### `clean`

- Keep natural breathing room.
- Remove only obvious dead air and clear mistakes.
- Head pad: `120–200ms`
- Tail pad: `150–250ms`
- Merge adjacent kept segments when the gap is `< 350ms`

### `creator`

- Tighten weak sentence starts and vague transitions.
- Remove most filler words and low-value repetition.
- Head pad: `80–150ms`
- Tail pad: `100–180ms`
- Merge adjacent kept segments when the gap is `< 250ms`

### `viral`

- Maximize density and forward motion.
- Keep only functional breaths.
- Allow visible jump cuts if energy improves.
- Head pad: `40–100ms`
- Tail pad: `60–120ms`
- Merge adjacent kept segments when the gap is `< 180ms`

## Trim logic

Use `trim` instead of `delete` when:

- the sentence contains one useful clause surrounded by rambling
- the line starts with fillers but ends with the core point
- the line needs a shorter tail after the key phrase lands

## Jump-cut mitigation

Flag `needs_cover` when:

- the speaker's face or shoulders visibly jump
- the hand position resets between adjacent kept lines
- the mouth shape changes abruptly at the cut
- the cut is aggressive but the content must stay

Preferred mitigation order:

1. small punch-in
2. alternate crop position
3. subtitle emphasis or on-screen keyword
4. B-roll / cutaway / screenshot

## Subtitle guidance

- Split subtitles by spoken sense units, not by maximum character count alone.
- Prefer short lines for fast presets.
- Highlight only key words, numbers, promises, and contrasts.
- If the cut is aggressive, subtitles should help hide cadence changes.

## Audio guidance

- Do not cut off consonants, breaths, or room tone too abruptly.
- Keep a tiny audio safety margin around hard cuts when possible.
- If exporting through another tool, note where short crossfades or room-tone fill may be needed.

## Escalate for manual review

Mark a sentence `review` instead of forcing a decision when:

- ASR confidence is weak
- two speakers overlap
- the sentence is semantically important but poorly transcribed
- the user intent depends on tone rather than literal words
