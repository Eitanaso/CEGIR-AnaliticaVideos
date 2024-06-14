import argparse
from detectar_ciclistas import detect
from general import get_video, get_model
from clases.objeto_global import Objeto_Global

from datetime import datetime
import time
import numpy as np

import json

from PIL import Image
import pyscreenshot as ImageGrab

import pandas as pd

import cv2

import tkinter as tk

import ssl
import random
import json
import time
import uuid
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from datetime import date, datetime
import pytz
import boto3

import re

#SOURCE_VIDEO_PATH = 'c:\\Users\\Analitica2\\Desktop\\test\\comercio_ambulante_paseo_estacion.mp4'
#rtsp_url = SOURCE_VIDEO_PATH
#MODEL = "yolo_4158imgs_augment_30brillo.pt"
MODEL = 'yolov8x.pt'
selected_classes = 1
segs_frame = 5
#fps = 25

global user_inputs
user_inputs = []


# conectar a cuenta con permiso de escritura para mandar datos al bucket s3 (acces key y secret acces key)
# descargar aws CLI
# en el cmd escribir: aws configure y rellenar como es debido (region us-east-1 y formato nada)

s3 = boto3.client('s3')
#ingresar bucket correcto
bucket = 'camare-iot-997128247840'


tz = pytz.timezone('America/Santiago') #America/Mexico_City , #America/Bogota

#CLIENT_NAME = "sensor-pruebas"
#ingresar nombre de cliente correcto
CLIENT_NAME = "sensor"
#global TOPIC
#TOPIC = "iot-sensor/device-mx/001" # 001 -> IDcam-subID-comuna-calle1-calle2 (quitar caracteres especiales)
#TOPIC = "iot-sensor/device-mx/"
TOPIC = "iot-sensorps/device-mxps/001"
PHAT = "D:\\analitica_camara_CEGIR\\cer-prod\\"

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

    #print('3', user_inputs)

    if info_obligatoria:
        window.destroy()
    else:
        user_inputs = []
        print('-------------------------------------------------------------')

window = tk.Tk()
label = tk.Label(window, text='Datos utiles')
label.pack()

label = tk.Label(window, text='ID camara:')
label.pack()
entry_ID = tk.Entry(window)
entry_ID.pack()

label = tk.Label(window, text='Sub ID camara:')
label.pack()
entry_subID = tk.Entry(window)
entry_subID.pack()

label = tk.Label(window, text='Nombre calle 1:')
label.pack()
entry_calle1 = tk.Entry(window)
entry_calle1.pack()

label = tk.Label(window, text='Nombre calle 2:')
label.pack()
entry_calle2 = tk.Entry(window)
entry_calle2.pack()

label = tk.Label(window, text='Comuna:')
label.pack()
entry_comuna = tk.Entry(window)
entry_comuna.pack()

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

close_button = tk.Button(window, text='Close', command=get_user_input)
close_button.pack()

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

centros_zonas = [(50, 30)]

def main(model, i=0):
    # datetime object containing current date and time
    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("inicio =", dt_string)

    #cap = get_video(rstp_url)
    model_name = model
    model = get_model(model)
    #_, output_frame = cap.read()
    starttime = time.monotonic()
    print(starttime)
    global img
    img = ImageGrab.grab()
    img = np.asarray(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imshow('Seleccion de 2 puntos de camara', img)
    global puntos
    puntos = []
    cv2.setMouseCallback('Seleccion de 2 puntos de camara', click_event)
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    print(puntos)
    bbox = (puntos[0][0], puntos[0][1],puntos[1][0],puntos[1][1])
    #while cap.isOpened():
    df=pd.DataFrame({'Hora Deteccion':[], 'Cantidad Detectado':[]})
    
    window.mainloop()

    frame = ImageGrab.grab(bbox=bbox)
    frame = np.asarray(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow('Seleccion de zona de deteccion', frame)
    puntos = []
    cv2.setMouseCallback('Seleccion de zona de deteccion', click_event)
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    print(puntos)
    zonas = [puntos]
    #print(user_inputs)
    prev_det = 0
    while True:
        #ret, frame = cap.read()
        #bbox = (100, 100, 700, 800)
        frame = ImageGrab.grab(bbox=bbox)
        frame = np.asarray(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #if not ret:
            #break
        #if i % int(fps * segs_frame) == 0:
        output_frame, dets = detect(frame, model, selected_classes, zonas, centros_zonas)
        #print(output_frame.shape)
        #print(user_inputs)
        #print(len(dets))
        cv2.imshow('Detecciones', output_frame)
        if (len(dets) > 0):
            momento = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            datetime_local = datetime.now(tz)
            cv2.imwrite(f'D:\\analitica_camara_CEGIR\\datos_ciclistas_vereda\\{momento}_{user_inputs[0]}_{user_inputs[1]}_{user_inputs[2]}_{user_inputs[3]}_{user_inputs[4]}.jpg', output_frame)
            datos = {
			"type": "GS","id": str(uuid.uuid4()), 'region': 'Metropolitana de Santiago', 'Provincia': 'Santiago',
            'id_camara': user_inputs[0], 'sub_id_camara': user_inputs[1], 'comuna': user_inputs[2],
            'nombre_calle1': user_inputs[3], 'nombre_calle2': user_inputs[4],
                      'direccion_cardinal_enfoque_camara': user_inputs[5], 'marca_camara': user_inputs[6],
                     'modelo': user_inputs[7], 'resolucion_screenshot': output_frame.shape,
                #'dia': momento.split(' ')[0], 'hora_min_seg': momento.split(' ')[1], 
			    "date": datetime_local.strftime("%Y-%m-%d %H:%M:%S"),
			    "timestamp": int(time.time()),
                'modelo_detector': model_name,
                'ciclistas_vereda': len(dets),
                'nombre_imagen': f'{momento}_{user_inputs[0]}_{user_inputs[1]}_{user_inputs[2]}_{user_inputs[3]}_{user_inputs[4]}.jpg',
                }
            #IoTclient.publish(TOPIC, create_payload(datos), 0)
            with open(f'D:\\analitica_camara_CEGIR\\datos_ciclistas_vereda\\{momento}_{user_inputs[0]}_{user_inputs[1]}_{user_inputs[2]}_{user_inputs[3]}_{user_inputs[4]}.json', 'w') as f:
                json.dump(datos, f)
            file_name = f'D:\\analitica_camara_CEGIR\\datos_ciclistas_vereda\\{momento}_{user_inputs[0]}_{user_inputs[1]}_{user_inputs[2]}_{user_inputs[3]}_{user_inputs[4]}.jpg'
            key_name = f'{momento}_{user_inputs[0]}_{user_inputs[1]}_{user_inputs[2]}_{user_inputs[3]}_{user_inputs[4]}.jpg'
            #s3.upload_file(file_name, bucket, key_name)
        prev_det = len(dets)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        nueva_fila = {'Hora Deteccion':dt_string, 'Cantidad Detectado':len(dets)}
        df = pd.concat([df, pd.DataFrame(nueva_fila, index=[0])], ignore_index=True)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        i += 1
        time.sleep(segs_frame)# - ((time.monotonic() - starttime) % 60.0))

    #df.to_csv('C:\\Users\\Analitica2\\Desktop\\codigo_funcional\\graffitis.csv', index=False)

    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("fin =", dt_string)

if __name__ == '__main__':

    main(MODEL)