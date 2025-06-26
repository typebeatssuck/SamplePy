"""
Basic file utilities for SamplePy
Simple file operations without complex audio processing
"""

from pathlib import Path
from typing import List, Dict, Any
import os

class FileUtils:
    """Basic file utilities"""
    
    @staticmethod
    def get_files_in_directory(directory: Path) -> List[Path]:
        """Get all files in a directory"""
        try:
            return [f for f in directory.iterdir() if f.is_file()]
        except Exception:
            return []
    
    @staticmethod
    def get_directories_in_directory(directory: Path) -> List[Path]:
        """Get all directories in a directory"""
        try:
            return [d for d in directory.iterdir() if d.is_dir()]
        except Exception:
            return []
    
    @staticmethod
    def get_file_info(file_path: Path) -> Dict[str, Any]:
        """Get basic file information"""
        try:
            stat = file_path.stat()
            return {
                'name': file_path.name,
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'is_file': file_path.is_file(),
                'is_dir': file_path.is_dir(),
                'extension': file_path.suffix
            }
        except Exception:
            return {
                'name': file_path.name,
                'size': 0,
                'modified': 0,
                'is_file': False,
                'is_dir': False,
                'extension': ''
            }
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

    @staticmethod
    def create_file(path: Path) -> bool:
        """Create a new empty file at the given path. Returns True on success."""
        try:
            path.touch(exist_ok=False)
            return True
        except Exception:
            return False

    @staticmethod
    def create_folder(path: Path) -> bool:
        """Create a new folder at the given path. Returns True on success."""
        try:
            path.mkdir(parents=False, exist_ok=False)
            return True
        except Exception:
            return False

    @staticmethod
    def delete_path(path: Path) -> bool:
        """Delete a file or folder at the given path. Returns True on success."""
        try:
            if path.is_dir():
                os.rmdir(path)
            else:
                path.unlink()
            return True
        except Exception:
            return False

    @staticmethod
    def rename_path(path: Path, new_path: Path) -> bool:
        """Rename a file or folder to new_path. Returns True on success."""
        try:
            path.rename(new_path)
            return True
        except Exception:
            return False 