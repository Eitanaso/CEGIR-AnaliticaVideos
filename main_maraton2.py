import argparse
from maraton.detectar_conteo_maraton import detect
from general import get_video, get_model
from clases.objeto_global import Objeto_Global

from datetime import datetime

import cv2

import pyscreenshot as ImageGrab
import time
import numpy as np
import pandas as pd

from maraton.objeto_maraton import Objeto_Estacionados
import supervision as sv

SOURCE_VIDEO_PATH = 'C:\\Users\\eitan\\Desktop\\cosas CEGIR\\maraton\\maraton6.1.mp4'
rtsp_url = SOURCE_VIDEO_PATH
#MODEL = "yolov8_detector_graffitis.pt"
MODEL = 'yolov8x.pt'
#MODEL = 'yolo_4158imgs_augment_30brillo.pt'
selected_classes = 0
segs_frame = 0.15
fps = 25

zonas = [
        #[(10, 230), (400, 80), (718, 242), (718, 478), (300, 478)],
]
centros_zonas = [(50, 30)]



def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Mostrar el punto seleccionado
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        # Mostrar las coordenadas del punto
        print("Coordenadas del punto:", x, y)
        # Guardar las coordenadas en una lista
        puntos.append((x, y))
        # Refrescar la imagen
        #cv2.imshow('image', img)

def main(rstp_url, model, i=0):
    # datetime object containing current date and time
    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("inicio =", dt_string)

    cap = get_video(rstp_url)
    model = get_model(model)
    _, output_frame = cap.read()
    starttime = time.monotonic()
    print(starttime)
    global img
    _, img = cap.read()
    cv2.imshow('frame', img)
    global puntos
    puntos = []
    cv2.setMouseCallback('frame', click_event)
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            zonas.append(puntos)
            break
    cv2.destroyAllWindows()

    #while cap.isOpened():
    df=pd.DataFrame({'Hora Deteccion':[], 'Cantidad Detectado':[]})
    objeto_estacionados = Objeto_Estacionados()
    objeto_estacionados.frame_wh(output_frame)
    objeto_estacionados.create_polygone_zones(zonas)
    objeto_estacionados.create_polygone_zone_annotators(centros_zonas)
    byte_tracker = sv.ByteTrack(track_thresh = 0.15, 
                                         track_buffer = int(1/segs_frame), 
                                         match_thresh = 0.8, 
                                         frame_rate = int(1/segs_frame)
                                         )
    
    video_writer = cv2.VideoWriter('C:\\Users\\eitan\\Desktop\\cosas CEGIR\\maraton\\maraton_resultado.mp4', cv2.VideoWriter_fourcc(*'mp4v'), int(1/segs_frame), (output_frame.shape[1], output_frame.shape[0]))
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if i % int(fps * segs_frame) == 0:
            output_frame, conteo_total = detect(frame, model, selected_classes, zonas, centros_zonas, objeto_estacionados, byte_tracker)
            print(conteo_total)
            cv2.imshow('Camara Paseo Estacion con analitica', output_frame)
            video_writer.write(output_frame)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        nueva_fila = {'Hora Deteccion':dt_string, 'Cantidad Detectado':conteo_total}
        df = pd.concat([df, pd.DataFrame(nueva_fila, index=[0])], ignore_index=True)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        i += 1
        #time.sleep(segs_frame)# - ((time.monotonic() - starttime) % 60.0))

    df.to_csv('C:\\Users\\eitan\\Desktop\\cosas CEGIR\\maraton\\maraton.csv', index=False)

    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("fin =", dt_string)

if __name__ == '__main__':

    main(rtsp_url, MODEL)