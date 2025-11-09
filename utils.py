import os
import re
from datetime import datetime

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


# Validaciones simples con expresiones regulares
RE_DNI = re.compile(r"^\d{7,8}$")  # DNI argentino simple (7 u 8 digitos)
RE_HORA = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")  # HH:mm entre 00:00 y 23:59
RE_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$")  # Formato YYYY-MM-DD


# Devuelve True si el DNI cumple el formato, False si no
def validar_dni(dni):
    return bool(RE_DNI.match(dni))


# Valida que la fecha cumpla el formato y sea una fecha valida
def validar_fecha(fecha):
    if not RE_FECHA.match(fecha):
        return False
    
    # Intenta convertir la cadena a fecha para verificar que sea valida
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True
    
    # Si hay error al convertir, la fecha no es valida
    except ValueError:
        return False


 # Devuelve True si la hora cumple el formato HH:mm, False si no
def validar_hora(hora):
    return bool(RE_HORA.match(hora))


# Compara dos fechas en formato YYYY-MM-DD
# Retorna -1 si a < b, 0 si son iguales, 1 si a > b
def comparar_fecha_str(a, b):
    da = tuple(map(int, a.split("-")))
    db = tuple(map(int, b.split("-")))
    return (da > db) - (da < db)