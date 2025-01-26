#Mapa de calor basico
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
#Mapa de calor geografico
import folium
from folium.plugins import HeatMap
#Cargar datos desde CSV o JSON
import pandas as pd
#Exportar reportes pdf
from fpdf import FPDF
#Guardar y cargar configuraciones
import json

#Generar mapa de basico
def generar_mapa_calor_basico(datos, nombre_archivo="Mapa_calor_basico.png", paleta="viridis"):
    """
    Generar mapa de calor basico
    """
    try:
        #Validar datos
        if not isinstance(datos, (list, np.ndarray)):
            raise ValueError ("Error: los datos deben ser una lista")
        datos = np.array(datos)
        if len(datos.shape) !=2:
            raise ValueError ("Error: los datos deben ser una matriz 2D")
        #Etiquetas dinamicas
        etiquetas_x=[f"x-{i+1}" for i in range(datos.shape[1])]
        etiquetas_y=[f"Y-{i+1}" for i in range(datos.shape[0])]
        #Crear el mapa de calor
        plt.figure(figsize=(10,8))
        sns.heatmap(datos, annot=True,fmt=".2f", cmap=paleta, xticklabels=etiquetas_x, yticklabels=etiquetas_y)
        plt.title("Mapa de calor basico")
        plt.savefig(nombre_archivo)
        return f"Mapa de calor basico generado correctamente con el nombre {nombre_archivo}"
    except Exception as e:
        return f"Error generando el mapa de calor basico: {str(e)}"

def generar_mapa_calor_geografico(coordenadas, nombre_archivo="Mapa_calor.html"):
    """
    Generar mapa de calor geografico basado en coordenadas
    """
    try:
        #Validar coordenadas
        if not all(isinstance(coord, tuple) and len(coord) == 2 for coord in coordenadas):
            raise ValueError ("Las coordenadas deben ser una lista de tuplas")
        #Crear mapa con centro en las coordenadas
        mapa = folium.Map(location=coordenadas[0], zoom_start=12)

        #Agregar los puntos al mapa
        for lat, lon in coordenadas:
            folium.CircleMarker(location=[lat, lon]).add_to(mapa)

        #Guardar el mapa en un HTML
        mapa.save(nombre_archivo)
    except Exception as e:
        return f"Error generando el mapa de calor geografico: {str(e)}"

def cargar_datos_csv(archivo_csv):
    """
    Cargar datos desde un CSV
    """
    try:
        return pd.read_csv(archivo_csv)
    except Exception as e:
        return f"Error cargando los datos del CSV: {str(e)}"

def cargar_datos_json(archivo_json):
    """
    Cargar datos desde un JSON
    """
    try:
        datos = pd.read_json(archivo_json)
        return datos
    except Exception as e:
        return f"Error cargando los datos del JSON: {str(e)}"

def generar_reporte_pdf(titulo, estadisticas, nombre_archivo="Reporte_calor.pdf"):
    """
    Generar un PDF con estadisticas y titulo
    """
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', size=16)
        pdf.cell(200, 10, txt=titulo, ln=True,align='C')
        pdf.ln(10)
        
        for linea in estadisticas:
            pdf.cell(200, 10, txt=linea, ln=True)
        
        pdf.output(nombre_archivo)
        return f"Reporte generado correctamente en {nombre_archivo}"
    except Exception as e:
        return f"Error generando el reporte PDF: {str(e)}"

def guardar_configuracion(configuracion, nombre_archivo="config.json"):
    """
    Guarda configuraciones en un archivo JSON
    """
    try:
        with open(nombre_archivo, "w") as archivo:
            json.dump(configuracion, archivo)
        return f"Configuracion guardada correctamente en {nombre_archivo}"
    except Exception as e:
        return f"Error cargando la configuracion: {str(e)}"

def cargar_configuracion(nombre_archivo="config.json"):
    """
    Carga configuraciones desde el archivo JSON
    """
    try:
        with open(nombre_archivo, "r") as archivo:
            configuracion= json.load(archivo)
        return configuracion
    except Exception as e:
        return f"Error cargando la configuracion: {str(e)}"