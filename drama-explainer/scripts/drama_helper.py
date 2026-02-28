#!/usr/bin/env python3
"""
短剧解说项目管理与画面匹配辅助脚本
支持项目目录初始化、状态跟踪、画面分配和 timeline 生成
支持多源视频独立处理
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# 项目子目录结构
PROJECT_DIRS = [
    "analysis",
    "scripts",
    "audio",
    "clips/voiceover",
    "clips/original",
    "clips/merged",
    "output",
]

STATE_FILE = "state.json"

STEP_NAMES = {
    "1_analysis": "分析原片",
    "2_plot_analysis": "初步剧情分析",
    "3_visual_analysis": "视觉分析",
    "4_verification": "校验与人物建档",
    "5_script": "撰写文案",
    "6_audio": "生成音频",
    "7_matching": "画面匹配",
    "8_clips": "截取视频",
    "9_render": "渲染输出",
}


def create_initial_state(name: str, sources: List[str], style: int) -> Dict:
    """创建初始状态（支持多源）"""
    abs_sources = [os.path.abspath(s) for s in sources]
    media_sources = [
        {
            "path": s,
            "duration": 0,
            "width": 0,
            "height": 0,
            "fps": 25,
        }
        for s in abs_sources
    ]

    return {
        "project": {
            "name": name,
            "sources": abs_sources,
            "style": style,
            "created_at": datetime.now(timezone.utc).isoformat(),
        },
        "progress": {
            "current_step": 0,
            "steps": {key: "pending" for key in STEP_NAMES},
        },
        "media": {
            "sources": media_sources,
        },
        "segments": [],
        "used_time_ranges": {str(i + 1): [] for i in range(len(abs_sources))},
    }


def load_state(project_dir: str) -> Dict:
    """加载项目状态"""
    state_path = os.path.join(project_dir, STATE_FILE)
    if not os.path.exists(state_path):
        print(f"错误: 项目状态文件不存在: {state_path}")
        print("请先运行 init 初始化项目")
        sys.exit(1)
    with open(state_path, "r", encoding="utf-8") as f:
        state = json.load(f)
    return _migrate_state(state)


def _migrate_state(state: Dict) -> Dict:
    """向后兼容：将旧格式迁移为新格式"""
    project = state.get("project", {})

    # project.source (string) → project.sources (array)
    if "source" in project and "sources" not in project:
        project["sources"] = [project.pop("source")]

    # media 扁平格式 → media.sources 数组格式
    media = state.get("media", {})
    if "sources" not in media and "duration" in media:
        sources = project.get("sources", [])
        path = sources[0] if sources else ""
        media_entry = {
            "path": path,
            "duration": media.pop("duration", 0),
            "width": media.pop("width", 0),
            "height": media.pop("height", 0),
            "fps": media.pop("fps", 25),
        }
        # 清理旧字段
        for key in ["codec", "audio_channels", "audio_sample_rate"]:
            media.pop(key, None)
        media["sources"] = [media_entry]

    # used_time_ranges: list → dict keyed by source_index
    ranges = state.get("used_time_ranges", {})
    if isinstance(ranges, list):
        state["used_time_ranges"] = {"1": ranges}

    return state


def save_state(project_dir: str, state: Dict) -> None:
    """保存项目状态"""
    state_path = os.path.join(project_dir, STATE_FILE)
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def get_total_duration(state: Dict, source_index: int = 1) -> float:
    """获取指定源的视频总时长"""
    sources = state.get("media", {}).get("sources", [])
    idx = source_index - 1
    if 0 <= idx < len(sources):
        return sources[idx].get("duration", 0)
    return 0


def get_used_ranges(state: Dict, source_index: int = 1) -> List[List[float]]:
    """获取指定源的已用时间段"""
    ranges = state.get("used_time_ranges", {})
    return ranges.get(str(source_index), [])


def add_used_range(
    state: Dict, source_index: int, start: float, end: float
) -> None:
    """添加已用时间段到指定源"""
    key = str(source_index)
    if key not in state["used_time_ranges"]:
        state["used_time_ranges"][key] = []
    state["used_time_ranges"][key].append([start, end])


def is_time_available(
    used_ranges: List[List[float]], start: float, end: float, duration: float
) -> bool:
    """检查时间段是否可用"""
    if start < 0 or end > duration:
        return False
    for used_start, used_end in used_ranges:
        if not (end <= used_start or start >= used_end):
            return False
    return True


def find_available_slot(
    used_ranges: List[List[float]],
    total_duration: float,
    needed_duration: float,
    preferred_start: Optional[float] = None,
) -> Optional[Tuple[float, float]]:
    """寻找可用时间段"""
    if preferred_start is not None:
        end = preferred_start + needed_duration
        if is_time_available(used_ranges, preferred_start, end, total_duration):
            return (preferred_start, end)
        for offset in [5, 10, 20, 30]:
            fwd_start = preferred_start + offset
            if is_time_available(
                used_ranges, fwd_start, fwd_start + needed_duration, total_duration
            ):
                return (fwd_start, fwd_start + needed_duration)
            bwd_start = preferred_start - offset
            if bwd_start >= 0 and is_time_available(
                used_ranges, bwd_start, bwd_start + needed_duration, total_duration
            ):
                return (bwd_start, bwd_start + needed_duration)

    current = 0.0
    while current + needed_duration <= total_duration:
        if is_time_available(
            used_ranges, current, current + needed_duration, total_duration
        ):
            return (current, current + needed_duration)
        current += 0.5
    return None


def cmd_init(args: argparse.Namespace) -> None:
    """初始化项目���录和状态文件（支持多源）"""
    project_dir = args.project_dir

    if os.path.exists(os.path.join(project_dir, STATE_FILE)):
        print(f"错误: 项目已存在: {project_dir}")
        print("如需重新初始化，请先删除该目录")
        sys.exit(1)

    for sub_dir in PROJECT_DIRS:
        os.makedirs(os.path.join(project_dir, sub_dir), exist_ok=True)

    name = os.path.basename(os.path.abspath(project_dir))
    state = create_initial_state(name, args.source, args.style)
    save_state(project_dir, state)

    print(f"项目初始化完成: {project_dir}")
    print(f"  原片数量: {len(args.source)}")
    for i, src in enumerate(args.source, 1):
        print(f"    [{i}] {src}")
    print(f"  风格: {args.style}")
    print(f"  目录结构:")
    for sub_dir in PROJECT_DIRS:
        print(f"    {sub_dir}/")


def cmd_add(args: argparse.Namespace) -> None:
    """添加解说片段"""
    state = load_state(args.project_dir)
    source_index = args.source_index if args.source_index else 1

    segment = {
        "id": args.index,
        "source_index": source_index,
        "vo_text": args.text,
        "vo_duration": args.vo_duration,
        "orig_duration": args.orig_duration if args.orig_duration else args.vo_duration,
        "vo_video": None,
        "orig_video": None,
        "audio_file": f"audio/vo_{args.index:02d}.mp3",
        "status": "pending",
    }

    existing_ids = {s["id"] for s in state["segments"]}
    if args.index in existing_ids:
        state["segments"] = [
            segment if s["id"] == args.index else s for s in state["segments"]
        ]
        print(f"更新片段 #{args.index}")
    else:
        state["segments"].append(segment)
        state["segments"].sort(key=lambda s: s["id"])
        print(f"添加片段 #{args.index}")

    print(f"  源文件: [{source_index}]")
    print(f"  解说时长: {segment['vo_duration']}s")
    print(f"  原片时长: {segment['orig_duration']}s")
    print(f"  文案: {args.text[:40]}...")

    save_state(args.project_dir, state)


def cmd_allocate_video(args: argparse.Namespace) -> None:
    """为解说分配画面"""
    state = load_state(args.project_dir)

    segment = None
    for s in state["segments"]:
        if s["id"] == args.index:
            segment = s
            break

    if segment is None:
        print(f"错误: 片段 #{args.index} 不存在")
        sys.exit(1)

    source_index = segment.get("source_index", 1)
    total_duration = get_total_duration(state, source_index)

    if total_duration <= 0:
        print("错误: 视频时长未设置，请先完成步骤1（分析原片）")
        sys.exit(1)

    used_ranges = get_used_ranges(state, source_index)
    slot = find_available_slot(
        used_ranges,
        total_duration,
        segment["vo_duration"],
        args.preferred_start,
    )

    if slot is None:
        print(f"错误: 无法为片段 #{args.index} 找到 {segment['vo_duration']}s 的画面")
        sys.exit(1)

    segment["vo_video"] = {"start": slot[0], "end": slot[1]}
    add_used_range(state, source_index, slot[0], slot[1])
    save_state(args.project_dir, state)
    print(f"解说画面 #{args.index} (源[{source_index}]): {slot[0]:.1f}s - {slot[1]:.1f}s")


def cmd_allocate_orig(args: argparse.Namespace) -> None:
    """为原片分配画面"""
    state = load_state(args.project_dir)

    segment = None
    for s in state["segments"]:
        if s["id"] == args.index:
            segment = s
            break

    if segment is None:
        print(f"错误: 片段 #{args.index} 不存在")
        sys.exit(1)

    source_index = segment.get("source_index", 1)
    total_duration = get_total_duration(state, source_index)

    if total_duration <= 0:
        print("错误: 视频时长未设置，请先完成步骤1（分析原片）")
        sys.exit(1)

    used_ranges = get_used_ranges(state, source_index)
    slot = find_available_slot(
        used_ranges,
        total_duration,
        segment["orig_duration"],
        args.preferred_start,
    )

    if slot is None:
        print(
            f"错误: 无法为片段 #{args.index} 找到 {segment['orig_duration']}s 的原片画面"
        )
        sys.exit(1)

    segment["orig_video"] = {"start": slot[0], "end": slot[1]}
    add_used_range(state, source_index, slot[0], slot[1])
    save_state(args.project_dir, state)
    print(f"原片画面 #{args.index} (源[{source_index}]): {slot[0]:.1f}s - {slot[1]:.1f}s")


def cmd_auto(args: argparse.Namespace) -> None:
    """自动按序分配所有片段的画面"""
    state = load_state(args.project_dir)

    # 重置所有源的已用时间段
    sources = state.get("project", {}).get("sources", [])
    state["used_time_ranges"] = {str(i + 1): [] for i in range(len(sources))}

    for segment in state["segments"]:
        source_index = segment.get("source_index", 1)
        total_duration = get_total_duration(state, source_index)

        if total_duration <= 0:
            print(f"错误: 源[{source_index}] 视频时长未设置，请先完成步骤1")
            sys.exit(1)

        used_ranges = get_used_ranges(state, source_index)
        vo_slot = find_available_slot(
            used_ranges, total_duration, segment["vo_duration"]
        )
        if vo_slot is None:
            print(f"错误: 无法为片段 #{segment['id']} 分配解说画面 (源[{source_index}])")
            sys.exit(1)
        segment["vo_video"] = {"start": vo_slot[0], "end": vo_slot[1]}
        add_used_range(state, source_index, vo_slot[0], vo_slot[1])

        used_ranges = get_used_ranges(state, source_index)
        orig_slot = find_available_slot(
            used_ranges, total_duration, segment["orig_duration"]
        )
        if orig_slot is None:
            print(f"错误: 无法为片段 #{segment['id']} 分配原片画面 (源[{source_index}])")
            sys.exit(1)
        segment["orig_video"] = {"start": orig_slot[0], "end": orig_slot[1]}
        add_used_range(state, source_index, orig_slot[0], orig_slot[1])

    save_state(args.project_dir, state)
    print(f"自动分配完成，共 {len(state['segments'])} 个片段")


def cmd_timeline(args: argparse.Namespace) -> None:
    """生成 timeline.json"""
    state = load_state(args.project_dir)
    clips = []
    current_time = 0.0
    sources = state.get("project", {}).get("sources", [])

    for segment in state["segments"]:
        vo_dur = segment["vo_duration"]
        orig_dur = segment["orig_duration"]
        seg_id = segment["id"]

        clips.append(
            {
                "path": f"clips/voiceover/clip_vo_{seg_id:02d}.mp4",
                "start": current_time,
                "end": current_time + vo_dur,
                "mute": True,
            }
        )
        clips.append(
            {
                "path": f"audio/vo_{seg_id:02d}.mp3",
                "start": current_time,
                "end": current_time + vo_dur,
            }
        )
        current_time += vo_dur

        clips.append(
            {
                "path": f"clips/original/clip_orig_{seg_id:02d}.mp4",
                "start": current_time,
                "end": current_time + orig_dur,
                "mute": False,
            }
        )
        current_time += orig_dur

    total_vo = sum(s["vo_duration"] for s in state["segments"])
    total_orig = sum(s["orig_duration"] for s in state["segments"])

    # 使用第一个源文件的分辨率作为输出参数
    first_source = {}
    media_sources = state.get("media", {}).get("sources", [])
    if media_sources:
        first_source = media_sources[0]

    timeline = {
        "clips": clips,
        "voiceover": None,
        "bgm": None,
        "output": {
            "width": first_source.get("width", 720),
            "height": first_source.get("height", 1280),
            "fps": first_source.get("fps", 25),
            "total_duration": total_vo + total_orig,
        },
    }

    timeline_path = os.path.join(args.project_dir, "output", "timeline.json")
    with open(timeline_path, "w", encoding="utf-8") as f:
        json.dump(timeline, f, indent=2, ensure_ascii=False)

    print(f"Timeline 已生成: {timeline_path}")
    print(json.dumps(timeline, indent=2, ensure_ascii=False))


def cmd_step(args: argparse.Namespace) -> None:
    """更新步骤状态"""
    state = load_state(args.project_dir)
    step_key = args.step

    if step_key not in state["progress"]["steps"]:
        print(f"错误: 无效步骤: {step_key}")
        print(f"可选步骤: {', '.join(STEP_NAMES.keys())}")
        sys.exit(1)

    state["progress"]["steps"][step_key] = args.status
    step_num = int(step_key.split("_")[0])
    if args.status == "in_progress":
        state["progress"]["current_step"] = step_num
    elif args.status == "completed" and step_num >= state["progress"]["current_step"]:
        state["progress"]["current_step"] = step_num + 1

    save_state(args.project_dir, state)
    print(f"步骤 {step_key} ({STEP_NAMES[step_key]}): {args.status}")


def cmd_summary(args: argparse.Namespace) -> None:
    """显示项目摘要"""
    state = load_state(args.project_dir)

    print("\n" + "=" * 60)
    print(f"项目: {state['project']['name']}")
    print("=" * 60)

    sources = state["project"].get("sources", [])
    print(f"原片数量: {len(sources)}")
    for i, src in enumerate(sources, 1):
        print(f"  [{i}] {src}")
    print(f"风格: {state['project']['style']}")
    print(f"创建时间: {state['project']['created_at']}")

    media_sources = state.get("media", {}).get("sources", [])
    for i, ms in enumerate(media_sources, 1):
        if ms.get("duration", 0) > 0:
            print(f"\n源[{i}] 视频信息:")
            print(f"  时长: {ms['duration']:.1f}s")
            print(f"  分辨率: {ms['width']}x{ms['height']}")

    print(f"\n进度 (当前步骤: {state['progress']['current_step']}):")
    print("-" * 40)
    for key, name in STEP_NAMES.items():
        status = state["progress"]["steps"].get(key, "pending")
        icon = {"pending": " ", "in_progress": "~", "completed": "x"}.get(status, "?")
        print(f"  [{icon}] {key}: {name} ({status})")

    if state["segments"]:
        total_vo = sum(s["vo_duration"] for s in state["segments"])
        total_orig = sum(s["orig_duration"] for s in state["segments"])

        print(f"\n片段: {len(state['segments'])} 个")
        print(f"解说总时长: {total_vo:.1f}s")
        print(f"原片总时长: {total_orig:.1f}s")
        print(f"预估成片时长: {total_vo + total_orig:.1f}s")

        total_media_duration = sum(
            ms.get("duration", 0) for ms in media_sources
        )
        if total_media_duration > 0:
            usage = (total_vo + total_orig) / total_media_duration * 100
            print(f"画面使用率: {usage:.1f}%")

        print(f"\n片段详情:")
        print("-" * 60)
        for seg in state["segments"]:
            source_idx = seg.get("source_index", 1)
            print(f"\n  #{seg['id']} (源[{source_idx}]):")
            print(f"    文案: {seg['vo_text'][:40]}...")
            print(f"    解说: {seg['vo_duration']:.1f}s | 原片: {seg['orig_duration']:.1f}s")
            if seg["vo_video"]:
                print(
                    f"    解说画面: {seg['vo_video']['start']:.1f}s - {seg['vo_video']['end']:.1f}s"
                )
            if seg["orig_video"]:
                print(
                    f"    原片画面: {seg['orig_video']['start']:.1f}s - {seg['orig_video']['end']:.1f}s"
                )
            print(f"    状态: {seg['status']}")

    print("\n" + "=" * 60)


def cmd_verify(args):
    """验证 scene_matching.json 是否有时间冲突（支持多源）"""
    json_path = args.json_file

    if not os.path.exists(json_path):
        print(f"错误：文件不存在：{json_path}")
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    errors = []
    warnings = []

    segments = data.get("segments", [])

    # 按 source_index 分组检查
    source_ranges: Dict[int, List[Tuple[float, float, str]]] = {}

    for i, seg in enumerate(segments):
        source_index = seg.get("source_index", 1)
        vo_start = seg.get("vo_video", {}).get("start")
        vo_end = seg.get("vo_video", {}).get("end")
        orig_start = seg.get("orig_video", {}).get("start")
        orig_end = seg.get("orig_video", {}).get("end")

        if None in [vo_start, vo_end, orig_start, orig_end]:
            errors.append(f"片段{i+1}: 时间段数据不完整")
            continue

        # 检查同一片段内 vo_video 和 orig_video 是否重叠
        if not (vo_end <= orig_start or orig_end <= vo_start):
            overlap_start = max(vo_start, orig_start)
            overlap_end = min(vo_end, orig_end)
            errors.append(
                f"片段{i+1} (源[{source_index}]): "
                f"vo_video[{vo_start:.1f}-{vo_end:.1f}] 与 "
                f"orig_video[{orig_start:.1f}-{orig_end:.1f}] "
                f"重叠 {overlap_start:.1f}s-{overlap_end:.1f}s"
            )

        # 收集时间段按源分组
        if source_index not in source_ranges:
            source_ranges[source_index] = []
        source_ranges[source_index].append(
            (vo_start, vo_end, f"片段{i+1}_vo")
        )
        source_ranges[source_index].append(
            (orig_start, orig_end, f"片段{i+1}_orig")
        )

    # 按源分组检查全局时间冲突
    for source_idx, ranges in sorted(source_ranges.items()):
        ranges.sort(key=lambda x: x[0])
        for j in range(len(ranges) - 1):
            curr = ranges[j]
            next_r = ranges[j + 1]
            if curr[1] > next_r[0]:
                errors.append(
                    f"源[{source_idx}] 全局冲突："
                    f"{curr[2]}[{curr[0]:.1f}-{curr[1]:.1f}] 与 "
                    f"{next_r[2]}[{next_r[0]:.1f}-{next_r[1]:.1f}] 重叠"
                )

    # 输出结果
    if errors:
        print("\n\u274c 验证失败 - 发现以下问题:\n")
        for err in errors:
            print(f"  ERROR: {err}")
        if warnings:
            print()
        for warn in warnings:
            print(f"  WARNING: {warn}")
        print(f"\n共发现 {len(errors)} 个错误，必须修正后才能继续。\n")
        sys.exit(1)
    else:
        print("\n\u2705 验证通过 - 所有时间段无冲突！\n")
        if warnings:
            print("注意:\n")
            for warn in warnings:
                print(f"  WARNING: {warn}")
            print()
        sys.exit(0)


def build_parser() -> argparse.ArgumentParser:
    """构建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description="短剧解说项目管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s init --project-dir 我的短剧01 --source video.mp4
  %(prog)s init --project-dir 我的短剧01 --source part1.mp4 part2.mp4 part3.mp4
  %(prog)s add --project-dir 我的短剧01 1 10.5 "这个男人刚走进办公室"
  %(prog)s add --project-dir 我的短剧01 5 8.0 "到了第二个视频" --source-index 2
  %(prog)s auto --project-dir 我的短剧01
  %(prog)s timeline --project-dir 我的短剧01
  %(prog)s summary --project-dir 我的短剧01
        """,
    )
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # init（支持多源）
    p_init = subparsers.add_parser("init", help="初始化项目")
    p_init.add_argument("--project-dir", required=True, help="项目目录路径")
    p_init.add_argument(
        "--source", required=True, nargs="+", help="原片文件路径（支持多个）"
    )
    p_init.add_argument("--style", type=int, default=1, help="解说风格ID (默认1)")

    # add
    p_add = subparsers.add_parser("add", help="添加解说片段")
    p_add.add_argument("--project-dir", required=True, help="项目目录路径")
    p_add.add_argument("index", type=int, help="片段序号")
    p_add.add_argument("vo_duration", type=float, help="解说音频时长(秒)")
    p_add.add_argument("text", help="解说文案")
    p_add.add_argument(
        "--orig-duration", type=float, help="原片片段时长(秒)，默认等于解说时长"
    )
    p_add.add_argument(
        "--source-index", type=int, default=1, help="源文件编号（从1开始，默认1）"
    )

    # allocate_video
    p_alloc_vo = subparsers.add_parser("allocate_video", help="为解说分配画面")
    p_alloc_vo.add_argument("--project-dir", required=True, help="项目目录路径")
    p_alloc_vo.add_argument("index", type=int, help="片段序号")
    p_alloc_vo.add_argument(
        "preferred_start", type=float, nargs="?", default=None, help="优先起始秒"
    )

    # allocate_orig
    p_alloc_orig = subparsers.add_parser("allocate_orig", help="为原片分配画面")
    p_alloc_orig.add_argument("--project-dir", required=True, help="项目目录路径")
    p_alloc_orig.add_argument("index", type=int, help="片段序号")
    p_alloc_orig.add_argument(
        "preferred_start", type=float, nargs="?", default=None, help="优先起始秒"
    )

    # auto
    p_auto = subparsers.add_parser("auto", help="自动按序分配所有画面")
    p_auto.add_argument("--project-dir", required=True, help="项目目录路径")

    # timeline
    p_timeline = subparsers.add_parser("timeline", help="生成 timeline.json")
    p_timeline.add_argument("--project-dir", required=True, help="项目目录路径")

    # step
    p_step = subparsers.add_parser("step", help="更新步骤状态")
    p_step.add_argument("--project-dir", required=True, help="项目目录路径")
    p_step.add_argument("step", choices=list(STEP_NAMES.keys()), help="步骤名称")
    p_step.add_argument(
        "status", choices=["pending", "in_progress", "completed"], help="状态"
    )

    # summary
    p_summary = subparsers.add_parser("summary", help="显示项目摘要")
    p_summary.add_argument("--project-dir", required=True, help="项目目录路径")

    # verify
    p_verify = subparsers.add_parser(
        "verify", help="验证 scene_matching.json 时间冲突"
    )
    p_verify.add_argument("json_file", help="scene_matching.json 文件路径")

    return parser


COMMAND_MAP = {
    "init": cmd_init,
    "add": cmd_add,
    "allocate_video": cmd_allocate_video,
    "allocate_orig": cmd_allocate_orig,
    "auto": cmd_auto,
    "timeline": cmd_timeline,
    "step": cmd_step,
    "summary": cmd_summary,
    "verify": cmd_verify,
}


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    handler = COMMAND_MAP.get(args.command)
    if handler:
        handler(args)
    else:
        print(f"未知命令: {args.command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
