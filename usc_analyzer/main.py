"""USC Analyzer - Analyze USC (Universal Sekai Chart) files."""

import json
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

from .type import (
    USCFile,
    SingleNote,
    DamageNote,
    Slide,
    Guide,
    TimeScaleGroup,
    BPM,
    beat_to_tick,
)


@dataclass
class NoteStatistics:
    """Statistics about notes in a USC file."""
    
    # Single notes
    total_single: int = 0
    normal_tap: int = 0
    critical_tap: int = 0
    normal_trace: int = 0
    critical_trace: int = 0
    
    # Flicks
    total_flick: int = 0
    normal_flick: int = 0
    critical_flick: int = 0
    trace_flick: int = 0
    critical_trace_flick: int = 0
    
    # By direction
    left_flick: int = 0
    up_flick: int = 0
    right_flick: int = 0
    none_direction_flick: int = 0
    
    # Other note types
    damage_notes: int = 0
    slides: int = 0
    guides: int = 0
    
    # Slide connections
    slide_connections: int = 0
    slide_normal: int = 0
    slide_trace: int = 0
    slide_none: int = 0
    
    @property
    def total_notes(self) -> int:
        """Total number of playable notes (excluding guides)."""
        return self.total_single + self.damage_notes + self.slides
    
    @property
    def total_objects(self) -> int:
        """Total number of all objects."""
        return self.total_notes + self.guides


@dataclass
class ChartInfo:
    """Information about the chart."""
    
    version: int
    offset: float
    
    # BPM information
    initial_bpm: Optional[float] = None
    bpm_changes: int = 0
    min_bpm: Optional[float] = None
    max_bpm: Optional[float] = None
    
    # Time scale groups
    time_scale_groups: int = 0
    
    # Beat/tick range
    min_beat: Optional[float] = None
    max_beat: Optional[float] = None
    
    @property
    def min_tick(self) -> Optional[int]:
        """Minimum tick (converted from min_beat)."""
        return beat_to_tick(self.min_beat) if self.min_beat is not None else None
    
    @property
    def max_tick(self) -> Optional[int]:
        """Maximum tick (converted from max_beat)."""
        return beat_to_tick(self.max_beat) if self.max_beat is not None else None
    
    @property
    def duration_beats(self) -> Optional[float]:
        """Chart duration in beats."""
        if self.min_beat is not None and self.max_beat is not None:
            return self.max_beat - self.min_beat
        return None
    
    @property
    def duration_ticks(self) -> Optional[int]:
        """Chart duration in ticks."""
        if self.min_tick is not None and self.max_tick is not None:
            return self.max_tick - self.min_tick
        return None


