"""
Core audio conversion functionality
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
from pydub import AudioSegment

class AudioConverter:
    """Core audio conversion operations"""
    
    # Supported audio formats
    SUPPORTED_FORMATS = {
        'mp3': ['.mp3'],
        'wav': ['.wav'],
        'flac': ['.flac'],
        'm4a': ['.m4a'],
        'ogg': ['.ogg'],
        'aac': ['.aac']
    }
    
    @staticmethod
    def get_audio_files(directory: Path, format_filter: Optional[str] = None) -> List[Path]:
        """
        Get all audio files from a directory
        
        Args:
            directory: Directory to search
            format_filter: Optional format filter (e.g., 'mp3', 'wav')
        
        Returns:
            List of audio file paths
        """
        audio_files = []
        
        if not directory.exists():
            return audio_files
        
        # Get all supported extensions
        extensions = []
        if format_filter:
            if format_filter.lower() in AudioConverter.SUPPORTED_FORMATS:
                extensions = AudioConverter.SUPPORTED_FORMATS[format_filter.lower()]
            else:
                return audio_files
        else:
            # Get all supported extensions
            for format_exts in AudioConverter.SUPPORTED_FORMATS.values():
                extensions.extend(format_exts)
        
        # Find audio files
        for ext in extensions:
            audio_files.extend(directory.glob(f"*{ext}"))
            audio_files.extend(directory.glob(f"*{ext.upper()}"))
        
        return sorted(audio_files)
    
    @staticmethod
    def convert_file(
        audio_file: Path, 
        output_format: str, 
        quality: int = 192, 
        delete_original: bool = False
    ) -> Dict[str, Any]:
        """
        Convert an audio file to a different format
        
        Args:
            audio_file: Path to input audio file
            output_format: Output format (e.g., 'mp3', 'wav', 'flac')
            quality: Audio quality for lossy formats (kbps)
            delete_original: Whether to delete the original file
        
        Returns:
            Dictionary with conversion result
        """
        try:
            # Load audio file
            audio = AudioSegment.from_file(str(audio_file))
            
            # Create output filename
            output_file = audio_file.parent / f"{audio_file.stem}.{output_format}"
            
            # Export with appropriate parameters
            if output_format.lower() == 'mp3':
                audio.export(str(output_file), format='mp3', bitrate=f"{quality}k")
            elif output_format.lower() == 'wav':
                audio.export(str(output_file), format='wav')
            elif output_format.lower() == 'flac':
                audio.export(str(output_file), format='flac')
            elif output_format.lower() == 'ogg':
                audio.export(str(output_file), format='ogg', bitrate=f"{quality}k")
            else:
                audio.export(str(output_file), format=output_format)
            
            # Delete original if requested
            if delete_original and output_file.exists():
                audio_file.unlink()
            
            return {
                "success": True,
                "input_file": str(audio_file),
                "output_file": str(output_file),
                "format": output_format,
                "quality": quality
            }
        
        except Exception as e:
            return {
                "success": False,
                "input_file": str(audio_file),
                "error": str(e)
            }
    
    @staticmethod
    def convert_batch(
        input_files: List[Path],
        output_format: str,
        quality: int = 192,
        delete_original: bool = False
    ) -> Dict[str, Any]:
        """
        Convert multiple audio files
        
        Args:
            input_files: List of input audio files
            output_format: Output format
            quality: Audio quality
            delete_original: Whether to delete originals
        
        Returns:
            Dictionary with batch conversion results
        """
        results = []
        successful = 0
        failed = 0
        
        for audio_file in input_files:
            result = AudioConverter.convert_file(audio_file, output_format, quality, delete_original)
            results.append(result)
            
            if result["success"]:
                successful += 1
            else:
                failed += 1
        
        return {
            "total_files": len(input_files),
            "successful": successful,
            "failed": failed,
            "results": results
        } 