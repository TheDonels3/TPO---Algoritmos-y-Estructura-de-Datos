import json
import os

# Rutas de archivos JSON
CLIENTES_JSON = "archivos/clientes.json"
TURNS_JSON = "archivos/turnos.json"

# ========== FUNCIONES PARA CLIENTES ==========
def cargar_clientes():
    """Carga clientes desde el archivo JSON"""
    if os.path.exists(CLIENTES_JSON):
        try:
            with open(CLIENTES_JSON, 'r', encoding='utf-8') as f:
                contenido = f.read().strip()

                if not contenido:
                    return {}
                return json.loads(contenido)
            
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠ Error al cargar clientes: {e}. Iniciando con diccionario vacío.")
            return {}
        except IOError as e:
            print(f"⚠ Error al leer el archivo de clientes: {e}. Iniciando con diccionario vacío.")
            return {}
    return {}


def guardar_clientes(clientes_dict):
    """Guarda clientes en el archivo JSON"""
    try:
        with open(CLIENTES_JSON, 'w', encoding='utf-8') as f:
            json.dump(clientes_dict, f, ensure_ascii=False, indent=2)
        return True
    
    except IOError as e:
        print(f"✖ Error al guardar clientes: {e}")
        return False
    
# Diccionario de clientes: {dni: {datos del cliente}}
# clientes = {}

# Lista de turnos
turnos = []

def _obtener_next_turno_id(turnos):
    """Calcula el siguiente ID de turno basándose en el ID máximo existente."""
    if not turnos:
        return 1
    # Encuentra el máximo ID y le suma 1
    return max(t.get("id") for t in turnos) + 1

def cargar_turnos():
    """Carga turnos desde el archivo JSON y devuelve la lista de turnos."""
    if os.path.exists(TURNS_JSON):
        try:
            with open(TURNS_JSON, 'r', encoding='utf-8') as f:
                contenido = f.read().strip()
                if not contenido:
                    return []
                return json.loads(contenido)
            
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
        with open(TURNS_JSON, 'w', encoding='utf-8') as f:
            json.dump(turnos_list, f, ensure_ascii=False, indent=2)
        return True
    
    except IOError as e:
        print(f"✖ Error al guardar turnos: {e}")
        return False


# Slots bloqueados: lista de tuplas (fecha, hora)
slots_bloqueados = []

# Conjuntos por fecha para 'bloqueos' (slots no disponibles)
# {"2025-10-08": {"10:30", "14:00"}}
bloqueos_por_fecha = {}

