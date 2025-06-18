"""
SamplePy - Audio Processing CLI Tool
Main entry point for the application
"""

import typer
from pathlib import Path
from .cli.aesthetic import cli

# Import CLI commands
from .cli.commands import convert, metadata, organize, analyze

# Create main app
app = typer.Typer(
    name="spy",
    help="SamplePy - Audio Processing CLI Tool",
    add_completion=False,
    rich_markup_mode="rich"
)

# Add commands to main app
app.command()(convert)
app.command()(metadata)
app.command()(organize)
app.command()(analyze)

@app.callback()
def main(
    version: bool = typer.Option(False, "--version", "-v", help="Show version and exit")
):
    """
    SamplePy - A powerful CLI tool for bulk audio operations
    
    Features:
    • Convert audio files between formats (MP3, WAV, FLAC, OGG, M4A, AAC)
    • View and edit metadata (title, artist, album, etc.)
    • Organize files by artist, album, genre, or year
    • Analyze audio files for technical information
    
    Examples:
    • spy convert -f mp3 -q 320
    • spy metadata show
    • spy metadata set -f artist -v "New Artist"
    • spy organize artist
    • spy analyze
    """
    if version:
        cli.print_header("SamplePy", "Audio Processing CLI Tool")
        cli.print_info("Version: 1.0.0")
        cli.print_info("Author: SamplePy Team")
        raise typer.Exit()

if __name__ == "__main__":
    app() 