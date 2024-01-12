import supervision as sv
from clases.objeto_detector import Objeto_Detector
from clases.objeto_estacionados import Objeto_Estacionados
from clases.objeto_contadores import Objeto_Contadores
from clases.objeto_trayectoria import Objeto_Trayectorias
from clases.objeto_velocidades import Objeto_Velocidades

#--------------------------------------------------------------------------------------------------------------------
# Creacion de una clase general que organiza el/los analisis deseado/s
# Por mayores dudas de la clase y sus funciones, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
#--------------------------------------------------------------------------------------------------------------------

class Objeto_Global:
    def __init__(self, fps):
        self.bt_track_thresh = 0.15
        self.bt_track_buffer_mult = 2
        self.bt_match_thresh = 0.8
        self.bt_frame_rate = fps

        self.byte_tracker = None

        self.solo_detector = False
        self.contadores = False
        self.estacionados = False
        self.trayectorias = False
        self.velocidades = False
        self.velocidad_por_zonas = False

        self.objeto_Detector = None
        self.objeto_Contadores = None
        self.objeto_Estacionados = None
        self.objeto_Trayectorias = None
        self.objeto_Velocidades = None

        self.box_annotators = []
        self.line_annotators = []
        self.polygon_zone_annotators = []
        self.polygone_zone_annotators_vel = []

    def __str__(self):
        return f"Objeto Global que reune los distintos trabajos a realizar en el video" #f"{self.byte_tracker}(hola)"
    
    def set_byte_tracker_track_threshold(self, num):
        self.bt_track_thresh = num

    def set_byte_tracker_track_buffer_multiplicator(self, num):
        self.bt_track_buffer_mult = num
    
    def set_byte_tracker_match_threshold(self, num):
        self.bt_match_thresh = num
    
    def set_byte_tracker_frame_rate(self, num):
        self.bt_frame_rate = num
    
    def create_byte_tracker(self):
        self.byte_tracker = sv.ByteTrack(track_thresh = self.bt_track_thresh, 
                                         track_buffer = self.bt_frame_rate * self.bt_track_buffer_mult, 
                                         match_thresh = self.bt_match_thresh, 
                                         frame_rate = self.bt_frame_rate)
        
    def create_detector(self):
        self.solo_detector = True
        self.objeto_Detector = Objeto_Detector()
        self.objeto_Detector.create_box_annotator()

    def create_estacionados(self, frame, zonas, centros_zonas):
        self.estacionados = True
        self.objeto_Estacionados = Objeto_Estacionados()
        self.objeto_Estacionados.frame_wh(frame)
        self.objeto_Estacionados.create_polygone_zones(zonas)
        self.objeto_Estacionados.create_polygone_zone_annotators(centros_zonas)
    
    def create_contadores(self, lineas_contadores):#, guardar_archivo):
        self.contadores = True
        self.objeto_Contadores = Objeto_Contadores()#guardar_archivo)
        self.objeto_Contadores.create_line_zones(lineas_contadores)
        self.objeto_Contadores.create_line_zone_annotators()

    def create_trayectorias(self, frame, guardar_evento):
        self.trayectorias = True
        self.objeto_Trayectorias = Objeto_Trayectorias(guardar_evento)
        self.objeto_Trayectorias.frame_wh(frame)
    
    def create_velocidades(self, frame, por_zonas, zonas, min_max, guardar_evento):
        self.velocidades = True
        self.velocidad_por_zonas = por_zonas
        self.objeto_Velocidades = Objeto_Velocidades(guardar_evento)
        if por_zonas:
            self.objeto_Velocidades.frame_wh(frame)
            self.objeto_Velocidades.create_polygone_zones(zonas, min_max)
            self.objeto_Velocidades.create_polygone_zone_annotators()











