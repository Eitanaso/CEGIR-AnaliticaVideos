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
        if tareas.estacionados:
            annotated_frame = tareas.objeto_Estacionados.anotar_frame(annotated_frame, detections, model)
        if tareas.contadores:
            annotated_frame = tareas.objeto_Contadores.anotar_frame(annotated_frame, detections, model)
        if tareas.trayectorias:
            annotated_frame = tareas.objeto_Trayectorias.anotar_frame(annotated_frame, detections, model)
        if tareas.velocidades:
            if not tareas.velocidad_por_zonas:
                annotated_frame = tareas.objeto_Velocidades.anotar_frame(annotated_frame, detections, model)
            else:
                annotated_frame = tareas.objeto_Velocidades.anotar_frame_zonas(annotated_frame, detections, model)

    return  annotated_frame



def run_detect(cap, model, clases, fps, procesamiento, tiempos=[], i=0, mostrar_video=True, guardar_video_resultado=False, dir_resultado=''):

    #p1 = threading.Thread(target=Receive(cap))
    #p2 = threading.Thread(target=Display(procesamiento, fps, model, clases))
    #p1.start()
    #p2.start()

    ret, frame = cap.read()
    frame = frame[60:-60, 240:-240]
    frame = cv2.resize(frame, (720, 480))
    segundo_entre_registros = 5 * 60
    segundos_reinicio_contador = 30 * 60
    columnas_indicador = {'id_camara':[], 'calles_camara':[], 'fecha':[], 'hora_inicio':[], 'hora_final':[], 'flujo_personas_oeste_este':[], 'flujo_personas_este_oeste':[]}
    df=pd.DataFrame(columnas_indicador)
    momento = datetime.datetime.now()
    momento = f'{momento.month}_{momento.day}_{momento.hour}_{momento.minute}'
    if guardar_video_resultado:
        video_writer = cv2.VideoWriter(dir_resultado, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame.shape[1], frame.shape[0]))
    
    if not procesamiento['solo_mostrar']:
        tareas = Objeto_Global(fps)
        tareas.create_byte_tracker()
        if procesamiento['solo_detector']:
            tareas.create_detector()
        if procesamiento['mostrar_estacionados']:
            tareas.create_estacionados(frame, procesamiento['zonas_estacionados'], procesamiento['centros_zonas_estacionados'])
        if procesamiento['mostrar_contadores']:
            tareas.create_contadores(procesamiento['lineas_contadores'])#, procesamiento['guardar_archivo_contador'])
        if procesamiento['mostrar_trayectorias']:
            tareas.create_trayectorias(frame, procesamiento['guardar_videos_evento'])
        if procesamiento['mostrar_velocidades']:
            tareas.create_velocidades(frame, procesamiento['velocidades_por_zonas'], procesamiento['zonas_velocidades'], procesamiento['min_max_zonas'], procesamiento['guardar_videos_evento'])

    while cap.isOpened():
    #while True:
        ret, frame = cap.read()
        if not ret:
            break
            #cap = cv2.VideoCapture(r'rtsp://admin:Cafa2414$@10.0.10.182:554/0/profile2/media.smp')
            #ret, frame = cap.read()
        # Perform detection
        frame = frame[60:-60, 240:-240]
        frame = cv2.resize(frame, (720, 480))
        ti = time.time()
        if procesamiento['solo_mostrar']:
            output_frame = frame
        else:
            output_frame = detect(frame, model, clases, tareas)
            if procesamiento['guardar_archivo_contador']:
                if i % int(fps * segundo_entre_registros) == 0:
                    df = guardar_xlsx_contador(df, tareas.objeto_Contadores.contadores[0])
                if i % int(fps * segundos_reinicio_contador) == 0:
                    #df.to_csv(r'C:\Users\eitan\Pictures\comercio_ambulante_paseo_estacion_indicadores_transito_peatonal_cruz_verde.csv', index=False)
                    df.to_csv(r'C:\Users\admin\Desktop\archivo_generado\paseo_estacion_indicadores_transito_peatonal_cruz_verde' + momento + '.csv', index=False)
                    tareas.objeto_Contadores.contadores[0].reset()
        tiempos.append((time.time() - ti)*1000)
        i += 1
        #output_frame=frame

        # Display the frame with detections
        if guardar_video_resultado:
            video_writer.write(output_frame)
            #if (i-1) % 25 == 0:
                #cv2.imwrite(dir_resultado[:-4] + '_' + str((i-1)//25) + '.jpg', frame)
        if mostrar_video:
            cv2.imshow('Camara Paseo Estacion con analitica', output_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            #df.to_csv(r'C:\Users\eitan\Pictures\comercio_ambulante_paseo_estacion_indicadores_transito_peatonal_cruz_verde.csv', index=False)
            df.to_csv(r'C:\Users\admin\Desktop\archivo_generado\paseo_estacion_indicadores_transito_peatonal_cruz_verde' + momento + '.csv', index=False)
            break

def guardar_xlsx_contador(df, contador):
    id_camara = '1'
    calles_camara = 'paseo_estacion_cruz_verde'
    fecha_hora = datetime.datetime.now()
    fecha= f'{fecha_hora.year}_{fecha_hora.month}_{fecha_hora.day}'
    hora_inicio= f'{fecha_hora.hour}_{fecha_hora.minute}_{fecha_hora.second}'
    hora_final = '-'
    flujo_personas_oeste_este = contador.in_count
    flujo_personas_este_oeste = contador.out_count
    nueva_fila = {'id_camara':id_camara, 'calles_camara':calles_camara, 'fecha':fecha, 'hora_inicio':hora_inicio, 'hora_final':hora_final, 'flujo_personas_oeste_este':flujo_personas_oeste_este, 'flujo_personas_este_oeste':flujo_personas_este_oeste}
    df = pd.concat([df, pd.DataFrame(nueva_fila, index=[0])], ignore_index=True)
    return df