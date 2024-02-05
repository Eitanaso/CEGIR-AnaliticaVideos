# pip install moviepy

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


# Set the file paths
input_video = 'D:\\Descargas\\uoct\\Alameda - Manuel RodrÃ_guez-2023-07-07_17h00min00s000ms_1-003.mp4'
output_video = 'D:\\Descargas\\uoct\\test6.mp4'


# Set the start and end times in seconds
start_time = 0 * 60 + 0  # Start time of the trimmed video (in seconds)
end_time = 1 * 60 + 0  # End time of the trimmed video (in seconds)

# Cut the video using ffmpeg_extract_subclip function
ffmpeg_extract_subclip(input_video, start_time, end_time, targetname=output_video)