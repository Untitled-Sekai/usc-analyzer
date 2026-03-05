"""Command-line interface for USC Analyzer."""

import argparse
import sys
from pathlib import Path
import json

from . import USCAnalyzer, __version__


def main() -> int:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Analyze USC (Universal Sekai Chart) files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "file",
        type=str,
        help="Path to USC file",
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"usc-analyzer {__version__}",
    )
    
    parser.add_argument(
        "-s", "--summary",
        action="store_true",
        help="Show summary of the chart (default)",
    )
    
    parser.add_argument(
        "-n", "--notes",
        action="store_true",
        help="Show detailed note statistics",
    )
    
    parser.add_argument(
        "-c", "--chart",
        action="store_true",
        help="Show chart information",
    )
    
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate the USC file",
    )
    
    parser.add_argument(
        "--bpm",
        action="store_true",
        help="Show BPM changes",
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format",
    )
    
    args = parser.parse_args()
    
    # Load and analyze file
    try:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            return 1
        
        analyzer = USCAnalyzer.from_file(file_path)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    # Show summary by default
    if not any([args.notes, args.chart, args.validate, args.bpm]):
        args.summary = True
    
    # Validation
    if args.validate:
        issues = analyzer.validate()
        if args.json:
            output = {"valid": len(issues) == 0, "issues": issues}
            print(json.dumps(output, indent=2))
        else:
            if issues:
                print("=== Validation Issues ===")
                for issue in issues:
                    print(f"  - {issue}")
                print()
            else:
                print("✓ USC file is valid")
                print()
    
    # BPM changes
    if args.bpm:
        bpm_changes = analyzer.get_bpm_changes()
        if args.json:
            output = [
                {"beat": bpm.beat, "bpm": bpm.bpm}
                for bpm in bpm_changes
            ]
            print(json.dumps(output, indent=2))
        else:
            print("=== BPM Changes ===")
            for bpm in bpm_changes:
                print(f"  Beat {bpm.beat}: {bpm.bpm} BPM")
            print()
    
    # Note statistics
    if args.notes:
        stats = analyzer.analyze_notes()
        if args.json:
            output = {
                "total_notes": stats.total_notes,
                "single": {
                    "total": stats.total_single,
                    "normal_tap": stats.normal_tap,
                    "critical_tap": stats.critical_tap,
                    "normal_trace": stats.normal_trace,
                    "critical_trace": stats.critical_trace,
                },
                "flicks": {
                    "total": stats.total_flick,
                    "normal": stats.normal_flick,
                    "critical": stats.critical_flick,
                    "trace": stats.trace_flick,
                    "critical_trace": stats.critical_trace_flick,
                    "by_direction": {
                        "left": stats.left_flick,
                        "up": stats.up_flick,
                        "right": stats.right_flick,
                        "none": stats.none_direction_flick,
                    },
                },
                "damage": stats.damage_notes,
                "slides": {
                    "total": stats.slides,
                    "normal": stats.slide_normal,
                    "trace": stats.slide_trace,
                    "none": stats.slide_none,
                    "connections": stats.slide_connections,
                },
                "guides": stats.guides,
            }
            print(json.dumps(output, indent=2))
        else:
            print("=== Note Statistics ===")
            print(f"Total Notes: {stats.total_notes}")
            print(f"  Single: {stats.total_single}")
            print(f"    Normal Tap: {stats.normal_tap}")
            print(f"    Critical Tap: {stats.critical_tap}")
            print(f"    Normal Trace: {stats.normal_trace}")
            print(f"    Critical Trace: {stats.critical_trace}") 
            print(f"  Flicks: {stats.total_flick}")
            print(f"    Normal: {stats.normal_flick}")
            print(f"    Critical: {stats.critical_flick}")
            print(f"    Trace: {stats.trace_flick}")
            print(f"    Critical Trace: {stats.critical_trace_flick}")
            print(f"  Damage: {stats.damage_notes}")
            print(f"  Slides: {stats.slides}")
            print(f"  Guides: {stats.guides}")
            print()
    
    # Chart information
    if args.chart:
        info = analyzer.analyze_chart()
        if args.json:
            output = {
                "version": info.version,
                "offset": info.offset,
                "bpm": {
                    "initial": info.initial_bpm,
                    "changes": info.bpm_changes,
                    "min": info.min_bpm,
                    "max": info.max_bpm,
                },
                "time_scale_groups": info.time_scale_groups,
                "range": {
                    "min_beat": info.min_beat,
                    "max_beat": info.max_beat,
                    "min_tick": info.min_tick,
                    "max_tick": info.max_tick,
                    "duration_beats": info.duration_beats,
                    "duration_ticks": info.duration_ticks,
                },
            }
            print(json.dumps(output, indent=2))
        else:
            print("=== Chart Information ===")
            print(f"Version: {info.version}")
            print(f"Offset: {info.offset}")
            print(f"Initial BPM: {info.initial_bpm}")
            print(f"BPM Changes: {info.bpm_changes}")
            print(f"BPM Range: {info.min_bpm} - {info.max_bpm}")
            print(f"Time Scale Groups: {info.time_scale_groups}")
            print(f"Beat Range: {info.min_beat} - {info.max_beat}")
            print(f"Duration: {info.duration_beats:.2f} beats")
            print()
    
    # Summary
    if args.summary and not args.json:
        print(analyzer.summary())
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
