import cv2
import numpy as np
import matplotlib.pyplot as plt
# Para visualizar en COLAB
from google.colab.patches import cv2_imshow # cv.imshow
from PIL import Image
from PIL import ImageFilter
from PIL import ImageOps
from IPython import display #Importamos la función display del paquete IPython
import time

def resize_imagen(imagen, red_social):
  """
  funcion que retorna una imagen adaptada a una red social de las disponibles
  :param imagen: imagen tipo pillow
  :param red_social: "Youtube", "Instagram", "Twitter", "Facebook"
  :return imagen tipo pillow o objeto tipo str si existio algun error en la carga de la imagen:
  """
  #intenta abrir la imagen sino retorna el error
  #la idea es que si la funcion retorna un objeto tipo str
  #pueda ser capturado el error
  try:
    img = Image.open(imagen)
  except:
    return ("No ha sido posible cargar la imagen, ingrese correctamente la ruta")

  #desempaqueta el tamaño de la imagen
  ancho, alto = img.size
  rel_aspecto_original = ancho/alto
    #Asigna el tamaño final según la red social
  if red_social == "Youtube":
    ancho_final, alto_final = 1280, 720

  elif red_social == "Instagram":
    ancho_final, alto_final = 1080, 1080

  elif red_social == "Twitter":
    ancho_final, alto_final = 1024, 512

  elif red_social == "Facebook":
    ancho_final, alto_final = 1200, 628

  rel_aspecto_final = ancho_final/alto_final

  if rel_aspecto_original > rel_aspecto_final:
    ancho_nuevo = int((ancho*alto_final/alto))
    img2 = img.resize((ancho_nuevo, alto_final))
    # recortar ancho
    inicio_ancho_recorte = img2.size[0]//2-ancho_final//2
    final_ancho_recorte = inicio_ancho_recorte + ancho_final
    img3 = img2.crop((inicio_ancho_recorte,0,final_ancho_recorte,alto_final))


  else:
    alto_nuevo = int ((alto*ancho_final/ancho))
    img2 = img.resize((ancho_final, alto_nuevo))
    # recortar alto
    inicio_alto_recorte = img2.size[1]//2-alto_final//2
    final_alto_recorte = inicio_alto_recorte + alto_final
    img3 = img2.crop((0,inicio_alto_recorte,ancho_final,final_alto_recorte))

  fig, axes = plt.subplots(1, 2, figsize=(12, 6))
  ax = axes.ravel()
  ax[0].imshow(img)
  ax[0].set_title("Original")
  ax[0].axis('off')
  ax[1].imshow(img3)
  ax[1].set_title(f"{red_social}")
  ax[1].axis('off')
  plt.show()

  return img3

def ajuste_contraste(img):
  img_eq  = ImageOps.equalize(img)
  
  fig, axes = plt.subplots(1, 2, figsize=(12, 6))
  ax = axes.ravel()
  ax[0].imshow(img)
  ax[0].set_title("Original")
  ax[0].axis('off')


  ax[1].imshow(img_eq)
  ax[1].set_title("Ajuste de Contraste")
  ax[1].axis('off')

  plt.show()
  return img_eq

def aplicar_filtros(img, filtro_elejido):

  filtros_disponibles = {
            "BLUR": ImageFilter.BLUR,
            "CONTOUR": ImageFilter.CONTOUR,
            "DETAIL": ImageFilter.DETAIL,
            "EDGE_ENHANCE": ImageFilter.EDGE_ENHANCE,
            "EDGE_ENHANCE_MORE": ImageFilter.EDGE_ENHANCE_MORE,
            "EMBOSS": ImageFilter.EMBOSS,
            "FIND_EDGES": ImageFilter.FIND_EDGES,
            "SMOOTH": ImageFilter.SMOOTH,
            "SHARPEN": ImageFilter.SHARPEN
        }

  filtro_elejido = filtro_elejido.upper()

  if filtro_elejido not in filtros_disponibles:
    raise TypeError("El filtro no está disponible")

  img_filtrada = img.filter(filtros_disponibles[filtro_elejido])

  imagenes = []

  for filtro in filtros_disponibles:
    imagenes.append((filtro, img.filter(filtros_disponibles[filtro])))

  fig, axes = plt.subplots(5, 2, figsize=(10, 20))
  ax = axes.ravel()

  ax[0].imshow(img)
  ax[0].set_title("ORIGINAL")
  ax[0].axis('off')

  for i in range(len(imagenes)):
    ax[i+1].imshow(imagenes[i][1])
    if filtro_elejido == imagenes[i][0]:
      ax[i+1].set_title(imagenes[i][0], color="red")
    else:
      ax[i+1].set_title(imagenes[i][0])
    ax[i+1].axis('off')

  plt.show()

  return img_filtrada

def dibujar(img):

  imgcv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

  img_gray  = cv2.cvtColor(imgcv, cv2.COLOR_BGR2GRAY)
  img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
  img_edged = cv2.Canny(img_blur, 100, 200)

  imgcv = cv2.cvtColor(imgcv, cv2.COLOR_BGR2RGB)
  img_pil = Image.fromarray(imgcv)

  img_edged = cv2.cvtColor(img_edged, cv2.COLOR_BGR2RGB)
  img_edged__pil = Image.fromarray(img_edged)

  fig, axes = plt.subplots(1, 2, figsize=(12, 6))
  ax = axes.ravel()
  ax[0].imshow(img_pil)
  ax[0].set_title("Original")
  ax[0].axis('off')


  ax[1].imshow(img_edged__pil)
  ax[1].set_title("Dibujo")
  ax[1].axis('off')
  plt.show()
  return img_edged__pil