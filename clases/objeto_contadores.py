import supervision as sv
from general import create_labels
from clases.line_counter_edit import Contador_Actualizado, Anotador_Linea_Actualizado

from funciones.general import isin_polygon
import numpy as np

#--------------------------------------------------------------------------------------------------------------------
# Creacion de la clase que se encarga de los contadores en un espacio
# Por mayores dudas de las funciones, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
#--------------------------------------------------------------------------------------------------------------------

class Objeto_Contadores:
    def __init__(self, color, pos_texto):#, guardar_archivo):
        self.n_contadores = 0
        self.contadores = []
        self.anotador_contadores = []
        self.frame_w = 0
        self.frame_h = 0
        #self.trigger_position = sv.Position.CENTER

        self.color = sv.Color(r=color[0], g=color[1], b=color[2])
        self.rgb = color

        #self.documento_contador = guardar_archivo

        #self.box_annotator = sv.BoxAnnotator(color=sv.Color(r=0, g=0, b=255), text_color=sv.Color.white(), thickness=1, text_thickness=1, text_scale=0.5)
        #self.box_annotator = sv.BoxAnnotator(color=sv.Color(r=0, g=255, b=0), text_color=sv.Color.white(), thickness=1, text_thickness=1, text_scale=0.5)
        self.box_annotator = sv.BoxAnnotator(color=self.color, text_color=sv.Color.white(), thickness=1, text_thickness=1, text_scale=0.5)
        self.fps = 25
        self.show_bbox = True
        self.show_label = True

        self.pos_texto = pos_texto

    def frame_wh(self, frame):
        self.frame_w = frame.shape[1]
        self.frame_h = frame.shape[0]

    def create_line_zones(self, line):
        self.n_contadores = len(line)
        for i in range(self.n_contadores):
            #lz = sv.LineZone(start = sv.Point(line[i][0][0], line[i][0][1]), end = sv.Point(line[i][1][0], line[i][1][1]))
            lz = Contador_Actualizado(name='Contador', start = sv.Point(line[i][0][0], line[i][0][1]), end = sv.Point(line[i][1][0], line[i][1][1]))
            self.contadores.append(lz)

    def create_line_zone_annotators(self, texto_in='↑ N° per', texto_out='↓ N° per'): # ← → ↑ ↓
        for i in range(self.n_contadores):
            anotador_lz = Anotador_Linea_Actualizado(thickness=1, text_thickness=1, text_scale=0.75, color = self.color, #sv.Color.green(), 
                                                     text_color=sv.Color.white(), text_padding=1, text_offset=1,
                                           custom_in_text=texto_in, custom_out_text=texto_out)
            self.anotador_contadores.append(anotador_lz)
        
    def anotar_frame(self, frame, detecciones, modelo):
        annotated_frame = frame
        #try: 
            #zona = np.array([(0, 480), (0, 213), (353, 480)]) # cam 1 entre vereda y calle
            #zona = np.array([(0, 210), (0, 0), (377, 0), (720, 166), (720, 480), (318, 480)])
            #zona = np.array([(0, 480), (0, 182), (189, 75), (388, 81), (445, 479)]) # cam 2 calle
            #zona = np.array([(397, 141), (392, 88), (145, 70), (56, 125)])
            #zona = np.array([(335, 480), (342, 271), (459, 272), (513, 480)]) # cam 2 entre vereda y calle
            #zona = np.array([(444, 574), (598, 564), (655, 720), (432, 720)]) # 
            #zona = np.array([(0, 570), (465, 561), (449, 720), (0, 720)])
            #zona = np.array([(0, 720), (0, 90), (470, 94), (583, 720)]) # 
            #zona = np.array([(0, 370), (1002, 0), (1280, 0), (1280, 188), (816, 720), (0, 720)])
            #zona = np.array([(305, 365), (974, 401), (646, 1080), (0, 1080)])
            #zona = np.array([(0, 833), (0, 393), (553, 486), (504, 818)])
            #detecciones = detecciones[isin_polygon(detecciones.xyxy, sv.PolygonZoneAnnotator(color=sv.Color(r=0, g=255, b=0), zone=sv.PolygonZone(zona, frame_resolution_wh=(frame.shape[1], frame.shape[0]), triggering_position=sv.Position.CENTER)).zone.mask)]
        #except: None
        for i in range(self.n_contadores):
            detections_i = detecciones
            labels_i = create_labels(detections_i, modelo)
            if self.show_bbox:    
                annotated_frame = self.box_annotator.annotate(
                    scene = annotated_frame,
                    detections = detections_i,
                    labels = labels_i, skip_label = ~self.show_label
                    )
            self.contadores[i].trigger(detections_i)
            annotated_frame = self.anotador_contadores[i].annotate(annotated_frame, line_counter=self.contadores[i], pos_texto=self.pos_texto, color=self.rgb)
        return annotated_frame