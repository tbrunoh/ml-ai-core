
import subprocess
import json
import os
import uuid

from acrcloud.recognizer import ACRCloudRecognizer
from dotenv import load_dotenv

load_dotenv()


class AudioUtils:
    def __init__(self):
        pass
    def extract_audio_from_video(video_path, audio_output_dir, audio_format="mp3"):
        """
        Extracts audio from a video file for music recognition.
        :param video_path: Path to the video file
        :param audio_output_path: Path to save extracted audio
        :param audio_format: Format of extracted audio (default: mp3)
        :return: Dictionary with success status or error message
        """
        try:
            if not os.path.exists(video_path):
                return {"error": "Video file does not exist."}

            audio_output_path = f"{audio_output_dir}/{uuid.uuid4()}"
            audio_output_path = f"{os.path.splitext(audio_output_path)[0]}.{audio_format}"
            cmd = ["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_output_path]

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return {"success": True, "audio_file": audio_output_path}

        except FileNotFoundError:
            return {"error": "FFmpeg not found. Make sure it is installed and accessible."}
        except subprocess.CalledProcessError as e:
            return {"error": f"Failed to extract audio. FFmpeg error: {e.stderr}"}

    def identify_music_acrcloud(audio_path):
        """
        Uses ACRCloud to identify music from an audio file.
        :param audio_path: Path to the extracted audio file
        :param config: Dictionary containing ACRCloud API credentials
        """
        print(f"access key: {os.getenv('ACRCLOUD_KEY')}")
        
        config = {
            'host': os.getenv('ACRCLOUD_HOST'),
            'access_key': os.getenv('ACRCLOUD_KEY'),
            'access_secret':os.getenv('ACRCLOUD_SECRET'),
            'timeout':10
        }
        recognizer = ACRCloudRecognizer(config)
        
        try:
            result = recognizer.recognize_by_file(audio_path, 0)
            return result
        except Exception as e:
            return {"error": str(e)}