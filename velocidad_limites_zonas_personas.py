import cv2
from ultralytics import YOLO
import supervision as sv
import numpy as np
import time
from funciones.general import *
from funciones.velocidades import *

from datetime import datetime, timedelta
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

#--------------------------------------------------------------------------------------------------------------------
# Codigo encargado de mostrar las velocidades de las personas que corren o estan detenidas (Falta generalizarlo y crear una clase para funcionar en main)
# Codigo modificado de un tutorial de Supervision y de un codigo para la conexion de camaras de Luis Escares
# Por mayores dudas de las funciones, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
#--------------------------------------------------------------------------------------------------------------------

MODEL = "yolov8x.pt"
# Load YOLOv8 model
model = YOLO(MODEL)
model.fuse()
#selected_classes = [0,1,2,5]
selected_classes = [0]
#print(model.model.names)

#----------------------------------------------------------

# Connect to RTSP stream
#rtsp_url = r'rtsp://admin:Cafa2414$@10.0.10.182:554/0/profile2/media.smp'
#---------------------- Ubicacion del video a analizar ------------------------------#
SOURCE_VIDEO_PATH = r'C:\\CEGIR-AnaliticaVideos-new_main\\comercio_ambulante_paseo_estacion.mp4'
#------------------------------------------------------------------------------------#
rtsp_url = SOURCE_VIDEO_PATH
#TARGET_VIDEO_PATH = r'C:\\CEGIR-AnaliticaVideos-new_main\comercio_ambulante_detectado.mp4'
cap = cv2.VideoCapture(rtsp_url)
#cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)

#------------------------------------------------------------------
# create VideoInfo instance
#video_info = sv.VideoInfo.from_video_path(SOURCE_VIDEO_PATH)
fps=25
# create BYTETracker instance
byte_tracker = sv.ByteTrack(track_thresh=0.15, track_buffer=fps*2, match_thresh=0.8, frame_rate=fps)

#box_annotator1 = sv.BoxAnnotator(color=sv.Color(r=0, g=255, b=0), text_color=sv.Color.white(), thickness=1, text_thickness=1, text_scale=0.5)
box_annotator2 = sv.BoxAnnotator(color=sv.Color(r=255, g=0, b=0), text_color=sv.Color.white(), thickness=1, text_thickness=1, text_scale=0.5)
#box_annotator3 = sv.BoxAnnotator(color=sv.Color(r=0, g=0, b=255), text_color=sv.Color.white(), thickness=1, text_thickness=1, text_scale=0.5)

#------------------------------------------------------------------
i = 0
anteriores = {}
ult_mov_x = {}
ult_mov_y = {}
calc_centro = 'centro-sup'
ult_vel = {}
ults_vel = {}
tpo_calc_vel = 0.5
#sup1 = 10
#inf1 = 0
sup2 = 30
inf2 = 0
#sup3 = 10
#inf3 = 0

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

    if entry_vinf.get():
        #if str(user_input).isdigit():
        user_input = entry_vinf.get()
        #else:
           #info_obligatoria = False
           #print('Numero invalido, debe ser entero, recomendado 0')
           #entry_vinf.focus_set()
        user_inputs.append(user_input)
    else:
        info_obligatoria = False
        print('Falta velocidad inferior de Camara')
        entry_vinf.focus_set()

    if entry_vsup.get():
        #if str(user_input).isdigit():
        user_input = entry_vsup.get()
        #else:
           #info_obligatoria = False
           #print('Numero invalido, debe ser entero, recomendado 100')
           #entry_vsup.focus_set()
        user_inputs.append(user_input)
    else:
        info_obligatoria = False
        print('Falta velocidad inferior de Camara')
        entry_vsup.focus_set()

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

label = tk.Label(window, text='Velocidad Inferior de zona (obligatorio, recomendado 0):') #obligatorio
label.pack()
entry_vinf = tk.Entry(window)
entry_vinf.pack()

label = tk.Label(window, text='Velocidad Superior de zona (obligatorio, recomendado 100):') #obligatorio
label.pack()
entry_vsup = tk.Entry(window)
entry_vsup.pack()

label = tk.Label(window, text='Fecha y hora de video (Obligatorio, en formato YYYY/MM/DD HH:MM:SS):') #obligatorio
label.pack()
entry_fecha_vid = tk.Entry(window)
entry_fecha_vid.pack()

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

