import barcode
import barcode.ean
from barcode.writer import ImageWriter
import os
import subprocess

EXTENSIONBARRAS = {
    "png",
    "svg",
}

FORMATOBARRAS ={
    "codabar",
    "code128",
    "code39",
    "ean",
    "ean13",
    "ean13-guard",
    "ean14",
    "ean8",
    "ean8-guard",
    "gs1",
    "gs1_128",
    "gtin",
    "isbn",
    "isbn10",
    "isbn13",
    "issn",
    "itf",
    "jan",
    "nw-7",
    "pzn",
    "upc",
    "upca",
}

def calcular_checksum_ean(ean):
    """Calcula el checksum para un código EAN-13 o EAN-8."""
    suma_pares = sum(int(ean[i]) for i in range(len(ean)) if i % 2 == 1)
    suma_impares = sum(int(ean[i]) for i in range(len(ean)) if i % 2 == 0)
    total = suma_impares + (suma_pares * 3)
    checksum = (10 - (total % 10)) % 10
    return checksum

def generar_codigo_barras(texto, formato="code128", carpeta_salida="Codigo de barras", nombre_archivo="codigo_barras", extension="png"):
    """Generar un codigo de barras a partir de un texto dado
        :param texto: texto o número para el codigo de barras.
        :param formato: Formato del codigo de barras (code128, ean13, ean8, upc, upca, qr).
        :param carpeta_salida: Carpeta donde se guardara el codigo de barras.
        :param nombre_archivo: Nombre del archivo para el codigo de barras.
        :param extension: Extension del archivo para el codigo de barras (png, svg).
        :return: Ruta completa del archivo generado
    """

    #Validar el formato del codigo de barras
    if formato not in barcode.PROVIDED_BARCODES:
        raise ValueError (f"Formato '{formato} no soportado. Formatos disponibles: {', '.join(barcode.PROVIDED_BARCODES)}")

    # Validar y corregir texto para formatos específicos
    if formato in ("ean13", "ean8", "upc"):
        if not texto.isdigit():
            raise ValueError("Texto no válido para este formato. Debe ser un número de 13 dígitos.")
        if formato == "ean13" and len(texto) ==12:
            checksum= calcular_checksum_ean(texto)
            texto += str(checksum)
        elif formato == "ean8" and len(texto) == 7:
            checksum= calcular_checksum_ean(texto)
            texto += str(checksum)
        elif formato == "upc" and len(texto) == 11:
            checksum= calcular_checksum_ean(texto)
            texto += str(checksum)
        elif len(texto) != 13 and formato == "ean13":
            raise ValueError("EAN-13 debe tener 13 dígitos")
        elif len(texto) != 8 and formato == "ean8":
            raise ValueError("EAN-8 debe tener 8 dígitos")
        elif len(texto) != 12 and formato == "upc":
            raise ValueError("UPC debe tener 12 dígitos")

    #Crea la carpeta si no existe
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    #Crear el generado de barras
    codigo = barcode.get_barcode_class(formato)
    write= ImageWriter() if extension == 'png' else None
    barras_barras = codigo(texto, writer=write)

    #Generar el archivo
    ruta_archivo = os.path.join(carpeta_salida, f"{nombre_archivo}.{extension}")
    barras_barras.save(ruta_archivo.replace(f".{extension}", ""), options={"write_text": True})

    #abrir el archivo generado
    try:
        if os.name == "nt":
            os.startfile(ruta_archivo)
        elif os.name == "posix":
            subprocess.call(["open", ruta_archivo])
        else:
            subprocess.call(["xdg-open", ruta_archivo])
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")

    return ruta_archivo
