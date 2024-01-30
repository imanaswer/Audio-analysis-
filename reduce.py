from moviepy.editor import VideoFileClip

def reduce_video_size(input_path, output_path, target_bitrate):
    # Load the video clip
    video_clip = VideoFileClip(input_path)

    # Write the modified video to the output file with the specified bitrate
    video_clip.write_videofile(output_path, bitrate=target_bitrate)

    # Close the video clip
    video_clip.close()

# Example usage:
input_video_path = "F:\work\Fro\classvid.mp4"
output_video_path = "F:\work\Fro\output_video.mp4"

# Set the target bitrate (in kilobits per second) to achieve the desired file size
target_bitrate = "200k"  # Adjust this value based on experimentation

reduce_video_size(input_video_path, output_video_path, target_bitrate)
