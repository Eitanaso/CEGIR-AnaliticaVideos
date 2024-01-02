import cv2
from ultralytics import YOLO
import supervision as sv
import numpy as np
import time
from funciones.general import *
from funciones.velocidades import *

#--------------------------------------------------------------------------------------------------------------------
# Codigo encargado de mostrar las velocidades de las personas (Falta generalizarlo y crear una clase para funcionar en main)
# Codigo modificado de un tutorial de Supervision y de un codigo para la conexion de camaras de Luis Escares
# Por mayores dudas de las funciones, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
#--------------------------------------------------------------------------------------------------------------------

MODEL = "yolov8n.pt"
# Load YOLOv8 model
model = YOLO(MODEL)
model.fuse()
#selected_classes = [0,1,2,5]
selected_classes = [0]
#print(model.model.names)

#----------------------------------------------------------

# Connect to RTSP stream
#rtsp_url = r'rtsp://admin:Cafa2414$@10.0.10.182:554/0/profile2/media.smp'
SOURCE_VIDEO_PATH = r'C:\Users\eitan\Pictures\comercio_ambulante_paseo_estacion.mp4'
rtsp_url = SOURCE_VIDEO_PATH
TARGET_VIDEO_PATH = r'C:\Users\eitan\Pictures\comercio_ambulante_detectado.mp4'
cap = cv2.VideoCapture(rtsp_url)
#cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)

#------------------------------------------------------------------
# create VideoInfo instance
#video_info = sv.VideoInfo.from_video_path(SOURCE_VIDEO_PATH)
fps=25
# create BYTETracker instance
byte_tracker = sv.ByteTrack(track_thresh=0.15, track_buffer=fps*2, match_thresh=0.8, frame_rate=fps)

box_annotator = sv.BoxAnnotator(color=sv.Color(r=0, g=255, b=0), text_color=sv.Color.white(), thickness=1, text_thickness=1, text_scale=0.5)

#------------------------------------------------------------------
i = 0
anteriores = {}
ult_mov_x = {}
ult_mov_y = {}
calc_centro = 'centro-sup'
ult_vel = {}
ults_vel = {}
tpo_calc_vel = 0.5

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
    #----------------------------------------------------------
    results = model(frame, verbose=False)[0]
    detections = sv.Detections.from_ultralytics(results)
    # only consider class id from selected_classes define above
    detections = detections[np.isin(detections.class_id, selected_classes)]
    # tracking detections
    detections = byte_tracker.update_with_detections(detections)

    #-------------------------------Velocidad de detecciones---------------

    anteriores = guardar_centros_anteriores_v3(anteriores, detections.tracker_id, detections.xyxy, ult_mov_x, ult_mov_y, fps, def_centro=calc_centro, width=720, height=480)

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

    try:
      #print(isnot_zero_start(detections1.tracker_id, ult_vel, anteriores, video_info.fps, tpo_calc_vel))
      detections = detections[isnot_zero_start(detections.tracker_id, ult_vel, anteriores, fps, tpo_calc_vel)]
    except: None
    #----------------------------------------------------------------------

    labels = []
    for bbox, _, confidence, class_id, tracker_id in detections:
        labels.append(f"{ult_vel[tracker_id]:0.2f} p/s")

    annotated_frame = frame.copy()

    annotated_frame=box_annotator.annotate(
        scene=annotated_frame,
        detections=detections,
        labels=labels, skip_label=False
        )

    return  annotated_frame

tiempos = []
ret, frame = cap.read()
cv2.imwrite(r"C:\Users\eitan\Pictures\frame_prueba.png",frame)

while cap.isOpened():
    ret, frame = cap.read()
    #frame = cv2.resize(frame, (640, 640))
    if not ret:
        break
    # Perform detection
    ti = time.time()
    output_frame = detect(frame)
    tiempos.append((time.time() - ti)*1000)
    i += 1
    #output_frame=frame

    # Display the frame with detections
    cv2.imshow('Camara Paseo Estacion con analitica', output_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print(np.sum(tiempos)/len(tiempos))
cap.release()
cv2.destroyAllWindows()