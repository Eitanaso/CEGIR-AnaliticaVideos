# Importar librerias utiles
import numpy as np

#--------------------------------------------------------------------------------------------------------------------
# Creacion de funciones utiles para distintas tareas
# Por mayores dudas de las funciones, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
#--------------------------------------------------------------------------------------------------------------------

# Funcion para encontrar el centro definido de una bbox
def centro(bbox: np.ndarray, def_centro: str = 'centro') -> np.ndarray:
  '''
  Funcion que calcula la posicion del centro de una bbox de acuerdo a la definicion dada.
  Entrega los 2 puntos del centro como una lista (x, y).
  Se utiliza para obtener el centro de una bbox por si es necesario hacer algo con este.

  Variables:
  - bbox (np.ndarray): lista de las posiciones x,y de la bbox de una deteccion realizada por el modelo
  - def_centro (str): texto que indica el punto de la bbox desde el cual se considera que la deteccion esta dentro del poligono. 
  Hasta la fecha, las unicas opciones son 'centro' (opcion por defecto) y 'centro-sup'

  Ante mas dudas de esta funcion, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
  '''
  if def_centro == 'centro':
    x_c = int((bbox[0] + bbox[2]) / 2)
    y_c = int((bbox[1] + bbox[3]) / 2)
  elif def_centro == 'centro-sup':
    x_c = int((bbox[0] + bbox[2]) / 2)
    y_c = int(min(bbox[1], bbox[3]))
  return np.array([x_c, y_c])

# Funcion para revisar si las detecciones estan en el poligono
def isin_polygon(det_box: np.ndarray, mask_poli: np.ndarray, bbox_dentro: str = 'centro') -> np.ndarray:
  '''
  Funcion que revisa si el centro de las detecciones recibidas se encuentran dentro de un poligono definido. 
  Entrega una lista con valores boleanos que representan si la deteccion se encuentra dentro o fuera del poligono.
  Se utiliza para guardar solo las detecciones dentro del poligono definido.

  Variables:
  - det_box (np.ndarray): lista de las posiciones x,y de las bbox detectadas por el modelo
  - mask_poli (np.ndarray): mascara que representa la zona dentro de la cual se esta analizando las detecciones
  - bbox_dentro (str): texto que indica el punto de la bbox desde el cual se considera que la deteccion esta dentro del poligono. 
  Hasta la fecha, las unicas opciones son 'centro' (opcion por defecto) y 'centro-sup'

  Ante mas dudas de esta funcion, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
  '''
  res = []
  for bbox in det_box:
    coord_centro = centro(bbox, def_centro=bbox_dentro)
    x_c = coord_centro[0]
    y_c = coord_centro[1]
    if mask_poli[y_c][x_c]:
      res.append(True)
    else:
      res.append(False)
  return np.array(res)

# Funcion que se utilizo para obtener los centros de las bbox de las detecciones
def bbox_centros(bboxs_dets: np.ndarray, def_centro: str = 'centro') -> np.ndarray:
  '''
  Funcion que se utiliza para encontrar los centros de todas las detecciones realizadas por el modelo
  segun la definicion del centro que se designe.
  Entrega una lista de los centros de cada bbox en formato [(x1, y1), (x2, y2), (x3, y3), ..., (xn, yn)]
  Se utiliza para tener directamente un listado de los centros de todas las detecciones realizadas por el modelo.

  Variables:
  - bbox_dets (np.ndarray): lista con las bbox de las detecciones realizadas por el modelo
  - def_centro (str): texto que indica cual sera la definicion del centro que se utilizara en este listado de centros de detecciones. 
  Hasta la fecha, las unicas opciones son 'centro' (opcion por defecto) y 'centro-sup'

  Ante mas dudas de esta funcion, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
  '''
  res = []
  for bbox in bboxs_dets:
    if def_centro == 'centro':
      x_c = int((bbox[0] + bbox[2]) / 2)
      y_c = int((bbox[1] + bbox[3]) / 2)
    elif def_centro == 'centro-sup':
      x_c = int((bbox[0] + bbox[2]) / 2)
      y_c = int(min(bbox[1], bbox[3]))
    res.append([x_c, y_c])
  return np.array(res)

def guardar_xlsx_contador():
  return None