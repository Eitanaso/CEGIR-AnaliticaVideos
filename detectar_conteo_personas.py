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
#import datetime as datetime

import tkinter as tk

import ssl
import random
import json
import time
import uuid
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from datetime import date, datetime, timedelta
import pytz
import boto3

import re



#--------------------------------------------------------------------------------------------------------------------
# Creacion de funciones para iniciar el procesamiento segun lo solicitado
# Funciones creadas a partir de código de la libreria Supervision y de codigo para la conexion a camaras y guardado de archivos de Luis Escares
# Por mayores dudas de las funciones, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
#--------------------------------------------------------------------------------------------------------------------

global user_inputs
user_inputs = []

# conectar a cuenta con permiso de escritura para mandar datos al bucket s3 (acces key y secret acces key)
# descargar aws CLI
# en el cmd escribir: aws configure y rellenar como es debido (region us-east-1 y formato nada)

s3 = boto3.client('s3')
#bucket = 'camare-iot-120474950462'
bucket = 'camare-iot-997128247840'

tz = pytz.timezone('America/Santiago') #America/Mexico_City , #America/Bogota

#CLIENT_NAME = "sensor-pruebas"
CLIENT_NAME = "sensor"
#global TOPIC
#TOPIC = "iot-sensor/device-mx/001" # 001 -> IDcam-subID-comuna-calle1-calle2 (quitar caracteres especiales)
#TOPIC = "iot-sensor/device-mx/"
TOPIC = "iot-sensorps/device-mxps/001"
PHAT = "C:\\CEGIR-AnaliticaVideos-new_main\\cer-prod\\"

BROKER_PATH = "a1htxdpw7uo3bd-ats.iot.us-east-1.amazonaws.com"
ROOT_CA_PATH = PHAT+'AmazonRootCA1.pem'

PRIVATE_KEY_PATH = PHAT+'private.pem.key'
CERTIFICATE_PATH = PHAT+'certificate.pem.crt'

# Create and Configure the IoT Client
IoTclient = AWSIoTMQTTClient(CLIENT_NAME)
IoTclient.configureEndpoint(BROKER_PATH, 8883)
print(ROOT_CA_PATH)
IoTclient.configureCredentials(ROOT_CA_PATH, PRIVATE_KEY_PATH, CERTIFICATE_PATH)

# Allow the device to queue infinite messages
IoTclient.configureOfflinePublishQueueing(-1)
# Number of messages to send after a connection returns
IoTclient.configureDrainingFrequency(2)  # 2 requests/second
# How long to wait for a [dis]connection to complete (in seconds)
IoTclient.configureConnectDisconnectTimeout(10)
# How long to wait for publish/[un]subscribe (in seconds)
IoTclient.configureMQTTOperationTimeout(5) 

IoTclient.connect()
IoTclient.publish(TOPIC, "connected", 0)

# Create and Send Payloads to the IoT Topic
def create_payload(datos):
	
	


	#pesoNeto=round(random.uniform(50, 200), 2)
	#pesoSeco=pesoNeto-(pesoNeto*0.15)

	payload = json.dumps(datos)
	print(payload)
	return payload



def get_user_input():
    info_obligatoria = True
    #print('2', user_inputs)
    #user_inputs = []
    #print('2', user_inputs)

    global user_inputs

    if entry_ID.get():
        user_input = entry_ID.get()
        user_inputs.append(re.sub('[^A-Za-z0-9]+', '', user_input))
    else:
        info_obligatoria = False
        print('Falta ID de Camara')
        entry_ID.focus_set()

    if entry_subID.get():
        user_input = entry_subID.get()
        user_inputs.append(re.sub('[^A-Za-z0-9]+', '', user_input))
    else:
        info_obligatoria = False
        print('Falta sub ID de Camara')
        entry_ID.focus_set()

    if entry_comuna.get():
        user_input = entry_comuna.get()
        user_inputs.append(re.sub('[^A-Za-z0-9]+', '', user_input))
    else:
        info_obligatoria = False
        print('Falta comuna de Camara')
        entry_ID.focus_set()

    if entry_calle1.get():
        user_input = entry_calle1.get()
        user_inputs.append(re.sub('[^A-Za-z0-9]+', '', user_input))
    else:
        info_obligatoria = False
        print('Falta calle 1 de Camara')
        entry_ID.focus_set()

    if entry_calle2.get():
        user_input = entry_calle2.get()
        user_inputs.append(re.sub('[^A-Za-z0-9]+', '', user_input))
    else:
        info_obligatoria = False
        print('Falta calle 2 de Camara')
        entry_ID.focus_set()

    user_input = entry_enfoque.get()
    user_inputs.append(re.sub('[^A-Za-z0-9]+', '', user_input))

    user_input = entry_marca.get()
    user_inputs.append(re.sub('[^A-Za-z0-9]+', '', user_input))

    user_input = entry_modelo.get()
    user_inputs.append(re.sub('[^A-Za-z0-9]+', '', user_input))

    if entry_fecha_vid.get():
        #if str(user_input).isdigit():
        user_input = entry_fecha_vid.get()
        #else:
           #info_obligatoria = False
           #print('Numero invalido, debe ser entero, recomendado 100')
           #entry_vsup.focus_set()
        user_inputs.append(user_input)
    else:
        info_obligatoria = False
        print('Falta fecha y hora del video')
        entry_fecha_vid.focus_set()

    if entry_tpo.get():
        #if str(user_input).isdigit():
        user_input = entry_tpo.get()
        #else:
           #info_obligatoria = False
           #print('Numero invalido, debe ser entero, recomendado 100')
           #entry_vsup.focus_set()
        user_inputs.append(user_input)
    else:
        info_obligatoria = False
        print('Falta tiempo de analisis de video')
        entry_tpo.focus_set()

    #print('3', user_inputs)

    if info_obligatoria:
        window.destroy()
    else:
        user_inputs = []
        print('-------------------------------------------------------------')

