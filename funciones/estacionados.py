# Importar librerias utiles
import numpy as np
from collections import deque

#--------------------------------------------------------------------------------------------------------------------
# Creacion de funciones utiles para el analisis de personas estacionadas en un espacio definido
# Por mayores dudas de las funciones, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
#--------------------------------------------------------------------------------------------------------------------

# Creacion de stacks, para tener una lista con tamano maximo de formato FIFO
def create_sized_list(size: int) -> deque:
  '''
  Funcion utilizada para generar una lista FIFO, la cual se utilizara para guardar elementos que se actualizaran con el tiempo.
  Entrega la lista FIFO creada, pero sin ningun elemento.

  Variables:
  - size (int): un numero que indica el tamano de la lista FIFO, es decir, la cantidad de objetos que tendra la lista adentro

  Ante mas dudas de esta funcion, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
  '''
  return deque(maxlen=size)

# Agregar objetos a la lista FIFO creada con la funcion anterior
def add_item(sized_list: deque, item) -> None:
  '''
  Funcion utilizada para agregar un objeto a una lista FIFO, realiza automaticamente la eliminacion del primer objeto si ya esta llena.
  Esta funcion no entrega nada, solo actualiza la lista que recibe como variable.

  Variables:
  - sized_list (deque): la lista FIFO a la cual se le agregara un objeto nuevo
  - item (Any): Se le puede agregar cualquier tipo de objeto según sea necesario. Actualmente se usa para agregar boleanos

  Ante mas dudas de esta funcion, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
  '''
  sized_list.append(item)

# Funcion utilizada para guardar las detecciones dentro de un area en un diccionario
def save_detections_in_area_dixi(dixi: dict, dets, tpo_det: int) -> dict:
  '''
  Funcion que guarda listas FIFO por cada detección que se encuentra en la zona demarcada.
  Estas listas FIFO tienen cierto tamano que representa el tiempo de la deteccion dentro de la zona.
  Dentro del diccionario, se encuentran las detecciones que alguna vez pasaron dentro de la zona, para asi ser robusto ante las 
  detecciones que salen y vuelven a entrar en la zona. Sin embargo, si ha pasado harto tiempo
  desde que se encontraba adentro, se borra la identificacion de la deteccion. 
  Entrega el diccionario recibido como variable actualizado con las detecciones realizadas por el modelo.
  Se utiliza para analizar la estancia de una deteccion dentro de una zona, de esta manera, se podran realizar los analisis requeridos.

  Variables:
  - dixi (dict): recibe el diccionario que se quiere actualizar con las detecciones encontradas en el area
  - dets (Detections): detecciones realizadas por el modelo que se encuentran dentro de la zona a analizar
  - tpo_det (int): largo de las listas FIFO que se guardaran en el diccionario por cada deteccion.
  Se ve representado dentro del código general por el tiempo en segundos multiplicado por los FPS del video (s * FPS)

  Ante mas dudas de esta funcion, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
  '''
  result = dixi.copy()
  dets_in_dixi = dixi.keys()
  # se prueba si el modelo no detecto nada, para que no genere error tratando de acceder a un objeto que no existe
  try: 
    dets_now = dets.tracker_id
  except: 
    dets_now = []
  # se revisa si las detecciones previas siguen dentro de la zona, y se adjunta un valor boleano de acuerdo al caso
  for det in dets_in_dixi:
    if det not in dets_now:
      add_item(result[det], False)
    else:
      add_item(result[det], True)
  # se revisan las nuevas detecciones, y se crea su lista FIFO si es una nueva deteccion en la zona
  for det in dets_now:
    if det not in dets_in_dixi:
      result[det] = create_sized_list(tpo_det)
      add_item(result[det], True)
  # Borrar una deteccion si ya no se le ha visto dentro de la zona por mucho tiempo (su lista FIFO esta llena de False)
  # Esto se realiza para no llenar el diccionario con información poco relevante
  borrar = []
  for det in result.keys():
     # Revisa si esta llena la lista
    if len(result[det]) == tpo_det:
      # Revisa si todos los valores dentro de la lista por si solos son falsos
      if not np.array(result[det]).any(): 
        borrar.append(det)
  for det in borrar:
    del result[det]
  return result

