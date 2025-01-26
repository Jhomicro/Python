import json

# UNIDADES de medida
UNIDADES ={
    "Longitud":{
        "metros": 1,
        "kilometros": 1000,
        "centimetros": 0.01,
        "milimetros": 0.001,
        "pulgadas": 0.0254,
        "yards": 0.9144,
        "Millas": 1609.34,
        "Nanómetros": 1e-9,
        "Micrómetro": 1e-6
    },
    "Peso":{
        "kilogramos": 1,
        "gramos": 1000,
        "libras": 2.20462,
        "onzas": 35.274,
        "Toneladas": 1000
    },
    "Volumen":{
        "litros": 1,
        "mililitros": 0.001,
        "Galones": 0.264172,
        "Pintas": 2.11338,
        "Onzas líquidas": 33.814,
        "Cúbicos":1000,
        "centilitros": 0.01,
        "decilitros": 0.1
    },
    "Temperatura":{
        "Celsius": ["C", "lambda c: c", "lambda c: c"],
        "Fahrenheit":["F", "lambda c: c * 9/5 + 32", "lambda f: (f - 32)* 5/9"],
        "kelvin": ["K", "lambda c: c + 273.15", "lambda k: k - 273.15"]
    },
    "Tiempo":{
        "milisegundos": 0.001,
        "segundos": 1,
        "minutos": 60,
        "horas": 3600,
        "dias": 86400,
        "semanas": 604800
    },
    "Energía":{
        "Joules": 1,
        "Kilojoules": 1000,
        "Calorías": 4.184,
        "Kilocalorías": 4184,
        "Vatios-hora": 3600,
        "Kilovatios-hora": 3.6e+6,
        "Electrón-voltios": 1.60218e-19
    },
    "Velocidad":{
        "metros/segundos": 1,
        "kilometros/hora": 1000/ 3600,
        "Millas/hora": 1609.34 / 3600,
        "Nudos": 1852 / 3600,
    }
}


def convertir_UNIDADES(cantidad, unidad_origen, unidad_destino, tipo):
    """
    Realiza la conversión de UNIDADES basado en el tipo.
    """
    if tipo not in UNIDADES:
        raise ValueError (f"El tipo {tipo} no existe en las unidades disponibles.")


    # Verificar si las UNIDADES están en el diccionario
    if unidad_origen not in UNIDADES[tipo] or unidad_destino not in UNIDADES[tipo]:
        return "Unidad no encontrada en el directorio de conversiones."

    # Manejar conversiones especiales como temperatura
    if tipo == "Temperatura":
        if unidad_origen == unidad_destino:
            return cantidad
        cantidad_celsius = eval(UNIDADES[tipo][unidad_origen][1])(cantidad)
        return eval(UNIDADES[tipo][unidad_destino][2])(cantidad_celsius)

    # Conversiones lineales
    cantidad_base = cantidad * UNIDADES[tipo][unidad_origen]
    return cantidad_base / UNIDADES[tipo][unidad_destino]