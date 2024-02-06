# pip install moviepy

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


# Set the file paths
input_video = 'D:\\Descargas\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 01-2024-01-07_17h15min00s000ms.mp4'
output_video = 'D:\\Descargas\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 01-2024-01-07_17h15min00s000ms_corte_corriendo.mp4'


# Set the start and end times in seconds
start_time = 10 * 60 + 50  # Start time of the trimmed video (in seconds)
end_time = 11 * 60 + 30  # End time of the trimmed video (in seconds)

# Cut the video using ffmpeg_extract_subclip function
ffmpeg_extract_subclip(input_video, start_time, end_time, targetname=output_video)