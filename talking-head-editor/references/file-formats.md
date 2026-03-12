# Talking-Head Output Formats

Use this file when returning structured editing outputs.

## `edit_decision.json`

```json
{
  "meta": {
    "project_name": "sample_talking_head",
    "pacing_preset": "creator",
    "source_type": "srt",
    "confidence": "high"
  },
  "sentences": [
    {
      "sentence_id": "sent_001",
      "start": 0.42,
      "end": 3.18,
      "text": "今天我想讲三个让视频更紧凑的方法。",
      "decision": "keep",
      "reason": "hook"
    },
    {
      "sentence_id": "sent_002",
      "start": 3.18,
      "end": 4.01,
      "text": "嗯，先说第一个。",
      "decision": "trim",
      "reason": "filler"
    }
  ],
  "merged_segments": [
    {
      "segment_id": "seg_001",
      "start": 0.34,
      "end": 6.22,
      "source_sentence_ids": ["sent_001", "sent_002", "sent_003"],
      "notes": "same framing, small punch-in recommended"
    }
  ],
  "cover_notes": [
    {
      "segment_id": "seg_001",
      "type": "punch_in",
      "note": "104% zoom for the second sentence"
    }
  ],
  "subtitle_plan": {
    "style": "keyword_emphasis",
    "max_words_per_unit": 10,
    "notes": "highlight numbers and contrasts"
  }
}
```

## Sentence decision table

Use this lightweight table in conversational responses:

| sentence_id | start | end | decision | reason |
| --- | --- | --- | --- | --- |
| sent_001 | 0.42 | 3.18 | keep | hook |
| sent_002 | 3.18 | 4.01 | trim | filler |

## Merged segment table

| segment_id | start | end | sentence_ids | notes |
| --- | --- | --- | --- | --- |
| seg_001 | 0.34 | 6.22 | sent_001,sent_002,sent_003 | punch-in recommended |

## Field rules

- `start` and `end` use seconds with up to 2 decimal places unless a downstream tool requires milliseconds.
- `decision` must be one of `keep`, `trim`, `delete`, or `review`.
- `reason` should be short and reusable.
- `merged_segments` must be sorted by time and must not overlap.
- `source_sentence_ids` preserve traceability from transcript decisions to execution ranges.
