# utils.py
import os
import re
from datetime import datetime

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

# Validaciones simples
RE_DNI = re.compile(r"^\d{7,8}$")  # DNI argentino simple (7 u 8 dígitos)
RE_HORA = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")  # HH:mm 00..23:00..59
RE_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$")  # YYYY-MM-DD

def hoy_str():
    return datetime.now().strftime("%Y-%m-%d")

def validar_dni(dni:str)->bool:
    return bool(RE_DNI.match(dni))

def validar_fecha(fecha:str)->bool:
    if not RE_FECHA.match(fecha):
        return False
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validar_hora(hora:str)->bool:
    return bool(RE_HORA.match(hora))

def comparar_fecha_str(a:str, b:str)->int:
    # Retorna -1 si a<b, 0 si igual, 1 si a>b
    da = tuple(map(int, a.split("-")))
    db = tuple(map(int, b.split("-")))
    return (da>db) - (da<db)
