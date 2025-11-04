# Estructuras de datos globales para el sistema de gestión de turnos
import json
import os

# Rutas de archivos JSON
CLIENTES_JSON = "clientes.json"
TURNS_JSON = "turnos.json"

# ========== FUNCIONES DE PERSISTENCIA PARA CLIENTES ==========

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
clientes = {}

# Lista de turnos
turnos = []

# Contador para IDs de turnos
turno_id_counter = 1

# Slots bloqueados: lista de tuplas (fecha, hora)
slots_bloqueados = []

# Conjuntos por fecha para 'bloqueos' (slots no disponibles)
# {"2025-10-08": {"10:30", "14:00"}}
bloqueos_por_fecha = {}

# Autoincremental simple
_next_turno_id = 1
def next_turno_id():
    global _next_turno_id
    val = _next_turno_id
    _next_turno_id += 1
    return val
