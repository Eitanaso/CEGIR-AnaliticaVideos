import cv2
from datetime import datetime
import argparse
import os

#--------------------------------------------------------------------------------------------------------------------
# Guardado de videos grabados en tiempo real
# Codigo para la conexion a una camara creado por Luis Escares y modificado por Eitan Hasson Arellano
#--------------------------------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='Guardar un video en vivo')
parser.add_argument('--tpo', help='Tiempo a guardar del video en vivo.', required=True, type=int)
parser.add_argument('--fps', help='FPS de la camara', required=False, default=25)
parser.add_argument('--camara', help='Camara a utilizar', required=False, default=r'rtsp://admin:Cafa2414$@10.0.10.182:554/0/profile2/media.smp')
args = vars(parser.parse_args())

# Connect to RTSP stream
#rtsp_url = args['camara']
SOURCE_VIDEO_PATH = r'C:\Users\eitan\Pictures\comercio_ambulante_paseo_estacion.mp4'
rtsp_url = SOURCE_VIDEO_PATH
ahora = datetime.now()
carpeta = f'{ahora.year}_{ahora.month}_{ahora.day}_{ahora.hour}_{ahora.minute}_{ahora.second}'
path = 'C:\\Users\\eitan\\Pictures\\comercio_ambulante_detectado\\'
isExist = os.path.exists(path+carpeta)
if not isExist:
    os.makedirs(path+carpeta)
cap = cv2.VideoCapture(rtsp_url)
#cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)

ret, frame = cap.read()
h, w, _ = frame.shape
fps = args['fps']

#fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#video_writer = cv2.VideoWriter(TARGET_VIDEO_PATH, fourcc, fps, (w, h))

i = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (w, h))
    #video_writer.write(frame)
    ahora2 = datetime.now()
    tiempo = f'\\{ahora2.hour}_{ahora2.minute}_{ahora2.second}'
    TARGET_VIDEO_PATH = path + carpeta + tiempo + '.jpg'
    if i % 2*fps == 0:
        #print('jfdjdf')
        cv2.imwrite(TARGET_VIDEO_PATH, frame)
    i += 1
    if i > args['tpo'] * fps:
        break
#video_writer.release()
cap.release()
