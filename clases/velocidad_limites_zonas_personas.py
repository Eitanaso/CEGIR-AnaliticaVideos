import cv2
from ultralytics import YOLO
import supervision as sv
import numpy as np
import time
from funciones.general import *
from funciones.velocidades import *

#--------------------------------------------------------------------------------------------------------------------
# Codigo encargado de mostrar las velocidades de las personas que corren o estan detenidas (Falta generalizarlo y crear una clase para funcionar en main)
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

box_annotator1 = sv.BoxAnnotator(color=sv.Color(r=0, g=255, b=0), text_color=sv.Color.white(), thickness=1, text_thickness=1, text_scale=0.5)
box_annotator2 = sv.BoxAnnotator(color=sv.Color(r=255, g=0, b=0), text_color=sv.Color.white(), thickness=1, text_thickness=1, text_scale=0.5)
box_annotator3 = sv.BoxAnnotator(color=sv.Color(r=0, g=0, b=255), text_color=sv.Color.white(), thickness=1, text_thickness=1, text_scale=0.5)

#------------------------------------------------------------------
i = 0
anteriores = {}
ult_mov_x = {}
ult_mov_y = {}
calc_centro = 'centro-sup'
ult_vel = {}
ults_vel = {}
tpo_calc_vel = 0.5
sup1 = 100
inf1 = 25
sup2 = 100
inf2 = 15
sup3 = 100
inf3 = 15

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
    global sup1
    global inf1
    global sup2
    global inf2
    global sup3
    global inf3
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

    try: detections1 = detections[isin_polygon(detections.xyxy, polygon_zone_annotator1.zone.mask)]
    except: detections1 = detections
    try: detections2 = detections[isin_polygon(detections.xyxy, polygon_zone_annotator2.zone.mask)]
    except: detections2 = detections
    try: detections3 = detections[isin_polygon(detections.xyxy, polygon_zone_annotator3.zone.mask)]
    except: detections3 = detections

    try:
      #print(isnot_zero_start(detections1.tracker_id, ult_vel, anteriores, video_info.fps, tpo_calc_vel))
      detections1 = detections1[isnot_zero_start(detections1.tracker_id, ult_vel, anteriores, fps, tpo_calc_vel)]
    except: None
    try:
      #print(isnot_zero_start(detections1.tracker_id, ult_vel, anteriores, video_info.fps, tpo_calc_vel))
      detections2 = detections2[isnot_zero_start(detections2.tracker_id, ult_vel, anteriores, fps, tpo_calc_vel)]
    except: None
    try:
      #print(isnot_zero_start(detections1.tracker_id, ult_vel, anteriores, video_info.fps, tpo_calc_vel))
      detections3 = detections3[isnot_zero_start(detections3.tracker_id, ult_vel, anteriores, fps, tpo_calc_vel)]
    except: None

    try:
      #print(isbetween_sup_inf(detections1.tracker_id, ult_vel, sup1, inf1))
      detections1 = detections1[isbetween_sup_inf(detections1.tracker_id, ult_vel, sup1, inf1)]
      #detections1 = detections1[isbetween_sup_infv3(detections1.tracker_id, ult_vel, sup1, inf1, ults_vel, detections.tracker_id)]
    except: None
    try:
      #print(isbetween_sup_inf(detections1.tracker_id, ult_vel, sup1, inf1))
      detections2 = detections2[isbetween_sup_inf(detections2.tracker_id, ult_vel, sup2, inf2)]
      #detections2 = detections2[isbetween_sup_infv3(detections2.tracker_id, ult_vel, sup2, inf2, ults_vel, detections.tracker_id)]
    except: None
    try:
      #print(isbetween_sup_inf(detections1.tracker_id, ult_vel, sup1, inf1))
      detections3 = detections3[isbetween_sup_inf(detections3.tracker_id, ult_vel, sup3, inf3)]
      #detections3 = detections3[isbetween_sup_infv3(detections3.tracker_id, ult_vel, sup3, inf3, ults_vel, detections.tracker_id)]
    except: None
    #----------------------------------------------------------------------

    labels1 = []
    for bbox, _, confidence, class_id, tracker_id in detections1:
        labels1.append(f"{ult_vel[tracker_id]:0.2f} p/s")
    labels2 = []
    for bbox, _, confidence, class_id, tracker_id in detections2:
        labels2.append(f"{ult_vel[tracker_id]:0.2f} p/s")
    labels3 = []
    for bbox, _, confidence, class_id, tracker_id in detections3:
        labels3.append(f"{ult_vel[tracker_id]:0.2f} p/s")

    annotated_frame = frame.copy()

    annotated_frame=box_annotator1.annotate(
        scene=annotated_frame,
        detections=detections1,
        labels=labels1, skip_label=False
        )

    for id in detections1.tracker_id:
      centros = anteriores[id]
      if len(centros) > 1:
        if len(centros) < 2 * fps:
          for j in range(1, len(centros)):
            annotated_frame = sv.draw_line(annotated_frame, sv.Point(centros[j - 1][0], centros[j - 1][1]), sv.Point(centros[j][0], centros[j][1]), sv.Color(r=0, g=255, b=0), 2)
        else:
          for j in range(len(centros) - 2 * fps + 1, len(centros)):
            annotated_frame = sv.draw_line(annotated_frame, sv.Point(centros[j - 1][0], centros[j - 1][1]), sv.Point(centros[j][0], centros[j][1]), sv.Color(r=0, g=255, b=0), 2)

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

    annotated_frame=box_annotator3.annotate(
        scene=annotated_frame,
        detections=detections3,
        labels=labels3, skip_label=False
        )

    for id in detections3.tracker_id:
      centros = anteriores[id]
      if len(centros) > 1:
        if len(centros) < 2 * fps:
          for j in range(1, len(centros)):
            annotated_frame = sv.draw_line(annotated_frame, sv.Point(centros[j - 1][0], centros[j - 1][1]), sv.Point(centros[j][0], centros[j][1]), sv.Color(r=0, g=0, b=255), 2)
        else:
          for j in range(len(centros) - 2 * fps + 1, len(centros)):
            annotated_frame = sv.draw_line(annotated_frame, sv.Point(centros[j - 1][0], centros[j - 1][1]), sv.Point(centros[j][0], centros[j][1]), sv.Color(r=0, g=0, b=255), 2)

    #annotated_frame = polygon_zone_annotator1.annotate(annotated_frame, f"[{inf1}, {sup1}]")
    #annotated_frame = polygon_zone_annotator2.annotate(annotated_frame, f"[{inf2}, {sup2}]")
    #annotated_frame = polygon_zone_annotator3.annotate(annotated_frame, f"[{inf3}, {sup3}]")
    return  annotated_frame

