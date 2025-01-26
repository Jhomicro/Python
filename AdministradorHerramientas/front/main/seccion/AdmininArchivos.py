#Explorar archivos
import os
#Mover o copiar archivos
import shutil
#Soporte para archivos comprimidos
import zipfile
import rarfile
import py7zr
#Ordenar archivos
from datetime import datetime
#Protección archivos
from cryptography.fernet import Fernet
# Explorar dispositivos conectados
import psutil
# Vista previa imagen
from PIL import Image
# Vista previa pdf
from PyPDF2 import PdfReader
import cv2

PAPELERA = os.path.expanduser("~/.papelera")  # Variable globar
#! Logica del administrador de archivos

#?Explorador de archivos
def listar_archivos(directorio):
    """
    Lista todos los archivos y carpetas en el directorio actual.
    """
    try:
        for root, dirs, files in os.walk(directorio):
            yield root, dirs, files
    except Exception as e:
        print(f"Error al listar los archivos en {directorio}: {e}")
        return []

#!Gestión de archivos

def crear_archivo(ruta, contenido=''):
    """
    Crear un archivo
    """
    with open(ruta, 'w') as archivo:
        archivo.write(contenido)
#? Renombrar archivos
def renombrar_archivo(ruta, nuevo_nombre):
    os.rename(ruta, nuevo_nombre)

#? Eliminar archivos
def eliminar_archivo(ruta):
    os.remove(ruta)

#? Crear carpeta

def crear_carpeta(ruta):
    os.makedirs(ruta, exist_ok=True)

#? Eliminar carpeta
def eliminar_carpeta(ruta):
    os.rmdir(ruta)

#! Mover o copiar archivos

def mover_archivo(ruta_origen, ruta_destino):
    try:
        if not os.path.exists(ruta_destino):
            print(f"El archivo {ruta_origen} no existe.")
            return
        shutil.move(ruta_origen, ruta_destino)
        print(f"El archivo {ruta_origen}, fue movido a {ruta_destino}")
    except Exception as e:
        print(f"Error al mover el archivo: {e}")

def copiar_archivo(ruta_origen, ruta_destino):
    shutil.copy(ruta_origen, ruta_destino)

#! Busqueda avanzada de archivos
def buscar_archivo(directorio, nombre_archivo = None, extension= None):
    """
    Busca un archivo en el directorio y sus subdirectorios.
    """
    for root, dirs, files in os.walk(directorio):
        for file in files:
            if (nombre_archivo and nombre_archivo in file) or (extension and file.endswith(extension)):
                    print(os.path.join(root, file))

#!Buscar en el contenido del archivo:
def buscar_en_contenido(directorio, texto):
    """
    Busca una cadena de texto en el contenido de un archivo.
    """
    for root, dirs, files in os.walk(directorio):
        for file in files:
            if file.endswith('.txt') or file.endswith('.csv'):
                with open(os.path.join(root, file), 'r') as archivo:
                    if texto in archivo.read():
                        print(f"Texto encontrado en {os.path.join(root, file)}")

#! Información detallada de archivos
def obtener_info_detallada(ruta):
    """
    Obtiene información detallada sobre un archivo.
    """
    if os.path.exists(ruta):
        info = os.stat(ruta)
        return {
            'Nombre': os.path.basename(ruta),
            'Ruta': ruta,
            'Tamaño': info.st_size,
            'Creación': info.st_birthtime,
            'Modificado': datetime.fromtimestamp(info.st_mtime),
            'Acceso': datetime.fromtimestamp(info.st_atime),
            'Permisos': oct(info.st_mode),
            'Tipo': 'Archivo' if os.path.isfile(ruta) else 'Carpeta',
        }

#! descompresión de archivos
def descromprimir_zip(ruta_zip, destino):
    """
    Descomprimir archivos zip
    """
    with zipfile.ZipFile(ruta_zip, 'r') as zip_ref:
        zip_ref.extractall(destino)

def descomprimir_rar(ruta_rar, destino):
    with rarfile.RarFile(ruta_rar) as rar_ref:
        rar_ref.extractall(destino)

def descomprimir_7z(ruta_7z, destino):
    with py7zr.SevenZipFile(ruta_7z, mode='r') as z:
        z.extractall(path=destino)

#! Crear archivo comprimido
def descomprimir_archivo(ruta_archivo, destino, tipo):
    """
    Descomprime un archivo en el formato especifico.
    Formatos soportados: 7zip, rar, zip
    """
    try:
        if tipo == 'zip':
            with zipfile.ZipFile(ruta_archivo, mode='r') as zip_ref:
                zip_ref.extractall(destino)
        elif tipo == 'rar':
            with rarfile.RarFile(destino) as rar_ref:
                rar_ref.extract(destino)
        elif tipo == '7z':
            with py7zr.SevenZipFile(destino, mode='r') as z:
                z.extractall(path=destino)
        else:
            return f"Formato {tipo} no soportado"
    except Exception as e:
        return f"Error descomprimiendo {ruta_archivo}: {str(e)}"

#! Organización inteligente
def organizar_archivos(directorio):
    """
    Organiza los archivos según sus extensiones en carpetas distintas.
    """
    for root, dirs, files in os.walk(directorio):
        for file in files:
            path = os.path.join(root, file)
            fecha_mod=datetime.fromtimestamp(os.path.getatime(path))
            fecha_str= fecha_mod.strftime("%Y-%m-%d")
            carpeta_destino=os.path.join(root, fecha_str)
            if not os.path.exists(carpeta_destino):
                os.makedirs(carpeta_destino)
            shutil.move(path,os.path.join(carpeta_destino,file))

