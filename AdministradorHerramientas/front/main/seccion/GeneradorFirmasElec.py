from PIL import Image, ImageDraw, ImageFont
from fpdf import FPDF

def generador_forma_texto(nombre, cargo, archivo_salida="Firma.png"):
    """
    Genera una firma electrónica básica con el nombre y cargo.

    Parámetros:
    - nombre (str): Nombre de la persona.
    - cargo (str): Cargo de la persona.
    - archivo_salida (str): Nombre del archivo de salida.

    Retorna:
    - str: Mensaje indicando si la firma fue generada con éxito.
    """
    try:
        #Crear una imagen en blanco
        ancho, alto = 400, 150
        imagen = Image.new("RGB", (ancho, alto), color=(255,255,255))
        draw = ImageDraw.Draw(imagen)

        #Usar una fuente basica
        try:
            font = ImageFont.truetype("Arial.ttf", 20)
        except IOError:
            font = ImageFont.load_default()

        #Escribir el nombre y cargo
        draw.text((10, 10), f"Firma: {nombre}", fill=(0,0,0), font=font)
        draw.text((10, 50), f"Cargo: {cargo}", fill=(0,0,0), font=font)

        #Guardar la imagen
        imagen.save(archivo_salida)
        return f"Firma generada correctamente en {archivo_salida}"
    except Exception as e:
        return f"Error generando la firma: {str(e)}"

def generar_pdf_firma(nombre, cargo, archivo_pdf="firma_documento.pdf"):
    """
    Genera un archivo PDF con la firma electrónica, incluyendo nombre, cargo

    Parametros:
    - nombre (str): Nombre de la persona
    - cargo (str): Cargo de la persona
    - archivo_pdf: Nombre del archivo PDF de salida.

    Retorna:
    - str: Mensaje indicando si el pdf fue generado con exito
    """

    try:
        # Crear un objeto FPDF
        pdf = FPDF()
        pdf.add_page()

        # Establecer el titulo
        pdf.set_font("Arial", size=14)
        pdf.cell(200, 10, txt="Firma electrónica", ln=True, align='C')
        # Agregar espacio
        pdf.ln(10)
        # Agregar nombre y cargo
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Nombre: {nombre}", ln=True)
        pdf.cell(200, 10, txt=f"Cargo: {cargo}", ln=True)

        # Guardar el PDF
        pdf.output(archivo_pdf)
        return f"PDF generado correctamente en {archivo_pdf}"
    except Exception as e:
        return f"Error generando el PDF: {str(e)}"