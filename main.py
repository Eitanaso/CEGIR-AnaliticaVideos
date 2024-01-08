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
#SOURCE_VIDEO_PATH = r'rtsp://admin:Cafa2414$@10.0.10.182:554/3/profile2/media.smp'
#TARGET_VIDEO_PATH = r'C:\Users\eitan\Pictures\comercio_ambulante_detectado.mp4'

rtsp_url = SOURCE_VIDEO_PATH
MODEL = "yolov8n.pt"
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
    'mostrar_trayectorias': True,
    'mostrar_velocidades': False,
    'velocidades_por_zonas': False,
    'zonas_velocidades': [
        [(316, 480), (232, 428), (563, 199), (720, 208), (720, 480)],
        [(232, 428), (563, 199), (457, 160), (74, 300)],
        [(74, 300), (457, 160), (352, 87), (0, 195)],
    ],
    'min_max_zonas': [
        [0, 100],
        [0, 90],
        [0, 70],
    ],
    'guardar_videos_evento': True,
}

def main(rstp_url, model, clases, fps, procesamiento):
    cap = get_video(rstp_url)
    model = get_model(model)
    #print(model.model.names)
    run_detect(cap, model, clases, fps, procesamiento)



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
