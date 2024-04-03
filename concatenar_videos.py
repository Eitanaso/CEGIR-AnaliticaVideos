import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np

letra = 20
letra = 40
letra = 60
pos = letra + 10
izq = 70

source = [
  #'C:\\Users\\eitan\\Pictures\\comercio_ambulante_paseo_estacion.mp4',
  #'C:\\Users\\eitan\\Pictures\\comercio_ambulante_paseo_estacion.mp4',
  #'C:\\Users\\eitan\\Pictures\\comercio_ambulante_paseo_estacion.mp4',
  #'C:\\Users\\eitan\\Pictures\\comercio_ambulante_paseo_estacion.mp4',
  #'C:\\Users\\eitan\\Pictures\\comercio_ambulante_paseo_estacion.mp4',
  #'C:\\Users\\eitan\\Pictures\\comercio_ambulante_paseo_estacion.mp4',
  #'C:\\Users\\eitan\\Pictures\\comercio_ambulante_paseo_estacion.mp4',
  #'C:\\Users\\eitan\\Pictures\\comercio_ambulante_paseo_estacion.mp4',
  #'C:\\Users\\eitan\\Pictures\\comercio_ambulante_paseo_estacion.mp4',
  #'C:\\Users\\eitan\\Pictures\\comercio_ambulante_paseo_estacion.mp4',
  #'C:\\Users\\eitan\\Pictures\\comercio_ambulante_paseo_estacion.mp4',
  #'C:\\Users\\eitan\\Pictures\\comercio_ambulante_paseo_estacion.mp4',
  #'C:\\Users\\eitan\\Pictures\\comercio_ambulante_paseo_estacion.mp4',
  #'C:\\Users\\eitan\\Pictures\\comercio_ambulante_paseo_estacion.mp4',
  #'C:\\Users\\eitan\\Pictures\\comercio_ambulante_paseo_estacion.mp4',
  #'C:\\Users\\eitan\\Pictures\\comercio_ambulante_paseo_estacion.mp4',
  #'C:\\Users\\eitan\\Pictures\\comercio_ambulante_paseo_estacion.mp4',
  #'C:\\Users\\eitan\\Pictures\\comercio_ambulante_paseo_estacion.mp4',
  #'C:\\Users\\eitan\\Pictures\\comercio_ambulante_paseo_estacion.mp4',
  #'C:\\Users\\eitan\\Pictures\\comercio_ambulante_paseo_estacion.mp4',
  #'C:\\Users\\eitan\\Pictures\\comercio_ambulante_paseo_estacion.mp4',
  #'C:\\Users\\eitan\\Pictures\\comercio_ambulante_paseo_estacion.mp4',
  #'C:\\Users\\eitan\\Pictures\\comercio_ambulante_paseo_estacion.mp4',
  #'C:\\Users\\eitan\\Pictures\\comercio_ambulante_paseo_estacion.mp4',
  'C:\\Users\\eitan\\Desktop\\tests\\paseo_estacion_loop.mp4',
  'C:\\Users\\eitan\\Desktop\\tests\\paseo_estacion_loop.mp4',
  'C:\\Users\\eitan\\Desktop\\tests\\paseo_estacion_loop.mp4',
  'C:\\Users\\eitan\\Desktop\\tests\\paseo_estacion_loop.mp4',
  'C:\\Users\\eitan\\Desktop\\tests\\paseo_estacion_loop.mp4',
  'C:\\Users\\eitan\\Desktop\\tests\\paseo_estacion_loop.mp4',
  'C:\\Users\\eitan\\Desktop\\tests\\paseo_estacion_loop.mp4',
  'C:\\Users\\eitan\\Desktop\\tests\\paseo_estacion_loop.mp4',
  'C:\\Users\\eitan\\Desktop\\tests\\paseo_estacion_loop.mp4',
  'C:\\Users\\eitan\\Desktop\\tests\\paseo_estacion_loop.mp4',
  'C:\\Users\\eitan\\Desktop\\tests\\paseo_estacion_loop.mp4',
  'C:\\Users\\eitan\\Desktop\\tests\\paseo_estacion_loop.mp4',
]
target = 'd:\\Descargas\\paseo_estacion_loop_12h.mp4'


cap = cv2.VideoCapture(source[0])
ret, frame = cap.read()
h, w, _ = frame.shape
tamano = frame.shape
fps = 25

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(target, fourcc, fps, (w, h))

for i in range(len(source)):
  path = source[i]
  cap = cv2.VideoCapture(path)
  print(i)

  while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
      break
    video_writer.write(frame)



video_writer.release()
cap.release()