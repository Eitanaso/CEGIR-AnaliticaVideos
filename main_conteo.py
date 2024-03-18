import argparse
from detectar_conteo import run_detect, detect
from general import get_video, get_model
from clases.objeto_global import Objeto_Global

parser = argparse.ArgumentParser(description='Ejecutar la deteccion del modelo')
#parser.add_argument('--tpo', help='Tiempo a guardar del video en vivo.', required=True, type=int)
#parser.add_argument('--fps', help='FPS de la camara', required=False, default=25)
#parser.add_argument('--camara', help='Camara a utilizar', required=False, default=r'rtsp://admin:Cafa2414$@10.0.10.182:554/0/profile2/media.smp')
#args = vars(parser.parse_args())


SOURCE_VIDEO_PATH = r'C:\Users\eitan\Pictures\comercio_ambulante_paseo_estacion.mp4'
rtsp_url = SOURCE_VIDEO_PATH
MODEL = "yolov8x.pt"
fijas = {
    'solo_mostrar': False,
    'mostrar_video': True,
    'contador': True, 
    'pos_texto_contador': [(50, 280), (50, 310)],
    'color_contador': (0, 255, 0),
}
datos = {
    'ID_cam': '001', 
    'pos_cam': 'Plaza_Argentina', 
    'dia': '2023_11_13', 
    'hora': '16_09_22'
}
variables = {
    'selected_classes': 0,
    'fps': 25,
    'linea_contador': [(160, 334), (468, 185)],
    'texto_contador': ['Per ab-arr', 'Per arr-ab'],
    'periodicidad_contador': 30,
    'nombre_contador': 'contador',
    'direccion_archivo': 'C:\\Users\\eitan\\Desktop\\tests\\',
}
procesamiento = {
    'var_fijas': fijas,
    'info': datos,
    'var': variables,
}

def main(rstp_url, model, procesamiento):
    cap = get_video(rstp_url)
    model = get_model(model)
    run_detect(cap, model, procesamiento)

if __name__ == '__main__':

    main(rtsp_url, MODEL, procesamiento)