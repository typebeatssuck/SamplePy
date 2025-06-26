"""
SamplePy - Simple File Browser TUI
Main entry point for the application
"""

from .cli.tui_minimal import run_minimal_tui

def main():
    """Main entry point that launches the TUI"""
    run_minimal_tui()

if __name__ == "__main__":
    main() 