import qrcode
import os
from PIL import Image, ImageTk

FORMATO= {
    "png",
    "jpeg",
    "jpg",
    "bmp",
}

def GeneradorQr(dato, formato="png"):
    """Generar un codigo QR a partir de un dato proporcionado y lo guarde como imagen"""
    try:
        #Nombre de la carpeta donde se guardan los Codigo QR
        folder_name = "Codigo QR"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        if formato not in FORMATO:
            raise ValueError("Formato no válido. Los formatos válidos son: png, jpeg, jpg, bmp")

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(dato)
        qr.make(fit=True)

        #Crear una imagen del QR
        img = qr.make_image(fill_color="black", back_color="white")

        #Determinar el siguiente número disponible para el archivo
        base_name = "Codigo_qr"
        extension = f".{formato}"
        i = 1
        while os.path.exists(os.path.join(folder_name,f"{base_name}{i}{extension}")):
            i += 1

        #Nombre del archivo
        filename= os.path.join(folder_name,f"{base_name}{i}{extension}")

        #Guarda la imagen
        img.save(filename, format=formato.upper())
        return f"Codigo generado correctamente: {filename}"
    except Exception as e:
        return f"Error al generar el código QR: {e}"
def mostrar_imagen(img):
    # Convertir la imagen PIL a un formato que Tkinter pueda usar (PhotoImage)
    """Muestra una vista previa de la imagen con un delay de 10 segundos"""
    return ImageTk.PhotoImage(img)