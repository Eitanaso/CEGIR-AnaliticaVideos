import cv2
from ultralytics import YOLO
import supervision as sv
import numpy as np
import time
from collections import deque

MODEL = "yolov8x.pt"
# Load YOLOv8 model
model = YOLO(MODEL)
model.fuse()
#selected_classes = [0,1,2,5]
selected_classes = [0,2]
print(model.model.names)

#----------------------------------------------------------

# Connect to RTSP stream
rtsp_url = r'rtsp://admin:Cafa2414$@10.0.10.182:554/0/profile2/media.smp'
#SOURCE_VIDEO_PATH = r'C:\Users\eitan\Pictures\comercio_ambulante_paseo_estacion.mp4'
#rtsp_url = SOURCE_VIDEO_PATH
#TARGET_VIDEO_PATH = r'C:\Users\eitan\Pictures\comercio_ambulante_detectado.mp4'
cap = cv2.VideoCapture(rtsp_url)
#cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)


#------------------------Funciones-----------------------------------------
def isin_polygon(det_box, mask_poli, bbox_dentro='centro'):
  res = []
  for bbox in det_box:
    coord_centro = centro(bbox, def_centro=bbox_dentro)
    x_c = coord_centro[0]
    y_c = coord_centro[1]
    if mask_poli[y_c][x_c]:
      res.append(True)
    else:
      res.append(False)
  return np.array(res)

def centro(bbox, def_centro='centro'):
  if def_centro == 'centro':
    x_c = int((bbox[0] + bbox[2]) / 2)
    y_c = int((bbox[1] + bbox[3]) / 2)
  elif def_centro == 'centro-sup':
    x_c = int((bbox[0] + bbox[2]) / 2)
    y_c = int(min(bbox[1], bbox[3]))
  return np.array([x_c, y_c])

def bbox_centros(bboxs_dets, def_centro='centro'):
  '''
  bbox_dets: lista de las bbox detectadas
  def_centro: lugar que se define el centro para medir (puede ser centro o centro-sup)
  '''
  res = []
  for bbox in bboxs_dets:
    if def_centro == 'centro':
      x_c = int((bbox[0] + bbox[2]) / 2)
      y_c = int((bbox[1] + bbox[3]) / 2)
    elif def_centro == 'centro-sup':
      x_c = int((bbox[0] + bbox[2]) / 2)
      y_c = int(min(bbox[1], bbox[3]))
    res.append([x_c, y_c])
  return np.array(res)

def misma_zona(dets, cods, bboxs, rango = 30):
  res = []
  for i in range(len(dets.xyxy)):
    cod_det = dets.tracker_id[i]
    bbox_det = dets.xyxy[i]
    x_c = int((bbox_det[0] + bbox_det[2]) / 2)
    y_c = int((bbox_det[1] + bbox_det[3]) / 2)
    in_range = True
    for j in range(len(cods)):
      if cod_det not in cods[j]:
        in_range = False
        break
        #esto se usaba para detectar que persona no se moviera cierto rango
    '''if in_range:
      for j in range(len(cods)):
        pos_cod = list(cods[j]).index(cod_det)
        bbox_centro_j = bboxs[j][pos_cod]
        x_bbox = bbox_centro_j[0]
        y_bbox = bbox_centro_j[1]
        if (x_bbox - rango > x_c) or (x_bbox + rango < x_c) or (y_bbox - rango > y_c) or (y_bbox + rango < y_c):
          in_range = False
          break'''
    res.append(in_range)
  return np.array(res)

# estos son stacks
def create_sized_list(size):
    return deque(maxlen=size)

def add_item(sized_list, item):
    sized_list.append(item)
#------------------------------------------------------------------
# create VideoInfo instance
#video_info = sv.VideoInfo.from_video_path(SOURCE_VIDEO_PATH)
fps=25
# create BYTETracker instance
byte_tracker = sv.ByteTrack(track_thresh=0.15, track_buffer=fps*2, match_thresh=0.8, frame_rate=fps)

box_annotator1 = sv.BoxAnnotator(color=sv.Color(r=255, g=0, b=0), text_color=sv.Color.white(), thickness=1, text_thickness=1, text_scale=0.5)
box_annotator2 = sv.BoxAnnotator(color=sv.Color(r=255, g=0, b=0), text_color=sv.Color.white(), thickness=1, text_thickness=1, text_scale=0.5)

#------------------------------------------------------------------
i = 0
seg_det = 1 #segundos de personas detenidos

