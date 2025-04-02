
import subprocess
import json
import os
import uuid


class VideoUtils:
    def __init__(self):
        pass
    def verify_video_format(file_path, allowed_formats=("mp4", "mov", "avi"), allowed_codecs=("h264", "aac")):
        """
        Verifies the format, codec, and integrity of an uploaded video.
        :param file_path: Path to the video file
        :param allowed_formats: Tuple of allowed video formats
        :param allowed_codecs: Tuple of allowed codecs (video & audio)
        :return: Dict with verification results
        """
        try:
            # Run ffprobe to get video metadata
            cmd = [
                "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=codec_name",
                "-show_format", "-of", "json", file_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            metadata = json.loads(result.stdout)
            
            # Extract format and codec info
            format_name = metadata.get("format", {}).get("format_name", "").lower()
            video_codec = metadata.get("streams", [{}])[0].get("codec_name", "").lower()
            
            print("format name found %s", format_name)
            print("video codec name found %s", video_codec)
            
            # Verify format and codec
            format_valid = bool(set(format_name) & set(allowed_formats)) #FIXME
            codec_valid = video_codec in allowed_codecs
            
            return {
                "format": format_name,
                "format_valid": format_valid,
                "video_codec": video_codec,
                "codec_valid": codec_valid,
                "status": "Valid" if format_valid and codec_valid else "Invalid"
            }
        except subprocess.CalledProcessError:
            return {"error": "Failed to process video file. Corrupted or unsupported format."}

    def generate_thumbnail(video_path, output_path, time_frame="00:00:05"):
        """
        Generates a thumbnail from the video at the specified time frame.
        :param video_path: Path to the video file
        :param output_path: Path to save the generated thumbnail
        :param time_frame: Time position to capture the thumbnail (default: 5 seconds)
        """
        try:
            cmd = [
                "ffmpeg", "-ss", time_frame, "-i", video_path, "-vframes", "1", "-q:v", "2", output_path
            ]
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            return {"success": True, "thumbnail": output_path}
        except subprocess.CalledProcessError:
            return {"error": "Failed to generate thumbnail."}

    def generate_video_preview(video_path, output_path, duration=5):
        """
        Generates a short preview (GIF or MP4) from the video.
        :param video_path: Path to the video file
        :param output_path: Path to save the preview clip
        :param duration: Duration of the preview clip in seconds (default: 5 seconds)
        """
        try:
            cmd = [
                "ffmpeg", "-i", video_path, "-t", str(duration), "-vf", "scale=320:-1", "-q:v", "5", output_path
            ]
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            return {"success": True, "preview": output_path}
        except subprocess.CalledProcessError:
            return {"error": "Failed to generate video preview."}

    def extract_video_metadata(video_path):
        """
        Extracts and validates metadata such as resolution, bitrate, and frame rate.
        :param video_path: Path to the video file
        :return: Dict with extracted metadata
        """
        try:
            cmd = [
                "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", 
                "stream=width,height,bit_rate,r_frame_rate", "-show_format", "-of", "json", video_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            metadata = json.loads(result.stdout)
            
            video_stream = metadata.get("streams", [{}])[0]
            width = video_stream.get("width")
            height = video_stream.get("height")
            bit_rate = video_stream.get("bit_rate")
            frame_rate = video_stream.get("r_frame_rate")
            duration = metadata.get("format", {}).get("duration")
            
            return {
                "resolution": f"{width}x{height}" if width and height else "Unknown",
                "bit_rate": bit_rate if bit_rate else "Unknown",
                "frame_rate": frame_rate if frame_rate else "Unknown",
                "duration": duration if duration else "Unknown"
            }
        except subprocess.CalledProcessError:
            return {"error": "Failed to extract video metadata."}

    def enforce_file_constraints(video_path, max_size_mb=int(100), max_duration_sec=600):
        """
        Enforces max file size and max duration limits.
        :param video_path: Path to the video file
        :param max_size_mb: Maximum allowed file size in MB (default: 100MB)
        :param max_duration_sec: Maximum allowed duration in seconds (default: 10 minutes)
        :return: Dict indicating whether constraints are met
        """
        file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
        metadata = extract_video_metadata(video_path)
        duration = float(metadata.get("duration", 0))
        
        print("file size ", file_size_mb)
        print("duration ", duration)
        
        size_valid = file_size_mb <= max_size_mb
        duration_valid = duration <= max_duration_sec
        
        return {
            "file_size": f"{file_size_mb:.2f}MB",
            "duration": f"{duration:.2f}s",
            "size_valid": size_valid,
            "duration_valid": duration_valid,
            "status": "Valid" if size_valid and duration_valid else "Invalid"
        }


    def scale_video(input_video_path, output_video_dir, width, height, format="mp4"):
        """
        Scale a video to the given dimensions using FFmpeg.

        Args:
            input_video_path (str): Path to the input video file.
            output_video_path (str): Path to save the scaled video.
            width (int): Target width of the scaled video.
            height (int): Target height of the scaled video.
        """
        
        output_video_path = f"{output_video_dir}/{uuid.uuid4()}.{format}"
        # FFmpeg command to scale the video
        ffmpeg_command = [
            'ffmpeg', 
            '-i', input_video_path,   # Input video file
            '-vf', f'scale={width}:{height}',  # Video filter to scale
            '-c:a', 'copy',  # Keep audio codec unchanged
            output_video_path  # Output video file
        ]
        
        # Run FFmpeg command
        subprocess.run(ffmpeg_command, check=True)
        print(f"Video scaled to {width}x{height} and saved at {output_video_path}")


    def add_watermark(input_video_path, output_video_path, watermark_image_path, position='top-right'):
        """
        Add a watermark to a video using FFmpeg.

        Args:
            input_video_path (str): Path to the input video file.
            output_video_path (str): Path to save the output video with watermark.
            watermark_image_path (str): Path to the watermark image (e.g., PNG).
            position (str): Position to place the watermark ('top-left', 'top-right', 'bottom-left', 'bottom-right').
        """
        # Define position for the watermark
        positions = {
            'top-left': '10:10',
            'top-right': 'main_w-10-overlay_w-10',
            'bottom-left': '10:main_h-overlay_h-10',
            'bottom-right': 'main_w-10-overlay_w-10:main_h-overlay_h-10'
        }

        # Get the position string based on input
        position_string = positions.get(position, 'top-right')  # Default is 'top-right'

        # FFmpeg command to add watermark
        ffmpeg_command = [
            'ffmpeg', 
            '-i', input_video_path,  # Input video
            '-i', watermark_image_path,  # Watermark image
            '-filter_complex', f'[1]scale=200:200[wm];[0][wm]overlay={position_string}',  # Overlay watermark
            '-c:a', 'copy',  # Keep audio codec unchanged
            output_video_path  # Output video file
        ]

        # Run FFmpeg command
        subprocess.run(ffmpeg_command, check=True)
        print(f"Watermarked video saved at {output_video_path}")
        