tiempos = []
ret, frame = cap.read()
polygon_zone1 = sv.PolygonZone(np.array(
    [(18, 213), (120, 322), (471, 193), (377, 128)]
    ), frame_resolution_wh=(frame.shape[1], frame.shape[0]), 
triggering_position=sv.Position.CENTER)

polygon_zone2 = sv.PolygonZone(np.array(
    [(120, 322), (293, 434), (607, 219), (471, 193)]
    ), frame_resolution_wh=(frame.shape[1], frame.shape[0]), 
triggering_position=sv.Position.CENTER)

polygon_zone3 = sv.PolygonZone(np.array(
    [(293, 434), (359, 480), (720, 480), (720, 208), (607, 219)]
    ), frame_resolution_wh=(frame.shape[1], frame.shape[0]), 
triggering_position=sv.Position.CENTER)


polygon_zone_annotator1 = sv.PolygonZoneAnnotator(thickness=1, text_thickness=1, text_scale=0.5, zone=polygon_zone1, color=sv.Color(r=0, g=255, b=0), text_color=sv.Color.white(), text_padding=2, )#, center=(140, 310))
polygon_zone_annotator1.center = sv.Point(376, 133)
polygon_zone_annotator2 = sv.PolygonZoneAnnotator(thickness=1, text_thickness=1, text_scale=0.5, zone=polygon_zone2, color=sv.Color(r=255, g=0, b=0), text_color=sv.Color.white(), text_padding=2, )#, center=(140, 310))
polygon_zone_annotator2.center = sv.Point(470, 198)
polygon_zone_annotator3 = sv.PolygonZoneAnnotator(thickness=1, text_thickness=1, text_scale=0.5, zone=polygon_zone3, color=sv.Color(r=0, g=0, b=255), text_color=sv.Color.white(), text_padding=2, )#, center=(140, 310))
polygon_zone_annotator3.center = sv.Point(606, 224)
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