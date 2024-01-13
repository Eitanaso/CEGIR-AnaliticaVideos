# pip install moviepy

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


# Set the file paths
input_video = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_20h53min00s000ms.mp4'
output_video = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_20h53min00s000ms_corte_vehiculo_detenido2.mp4'


# Set the start and end times in seconds
start_time = 14 * 60 + 10  # Start time of the trimmed video (in seconds)
end_time = 15 * 60 + 30  # End time of the trimmed video (in seconds)

# Cut the video using ffmpeg_extract_subclip function
ffmpeg_extract_subclip(input_video, start_time, end_time, targetname=output_video)