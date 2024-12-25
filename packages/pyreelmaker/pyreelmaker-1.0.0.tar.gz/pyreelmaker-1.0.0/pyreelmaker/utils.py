from moviepy.video.fx.all import resize

def adjust_resolution(video_path, output_path, width=1080, height=1920):
    """
    Adjusts the resolution of a video to the given dimensions.

    :param video_path: Path to the input video.
    :param output_path: Path to save the resized video.
    :param width: Desired width.
    :param height: Desired height.
    """
    clip = VideoFileClip(video_path)
    resized_clip = resize(clip, height=height, width=width)
    resized_clip.write_videofile(output_path, codec="libx264")
