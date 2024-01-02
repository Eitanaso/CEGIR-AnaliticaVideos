# Importar librerias utiles
import numpy as np
from funciones.general import bbox_centros

#--------------------------------------------------------------------------------------------------------------------
# Creacion de funciones utiles para el analisis de personas estacionadas en un espacio definido
# Por mayores dudas de las funciones, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
#--------------------------------------------------------------------------------------------------------------------

# Funcion que se utiliza para guardar los centros de las detecciones realizadas
def guardar_centros_anteriores_v3(anteriores: dict, tracker_id: np.ndarray, bbox: np.ndarray, 
                                  velocidades_x: dict, velocidades_y: dict, fps: int, def_centro: str = 'centro',
                                  width: int = 1920, height: int = 1080) -> dict:
  '''
  Funcion que guarda en un diccionario los centros definidos de las detecciones del modelo. Si se da el caso que en un frame
  una deteccion que estaba en el diccionario se perdio, intenta predecir la posicion del centro de acuerdo a la velocidad
  relativa que llevara la misma en x e y.
  Entrega el diccionario actualizado con la posicion del centro de cada deteccion que hay dentro del video.
  Se utiliza para guardar los centros de una deteccion, principalmente, para calcular la velocidad del objeto detectado.

  Variables:
  - anteriores (dict): diccionario actualizable con los centros de las detecciones
  - tracker_id (np.ndarray): lista de identificaciones de los objetos detectados por el modelo
  - bbox (np.ndarray): lista de bboxes de los objetos detectados por el modelo
  - velocidades_x (dict): diccionario con la ultima distancia recorrida en x en 1 segundo de cada deteccion
  - velocidades_y (dict): diccionario con la ultima distancia recorrida en y en 1 segundo de cada deteccion
  - fps (int): valor que indica los FPS de los videos analizados (los que graba la camara)
  - def_centro (str): texto que indica cual sera la definicion del centro que se utilizara en este listado de centros de detecciones. 
  Hasta la fecha, las unicas opciones son 'centro' (opcion por defecto) y 'centro-sup'

  Ante mas dudas de esta funcion, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
  '''
  resultado = anteriores
  centros_bboxs = bbox_centros(bbox, def_centro)
  for i in range(len(tracker_id)):
    centro_i = centros_bboxs[i]
    id_i = tracker_id[i]
    # Verificar si es una deteccion existente o nueva
    try:
      resultado[id_i].append(centro_i)
    except:
      resultado[id_i] = [centro_i]
  # Actualizar los centros de las detecciones que no se encontraron, para estar de acuerdo a los frames que existen
  # Se perdio el item, pero si se retoma, aun existe su posicion en los frames perdidos
  for i in list(resultado.keys()):
    if i not in tracker_id:
      resultado[i].append([resultado[i][-1][0] + (velocidades_x[i] / fps), resultado[i][-1][1] + (velocidades_y[i] / fps)])
  # Borrar una deteccion si su centro calculado esta fuera del rango de la imagen
  # Esto se realiza para no llenar el diccionario con información poco relevante
  borrar = []
  for id in resultado.keys():
    if resultado[id][-1][0] > width or resultado[id][-1][0] < 0 or resultado[id][-1][1] < 0 or resultado[id][-1][1] > height:
      borrar.append(id)
  for id in borrar:
    del resultado[id]
  return resultado

