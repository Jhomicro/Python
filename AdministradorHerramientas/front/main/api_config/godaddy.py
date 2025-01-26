import requests
def buscar_dominio_godaddy(dominio, environment="OTE"):
    """
    Realiza una busqueda de un dominio utilizando la api de Godaddy
    """
    api_config = API_CONFIG_GODADDY[environment]

    url = f"{api_config['BASE_URL']}domains/available?domain={dominio}"
    headers = {
        "Authorization": f"sso-key {api_config['API_KEY']}:{api_config['API_SECRET']}",
        "Accept": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        #Verificamos el estado de la respuesta
        if response.status_code == 200:
            return response.json()  # Se obtiene la información del dominio
        else:
            # Si la respuesta tiene otro código de estado, mostramos el mensaje de error
            return {"Error": f"Error {response.status_code}: {response.text}"}
    except requests.exceptions.RequestException as e:
        # Capturamos excepciones generales de la librería 'requests'
        return {"Error": f"Error en la solicitud HTTP: {str(e)}"}
    except Exception as e:
        # Capturamos cualquier otra excepción que pueda ocurrir
        return {"Error": str(e)}