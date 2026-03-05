# USC Analyzer

A Python library for analyzing USC (Universal Sekai Chart) files.

## Features

- **Parse USC files** - Load and validate USC chart files with Pydantic models
- **Analyze charts** - Get detailed statistics about notes, BPM, and chart metadata
- **Validate structure** - Check for common issues in USC files
- **CLI tool** - Command-line interface for quick analysis
- **Type-safe** - Full type hints and Pydantic validation

## Installation

```bash
pip install usc-analyzer
```

## Quick Start

### Python API

```python
from usc_analyzer import USCAnalyzer

# Load and analyze a USC file
analyzer = USCAnalyzer.from_file("chart.usc")

# Get note statistics
stats = analyzer.analyze_notes()
print(f"Total notes: {stats.total_notes}")
print(f"Single notes: {stats.total_single}")
print(f"Slides: {stats.slides}")
print(f"Flicks: {stats.total_flick}")

# Get chart information
info = analyzer.analyze_chart()
print(f"BPM: {info.initial_bpm}")
print(f"Duration: {info.duration_beats} beats")

# Validate the file
issues = analyzer.validate()
if issues:
    for issue in issues:
        print(f"Warning: {issue}")

# Print full summary
print(analyzer.summary())
```

### CLI Tool

```bash
# Show summary of a chart
usc-analyze chart.usc

# Show detailed note statistics
usc-analyze chart.usc --notes

# Show chart information
usc-analyze chart.usc --chart

# Validate the file
usc-analyze chart.usc --validate

# Show BPM changes
usc-analyze chart.usc --bpm

# Output as JSON
usc-analyze chart.usc --json
```

## USC File Format

USC (Universal Sekai Chart) files are JSON-based chart files for rhythm games. They contain:

- **Notes**: Single notes (tap, flick, trace), damage notes
- **Slides**: Long notes with multiple connection points
- **Guides**: Visual guide lines
- **BPM**: Tempo changes
- **Time Scale Groups**: Note speed control

For detailed format specification, see [USC.md](https://gist.github.com/Piliman22/83e3886ba34979425df841002754ff3b).

## API Reference

### USCAnalyzer

Main analyzer class for USC files.

```python
# Load from file
analyzer = USCAnalyzer.from_file("chart.usc")

# Load from dict
analyzer = USCAnalyzer.from_dict(data)

# Load from JSON string
analyzer = USCAnalyzer.from_json(json_str)
```

#### Methods

- `analyze_notes() -> NoteStatistics` - Get detailed note statistics
- `analyze_chart() -> ChartInfo` - Get chart metadata
- `get_bpm_changes() -> list[BPM]` - Get all BPM changes
- `get_time_scale_groups() -> list[TimeScaleGroup]` - Get time scale groups
- `validate() -> list[str]` - Validate file structure
- `summary() -> str` - Generate a summary report

### Data Classes

#### NoteStatistics

Contains detailed note counts:

- `total_notes` - Total playable notes
- `total_single` - Single notes (tap, flick, trace)
- `normal_tap`, `critical_tap` - Tap notes
- `normal_trace`, `critical_trace` - Trace notes
- `total_flick` - Flick notes
- `damage_notes` - Damage notes
- `slides` - Slide/long notes
- `guides` - Guide notes

#### ChartInfo

Contains chart metadata:

- `version` - USC file version
- `offset` - Time offset
- `initial_bpm` - Starting BPM
- `bpm_changes` - Number of BPM changes
- `min_bpm`, `max_bpm` - BPM range
- `time_scale_groups` - Number of time scale groups
- `min_beat`, `max_beat` - Chart beat range
- `duration_beats`, `duration_ticks` - Chart duration

### Utility Functions

```python
from usc_analyzer import beat_to_tick, tick_to_beat, compare_beats_tick

# Convert between beats and ticks
tick = beat_to_tick(1.5)  # 1.5 beats -> 720 ticks
beat = tick_to_beat(720)  # 720 ticks -> 1.5 beats

# Compare beats using tick conversion (recommended)
if compare_beats_tick(beat1, beat2):
    print("Beats are equal")
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/usc-analyzer.git
cd usc-analyzer

# Install dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
# Format with black
black .

# Lint with ruff
ruff check .

# Type check with mypy
mypy usc_analyzer
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Links

- [GitHub Repository](https://github.com/Untitled-Sekai/usc-analyzer)
- [PyPI Package](https://pypi.org/project/usc-analyzer/)
- [Issue Tracker](https://github.com/Untitled-Sekai/usc-analyzer/issues)
