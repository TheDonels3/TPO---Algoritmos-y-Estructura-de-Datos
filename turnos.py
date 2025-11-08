from utils import limpiar_pantalla, validar_fecha, validar_hora
from storage import turnos, bloqueos_por_fecha, next_turno_id


# ---------------------------------------------------------
# FUNCIONES AUXILIARES 
# ---------------------------------------------------------

# Verifica si ya existe un turno ocupado en una fecha y hora determinada
def _existe_turno_en_slot(fecha, hora) -> bool:
    return any(t for t in turnos if t["fecha"] == fecha and t["hora"] == hora and t["estado"] == "Ocupado")


# Verifica si un horario específico está bloqueado para una fecha
def _slot_bloqueado(fecha, hora) -> bool:
    return hora in bloqueos_por_fecha.get(fecha, set())


# Verifica si un cliente con un DNI dado está activo en el sistema
def _cliente_activo(clientes, dni) -> bool:
    c = clientes.get(dni)
    return bool(c and c.get("activo", False))


# ---------------------------------------------------------
# FUNCIÓN PRINCIPAL: ALTA DE TURNO
# ---------------------------------------------------------

def alta_turno(clientes, dni, fecha, hora):
    """
    Registra un nuevo turno para un cliente, si pasa todas las validaciones:
    - Fecha válida
    - Hora válida
    - Cliente activo
    - Horario no bloqueado
    - Horario no ocupado
    """

    # Validación del formato de fecha (debe ser YYYY-MM-DD)
    if not validar_fecha(fecha):
        print("✖ Fecha inválida. Formato esperado YYYY-MM-DD.")
        input("\nEnter...")
        limpiar_pantalla()
        return
    
    # Validación del formato de hora (debe ser HH:mm)
    if not validar_hora(hora):
        print("✖ Hora inválida. Formato esperado HH:mm.")
        input("\nEnter...")
        limpiar_pantalla()
        return
    
    # Verificación de que el cliente exista y esté activo
    if not _cliente_activo(clientes, dni):
        print("✖ Cliente inexistente o inactivo.")
        input("\nEnter...")
        limpiar_pantalla()
        return
    
    # Comprobación de que el horario no esté bloqueado en esa fecha
    if _slot_bloqueado(fecha, hora):
        print("✖ El horario está BLOQUEADO para esa fecha.")
        input("\nEnter...")
        limpiar_pantalla()
        return
    
    # Verificación de que no exista ya un turno ocupado en ese horario
    if _existe_turno_en_slot(fecha, hora):
        print("✖ El horario ya está OCUPADO.")
        input("\nEnter...")
        limpiar_pantalla()
        return

    # Si todas las validaciones pasan, se crea el turno y se guarda
    t = {
        "id": next_turno_id(),   # Se genera un nuevo ID único
        "dni": dni,              # DNI del cliente
        "fecha": fecha,          # Fecha del turno
        "hora": hora,            # Hora del turno
        "estado": "Ocupado"      # Estado inicial del turno
    }

    # Se agrega el turno a la lista global de turnos
    turnos.append(t)
    print("✔ Turno registrado correctamente.")
    
    # (Opcional) Llamada a una función para confirmar turno por mensaje o correo
    # confirmar_turno(t, clientes[dni])

    input("\nEnter para continuar...")
    limpiar_pantalla()


# ---------------------------------------------------------
# FUNCIÓN: LISTAR TURNOS
# ---------------------------------------------------------

def listar_turnos(turnos):
    """
    Muestra todos los turnos registrados en pantalla.
    Si no hay turnos, informa al usuario.
    """

    # Si no hay turnos, se muestra un mensaje y se limpia la pantalla
    if len(turnos) == 0:
        print("No hay turnos registrados.")
        input("\nPresione Enter para continuar...")
        limpiar_pantalla()
        return
     
    # Recorre la lista de turnos y muestra la información de cada uno
    for turno in turnos:
        print(
            f"DNI: {turno['cliente_dni']} - "
            f"Fecha: {turno['fecha']} - "
            f"Hora: {turno['hora']} - "
            f"Tipo: {turno['tipo']} - "
            f"Estado: {turno['estado']}"
        )

    # Pausa para que el usuario lea la lista antes de limpiar la pantalla
    input("\nPresione Enter para continuar...")
    limpiar_pantalla()
