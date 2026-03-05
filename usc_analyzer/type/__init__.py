"""USC type definitions."""

from .usc import (
    # Type definitions
    Direction,
    Ease,
    JudgeType,
    ConnectionType,
    GuideColor,
    GuideFade,
    # Models
    BaseUSCObject,
    SingleNote,
    DamageNote,
    SlideConnection,
    Slide,
    GuideMidpoint,
    Guide,
    TimeScaleChange,
    TimeScaleGroup,
    BPM,
    USCObject,
    USCData,
    USCFile,
    # Utility functions
    beat_to_tick,
    tick_to_beat,
    compare_beats,
    compare_beats_tick,
)

__all__ = [
    # Type definitions
    "Direction",
    "Ease",
    "JudgeType",
    "ConnectionType",
    "GuideColor",
    "GuideFade",
    # Models
    "BaseUSCObject",
    "SingleNote",
    "DamageNote",
    "SlideConnection",
    "Slide",
    "GuideMidpoint",
    "Guide",
    "TimeScaleChange",
    "TimeScaleGroup",
    "BPM",
    "USCObject",
    "USCData",
    "USCFile",
    # Utility functions
    "beat_to_tick",
    "tick_to_beat",
    "compare_beats",
    "compare_beats_tick",
]