#! Protección de archivos
#?Generar clave
def generar_clave():
    return Fernet.generate_key()

#?Encriptar archivo
def encriptar_archivo(ruta_archivo, clave):
    with open(ruta_archivo, 'rb') as archivo:
        contenido = archivo.read()
    f = Fernet(clave)
    contenido_encryptado = f.encrypt(contenido)
    with open(f"{ruta_archivo}.enc", 'rb') as archivo_encriptado:
        archivo_encriptado.write(contenido_encryptado)

CLAVE = generar_clave()
with open ("clave.key", "wb") as clave_file:
    clave_file.write(CLAVE)
#? Encriptar todos los archivos
def encriptar_todos_archivos(directorio):
    """
    Encripta todos los archivos de un directorio y subdirectorio
    """
    try:
        for root, dirs, files in os.walk(directorio):
            for file in files:
                ruta_archivo = os.path.join(root, file)
                #Evitar cifrar archivos ya cifrados o la clave
                if not ruta_archivo.endswith('.enc') and "clave.key" not in ruta_archivo:
                    encriptar_archivo(ruta_archivo, CLAVE)
                    os.remove(ruta_archivo)#Eliminar el archivo original despues de cifrar
                    print(f"Archivo encriptado: {ruta_archivo}.enc")
    except Exception as e:
        print(f"Error al encriptar archivo: {e}")

#?Desencriptar archivo
def desencriptar_archivo(ruta, clave):
    with open(ruta, 'rb') as archivo:
        contenido_encriptado = archivo.read()
    f = Fernet(clave)
    contenido = f.decrypt(contenido_encriptado)
    with open(ruta.replace('.enc', ''), 'wb') as archivo_desencriptado:
        archivo_desencriptado.write(contenido)

#! Recuperación de papelera de reciclaje
def mover_a_papelera(ruta):
    """
    Agrega un archivo a la papelera de reciclaje.
    """
    if not os.path.exists(PAPELERA):
        os.makedirs(PAPELERA)
    archivo = os.path.basename(ruta)
    shutil.move(ruta, os.path.join(PAPELERA, archivo))

def recuperar_de_papelera(nombre_archivo):
    ruta= os.path.join(PAPELERA, nombre_archivo)
    if not os.path.exists(ruta):
        shutil.move(ruta, os.getcwd())

#!Gestionar permisos
def cambiar_permisos(ruta, permisos):
    """
    Cambia los permisos de un archivo.
    """
    os.chmod(ruta, permisos)

def obtener_permisos(ruta):
    """
    Obtiene los permisos de un archivo.
    """
    return oct(os.stat(ruta).st_mode)[-3:]

#! Acceder a una carpeta de red montada, usando una ruta de red
def explorar_carpeta_red(ruta_red):
    """
    Monta una carpeta de red en una ruta local.
    """
    if os.path.exists(ruta_red):
        for root, dirs, files in os.walk(ruta_red):
            print(f"Directorio: {root}")
            for file in files:
                print(f"Archivo: {file}")
    else:
        print(f"No se pudo acceder a la carpeta compartida")

#! Explorar dispositivos conectados
def explorar_dispositivos_conectados():
    """
    Explorar los dispositivos conectados o discos monstados en el sistema
    """
    particiones = psutil.disk_partitions()
    for p in particiones:
        print(f"Dispositivo: {p.device}, Punto de montaje: {p.mountpoint}")
        if p.fstype:
            #Verificar el uso del disposito
            uso = psutil.disk_usage(p.mountpoint)
            print(f" - Total: {uso.total} bytes")
            print(f"- Usado: {uso.used} bytes")
            print(f"- Libre: {uso.free} bytes")
            print(f"- Porcentaje usado: {uso.percent}%")

#!Detectar si es un disco o memoria
def es_usb(directorio):
    """
    Verificar si el dispositivo esta montado en un directorio tipico a un directorio
    """
    if "usb" in directorio.lower() or "removable" in directorio.lower():
        return True
    return False

#! Vistas previas
def vista_previa_imagen(ruta_imagen):
    """
    Mostrar una vista previa de una imagen.
    """
    try:
        with Image.open(ruta_imagen) as img:
            img.show()
    except Exception as e:
        print(f"Error al mostrar la vista previa: {e}")

#? Vista previa pdf
def vista_previa_pdf(ruta_pdf, paginas = 1):
    """
    Mostrar una vista previa de un PDF.
    """
    try:
        with open(ruta_pdf, "rb") as archivo_pdf:
            lector =PdfReader(archivo_pdf)
            contenido = ""
            for i in range(min(paginas, len(lector.pages))):
                contenido += lector.pages[i].extract_text()
                print(contenido)
    except Exception as e:
        print(f"Error al mostrar la vista previa: {e}")

#? Vistas previa video

def vista_previa_video(ruta_video):
    """
    Mostrar una vista previa de un video.
    """
    try:
        cap = cv2.VideoCapture(ruta_video)
        if not cap.isOpened():
            print("No se pudo abrir el video. Verifica la ruta o el formato del archivo.")
            return
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Vista previa del video", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"No se pudo cargar el video: {e}")
