import argparse
from detectar_graffitis import detect
from general import get_video, get_model
from clases.objeto_global import Objeto_Global

from datetime import datetime

import cv2

SOURCE_VIDEO_PATH = 'c:\\Users\\Analitica2\\Desktop\\test\\comercio_ambulante_paseo_estacion.mp4'
rtsp_url = SOURCE_VIDEO_PATH
MODEL = "yolov8_detector_graffitis.pt"
#MODEL = 'yolov8x.pt'
selected_classes = 0
segs_frame = 1
fps = 25

def main(rstp_url, model, i=0):
    # datetime object containing current date and time
    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("inicio =", dt_string)

    cap = get_video(rstp_url)
    model = get_model(model)
    _, output_frame = cap.read()
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if i % int(fps * segs_frame) == 0:
            output_frame = detect(frame, model, selected_classes)
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