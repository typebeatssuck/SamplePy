"""
Centralized aesthetic control for SamplePy CLI interface
"""

from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.align import Align
from rich.layout import Layout
from rich.columns import Columns
from rich.rule import Rule
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.tree import Tree
from rich.live import Live
from rich.status import Status
from rich.console import Group
from rich import box
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
import json

class CLIManager:
    """
    Centralized CLI manager for SamplePy interface.
    All colors, themes, and visual elements are controlled from here.
    """
    
    def __init__(self):
        # Color palette - modify these to change the entire app's look
        self.colors = {
            # Primary colors
            'primary': 'bold blue',
            'secondary': 'cyan',
            'accent': 'bright_green',
            'warning': 'yellow',
            'error': 'red',
            'success': 'green',
            'info': 'bright_blue',
            
            # Text colors
            'text': 'white',
            'text_dim': 'dim white',
            'text_bright': 'bright_white',
            
            # Status colors
            'status_ok': 'green',
            'status_warning': 'yellow',
            'status_error': 'red',
            'status_info': 'blue',
            
            # File type colors
            'file_mp3': 'bright_green',
            'file_wav': 'bright_blue',
            'file_flac': 'bright_magenta',
            'file_ogg': 'bright_cyan',
            'file_m4a': 'bright_yellow',
            'file_aac': 'bright_red',
            
            # Metadata colors
            'metadata_title': 'bright_white',
            'metadata_artist': 'cyan',
            'metadata_album': 'blue',
            'metadata_year': 'yellow',
            'metadata_genre': 'magenta',
            'metadata_duration': 'green',
            'metadata_bitrate': 'bright_red',
            
            # Progress colors
            'progress_bar': 'blue',
            'progress_text': 'white',
            'progress_complete': 'green',
            
            # Panel colors
            'panel_title': 'bold blue',
            'panel_border': 'blue',
            'panel_content': 'white',
            
            # Table colors
            'table_header': 'bold blue',
            'table_row': 'white',
            'table_alt_row': 'dim white',
            'table_border': 'blue',
        }
        
        # Box styles for panels and tables
        self.boxes = {
            'default': box.ROUNDED,
            'simple': box.SIMPLE,
            'double': box.DOUBLE,
            'bold': box.HEAVY,
            'minimal': box.MINIMAL,
        }
        
        # Spinner styles
        self.spinners = {
            'dots': 'dots',
            'dots2': 'dots2',
            'dots3': 'dots3',
            'dots4': 'dots4',
            'dots5': 'dots5',
            'dots6': 'dots6',
            'dots7': 'dots7',
            'dots8': 'dots8',
            'dots9': 'dots9',
            'dots10': 'dots10',
            'dots11': 'dots11',
            'dots12': 'dots12',
            'line': 'line',
            'line2': 'line2',
            'pipe': 'pipe',
            'simpleDots': 'simpleDots',
            'simpleDotsScrolling': 'simpleDotsScrolling',
            'star': 'star',
            'star2': 'star2',
            'flip': 'flip',
            'hamburger': 'hamburger',
            'growVertical': 'growVertical',
            'growHorizontal': 'growHorizontal',
            'balloon': 'balloon',
            'balloon2': 'balloon2',
            'noise': 'noise',
            'bounce': 'bounce',
            'boxBounce': 'boxBounce',
            'boxBounce2': 'boxBounce2',
            'triangle': 'triangle',
            'arc': 'arc',
            'circle': 'circle',
            'square': 'square',
            'square2': 'square2',
            'diamond': 'diamond',
            'diamond2': 'diamond2',
            'zigzag': 'zigzag',
            'zigzag2': 'zigzag2',
            'zigzag3': 'zigzag3',
        }
        
        # Initialize console with custom theme
        self.console = Console(theme=self._create_theme())
    
    def _create_theme(self) -> Theme:
        """Create custom Rich theme with our color palette."""
        return Theme({
            "info": self.colors['info'],
            "warning": self.colors['warning'],
            "danger": self.colors['error'],
            "success": self.colors['success'],
            "primary": self.colors['primary'],
            "secondary": self.colors['secondary'],
            "accent": self.colors['accent'],
        })
    
    def get_color(self, color_name: str) -> str:
        """Get a color from the palette."""
        return self.colors.get(color_name, 'white')
    
    def set_color(self, color_name: str, color_value: str):
        """Set a color in the palette."""
        self.colors[color_name] = color_value
        # Recreate theme with new colors
        self.console = Console(theme=self._create_theme())
    
    def get_file_color(self, file_extension: str) -> str:
        """Get color for a specific file type."""
        extension = file_extension.lower().lstrip('.')
        return self.colors.get(f'file_{extension}', self.colors['text'])
    
    def print_header(self, title: str, subtitle: str = None):
        """Print a styled header."""
        header_text = f"[{self.colors['primary']}]{title}[/{self.colors['primary']}]"
        if subtitle:
            header_text += f"\n[{self.colors['text_dim']}]{subtitle}[/{self.colors['text_dim']}]"
        
        self.console.print(Panel(
            Align.center(header_text),
            title=f"[{self.colors['panel_title']}]SamplePy[/{self.colors['panel_title']}]",
            border_style=self.colors['panel_border'],
            box=self.boxes['default']
        ))
    
    def print_section(self, title: str, content: str):
        """Print a styled section."""
        self.console.print(Panel(
            content,
            title=f"[{self.colors['panel_title']}]{title}[/{self.colors['panel_title']}]",
            border_style=self.colors['panel_border'],
            box=self.boxes['default']
        ))
    
    def print_info(self, message: str):
        """Print an info message."""
        self.console.print(f"[{self.colors['info']}]ℹ[/{self.colors['info']}] {message}")
    
    def print_success(self, message: str):
        """Print a success message."""
        self.console.print(f"[{self.colors['success']}]✓[/{self.colors['success']}] {message}")
    
    def print_warning(self, message: str):
        """Print a warning message."""
        self.console.print(f"[{self.colors['warning']}]⚠[/{self.colors['warning']}] {message}")
    
    def print_error(self, message: str):
        """Print an error message."""
        self.console.print(f"[{self.colors['error']}]✗[/{self.colors['error']}] {message}")
    
    def create_table(self, title: str = None, show_header: bool = True) -> Table:
        """Create a styled table."""
        table = Table(
            title=title,
            show_header=show_header,
            header_style=self.colors['table_header'],
            border_style=self.colors['table_border'],
            box=self.boxes['default']
        )
        return table
    
    def create_progress(self, description: str = "Processing...") -> Progress:
        """Create a styled progress bar."""
        return Progress(
            SpinnerColumn(spinner_name=self.spinners['dots']),
            TextColumn(f"[{self.colors['progress_text']}]{description}"),
            BarColumn(bar_width=40, style=self.colors['progress_bar']),
            TaskProgressColumn(),
            console=self.console
        )
    
    def create_status(self, status: str) -> Status:
        """Create a styled status indicator."""
        return Status(
            status,
            spinner=self.spinners['dots'],
            spinner_style=self.colors['primary']
        )
    
    def print_file_info(self, file_path: Path, metadata: Dict[str, Any] = None):
        """Print styled file information."""
        file_ext = file_path.suffix
        file_color = self.get_file_color(file_ext)
        
        # File name with color
        file_text = f"[{file_color}]{file_path.name}[/{file_color}]"
        
        if metadata:
            # Add metadata if available
            meta_text = []
            for key, value in metadata.items():
                if key in self.colors:
                    color = self.colors[f'metadata_{key}']
                    meta_text.append(f"[{color}]{key.title()}: {value}[/{color}]")
                else:
                    meta_text.append(f"{key.title()}: {value}")
            
            file_text += f" - {' | '.join(meta_text)}"
        
        self.console.print(file_text)
    
    def print_summary(self, title: str, items: List[Dict[str, Any]]):
        """Print a styled summary."""
        table = self.create_table(title=title)
        
        if items:
            # Add columns based on first item
            for key in items[0].keys():
                table.add_column(key.title(), style=self.colors['table_header'])
            
            # Add rows
            for i, item in enumerate(items):
                row_style = self.colors['table_row'] if i % 2 == 0 else self.colors['table_alt_row']
                table.add_row(*[str(value) for value in item.values()], style=row_style)
        
        self.console.print(table)
    
    def print_rule(self, title: str = None):
        """Print a styled rule/separator."""
        self.console.print(Rule(title, style=self.colors['panel_border']))
    
    def print_columns(self, items: List[str], title: str = None):
        """Print items in columns."""
        if title:
            self.console.print(f"[{self.colors['primary']}]{title}[/{self.colors['primary']}]")
        
        columns = Columns(items, equal=True, expand=True)
        self.console.print(columns)
    
    def print_tree(self, title: str, items: List[str]):
        """Print a styled tree structure."""
        tree = Tree(f"[{self.colors['primary']}]{title}[/{self.colors['primary']}]")
        
        for item in items:
            tree.add(f"[{self.colors['text']}]{item}[/{self.colors['text']}]")
        
        self.console.print(tree)
    
    def print_markdown(self, content: str):
        """Print styled markdown content."""
        markdown = Markdown(content)
        self.console.print(markdown)
    
    def print_syntax(self, code: str, language: str = "python"):
        """Print syntax-highlighted code."""
        syntax = Syntax(code, language, theme="monokai")
        self.console.print(syntax)
    
    def save_theme(self, file_path: Path):
        """Save current theme to a JSON file."""
        theme_data = {
            'colors': self.colors,
            'boxes': {k: str(v) for k, v in self.boxes.items()},
            'spinners': self.spinners
        }
        
        with open(file_path, 'w') as f:
            json.dump(theme_data, f, indent=2)
    
    def load_theme(self, file_path: Path):
        """Load theme from a JSON file."""
        if file_path.exists():
            with open(file_path, 'r') as f:
                theme_data = json.load(f)
            
            self.colors.update(theme_data.get('colors', {}))
            self.console = Console(theme=self._create_theme())

# Global CLI manager instance
cli = CLIManager() 