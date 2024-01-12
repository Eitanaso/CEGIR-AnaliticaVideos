# pip install moviepy

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


# Set the file paths
input_video = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 01-2024-01-07_19h06min54s000ms.mp4'
output_video = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\test.mp4'


# Set the start and end times in seconds
start_time = 38  # Start time of the trimmed video (in seconds)
end_time = 43  # End time of the trimmed video (in seconds)

# Cut the video using ffmpeg_extract_subclip function
ffmpeg_extract_subclip(input_video, start_time, end_time, targetname=output_video)