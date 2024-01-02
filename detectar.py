import cv2
import supervision as sv
import numpy as np
import time
from funciones.general import *
from funciones.estacionados import *
from clases.objeto_global import Objeto_Global

#--------------------------------------------------------------------------------------------------------------------
# Creacion de funciones para iniciar el procesamiento segun lo solicitado
# Funciones creadas a partir de código de la libreria Supervision y de codigo para la conexion a camaras de Luis Escares
# Por mayores dudas de las funciones, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
#--------------------------------------------------------------------------------------------------------------------


def detect(frame, model, selected_classes, tareas):
    #----------------------------------------------------------
    results = model(frame, verbose=False)[0]
    detections = sv.Detections.from_ultralytics(results)
    # only consider class id from selected_classes define above
    detections = detections[np.isin(detections.class_id, selected_classes)]
    # tracking detections
    detections = tareas.byte_tracker.update_with_detections(detections)
    #----------------------Detenidos cierto tiempo----------------
    #-----------------Nueva forma---------------------------------
    #----------------------------------------------------------------------

    annotated_frame = frame.copy()

    if tareas.solo_detector:
        annotated_frame=tareas.objeto_Detector.anotar_frame(annotated_frame, detections, model)
    else:
        if tareas.estacionados:
            annotated_frame = tareas.objeto_Estacionados.anotar_frame(annotated_frame, detections, model)
        if tareas.contadores:
            annotated_frame = tareas.objeto_Contadores.anotar_frame(annotated_frame, detections, model)

    return  annotated_frame

def run_detect(cap, model, clases, fps, procesamiento, tiempos=[], i=0):

    ret, frame = cap.read()

    if not procesamiento['solo_mostrar']:
        tareas = Objeto_Global(fps)
        tareas.create_byte_tracker()
        if procesamiento['solo_detector']:
            tareas.create_detector()
        if procesamiento['mostrar_estacionados']:
            tareas.create_estacionados(frame, procesamiento['zonas_estacionados'], procesamiento['centros_zonas_estacionados'])
        if procesamiento['mostrar_contadores']:
            tareas.create_contadores(procesamiento['lineas_contadores'])

    while cap.isOpened():
        ret, frame = cap.read()
        #frame = cv2.resize(frame, (640, 640))
        if not ret:
            break
        # Perform detection
        ti = time.time()
        if procesamiento['solo_mostrar']:
            output_frame = frame
        else:
            output_frame = detect(frame, model, clases, tareas)
        tiempos.append((time.time() - ti)*1000)
        i += 1
        #output_frame=frame

        # Display the frame with detections
        cv2.imshow('Camara Paseo Estacion con analitica', output_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break