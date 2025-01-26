from datetime import datetime, timedelta
import pytz
from pytz import timezone
from astral import LocationInfo
from astral.sun import sun

def calcular_fecha_hora(fecha_inicio_str, dias = 0, horas= 0, minutos = 0):
    """
        Calcular una nueva fecha y hora sumando o restando días, horas o minutos a una fecha base
    """

    try:
        if " " in fecha_inicio_str:
            fecha_base = datetime.strptime(fecha_inicio_str,"%Y-%m-%d %H:%M:%S")
        else:
            fecha_base = datetime.strptime(fecha_inicio_str,"%Y-%m-%d")

        nueva_fecha_hora = fecha_base + timedelta(days=dias, hours=horas, minutes=minutos)

        return nueva_fecha_hora
    except ValueError as e:
        raise ValueError(f"Formato de fecha no valido")

def convertir_zona_horaria(fecha_hora, zona_origen, zona_destino):
    """
    Convierte una fecha y hora de una zona horaria a otra.
    """
    try:
        tz_origen = timezone(zona_origen)
        tz_destino = timezone(zona_destino)
        if fecha_hora.tzinfo is None:
            fecha_hora = tz_origen.localize(fecha_hora)
        return fecha_hora.astimezone(tz_destino)
    except Exception as e:
        raise ValueError(f"Error al convertir zonas horarias: {e}")

def diferencia_entre_fechas(fecha_inicio_str, dia_objetivo, unidad="segundos"):
    """
    Calcula la diferencia entre dos fechas en la unidad especificada (días, horas, minutos, segundos).
    """
    try:
        formato = "%Y-%m-%d %H:%M:%S" if " " in fecha_inicio_str else "%Y-%m-%d"
        fecha_inicio = datetime.strptime(fecha_inicio_str, formato)
        fecha_fin = datetime.strptime(dia_objetivo, formato)
        delta = fecha_fin - fecha_inicio

        if unidad == "días":
            return delta.days
        elif unidad == "horas":
            return delta.days * 24 + delta.seconds // 3600
        elif unidad == "minutos":
            return delta.days * 24 * 60 + delta.seconds // 60
        elif unidad == "segundos":
            return delta.total_seconds()
        else:
            raise ValueError("Unidad no valida. Use días, horas, minutos, o segundos:")
    except Exception as e:
        raise ValueError(f"Formato de fecha no válido: {e}")

def calcula_proxima_dia(fecha_inicio_str, dia_objetivo):
    """
    Calcula la fecha del próximo lunes, viernes, o cualquier día de la semana.
    Parámetros:
        fecha_inicio_str (str): Fecha de inicio en formato 'YYYY-MM-DD'.
        dia_objetivo_o_str (Union[int, str]): Día objetivo (0-6) o una fecha en formato 'YYYY-MM-DD'.

    Retorna:
        datetime: Fecha del próximo día objetivo.
    """
    try:

        fecha_base = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
        dias_a_sumar = (dia_objetivo - fecha_base.weekday()) % 7
        if dias_a_sumar == 0:
            dias_a_sumar = 7
        return fecha_base + timedelta(days=dias_a_sumar)
    except Exception as e:
        raise ValueError(f"Error al calcular la próxima fecha: {e}")

def calcular_amanecer_atardecer(fecha, lat, lon):
    """
    Calcula horarios de amanecer y atardecer basados en una ubicación.
    """


    try:
        if isinstance(fecha, datetime):
            fecha = fecha.date()
        ciudad = LocationInfo(latitude=lat, longitude= lon)
        s = sun (ciudad.observer, date= fecha)
        tz=pytz.timezone("America/New_York")
        #Retornar los horarios de amanecer y atardecer
        sunrise_local= s['sunrise'].astimezone(tz)
        sunset_local= s['sunset'].astimezone(tz)
        return sunrise_local, sunset_local
    except Exception as e:
        raise ValueError(f"Error al calcular horarios de amanecer y atardecer: {e}")
