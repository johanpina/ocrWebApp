import io
import os
from datetime import datetime
import pytesseract
from PIL import Image

from dotenv import load_dotenv
_=load_dotenv('.venv')

from schemas import ZerSchema

# Configurar Tesseract
pytesseract.pytesseract.tesseract_cmd = r""+os.getenv('TESSERACT_PATH')   #r'/usr/bin/tesseract'  # Asegurar esta ruta instalada en el sistema.
LOCALPATH = os.getenv('LOCALPATH')#'/mnt/compartido/'

MESES = {"enero":'01', "febrero":'02',"marzo":'03',"abril":'04',"mayo":'05' ,"junio":'06',"julio":'07',"agosto":'08',"septimbre":'09',
           "octubre":'10',"noviembre":'11',"diciembre":'12','a.m.':'am','p.m.':'pm','a. m.':'am','p. m.':'pm','alas':'','a las':''} 
FORMAT = "%d de %m de %Y %H:%M %p"

def repeatedImage(actual_image:str):
    #Vamos a listar los archivos en la carpeta y luego vamos a verificar si ya existe.
    # si ya existe uno entonces vamos a retornar una excepción.
    actual_image = actual_image.split('/')[-1]
    files = os.listdir(LOCALPATH)
    # print(files,'\n',actual_image)
    return actual_image in files
    
        
def text2date(textFecha:str)-> str:
    for key in MESES.keys():
        textFecha = textFecha.replace(key, MESES[key])
    
    return datetime.strptime(textFecha, FORMAT).__str__()
    
def dictionary_from_text(text):
  text_list = text.split('\n')
  conv_ind =  text_list.index('Conversación')+1
  fecha = text_list[-4]
  referencia= text_list[3]
  nombre = text_list[6]
  placa = text_list[conv_ind].translate( { ord("-"): None } ).upper()
  Pago = float(text_list[-6].replace(",",".")[1::])

  fecha_str = text2date(fecha)
  ## Forma de lo que vamos a retornar.
  dictionary = ZerSchema(
      referencia=referencia,
      nombre=nombre,
      placa=placa,
      pago=Pago,
      fecha=fecha_str,
      #path = imagePath/reference/nombre
      path = f"{referencia}_{placa}_{nombre.replace(' ','-')}.jpg"
  )
  return dictionary


async def ocr_image(image_data: bytes) -> str:
    image = Image.open(io.BytesIO(image_data))
    text = pytesseract.image_to_string(image, lang="spa", config="--psm 6")  # Ajusta el idioma y la configuración según tus necesidades
    return text

async def ocr_ZER(image_data: bytes) -> str:
    image = Image.open(io.BytesIO(image_data))
    text = pytesseract.image_to_string(image, lang="spa", config="--psm 6")  # Ajusta el idioma y la configuración según tus necesidades
    dict = dictionary_from_text(text=text)
    if not repeatedImage(dict.path):
        image.save(LOCALPATH+dict.path)
        return dict
    else:
        return None