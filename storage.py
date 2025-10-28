# Estructuras de datos globales para el sistema de gestión de turnos

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