# Funcion que se utiliza para calcular la velocidad de una deteccion
def get_velocidad(positions: list, dist: int, total: str = 'total') -> float:
  '''
  Funcion que calcula la velocidad de una deteccion segun el desplazamiento realizado y
  el tipo de velocidad que sea necesario.
  Entrega un valor de velocidad medido de acuerdo a la variable total, la cual puede ser la velocidad normal,
  la velocidad relativa en el eje x o en el eje y.
  Se utiliza para obtener las distintas velocidades de una deteccion para representarlo en un video.

  Variables:
  - positions (list): lista con las posiciones de los centros de una deteccion
  - dist (int): valor que indica el lugar desde el que se medira el desplazamiento realizado. Se ve definido
  por el tiempo multiplicado por los FPS (s * fps)
  - total (str): texto que indica el tipo de velocidad que se calculara. Las opciones son 
  'total', 'x' e 'y'. Por defecto se tiene 'total', la cual se utiliza para calcular la velocidad normal
  mediante su desplazamiento en x e y. La opcion 'x' o 'y' se utilizan en casos mas complejos, e indican
  que la funcion entregue la velocidad relativa en el eje elegido

  Ante mas dudas de esta funcion, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
  '''
  start_x, start_y = positions[-(dist + 1)]
  end_x, end_y = positions[-1]

  delta_x = end_x - start_x
  delta_y = end_y - start_y

  if total == 'total':
    return np.sqrt(delta_x**2 + delta_y**2)
  elif total == 'x':
    return delta_x
  elif total == 'y':
    return delta_y


def velocidad(ultima_velocidad, tracker_id, anteriores, fps: int, tpo: int, total: str = 'total') -> float:
  '''
  Funcion que
  Entrega
  Se utiliza

  Variables:
  - ultima_velocidad ():
  - tracker_id ():
  - anteriores ():
  - fps (int):
  - tpo (int):
  - total (str): indica si se desea calcular la velocidad de todo, o solo la rapidez en x o y

  Ante mas dudas de esta funcion, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
  '''
  try:
    resultado = ultima_velocidad[tracker_id]
  except:
    resultado = 0
  if total == 'total':
    if (len(anteriores[tracker_id]) % int(tpo * fps + 1) == 0) and (len(anteriores[tracker_id]) > 0): #quizas da problema con el dist+1 de arriba
      centros_id = anteriores[tracker_id]
      vel = get_velocidad(centros_id, int(tpo * fps))
      resultado = vel / tpo
  elif (total == 'x') or (total == 'y'):
    if (len(anteriores[tracker_id]) % int(tpo * fps + 1) == 0) and (len(anteriores[tracker_id]) > 0): #quizas da problema con el dist+1 de arriba
      centros_id = anteriores[tracker_id]
      if total == 'x':
        vel = get_velocidad(centros_id, int(tpo * fps), total='x')
      elif total == 'y':
        vel = get_velocidad(centros_id, int(tpo * fps), total='y')
      resultado = vel / tpo
    elif (len(anteriores[tracker_id]) < int(tpo * fps)) and (len(anteriores[tracker_id]) > 1):
      centros_id = anteriores[tracker_id]
      if total == 'x':
        vel = get_velocidad(centros_id, 1, total='x')
      elif total == 'y':
        vel = get_velocidad(centros_id, 1, total='y')
      resultado = vel * fps
  #ultima_velocidad[tracker_id] = resultado
  return resultado

def velocidadv2(ultima_velocidad, tracker_id, anteriores, fps, tpo, total='total') -> float:
  '''
  Funcion que
  Entrega
  Se utiliza

  Variables:
  - ultima_vel
  -
  - total (str): indica si se desea calcular la velocidad de todo, o solo la rapidez en x o y

  Ante mas dudas de esta funcion, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
  '''
  try:
    resultado = ultima_velocidad[tracker_id][-1]
  except:
    resultado = 0
  if total == 'total':
    if (len(anteriores[tracker_id]) % int(tpo * fps + 1) == 0) and (len(anteriores[tracker_id]) > 0): #quizas da problema con el dist+1 de arriba
      centros_id = anteriores[tracker_id]
      vel = get_velocidad(centros_id, int(tpo * fps))
      resultado = vel / tpo
  elif (total == 'x') or (total == 'y'):
    if (len(anteriores[tracker_id]) % int(tpo * fps + 1) == 0) and (len(anteriores[tracker_id]) > 0): #quizas da problema con el dist+1 de arriba
      centros_id = anteriores[tracker_id]
      if total == 'x':
        vel = get_velocidad(centros_id, int(tpo * fps), total='x')
      elif total == 'y':
        vel = get_velocidad(centros_id, int(tpo * fps), total='y')
      resultado = vel / tpo
    elif (len(anteriores[tracker_id]) < int(tpo * fps)) and (len(anteriores[tracker_id]) > 1):
      centros_id = anteriores[tracker_id]
      if total == 'x':
        vel = get_velocidad(centros_id, 1, total='x')
      elif total == 'y':
        vel = get_velocidad(centros_id, 1, total='y')
      resultado = vel * fps
  #ultima_velocidad[tracker_id] = resultado
  return resultado

