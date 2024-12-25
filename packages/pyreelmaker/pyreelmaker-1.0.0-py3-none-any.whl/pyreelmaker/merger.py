from moviepy.editor import concatenate_videoclips, VideoFileClip

def merge_segments(segment_paths, output_path):
    """
    Combines multiple video segments into one reel.

    :param segment_paths: List of video segment file paths.
    :param output_path: Path to save the combined reel.
    """
    try:
        clips = [VideoFileClip(path) for path in segment_paths]
        final_clip = concatenate_videoclips(clips, method="compose")
        final_clip.write_videofile(output_path, codec="libx264")
    except Exception as e:
        raise RuntimeError(f"Error merging segments: {e}")
