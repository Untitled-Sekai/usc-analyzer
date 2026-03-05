"""Example usage of USC Analyzer."""

from usc_analyzer import USCAnalyzer

# Load and analyze a USC file
analyzer = USCAnalyzer.from_file("examples/sample.usc")

# Print full summary
print(analyzer.summary())
print()

# Get detailed statistics
stats = analyzer.analyze_notes()
print(f"Total playable notes: {stats.total_notes}")
print(f"  Normal taps: {stats.normal_tap}")
print(f"  Critical taps: {stats.critical_tap}")
print(f"  Flicks: {stats.total_flick}")
print(f"  Slides: {stats.slides}")
print()

# Get chart information
info = analyzer.analyze_chart()
print(f"Chart duration: {info.duration_beats:.2f} beats ({info.duration_ticks} ticks)")
print(f"BPM: {info.initial_bpm}")
print()

# Validate the file
issues = analyzer.validate()
if issues:
    print("Validation issues found:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("✓ Chart is valid!")