# Function to perform YOLOv8 detection
def detect(frame):
    #----------------Variables globales importantes-----------
    global i
    global anteriores
    global ult_mov_x
    global ult_mov_y
    global calc_centro
    global ult_vel
    global ults_vel
    global tpo_calc_vel
    #global sup1
    #global inf1
    global sup2
    global inf2
    #global sup3
    #global inf3
    #----------------------------------------------------------
    results = model(frame, verbose=False)[0]
    detections = sv.Detections.from_ultralytics(results)
    # only consider class id from selected_classes define above
    detections = detections[np.isin(detections.class_id, selected_classes)]
    # tracking detections
    detections = byte_tracker.update_with_detections(detections)

    #-------------------------------Velocidad de detecciones---------------

    anteriores = guardar_centros_anteriores_v3(anteriores, detections.tracker_id, detections.xyxy, ult_mov_x, ult_mov_y, fps, def_centro=calc_centro)

    if len(ult_vel) == 0:
      for key in anteriores.keys():
        ult_vel[key] = 0
        ult_mov_x[key] = 0
        ult_mov_y[key] = 0
        ults_vel[key] = [0]

    for key in anteriores.keys():
      ult_vel[key] = velocidad(ult_vel, key, anteriores, fps, tpo_calc_vel)
      ult_mov_x[key] = velocidad(ult_mov_x, key, anteriores, fps, tpo_calc_vel, 'x')
      ult_mov_y[key] = velocidad(ult_mov_y, key, anteriores, fps, tpo_calc_vel, 'y')
      try:
        ults_vel[key].append(velocidadv2(ults_vel, key, anteriores, fps, 0.3))
      except:
        ults_vel[key] = [0]

    #try: detections1 = detections[isin_polygon(detections.xyxy, polygon_zone_annotator1.zone.mask)]
    #except: detections1 = detections
    try: detections2 = detections[isin_polygon(detections.xyxy, polygon_zone_annotator2.zone.mask)]
    except: detections2 = detections
    #try: detections3 = detections[isin_polygon(detections.xyxy, polygon_zone_annotator3.zone.mask)]
    #except: detections3 = detections

    #try:
      #print(isnot_zero_start(detections1.tracker_id, ult_vel, anteriores, video_info.fps, tpo_calc_vel))
      #detections1 = detections1[isnot_zero_start(detections1.tracker_id, ult_vel, anteriores, fps, tpo_calc_vel)]
    #except: None
    try:
      #print(isnot_zero_start(detections1.tracker_id, ult_vel, anteriores, video_info.fps, tpo_calc_vel))
      detections2 = detections2[isnot_zero_start(detections2.tracker_id, ult_vel, anteriores, fps, tpo_calc_vel)]
    except: None
    #try:
      #print(isnot_zero_start(detections1.tracker_id, ult_vel, anteriores, video_info.fps, tpo_calc_vel))
      #detections3 = detections3[isnot_zero_start(detections3.tracker_id, ult_vel, anteriores, fps, tpo_calc_vel)]
    #except: None

    #try:
      #print(isbetween_sup_inf(detections1.tracker_id, ult_vel, sup1, inf1))
      #detections1 = detections1[isbetween_sup_inf(detections1.tracker_id, ult_vel, sup1, inf1)]
      #detections1 = detections1[isbetween_sup_infv3(detections1.tracker_id, ult_vel, sup1, inf1, ults_vel, detections.tracker_id)]
    #except: None
    try:
      #print(isbetween_sup_inf(detections1.tracker_id, ult_vel, sup1, inf1))
      detections2 = detections2[isbetween_sup_inf(detections2.tracker_id, ult_vel, sup2, inf2)]
      #detections2 = detections2[isbetween_sup_infv3(detections2.tracker_id, ult_vel, sup2, inf2, ults_vel, detections.tracker_id)]
    except: None
    #try:
      #print(isbetween_sup_inf(detections1.tracker_id, ult_vel, sup1, inf1))
      #detections3 = detections3[isbetween_sup_inf(detections3.tracker_id, ult_vel, sup3, inf3)]
      #detections3 = detections3[isbetween_sup_infv3(detections3.tracker_id, ult_vel, sup3, inf3, ults_vel, detections.tracker_id)]
    #except: None
    #----------------------------------------------------------------------

    #labels1 = []
    #for bbox, _, confidence, class_id, tracker_id in detections1:
        #labels1.append(f"{ult_vel[tracker_id]:0.2f} p/s")
    labels2 = []
    for bbox, _, confidence, class_id, tracker_id in detections2:
        labels2.append(f"{ult_vel[tracker_id]:0.2f} p/s")
    #labels3 = []
    #for bbox, _, confidence, class_id, tracker_id in detections3:
        #labels3.append(f"{ult_vel[tracker_id]:0.2f} p/s")

    annotated_frame = frame.copy()

    #annotated_frame=box_annotator1.annotate(
        #scene=annotated_frame,
        #detections=detections1,
        #labels=labels1, skip_label=False
        #)

    #for id in detections1.tracker_id:
      #centros = anteriores[id]
      #if len(centros) > 1:
        #if len(centros) < 2 * fps:
          #for j in range(1, len(centros)):
            #annotated_frame = sv.draw_line(annotated_frame, sv.Point(centros[j - 1][0], centros[j - 1][1]), sv.Point(centros[j][0], centros[j][1]), sv.Color(r=0, g=255, b=0), 2)
        #else:
          #for j in range(len(centros) - 2 * fps + 1, len(centros)):
            #annotated_frame = sv.draw_line(annotated_frame, sv.Point(centros[j - 1][0], centros[j - 1][1]), sv.Point(centros[j][0], centros[j][1]), sv.Color(r=0, g=255, b=0), 2)

    annotated_frame=box_annotator2.annotate(
        scene=annotated_frame,
        detections=detections2,
        labels=labels2, skip_label=False
        )

    for id in detections2.tracker_id:
      centros = anteriores[id]
      if len(centros) > 1:
        if len(centros) < 2 * fps:
          for j in range(1, len(centros)):
            annotated_frame = sv.draw_line(annotated_frame, sv.Point(centros[j - 1][0], centros[j - 1][1]), sv.Point(centros[j][0], centros[j][1]), sv.Color(r=255, g=0, b=0), 2)
        else:
          for j in range(len(centros) - 2 * fps + 1, len(centros)):
            annotated_frame = sv.draw_line(annotated_frame, sv.Point(centros[j - 1][0], centros[j - 1][1]), sv.Point(centros[j][0], centros[j][1]), sv.Color(r=255, g=0, b=0), 2)

    #annotated_frame=box_annotator3.annotate(
        #scene=annotated_frame,
        #detections=detections3,
        #labels=labels3, skip_label=False
        #)

    #for id in detections3.tracker_id:
      #centros = anteriores[id]
      #if len(centros) > 1:
        #if len(centros) < 2 * fps:
          #for j in range(1, len(centros)):
            #annotated_frame = sv.draw_line(annotated_frame, sv.Point(centros[j - 1][0], centros[j - 1][1]), sv.Point(centros[j][0], centros[j][1]), sv.Color(r=0, g=0, b=255), 2)
        #else:
          #for j in range(len(centros) - 2 * fps + 1, len(centros)):
            #annotated_frame = sv.draw_line(annotated_frame, sv.Point(centros[j - 1][0], centros[j - 1][1]), sv.Point(centros[j][0], centros[j][1]), sv.Color(r=0, g=0, b=255), 2)

    #annotated_frame = polygon_zone_annotator1.annotate(annotated_frame, f"[{inf1}, {sup1}]")
    annotated_frame = polygon_zone_annotator2.annotate(annotated_frame, f"[{inf2}, {sup2}]")
    #annotated_frame = polygon_zone_annotator3.annotate(annotated_frame, f"[{inf3}, {sup3}]")
    return  annotated_frame, detections2

