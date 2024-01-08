import math
import numpy as np

from funciones.general import bbox_centros

def guardar_centros_anteriores_v2(anteriores, tracker_id, bbox, def_centro: str = 'centro',
                                  width: int = 1920, height: int = 1080):
  # version futura, agregar flag tal que, si lleva mas de x tiempo sin encontrar la deteccion, borrarlo del diccionario
  resultado = anteriores
  centros_bboxs = bbox_centros(bbox)
  for i in range(len(tracker_id)):
    centro_i = centros_bboxs[i]
    id_i = tracker_id[i]
    try:
      resultado[id_i].append(centro_i)
    except:
      resultado[id_i] = [centro_i]
  # actualizar los centros de las detecciones que no se encontraron, para estar de acuerdo a los frames que existen
  # se perdio el item, pero si se retoma, aun existe su posicion en los frames perdidos
  # lo mas simple es dejarlo detenido en ese tiempo, a futuro se podría analizar el agregar algún flag que indique que una deteccion se perdio
  # para luego usar el flag una vez se re encontro, revisar cuantos frames pasaron y aproximar los centros avanzando, sin embargo es mas complejo
  for i in list(resultado.keys()):
    if i not in tracker_id:
      resultado[i].append(resultado[i][-1])
  borrar = []
  for id in resultado.keys():
    if resultado[id][-1][0] > width or resultado[id][-1][0] < 0 or resultado[id][-1][1] < 0 or resultado[id][-1][1] > height:
      borrar.append(id)
  for id in borrar:
    del resultado[id]
  return resultado

def find_angle(x, y):
    tan_alpha = y / x
    alpha = math.atan(tan_alpha)  # Calculate the angle in radians
    alpha_degrees = math.degrees(alpha)  # Convert the angle to degrees
    return alpha_degrees

def calcular_angulos(ultimos_angulos, centros_anteriores, ids, frame_rate):
  for id in ids:
    centros_id = centros_anteriores[id]
    frames_detectado = len(centros_id)
    if frames_detectado % frame_rate == 0:
      seg_detectado = frames_detectado // frame_rate
      if seg_detectado > 0:
        centro_seg_anterior = centros_id[(seg_detectado - 1) * frame_rate]
        centro_seg_actual = centros_id[(seg_detectado * frame_rate) - 1]
        #print(centro_seg_anterior, centro_seg_actual)
        if (centro_seg_anterior != centro_seg_actual).all():
          dx = np.abs(centro_seg_actual[0] - centro_seg_anterior[0])
          dy = np.abs(centro_seg_actual[1] - centro_seg_anterior[1])
          if dx != 0:
            angulo_actual = find_angle(dx, dy)
          else:
            angulo_actual = 90
          try:
            ultimos_angulos[id].append(angulo_actual)
          except:
            ultimos_angulos[id] = [angulo_actual]
  return ultimos_angulos

def get_angulo_label(ultimos_angulos, id):
  try:
    return np.round(ultimos_angulos[id][-1], 2)
  except:
    return 'N/A'

def get_diff_angulos(ultimos_angulos, ids, diff=50, tpo_prev=1):
  res = []
  for id in ids:
    try:
      sus_angulos = ultimos_angulos[id]
      if len(sus_angulos) > tpo_prev:
        angulo_actual = sus_angulos[-1]
        diff_mayor = False
        for i in range(len(sus_angulos) - 2, len(sus_angulos) - 2 - tpo_prev, -1):
          angulo_comparado = sus_angulos[i]
          if np.abs(angulo_actual - angulo_comparado) > diff:
            diff_mayor = True
            break
        res.append(diff_mayor)
      else:
        res.append(False)
    except:
      res.append(False)
  return np.array(res)