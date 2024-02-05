import argparse
from detectar import run_detect, detect
from general import get_video, get_model
from clases.objeto_global import Objeto_Global

import queue
import threading
import multiprocessing
import time
import cv2

q = queue.Queue()

#--------------------------------------------------------------------------------------------------------------------
# Creacion de variables y funcion main para el control de los distintos tipos de analisis a realizar en videos
# Por mayores dudas de las variables o la funcion, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
#--------------------------------------------------------------------------------------------------------------------

# camara, modelo, clases, fps, tipo de tarea (deteccion, conteo, personas detenidas, velocidad), 
# puntos de los objetos a crear para la tarea (linea(s) para conteo, zona(s) para personas detenidas/velocidades), limites para velocidades
# colores de los objetos creados, nombres de los objetos a mostrar
# extras: mostrar etiquetas, mostrar trazas

parser = argparse.ArgumentParser(description='Ejecutar la deteccion del modelo')
#parser.add_argument('--tpo', help='Tiempo a guardar del video en vivo.', required=True, type=int)
#parser.add_argument('--fps', help='FPS de la camara', required=False, default=25)
#parser.add_argument('--camara', help='Camara a utilizar', required=False, default=r'rtsp://admin:Cafa2414$@10.0.10.182:554/0/profile2/media.smp')
#args = vars(parser.parse_args())


SOURCE_VIDEO_PATH = r'C:\Users\eitan\Pictures\comercio_ambulante_paseo_estacion.mp4'
#SOURCE_VIDEO_PATH = r'rtsp://root:pass@10.0.10.184/axis-media/media.amp'
#SOURCE_VIDEO_PATH = r'rtsp://admin:Cafa2414$@10.0.10.182:554/0/profile2/media.smp'
#TARGET_VIDEO_PATH = r'C:\Users\eitan\Pictures\comercio_ambulante_detectado.mp4'

rtsp_url = SOURCE_VIDEO_PATH
MODEL = "yolov8x.pt"
selected_classes = [0]
fps = 25

procesamiento = {
    'solo_mostrar': False,
    'solo_detector': False,
    'mostrar_contadores': False,
    'lineas_contadores': [
        #[(125, 333), (483, 195)],
        
        #[(450, 211), (1048, 207)],
        #[(1462, 768), (1739,775)],
        #[(334, 648), (1115, 350)],

        #[(0, 430), (160, 334)],
        [(160, 334), (468, 185)],
    ],
    'guardar_archivo_contador': False, 
    'mostrar_estacionados': False,
    'zonas_estacionados': [
        [(40, 188), (187, 337), (371, 412), (408, 333), (265, 273), (131, 167)],
        [(427, 256), (579, 301), (706, 325), (703, 242), (578, 218), (476, 181)],
    ],
    'centros_zonas_estacionados': [(75, 195), (480, 185)],
    'mostrar_trayectorias': False,
    'mostrar_velocidades': False,
    'velocidades_por_zonas': False,
    'zonas_velocidades': [
        [(1480, 1080), (1505, 480), (1706, 362), (1920, 450), (1920, 1080)],
        [(1480, 1080), (1505, 480), (1224, 377), (318, 756), (628, 1080)],
        [(318, 756), (1224, 377), (966, 222), (129, 485)],
    ],
    'min_max_zonas': [
        [0, 175],
        [0, 185],
        [0, 150],
    ],
    'guardar_videos_evento': False,
}

def main(rstp_url, model, clases, fps, procesamiento):
    cap = get_video(rstp_url)
    model = get_model(model)
    #print(model.model.names)
    run_detect(cap, model, clases, fps, procesamiento, mostrar_video=True, 
        guardar_video_resultado=True, dir_resultado='D:\\Descargas\\pruebas_horario\\imgs\\23_0_47.mp4')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
