import argparse
from detectar_conteo_frames_zona import detect
from general import get_video, get_model
from clases.objeto_global import Objeto_Global

from datetime import datetime

import cv2

SOURCE_VIDEO_PATH = 'c:\\Users\\Analitica2\\Desktop\\test\\comercio_ambulante_paseo_estacion.mp4'
rtsp_url = SOURCE_VIDEO_PATH
#MODEL = "yolov8_detector_graffitis.pt"
MODEL = 'yolov8x.pt'
MODEL = 'yolo_4158imgs_augment_30brillo.pt'
selected_classes = 0
segs_frame = 3
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
        cv2.imshow('image', img)

def main(rstp_url, model, i=0):
    # datetime object containing current date and time
    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("inicio =", dt_string)

    cap = get_video(rstp_url)
    model = get_model(model)
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
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if i % int(fps * segs_frame) == 0:
            output_frame = detect(frame, model, selected_classes, zonas, centros_zonas)
        cv2.imshow('Camara Paseo Estacion con analitica', output_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        i += 1

    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("fin =", dt_string)

if __name__ == '__main__':

    main(rtsp_url, MODEL)