def isnot_zero_start(dets_ids, vels, anteriores, fps: int, tpo: int) -> np.ndarray:
  '''
  Funcion que
  Entrega
  Se utiliza

  Variables:
  - dets_ids ():
  - vels ():
  - anteriores ():
  - fps (int):
  - tpo (int):

  Ante mas dudas de esta funcion, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
  '''
  res = []
  for id in dets_ids:
    valor = False
    vel = vels[id]
    if vel == 0 and (len(anteriores[id]) > 1*fps * tpo + 1):
      #print(vel)
      #print(id, len(anteriores[id]), 1*fps*tpo+1, vel)
      valor = True
    if vel > 0:
      #print(vel)
      valor = True
    res.append(valor)
  return np.array(res)

def isbetween_sup_inf(dets_ids, vels, sup: float, inf: float) -> np.ndarray:
  '''
  Funcion que
  Entrega
  Se utiliza

  Variables:
  - dets_ids ():
  - vels ():
  - sup (float):
  - inf (float):

  Ante mas dudas de esta funcion, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
  '''
  res = []
  #print('a')
  #dets_ids = dets.tracker_id
  for id in dets_ids:
    #print('b')
    vel = vels[id]
    #print('c')
    if (vel > sup) or (vel < inf):
      #print('d')
      res.append(True)
    else:
      #print('e')
      res.append(False)
  #print('f')
  return np.array(res)

def compara(x, y, p) -> bool:
  '''
  Funcion que
  Entrega
  Se utiliza

  Variables:
  - x ():
  - y ():
  - p ():

  Ante mas dudas de esta funcion, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
  '''
  res = False
  if np.abs(x/y) <= p:
    res = True
  return res

def isbetween_sup_infv2(dets_ids, vels, sup: float, inf: float, ults_vels) -> np.ndarray:
  '''
  Funcion que
  Entrega
  Se utiliza

  Variables:
  -
  -
  -

  Ante mas dudas de esta funcion, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
  '''
  res = []
  #print('a')
  #dets_ids = dets.tracker_id
  for id in dets_ids:
    #print('b')
    vel = vels[id]
    vel_1 = ults_vels[id][-1]
    vel_2 = ults_vels[id][-2]
    vel_3 = ults_vels[id][-3]
    #print('c')
    if ((vel > sup) or (vel < inf)):
      if compara(vel_1, vel_2, 0.4) and compara(vel_2, vel_3, 0.4):
        #print('d')
        res.append(True)
      elif vel < inf and vel_1 < inf and vel_2 < inf and vel_3 < inf:
        res.append(True)
      else:
        res.append(True)
    else:
      #print('e')
      res.append(False)
  #print('f')
  return np.array(res)

def isbetween_sup_infv3(dets_ids, vels, sup: float, inf: float, ults_vels, dets_est) -> np.ndarray:
  '''
  Funcion que
  Entrega
  Se utiliza

  Variables:
  -
  -
  -

  Ante mas dudas de esta funcion, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
  '''
  res = []
  #print('a')
  #dets_ids = dets.tracker_id
  for id in dets_ids:
    #print('b')
    vel = vels[id]
    vel_1 = ults_vels[id][-1]
    vel_2 = ults_vels[id][-2]
    vel_3 = ults_vels[id][-3]
    #print('c')
    if ((vel > sup) or (vel < inf)):
      if compara(vel_1, vel_2, 0.4) and compara(vel_2, vel_3, 0.4):
        #print('d')
        res.append(True)
      elif vel < inf and vel_1 < inf and vel_2 < inf and vel_3 < inf:
        res.append(True)
      else:
        res.append(True)
    elif id in dets_est:
      res.append(True)
    else:
      #print('e')
      res.append(False)
  #print('f')
  return np.array(res)
