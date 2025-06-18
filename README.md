# SamplePy

A powerful CLI tool for bulk audio operations with a clean, modular architecture.

## Features

- **Audio Conversion**: Convert between MP3, WAV, FLAC, OGG, M4A, and AAC formats
- **Metadata Management**: View and edit audio file metadata (title, artist, album, etc.)
- **File Organization**: Organize files by artist, album, genre, or year
- **Audio Analysis**: Get technical information about audio files
- **Rich CLI Interface**: Beautiful, colored output with progress bars and tables

## Architecture

SamplePy is built with a clean separation of concerns:

```
samplepy/
├── core/           # Core business logic (API-ready)
│   ├── converter.py    # Audio conversion operations
│   ├── metadata.py     # Metadata management
│   ├── organizer.py    # File organization
│   └── analyzer.py     # Audio analysis
├── cli/            # CLI interface layer
│   ├── aesthetic.py    # Rich interface styling
│   └── commands.py     # CLI command implementations
└── main.py         # Main entry point
```

The core functionality is completely separated from the CLI, making it easy to:
- Use as a library in other Python projects
- Build API endpoints later
- Test business logic independently
- Maintain clean code organization

## Installation

### From Source

1. Clone the repository:
```bash
git clone https://github.com/samplepy/samplepy.git
cd samplepy
```

2. Install in editable mode:
```bash
pip install -e .
```

3. Test the installation:
```bash
spy --help
```

## Usage

### Basic Commands

```bash
# Convert audio files to MP3 with 320kbps quality
spy convert -f mp3 -q 320

# Show metadata for all audio files
spy metadata show

# Set artist metadata for all files
spy metadata set -f artist -v "New Artist"

# Organize files by artist
spy organize artist

# Analyze audio files
spy analyze
```

### Command Options

#### Convert
- `-f, --format`: Output format (mp3, wav, flac, ogg, m4a, aac)
- `-q, --quality`: Audio quality in kbps (default: 192)
- `-d, --delete`: Delete original files after conversion
- `-p, --path`: Directory containing audio files (default: current directory)

#### Metadata
- `action`: Either "show" or "set"
- `-f, --field`: Metadata field to set (title, artist, album, etc.)
- `-v, --value`: Value to set for the field
- `-p, --path`: Directory containing audio files

#### Organize
- `by`: Organization type (artist, album, genre, year)
- `-p, --path`: Directory containing audio files

#### Analyze
- `-p, --path`: Directory to analyze (default: current directory)

## Using as a Library

The core functionality can be used directly in Python code:

```python
from samplepy.core.converter import AudioConverter
from samplepy.core.metadata import MetadataManager
from pathlib import Path

# Convert a file
result = AudioConverter.convert_file(
    Path("song.wav"), 
    "mp3", 
    quality=320
)

# Get metadata
metadata = MetadataManager.get_metadata(Path("song.mp3"))
print(f"Artist: {metadata.get('artist', 'Unknown')}")
```

## Development

### Project Structure

- **Core Module**: Pure business logic, no dependencies on CLI or external libraries beyond audio processing
- **CLI Module**: Rich interface layer that uses the core functionality
- **Main Entry Point**: Simple Typer app that ties everything together

### Adding New Features

1. **Core Logic**: Add new functionality to the appropriate module in `samplepy/core/`
2. **CLI Interface**: Add corresponding CLI commands in `samplepy/cli/commands.py`
3. **Styling**: Use the centralized `CLIManager` in `samplepy/cli/aesthetic.py`

### Testing

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Code formatting
black samplepy/

# Linting
flake8 samplepy/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Roadmap

- [ ] API layer for web services
- [ ] Batch processing with resume capability
- [ ] Audio effects and filters
- [ ] Playlist generation
- [ ] Integration with music databases
- [ ] GUI interface
