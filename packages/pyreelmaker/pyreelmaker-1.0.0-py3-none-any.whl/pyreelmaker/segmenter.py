from moviepy.video.io.VideoFileClip import VideoFileClip

def extract_segment(video_path, start_time, end_time, output_path):
    """
    Extracts a video segment from a larger video.

    :param video_path: Path to the input video.
    :param start_time: Start time (in seconds).
    :param end_time: End time (in seconds).
    :param output_path: Path to save the extracted segment.
    """
    try:
        clip = VideoFileClip(video_path).subclip(start_time, end_time)
        clip.write_videofile(output_path, codec="libx264")
    except Exception as e:
        raise RuntimeError(f"Error extracting segment: {e}")
