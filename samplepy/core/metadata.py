"""
Core metadata management functionality
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
from mutagen import File

class MetadataManager:
    """Core metadata operations"""
    
    @staticmethod
    def get_metadata(audio_file: Path) -> Dict[str, Any]:
        """
        Get metadata from an audio file
        
        Args:
            audio_file: Path to audio file
        
        Returns:
            Dictionary containing metadata
        """
        metadata = {}
        
        try:
            # Use mutagen to read metadata
            audio = File(str(audio_file))
            
            if audio is None:
                return metadata
            
            # Get basic metadata
            if hasattr(audio, 'tags') and audio.tags:
                tags = audio.tags
                
                # Common tag fields
                tag_mappings = {
                    'title': ['title', 'TIT2', 'TITLE'],
                    'artist': ['artist', 'TPE1', 'ARTIST'],
                    'album': ['album', 'TALB', 'ALBUM'],
                    'year': ['year', 'TYER', 'YEAR'],
                    'genre': ['genre', 'TCON', 'GENRE'],
                    'track': ['track', 'TRCK', 'TRACK'],
                    'comment': ['comment', 'COMM', 'COMMENT']
                }
                
                for key, possible_tags in tag_mappings.items():
                    for tag in possible_tags:
                        if tag in tags:
                            value = tags[tag]
                            if isinstance(value, list) and len(value) > 0:
                                metadata[key] = str(value[0])
                            elif value:
                                metadata[key] = str(value)
                            break
            
            # Get technical information
            if hasattr(audio, 'info'):
                info = audio.info
                
                if hasattr(info, 'length'):
                    duration_seconds = info.length
                    minutes = int(duration_seconds // 60)
                    seconds = int(duration_seconds % 60)
                    metadata['duration'] = f"{minutes:02d}:{seconds:02d}"
                
                if hasattr(info, 'bitrate'):
                    metadata['bitrate'] = f"{info.bitrate // 1000} kbps"
                
                if hasattr(info, 'sample_rate'):
                    metadata['sample_rate'] = f"{info.sample_rate} Hz"
                
                if hasattr(info, 'channels'):
                    metadata['channels'] = info.channels
        
        except Exception as e:
            metadata['error'] = str(e)
        
        return metadata
    
    @staticmethod
    def set_metadata(audio_file: Path, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Set metadata for an audio file
        
        Args:
            audio_file: Path to audio file
            metadata: Dictionary containing metadata to set
        
        Returns:
            Dictionary with operation result
        """
        try:
            # Use mutagen to write metadata
            audio = File(str(audio_file))
            
            if audio is None:
                return {"success": False, "error": "Could not read audio file"}
            
            if hasattr(audio, 'tags') and audio.tags:
                tags = audio.tags
                
                # Set metadata based on file type
                for key, value in metadata.items():
                    if key == 'title' and 'TIT2' in tags:
                        tags['TIT2'] = str(value)
                    elif key == 'artist' and 'TPE1' in tags:
                        tags['TPE1'] = str(value)
                    elif key == 'album' and 'TALB' in tags:
                        tags['TALB'] = str(value)
                    elif key == 'year' and 'TYER' in tags:
                        tags['TYER'] = str(value)
                    elif key == 'genre' and 'TCON' in tags:
                        tags['TCON'] = str(value)
                    elif key == 'track' and 'TRCK' in tags:
                        tags['TRCK'] = str(value)
                    elif key == 'comment' and 'COMM' in tags:
                        tags['COMM'] = str(value)
                
                audio.save()
                return {"success": True, "file": str(audio_file), "metadata": metadata}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
        
        return {"success": False, "error": "No tags found in audio file"}
    
    @staticmethod
    def get_batch_metadata(audio_files: List[Path]) -> Dict[str, Any]:
        """
        Get metadata for multiple audio files
        
        Args:
            audio_files: List of audio file paths
        
        Returns:
            Dictionary with batch metadata results
        """
        results = []
        successful = 0
        failed = 0
        
        for audio_file in audio_files:
            metadata = MetadataManager.get_metadata(audio_file)
            
            if 'error' not in metadata:
                successful += 1
            else:
                failed += 1
            
            results.append({
                "file": str(audio_file),
                "metadata": metadata
            })
        
        return {
            "total_files": len(audio_files),
            "successful": successful,
            "failed": failed,
            "results": results
        }
    
    @staticmethod
    def set_batch_metadata(audio_files: List[Path], metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Set metadata for multiple audio files
        
        Args:
            audio_files: List of audio file paths
            metadata: Dictionary containing metadata to set
        
        Returns:
            Dictionary with batch operation results
        """
        results = []
        successful = 0
        failed = 0
        
        for audio_file in audio_files:
            result = MetadataManager.set_metadata(audio_file, metadata)
            results.append(result)
            
            if result["success"]:
                successful += 1
            else:
                failed += 1
        
        return {
            "total_files": len(audio_files),
            "successful": successful,
            "failed": failed,
            "results": results
        } 