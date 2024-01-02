import supervision as sv
from general import create_labels

#--------------------------------------------------------------------------------------------------------------------
# Creacion de la clase que se encarga de los contadores en un espacio
# Por mayores dudas de las funciones, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
#--------------------------------------------------------------------------------------------------------------------

class Objeto_Contadores:
    def __init__(self):
        self.n_contadores = 0
        self.contadores = []
        self.anotador_contadores = []
        self.frame_w = 0
        self.frame_h = 0
        #self.trigger_position = sv.Position.CENTER

        self.box_annotator = sv.BoxAnnotator(color=sv.Color(r=0, g=0, b=255), text_color=sv.Color.white(), thickness=1, text_thickness=1, text_scale=0.5)
        self.fps = 25
        self.show_bbox = True
        self.show_label = True

    def frame_wh(self, frame):
        self.frame_w = frame.shape[1]
        self.frame_h = frame.shape[0]

    def create_line_zones(self, line):
        self.n_contadores = len(line)
        for i in range(self.n_contadores):
            lz = sv.LineZone(start = sv.Point(line[i][0][0], line[i][0][1]), end = sv.Point(line[i][1][0], line[i][1][1]))
            self.contadores.append(lz)

    def create_line_zone_annotators(self, texto_in='Nro per ARR-ABA', texto_out='Nro per ABA-ARR'):
        for i in range(self.n_contadores):
            anotador_lz = sv.LineZoneAnnotator(thickness=1, text_thickness=1, text_scale=0.75, color = sv.Color.blue(), text_color=sv.Color.white(), text_padding=1, text_offset=1,
                                           custom_in_text=texto_in, custom_out_text=texto_out)
            self.anotador_contadores.append(anotador_lz)
        
    def anotar_frame(self, frame, detecciones, modelo):
        annotated_frame = frame
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
            self.anotador_contadores[i].annotate(annotated_frame, line_counter=self.contadores[i])
        return annotated_frame