class USCAnalyzer:
    """Analyzer for USC files."""
    
    def __init__(self, usc_file: USCFile):
        """
        Initialize analyzer with a parsed USC file.
        
        Args:
            usc_file: Parsed USC file object
        """
        self.usc_file = usc_file
        self._note_stats: Optional[NoteStatistics] = None
        self._chart_info: Optional[ChartInfo] = None
    
    @classmethod
    def from_file(cls, file_path: str | Path) -> "USCAnalyzer":
        """
        Load and analyze a USC file.
        
        Args:
            file_path: Path to the USC file
            
        Returns:
            USCAnalyzer instance
            
        Raises:
            FileNotFoundError: If the file does not exist
            json.JSONDecodeError: If the file is not valid JSON
            pydantic.ValidationError: If the file does not match USC schema
        """
        path = Path(file_path)
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        
        usc_file = USCFile.model_validate(data)
        return cls(usc_file)
    
    @classmethod
    def from_dict(cls, data: dict) -> "USCAnalyzer":
        """
        Create analyzer from a dictionary.
        
        Args:
            data: USC data as dictionary
            
        Returns:
            USCAnalyzer instance
        """
        usc_file = USCFile.model_validate(data)
        return cls(usc_file)
    
    @classmethod
    def from_json(cls, json_str: str) -> "USCAnalyzer":
        """
        Create analyzer from a JSON string.
        
        Args:
            json_str: USC data as JSON string
            
        Returns:
            USCAnalyzer instance
        """
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def analyze_notes(self) -> NoteStatistics:
        """
        Analyze note statistics.
        
        Returns:
            NoteStatistics object with detailed note counts
        """
        if self._note_stats is not None:
            return self._note_stats
        
        stats = NoteStatistics()
        
        for obj in self.usc_file.usc.objects:
            if isinstance(obj, SingleNote):
                stats.total_single += 1
                
                # Check if it's a flick
                if obj.direction is not None:
                    stats.total_flick += 1
                    
                    # Count by direction
                    if obj.direction == "left":
                        stats.left_flick += 1
                    elif obj.direction == "up":
                        stats.up_flick += 1
                    elif obj.direction == "right":
                        stats.right_flick += 1
                    elif obj.direction == "none":
                        stats.none_direction_flick += 1
                    
                    # Count by type
                    if obj.critical and obj.trace:
                        stats.critical_trace_flick += 1
                    elif obj.critical:
                        stats.critical_flick += 1
                    elif obj.trace:
                        stats.trace_flick += 1
                    else:
                        stats.normal_flick += 1
                else:
                    # Regular tap/trace
                    if obj.critical and obj.trace:
                        stats.critical_trace += 1
                    elif obj.critical:
                        stats.critical_tap += 1
                    elif obj.trace:
                        stats.normal_trace += 1
                    else:
                        stats.normal_tap += 1
            
            elif isinstance(obj, DamageNote):
                stats.damage_notes += 1
            
            elif isinstance(obj, Slide):
                stats.slides += 1
                stats.slide_connections += len(obj.connections)
                
                # Get judge type from start connection
                if obj.connections:
                    start = obj.connections[0]
                    if start.judgeType == "normal":
                        stats.slide_normal += 1
                    elif start.judgeType == "trace":
                        stats.slide_trace += 1
                    elif start.judgeType == "none":
                        stats.slide_none += 1
            
            elif isinstance(obj, Guide):
                stats.guides += 1
        
        self._note_stats = stats
        return stats
    
    def analyze_chart(self) -> ChartInfo:
        """
        Analyze chart information.
        
        Returns:
            ChartInfo object with chart metadata
        """
        if self._chart_info is not None:
            return self._chart_info
        
        info = ChartInfo(
            version=self.usc_file.version,
            offset=self.usc_file.usc.offset,
        )
        
        bpm_values: list[float] = []
        beats: list[float] = []
        
        for obj in self.usc_file.usc.objects:
            if isinstance(obj, BPM):
                info.bpm_changes += 1
                bpm_values.append(obj.bpm)
                beats.append(obj.beat)
                
                if info.initial_bpm is None and obj.beat == 0.0:
                    info.initial_bpm = obj.bpm
            
            elif isinstance(obj, TimeScaleGroup):
                info.time_scale_groups += 1
            
            elif isinstance(obj, (SingleNote, DamageNote)):
                beats.append(obj.beat)
            
            elif isinstance(obj, Slide):
                for conn in obj.connections:
                    beats.append(conn.beat)
            
            elif isinstance(obj, Guide):
                for midpoint in obj.midpoints:
                    beats.append(midpoint.beat)
        
        if bpm_values:
            info.min_bpm = min(bpm_values)
            info.max_bpm = max(bpm_values)
        
        if beats:
            info.min_beat = min(beats)
            info.max_beat = max(beats)
        
        self._chart_info = info
        return info
    
    def get_bpm_changes(self) -> list[BPM]:
        """
        Get all BPM change events.
        
        Returns:
            List of BPM objects sorted by beat
        """
        bpm_changes = [obj for obj in self.usc_file.usc.objects if isinstance(obj, BPM)]
        return sorted(bpm_changes, key=lambda x: x.beat)
    
    def get_time_scale_groups(self) -> list[TimeScaleGroup]:
        """
        Get all time scale groups.
        
        Returns:
            List of TimeScaleGroup objects in order of appearance
        """
        return [obj for obj in self.usc_file.usc.objects if isinstance(obj, TimeScaleGroup)]
    
    def validate(self) -> list[str]:
        """
        Validate the USC file structure.
        
        Returns:
            List of validation warnings/errors (empty if valid)
        """
        issues: list[str] = []
        
        # Check if there's at least one BPM
        bpm_changes = self.get_bpm_changes()
        if not bpm_changes:
            issues.append("No BPM defined in the chart")
        elif bpm_changes[0].beat != 0.0:
            issues.append(f"Initial BPM should be at beat 0.0, found at beat {bpm_changes[0].beat}")
        
        # Check time scale groups
        time_scale_groups = self.get_time_scale_groups()
        max_tsg_index = len(time_scale_groups) - 1
        
        # Validate timeScaleGroup references
        for obj in self.usc_file.usc.objects:
            if isinstance(obj, (SingleNote, DamageNote)):
                if obj.timeScaleGroup > max_tsg_index:
                    issues.append(
                        f"Invalid timeScaleGroup {obj.timeScaleGroup} at beat {obj.beat} "
                        f"(max index: {max_tsg_index})"
                    )
            elif isinstance(obj, Slide):
                for conn in obj.connections:
                    if conn.timeScaleGroup > max_tsg_index:
                        issues.append(
                            f"Invalid timeScaleGroup {conn.timeScaleGroup} in slide at beat {conn.beat} "
                            f"(max index: {max_tsg_index})"
                        )
        
        # Validate slide structure
        for i, obj in enumerate(self.usc_file.usc.objects):
            if isinstance(obj, Slide):
                if not obj.connections:
                    issues.append(f"Slide at index {i} has no connections")
                    continue
                
                if obj.connections[0].type != "start":
                    issues.append(
                        f"Slide at index {i} does not start with 'start' type "
                        f"(found: {obj.connections[0].type})"
                    )
                
                if obj.connections[-1].type != "end":
                    issues.append(
                        f"Slide at index {i} does not end with 'end' type "
                        f"(found: {obj.connections[-1].type})"
                    )
        
        return issues
    
    def summary(self) -> str:
        """
        Generate a summary report of the chart.
        
        Returns:
            Formatted summary string
        """
        note_stats = self.analyze_notes()
        chart_info = self.analyze_chart()
        
        lines = [
            "=== USC Chart Summary ===",
            "",
            f"Version: {chart_info.version}",
            f"Offset: {chart_info.offset}",
            "",
            "=== BPM Information ===",
            f"Initial BPM: {chart_info.initial_bpm if chart_info.initial_bpm else 'N/A'}",
            f"BPM Changes: {chart_info.bpm_changes}",
            f"BPM Range: {chart_info.min_bpm} - {chart_info.max_bpm}" if chart_info.min_bpm else "BPM Range: N/A",
            "",
            "=== Chart Range ===",
            f"Beat Range: {chart_info.min_beat} - {chart_info.max_beat}" if chart_info.min_beat else "Beat Range: N/A",
            f"Tick Range: {chart_info.min_tick} - {chart_info.max_tick}" if chart_info.min_tick else "Tick Range: N/A",
            f"Duration: {chart_info.duration_beats:.2f} beats ({chart_info.duration_ticks} ticks)" if chart_info.duration_beats else "Duration: N/A",
            "",
            "=== Note Statistics ===",
            f"Total Notes: {note_stats.total_notes}",
            f"  Single Notes: {note_stats.total_single}",
            f"    Normal Tap: {note_stats.normal_tap}",
            f"    Critical Tap: {note_stats.critical_tap}",
            f"    Normal Trace: {note_stats.normal_trace}",
            f"    Critical Trace: {note_stats.critical_trace}",
            f"  Flicks: {note_stats.total_flick}",
            f"    Normal Flick: {note_stats.normal_flick}",
            f"    Critical Flick: {note_stats.critical_flick}",
            f"    Trace Flick: {note_stats.trace_flick}",
            f"    Critical Trace Flick: {note_stats.critical_trace_flick}",
            f"    By Direction:",
            f"      Left: {note_stats.left_flick}",
            f"      Up: {note_stats.up_flick}",
            f"      Right: {note_stats.right_flick}",
            f"      None: {note_stats.none_direction_flick}",
            f"  Damage Notes: {note_stats.damage_notes}",
            f"  Slides: {note_stats.slides}",
            f"    Normal: {note_stats.slide_normal}",
            f"    Trace: {note_stats.slide_trace}",
            f"    None: {note_stats.slide_none}",
            f"    Total Connections: {note_stats.slide_connections}",
            f"Guides: {note_stats.guides}",
            "",
            "=== Time Scale Groups ===",
            f"Total Groups: {chart_info.time_scale_groups}",
        ]
        
        return "\n".join(lines)


def analyze_file(file_path: str | Path) -> USCAnalyzer:
    """
    Convenience function to analyze a USC file.
    
    Args:
        file_path: Path to the USC file
        
    Returns:
        USCAnalyzer instance
    """
    return USCAnalyzer.from_file(file_path)
