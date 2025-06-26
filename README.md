# SamplePy

A simple, clean file browser TUI built with Textual.

## Features

- **File Browser**: Navigate through directories with a clean interface
- **File Information**: View file sizes and types
- **Simple Navigation**: Use arrow keys to navigate, Enter to open folders
- **Clean Interface**: Minimal, focused design without bloat

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

3. Run the TUI:
```bash
python -m samplepy
```

## Usage

### Basic Navigation

- **Arrow Keys**: Navigate through files and folders
- **Enter**: Open selected folder or select file
- **Backspace**: Go back to previous directory
- **R**: Refresh the current directory
- **Q**: Quit the application

### Example

```bash
# Start the TUI
python -m samplepy

# Or run the demo
python samplepy/examples/simple_demo.py
```

## Architecture

SamplePy is built with a clean, minimal architecture:

```
samplepy/
├── core/           # Core file utilities
│   └── file_utils.py   # Basic file operations
├── cli/            # TUI interface
│   └── tui_minimal.py  # Simple file browser TUI
├── examples/       # Example usage
│   └── simple_demo.py  # Basic demo
└── main.py         # Main entry point
```

## Development

### Project Structure

- **Core Module**: Simple file utilities without complex dependencies
- **CLI Module**: Clean TUI interface using Textual
- **Examples**: Simple demos showing basic usage

### Adding Features

1. Keep it simple - focus on core file operations
2. Maintain clean separation between UI and logic
3. Avoid complex audio processing or database operations

## License

This project is licensed under the MIT License - see the LICENSE file for details.
