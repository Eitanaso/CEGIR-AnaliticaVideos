import argparse

from ultralytics import YOLO

from datetime import datetime

import cv2

import pyscreenshot as ImageGrab
import time
import numpy as np
import pandas as pd

import supervision as sv

import json


MODEL = 'yolov8x.pt'
MODEL = 'yolo_4158imgs_augment_30brillo.pt'
selected_classes = 0
segs_frame = 1

pantallazos = True

SOURCE_VIDEO_PATH = 'C:\\Users\\eitan\\Desktop\\cosas CEGIR\\contar_personas_zona_pantallazos\\transito_peatonal_1min10seg.mov'
rtsp_url = SOURCE_VIDEO_PATH
fps = 25

pantalla = ()
pantalla = (1040, 232, 1781, 729)

zonas = [
        [(10, 234), (112, 351), (524, 188), (387, 92)]
        #[(7, 236), (123, 365), (497, 187), (386, 96)],
]
centros_zonas = [(50, 30)]

def get_model(MODEL):
    model = YOLO(MODEL)
    print(model.model.names)
    model.fuse()
    return model

def create_labels(detecciones, modelo):
    labels = []
    for bbox, xyxy, confidence, class_id, tracker_id in detecciones:
        labels.append(f"{modelo.model.names[class_id]} {[tracker_id]}")
    return labels

# Funcion para encontrar el centro definido de una bbox
def centro(bbox: np.ndarray, def_centro: str = 'centro') -> np.ndarray:
  '''
  Funcion que calcula la posicion del centro de una bbox de acuerdo a la definicion dada.
  Entrega los 2 puntos del centro como una lista (x, y).
  Se utiliza para obtener el centro de una bbox por si es necesario hacer algo con este.

  Variables:
  - bbox (np.ndarray): lista de las posiciones x,y de la bbox de una deteccion realizada por el modelo
  - def_centro (str): texto que indica el punto de la bbox desde el cual se considera que la deteccion esta dentro del poligono. 
  Hasta la fecha, las unicas opciones son 'centro' (opcion por defecto) y 'centro-sup'

  Ante mas dudas de esta funcion, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
  '''
  if def_centro == 'centro':
    x_c = int((bbox[0] + bbox[2]) / 2)
    y_c = int((bbox[1] + bbox[3]) / 2)
  elif def_centro == 'centro-sup':
    x_c = int((bbox[0] + bbox[2]) / 2)
    y_c = int(min(bbox[1], bbox[3]))
  elif def_centro == 'centro-inf':
    x_c = int((bbox[0] + bbox[2]) / 2)
    y_c = int(max(bbox[1], bbox[3]))
  return np.array([x_c, y_c])

# Funcion para revisar si las detecciones estan en el poligono
def isin_polygon(det_box: np.ndarray, mask_poli: np.ndarray, bbox_dentro: str = 'centro') -> np.ndarray:
  '''
  Funcion que revisa si el centro de las detecciones recibidas se encuentran dentro de un poligono definido. 
  Entrega una lista con valores boleanos que representan si la deteccion se encuentra dentro o fuera del poligono.
  Se utiliza para guardar solo las detecciones dentro del poligono definido.

  Variables:
  - det_box (np.ndarray): lista de las posiciones x,y de las bbox detectadas por el modelo
  - mask_poli (np.ndarray): mascara que representa la zona dentro de la cual se esta analizando las detecciones
  - bbox_dentro (str): texto que indica el punto de la bbox desde el cual se considera que la deteccion esta dentro del poligono. 
  Hasta la fecha, las unicas opciones son 'centro' (opcion por defecto) y 'centro-sup'

  Ante mas dudas de esta funcion, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
  '''
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

