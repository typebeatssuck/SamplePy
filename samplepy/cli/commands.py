"""
CLI commands for SamplePy using core functionality
"""

import typer
from pathlib import Path
from typing import Optional, List
from rich.prompt import Prompt, Confirm

from ..core.converter import AudioConverter
from ..core.metadata import MetadataManager
from ..core.organizer import FileOrganizer
from ..core.analyzer import AudioAnalyzer
from .aesthetic import cli

def convert(
    format: str = typer.Option(..., "-f", "--format", help="Output format (mp3, wav, flac, ogg, m4a, aac)"),
    quality: int = typer.Option(192, "-q", "--quality", help="Audio quality in kbps (for lossy formats)"),
    delete_original: bool = typer.Option(False, "-d", "--delete", help="Delete original files after conversion"),
    directory: Optional[Path] = typer.Option(Path.cwd(), "-p", "--path", help="Directory containing audio files")
):
    """Convert audio files to different formats"""
    cli.print_header("Audio Conversion", f"Converting to {format.upper()} format")
    
    # Get audio files
    audio_files = AudioConverter.get_audio_files(directory)
    
    if not audio_files:
        cli.print_warning(f"No audio files found in {directory}")
        return
    
    cli.print_info(f"Found {len(audio_files)} audio files")
    
    # Confirm conversion
    if not Confirm.ask(f"Convert {len(audio_files)} files to {format.upper()}?"):
        return
    
    # Convert files
    with cli.create_progress(f"Converting to {format.upper()}") as progress:
        task = progress.add_task("Converting...", total=len(audio_files))
        
        for audio_file in audio_files:
            progress.update(task, description=f"Converting {audio_file.name}")
            
            result = AudioConverter.convert_file(audio_file, format, quality, delete_original)
            
            if result["success"]:
                cli.print_success(f"Converted: {audio_file.name}")
            else:
                cli.print_error(f"Failed to convert {audio_file.name}: {result['error']}")
            
            progress.advance(task)
    
    cli.print_success("Conversion completed!")

def metadata(
    action: str = typer.Argument(..., help="Action: show or set"),
    field: Optional[str] = typer.Option(None, "-f", "--field", help="Metadata field to set (title, artist, album, etc.)"),
    value: Optional[str] = typer.Option(None, "-v", "--value", help="Value to set for the field"),
    directory: Optional[Path] = typer.Option(Path.cwd(), "-p", "--path", help="Directory containing audio files")
):
    """Show or set metadata for audio files"""
    
    if action == "show":
        cli.print_header("Metadata Display", "Showing metadata for audio files")
        
        # Get audio files
        audio_files = AudioConverter.get_audio_files(directory)
        
        if not audio_files:
            cli.print_warning(f"No audio files found in {directory}")
            return
        
        # Get metadata for all files
        batch_result = MetadataManager.get_batch_metadata(audio_files)
        
        # Display metadata
        for result in batch_result["results"]:
            file_path = Path(result["file"])
            metadata = result["metadata"]
            
            if "error" in metadata:
                cli.print_error(f"Error reading {file_path.name}: {metadata['error']}")
            else:
                cli.print_file_info(file_path, metadata)
        
        cli.print_info(f"Processed {batch_result['successful']} files successfully")
    
    elif action == "set":
        if not field or not value:
            cli.print_error("Both field and value are required for setting metadata")
            return
        
        cli.print_header("Metadata Update", f"Setting {field} to '{value}'")
        
        # Get audio files
        audio_files = AudioConverter.get_audio_files(directory)
        
        if not audio_files:
            cli.print_warning(f"No audio files found in {directory}")
            return
        
        # Set metadata
        metadata_to_set = {field: value}
        batch_result = MetadataManager.set_batch_metadata(audio_files, metadata_to_set)
        
        # Display results
        for result in batch_result["results"]:
            if result["success"]:
                cli.print_success(f"Updated: {Path(result['file']).name}")
            else:
                cli.print_error(f"Failed to update {Path(result['file']).name}: {result['error']}")
        
        cli.print_info(f"Updated {batch_result['successful']} files successfully")
    
    else:
        cli.print_error(f"Unknown action: {action}. Use 'show' or 'set'")

def organize(
    by: str = typer.Argument(..., help="Organization type: artist, album, genre, or year"),
    directory: Optional[Path] = typer.Option(Path.cwd(), "-p", "--path", help="Directory containing audio files")
):
    """Organize audio files into folders by metadata"""
    cli.print_header("File Organization", f"Organizing by {by}")
    
    # Get audio files
    audio_files = AudioConverter.get_audio_files(directory)
    
    if not audio_files:
        cli.print_warning(f"No audio files found in {directory}")
        return
    
    # Get organization preview
    preview = FileOrganizer.get_organization_preview(audio_files, by)
    
    cli.print_info(f"Found {preview['total_files']} files to organize into {preview['folder_count']} folders")
    
    # Show preview
    for folder_name, files in preview["folders"].items():
        cli.print_section(f"Folder: {folder_name}", f"{len(files)} files")
        for file_path in files[:5]:  # Show first 5 files
            cli.console.print(f"  • {Path(file_path).name}")
        if len(files) > 5:
            cli.console.print(f"  ... and {len(files) - 5} more")
    
    # Confirm organization
    if not Confirm.ask("Proceed with organization?"):
        return
    
    # Organize files
    with cli.create_progress("Organizing files") as progress:
        task = progress.add_task("Organizing...", total=len(audio_files))
        
        for audio_file in audio_files:
            progress.update(task, description=f"Organizing {audio_file.name}")
            
            result = FileOrganizer.organize_file(audio_file, by)
            
            if result["success"]:
                cli.print_success(f"Organized: {audio_file.name}")
            else:
                cli.print_error(f"Failed to organize {audio_file.name}: {result['error']}")
            
            progress.advance(task)
    
    cli.print_success("Organization completed!")

def analyze(
    directory: Optional[Path] = typer.Option(Path.cwd(), "-p", "--path", help="Directory to analyze")
):
    """Analyze audio files and show technical information"""
    cli.print_header("Audio Analysis", "Analyzing audio files")
    
    # Get directory summary
    summary = AudioAnalyzer.get_directory_summary(directory)
    
    if summary["total_files"] == 0:
        cli.print_warning("No audio files found")
        return
    
    # Display summary
    cli.print_section("Directory Summary", 
        f"Total files: {summary['total_files']}\n"
        f"Total size: {summary['total_size']}\n"
        f"Formats: {', '.join([f'{k.upper()}: {v}' for k, v in summary['formats'].items()])}"
    )
    
    # Get audio files for detailed analysis
    audio_files = AudioConverter.get_audio_files(directory)
    
    # Analyze files
    batch_result = AudioAnalyzer.analyze_batch(audio_files)
    
    # Display results
    for result in batch_result["results"]:
        file_path = Path(result["file"])
        analysis = result["analysis"]
        
        if "error" in analysis:
            cli.print_error(f"Error analyzing {file_path.name}: {analysis['error']}")
        else:
            cli.print_file_info(file_path, analysis)
    
    cli.print_info(f"Analyzed {batch_result['successful']} files successfully") 