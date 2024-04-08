import argparse
from detectar_graffitis import detect
from general import get_video, get_model
from clases.objeto_global import Objeto_Global

from datetime import datetime
import time
import numpy as np

from PIL import Image
import pyscreenshot as ImageGrab

import pandas as pd

import cv2

#SOURCE_VIDEO_PATH = 'c:\\Users\\Analitica2\\Desktop\\test\\comercio_ambulante_paseo_estacion.mp4'
#rtsp_url = SOURCE_VIDEO_PATH
MODEL = "yolov8_detector_graffitis.pt"
#MODEL = 'yolov8x.pt'
selected_classes = 0
segs_frame = 10
fps = 25

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

def main(model, i=0):
    # datetime object containing current date and time
    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("inicio =", dt_string)

    #cap = get_video(rstp_url)
    model = get_model(model)
    #_, output_frame = cap.read()
    starttime = time.monotonic()
    print(starttime)
    global img
    img = ImageGrab.grab()
    img = np.asarray(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imshow('frame', img)
    global puntos
    puntos = []
    cv2.setMouseCallback('frame', click_event)
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    print(puntos)
    bbox = (puntos[0][0], puntos[0][1],puntos[1][0],puntos[1][1])
    #while cap.isOpened():
    df=pd.DataFrame({'Hora Deteccion':[], 'Cantidad Detectado':[]})
    while True:
        #ret, frame = cap.read()
        #bbox = (100, 100, 700, 800)
        frame = ImageGrab.grab(bbox=bbox)
        frame = np.asarray(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #if not ret:
            #break
        #if i % int(fps * segs_frame) == 0:
        output_frame, dets = detect(frame, model, selected_classes)
        print(len(dets))
        cv2.imshow('Camara Paseo Estacion con analitica', output_frame)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        nueva_fila = {'Hora Deteccion':dt_string, 'Cantidad Detectado':len(dets)}
        df = pd.concat([df, pd.DataFrame(nueva_fila, index=[0])], ignore_index=True)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        i += 1
        time.sleep(segs_frame)# - ((time.monotonic() - starttime) % 60.0))

    df.to_csv('C:\\Users\\Analitica2\\Desktop\\codigo_funcional\\graffitis.csv', index=False)

    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("fin =", dt_string)

if __name__ == '__main__':

    main(MODEL)