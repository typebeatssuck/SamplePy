# SamplePy Text User Interface (TUI)

SamplePy now includes a powerful Text User Interface (TUI) built with the Textual framework, providing an interactive way to manage your audio files.

## Features

### Basic TUI (`spy tui`)
- **File List**: View all audio files in the current directory
- **Progress Tracking**: Real-time progress bars for operations
- **Metadata Editor**: View and edit file metadata
- **Organization Tools**: Organize files by artist, album, genre, or year
- **Keyboard Shortcuts**: Quick access to common functions

### Advanced TUI (`spy tui-advanced`)
All features from Basic TUI plus:
- **File Selection**: Select individual files for batch operations
- **Directory Tree**: Navigate through your file system
- **Tabbed Interface**: Organized tabs for different functions
- **Logging**: Real-time operation logs
- **Enhanced Analysis**: Detailed audio analysis results
- **Organization Preview**: See how files will be organized before making changes

## Installation

Make sure you have the required dependencies:

```bash
pip install -r requirements.txt
```

The TUI requires the `textual` package, which is included in the requirements.

## Usage

### Launching the TUI

```bash
# Basic TUI
spy tui

# Advanced TUI (recommended)
spy tui-advanced
```

### Basic TUI Controls

| Key | Action |
|-----|--------|
| `q` | Quit the application |
| `r` | Refresh file list |
| `c` | Convert files |
| `m` | Focus metadata editor |
| `o` | Focus organization widget |
| `a` | Analyze files |

### Advanced TUI Controls

| Key | Action |
|-----|--------|
| `q` | Quit the application |
| `r` | Refresh file list |
| `c` | Convert files |
| `m` | Focus metadata editor |
| `o` | Focus organization widget |
| `a` | Analyze files |
| `s` | Select all files |
| `d` | Deselect all files |

### Mouse Support

The TUI supports mouse interactions:
- Click on files to select/deselect them
- Click buttons to activate functions
- Use scroll wheel to navigate lists
- Click and drag to select multiple items

## Interface Layout

### Basic TUI
```
┌─────────────────────────────────────────────────────────────┐
│ SamplePy TUI                                    [Clock]     │
├─────────────┬───────────────────────────────────────────────┤
│ SamplePy    │ File List (scrollable)                        │
│ TUI         │                                               │
│             │ [File1.mp3] [Size] [Format] [Duration] ...   │
│ [Refresh]   │ [File2.wav] [Size] [Format] [Duration] ...   │
│ [Convert]   │ [File3.flac][Size] [Format] [Duration] ...   │
│ [Analyze]   │                                               │
│ [Change Dir]│                                               │
│             │ Progress Widget                               │
│             │ [Status Message]                              │
│             │ [████████████████████████████████████████]   │
│             │                                               │
│             │ Metadata Widget                               │
│             │ [Field] [Value] [Set]                         │
│             │                                               │
│             │ Organization Widget                           │
│             │ [Type] [Preview] [Organize]                   │
└─────────────┴───────────────────────────────────────────────┘
```

### Advanced TUI
```
┌─────────────────────────────────────────────────────────────┐
│ SamplePy Advanced TUI                           [Clock]     │
├─────────────┬───────────────────────────────────────────────┤
│ SamplePy    │ File Table (with selection)                   │
│ Advanced    │ [✓] [File1.mp3] [Size] [Format] [Duration]   │
│ TUI         │ [ ] [File2.wav] [Size] [Format] [Duration]   │
│             │ [✓] [File3.flac][Size] [Format] [Duration]   │
│ [Refresh]   │                                               │
│ [Convert]   │ Status Bar                                    │
│ [Analyze]   │ [Status Message] [████████████████████████]   │
│ [Change Dir]│                                               │
│ [Select All]│ Tabbed Interface                              │
│ [Deselect]  │ ┌─────────┬─────────┬─────────┐               │
│             │ │Metadata │Organize │Analysis │               │
│ Directory   │ ├─────────┴─────────┴─────────┤               │
│ Tree        │ │                             │               │
│ [📁 Music]  │ │ Tab Content                 │               │
│ [📁 Videos] │ │                             │               │
│             │ │                             │               │
│ Log         │ └─────────────────────────────┘               │
│ [INFO] ...  │                                               │
│ [ERROR] ... │                                               │
└─────────────┴───────────────────────────────────────────────┘
```

## Features in Detail

### File Management
- **Automatic Detection**: Automatically detects audio files in the current directory
- **File Information**: Shows file size, format, duration, and metadata
- **Selection**: Select individual files for batch operations
- **Refresh**: Reload the file list to see changes

### Audio Conversion
- **Batch Conversion**: Convert multiple files at once
- **Progress Tracking**: Real-time progress bars
- **Format Support**: MP3, WAV, FLAC, OGG, M4A, AAC
- **Quality Control**: Adjustable bitrate settings

### Metadata Editing
- **View Metadata**: See all metadata for selected files
- **Edit Fields**: Change title, artist, album, genre, etc.
- **Batch Editing**: Apply changes to multiple files at once
- **Validation**: Ensures metadata is properly formatted

### File Organization
- **Preview Mode**: See how files will be organized before making changes
- **Multiple Criteria**: Organize by artist, album, genre, or year
- **Safe Operations**: Files are moved to new folders based on metadata
- **Progress Tracking**: See organization progress in real-time

### Audio Analysis
- **Technical Information**: Bitrate, sample rate, channels, duration
- **Format Detection**: Automatic format identification
- **Directory Summary**: Overview of all audio files in directory
- **Detailed Reports**: Comprehensive analysis results

## Tips and Tricks

1. **Use the Advanced TUI**: The advanced version provides more features and better organization
2. **File Selection**: Select specific files before running operations to avoid processing unwanted files
3. **Preview Organization**: Always preview organization before applying changes
4. **Check Logs**: The log panel shows detailed information about operations
5. **Keyboard Shortcuts**: Learn the keyboard shortcuts for faster navigation

## Troubleshooting

### Common Issues

1. **No files showing**: Make sure you're in a directory with audio files
2. **Conversion errors**: Check that the target format is supported
3. **Permission errors**: Ensure you have write permissions in the directory
4. **Display issues**: Try resizing your terminal window

### Getting Help

- Use `spy --help` for command-line options
- Check the log panel in the advanced TUI for error details
- Ensure all dependencies are installed correctly

## Future Enhancements

Planned features for future versions:
- Directory picker dialog
- Conversion settings dialog
- Drag and drop support
- Custom themes and colors
- Plugin system for additional formats
- Batch rename functionality
- Audio preview capabilities 