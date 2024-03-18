from funciones.trayectorias import guardar_centros_anteriores_v2, calcular_angulos, get_diff_angulos, get_angulo_label
import supervision as sv
import cv2
from collections import deque
    
from funciones.general import isin_polygon
import numpy as np

class Objeto_Trayectorias:
    def __init__(self, guardar_evento):
        self.anteriores = {}
        self.ult_angulo = {}
        self.fps = 25
        self.box_annotator = sv.BoxAnnotator(color=sv.Color.green(), text_color=sv.Color.white(), thickness=1, text_thickness=1, text_scale=0.3)
        self.box_annotator2 = sv.BoxAnnotator(color=sv.Color.blue(), text_color=sv.Color.white(), thickness=1, text_thickness=1, text_scale=0.3)
        self.box_annotator3 = sv.BoxAnnotator(color=sv.Color.red(), text_color=sv.Color.white(), thickness=1, text_thickness=1, text_scale=0.3)
        self.mostrar_bajos = False
        self.mostrar_medios = False
        self.mostrar_altos = True

        self.frame_w = 0
        self.frame_h = 0

        self.guardar_evento = guardar_evento
        self.frames_preproc = deque(maxlen=self.fps * 2)
        self.frames_postproc = deque(maxlen=self.fps * 2)
        self.ocurre_evento = False
        self.guardando_evento = False
        self.i = 0
        self.video_writer_pre = None
        self.video_writer_post = None

    def frame_wh(self, frame):
        self.frame_w = frame.shape[1]
        self.frame_h = frame.shape[0]
    
    def anotar_frame(self, frame, detecciones, modelo):
        annotated_frame = frame.copy()
        self.frames_preproc.append(frame)
        #try: 
            #zona = np.array([(1489, 373), (1407, 687), (469, 279), (167, 650), (1701, 1007), (1871, 349)])
            #detecciones = detecciones[isin_polygon(detecciones.xyxy, sv.PolygonZoneAnnotator(color=sv.Color(r=0, g=255, b=0), zone=sv.PolygonZone(zona, frame_resolution_wh=(frame.shape[1], frame.shape[0]), triggering_position=sv.Position.CENTER)).zone.mask)]
        #except: None

        try:
            self.anteriores = guardar_centros_anteriores_v2(self.anteriores, detecciones.tracker_id, detecciones.xyxy)
            for id in self.ult_angulo.keys():
                if id not in self.anteriores.keys():
                    del self.ult_angulo[id]
        except:
            None

        try:
            self.ult_angulo = calcular_angulos(self.ult_angulo, self.anteriores, detecciones.tracker_id, frame_rate=self.fps)
        except:
            None

        try:
            angulos_mayor_50 = get_diff_angulos(self.ult_angulo, detecciones.tracker_id, diff=70, tpo_prev=2)
            angulos_mayor_25 = get_diff_angulos(self.ult_angulo, detecciones.tracker_id, diff=45, tpo_prev=2)
            angulos_mayor_25 = angulos_mayor_25 & ~angulos_mayor_50

            detections_mal = detecciones[angulos_mayor_50]
            detections_medio = detecciones[angulos_mayor_25]
            detections_bien = detecciones[~(angulos_mayor_25 | angulos_mayor_50)]
        except:
            None

        try: 
            if self.mostrar_altos:
                labels_mal = [
                    f"{tracker_id}, Ang: {get_angulo_label(self.ult_angulo, tracker_id)}"
                    #'CORRIENDO'
                for bbox, _, confidence, class_id, tracker_id
                in detections_mal
                ]
            
                for id in detections_mal.tracker_id:
                    #id = det.tracker_id
                    centros = self.anteriores[id]
                    if len(centros) > 1:
                        if len(centros) < 2 * self.fps:
                            for j in range(1, len(centros)):
                                annotated_frame = sv.draw_line(annotated_frame, sv.Point(centros[j - 1][0], centros[j - 1][1]), sv.Point(centros[j][0], centros[j][1]), sv.Color.red(), 2)
                        else:
                            for j in range(len(centros) - 2 * self.fps + 1, len(centros)):
                                annotated_frame = sv.draw_line(annotated_frame, sv.Point(centros[j - 1][0], centros[j - 1][1]), sv.Point(centros[j][0], centros[j][1]), sv.Color.red(), 2)

                if (len(labels_mal) >= 1) and (self.ocurre_evento == False):
                    self.ocurre_evento = True 

                annotated_frame=self.box_annotator3.annotate(
                    scene=annotated_frame,
                    detections=detections_mal,
                    labels=labels_mal
                    )
            if self.mostrar_medios:
                labels_medio = [
                    f"{tracker_id}, Ang: {get_angulo_label(self.ult_angulo, tracker_id)}"
                    #'CORRIENDO'
                for bbox, _, confidence, class_id, tracker_id
                in detections_medio
                ]
            
                for id in detections_medio.tracker_id:
                    #id = det.tracker_id
                    centros = self.anteriores[id]
                    if len(centros) > 1:
                        if len(centros) < 2 * self.fps:
                            for j in range(1, len(centros)):
                                annotated_frame = sv.draw_line(annotated_frame, sv.Point(centros[j - 1][0], centros[j - 1][1]), sv.Point(centros[j][0], centros[j][1]), sv.Color.blue(), 2)
                        else:
                            for j in range(len(centros) - 2 * self.fps + 1, len(centros)):
                                annotated_frame = sv.draw_line(annotated_frame, sv.Point(centros[j - 1][0], centros[j - 1][1]), sv.Point(centros[j][0], centros[j][1]), sv.Color.blue(), 2)

                if (len(labels_medio) >= 1) and (self.ocurre_evento == False):
                    self.ocurre_evento = True 

                annotated_frame=self.box_annotator2.annotate(
                    scene=annotated_frame,
                    detections=detections_medio,
                    labels=labels_medio
                    )
            if self.mostrar_bajos:
                labels_bien = [
                    f"{tracker_id}, Ang: {get_angulo_label(self.ult_angulo, tracker_id)}"
                for bbox, _, confidence, class_id, tracker_id
                in detections_bien
                ]
            
                for id in detections_bien.tracker_id:
                    #id = det.tracker_id
                    centros = self.anteriores[id]
                    if len(centros) > 1:
                        if len(centros) < 2 * self.fps:
                            for j in range(1, len(centros)):
                                annotated_frame = sv.draw_line(annotated_frame, sv.Point(centros[j - 1][0], centros[j - 1][1]), sv.Point(centros[j][0], centros[j][1]), sv.Color.green(), 2)
                        else:
                            for j in range(len(centros) - 2 * self.fps + 1, len(centros)):
                                annotated_frame = sv.draw_line(annotated_frame, sv.Point(centros[j - 1][0], centros[j - 1][1]), sv.Point(centros[j][0], centros[j][1]), sv.Color.green(), 2)

                if (len(labels_bien) >= 1) and (self.ocurre_evento == False):
                    self.ocurre_evento = True 

                annotated_frame=self.box_annotator.annotate(
                    scene=annotated_frame,
                    detections=detections_bien,
                    labels=labels_bien
                    )
        except:
            None
        
        self.frames_postproc.append(annotated_frame)

        if self.guardar_evento and self.ocurre_evento:
            self.guardar_video(frame, annotated_frame)

        return annotated_frame
    
    def guardar_video(self, frame_pre, frame_post):
        if not self.guardando_evento:
            self.video_writer_pre = cv2.VideoWriter('C:\\Users\\eitan\\Pictures\\cambio_trayectoria_pre.mp4', cv2.VideoWriter_fourcc(*'mp4v'), self.fps, (self.frame_w, self.frame_h))
            self.video_writer_post = cv2.VideoWriter('C:\\Users\\eitan\\Pictures\\cambio_trayectoria_post.mp4', cv2.VideoWriter_fourcc(*'mp4v'), self.fps, (self.frame_w, self.frame_h))
            self.i = 0
            self.guardando_evento = True
            print('Guardando Evento Trayectoria')
            for f in self.frames_preproc:
                self.video_writer_pre.write(f)
            for f in self.frames_postproc:
                self.video_writer_post.write(f)
        else:
            if self.i < self.fps * 3:
                self.i += 1
                self.video_writer_pre.write(frame_pre)
                self.video_writer_post.write(frame_post)
            else:
                print('Evento Trayectoria Guardado')
                self.video_writer_pre.release()
                self.video_writer_post.release()
                self.guardando_evento = False
                self.ocurre_evento = False