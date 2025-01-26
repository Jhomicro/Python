import requests
import time

def obtener_dominio_domainr(dominio):
    """
    Realizar la busqueda de un dominio en la api de domainr
    """
    try:
        url = API_CONFIG_DOMAINR["BASE_URL"]
        headers = {
            "x-rapidapi-key": API_CONFIG_DOMAINR["API_KEY"],
            "x-rapidapi-host": "domain-checker7.p.rapidapi.com",
        }

        params = {
            "domain": dominio,
        }

    # Realizamos la petición
        response = requests.get(url, headers=headers)
        if response.status_code == 429:
            print("Límite de solicitudes alcanzado. Esperando 60 segundos para reintentar...")
            time.sleep(60)
            return obtener_dominio_domainr(dominio)
        if response.status_code == 200:
            data = response.json()
            print("Respuesta completa de la api:" , data)
            # Accediendo tanto al dominio como a las sugerencias
            domain_info = data.get("domain", {})
            return {
                "domain": domain_info
            }
        else:
            return {"Error": f"Error {response.status_code}: {response.status_code}"}
    except Exception as e:
        return {"Error": str(e)}
def obtener_sugerencias_domainr(dominio):
    """
    Obtener las sugerencias para un dominio en la API de domainr
    """
    try:
        url = API_CONFIG_DOMAINR["BASE_URL"]
        headers = {
            "x-rapidapi-key": API_CONFIG_DOMAINR["API_KEY"],
            "x-rapidapi-host": "domain-checker7.p.rapidapi.com",
        }

        params = {
            "domain": dominio,
        }

        # Realizamos la petición
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            # Accediendo a las sugerencias
            suggestions = data.get("suggestions", [])
            return {"suggestions": suggestions}
        else:
            return {"Error": f"Error {response.status_code}: {response.status_code}"}
    except Exception as e:
        return {"Error": str(e)}