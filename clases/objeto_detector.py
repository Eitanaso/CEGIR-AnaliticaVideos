import supervision as sv
from general import create_labels

#--------------------------------------------------------------------------------------------------------------------
# Creacion de la clase que se encarga solo de las detecciones en un video
# Por mayores dudas de las funciones, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
#--------------------------------------------------------------------------------------------------------------------

class Objeto_Detector:
    def __init__(self):
        self.color = sv.Color(r=0, g=255, b=0)
        self.text_color = sv.Color.white()
        self.thickness = 1
        self.text_thickness = 1
        self.text_scale = 0.5

        self.box_annotator = None
        self.skip_label = True

    def create_box_annotator(self):
        self.box_annotator = sv.BoxAnnotator(color = self.color, 
                                             text_color = self.text_color, 
                                             thickness = self.thickness, 
                                             text_thickness = self.text_thickness, 
                                             text_scale = self.text_scale)
        
    def set_skip_label(self, valor):
        self.skip_label = valor
        
    def anotar_frame(self, frame, detecciones, modelo):
        annotated_frame = frame
        if self.skip_label:
            annotated_frame = self.box_annotator.annotate(scene = annotated_frame, detections = detecciones, skip_label = self.skip_label)
        else:
            labels = create_labels(detecciones, modelo)
            annotated_frame = self.box_annotator.annotate(scene = annotated_frame, detections = detecciones, labels = labels)
        return annotated_frame