procesamiento = {'solo_mostrar': False, 'solo_detector': False, 'mostrar_contadores': False, 'lineas_contadores': [], 'guardar_archivo_contador': False,  'mostrar_estacionados': False, 'zonas_estacionados': [], 'centros_zonas_estacionados': [], 'mostrar_trayectorias': False, 'mostrar_velocidades': False, 'velocidades_por_zonas': False, 'zonas_velocidades': [], 'min_max_zonas': [], 'guardar_videos_evento': False,}
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
rtsp_url = 'D:\\Descargas\\pruebas_horario\\23_0_47.mp4'
#procesamiento['mostrar_contadores'] = True
#procesamiento['lineas_contadores'] = [[(120, 334), (494, 180)]]
procesamiento['mostrar_estacionados'] = True
procesamiento['zonas_estacionados'] = [[(0, 0), (0, 1080), (1920, 1080), (1920, 0)]]
procesamiento['zonas_estacionados'] = [[(0, 0), (0, 480), (720, 480), (720, 0)]]
procesamiento['centros_zonas_estacionados'] = [(30, 30)]
procesamiento['solo_mostrar'] = True
#MODEL = "best.pt"
#------------------------------------------------------------------------------------------------------------------------------------------------------------
# (182) Paseo Estacion Hanwha - Camara - 01-2024-01-07_17h15min00s000ms (20m) ---> ambulantes estacionados, se van por vehiculo carabinero, vuelven y despues se van corriendo
# corriendo en 10:50 - 11:30
#rtsp_url = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 01-2024-01-07_17h15min00s000ms_corte_corriendo.mp4'
#procesamiento['mostrar_velocidades'] = True
#procesamiento['velocidades_por_zonas'] = True
#procesamiento['zonas_velocidades'] = [[(316, 480), (232, 428), (563, 199), (720, 208), (720, 480)], [(232, 428), (563, 199), (457, 160), (74, 300)], [(74, 300), (457, 160), (352, 87), (0, 195)],]
#procesamiento['min_max_zonas'] = [[0, 90], [0, 85], [0, 80]]
# ambulante se instala en 3:30 - 6:30 (mas tiempo, pero corte aqui)
#rtsp_url = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 01-2024-01-07_17h15min00s000ms_corte_ambulante_instala.mp4'
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 01-2024-01-07_17h15min00s000ms_corte_ambulante_instala.mp4'
# ambulante se instala en 17:20 - 20:00 (final)
#rtsp_url = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 01-2024-01-07_17h15min00s000ms_corte_ambulante_instala2.mp4'
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 01-2024-01-07_17h15min00s000ms_corte_ambulante_instala2.mp4'
#procesamiento['mostrar_estacionados'] = True
#procesamiento['zonas_estacionados'] = [[(87, 220), (194, 326), (437, 248), (340, 148)]]
#procesamiento['centros_zonas_estacionados'] = [(340, 148)]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# (182) Paseo Estacion Hanwha - Camara - 01-2024-01-07_18h21min00s000ms (6m) ---> ciclistas, ambulantes se retiran y uno corre frente a un vehículo de carabineros
# corriendo en 5:20 - 5:31
#rtsp_url = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 01-2024-01-07_18h21min00s000ms_corte_corriendo.mp4'
#procesamiento['mostrar_velocidades'] = True
#procesamiento['velocidades_por_zonas'] = True
#procesamiento['zonas_velocidades'] = [[(316, 480), (232, 428), (563, 199), (720, 208), (720, 480)], [(232, 428), (563, 199), (457, 160), (74, 300)], [(74, 300), (457, 160), (352, 87), (0, 195)],]
#procesamiento['min_max_zonas'] = [[0, 95], [0, 98.5], [0, 80]]
# personas caminando entre vereda y calle en 2:25 - 2:55
#rtsp_url = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 01-2024-01-07_18h21min00s000ms_corte_entre_vereda_calle.mp4'
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 01-2024-01-07_18h21min00s000ms_corte_entre_vereda_calle.1.mp4'
#rtsp_url = 'D:\\Descargas\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 01-2024-01-07_18h21min00s000ms_corte_entre_vereda_calle.2.mp4'
#procesamiento['mostrar_contadores'] = True
#procesamiento['lineas_contadores'] = [[(0, 480), (163, 371)]]
# ambulante se instala en 00:00 - 3:01
#rtsp_url = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 01-2024-01-07_18h21min00s000ms_corte_ambulante_instala.mp4'
#procesamiento['mostrar_estacionados'] = True
#procesamiento['zonas_estacionados'] = [[(363, 321), (483, 211), (720, 306), (707, 439)]]
#procesamiento['centros_zonas_estacionados'] = [(483, 211)]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# (182) Paseo Estacion Hanwha - Camara - 01-2024-01-07_18h45min18s000ms (1m 44s) ---> ciclistas en vereda y personas caminando en la calle
# personas caminando entre vereda y calle en 1:05 - 1:25
#rtsp_url = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 01-2024-01-07_18h45min18s000ms_corte_entre_vereda_calle.mp4'
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 01-2024-01-07_18h45min18s000ms_corte_entre_vereda_calle.mp4'
#procesamiento['mostrar_contadores'] = True
#procesamiento['lineas_contadores'] = [[(0, 480), (163, 371)]]
# ciclista en vereda en 0:45 - 0:54
#rtsp_url = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 01-2024-01-07_18h45min18s000ms_corte_ciclista_vereda.mp4'
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 01-2024-01-07_18h45min18s000ms_corte_ciclista_vereda.mp4'
#procesamiento['mostrar_contadores'] = True
#procesamiento['lineas_contadores'] = [[(120, 334), (494, 180)]]
#selected_classes = [1]
# carabineros en 1:15-1:25
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 01-2024-01-07_18h45min18s000ms_corte_carabineros.mp4'
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# (182) Paseo Estacion Hanwha - Camara - 01-2024-01-07_19h06min54s000ms (43s) ---> ciclista contra el transito al final
# 39s - 43s ---> no sirve, no detecta la bicicleta ni el ciclista
#rtsp_url = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 01-2024-01-07_19h06min54s000ms.mp4'
#procesamiento['solo_detector'] = True
#selected_classes = [1]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# (182) Paseo Estacion Hanwha - Camara - 01-2024-01-07_20h53min00s000ms (16m 1s) ---> vehiculo estacionado mucho tiempo (no se ve mucho), ambulantes estacionados, otros eventos
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# (182) Paseo Estacion Hanwha - Camara - 01-2024-01-07_21h56min40s000ms (31s) ---> persona corriendo de noche
#rtsp_url = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 01-2024-01-07_21h56min40s000ms.mp4'
#procesamiento['mostrar_velocidades'] = True
#procesamiento['velocidades_por_zonas'] = True
#procesamiento['zonas_velocidades'] = [[(316, 480), (232, 428), (563, 199), (720, 208), (720, 480)], [(232, 428), (563, 199), (457, 160), (74, 300)], [(74, 300), (457, 160), (352, 87), (0, 195)],]
#procesamiento['min_max_zonas'] = [[0, 100], [0, 90], [0, 85]]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# (182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_17h15min00s000ms (20m) ---> personas cruzando mal, vehiculo esperando pasajeros, carabineros deteniendo a alguien
# ciclistas en sentido de transito en 00:00 - 00:07
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_17h15min00s000ms_corte_ciclista_transito.mp4'
# ciclista en transito en 5:47 - 5:53
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_17h15min00s000ms_corte_ciclista_transito2.mp4'
# ciclista en transito en 7:12 - 7:17
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_17h15min00s000ms_corte_ciclista_transito3.mp4'
#procesamiento['mostrar_contadores'] = True
#procesamiento['lineas_contadores'] = [[(0, 317), (465, 333)]]
#selected_classes = [1]
# ambulantes corriendo en 10:50 - 11:15
#rtsp_url = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_17h15min00s000ms_corte_corriendo.mp4'
#procesamiento['mostrar_velocidades'] = True
#procesamiento['velocidades_por_zonas'] = True
#procesamiento['zonas_velocidades'] = [[(473, 480), (453, 331), (720, 358), (720, 480)], [(453, 331), (439, 228), (720, 235), (720, 358)]]
#procesamiento['min_max_zonas'] = [[0, 54], [0, 50]]
# persona cruza por la calle en 00:40 - 1:05
#rtsp_url = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_17h15min00s000ms_corte_cruzando_calle.mp4'
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_17h15min00s000ms_corte_cruzando_calle.mp4'
# persona cruza por la calle en 1:50 - 2:15
#rtsp_url = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_17h15min00s000ms_corte_cruzando_calle2.mp4'
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_17h15min00s000ms_corte_cruzando_calle2.mp4'
# persona cruza por la calle en 2:35 - 3:10
#rtsp_url = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_17h15min00s000ms_corte_cruzando_calle3.mp4'
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_17h15min00s000ms_corte_cruzando_calle3.mp4'
# persona cruza por la calle en 6:30 - 6:40
#rtsp_url = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_17h15min00s000ms_corte_cruzando_calle4.mp4'
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_17h15min00s000ms_corte_cruzando_calle4.mp4'
# persona cruza por la calle en 17:20 - 17:55
#rtsp_url = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_17h15min00s000ms_corte_cruzando_calle5.mp4'
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_17h15min00s000ms_corte_cruzando_calle5.mp4'
#procesamiento['mostrar_contadores'] = True
#procesamiento['lineas_contadores'] = [[(48, 480), (302, 86)]]
# personas caminando entre vereda y calle en 16:50 - 17:05
#rtsp_url = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_17h15min00s000ms_corte_entre_vereda_calle.mp4'
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_17h15min00s000ms_corte_entre_vereda_calle.mp4'
#procesamiento['mostrar_contadores'] = True
#procesamiento['lineas_contadores'] = [[(299, 395), (479, 388)]]
# ciclista en vereda en 13:10 - 13:30
#rtsp_url = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_17h15min00s000ms_corte_ciclista_vereda.mp4'
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_17h15min00s000ms_corte_ciclista_vereda.mp4'
#procesamiento['mostrar_contadores'] = True
#procesamiento['lineas_contadores'] = [[(459, 323), (720, 338)]]
#selected_classes = [1]
# ambulante se instala en 17:25 - 20:00 (final)
#rtsp_url = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_17h15min00s000ms_corte_ambulante_instala.mp4'
#procesamiento['mostrar_estacionados'] = True
#procesamiento['zonas_estacionados'] = [[(505, 480), (471, 300), (720, 317), (720, 480)]]
#procesamiento['centros_zonas_estacionados'] = [(471, 300)]
# persona entra a la calle y vuelve en 7:53 - 8:04
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_17h15min00s000ms_corte_persona_calle.mp4'
#procesamiento['mostrar_estacionados'] = True
#procesamiento['zonas_estacionados'] = [[(0, 480), (0, 182), (189, 75), (388, 81), (445, 479)]]
#procesamiento['centros_zonas_estacionados'] = [(189, 75)]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# (182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_18h21min00s000ms (6m) ---> vehiculos dejando personas, ambulante corriendo de vehiculo de carabineros
# personas caminando entre vereda y calle en 2:25 - 3:15
#rtsp_url = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_18h21min00s000ms_corte_entre_vereda_calle.mp4'
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_18h21min00s000ms_corte_entre_vereda_calle.1.mp4'
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_18h21min00s000ms_corte_entre_vereda_calle.2.mp4'
#procesamiento['mostrar_contadores'] = True
#procesamiento['lineas_contadores'] = [[(299, 395), (479, 388)]]
# ciclista en transito en 3:05 - 3:12
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_18h21min00s000ms_corte_ciclista_transito1.mp4'
# ciclista en transito en 4:45 - 4:52
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_18h21min00s000ms_corte_ciclista_transito2.mp4'
#procesamiento['mostrar_contadores'] = True
#procesamiento['lineas_contadores'] = [[(0, 317), (465, 333)]]
#selected_classes = [1]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# (182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_18h45min18s000ms (1m 46s) ---> ciclistas y personas cruzando calle, personas en calle y caminando por reja
# persona cruza por la calle en 00:20 - 00:35
#rtsp_url = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_18h45min18s000ms_corte_cruzando_calle.mp4'
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_18h45min18s000ms_corte_cruzando_calle.mp4'
#procesamiento['mostrar_contadores'] = True
#procesamiento['lineas_contadores'] = [[(48, 480), (302, 86)]]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# (182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_19h06min54s000ms (43s) ---> ciclista contra el transito
# ciclista contra transito en 00:35 - 00:44
#rtsp_url = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_19h06min54s000ms_corte_ciclista_contra_transit.mp4'
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_19h06min54s000ms_corte_ciclista_contra_transit.mp4'
#procesamiento['mostrar_contadores'] = True
#procesamiento['lineas_contadores'] = [[(0, 317), (465, 333)]]
#selected_classes = [1]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# (182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_20h53min00s000ms (16m) ---> vehiculos estacionados mucho tiempo en alameda, personas (lejos) cruzando mal
# vehiculo se detiene en 4:45 - 7:00 (mas tiempo, pero es suficiente)
#rtsp_url = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_20h53min00s000ms_corte_vehiculo_detenido.mp4'
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_20h53min00s000ms_corte_vehiculo_detenido.mp4'
# vehiculo se detiene en 14:00 - 15:30 (cortar cuando ya este detectado)
#rtsp_url = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_20h53min00s000ms_corte_vehiculo_detenido2.mp4'
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_20h53min00s000ms_corte_vehiculo_detenido2.mp4'
#procesamiento['mostrar_estacionados'] = True
#procesamiento['zonas_estacionados'] = [[(240, 468), (294, 197), (408, 191), (452, 479)]]
#procesamiento['centros_zonas_estacionados'] = [(294, 197)]
#selected_classes = [2]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# (182) Paseo Estacion Hanwha - Camara - 02-2024-01-07_21h56min40s000ms (31s) ---> persona corriendo de noche (mismo anterior)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# (182) Paseo Estacion Hanwha - Camara - 04-2024-01-07_17h15min00s000ms (20m) ---> ambulantes van y vienen, vehiculo de carabineros pasando (quizas corren, no se ve mucho)
# ambulantes corriendo en 11:00 - 11:15
#rtsp_url = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 04-2024-01-07_17h15min00s000ms_corte_corriendo.mp4'
#procesamiento['mostrar_velocidades'] = True
#procesamiento['velocidades_por_zonas'] = True
#procesamiento['zonas_velocidades'] = [[(0, 480), (0, 245), (91, 232), (494, 443), (494, 480)], [(91, 232), (218, 171), (460, 264), (494, 443)]]
#procesamiento['min_max_zonas'] = [[0, 85], [0, 60]]
# persona corriendo en 12:05 - 12:15
#rtsp_url = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 04-2024-01-07_17h15min00s000ms_corte_corriendo2.mp4'
#procesamiento['mostrar_velocidades'] = True
#procesamiento['velocidades_por_zonas'] = True
#procesamiento['zonas_velocidades'] = [[(0, 480), (0, 245), (91, 232), (494, 443), (494, 480)], [(91, 232), (218, 171), (460, 264), (494, 443)]]
#procesamiento['min_max_zonas'] = [[0, 85], [0, 60]]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# (182) Paseo Estacion Hanwha - Camara - 04-2024-01-07_18h21min00s000ms (6m) ---> ambulante se instala, luego se retira al final por vehiculo de carabinero
# ciclista en vereda en 5:35 - final
#rtsp_url = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 04-2024-01-07_18h21min00s000ms_corte_ciclista_vereda.mp4'
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 04-2024-01-07_18h21min00s000ms_corte_ciclista_vereda.mp4'
#procesamiento['mostrar_contadores'] = True
#procesamiento['lineas_contadores'] = [[(470, 465), (62, 209)]]
#selected_classes = [1]
# ambulante se instala en 00:00 - 2:40
#rtsp_url = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 04-2024-01-07_18h21min00s000ms_corte_ambulante_instala.mp4'
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 04-2024-01-07_18h21min00s000ms_corte_ambulante_instala.mp4'
#procesamiento['mostrar_estacionados'] = True
#procesamiento['zonas_estacionados'] = [[(0, 480), (0, 264), (121, 232), (500, 480)]]
#procesamiento['centros_zonas_estacionados'] = [(121, 232)]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# (182) Paseo Estacion Hanwha - Camara - 04-2024-01-07_18h45min18s000ms (1m 42s) ---> carabineros pasan por la vereda al final
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 04-2024-01-07_18h45min18s000ms_corte.mp4'
#procesamiento['solo_detector'] = True
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# (182) Paseo Estacion Hanwha - Camara - 04-2024-01-07_19h06min54s000ms (41s) ---> no veo nada
# (182) Paseo Estacion Hanwha - Camara - 04-2024-01-07_20h53min00s000ms (16m) ---> no vi nada
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# (182) Paseo Estacion Hanwha - Camara - 04-2024-01-07_21h56min40s000ms (32s) ---> misma persona corriendo en la noche
# persona corriendo en l noche 00:20 - 00:33
#rtsp_url = 'C:\\Users\\admin\\Desktop\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 04-2024-01-07_21h56min40s000ms.mp4'
#procesamiento['mostrar_velocidades'] = True
#procesamiento['velocidades_por_zonas'] = True
#procesamiento['zonas_velocidades'] = [[(0, 480), (0, 245), (91, 232), (494, 443), (494, 480)], [(91, 232), (218, 171), (460, 264), (494, 443)]]
#procesamiento['min_max_zonas'] = [[0, 85], [0, 60]]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# peaton_cruzando_por_ciclovia
# corte para no desconcentrar en 0:09 - 0:24
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\peaton_cruzando_por_ciclovia_corte.mp4'
#procesamiento['mostrar_estacionados'] = True
#procesamiento['zonas_estacionados'] = [[(0, 208), (196, 201), (198, 209), (1, 226)]]
#procesamiento['centros_zonas_estacionados'] = [(198, 228)]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# video_flujo_personas_cruce_peatonal
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\video_flujo_personas_cruce_peatonal_corte.mp4'
#procesamiento['mostrar_contadores'] = True
#procesamiento['lineas_contadores'] = [[(470, 627), (583, 627)]]
#procesamiento['lineas_contadores'] = [[(0, 655), (465, 652)]]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# flujo_ciclistas_ciclovia -----> mkv
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\flujo_ciclistas_ciclovia.mkv'
#procesamiento['mostrar_contadores'] = True
#procesamiento['lineas_contadores'] = [[(496, 239), (496, 192)]]
#selected_classes = [1]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# cruce_calzada_corriendo
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\cruce_calzada_corriendo_corte.mp4'
#procesamiento['mostrar_velocidades'] = True
#procesamiento['velocidades_por_zonas'] = True
#procesamiento['zonas_velocidades'] = [[(0, 720), (1183, 191), (1280, 169), (1280, 720)],]
#procesamiento['min_max_zonas'] = [[0, 100],]
#procesamiento['mostrar_estacionados'] = True
#procesamiento['zonas_estacionados'] = [[(0, 720), (1183, 191), (1280, 169), (1280, 720)]]
#procesamiento['centros_zonas_estacionados'] = [(1183, 191)]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# personas_cruzando_mitad_cuadra.mp4
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\personas_cruzando_mitad_cuadra.mp4'
#procesamiento['mostrar_estacionados'] = True
#procesamiento['zonas_estacionados'] = [[(0, 240), (720, 273), (720, 480), (0, 480)]]
#procesamiento['centros_zonas_estacionados'] = [(80, 237)]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# transito_peatonal_1min10seg ------> mov
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# (182) Paseo Estacion Hanwha - Camara - 05-2024-01-17_13h38min00s000ms
# overoles blancos bien en 8:09 - 8:13
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 05-2024-01-17_13h38min00s000ms_corte.mp4'
# overoles blancos bien en 9:59 - 12:59
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 05-2024-01-17_13h38min00s000ms_corte2.mp4'
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 05-2024-01-17_13h38min00s000ms_corte2.1.mp4'
# 3:53 - 3:58
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 05-2024-01-17_13h38min00s000ms_corte3.mp4'
# (018) Paseo Estación _ Matucana-2024-01-17_13h38min00s000ms
# 1:24 - 1:50
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(018) Paseo Estación _ Matucana-2024-01-17_13h38min00s000ms_corte.mp4'
# (184) Paseo Estacion Axis PTZ-2024-01-17_13h38min00s000ms
# 2:23 - 2:28
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(184) Paseo Estacion Axis PTZ-2024-01-17_13h38min00s000ms_corte.mp4'
#procesamiento['solo_detector'] = True
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# (021) Paseo Estación _ Exposición-2023-09-10_12h00min00s000ms
# corte en 0:36 - 0:49
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(021) Paseo Estación _ Exposición-2023-09-10_12h00min00s000ms_corte.mp4'
#procesamiento['mostrar_contadores'] = True
#procesamiento['lineas_contadores'] = [[(131, 308), (582, 318)]]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# vista_360_(021) Paseo Estación _ Exposición-2023-09-20_12h10min00s000ms
# cruce peatonal en 6:38 - 6:54
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\vista_360_(021) Paseo Estación _ Exposición-2023-09-20_12h10min00s000ms_corte.mp4'
#procesamiento['mostrar_contadores'] = True
#procesamiento['lineas_contadores'] = [[(198, 617), (886, 190)]]
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\cruce_exposicion_no_vehi.mp4'
#procesamiento['mostrar_contadores'] = True
#procesamiento['lineas_contadores'] = [[(170, 404), (578, 635)]]
#selected_classes = [2]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# (020) Alameda _ Matucana-2023-09-07_18h00min00s000ms
# personas cruzando mal en 12:50 - 13:23
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(020) Alameda _ Matucana-2023-09-07_18h00min00s000ms_corte.mp4'
#procesamiento['mostrar_estacionados'] = True
#procesamiento['zonas_estacionados'] = [[(0, 1007), (514, 773), (630, 574), (1434, 589), (1580, 702), (1920, 768), (1920, 857)]]
#procesamiento['centros_zonas_estacionados'] = [(1300, 575)]
# ciclista en vereda en 26:20 - 26:27
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(020) Alameda _ Matucana-2023-09-07_18h00min00s000ms_corte2.mp4'
#procesamiento['mostrar_contadores'] = True
#procesamiento['lineas_contadores'] = [[(457, 817), (215, 680)]]
#selected_classes = [1]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# (001) Alameda _ San Borja-2023-08-16_13h29min00s000ms
# ciclistas en calle en 0:40 - 0:54
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(001) Alameda _ San Borja-2023-08-16_13h29min00s000ms_corte.mp4'
#procesamiento['mostrar_contadores'] = True
#procesamiento['lineas_contadores'] = [[(157, 455), (860, 553)]]
#selected_classes = [1]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# (016) Alameda - Persa Estación-2023-08-16_16h00min00s000ms
# ciclistas en ciclovia en 0:39 - 0:49
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(016) Alameda - Persa Estación-2023-08-16_16h00min00s000ms_corte.mp4'
#procesamiento['mostrar_contadores'] = True
#procesamiento['lineas_contadores'] = [[(634, 635), (877, 642)]]
#selected_classes = [1]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# vehiculo_mal_estacionado_(006) Alameda _ Toro Mazote-2023-09-28_17h54min45s000ms-vehiculo_mal_estacionado
# vehiculo del video en 0:58 - 1:23
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\vehiculo_mal_estacionado_(006) Alameda _ Toro Mazote-2023-09-28_17h54min45s000ms-vehiculo_mal_estacionado_corte.mp4'
#procesamiento['mostrar_estacionados'] = True
#procesamiento['zonas_estacionados'] = [[(577, 320), (828, 469), (980, 412), (732, 270)]]
#procesamiento['centros_zonas_estacionados'] = [(740, 270)]
#selected_classes = [2]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# sin procesar Detección de persona ocupando un lugar predeterminado
# corte desde 00:00 - 1:16
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\sin procesar Detección de persona ocupando un lugar predeterminado_corte.mp4'
#procesamiento['mostrar_estacionados'] = True
#procesamiento['zonas_estacionados'] = [[(24, 197), (322, 464), (416, 351), (157, 159)]]
#procesamiento['centros_zonas_estacionados'] = [(330, 470)]
# conteo de personas desde 
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\sin procesar Detección de persona ocupando un lugar predeterminado_corte2.mp4'
#procesamiento['mostrar_contadores'] = True
#procesamiento['lineas_contadores'] = [[(141, 358), (540, 202)]]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# (003) Mall Plaza _ Marinero Díaz-lanzazo12
# corte en 0:39 - 0:48
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(003) Mall Plaza _ Marinero Díaz-lanzazo12_corte.mp4'
#procesamiento['mostrar_trayectorias'] = True
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# (016) Alameda - Persa Estación-2022-11-15_17h10min34s870ms
# corte en 0:19 - 0:25
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(016) Alameda - Persa Estación-2022-11-15_17h10min34s870ms_corte.mp4'
#procesamiento['mostrar_velocidades'] = True
#procesamiento['velocidades_por_zonas'] = True
#procesamiento['zonas_velocidades'] = [[(422, 434), (747, 352), (807, 509), (526, 602)]]
#procesamiento['min_max_zonas'] = [[0, 30]]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# pelea_campal_(018) Paseo Estación _ Matucana-2023-01-10_18h08min53s955ms
# corte en 0:50 - 1:00
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\pelea_campal_(018) Paseo Estación _ Matucana-2023-01-10_18h08min53s955ms_corte.mp4'
#procesamiento['mostrar_velocidades'] = True
#procesamiento['velocidades_por_zonas'] = True
#procesamiento['zonas_velocidades'] = [[(0, 720), (0, 450), (300, 351), (1050, 531), (1080, 720)], [(300, 350), (1050, 530), (1110, 380), (420, 290)], [(420, 289), (1110, 379), (1100, 290), (610, 240)],[(0, 450), (300, 351), (420, 290), (310, 200), (0, 250)]]
#procesamiento['min_max_zonas'] = [[0, 135], [0, 80], [0, 75], [0, 55]]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------