tiempos = []
ret, frame = cap.read()
#polygon_zone1 = sv.PolygonZone(np.array(
    #[(18, 213), (120, 322), (471, 193), (377, 128)]
    #), frame_resolution_wh=(frame.shape[1], frame.shape[0]), 
#triggering_position=sv.Position.CENTER)
#print(frame)
#print(frame.shape)
img = frame.copy()
#img = np.asarray(img)
#img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
cv2.imshow('Seleccion de poligono velocidades', img)
global puntos
puntos = []
cv2.setMouseCallback('Seleccion de poligono velocidades', click_event)
while True:
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
cv2.destroyAllWindows()
print(puntos)

polygon_zone2 = sv.PolygonZone(np.array(
    puntos #[(120, 322), (293, 434), (607, 219), (471, 193)]
    ), frame_resolution_wh=(frame.shape[1], frame.shape[0]), 
triggering_position=sv.Position.CENTER)

window.mainloop()

#polygon_zone3 = sv.PolygonZone(np.array(
    #[(293, 434), (359, 480), (720, 480), (720, 208), (607, 219)]
    #), frame_resolution_wh=(frame.shape[1], frame.shape[0]), 
#triggering_position=sv.Position.CENTER)


#polygon_zone_annotator1 = sv.PolygonZoneAnnotator(thickness=1, text_thickness=1, text_scale=0.5, zone=polygon_zone1, color=sv.Color(r=0, g=255, b=0), text_color=sv.Color.white(), text_padding=2, )#, center=(140, 310))
#polygon_zone_annotator1.center = sv.Point(376, 133)
polygon_zone_annotator2 = sv.PolygonZoneAnnotator(thickness=1, text_thickness=1, text_scale=0.5, zone=polygon_zone2, color=sv.Color(r=255, g=0, b=0), text_color=sv.Color.white(), text_padding=2, )#, center=(140, 310))
polygon_zone_annotator2.center = sv.Point(50, 30)#(470, 198)
#polygon_zone_annotator3 = sv.PolygonZoneAnnotator(thickness=1, text_thickness=1, text_scale=0.5, zone=polygon_zone3, color=sv.Color(r=0, g=0, b=255), text_color=sv.Color.white(), text_padding=2, )#, center=(140, 310))
#polygon_zone_annotator3.center = sv.Point(606, 224)
#cv2.imwrite(r"C:\Users\eitan\Pictures\frame_prueba.png",frame)

