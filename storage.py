import json
import os
from datetime import datetime


# Rutas de archivos JSON
ARCHIVO_LOG = "archivos/logs.log"
CLIENTES_JSON = "archivos/clientes.json"
TURNS_JSON = "archivos/turnos.json"

# ========== FUNCIONES PARA CLIENTES ==========
def cargar_clientes():
    """Carga clientes desde el archivo JSON"""
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_completa = os.path.join(ruta_actual, CLIENTES_JSON)
    
    if os.path.exists(ruta_completa):
        try:
            with open(ruta_completa, 'r', encoding='utf-8') as f:
                return json.load(f) or {}
            
        except (json.JSONDecodeError) as e:
            print(f"⚠ Error al cargar clientes: {e}. Iniciando con diccionario vacío.")
            return {}
        except IOError as e:
            print(f"⚠ Error al leer el archivo de clientes: {e}. Iniciando con diccionario vacío.")
            return {}
    return {}


def guardar_clientes(clientes_dict):
    """Guarda clientes en el archivo JSON"""
    try:
        ruta_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_completa = os.path.join(ruta_actual, CLIENTES_JSON)

        with open(ruta_completa, 'w', encoding='utf-8') as f:
            json.dump(clientes_dict, f, ensure_ascii=False, indent=2)
        return True
    
    except IOError as e:
        print(f"✖ Error al guardar clientes: {e}")
        return False
    
# ========== FUNCIONES PARA TURNOS ==========

def _obtener_next_turno_id(turnos):
    """Calcula el siguiente ID de turno basándose en el ID máximo existente."""
    # Encuentra el máximo ID y le suma 1
    if not turnos:
        return 1
    else:
        return max((t.get("id") for t in turnos)) + 1

def cargar_turnos():
    """Carga turnos desde el archivo JSON y devuelve la lista de turnos."""
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_completa = os.path.join(ruta_actual, TURNS_JSON)
    
    if os.path.exists(ruta_completa):
        try:
            with open(ruta_completa, 'r', encoding='utf-8') as f:
                return json.load(f) or []
            
        except (json.JSONDecodeError) as e:
            print(f"⚠ Error al cargar turnos: {e}. Iniciando con lista vacía.")
            return []
        except (IOError) as e:
            print(f"⚠ Error al cargar turnos: {e}. Iniciando con lista vacía.")
            return []
        
    return [] # lista vacia si no hay archivo 

def guardar_turnos(turnos_list):
    """Guarda la lista de turnos en el archivo JSON."""
    try:
        ruta_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_completa = os.path.join(ruta_actual, TURNS_JSON)
        
        with open(ruta_completa, 'w', encoding='utf-8') as f:
            json.dump(turnos_list, f, ensure_ascii=False, indent=2)
        return True
    
    except IOError as e:
        print(f"✖ Error al guardar turnos: {e}")
        return False

# ========== FUNCIONES PARA LOGS ==========

#Funcion de Creacion de Log (Avisos)
def log(tipo, funcion, mensaje):
    """
    Escribe una línea en el archivo de log y verifica existencia
    """
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_completa = os.path.join(ruta_actual, ARCHIVO_LOG)

    if not os.path.exists(ruta_completa):
        with open(ruta_completa, "w", encoding="utf-8") as f:
            print()

    with open(ruta_completa, "a", encoding="utf-8") as f:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{fecha} | {tipo} | {funcion} | {mensaje}\n")


# Funcion para VISUALIZAR el Log
def ver_log():
    """
    Muestra en pantalla el contenido del archivo de log.
    """
    try:
        ruta_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_completa = os.path.join(ruta_actual, ARCHIVO_LOG)
        
        with open(ruta_completa, "r", encoding="utf-8") as f:
            contenido = f.read()

        if contenido.strip() == "":
            print("El archivo de LOG está vacío.")
        else:
            print(contenido)

    except FileNotFoundError:
        print("✖ El archivo de LOG no existe.")