# Funcion que analiza si las detecciones se han encontrado dentro de una misma zona por cierto tiempo
def det_in_same_area(dets, dixi: dict, tpo_det: int, porcentaje: float) -> np.ndarray:
  '''
  Funcion que se utiliza para marcar solo las detecciones del modelo que se encuentren dentro de la zona analizada una 
  cierta cantidad de tiempo asignada por el usuario, junto a un umbral para ser robusto a la salida y retorno del objeto a la misma zona.
  Entrega una lista con valores boleanos que representan si la deteccion se encuentra dentro por un tiempo extendido.
  Se utiliza cuando se quieren encontrar objetos que se encuentren mucho tiempo ocupando una zona dentro de una imagen.
  Si se analizan personas, se les puede considerar vendedores ambulantes, o personas con potencial de estar buscando una victima de robo,
  como tambien una persona esperando a alguien o algo. Es importante que el usuario reconozca el contexto.

  Variables:
  - dets (Detections): detecciones realizadas por el modelo que se encuentran dentro de la zona a analizar
  - dixi (dict): diccionario con las detecciones que se encuentran dentro de la zona y con la cantidad de 
  tiempo que se han encontrado dentro de la misma
  - tpo_det (int): numero que se utiliza para analizar si la deteccion se ha encontrado tiempo suficiente dentro de la zona para marcarlo en la imagen.
  Se ve representado dentro del código general por el tiempo en segundos multiplicado por los FPS del video (s * FPS)
  - porcentaje (float): valor decimal para agregar robustez al analisis del tiempo de estancia de una deteccion en una zona.
  Es decir, se asigna un porcentaje del tiempo total para decir si estuvo suficiente tiempo dentro de la zona, para tener en cuenta
  si el objeto salio por un pequeno rato y vovlio a la zona analizada.

  Ante mas dudas de esta funcion, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
  '''
  result = []
  for det in dets:
    # Se revisa que una deteccion haya estado el tiempo suficiente dentro del diccionario
    if len(dixi[det]) == tpo_det:
      # Se analiza que este tiempo dentro del diccionario haya sido sobre el umbral de porcentaje de tiempo dentro de la zona estudiada
      if np.array(dixi[det]).tolist().count(True) >= int(porcentaje * tpo_det):
        result.append(True)
      else:
        result.append(False)
    else:
      result.append(False)
  return np.array(result)

#--------------------------------------------------------------------------------------------------------------------
# Funciones obsoletas que se utilizaron en otras versiones del codigo, no son utiles actualmente
# Por mayores dudas de estas funciones, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
#--------------------------------------------------------------------------------------------------------------------

# Funcion que se utilizo para revisar si las detecciones se encontraban dentro de una misma zona
# Adicionalmente, tenia la opcion de revisar que el centro del objeto no se moviera mucho dentro de la zona
def misma_zona(dets, cods: deque, bboxs: deque, rango: int = 30, sin_mov: bool = False) -> np.ndarray:
  '''
  Funcion obsoleta.

  Funcion que se utiliza para verificar si las detecciones realizadas dentro de la zona ya han estado dentro un tiempo y, si corresponde,
  si no se han movido mas que un umbral superior.
  Entrega una lista con valores boleanos que representan si la deteccion se ha encontrado dentro de la zona un tiempo y, si corresponde,
  si no se ha movido sobre el umbral superior.
  Se utiliza para marcar las detecciones dentro de la zona analizada que se encuentran dentro por una cierta cantidad de tiempo y, si
  corresponde, si no se ha movido mas que el umbral designado.

  Variables:
  - dets (Detections): lista de las detecciones realizadas por el modelo dentro de la zona analizada
  - cods (deque): lista FIFO que tiene guardadas los identificadores de las detecciones de los ultimos segundos dentro de la zona analizada
  - bboxs (deque): lista FIFO que tiene guardadas los centros de las detecciones de los ultimos segundos dentro de la zona analizada
  - rango (int): umbral superior que indica (en pixeles) la cantidad de movimiento aceptable del centro de la bbox para decir si el objeto 
  se movio o no dentro de la zona
  - sin_mov (bool): boleano que indica si se quiere analizar la posicion de los objetos, revisando si su centro se mueve mucho o no.
  Por defecto el False, debido a que complica el analisis cuando las bbox modifican su tamano

  Ante mas dudas de esta funcion, comunicarse con Eitan Hasson Arellano a traves del correo eitanhass@gmail.com
  '''
  res = []
  for i in range(len(dets.xyxy)):
    cod_det = dets.tracker_id[i]
    bbox_det = dets.xyxy[i]
    x_c = int((bbox_det[0] + bbox_det[2]) / 2)
    y_c = int((bbox_det[1] + bbox_det[3]) / 2)
    in_range = True
    # Se verifica si la deteccion se encuentra dentro de la lista con las detecciones que se encuentran cierto tiempo dentro de la zona
    for j in range(len(cods)):
      if cod_det not in cods[j]:
        in_range = False
        break
    # Se verifica si la deteccion no se ha movido mucho dentro de la zona
    if sin_mov:
      if in_range:
        for j in range(len(cods)):
          pos_cod = list(cods[j]).index(cod_det)
          bbox_centro_j = bboxs[j][pos_cod]
          x_bbox = bbox_centro_j[0]
          y_bbox = bbox_centro_j[1]
          if (x_bbox - rango > x_c) or (x_bbox + rango < x_c) or (y_bbox - rango > y_c) or (y_bbox + rango < y_c):
            in_range = False
            break
    res.append(in_range)
  return np.array(res)
