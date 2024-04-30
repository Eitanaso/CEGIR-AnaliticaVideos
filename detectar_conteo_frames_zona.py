import cv2
import supervision as sv
import numpy as np
import time
from funciones.general import *
from funciones.estacionados import *
from clases.objeto_global import Objeto_Global
from clases.objeto_estacionados import Objeto_Estacionados

#import queue
#import threading

import pandas as pd
import datetime as datetime

from general import get_model



#frame = 'C:\\Users\\Analitica2\\Downloads\\1_ABRIL\\15.jpg'
#frame = cv2.imread(frame)
#model = get_model("yolov8_detector_graffitis.pt")
#selected_classes = 0

def detect(frame, model, selected_classes, zonas, centros_zonas):
    #----------------------------------------------------------
    results = model(frame, verbose=False)[0]
    detections = sv.Detections.from_ultralytics(results)
    # only consider class id from selected_classes define above
    detections = detections[np.isin(detections.class_id, selected_classes)]
    # tracking detections
    #detections = tareas.byte_tracker.update_with_detections(detections)
    #----------------------Detenidos cierto tiempo----------------
    #-----------------Nueva forma---------------------------------
    #----------------------------------------------------------------------

    annotated_frame = frame.copy()

    objeto_estacionados = Objeto_Estacionados()
    objeto_estacionados.frame_wh(annotated_frame)
    objeto_estacionados.create_polygone_zones(zonas)
    objeto_estacionados.create_polygone_zone_annotators(centros_zonas)
    annotated_frame = objeto_estacionados.anotar_frame(annotated_frame, detections, model)
    '''while True:
        #annotated_frame = cv2.resize(annotated_frame, (720, 480))
        #annotated_frame = cv2.resize(annotated_frame, (1080, 720))
        cv2.imshow('Camara Paseo Estacion con analitica', annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break'''

    return  annotated_frame, detections

#if __name__ == '__main__':

    #detect(frame, model, selected_classes)