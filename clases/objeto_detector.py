import supervision as sv
from general import create_labels
import cv2
from scipy.stats import mode
import numpy as np
from sklearn.cluster import KMeans

#--------------------------------------------------------------------------------------------------------------------
# Creacion de la clase que se encarga solo de las detecciones en un video
# Por mayores dudas de las funciones, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
#--------------------------------------------------------------------------------------------------------------------

class Objeto_Detector:
    def __init__(self):
        self.color = sv.Color(r=255, g=0, b=0)
        self.text_color = sv.Color.white()
        self.thickness = 2
        self.text_thickness = 1
        self.text_scale = 0.5

        self.box_annotator = None
        self.skip_label = False

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
            label_i = []
            #carabinero = []
            '''overoles = []
            for i in range(len(labels)):
                det = detecciones[i]
                #if labels[i] == 'person [1]' or labels[i] == 'person [4]' or labels[i] == 'person [5]' or labels[i] == 'person [3]' or labels[i] == 'person [2]':
                    #x1, y1, x2, y2 = det.xyxy[0]
                    #asd = frame[int(y1):int(y2), int(x1):int(x2)]
                    #asd_mean = np.sum(asd, axis=(0,1))
                    #cv2.imshow('area', asd)
                    #print(labels[i], asd_mean, np.mean(asd, axis=(0,1)), np.std(asd, axis=(0,1)))
                x1, y1, x2, y2 = det.xyxy[0]
                per = frame[int(y1):int(y2), int(x1):int(x2)]
                per_prom = np.mean(per, axis=(0, 1))
                #if (per_prom[0] < per_prom[1] - 15) and (per_prom[0] < per_prom[2] - 15) and (abs(per_prom[1] - per_prom[2]) <= 7):
                #if (per_prom[0] < per_prom[1] - 10) and (per_prom[0] < per_prom[2] - 10) and (abs(per_prom[1] - per_prom[2]) <= 15):
                    #carabinero.append(True)
                #if (per_prom[0] > per_prom[1] + 7) and (per_prom[1] > per_prom[2] + 7):
                if (per_prom[0] > per_prom[1] + 5) and (per_prom[1] > per_prom[2] + 5):
                    overoles.append(True)
                    print(labels[i], per_prom)
                    label_i.append(labels[i])
                else:
                    #carabinero.append(False)
                    overoles.append(False)
            #detecciones = detecciones[np.array(carabinero)]
            detecciones = detecciones[np.array(overoles)]
            labels = label_i.copy()'''
            annotated_frame = self.box_annotator.annotate(scene = annotated_frame, detections = detecciones, labels = labels, skip_label=True)
        return annotated_frame