sup2 = int(user_inputs[9])
inf2 = int(user_inputs[8])

now = datetime.now()

# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("inicio =", dt_string)
while cap.isOpened():
    ret, frame = cap.read()
    #frame = cv2.resize(frame, (640, 640))
    if not ret:
        break
    # Perform detection
    ti = time.time()
    output_frame, dets = detect(frame)
    tiempos.append((time.time() - ti)*1000)
    i += 1
    #output_frame=frame

    # Display the frame with detections
    cv2.imshow('Detecciones', output_frame)
    if len(dets):
       momento = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
       datetime_local = datetime.now(tz)
       #diff = datetime.strptime(momento, "%Y_%m_%d_%H_%M_%S")-now
       #print(diff)
       #print(datetime.strptime(user_inputs[10], "%Y/%m/%d %H:%M:%S") + diff)
       #momento = datetime.strptime(user_inputs[10], "%Y/%m/%d %H:%M:%S") + diff
       momento = (datetime.strptime(user_inputs[10], "%Y/%m/%d %H:%M:%S") + timedelta(seconds=(i//fps)))#.time()
       #momento = pd.to_datetime(momento, format='%Y_%m_%d_%H_%M_%S')
       momento = momento.strftime("%Y_%m_%d_%H_%M_%S")
       cv2.imwrite(f'C:\\CEGIR-AnaliticaVideos-new_main\\datos_velocidades\\{momento}_{user_inputs[0]}_{user_inputs[1]}_{user_inputs[2]}_{user_inputs[3]}_{user_inputs[4]}.jpg', output_frame)
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
                'modelo_detector': MODEL,
                'velocidad_detectada': 1, 'cantidad_detectada': len(dets),
                'nombre_imagen': f'{momento}_{user_inputs[0]}_{user_inputs[1]}_{user_inputs[2]}_{user_inputs[3]}_{user_inputs[4]}.jpg', #quitar caracteres especiales
                }
       #IoTclient.publish(TOPIC, create_payload(datos), 0)
       with open(f'C:\\CEGIR-AnaliticaVideos-new_main\\datos_velocidades\\{momento}_{user_inputs[0]}_{user_inputs[1]}_{user_inputs[2]}_{user_inputs[3]}_{user_inputs[4]}.json', 'w') as f:
          json.dump(datos, f) 
       file_name = f'C:\\CEGIR-AnaliticaVideos-new_main\\datos_velocidades\\{momento}_{user_inputs[0]}_{user_inputs[1]}_{user_inputs[2]}_{user_inputs[3]}_{user_inputs[4]}.jpg'
       key_name = f'{momento}_{user_inputs[0]}_{user_inputs[1]}_{user_inputs[2]}_{user_inputs[3]}_{user_inputs[4]}.jpg'
       #s3.upload_file(file_name, bucket, key_name)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print(np.sum(tiempos)/len(tiempos))
cap.release()
cv2.destroyAllWindows()