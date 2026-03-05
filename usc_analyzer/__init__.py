"""USC Analyzer - Analyze USC (Universal Sekai Chart) files."""

from .main import (
    USCAnalyzer,
    NoteStatistics,
    ChartInfo,
    analyze_file,
)

from .type import (
    # Models
    USCFile,
    USCData,
    USCObject,
    SingleNote,
    DamageNote,
    Slide,
    SlideConnection,
    Guide,
    GuideMidpoint,
    TimeScaleGroup,
    TimeScaleChange,
    BPM,
    # Utility functions
    beat_to_tick,
    tick_to_beat,
    compare_beats,
    compare_beats_tick,
)

__version__ = "0.1.0"

__all__ = [
    # Main analyzer
    "USCAnalyzer",
    "NoteStatistics",
    "ChartInfo",
    "analyze_file",
    # Models
    "USCFile",
    "USCData",
    "USCObject",
    "SingleNote",
    "DamageNote",
    "Slide",
    "SlideConnection",
    "Guide",
    "GuideMidpoint",
    "TimeScaleGroup",
    "TimeScaleChange",
    "BPM",
    # Utility functions
    "beat_to_tick",
    "tick_to_beat",
    "compare_beats",
    "compare_beats_tick",
]
