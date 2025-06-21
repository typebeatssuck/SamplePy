"""
Minimal Text User Interface (TUI) for SamplePy using Textual framework
Pure ASCII styling with terminal-like appearance
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Header, Footer, Static, DataTable, 
    Input, Select, ProgressBar, Label
)
from textual.widgets.data_table import RowKey
from textual.reactive import reactive
from textual import work
from textual.binding import Binding
from pathlib import Path
from typing import Dict, Any, List, Optional
import asyncio

from ..core.converter import AudioConverter
from ..core.metadata import MetadataManager
from ..core.organizer import FileOrganizer
from ..core.analyzer import AudioAnalyzer


class AudioFileTable(DataTable):
    """Simple table for displaying audio files"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_columns("Name", "Size", "Format", "Duration", "Artist", "Album")
        self.files = []
        self.selected_files = set()
    
    def update_files(self, files: List[Path]):
        """Update the file list"""
        self.files = files
        self.clear()
        self.selected_files.clear()
        
        for file_path in files:
            try:
                metadata = MetadataManager.get_metadata(file_path)
                size = file_path.stat().st_size
                size_str = f"{size / (1024*1024):.1f} MB"
                
                self.add_row(
                    file_path.name,
                    size_str,
                    file_path.suffix.upper().lstrip('.'),
                    metadata.get('duration', 'Unknown'),
                    metadata.get('artist', 'Unknown'),
                    metadata.get('album', 'Unknown')
                )
            except Exception:
                self.add_row(
                    file_path.name,
                    "Unknown",
                    file_path.suffix.upper().lstrip('.'),
                    "Unknown",
                    "Unknown",
                    "Unknown"
                )
    
    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle row selection"""
        row_key = event.row_key
        if row_key in self.selected_files:
            self.selected_files.remove(row_key)
        else:
            self.selected_files.add(row_key)


class StatusBar(Container):
    """Simple status bar"""
    
    def compose(self) -> ComposeResult:
        yield Label("Ready", id="status-label")
        yield ProgressBar(id="status-progress")


class ActionMenu(Container):
    """Action menu that appears when 'A' is pressed"""
    
    def compose(self) -> ComposeResult:
        yield Label("Actions:", id="action-title")
        yield Static("", id="action-list")


class SamplePyMinimalTUI(App):
    """Minimal TUI application for SamplePy"""
    
    CSS = """
    App {
        background: black;
        color: white;
    }
    
    #main-container {
        height: 100%;
        width: 100%;
    }
    
    #file-table {
        height: 70%;
        border: solid white;
    }
    
    #status-bar {
        height: 10%;
        border-top: solid white;
    }
    
    #action-menu {
        height: 20%;
        border-top: solid white;
        display: none;
    }
    
    DataTable {
        border: solid white;
    }
    
    Label {
        color: white;
    }
    
    Static {
        color: white;
    }
    
    ProgressBar {
        border: solid white;
    }
    
    ProgressBar > .progress-bar {
        background: white;
    }
    
    ProgressBar > .progress-bar--bar {
        background: green;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
        Binding("a", "show_actions", "Actions"),
        Binding("1", "action_1", "Action 1"),
        Binding("2", "action_2", "Action 2"),
        Binding("3", "action_3", "Action 3"),
        Binding("4", "action_4", "Action 4"),
        Binding("5", "action_5", "Action 5"),
        Binding("escape", "hide_actions", "Hide Actions"),
    ]
    
    def __init__(self):
        super().__init__()
        self.current_directory = Path.cwd()
        self.audio_files = []
        self.actions_visible = False
        self.load_audio_files()
    
    def load_audio_files(self):
        """Load audio files from current directory"""
        self.audio_files = AudioConverter.get_audio_files(self.current_directory)
    
    def compose(self) -> ComposeResult:
        """Compose the TUI layout"""
        yield Header(show_clock=True)
        
        with Container(id="main-container"):
            yield AudioFileTable(id="file-table")
            yield StatusBar(id="status-bar")
            yield ActionMenu(id="action-menu")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Called when the app is mounted"""
        self.update_file_list()
        self.update_status("Ready")
        self.update_action_menu()
    
    def update_file_list(self):
        """Update the file list widget"""
        file_table = self.query_one("#file-table", AudioFileTable)
        file_table.update_files(self.audio_files)
        self.update_status(f"Loaded {len(self.audio_files)} audio files")
    
    def update_status(self, message: str, progress: float = 0.0):
        """Update status bar"""
        status_label = self.query_one("#status-label", Label)
        status_progress = self.query_one("#status-progress", ProgressBar)
        
        status_label.update(message)
        status_progress.progress = progress
    
    def update_action_menu(self):
        """Update the action menu"""
        action_menu = self.query_one("#action-menu", ActionMenu)
        action_list = action_menu.query_one("#action-list", Static)
        
        actions = [
            "1. Convert files",
            "2. Show metadata",
            "3. Organize files",
            "4. Analyze files",
            "5. Change directory"
        ]
        
        action_text = "\n".join(actions)
        action_list.update(action_text)
    
    def get_selected_files(self) -> List[Path]:
        """Get list of selected files"""
        file_table = self.query_one("#file-table", AudioFileTable)
        selected_files = []
        
        for row_key in file_table.selected_files:
            if row_key < len(self.audio_files):
                selected_files.append(self.audio_files[row_key])
        
        return selected_files
    
    def toggle_actions(self):
        """Toggle action menu visibility"""
        action_menu = self.query_one("#action-menu", ActionMenu)
        self.actions_visible = not self.actions_visible
        
        if self.actions_visible:
            action_menu.display = True
            self.update_status("Actions menu active - Press number or ESC to hide")
        else:
            action_menu.display = False
            self.update_status("Ready")
    
    @work
    async def convert_files(self, format: str = "mp3", quality: int = 192):
        """Convert audio files"""
        files = self.get_selected_files()
        if not files:
            files = self.audio_files
        
        if not files:
            self.update_status("No files to convert")
            return
        
        self.update_status(f"Converting {len(files)} files to {format.upper()}")
        
        for i, audio_file in enumerate(files):
            progress = (i / len(files)) * 100
            self.update_status(f"Converting {audio_file.name}", progress)
            
            try:
                result = AudioConverter.convert_file(audio_file, format, quality)
                if not result["success"]:
                    self.update_status(f"Failed to convert {audio_file.name}: {result['error']}")
            except Exception as e:
                self.update_status(f"Error converting {audio_file.name}: {str(e)}")
            
            await asyncio.sleep(0.1)
        
        self.update_status("Conversion completed!", 100)
        self.load_audio_files()
        self.update_file_list()
    
    @work
    async def show_metadata(self):
        """Show metadata for selected files"""
        files = self.get_selected_files()
        if not files:
            files = self.audio_files
        
        if not files:
            self.update_status("No files to analyze")
            return
        
        self.update_status("Reading metadata...")
        
        try:
            batch_result = MetadataManager.get_batch_metadata(files)
            self.update_status(f"Metadata read: {batch_result['successful']} successful, {batch_result['failed']} failed")
        except Exception as e:
            self.update_status(f"Error reading metadata: {str(e)}")
    
    @work
    async def organize_files(self, by: str = "artist"):
        """Organize files"""
        if not self.audio_files:
            self.update_status("No files to organize")
            return
        
        self.update_status(f"Organizing files by {by}...")
        
        try:
            result = FileOrganizer.organize_batch(self.audio_files, by)
            self.update_status(f"Organization completed: {result['successful']} successful, {result['failed']} failed")
            self.load_audio_files()
            self.update_file_list()
        except Exception as e:
            self.update_status(f"Error during organization: {str(e)}")
    
    @work
    async def analyze_files(self):
        """Analyze audio files"""
        files = self.get_selected_files()
        if not files:
            files = self.audio_files
        
        if not files:
            self.update_status("No files to analyze")
            return
        
        self.update_status("Analyzing audio files...")
        
        try:
            summary = AudioAnalyzer.get_directory_summary(self.current_directory)
            batch_result = AudioAnalyzer.analyze_batch(files)
            self.update_status(f"Analysis completed: {batch_result['successful']} successful, {batch_result['failed']} failed")
        except Exception as e:
            self.update_status(f"Error during analysis: {str(e)}")
    
    def action_quit(self) -> None:
        """Quit the application"""
        self.exit()
    
    def action_refresh(self) -> None:
        """Refresh the file list"""
        self.load_audio_files()
        self.update_file_list()
    
    def action_show_actions(self) -> None:
        """Show action menu"""
        self.toggle_actions()
    
    def action_hide_actions(self) -> None:
        """Hide action menu"""
        if self.actions_visible:
            self.toggle_actions()
    
    def action_1(self) -> None:
        """Action 1: Convert files"""
        if self.actions_visible:
            self.convert_files()
            self.toggle_actions()
    
    def action_2(self) -> None:
        """Action 2: Show metadata"""
        if self.actions_visible:
            self.show_metadata()
            self.toggle_actions()
    
    def action_3(self) -> None:
        """Action 3: Organize files"""
        if self.actions_visible:
            self.organize_files()
            self.toggle_actions()
    
    def action_4(self) -> None:
        """Action 4: Analyze files"""
        if self.actions_visible:
            self.analyze_files()
            self.toggle_actions()
    
    def action_5(self) -> None:
        """Action 5: Change directory"""
        if self.actions_visible:
            self.update_status("Directory change not implemented yet")
            self.toggle_actions()


def run_minimal_tui():
    """Run the minimal TUI application"""
    app = SamplePyMinimalTUI()
    app.run()


if __name__ == "__main__":
    run_minimal_tui() 