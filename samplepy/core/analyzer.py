"""
Core audio analysis functionality
"""

from pathlib import Path
from typing import Dict, Any, List
from pydub import AudioSegment
from mutagen import File

class AudioAnalyzer:
    """Core audio analysis operations"""
    
    @staticmethod
    def analyze_file(audio_file: Path) -> Dict[str, Any]:
        """
        Analyze an audio file and return technical information
        
        Args:
            audio_file: Path to audio file
        
        Returns:
            Dictionary containing analysis results
        """
        analysis = {}
        
        try:
            # Get file size
            analysis['size'] = f"{audio_file.stat().st_size / (1024*1024):.2f} MB"
            
            # Get format
            analysis['format'] = audio_file.suffix[1:].upper()
            
            # Use pydub for audio analysis
            audio = AudioSegment.from_file(str(audio_file))
            
            # Duration
            duration_ms = len(audio)
            minutes = int(duration_ms // 60000)
            seconds = int((duration_ms % 60000) // 1000)
            analysis['duration'] = f"{minutes:02d}:{seconds:02d}"
            
            # Sample rate
            analysis['sample_rate'] = f"{audio.frame_rate} Hz"
            
            # Channels
            analysis['channels'] = audio.channels
            
            # Try to get bitrate from mutagen
            try:
                audio_info = File(str(audio_file))
                if audio_info and hasattr(audio_info, 'info') and hasattr(audio_info.info, 'bitrate'):
                    analysis['bitrate'] = f"{audio_info.info.bitrate // 1000} kbps"
            except:
                analysis['bitrate'] = "Unknown"
        
        except Exception as e:
            analysis['error'] = str(e)
        
        return analysis
    
    @staticmethod
    def analyze_batch(audio_files: List[Path]) -> Dict[str, Any]:
        """
        Analyze multiple audio files
        
        Args:
            audio_files: List of audio file paths
        
        Returns:
            Dictionary with batch analysis results
        """
        results = []
        successful = 0
        failed = 0
        
        for audio_file in audio_files:
            analysis = AudioAnalyzer.analyze_file(audio_file)
            
            if 'error' not in analysis:
                successful += 1
            else:
                failed += 1
            
            results.append({
                "file": str(audio_file),
                "analysis": analysis
            })
        
        return {
            "total_files": len(audio_files),
            "successful": successful,
            "failed": failed,
            "results": results
        }
    
    @staticmethod
    def get_directory_summary(directory: Path) -> Dict[str, Any]:
        """
        Get summary information about audio files in a directory
        
        Args:
            directory: Directory to analyze
        
        Returns:
            Dictionary with directory summary
        """
        from .converter import AudioConverter
        
        audio_files = AudioConverter.get_audio_files(directory)
        
        if not audio_files:
            return {
                "total_files": 0,
                "total_size": "0 MB",
                "formats": {},
                "message": "No audio files found"
            }
        
        # Count by format
        format_counts = {}
        total_size = 0
        
        for audio_file in audio_files:
            format_ext = audio_file.suffix[1:].lower()
            format_counts[format_ext] = format_counts.get(format_ext, 0) + 1
            total_size += audio_file.stat().st_size
        
        return {
            "total_files": len(audio_files),
            "total_size": f"{total_size / (1024*1024):.2f} MB",
            "formats": format_counts,
            "directory": str(directory)
        } 