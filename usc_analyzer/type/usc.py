"""USC (Universal Sekai Chart files) type definitions using Pydantic."""

from typing import Annotated, Literal, Optional, Union
from pydantic import BaseModel, Field


# ========== Enums and Literals ==========

Direction = Literal["left", "up", "right", "none"]
Ease = Literal["in", "out", "linear"]
JudgeType = Literal["normal", "trace", "none"]
ConnectionType = Literal["start", "tick", "attach", "end"]
GuideColor = Literal["neutral", "red", "green", "blue", "yellow", "purple", "cyan", "black"]
GuideFade = Literal["in", "out", "none"]


# ========== Base Models ==========

class BaseUSCObject(BaseModel):
    """Base USC object with beat and timeScaleGroup."""
    beat: float
    timeScaleGroup: int


# ========== Single Note Models ==========

class SingleNote(BaseUSCObject):
    """
    Single note (tap, flick, trace, etc.)
    
    Type variants:
    - Normal tap: critical=False, trace=False, no direction
    - Critical tap: critical=True, trace=False, no direction
    - Normal trace: critical=False, trace=True, no direction
    - Critical trace: critical=True, trace=True, no direction
    - Flick: direction field present (left/up/right/none)
    """
    type: Literal["single"]
    lane: float
    size: float
    critical: bool = False
    trace: bool = False
    direction: Optional[Direction] = None


class DamageNote(BaseUSCObject):
    """Damage note."""
    type: Literal["damage"]
    lane: float
    size: float


# ========== Slide (Long Note) Models ==========

class SlideConnection(BaseModel):
    """A connection point in a slide (long note)."""
    beat: float
    timeScaleGroup: int
    lane: float
    size: float
    type: ConnectionType
    ease: Optional[Ease] = None
    critical: Optional[bool] = None
    judgeType: Optional[JudgeType] = None
    direction: Optional[Direction] = None  # For flick ending


class Slide(BaseModel):
    """
    Slide (long note) consisting of multiple connections.
    
    Structure:
    - First connection must be type "start"
    - Middle connections can be "tick" or "attach"
    - Last connection must be type "end"
    
    judgeType variants:
    - "normal": Normal tap judgment
    - "trace": Trace judgment (slide finger)
    - "none": No judgment (visual guide only)
    """
    type: Literal["slide"]
    critical: bool
    connections: list[SlideConnection]


# ========== Guide Note Models ==========

class GuideMidpoint(BaseModel):
    """A midpoint in a guide note."""
    beat: float
    timeScaleGroup: int
    lane: float
    size: float
    ease: Ease


class Guide(BaseModel):
    """
    Guide note (visual guide line).
    
    - First midpoint is the start point
    - Last midpoint is the end point
    """
    type: Literal["guide"]
    color: GuideColor
    fade: GuideFade
    midpoints: list[GuideMidpoint]


# ========== TimeScaleGroup Models ==========

class TimeScaleChange(BaseModel):
    """A time scale change within a TimeScaleGroup."""
    beat: float
    timeScale: float


class TimeScaleGroup(BaseModel):
    """
    Time scale group controlling note speed.
    
    Referenced by other objects through their timeScaleGroup index.
    Index is determined by order of appearance (0-indexed).
    """
    type: Literal["timeScaleGroup"]
    changes: list[TimeScaleChange]


# ========== BPM Model ==========

class BPM(BaseModel):
    """BPM change event."""
    type: Literal["bpm"]
    beat: float
    bpm: float


# ========== Union Types ==========

USCObject = Union[
    BPM,
    TimeScaleGroup,
    SingleNote,
    DamageNote,
    Slide,
    Guide,
]


# ========== Root Models ==========

class USCData(BaseModel):
    """USC data container."""
    objects: list[Annotated[USCObject, Field(discriminator="type")]]
    offset: float = Field(default=-0.0)


class USCFile(BaseModel):
    """Root USC file structure."""
    version: int = Field(default=2)
    usc: USCData


# ========== Utility Functions ==========

def beat_to_tick(beat: float) -> int:
    """
    Convert beat to tick.
    
    Args:
        beat: Beat value (floating point)
        
    Returns:
        Tick value (integer)
        
    Note:
        1 beat = 480 ticks
        1 measure (4 beats) = 1920 ticks
    """
    return round(beat * 480)


def tick_to_beat(tick: int) -> float:
    """
    Convert tick to beat.
    
    Args:
        tick: Tick value (integer)
        
    Returns:
        Beat value (floating point)
    """
    return tick / 480


def compare_beats(beat_a: float, beat_b: float, tolerance: float = 1e-6) -> bool:
    """
    Compare two beat values with tolerance.
    
    Args:
        beat_a: First beat value
        beat_b: Second beat value
        tolerance: Comparison tolerance (default: 1e-6)
        
    Returns:
        True if beats are equal within tolerance
        
    Note:
        Recommended to use tick-based comparison for exact matching:
        round(beat_a * 480) == round(beat_b * 480)
    """
    return abs(beat_a - beat_b) < tolerance


def compare_beats_tick(beat_a: float, beat_b: float) -> bool:
    """
    Compare two beat values using tick conversion.
    
    Args:
        beat_a: First beat value
        beat_b: Second beat value
        
    Returns:
        True if beats are equal when converted to ticks
    """
    return beat_to_tick(beat_a) == beat_to_tick(beat_b)
