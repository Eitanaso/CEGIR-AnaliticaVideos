# pip install moviepy

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


# Set the file paths
input_video = 'C:\\Users\\eitan\\Desktop\\cosas CEGIR\\maraton\\maraton6.mp4'
output_video = 'C:\\Users\\eitan\\Desktop\\cosas CEGIR\\maraton\\maraton6.1.mp4'


# Set the start and end times in seconds
start_time = 2 * 60 + 0  # Start time of the trimmed video (in seconds)
end_time = 4 * 60 + 00  # End time of the trimmed video (in seconds)

# Cut the video using ffmpeg_extract_subclip function
ffmpeg_extract_subclip(input_video, start_time, end_time, targetname=output_video)