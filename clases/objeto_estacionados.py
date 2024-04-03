import supervision as sv
import numpy as np
from general import create_labels
from funciones.general import isin_polygon
from funciones.estacionados import save_detections_in_area_dixi, det_in_same_area

from PIL import ImageFont, ImageDraw, Image
import numpy as np
import cv2

#--------------------------------------------------------------------------------------------------------------------
# Creacion de la clase que se encarga de las personas estacionadas en el espacio
# Por mayores dudas de las funciones, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
#--------------------------------------------------------------------------------------------------------------------

class Objeto_Estacionados:
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
        #self.all_dets = []
        #self.all_labels = []

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
            # probar si el modelo detecto algo, si no, intentaria acceder a nada y habria error
            #print('dhsj')
            try:
                detections_i = detecciones[isin_polygon(detecciones.xyxy, self.anotador_zonas_mal[i].zone.mask, bbox_dentro='centro')]
                detections_i2 = detecciones[isin_polygon(detecciones.xyxy, self.anotador_zonas_mal[i].zone.mask, bbox_dentro='centro')]
            except:
                detections_i = detecciones
                detections_i2 = detecciones
            # siguiente linea sirve para la gente estacionada, guardando tracking
            #self.dixi_a1[i] = save_detections_in_area_dixi(self.dixi_a1[i], detections_i, self.seg_det * self.fps)
            try: 
                detections_i2 = detections_i[ ~ det_in_same_area(detections_i.tracker_id, self.dixi_a1[i], self.seg_det * self.fps, self.tpo_perdida)]
                detections_i = detections_i[det_in_same_area(detections_i.tracker_id, self.dixi_a1[i], self.seg_det * self.fps, self.tpo_perdida)]
            except:
                None
            labels_i = create_labels(detections_i, modelo)
            labels_i2 = create_labels(detections_i2, modelo)
            #self.all_dets.append(detections_i)
            #self.all_labels.append(labels_i)
        #for i in range(self.n_zonas):
            #labels_i = self.all_labels[i]
            #detections_i = self.all_dets[i]
            if len(labels_i):
                #annotated_frame = self.anotador_zonas_mal[i].annotate(annotated_frame, 'OCUPADO')
                annotated_frame = self.anotador_zonas_mal[i].annotate(annotated_frame, f'N per: {len(labels_i)}')
                '''annotated_frame = self.anotador_zonas_mal[i].annotate(annotated_frame, f'N  per: {len(labels_i)}')

                image = np.zeros(annotated_frame.shape, dtype=np.uint8)
                image = cv2.cvtColor(annotated_frame.copy(), cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(image)
                font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 20)
                draw = ImageDraw.Draw(pil_image)
                draw.text((173, 217), '°', font=font, align='left', fill=(255,255,255)) # RGB
                image = np.asarray(pil_image)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                annotated_frame = image'''
            else:
                #annotated_frame = self.anotador_zonas_bien[i].annotate(annotated_frame, 'NO OCUPADO')
                annotated_frame = self.anotador_zonas_bien[i].annotate(annotated_frame, 'N per: 0')
                '''annotated_frame = self.anotador_zonas_bien[i].annotate(annotated_frame, 'N  per: 0')

                image = np.zeros(annotated_frame.shape, dtype=np.uint8)
                image = cv2.cvtColor(annotated_frame.copy(), cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(image)
                font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 20)
                draw = ImageDraw.Draw(pil_image)
                draw.text((173, 217), '°', font=font, align='left', fill=(255,255,255)) # RGB
                image = np.asarray(pil_image)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                annotated_frame = image'''
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
        return annotated_frame