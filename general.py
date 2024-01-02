import cv2
from ultralytics import YOLO

#--------------------------------------------------------------------------------------------------------------------
# Creacion de funciones generales pequenas, para no saturar el codigo
# Por mayores dudas de las funciones, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
#--------------------------------------------------------------------------------------------------------------------

def get_video(rtsp_url):
    return cv2.VideoCapture(rtsp_url)

def get_model(MODEL):
    model = YOLO(MODEL)
    model.fuse()
    return model

def create_labels(detecciones, modelo):
    labels = []
    for bbox, xyxy, confidence, class_id, tracker_id in detecciones:
        labels.append(f"{modelo.model.names[class_id]} {[tracker_id]}")
    return labels