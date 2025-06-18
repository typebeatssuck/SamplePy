"""
Core file organization functionality
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
from .metadata import MetadataManager

class FileOrganizer:
    """Core file organization operations"""
    
    @staticmethod
    def organize_file(
        audio_file: Path, 
        organization_type: str, 
        create_subfolders: bool = False
    ) -> Dict[str, Any]:
        """
        Organize a single audio file into folders
        
        Args:
            audio_file: Path to audio file
            organization_type: Type of organization ('artist', 'album', 'genre', 'year')
            create_subfolders: Whether to create subfolders
        
        Returns:
            Dictionary with organization result
        """
        try:
            # Get metadata
            metadata = MetadataManager.get_metadata(audio_file)
            
            # Determine folder name based on organization type
            folder_name = "Unknown"
            
            if organization_type == "artist":
                folder_name = metadata.get("artist", "Unknown Artist")
            elif organization_type == "album":
                folder_name = metadata.get("album", "Unknown Album")
            elif organization_type == "genre":
                folder_name = metadata.get("genre", "Unknown Genre")
            elif organization_type == "year":
                folder_name = metadata.get("year", "Unknown Year")
            
            # Clean folder name
            folder_name = "".join(c for c in folder_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            if not folder_name:
                folder_name = "Unknown"
            
            # Create folder
            target_folder = audio_file.parent / folder_name
            target_folder.mkdir(exist_ok=True)
            
            # Move file
            target_file = target_folder / audio_file.name
            audio_file.rename(target_file)
            
            return {
                "success": True,
                "original_path": str(audio_file),
                "new_path": str(target_file),
                "folder": str(target_folder),
                "organization_type": organization_type
            }
        
        except Exception as e:
            return {
                "success": False,
                "file": str(audio_file),
                "error": str(e)
            }
    
    @staticmethod
    def organize_batch(
        audio_files: List[Path],
        organization_type: str,
        create_subfolders: bool = False
    ) -> Dict[str, Any]:
        """
        Organize multiple audio files
        
        Args:
            audio_files: List of audio file paths
            organization_type: Type of organization
            create_subfolders: Whether to create subfolders
        
        Returns:
            Dictionary with batch organization results
        """
        results = []
        successful = 0
        failed = 0
        
        for audio_file in audio_files:
            result = FileOrganizer.organize_file(audio_file, organization_type, create_subfolders)
            results.append(result)
            
            if result["success"]:
                successful += 1
            else:
                failed += 1
        
        return {
            "total_files": len(audio_files),
            "successful": successful,
            "failed": failed,
            "organization_type": organization_type,
            "results": results
        }
    
    @staticmethod
    def get_organization_preview(
        audio_files: List[Path],
        organization_type: str
    ) -> Dict[str, Any]:
        """
        Get a preview of how files would be organized
        
        Args:
            audio_files: List of audio file paths
            organization_type: Type of organization
        
        Returns:
            Dictionary with organization preview
        """
        preview = {}
        
        for audio_file in audio_files:
            metadata = MetadataManager.get_metadata(audio_file)
            
            # Determine folder name
            folder_name = "Unknown"
            
            if organization_type == "artist":
                folder_name = metadata.get("artist", "Unknown Artist")
            elif organization_type == "album":
                folder_name = metadata.get("album", "Unknown Album")
            elif organization_type == "genre":
                folder_name = metadata.get("genre", "Unknown Genre")
            elif organization_type == "year":
                folder_name = metadata.get("year", "Unknown Year")
            
            # Clean folder name
            folder_name = "".join(c for c in folder_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            if not folder_name:
                folder_name = "Unknown"
            
            if folder_name not in preview:
                preview[folder_name] = []
            
            preview[folder_name].append(str(audio_file))
        
        return {
            "organization_type": organization_type,
            "total_files": len(audio_files),
            "folders": preview,
            "folder_count": len(preview)
        } 