#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 01-2024-01-07_18h45min18s000ms_corte_carabineros.mp4'
#rtsp_url = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\test.mp4'
#procesamiento['solo_detector'] = True


#rtsp_url = 'D:\\Descargas\\videos_casos_uso_nuevos_cegir\\validacion_flujo_peatonal_23_enero_11am.mkv'
#rtsp_url = 'D:\\Descargas\\videos_casos_uso_nuevos_cegir\\(182) Paseo Estacion Hanwha - Camara - 01-2024-01-23_11h17min00s000ms.mp4'
#rtsp_url = 'D:\\Descargas\\pruebas_horario\\0_0_47.mp4'
#procesamiento['mostrar_contadores'] = True
#procesamiento['lineas_contadores'] = [[(120, 334), (494, 180)]]
#procesamiento['mostrar_estacionados'] = True
#procesamiento['zonas_estacionados'] = [[(0, 0), (0, 480), (720, 480), (720, 0)]]
#procesamiento['centros_zonas_estacionados'] = [(30, 30)]
#MODEL = "best.pt"

#rtsp_url = 'D:\\Descargas\\uoct\\test6.mp4'
#procesamiento['solo_detector'] = True
#selected_classes = [2]


if __name__ == '__main__':

    #p1 = threading.Thread(target=Receive)
    #p2 = threading.Thread(target=Display)
    #p1 = multiprocessing.Process(target=Receive)
    #p2 = multiprocessing.Process(target=Display)
    #p1.start()
    #p2.start()
    main(rtsp_url, MODEL, selected_classes, fps, procesamiento)


