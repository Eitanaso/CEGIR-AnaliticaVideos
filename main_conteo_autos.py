import argparse
from detectar_conteo_autos import run_detect, detect
from general import get_video, get_model
from clases.objeto_global import Objeto_Global

from datetime import datetime

import cv2



parser = argparse.ArgumentParser(description='Ejecutar la deteccion del modelo')
#parser.add_argument('--tpo', help='Tiempo a guardar del video en vivo.', required=True, type=int)
#parser.add_argument('--fps', help='FPS de la camara', required=False, default=25)
#parser.add_argument('--camara', help='Camara a utilizar', required=False, default=r'rtsp://admin:Cafa2414$@10.0.10.182:554/0/profile2/media.smp')
#args = vars(parser.parse_args())


SOURCE_VIDEO_PATH = r'C:\\CEGIR-AnaliticaVideos-new_main\\comercio_ambulante_paseo_estacion.mp4'
rtsp_url = SOURCE_VIDEO_PATH
MODEL = "yolov8x.pt"
fijas = {
    'solo_mostrar': False,
    'mostrar_video': True,
    'contador': True, 
    'pos_texto_contador': [(50, 30), (50, 60)],
    'color_contador': (0, 255, 0),
    'model': MODEL,
}
datos = {
    'ID_cam': '001', 
    'pos_cam': 'Plaza_Argentina', 
    'dia': '2023_11_13', 
    'hora': '08_09_22'
}
variables = {
    'selected_classes': 2,
    'fps': 25,
    'linea_contador': [(160, 334), (468, 185)],
    'texto_contador': ['Auto in-out', 'Auto out-in'],
    'periodicidad_contador': 10,
    'nombre_contador': 'contador12h_2',
    'direccion_archivo': 'C:\\CEGIR-AnaliticaVideos-new_main\\conteo_autos\\',
}
procesamiento = {
    'var_fijas': fijas,
    'info': datos,
    'var': variables,
}

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Mostrar el punto seleccionado
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        # Mostrar las coordenadas del punto
        print("Coordenadas del punto:", x, y)
        # Guardar las coordenadas en una lista
        puntos.append((x, y))
        # Refrescar la imagen
        #cv2.imshow('image', img)

def main(rstp_url, model, procesamiento):
    # datetime object containing current date and time
    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("inicio =", dt_string)

    cap = get_video(rstp_url)
    ret, frame = cap.read()
    global img
    img = frame.copy()
    cv2.imshow('Seleccion de linea contador', img)
    global puntos
    puntos = []
    cv2.setMouseCallback('Seleccion de linea contador', click_event)
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    print(puntos)
    procesamiento['var']['linea_contador'] = puntos


    model = get_model(model)
    run_detect(cap, model, procesamiento)

    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("fin =", dt_string)

if __name__ == '__main__':

    main(rtsp_url, MODEL, procesamiento)