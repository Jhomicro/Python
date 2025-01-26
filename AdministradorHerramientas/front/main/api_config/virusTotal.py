import requests

def verificar_dominio_virusTotal(dominio):
    """
    Verifica un dominio usando la API de VirusTotal.
    :param dominio: Nombre del dominio a verificar (por ejemplo, "example.com")
    :param api_key: Tu clave de API de VirusTotal
    :return: Un diccionario con el resultado de la verificación
    """

    url = f"https://www.virustotal.com/api/v3/domains/{dominio}"
    headers = {
        "x-apikey": API_CONFIG_virus_total["API_KEY"]
    }

    try:
        #Realizar la solicitud GET a la api
        response = requests.get(url, headers=headers)

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            # Decodificar el resultado en JSON
            return response
        else:
            return {"error": f"Error de respuesta: {response.status_code}: {response.text}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Error de red: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}

#Seguridad de dominio
def seguridad_dominio(response):
    """
    Procesa la respuesta de la API de VirusTotal y devuelve un diccionario con los resultados
    :param response: Respuesta de la API de VirusTotal
    :return: Diccionario con los resultados de la verificación
    """

    if isinstance(response, dict) and "error" in response:
        return response #TODO Devuelce el error si esta presente

    if response.status_code == 200:
        data = response.json()

        # Verificar si el dominio ha sido analizado
        if "data" in data and "attributes" in data["data"]:
            attributes = data["data"]["attributes"]

            # Estadísticas del análisis
            analysis_stats = attributes.get("last_analysis_stats", {})

            # Información de las detecciones
            detections = analysis_stats.get("malicious", 0)
            suspicious = analysis_stats.get("suspicious", 0)
            harmless = analysis_stats.get("harmless", 0)
            unknown = analysis_stats.get("undetected", 0)

            # Si el dominio tiene detecciones maliciosas, considerarlo inseguro
            seguridad = {
                "dominio": response.url.split("/")[-1],
                "Detecciones Maliciosas": detections,
                "Detecciones sospechosas": suspicious,
                "Detecciones inofensivas": harmless,
                "desconocido": unknown,
                "Detecciones Totales": detections + suspicious + harmless + unknown,
            }

            #Determinar si el dominio es seguro

            if detections > 0:
                seguridad["seguridad"] = "Inseguro"
            else:
                seguridad["seguridad"] = "Seguro"

            return seguridad
        else:
            return {"error": "No se ha encontrado información sobre el dominio"}
    else:
        return {"error": f"Error de respuesta: {response.status_code}: {response.text}"}