def Receive():
    cap = get_video(rtsp_url)
    ret, frame = cap.read()
    q.put(frame)
    while ret:
        ret, frame = cap.read()
        #print('a')
        q.put(frame)
        #print('b')

def Display():
    model = get_model(MODEL)
    i = 0
    tiempos = []
    clases = selected_classes

    if not procesamiento['solo_mostrar']:
        tareas = Objeto_Global(fps)
        tareas.create_byte_tracker()
        if procesamiento['solo_detector']:
            tareas.create_detector()
        if procesamiento['mostrar_estacionados']:
            tareas.create_estacionados(frame, procesamiento['zonas_estacionados'], procesamiento['centros_zonas_estacionados'])
        if procesamiento['mostrar_contadores']:
            tareas.create_contadores(procesamiento['lineas_contadores'])
        if procesamiento['mostrar_trayectorias']:
            tareas.create_trayectorias()
        if procesamiento['mostrar_velocidades']:
            tareas.create_velocidades()

    while True:
        if q.empty() != True:
            frame = q.get()
            ti = time.time()
            if procesamiento['solo_mostrar']:
                output_frame = frame
            else:
                #print('c')
                output_frame = detect(frame, model, clases, tareas)
                #print('d')
                tiempos.append((time.time() - ti)*1000)
                i += 1
            cv2.imshow('Camara Paseo Estacion con analitica', output_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
