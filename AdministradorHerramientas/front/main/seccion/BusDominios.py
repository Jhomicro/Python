import sys
import os

#Ruta del directorio raíz del proyecto
ruta_raiz= os.path.abspath(os.path.join(os.path.dirname(__file__),"../../"))
if ruta_raiz not in sys.path:
    sys.path.insert(0, ruta_raiz)

from main.api_config.domainr import obtener_dominio_domainr, obtener_sugerencias_domainr
from main.api_config.godaddy import buscar_dominio_godaddy
from main.api_config.virusTotal import seguridad_dominio, verificar_dominio_virusTotal
import pandas as pd

"""
Lógica para buscar la disponibilidad de un dominio
Lo que va a realizar es:
1. Busqueda exhaustiva de disponibilidad de dominio.
2. Consulta MultitLD = Verifica la disponibilidad de un dominio en múltiples
    TLDs (ejemplo: .com, .net, .org, .io)
3. Sugerencias de Dominios Alternativos
4. Informe Detallado del Dominio
5. Verificación de Seguridad del Dominio
6. Monitoreo de Expiración
7. Generador de Reportes Personalizados
8. Verificación Geolocalizada
9. Consulta Masiva de Dominios

Parametros:
dominio (str): Nombre del dominio a buscar(ejemplo.com)

Retorna:
str: Mensaje indicando si el dominio está disponible o ya esta registrado
"""

# Función común para manejar respuesta api
def manejar_respuesta(response):
    # Verificar si es un diccionario (ya procesado)
    if isinstance(response, dict):
        return response
    # Si es una respuesta HTTP, manejarla
    if hasattr(response, 'status_code'):
        if response.status_code == 200:
            return response.json()
        return {
            "Error": f"Error: {response.status_code}: {response.text}",
            "Detalles": response.text
        }
    return {"Error": "Respuesta inesperada"}

# Función común para obtener resultados de busqueda de dominio
def buscar_dominio(dominio, func):
    try:
        response = func(dominio)
        return manejar_respuesta(response)
    except Exception as e:
        return {"Error": str(e)}

# 1. Busqueda exhaustiva de disponibilidad de dominio.
def busqueda_disponibilidad_exhaustiva(dominio):
    """
    Busca la disponibilidad en todas las api
    """
    resultado = {
        "godaddy" : buscar_dominio(dominio, buscar_dominio_godaddy),
        "domainr" : buscar_dominio(dominio, obtener_dominio_domainr)
    }
    return resultado
# 2. Consulta MultitLD = Verifica la disponibilidad de un dominio en múltiples TLDs
def buscar_MultitLD(base_dominio, tlds):
    """
    Consulta la disponibilidad de un dominio en múltiples TLDs
    """
    return {f"{base_dominio}.{tld}": busqueda_disponibilidad_exhaustiva(f"{base_dominio}.{tlds}") for tld in tlds}
# 3. Sugerencias de Dominios Alternativos
def sugerir_dominios_alternativos(base_dominio):
    """
    Obtiene sugerencias de dominios alternativos
    """
    try:
        response = obtener_sugerencias_domainr(base_dominio)
        return response.get("suggestions", {"Error": "No hay sugerencias disponibles"})
    except Exception as e:
        return {"Error": str(e)}
# 4. Informe Detallado del Dominio
def informe_dominio(dominio):
    """
    Obtiene un informe detallado del dominio
    """
    return {"dominio": dominio, "resultados": busqueda_disponibilidad_exhaustiva(dominio)}
# **5. Verificación de Seguridad del Dominio**
def verificar_seguridad_dominio(dominio):
    """
    Verifica la seguridad del dominio
    """
    try:
        #Obtener información de virus Total
        response = verificar_dominio_virusTotal(dominio)
        analisis_virusTotal = seguridad_dominio(response)

        return {**analisis_virusTotal, "Blacklisted": False, "Estado final": "Dominio seguro"}
    except Exception as e:
        return {"Error": f"Error al verificar la seguridad del dominio: {str(e)}"}

# **6. Monitoreo de Expiración**
def monitoreo_expiracion(dominio):
    """
    Monitorea la expiración del dominio
    """
    try:
        resultados = busqueda_disponibilidad_exhaustiva(dominio)
        fecha_expiracion = resultados.get("godaddy", {}).get("expires")
        if fecha_expiracion:
            return {"Dominio": dominio, "fecha de expiracion": fecha_expiracion}
        return {"Error": "Información no disponible"}
    except Exception as e:
        return {"Error": str(e)}

# **7. Generador de Reportes Personalizados**
def generar_reporte_personalizado(dominios, filename = "reporte_dominio.csv"):
    """
    Genera un reporte personalizado del dominio
    """
    try:
        data = [{"Dominio": dominio, "Detalles": str(informe_dominio(dominio))} for dominio in dominios]
        pd.DataFrame(data).to_csv(filename, index=False)
        return f"Reporte generado en {filename}"
    except Exception as e:
        return {"Error": str(e)}
# **8. Verificación Geolocalizada**
def verificar_ccTLDs(base_dominio, ccTLDs):
    """
    Verifica la geolocalización del dominio
    """
    return buscar_MultitLD(base_dominio, ccTLDs)
# **9. Consulta Masiva de Dominios**
def consulta_masiva(dominios, batch_size=10):
    """
    Consulta la disponibilidad de varios dominios
    """
    # Guardar los resultados
    resultados = {}
    for i in range(0, len(dominios), batch_size):
        batch = dominios[i:i+batch_size]
        for dominio in batch:
            resultados[dominio] = busqueda_disponibilidad_exhaustiva(dominio)
    return resultados

def formatear_resultado(resultado):
    """
    Formatea el resultado de la consulta
    """
    if not resultado:
        return "No se recibieron datos"
    mensajes=[]
    #Godaddy
    godaddy=resultado.get("godaddy", {})
    if godaddy:
        disponible= "Disponible" if godaddy.get("available", False) else "No disponible"
        mensajes.append(f"**Godaddy\nDominio:{godaddy.get('Domain', 'Desconocido')}\nEstado:{disponible}")
    #Domainr
    domainr = resultado.get("domainr", {})
    domain_data=domainr.get("domain")
    if domain_data and isinstance(domain_data, dict):
        dominio = domain_data.get("domain", "Desconocido")
        mensajes.append(f"**Domainr**\nDominio: {dominio}")
    else:
        dominio = "No especificado"
    mensajes.append(f"**Domainr\nDomain:{dominio}")

    return "\n\n".join(mensajes)