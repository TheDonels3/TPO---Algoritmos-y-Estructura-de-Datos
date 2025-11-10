import os
import re

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
    
    # Variables
    MAX_ANIO = 2027
    MIN_ANIO = 2025
    esValido = True
    meses = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # Validar formato
    if not bool(RE_FECHA.match(fecha)):
        esValido = False
        
    else:
        anio = int(fecha[0:4])
        mes = int(fecha[5:7])
        dia = int(fecha[8:10])

        # Año bisiesto 
        if (anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)):
            meses[1] = 29

        # Rango de año
        if (anio < MIN_ANIO or anio > MAX_ANIO):
            esValido = False

        # Rango de mes
        if not (1 <= mes <= 12):
            esValido = False
        
        #Rango de Dias
        elif not (1 <= dia <= meses[mes - 1]):
            esValido = False

    return esValido


# Devuelve True si la hora cumple el formato HH:mm, False si no
def validar_hora(hora):
    return bool(RE_HORA.match(hora))