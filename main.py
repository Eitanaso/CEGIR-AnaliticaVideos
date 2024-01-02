import argparse
from detectar import run_detect
from general import get_video, get_model

#--------------------------------------------------------------------------------------------------------------------
# Creacion de variables y funcion main para el control de los distintos tipos de analisis a realizar en videos
# Por mayores dudas de las variables o la funcion, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
#--------------------------------------------------------------------------------------------------------------------

# camara, modelo, clases, fps, tipo de tarea (deteccion, conteo, personas detenidas, velocidad), 
# puntos de los objetos a crear para la tarea (linea(s) para conteo, zona(s) para personas detenidas/velocidades), limites para velocidades
# colores de los objetos creados, nombres de los objetos a mostrar
# extras: mostrar etiquetas, mostrar trazas

parser = argparse.ArgumentParser(description='Ejecutar la deteccion del modelo')
#parser.add_argument('--tpo', help='Tiempo a guardar del video en vivo.', required=True, type=int)
#parser.add_argument('--fps', help='FPS de la camara', required=False, default=25)
#parser.add_argument('--camara', help='Camara a utilizar', required=False, default=r'rtsp://admin:Cafa2414$@10.0.10.182:554/0/profile2/media.smp')
#args = vars(parser.parse_args())


SOURCE_VIDEO_PATH = r'C:\Users\eitan\Pictures\comercio_ambulante_paseo_estacion.mp4'
#TARGET_VIDEO_PATH = r'C:\Users\eitan\Pictures\comercio_ambulante_detectado.mp4'

rtsp_url = SOURCE_VIDEO_PATH
MODEL = "yolov8n.pt"
selected_classes = [0,2]
fps = 25

procesamiento = {
    'solo_mostrar': False,
    'solo_detector': False,
    'mostrar_contadores': True,
    'lineas_contadores': [
        #[(125, 333), (483, 195)],
        [(0, 430), (160, 334)],
    ],
    'mostrar_estacionados': False,
    'zonas_estacionados': [
        [(40, 188), (187, 337), (371, 412), (408, 333), (265, 273), (131, 167)],
        [(427, 256), (579, 301), (706, 325), (703, 242), (578, 218), (476, 181)],
    ],
    'centros_zonas_estacionados': [(75, 195), (480, 185)],
    'mostrar_velocidades': False
}

def main(rstp_url, model, clases, fps, procesamiento):
    cap = get_video(rstp_url)
    model = get_model(model)
    run_detect(cap, model, clases, fps, procesamiento)

if __name__ == '__main__':
    main(rtsp_url, MODEL, selected_classes, fps, procesamiento)