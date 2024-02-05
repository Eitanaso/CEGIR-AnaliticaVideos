import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np

letra = 20
letra = 40
letra = 60
pos = letra + 10
izq = 70

source = [
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\contador_exposicion.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\conteo_grande.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\cruce_peatonal_toromazote.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\cruce_peaton_vehiculo_exposicion.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\cruce_mal_matucana.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\cruce_toro_mazote_mal.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\persona_calzada.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\atravesando_calle1.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\atravesando_calle2.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\atravesando_calle3.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\atravesando_calle4.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\atravesando_calle5.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\personas_calle.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\personas_lugar_riesgoso1.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\personas_lugar_riesgoso2.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\personas_lugar_riesgoso3.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\personas_ciclovia.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\ciclistas_transito1.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\ciclistas_transito2.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\ciclista_contra_transito.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\ciclista_ciclovia1.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\ciclista_ciclovia2.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\ciclista_vereda1.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\ciclista_vereda2.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\ciclista_vereda3.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\ciclista_vereda4.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\vehiculo_prohibido.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados\\vehiculo1.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados\\vehiculo2_corte.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\corriendo_plaza_arg.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\corriendo_delito.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\cambio_trayectoria.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\personas_corriendo4.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\personas_corriendo1_corte.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\personas_corriendo5.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\personas_corriendo2.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\personas_corriendo3_corte.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\personas_corriendo7_corte.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados\\corriendo_calzada.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\ambulantes1.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados\\ambulante2_corte.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados\\ambulante3.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados\\carabineros_exigente.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\carabineros.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\overoles1_corte.mp4',
  #'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados2\\overoles2.mp4',
  'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados\\overoles_blancos.mp4',
]
target = 'C:\\Users\\eitan\\Downloads\\videos_casos_uso_nuevos_cegir\\resultados_final\\presencia_overoles_blancos_2.mp4'
comuna = [
  'Estación Central',
]
lugar = [
  #'Plaza Argentina',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda esquina calle Toro Mazotte',
  #'Exposición cerca de Av. Alameda',
  #'Av. Alameda esquina calle Matucana',
  #'Av. Alameda esquina calle Toro Mazotte',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda esquina calle San Francisco de Borja',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda en Persa Estación',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda esquina calle Matucana',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda esquina calle Toro Mazotte',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda en Estación Central',
  #'Plaza Argentina',
  #'Av. Alameda en Persa Estación',
  #'Av. Alameda esquina calle Marinero Díaz',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda en Persa Estación',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda en Estación Central',
  #'Av. Alameda esquina calle Matucana',
  #'Plaza Argentina',
  'Av. Alameda en Estación Central',
]
vista = [
  #'Desde calle Exposición hacia Estación Central',
  #'Desde Av. Alameda hacia la Estación Central',
  #'Desde Av. Alameda hacia calle Toro Mazotte al sur',
  #'Desde Exposición hacia el oriente',
  #'Desde Av. Alameda hacia calle Matucana',
  #'Desde Av. Alameda hacia calle Toro Mazotte al sur',
  #'Desde Av. Alameda hacia Plaza Argentina',
  #'Desde Av. Alameda hacia Plaza Argentina',
  #'Desde Av. Alameda hacia Plaza Argentina',
  #'Desde Av. Alameda hacia Plaza Argentina',
  #'Desde Av. Alameda hacia Plaza Argentina',
  #'Desde Av. Alameda hacia Plaza Argentina',
  #'Desde Av. Alameda hacia USACH',
  #'Desde Av. Alameda hacia Plaza Argentina',
  #'Desde Av. Alameda hacia la Estación Central',
  #'Desde Av. Alameda hacia la Estación Central',
  #'Desde Av. Alameda hacia USACH',
  #'Desde Av. Alameda hacia calle San Francisco de Borja',
  #'Desde Av. Alameda hacia Plaza Argentina',
  #'Desde Av. Alameda hacia Plaza Argentina',
  #'Desde Av. Alameda hacia el poniente',
  #'Desde Av. Alameda hacia USACH',
  #'Desde Av. Alameda hacia calle Matucana',
  #'Desde Av. Alameda hacia Plaza Argentina',
  #'Desde Av. Alameda hacia el poniente',
  #'Desde Av. Alameda hacia la Estación Central',
  #'Desde Av. Alameda hacia calle Toro Mazotte al sur',
  #'Desde Av. Alameda hacia Plaza Argentina',
  #'Desde Av. Alameda hacia Plaza Argentina',
  #'Desde Av. Alameda hacia la Estación Central',
  #'Desde Av. Alameda hacia el Persa Estación',
  #'Desde Av. Alameda hacia calle Marinero Díaz',
  #'Desde Av. Alameda hacia Plaza Argentina',
  #'Desde Av. Alameda hacia la Estación Central',
  #'Desde Av. Alameda hacia el poniente',
  #'Desde Av. Alameda hacia la Estación Central',
  #'Desde Av. Alameda hacia la Estación Central',
  #'Desde Av. Alameda hacia el poniente',
  #'Desde Av. Alameda hacia el poniente',
  #'Desde Av. Alameda hacia la Estación Central',
  #'Desde Av. Alameda hacia la Estación Central',
  #'Desde Av. Alameda hacia el poniente',
  #'Desde Av. Alameda hacia la Estación Central',
  #'Desde Av. Alameda hacia el poniente',
  #'Desde Av. Alameda hacia calle Exposición',
  #'Desde Av. Alameda hacia la Estación Central',
  'Desde Av. Alameda hacia la Estación Central',
]
fecha = [
  #'Domingo 10 de septiembre de 2023',
  #'Domingo 7 de enero de 2024',
  #'Miércoles 20 de septiembre de 2023',
  #'Miércoles 20 de septiembre de 2023',
  #'Jueves 7 de septiembre de 2023',
  #'Miércoles 20 de septiembre de 2023',
  #'Domingo 7 de enero de 2024',
  #'Domingo 7 de enero de 2024',
  #'Domingo 7 de enero de 2024',
  #'Domingo 7 de enero de 2024',
  #'Domingo 7 de enero de 2024',
  #'Domingo 7 de enero de 2024',
  #'Domingo 7 de enero de 2024',
  #'Domingo 7 de enero de 2024',
  #'Domingo 7 de enero de 2024',
  #'Domingo 7 de enero de 2024',
  #'Domingo 7 de enero de 2024',
  #'Miércoles 16 de agosto de 2023',
  #'Domingo 7 de enero de 2024',
  #'Domingo 7 de enero de 2024',
  #'Miércoles 16 de agosto de 2023',
  #'Domingo 7 de enero de 2024',
  #'Jueves 7 de septiembre de 2023',
  #'Domingo 7 de enero de 2024',
  #'Domingo 7 de enero de 2024',
  #'Domingo 7 de enero de 2024',
  #'Jueves 28 de septiembre de 2023'
  #'Domingo 7 de enero de 2024',
  #'Domingo 7 de enero de 2024',
  #'Martes 10 de enero de 2023',
  #'Martes 15 de noviembre de 2022',
  #'Jueves 18 de mayo de 2023',
  #'Domingo 7 de enero de 2024',
  #'Domingo 7 de enero de 2024',
  #'Domingo 7 de enero de 2024',
  #'Domingo 7 de enero de 2024',
  #'Domingo 7 de enero de 2024',
  #'Domingo 7 de enero de 2024',
  #'Sábado 23 de abril de 2022',
  #'Mércoles 20 de diciembre de 2023',
  #'Domingo 7 de enero de 2024',
  #'Domingo 7 de enero de 2024',
  #'Domingo 7 de enero de 2024',
  #'Miércoles 17 de enero de 2024',
  #'Miércoles 17 de enero de 2024',
  'Miércoles 17 de enero de 2024',
]
hora = [
  #'12:00',
  #'18:38',
  #'13:07',
  #'12:16',
  #'18:13',
  #'13:07',
  #'17:23',
  #'17:15',
  #'17:16',
  #'17:21',
  #'17:32',
  #'18:45',
  #'17:32',
  #'17:32',
  #'18:23',
  #'18:46',
  #'17:32',
  #'13:29',
  #'17:22',
  #'19:07',
  #'16:00',
  #'17:32',
  #'18:26',
  #'17:28',
  #'18:26',
  #'18:46',
  #'17:55',
  #'20:57',
  #'21:07 (10 min después)',
  #'18:09',
  #'17:10',
  #'17:10',
  #'17:25',
  #'17:25',
  #'17:25',
  #'18:26',
  #'21:57',
  #'21:57',
  #'14:00',
  #'18:30',
  #'17:32',
  #'18:21',
  #'18:46',
  #'18:46',
  #'13:39',
  #'13:40'
  '13:46',
]

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

  texto = np.zeros(tamano, dtype=np.uint8)
  taxto = cv2.cvtColor(texto.copy(), cv2.COLOR_BGR2RGB)
  pil_image = Image.fromarray(texto)
  font = ImageFont.truetype('C:\\Windows\\Fonts\\arial.ttf', size=letra)
  draw = ImageDraw.Draw(pil_image)

  W, H = pil_image.size

  _, _, w1, h1 = draw.textbbox((0, 0), f'Comuna', font=font)
  draw.text((izq, (H-h1)/2 - 3*pos), f'Comuna', font=font, fill=(255, 233, 0))
  _, _, w, h = draw.textbbox((0, 0), f': {comuna[0]}', font=font)
  draw.text((izq + w1, (H-h)/2 - 3*pos), f': {comuna[0]}', font=font, fill='white')

  _, _, w1, h1 = draw.textbbox((0, 0), f'Lugar', font=font)
  draw.text((izq, (H-h1)/2 - 2*pos), f'Lugar', font=font, fill=(255, 233, 0))
  _, _, w, h = draw.textbbox((0, 0), f': {lugar[i]}', font=font)
  draw.text((izq + w1, (H-h)/2 - 2*pos), f': {lugar[i]}', font=font, fill='white')

  _, _, w1, h1 = draw.textbbox((0, 0), f'Vista', font=font)
  draw.text((izq, (H-h1)/2 - pos), f'Vista', font=font, fill=(255, 233, 0))
  _, _, w, h = draw.textbbox((0, 0), f': {vista[i]}', font=font)
  draw.text((izq + w1, (H-h)/2 - pos), f': {vista[i]}', font=font, fill='white')

  _, _, w1, h1 = draw.textbbox((0, 0), f'Fecha', font=font)
  draw.text((izq, (H-h1)/2 + pos), f'Fecha', font=font, fill=(255, 233, 0))
  _, _, w, h = draw.textbbox((0, 0), f': {fecha[i]}', font=font)
  draw.text((izq + w1, (H-h)/2 + pos), f': {fecha[i]}', font=font, fill='white')

  _, _, w1, h = draw.textbbox((0, 0), f'Hora', font=font)
  draw.text((izq, (H-h1)/2 + 2*pos), f'Hora', font=font, fill=(255, 233, 0))
  _, _, w, h = draw.textbbox((0, 0), f': {hora[i]}', font=font)
  draw.text((izq + w1, (H-h)/2 + 2*pos), f': {hora[i]}', font=font, fill='white')
  texto = np.asarray(pil_image)
  texto = cv2.cvtColor(texto, cv2.COLOR_RGB2BGR)

  for _ in range(int(fps*4)):
    video_writer.write(texto)

  while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
      break
    video_writer.write(frame)

video_writer.release()
cap.release()