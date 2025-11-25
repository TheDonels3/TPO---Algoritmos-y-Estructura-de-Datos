import json
import os
from datetime import datetime

# Rutas de archivos JSON
ARCHIVO_LOG = "archivos/logs.log"
CLIENTES_JSON = "archivos/clientes.json"
TURNS_JSON = "archivos/turnos.json"


# Funcion para Cargar los Clientes
def cargar_clientes():
    """Carga clientes desde el archivo JSON"""
    if os.path.exists(CLIENTES_JSON):
        try:
            with open(CLIENTES_JSON, 'r', encoding='utf-8') as f:
                contenido = f.read().strip()

                if not contenido:
                    log("INFO", "cargar_clientes", "Archivo de clientes vacío, se retorna diccionario vacío")
                    return {}

                # Cargar el JSON y retornarlo
                return json.loads(contenido)
            
        except json.JSONDecodeError as e:
            print(f"⚠ Error al cargar clientes: {e}. Iniciando con diccionario vacío.")
            log("ERRO", "cargar_clientes", f"JSONDecodeError: {e}")
            return {}

        except IOError as e:
            print(f"⚠ Error al leer el archivo de clientes: {e}. Iniciando con diccionario vacío.")
            log("ERRO", "cargar_clientes", f"IOError: {e}")
            return {}

    # Retorno por defecto si el archivo no existe
    log("INFO", "cargar_clientes", "Archivo de clientes no encontrado, se retorna diccionario vacío")
    return {}

# Funcion para Guradar los Clientes
def guardar_clientes(clientes_dict):
    """Guarda clientes en el archivo JSON"""
    try:
        with open(CLIENTES_JSON, 'w', encoding='utf-8') as f:
            json.dump(clientes_dict, f, ensure_ascii=False, indent=2)
            log("INFO", "guardar_clientes", "Clientes guardados correctamente")
        return True
    
    except IOError as e:
        print(f"✖ Error al guardar clientes: {e}")
        log("ERRO", "guardar_clientes", f"IOError: {e}")
        return False
    
# Diccionario de clientes: {dni: {datos del cliente}}
# clientes = {}

# Lista de turnos
turnos = []


# Funcion para Cargar el ID a Clientes
def _obtener_next_turno_id(turnos):
    """Calcula el siguiente ID de turno basándose en el ID máximo existente."""
    # Encuentra el máximo ID y le suma 1
    if not turnos:
        return 1
    else:
        return max((t.get("id") for t in turnos)) + 1


# Funcion para Cargar los Turnos de Clientes
def cargar_turnos():
    """Carga turnos desde el archivo JSON y devuelve la lista de turnos."""
    if os.path.exists(TURNS_JSON):
        try:
            with open(TURNS_JSON, 'r', encoding='utf-8') as f:
                contenido = f.read().strip()
                if not contenido:
                    log("INFO", "cargar_turnos", "Archivo de turnos vacío, se retorna lista vacía")
                    return []
                return json.loads(contenido)
            
        except (json.JSONDecodeError) as e:
            print(f"⚠ Error al cargar turnos: {e}. Iniciando con lista vacía.")
            log("ERRO", "cargar_turnos", f"JSONDecodeError: {e}")
            return []
        
        except (IOError) as e:
            print(f"⚠ Error al cargar turnos: {e}. Iniciando con lista vacía.")
            log("ERRO", "cargar_turnos", f"IOError: {e}")
            return []
        
    return [] # lista vacia si no hay archivo 


# Funcion para Guardar Turnos Cargados
def guardar_turnos(turnos_list):
    """Guarda la lista de turnos en el archivo JSON."""
    try:
        with open(TURNS_JSON, 'w', encoding='utf-8') as f:
            json.dump(turnos_list, f, ensure_ascii=False, indent=2)
            log("INFO", "guardar_turnos", "Turnos guardados correctamente")
        return True
    
    except IOError as e:
        print(f"✖ Error al guardar turnos: {e}")
        log("ERRO", "guardar_turnos", f"IOError: {e}")
        return False


#Funcion de Creacion de Log (Avisos)
def log(tipo, funcion, mensaje):
    """
    Escribe una línea en el archivo de log y verifica existencia
    """

    if not os.path.exists(ARCHIVO_LOG):
        with open(ARCHIVO_LOG, "w", encoding="utf-8") as f:
            print()

    with open(ARCHIVO_LOG, "a", encoding="utf-8") as f:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{fecha} | {tipo} | {funcion} | {mensaje}\n")


# Funcion para VISUALIZAR el Log
def ver_log():
    """
    Muestra en pantalla el contenido del archivo de log.
    """
    try:
        with open(ARCHIVO_LOG, "r", encoding="utf-8") as f:
            contenido = f.read()

        if contenido.strip() == "":
            print("El archivo de LOG está vacío.")
        else:
            print("\n====== REGISTRO DE LOGS ======\n")
            print(contenido)

    except FileNotFoundError:
        print("✖ El archivo de LOG no existe.")


# Slots bloqueados: lista de tuplas (fecha, hora)
slots_bloqueados = []

# Conjuntos por fecha para 'bloqueos' (slots no disponibles)
# {"2025-10-08": {"10:30", "14:00"}} -> Estructura del Diccionario
bloqueos_por_fecha = {}