window = tk.Tk()
label = tk.Label(window, text='Datos utiles')
label.pack()

label = tk.Label(window, text='ID camara (obligatorio):') #obligatorio
label.pack()
entry_ID = tk.Entry(window)
entry_ID.pack()

label = tk.Label(window, text='Sub ID camara (obligatorio):') #obligatorio
label.pack()
entry_subID = tk.Entry(window)
entry_subID.pack()

label = tk.Label(window, text='Comuna (obligatorio):') #obligatorio
label.pack()
entry_comuna = tk.Entry(window)
entry_comuna.pack()

label = tk.Label(window, text='Nombre calle 1 (obligatorio):') #obligatorio
label.pack()
entry_calle1 = tk.Entry(window)
entry_calle1.pack()

label = tk.Label(window, text='Nombre calle 2 (obligatorio):') #obligatorio
label.pack()
entry_calle2 = tk.Entry(window)
entry_calle2.pack()

label = tk.Label(window, text='Direccion cardinal que enfoca la camara:')
label.pack()
entry_enfoque = tk.Entry(window)
entry_enfoque.pack()

label = tk.Label(window, text='Marca de camara:')
label.pack()
entry_marca = tk.Entry(window)
entry_marca.pack()

label = tk.Label(window, text='Modelo de camara:')
label.pack()
entry_modelo = tk.Entry(window)
entry_modelo.pack()

label = tk.Label(window, text='Fecha y hora de video (Obligatorio, en formato YYYY/MM/DD HH:MM:SS):') #obligatorio
label.pack()
entry_fecha_vid = tk.Entry(window)
entry_fecha_vid.pack()

label = tk.Label(window, text='Tiempo de analisis en segundos (Obligatorio):') #obligatorio
label.pack()
entry_tpo = tk.Entry(window)
entry_tpo.pack()

close_button = tk.Button(window, text='Close', command=get_user_input)
close_button.pack()

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

    window.mainloop()

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
            #if (i != 0) and (i % int(fps * segundo_entre_registros) == 0):
                #df = guardar_xlsx_contador(df, tareas.objeto_Contadores.contadores[0], procesamiento['var']['texto_contador'], procesamiento['info']['hora'], j*segundo_entre_registros)
                #j += 1
            if (i != 0) and (i % int(fps * int(user_inputs[9])) == 0):
                #df.to_csv(path_archivo, index=False)
                momento = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                datetime_local = datetime.now(tz)
                momento = (datetime.strptime(user_inputs[8], "%Y/%m/%d %H:%M:%S") + timedelta(seconds=(i//fps)))#.time()
                momento = momento.strftime("%Y_%m_%d_%H_%M_%S")
                d = procesamiento['var']['direccion_archivo']
                #cv2.imwrite(f'{d}{momento}_{user_inputs[0]}_{user_inputs[1]}_{user_inputs[2]}_{user_inputs[3]}_{user_inputs[4]}.jpg', output_frame)
                datos = {
          "type": "GS", "id": str(uuid.uuid4()), 'region': 'Metropolitana de Santiago', 'Provincia': 'Santiago',
            'id_camara': user_inputs[0], 'sub_id_camara': user_inputs[1], 'comuna': user_inputs[2], 
            'nombre_calle1': user_inputs[3], 'nombre_calle2': user_inputs[4],
                     'direccion_cardinal_enfoque_camara': user_inputs[5], 'marca_camara': user_inputs[6],
                     'modelo': user_inputs[7], 'resolucion_screenshot': output_frame.shape,
                #'dia': momento.split(' ')[0], 'hora_min_seg': momento.split(' ')[1], 
                'date_det': momento,
			    "date": datetime_local.strftime("%Y-%m-%d %H:%M:%S"),
			    "timestamp": int(time.time()),
                'modelo_detector': procesamiento['var_fijas']['model'],
                'cant_personas_inout': tareas.objeto_Contadores.contadores[0].in_count, 'cant_personas_outin': tareas.objeto_Contadores.contadores[0].out_count,
                #'nombre_imagen': f'{momento}_{user_inputs[0]}_{user_inputs[1]}_{user_inputs[2]}_{user_inputs[3]}_{user_inputs[4]}.jpg', #quitar caracteres especiales
                }
                #IoTclient.publish(TOPIC, create_payload(datos), 0)
                with open(f'{d}{momento}_{user_inputs[0]}_{user_inputs[1]}_{user_inputs[2]}_{user_inputs[3]}_{user_inputs[4]}.json', 'w') as f:
                    json.dump(datos, f) 
                #file_name = f'{d}{momento}_{user_inputs[0]}_{user_inputs[1]}_{user_inputs[2]}_{user_inputs[3]}_{user_inputs[4]}.jpg'
                #key_name = f'{momento}_{user_inputs[0]}_{user_inputs[1]}_{user_inputs[2]}_{user_inputs[3]}_{user_inputs[4]}.jpg'
                #s3.upload_file(file_name, bucket, key_name)
                tareas.objeto_Contadores.contadores[0].reset()
        i += 1
        #output_frame=frame

        # Display the frame with detections
        #if guardar_video_resultado:
            #video_writer.write(output_frame)
            #if (i-1) % 25 == 0:
                #cv2.imwrite(dir_resultado[:-4] + '_' + str((i-1)//25) + '.jpg', frame)
        if procesamiento['var_fijas']['mostrar_video']:
            cv2.imshow('Conteo', output_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            #df.to_csv(path_archivo, index=False)
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