def definir_area_pantalla(bbox=None):
    global img
    global puntos
    img = ImageGrab.grab(bbox)
    img = np.asarray(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imshow('frame', img)
    puntos = []
    cv2.setMouseCallback('frame', click_event)
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            if bbox:
                zonas.append(puntos)
            break
    cv2.destroyAllWindows()
    print(puntos)
    bbox = (puntos[0][0], puntos[0][1],puntos[1][0],puntos[1][1])
    return bbox

def definir_zona_deteccion(bbox=None):
    global img
    global puntos
    img = ImageGrab.grab(bbox)
    img = np.asarray(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imshow('frame', img)
    puntos = []
    cv2.setMouseCallback('frame', click_event)
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            if bbox:
                zonas.append(puntos)
            break
    cv2.destroyAllWindows()
    print(puntos)

def get_frame(bbox):
    frame = ImageGrab.grab(bbox=bbox)
    frame = np.asarray(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame

def main_pantallazos(model, i=0):
    # datetime object containing current date and time
    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("inicio =", dt_string)

    #cap = get_video(rstp_url)
    model = get_model(model)
    #_, output_frame = cap.read()
    starttime = time.monotonic()
    #print(starttime)
    if len(pantalla) == 0:
        bbox = definir_area_pantalla()
    else:
        bbox = pantalla

    if len(zonas) == 0:
        definir_zona_deteccion(bbox)

    #while cap.isOpened():
    #df=pd.DataFrame({'Hora Deteccion':[], 'Cantidad Detectado':[]})

    frame = get_frame(bbox)

    objeto_estacionados = Objeto_Detecciones()
    objeto_estacionados.frame_wh(frame)
    objeto_estacionados.create_polygone_zones(zonas)
    objeto_estacionados.create_polygone_zone_annotators(centros_zonas)

    tpo_extra = 0

    json_conteo = {'conteo': 0}
    
    #video_writer = cv2.VideoWriter('C:\\Users\\eitan\\Desktop\\cosas CEGIR\\maraton\\maraton_resultado.mp4', cv2.VideoWriter_fourcc(*'mp4v'), int(1/segs_frame), (frame.shape[1], frame.shape[0]))
    while True:
        ti = time.time()
        #ret, frame = cap.read()
        #bbox = (100, 100, 700, 800)
        frame = get_frame(bbox)
        #if not ret:
            #break
        #if i % int(fps * segs_frame) == 0:
        output_frame, conteo_total = detect(frame, model, selected_classes, zonas, centros_zonas, objeto_estacionados)
        print(conteo_total)
        cv2.imshow('Camara Paseo Estacion con analitica', output_frame)
        #video_writer.write(output_frame)
        #now = datetime.now()
        #dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        #nueva_fila = {'Hora Deteccion':dt_string, 'Cantidad Detectado':conteo_total}
        #df = pd.concat([df, pd.DataFrame(nueva_fila, index=[0])], ignore_index=True)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        i += 1
        json_conteo['conteo'] = conteo_total
        with open('C:\\Users\\eitan\\Desktop\\cosas CEGIR\\contar_personas_zona_pantallazos\\json_conteo.json', 'w') as f:
            json.dump(json_conteo, f)
        procesamiento = time.time() - ti
        print(procesamiento)
        if segs_frame - procesamiento + tpo_extra >= 0:
            tpo_extra = 0
            time.sleep(segs_frame)# - ((time.monotonic() - starttime) % 60.0))
        else:
            tpo_extra = segs_frame - procesamiento
            time.sleep(segs_frame)

    #df.to_csv('C:\\Users\\eitan\\Desktop\\cosas CEGIR\\contar_personas_zona_pantallazos\\conteo.csv', index=False)


    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("fin =", dt_string)

def main_video(rtsp_url, model, i=0):
    # datetime object containing current date and time
    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("inicio =", dt_string)

    cap = cv2.VideoCapture(rtsp_url)
    model = get_model(model)
    _, output_frame = cap.read()
    starttime = time.monotonic()
    #print(starttime)
    global img
    _, img = cap.read()
    if len(zonas) == 0:
        cv2.imshow('frame', img)
        global puntos
        puntos = []
        cv2.setMouseCallback('frame', click_event)
        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                zonas.append(puntos)
                break
        cv2.destroyAllWindows()

    #while cap.isOpened():
    #df=pd.DataFrame({'Hora Deteccion':[], 'Cantidad Detectado':[]})
    objeto_estacionados = Objeto_Detecciones()
    objeto_estacionados.frame_wh(output_frame)
    objeto_estacionados.create_polygone_zones(zonas)
    objeto_estacionados.create_polygone_zone_annotators(centros_zonas)

    json_conteo = {'conteo': 0}
    
    #video_writer = cv2.VideoWriter('C:\\Users\\eitan\\Desktop\\cosas CEGIR\\maraton\\maraton_resultado.mp4', cv2.VideoWriter_fourcc(*'mp4v'), int(1/segs_frame), (output_frame.shape[1], output_frame.shape[0]))
    while cap.isOpened():
        #ti = time.time()
        ret, frame = cap.read()
        if not ret:
            break
        if i % int(fps * segs_frame) == 0:
            output_frame, conteo_total = detect(frame, model, selected_classes, zonas, centros_zonas, objeto_estacionados)
            print(conteo_total)
            cv2.imshow('Camara Paseo Estacion con analitica', output_frame)
            json_conteo['conteo'] = conteo_total
            with open('C:\\Users\\eitan\\Desktop\\cosas CEGIR\\contar_personas_zona_pantallazos\\json_conteo.json', 'w') as f:
                json.dump(json_conteo, f)
            #video_writer.write(output_frame)
        #now = datetime.now()
        #dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        #nueva_fila = {'Hora Deteccion':dt_string, 'Cantidad Detectado':conteo_total}
        #df = pd.concat([df, pd.DataFrame(nueva_fila, index=[0])], ignore_index=True)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        i += 1
        #procesamiento = time.time() - ti
        #print(procesamiento)
        #time.sleep(segs_frame)# - ((time.monotonic() - starttime) % 60.0))

    #df.to_csv('C:\\Users\\eitan\\Desktop\\cosas CEGIR\\maraton\\maraton.csv', index=False)

    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("fin =", dt_string)


def detect(frame, model, selected_classes, zonas, centros_zonas, objeto_estacionados):
    #----------------------------------------------------------
    results = model(frame, verbose=False)[0]
    detections = sv.Detections.from_ultralytics(results)
    # only consider class id from selected_classes define above
    detections = detections[np.isin(detections.class_id, selected_classes)]
    # tracking detections
    #detections = byte_tracker.update_with_detections(detections)
    #----------------------Detenidos cierto tiempo----------------
    #-----------------Nueva forma---------------------------------
    #----------------------------------------------------------------------

    annotated_frame = frame.copy()

    
    annotated_frame, conteo_total = objeto_estacionados.anotar_frame(annotated_frame, detections, model)
    '''while True:
        #annotated_frame = cv2.resize(annotated_frame, (720, 480))
        #annotated_frame = cv2.resize(annotated_frame, (1080, 720))
        cv2.imshow('Camara Paseo Estacion con analitica', annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break'''

    return  annotated_frame, conteo_total


class Objeto_Detecciones:
    def __init__(self):
        self.n_zonas = 0
        self.zonas = []
        self.anotador_zonas_bien = []
        self.anotador_zonas_mal = []
        self.frame_w = 0
        self.frame_h = 0
        self.trigger_position = sv.Position.CENTER
        self.trigger_position = sv.Position.BOTTOM_CENTER

        self.box_annotator = sv.BoxAnnotator(color=sv.Color(r=255, g=0, b=0), text_color=sv.Color.white(), thickness=1, text_thickness=1, text_scale=0.5)
        self.box_annotator2 = sv.BoxAnnotator(color=sv.Color(r=0, g=255, b=0), text_color=sv.Color.white(), thickness=1, text_thickness=1, text_scale=0.5)
        self.seg_det = 0
        self.dixi_a1 = []
        self.tpo_perdida = 0.3
        self.fps = 25
        self.show_bbox = True
        self.show_label = False

        self.conteo_total = 0
        self.conteo_acumulativo = False

    def frame_wh(self, frame):
        self.frame_w = frame.shape[1]
        self.frame_h = frame.shape[0]

    def create_polygone_zones(self, zonas):
        self.n_zonas = len(zonas)
        for i in range(self.n_zonas):
            pz = sv.PolygonZone(np.array(zonas[i]), frame_resolution_wh=(self.frame_w, self.frame_h), triggering_position=self.trigger_position)
            self.zonas.append(pz)
            self.dixi_a1.append({})

    def create_polygone_zone_annotators(self, centros_zonas):
        for i in range(self.n_zonas):
            anotador_pz_mal = sv.PolygonZoneAnnotator(thickness=1, text_thickness=1, text_scale=0.5, zone=self.zonas[i], color=sv.Color(r=255, g=0, b=0), text_color=sv.Color.white(), text_padding=2, )
            anotador_pz_mal.center = sv.Point(centros_zonas[i][0], centros_zonas[i][1])
            self.anotador_zonas_mal.append(anotador_pz_mal)
            anotador_pz_bien = sv.PolygonZoneAnnotator(thickness=1, text_thickness=1, text_scale=0.5, zone=self.zonas[i], color=sv.Color(r=0, g=255, b=0), text_color=sv.Color.white(), text_padding=2, )
            anotador_pz_bien.center = sv.Point(centros_zonas[i][0], centros_zonas[i][1])
            self.anotador_zonas_bien.append(anotador_pz_bien)
        
    def anotar_frame(self, frame, detecciones, modelo):
        annotated_frame = frame
        for i in range(self.n_zonas):
            try:
                detections_i = detecciones[isin_polygon(detecciones.xyxy, self.anotador_zonas_mal[i].zone.mask, bbox_dentro='centro')]
                detections_i2 = detecciones[isin_polygon(detecciones.xyxy, self.anotador_zonas_mal[i].zone.mask, bbox_dentro='centro')]
            except:
                detections_i = detecciones
                detections_i2 = detecciones

            labels_i = create_labels(detections_i, modelo)
            labels_i2 = create_labels(detections_i2, modelo)

            if not self.conteo_acumulativo:
                self.conteo_total = 0

            annotated_frame = self.anotador_zonas_mal[i].annotate(annotated_frame, f'N per: {len(labels_i) + self.conteo_total}')
            #print(self.conteo_total)
            
            self.conteo_total += len(labels_i)

            if self.show_bbox:       
                annotated_frame = self.box_annotator2.annotate(
                    scene = annotated_frame,
                    detections = detections_i2,
                    labels = labels_i2, skip_label = ~self.show_label
                    )
                annotated_frame = self.box_annotator.annotate(
                    scene = annotated_frame,
                    detections = detections_i,
                    labels = labels_i, skip_label = ~self.show_label
                    )
        return annotated_frame, self.conteo_total

if __name__ == '__main__':
    if pantallazos:
        main_pantallazos(MODEL)
    else:
        main_video(rtsp_url, MODEL)