"""
Enhanced video writer with compression control and parameter overlay.
Includes tunable compression settings for output file size management.
"""
import cv2
import numpy as np
import subprocess
import os
import tempfile

class CompressionSettings:
    """Configurable compression settings for output videos."""
    
    # Compression quality levels (0-100, higher = better quality, larger file)
    HIGH_QUALITY = 95     # Minimal compression, best quality
    MEDIUM_QUALITY = 75   # Balanced compression and quality  
    LOW_QUALITY = 50      # High compression, smaller files
    VERY_LOW_QUALITY = 25 # Maximum compression, lowest quality
    
    def __init__(self, quality=MEDIUM_QUALITY, use_h264=True, crf=23):
        """
        Initialize compression settings.
        
        Args:
            quality (int): Compression quality 0-100
            use_h264 (bool): Use H.264 codec for better compression
            crf (int): Constant Rate Factor for H.264 (0-51, lower = better quality)
        """
        self.quality = max(0, min(100, quality))  # Clamp to 0-100
        self.use_h264 = use_h264
        self.crf = max(0, min(51, crf))  # Clamp to valid CRF range

def add_info_overlay(frame, info_text, text_config=None):
    """
    Adds info text as an overlay at the bottom of the frame.
    
    Args:
        frame: Input video frame
        info_text: Text to overlay
        text_config: Optional dictionary with text styling options
    """
    if not info_text.strip():  # Skip if empty text
        return frame
        
    # Default text configuration
    default_config = {
        'font_scale': 0.5,
        'thickness': 1,
        'color': (255, 255, 255),  # White text
        'bg_alpha': 0.5,  # Background transparency
        'position': 'bottom',  # 'bottom', 'top', 'center'
        'margin': 10,
        'multiline': False
    }
    
    if text_config:
        default_config.update(text_config)
    
    config = default_config
    overlay = frame.copy()
    height, width = overlay.shape[:2]
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # Handle multiline text
    if config['multiline'] and '|' in info_text:
        lines = [line.strip() for line in info_text.split('|')]
    else:
        lines = [info_text]
    
    # Calculate text dimensions
    line_height = int(25 * config['font_scale'])
    total_text_height = len(lines) * line_height + config['margin']
    
    # Position calculation
    if config['position'] == 'bottom':
        start_y = height - total_text_height
        bg_y_start = height - total_text_height - config['margin']
        bg_y_end = height
    elif config['position'] == 'top':
        start_y = config['margin'] + line_height
        bg_y_start = 0
        bg_y_end = total_text_height + config['margin']
    else:  # center
        start_y = height // 2 - (total_text_height // 2)
        bg_y_start = start_y - config['margin']
        bg_y_end = start_y + total_text_height
    
    # Draw semi-transparent background
    cv2.rectangle(overlay, (0, bg_y_start), (width, bg_y_end), (0, 0, 0), -1)
    cv2.addWeighted(overlay, config['bg_alpha'], frame, 1 - config['bg_alpha'], 0, frame)
    
    # Draw text lines
    for i, line in enumerate(lines):
        y_pos = start_y + (i * line_height)
        cv2.putText(frame, line, (config['margin'], y_pos), font, 
                   config['font_scale'], config['color'], config['thickness'], cv2.LINE_AA)
    
    return frame

def compress_video_ffmpeg(input_path, output_path, compression_settings):
    """
    Compress video using FFmpeg for better compression than OpenCV.
    
    Args:
        input_path: Path to input video
        output_path: Path to output compressed video
        compression_settings: CompressionSettings object
    """
    try:
        if compression_settings.use_h264:
            # H.264 encoding with CRF (better quality control)
            cmd = [
                'ffmpeg', '-i', input_path,
                '-c:v', 'libx264',
                '-crf', str(compression_settings.crf),
                '-preset', 'medium',  # Balance speed vs compression
                '-c:a', 'aac',  # Audio codec
                '-y',  # Overwrite output file
                output_path
            ]
        else:
            # Basic quality-based compression
            cmd = [
                'ffmpeg', '-i', input_path,
                '-q:v', str(int((100 - compression_settings.quality) * 31 / 100)),
                '-y',
                output_path
            ]
        
        # Run FFmpeg
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            return True, "Compression successful"
        else:
            return False, f"FFmpeg error: {result.stderr}"
            
    except subprocess.TimeoutExpired:
        return False, "FFmpeg compression timed out"
    except FileNotFoundError:
        return False, "FFmpeg not found. Please install FFmpeg for compression."
    except Exception as e:
        return False, f"Compression error: {str(e)}"

def write_frames(writer, luma_out, ref_frames, color_mode, info_text, 
                text_config=None, compression_settings=None, temp_output_path=None):
    """
    Converts processed image data back to video frames, overlays info text,
    and writes them with optional compression.
    
    Args:
        writer: OpenCV VideoWriter object
        luma_out: Processed luma data
        ref_frames: Reference frames for color reconstruction
        color_mode: "gray" or "color"
        info_text: Text to overlay on frames
        text_config: Optional text styling configuration
        compression_settings: Optional CompressionSettings object
        temp_output_path: Path for temporary uncompressed output
    """
    for i, lum in enumerate(luma_out):
        if color_mode == "gray":
            frame_out = (lum * 255).clip(0, 255).astype('uint8')
            frame_out = cv2.cvtColor(frame_out, cv2.COLOR_GRAY2BGR)
        else:
            ycrcb = cv2.cvtColor(ref_frames[i], cv2.COLOR_BGR2YCrCb)
            ycrcb[:, :, 0] = (lum * 255).clip(0, 255).astype('uint8')
            frame_out = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
        
        # Add overlay if text provided
        if info_text:
            frame_out = add_info_overlay(frame_out, info_text, text_config)
        
        writer.write(frame_out)

def create_compressed_output(temp_path, final_path, compression_settings):
    """
    Create compressed output from temporary uncompressed video.
    
    Args:
        temp_path: Path to temporary uncompressed video
        final_path: Path to final compressed video
        compression_settings: CompressionSettings object
        
    Returns:
        tuple: (success, message, compression_ratio)
    """
    if not compression_settings:
        # No compression requested, just move the file
        if temp_path != final_path:
            os.rename(temp_path, final_path)
        return True, "No compression applied", 1.0
    
    # Get original file size
    original_size = os.path.getsize(temp_path)
    
    # Compress using FFmpeg
    success, message = compress_video_ffmpeg(temp_path, final_path, compression_settings)
    
    if success and os.path.exists(final_path):
        compressed_size = os.path.getsize(final_path)
        compression_ratio = original_size / compressed_size if compressed_size > 0 else 1.0
        
        # Clean up temporary file
        try:
            os.remove(temp_path)
        except:
            pass  # Ignore cleanup errors
            
        return True, f"Compressed successfully. Ratio: {compression_ratio:.1f}x", compression_ratio
    else:
        # Compression failed, keep original
        if temp_path != final_path:
            os.rename(temp_path, final_path)
        return False, f"Compression failed: {message}", 1.0

# Preset compression configurations for easy use
COMPRESSION_PRESETS = {
    'none': None,  # No compression
    'light': CompressionSettings(quality=85, crf=18),      # Light compression, high quality
    'medium': CompressionSettings(quality=75, crf=23),     # Balanced (default)
    'heavy': CompressionSettings(quality=60, crf=28),      # Heavy compression
    'maximum': CompressionSettings(quality=40, crf=35),    # Maximum compression
}