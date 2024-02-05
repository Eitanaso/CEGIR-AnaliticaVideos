from funciones.velocidades import guardar_centros_anteriores_v3, velocidad, velocidadv2, isnot_zero_start, isbetween_sup_infv2
import supervision as sv
import numpy as np
from funciones.general import isin_polygon
from collections import deque
import cv2

class Objeto_Velocidades:
    def __init__(self, guardar_evento):
        self.anteriores = {}
        self.ult_mov_x = {}
        self.ult_mov_y = {}
        self.ult_vel = {}
        self.ults_vel = {}
        self.tpo_calc_vel = 0.5
        self.fps = 25
        self.calc_centro = 'centro-sup'
        self.box_annotator = sv.BoxAnnotator(color=sv.Color(r=0, g=102, b=0), text_color=sv.Color.white(), thickness=1, text_thickness=1, text_scale=0.5)

        self.frame_w = 0
        self.frame_h = 0
        self.zonas = []
        self.anotador_zonas = []
        self.n_zonas = 0
        self.min_max = []
        self.trigger_position = sv.Position.CENTER

        self.guardar_evento = guardar_evento
        self.frames_preproc = deque(maxlen=self.fps * 2)
        self.frames_postproc = deque(maxlen=self.fps * 2)
        self.ocurre_evento = False
        self.guardando_evento = False
        self.i = 0
        self.video_writer_pre = None
        self.video_writer_post = None
    
    def anotar_frame(self, frame, detecciones, modelo):
        annotated_frame = frame

        try:
            self.anteriores = guardar_centros_anteriores_v3(self.anteriores, detecciones.tracker_id, detecciones.xyxy, self.ult_mov_x, self.ult_mov_y, self.fps, def_centro=self.calc_centro)
        except:
            None

        if len(self.ult_vel) == 0:
            for key in self.anteriores.keys():
                self.ult_vel[key] = 0
                self.ult_mov_x[key] = 0
                self.ult_mov_y[key] = 0
                self.ults_vel[key] = [0]

        for key in self.anteriores.keys():
            self.ult_vel[key] = velocidad(self.ult_vel, key, self.anteriores, self.fps, self.tpo_calc_vel)
            self.ult_mov_x[key] = velocidad(self.ult_mov_x, key, self.anteriores, self.fps, self.tpo_calc_vel, 'x')
            self.ult_mov_y[key] = velocidad(self.ult_mov_y, key, self.anteriores, self.fps, self.tpo_calc_vel, 'y')
            try:
                self.ults_vel[key].append(velocidadv2(self.ults_vel, key, self.anteriores, self.fps, 0.3))
            except:
                self.ults_vel[key] = [0]
        
        try:
            #print(isnot_zero_start(detections1.tracker_id, ult_vel, anteriores, video_info.fps, tpo_calc_vel))
            detecciones = detecciones[isnot_zero_start(detecciones.tracker_id, self.ult_vel, self.anteriores, self.fps, self.tpo_calc_vel)]
        except: 
            None

        labels = []
        for bbox, _, confidence, class_id, tracker_id in detecciones:
            if tracker_id in detecciones.tracker_id:
                labels.append(f"{self.ult_vel[tracker_id]:0.2f} p/s")

        annotated_frame=self.box_annotator.annotate(
           scene=annotated_frame,
            detections=detecciones,
            labels=labels
            )

        for id in detecciones.tracker_id:
            centros = self.anteriores[id]
            if len(centros) > 1:
                if len(centros) < 2 * self.fps:
                    for j in range(1, len(centros)):
                        annotated_frame = sv.draw_line(annotated_frame, sv.Point(centros[j - 1][0], centros[j - 1][1]), sv.Point(centros[j][0], centros[j][1]), sv.Color(r=0, g=102, b=0), 2)
                else:
                    for j in range(len(centros) - 2 * self.fps + 1, len(centros)):
                        annotated_frame = sv.draw_line(annotated_frame, sv.Point(centros[j - 1][0], centros[j - 1][1]), sv.Point(centros[j][0], centros[j][1]), sv.Color(r=0, g=102, b=0), 2)


        return annotated_frame

    def frame_wh(self, frame):
        self.frame_w = frame.shape[1]
        self.frame_h = frame.shape[0]
    
    def create_polygone_zones(self, zonas, min_max):
        self.n_zonas = len(zonas)
        self.box_annotator = sv.BoxAnnotator(color=sv.Color(r=200, g=0, b=0), text_color=sv.Color.white(), thickness=1, text_thickness=1, text_scale=0.5)
        for i in range(self.n_zonas):
            pz = sv.PolygonZone(np.array(zonas[i]), frame_resolution_wh=(self.frame_w, self.frame_h), triggering_position=self.trigger_position)
            self.zonas.append(pz)
            self.min_max.append(min_max[i])

    def create_polygone_zone_annotators(self):
        for i in range(self.n_zonas):
            anotador_pz = sv.PolygonZoneAnnotator(thickness=1, text_thickness=1, text_scale=0.5, zone=self.zonas[i], color=sv.Color(r=200, g=0, b=0), text_color=sv.Color.white(), text_padding=2, )
            #anotador_pz_mal.center = sv.Point(centros_zonas[i][0], centros_zonas[i][1])
            self.anotador_zonas.append(anotador_pz)
    
    def anotar_frame_zonas(self, frame, detecciones, modelo):
        annotated_frame = frame.copy()
        self.frames_preproc.append(frame)

        try:
            self.anteriores = guardar_centros_anteriores_v3(self.anteriores, detecciones.tracker_id, detecciones.xyxy, self.ult_mov_x, self.ult_mov_y, self.fps, def_centro=self.calc_centro)
            for id in self.ult_mov_x.keys():
                if id not in self.anteriores.keys():
                    del self.ult_mov_x[id]
            for id in self.ult_mov_y.keys():
                if id not in self.anteriores.keys():
                    del self.ult_mov_y[id]
            for id in self.ult_vel.keys():
                if id not in self.anteriores.keys():
                    del self.ult_vel[id]
            for id in self.ults_vel.keys():
                if id not in self.anteriores.keys():
                    del self.ults_vel[id]
        except:
            None

        if len(self.ult_vel) == 0:
            for key in self.anteriores.keys():
                self.ult_vel[key] = 0
                self.ult_mov_x[key] = 0
                self.ult_mov_y[key] = 0
                self.ults_vel[key] = [0]

        for key in self.anteriores.keys():
            self.ult_vel[key] = velocidad(self.ult_vel, key, self.anteriores, self.fps, self.tpo_calc_vel)
            self.ult_mov_x[key] = velocidad(self.ult_mov_x, key, self.anteriores, self.fps, self.tpo_calc_vel, 'x')
            self.ult_mov_y[key] = velocidad(self.ult_mov_y, key, self.anteriores, self.fps, self.tpo_calc_vel, 'y')
            try:
                self.ults_vel[key].append(velocidadv2(self.ults_vel, key, self.anteriores, self.fps, 0.3))
            except:
                self.ults_vel[key] = [0]

        for i in range(self.n_zonas):
            try:
                detections_i = detecciones[isin_polygon(detecciones.xyxy, self.anotador_zonas[i].zone.mask)]
            except:
                #print('1')
                detections_i = detecciones
        
            try:
                #print(isnot_zero_start(detections1.tracker_id, ult_vel, anteriores, video_info.fps, tpo_calc_vel))
                detections_i = detections_i[isnot_zero_start(detections_i.tracker_id, self.ult_vel, self.anteriores, self.fps, self.tpo_calc_vel)]
            except: 
                #print('2')
                None
            
            try:
                #print(self.min_max[i][1], self.min_max[i][0])
                #detections_i = detections_i[isbetween_sup_infv3(detections_i.tracker_id, self.ult_vel, self.min_max[i][1], self.min_max[i][0], self.ults_vel, detecciones.tracker_id)]
                detections_i = detections_i[isbetween_sup_infv2(detections_i.tracker_id, self.ult_vel, self.min_max[i][1], self.min_max[i][0], self.ults_vel)]
                #print(self.min_max[i][1], self.min_max[i][0])
            except:
                #print('3')
                None

            labels_i = []
            for bbox, _, confidence, class_id, tracker_id in detections_i:
                #labels_i.append(f"{self.ult_vel[tracker_id]:0.2f} p/s")
                labels_i.append(f"CORRIENDO")

            if (len(labels_i) >= 1) and (self.ocurre_evento == False):
                self.ocurre_evento = True 

            annotated_frame=self.box_annotator.annotate(
                scene=annotated_frame,
                detections=detections_i,
                labels=labels_i
                )
            
            #annotated_frame = self.anotador_zonas[i].annotate(annotated_frame)

            for id in detections_i.tracker_id:
                centros = self.anteriores[id]
                if len(centros) > 1:
                    if len(centros) < 2 * self.fps:
                        for j in range(1, len(centros)):
                            annotated_frame = sv.draw_line(annotated_frame, sv.Point(centros[j - 1][0], centros[j - 1][1]), sv.Point(centros[j][0], centros[j][1]), sv.Color(r=200, g=0, b=0), 2)
                    else:
                        for j in range(len(centros) - 2 * self.fps + 1, len(centros)):
                            annotated_frame = sv.draw_line(annotated_frame, sv.Point(centros[j - 1][0], centros[j - 1][1]), sv.Point(centros[j][0], centros[j][1]), sv.Color(r=200, g=0, b=0), 2)

        
        self.frames_postproc.append(annotated_frame)

        if self.guardar_evento and self.ocurre_evento:
            self.guardar_video(frame, annotated_frame)

        return annotated_frame
    
    def guardar_video(self, frame_pre, frame_post):
        if not self.guardando_evento:
            self.video_writer_pre = cv2.VideoWriter('C:\\Users\\eitan\\Pictures\\alta_velocidad_pre.mp4', cv2.VideoWriter_fourcc(*'mp4v'), self.fps, (self.frame_w, self.frame_h))
            self.video_writer_post = cv2.VideoWriter('C:\\Users\\eitan\\Pictures\\alta_velocidad_post.mp4', cv2.VideoWriter_fourcc(*'mp4v'), self.fps, (self.frame_w, self.frame_h))
            self.i = 0
            self.guardando_evento = True
            print('Guardando Evento Velocidad')
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
                print('Evento Velocidad Guardado')
                self.video_writer_pre.release()
                self.video_writer_post.release()
                self.guardando_evento = False
                self.ocurre_evento = False