import cv2
import supervision as sv
import numpy as np
import time
from funciones.general import *
from funciones.estacionados import *
from clases.objeto_global import Objeto_Global

#import queue
#import threading

import pandas as pd
import datetime as datetime



#--------------------------------------------------------------------------------------------------------------------
# Creacion de funciones para iniciar el procesamiento segun lo solicitado
# Funciones creadas a partir de código de la libreria Supervision y de codigo para la conexion a camaras y guardado de archivos de Luis Escares
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
        annotated_frame = tareas.objeto_Contadores.anotar_frame(annotated_frame, detections, model)

    return  annotated_frame



def run_detect(cap, model, procesamiento, i=0, j=1):

    #ret, frame = cap.read()
    #frame = frame[60:-60, 240:-240]
    #frame = cv2.resize(frame, (720, 480))
    segundo_entre_registros = procesamiento['var']['periodicidad_contador']
    segundos_reinicio_contador = procesamiento['var']['periodicidad_contador']
    columnas_indicador = {'Hora Conteo':[], procesamiento['var']['texto_contador'][0]:[], procesamiento['var']['texto_contador'][1]:[]}
    id_cam = procesamiento['info']['ID_cam']
    pos_cam = procesamiento['info']['pos_cam']
    dia = procesamiento['info']['dia']
    hora = procesamiento['info']['hora']
    nombre_cont = procesamiento['var']['nombre_contador']
    x1 = procesamiento['var']['linea_contador'][0][0]
    y1 = procesamiento['var']['linea_contador'][0][1]
    x2 = procesamiento['var']['linea_contador'][1][0]
    y2 = procesamiento['var']['linea_contador'][1][1]
    dir_archivo = procesamiento['var']['direccion_archivo']
    nombre_archivo = f'{id_cam}_{pos_cam}_{dia}_{hora}_{nombre_cont}_{x1}_{y1}_{x2}_{y2}.csv'
    path_archivo = f'{dir_archivo}{nombre_archivo}'
    df=pd.DataFrame(columnas_indicador)
    #momento = datetime.datetime.now()
    #momento = f'{momento.month}_{momento.day}_{momento.hour}_{momento.minute}'

    fps = procesamiento['var']['fps']
    
    if not procesamiento['var_fijas']['solo_mostrar']:
        tareas = Objeto_Global(fps)
        tareas.create_byte_tracker()
        if not procesamiento['var_fijas']['contador']:
            tareas.create_detector()
        else:
            tareas.create_contadores(procesamiento['var']['linea_contador'], procesamiento['var']['texto_contador'],
                                     procesamiento['var_fijas']['pos_texto_contador'], procesamiento['var_fijas']['color_contador'],)
            
    while cap.isOpened():
    #while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Perform detection
        #frame = frame[60:-60, 240:-240]
        #frame = cv2.resize(frame, (720, 480))
        #ti = time.time()
        if procesamiento['var_fijas']['solo_mostrar']:
            output_frame = frame
        else:
            output_frame = detect(frame, model, procesamiento['var']['selected_classes'], tareas)
            if (i != 0) and (i % int(fps * segundo_entre_registros) == 0):
                df = guardar_xlsx_contador(df, tareas.objeto_Contadores.contadores[0], procesamiento['var']['texto_contador'], procesamiento['info']['hora'], j*segundo_entre_registros)
                j += 1
            if i % int(fps * segundos_reinicio_contador) == 0:
                df.to_csv(path_archivo, index=False)
                tareas.objeto_Contadores.contadores[0].reset()
        i += 1
        #output_frame=frame

        # Display the frame with detections
        #if guardar_video_resultado:
            #video_writer.write(output_frame)
            #if (i-1) % 25 == 0:
                #cv2.imwrite(dir_resultado[:-4] + '_' + str((i-1)//25) + '.jpg', frame)
        if procesamiento['var_fijas']['mostrar_video']:
            cv2.imshow('Camara Paseo Estacion con analitica', output_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            df.to_csv(path_archivo, index=False)
            #df.to_csv(r'C:\Users\eitan\Pictures\comercio_ambulante_paseo_estacion_indicadores_transito_peatonal_cruz_verde.csv', index=False)
            #df.to_csv(r'C:\Users\admin\Desktop\archivo_generado\paseo_estacion_indicadores_transito_peatonal_cruz_verde' + momento + '.csv', index=False)
            break

def guardar_xlsx_contador(df, contador, texto_contador, hora_orig, tpo):
    hora = datetime.datetime.strptime(hora_orig, '%H_%M_%S').time()
    hora_cont = (datetime.datetime.combine(datetime.date.today(), hora) + datetime.timedelta(seconds=tpo)).time()
    flujo1 = contador.in_count
    flujo2 = contador.out_count
    nueva_fila = {'Hora Conteo':hora_cont, texto_contador[0]:flujo1, texto_contador[1]:flujo2}
    df = pd.concat([df, pd.DataFrame(nueva_fila, index=[0])], ignore_index=True)
    return df