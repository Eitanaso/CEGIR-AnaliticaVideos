import argparse
from detectar_personas import detect
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

#SOURCE_VIDEO_PATH = 'c:\\Users\\Analitica2\\Desktop\\test\\comercio_ambulante_paseo_estacion.mp4'
#rtsp_url = SOURCE_VIDEO_PATH
#MODEL = "yolo_4158imgs_augment_30brillo.pt"
MODEL = 'yolov8x.pt'
selected_classes = 0
segs_frame = 10
#fps = 25

user_inputs = []


# conectar a cuenta con permiso de escritura para mandar datos al bucket s3 (acces key y secret acces key)
# descargar aws CLI
# en el cmd escribir: aws configure y rellenar como es debido (region us-east-1 y formato nada)

s3 = boto3.client('s3')
bucket = 'camare-iot-120474950462'


tz = pytz.timezone('America/Santiago') #America/Mexico_City , #America/Bogota

CLIENT_NAME = "sensor-pruebas"
TOPIC = "iot-sensor/device-mx/001"
PHAT = "D:\\analitica_camara_CEGIR\\cer\\"

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
    user_input = entry_ID.get()
    user_inputs.append(user_input)
    user_input = entry_subID.get()
    user_inputs.append(user_input)
    user_input = entry_calle1.get()
    user_inputs.append(user_input)
    user_input = entry_calle2.get()
    user_inputs.append(user_input)
    user_input = entry_comuna.get()
    user_inputs.append(user_input)
    user_input = entry_enfoque.get()
    user_inputs.append(user_input)
    user_input = entry_marca.get()
    user_inputs.append(user_input)
    user_input = entry_modelo.get()
    user_inputs.append(user_input)
    window.destroy()

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
    
    window.mainloop()

    frame = ImageGrab.grab(bbox=bbox)
    frame = np.asarray(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow('frame', frame)
    puntos = []
    cv2.setMouseCallback('frame', click_event)
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
        cv2.imshow('Camara Paseo Estacion con analitica', output_frame)
        momento = datetime.now().strftime("%d_%m_%Y %H_%M_%S")
        datetime_local = datetime.now(tz)
        cv2.imwrite(f'D:\\analitica_camara_CEGIR\\datos_personas_cruce\\{momento}.jpg', output_frame)
        datos = {
			"type": "GS",
            'id_camara': user_inputs[0], 'sub_id_camara': user_inputs[1], 'nombre_calle1': user_inputs[2], 'nombre_calle2': user_inputs[3],
                     'comuna': user_inputs[4], 'direccion_cardinal_enfoque_camara': user_inputs[5], 'marca_camara': user_inputs[6],
                     'modelo': user_inputs[7], 'resolucion_screenshot': output_frame.shape,
                #'dia': momento.split(' ')[0], 'hora_min_seg': momento.split(' ')[1], 
			    "date": datetime_local.strftime("%Y-%m-%d %H:%M:%S"),
			    "timestamp": int(time.time()),
                'modelo_detector': model_name,
                'personas_cruce': len(dets),
                'nombre_imagen': f'{momento}.jpg',
                }
        #IoTclient.publish(TOPIC, create_payload(datos), 0)
        with open(f'D:\\analitica_camara_CEGIR\\datos_personas_cruce\\{momento}.json', 'w') as f:
            json.dump(datos, f)
        file_name = f'D:\\analitica_camara_CEGIR\\datos_personas_cruce\\{momento}.jpg'
        key_name = f'{momento}.jpg'
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