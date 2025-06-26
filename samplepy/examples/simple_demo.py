"""
Simple demo for SamplePy TUI
Shows how to use the basic file browser
"""

from samplepy.cli.tui_minimal import run_minimal_tui

if __name__ == "__main__":
    print("Starting SamplePy TUI...")
    print("Use arrow keys to navigate")
    print("Press Enter to open folders")
    print("Press Backspace to go back")
    print("Press 'r' to refresh")
    print("Press 'q' to quit")
    print()
    run_minimal_tui() 