lista_cod1 = create_sized_list(seg_det)
lista_pos1 = create_sized_list(seg_det)
lista_cod2 = create_sized_list(seg_det)
lista_pos2 = create_sized_list(seg_det)
# Function to perform YOLOv8 detection
def detect(frame):
    #----------------Variables globales importantes-----------
    global i
    global lista_cod1
    global lista_pos1
    global lista_cod2
    global lista_pos2
    global seg_det
    #----------------------------------------------------------
    results = model(frame, verbose=False)[0]
    detections = sv.Detections.from_ultralytics(results)
    # only consider class id from selected_classes define above
    detections = detections[np.isin(detections.class_id, selected_classes)]
    # tracking detections
    detections = byte_tracker.update_with_detections(detections)

    #-------------------------------Detecciones en Poligono---------------
    try: detections1 = detections[isin_polygon(detections.xyxy, polygon_zone_annotator1.zone.mask)] # detecciones por cada poligono
    except: None # si no hubo ninguna deteccion en general (itenta acceder a .xyxy que no existe), que no haga nada al respecto, sino, genera error
    try: detections2 = detections[isin_polygon(detections.xyxy, polygon_zone_annotator2.zone.mask)]
    except: None
    #----------------------Detenidos cierto tiempo----------------
    if i % fps == 0:
      add_item(lista_cod1, detections1.tracker_id)
      add_item(lista_pos1, bbox_centros(detections1.xyxy))
      add_item(lista_cod2, detections2.tracker_id)
      add_item(lista_pos2, bbox_centros(detections2.xyxy))
    if i < seg_det * fps:
      if len(detections1.xyxy) > 0:
        detections1 = detections1[np.array([False for _ in detections1.xyxy])]
      if len(detections2.xyxy) > 0:
        detections2 = detections2[np.array([False for _ in detections2.xyxy])]
    else:
      if len(detections1.xyxy) > 0:
        detections1 = detections1[misma_zona(detections1, lista_cod1, lista_pos1, rango=10000)] #rango no hace nada
      if len(detections2.xyxy) > 0:
        detections2 = detections2[misma_zona(detections2, lista_cod2, lista_pos2, rango=10000)] #rango no hace nada
    #----------------------------------------------------------------------

    labels1 = []
    for bbox, _, confidence, class_id, tracker_id in detections1:
        labels1.append(f"{model.model.names[class_id]} {[tracker_id]}")

    labels2 = []
    for bbox, _, confidence, class_id, tracker_id in detections2:
        labels2.append(f"{model.model.names[class_id]} {[tracker_id]}")

    annotated_frame = frame.copy()
    if len(labels1):
      annotated_frame = polygon_zone_annotator1.annotate(annotated_frame, 'OCUPADO')
    else:
      annotated_frame = polygon_zone_annotator1_1.annotate(annotated_frame, 'NO OCUPADO')
    if len(labels2):
      annotated_frame = polygon_zone_annotator2.annotate(annotated_frame, 'OCUPADO')
    else:
      annotated_frame = polygon_zone_annotator2_1.annotate(annotated_frame, 'NO OCUPADO')
    annotated_frame=box_annotator1.annotate(
        scene=annotated_frame,
        detections=detections1,
        labels=labels1, skip_label=True
        )
    annotated_frame=box_annotator2.annotate(
        scene=annotated_frame,
        detections=detections2,
        labels=labels2, skip_label=True
        )

    return  annotated_frame

tiempos = []
ret, frame = cap.read()
polygon_zone1 = sv.PolygonZone(np.array(
    [(40, 188), (187, 337), (371, 412), (408, 333), (265, 273), (131, 167)]
    ), frame_resolution_wh=(frame.shape[1], frame.shape[0]), 
triggering_position=sv.Position.CENTER)

polygon_zone2 = sv.PolygonZone(np.array(
    [(427, 256), (579, 301), (706, 325), (703, 242), (578, 218), (476, 181)]
    ), frame_resolution_wh=(frame.shape[1], frame.shape[0]), 
triggering_position=sv.Position.CENTER)

polygon_zone_annotator1 = sv.PolygonZoneAnnotator(thickness=1, text_thickness=1, text_scale=0.5, zone=polygon_zone1, color=sv.Color(r=255, g=0, b=0), text_color=sv.Color.white(), text_padding=2, )#, center=(140, 310))
polygon_zone_annotator1.center = sv.Point(75, 195)
polygon_zone_annotator2 = sv.PolygonZoneAnnotator(thickness=1, text_thickness=1, text_scale=0.5, zone=polygon_zone2, color=sv.Color(r=255, g=0, b=0), text_color=sv.Color.white(), text_padding=2, )#, center=(140, 310))
polygon_zone_annotator2.center = sv.Point(480, 185)
polygon_zone_annotator1_1 = sv.PolygonZoneAnnotator(thickness=1, text_thickness=1, text_scale=0.5, zone=polygon_zone1, color=sv.Color(r=0, g=255, b=0), text_color=sv.Color.white(), text_padding=2, )#, center=(140, 310))
polygon_zone_annotator1_1.center = sv.Point(75, 195)
polygon_zone_annotator2_1 = sv.PolygonZoneAnnotator(thickness=1, text_thickness=1, text_scale=0.5, zone=polygon_zone2, color=sv.Color(r=0, g=255, b=0), text_color=sv.Color.white(), text_padding=2, )#, center=(140, 310))
polygon_zone_annotator2_1.center = sv.Point(480, 185)
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