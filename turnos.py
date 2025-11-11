from os import remove
from utils import limpiar_pantalla, validar_fecha, validar_hora
from storage import cargar_turnos, guardar_turnos, bloqueos_por_fecha, _obtener_next_turno_id, cargar_clientes
from GMAIL import mensaje_confirmacion


# ---------------------------------------------------------
# FUNCIONES AUXILIARES 
# ---------------------------------------------------------

# Verifica si ya existe un turno ocupado en una fecha y hora determinada
def _existe_turno_en_slot(turnos, fecha, hora):
    return any(t for t in turnos if t["fecha"] == fecha and t["hora"] == hora and t["estado"] == "Ocupado")


# Verifica si un horario específico está bloqueado para una fecha
def _slot_bloqueado(fecha, hora):
    return hora in bloqueos_por_fecha.get(fecha, set())


# Verifica si un cliente con un DNI dado está activo en el sistema
def _cliente_activo(clientes, dni):
    c = clientes.get(dni)
    return bool(c and c.get("activo", False))


# ---------------------------------------------------------
# FUNCIÓN PRINCIPAL: ALTA DE TURNO
# ---------------------------------------------------------

def alta_turno(dni, fecha, hora):
    """
    Registra un nuevo turno para un cliente, si pasa todas las validaciones:
    - Fecha válida
    - Hora válida
    - Cliente activo
    - Horario no bloqueado
    - Horario no ocupado
    """
    
    clientes = cargar_clientes()
    turnos = cargar_turnos()
    next_id = _obtener_next_turno_id(turnos)

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
    if _existe_turno_en_slot(turnos, fecha, hora):
        print("✖ El horario ya está OCUPADO.")
        input("\nEnter...")
        limpiar_pantalla()
        return

    # Si todas las validaciones pasan, se crea el turno y se guarda
    t = {
        "id": next_id,           # Se genera un nuevo ID único
        "dni": dni,              # DNI del cliente
        "fecha": fecha,          # Fecha del turno
        "hora": hora,            # Hora del turno
        "estado": "Ocupado"      # Estado inicial del turno
    }

    mensaje_confirmacion(t)

    # Se agrega el turno a la lista global de turnos
    turnos.append(t)
    guardar_turnos(turnos)
    print("✔ Turno registrado correctamente.")
    
    # (Opcional) Llamada a una función para confirmar turno por mensaje o correo
    # confirmar_turno(t, clientes[dni])

    input("\nEnter para continuar...")
    limpiar_pantalla()


# ---------------------------------------------------------
# FUNCIÓN: LISTAR TURNOS
# ---------------------------------------------------------

def listar_turnos():
    """
    Muestra todos los turnos registrados en pantalla.
    Si no hay turnos, informa al usuario.
    """
    turnos = cargar_turnos()

    # Si no hay turnos, se muestra un mensaje y se limpia la pantalla
    if not turnos:
        print("No hay turnos registrados.")
        input("\nPresione Enter para continuar...")
        limpiar_pantalla()
        return
     
    # Recorre la lista de turnos (ordenada por fecha y hora) y muestra la información de cada uno
    for t in sorted(turnos, key=lambda x: (x["fecha"], x["hora"])):
        print(f"#{t['id']} | {t['fecha']} {t['hora']} | DNI {t['dni']} | {t['estado']}")
    
    input("\nPresione Enter para continuar...")
    limpiar_pantalla()

# ---------------------------------------------------------
# FUNCIÓN: LISTAR POR FECHA
# ---------------------------------------------------------

def listar_por_fecha(fecha):
    """
    Muestra todos los turnos en pantalla que conicidan con la fecha ingresada por parametro.
    """
    if not validar_fecha(fecha):
        print("✖ Fecha inválida. Formato esperado YYYY-MM-DD.")
        input("\nEnter...")
        limpiar_pantalla()
        return
    
    turnos = cargar_turnos()

    lista_fecha = [t for t in turnos if t["fecha"]==fecha]
    if not lista_fecha:
        print("No hay turnos para esa fecha.")
    for t in sorted(lista_fecha, key=lambda x: x["hora"]):
        print(f"#{t['id']} | {t['hora']} | DNI {t['dni']} | {t['estado']}")
    
    input("\nEnter para continuar...")
    limpiar_pantalla()


# ---------------------------------------------------------
# FUNCIÓN: DESBLOQUEAR_SLOT
# ---------------------------------------------------------

def desbloquear_slot(fecha, hora):

    turnos = cargar_turnos()

    # Validaciones
    if not validar_fecha(fecha):
        print("✖ Fecha inválida. Formato esperado YYYY-MM-DD.")
        input("\nEnter...")
        limpiar_pantalla()
        return

    if not validar_hora(hora):
        print("✖ Hora inválida. Formato esperado HH:mm.")
        input("\nEnter...")
        limpiar_pantalla()
        return


    # Busca el turno que coincida con la fecha y la hora indicadas
    for turno in turnos:
        if turno["fecha"] == fecha and turno["hora"] == hora:

            # Si el turno está ocupado, lo "desbloquea"
            if turno["estado"] == "Ocupado":

                turno["dni"] = "Sin Asignar"
                turno["estado"] = "Libre"
                print(f"✔ Turno {fecha} {hora} desbloqueado.")
                return
            
            # Si el turno ya estaba libre, informa que no se puede desbloquear
            else:
                print(f"✖ El turno {fecha} {hora} no está bloqueado.")
                return
            
    # En caso de no encontrar el turno lo informa
    print(f"✖ No se encontró el turno {fecha} {hora}.")

def eliminar_turno_por_id(id_turno):
    """
    Elimina un turno por su ID, recibida por parámetro.
    """
    turnos = cargar_turnos()

    for t in turnos:
        if t["id"] == id_turno:
            print(f"✔ Turno con ID {id_turno} - FECHA: {t['fecha']} - HORA: {t['hora']} - eliminado correctamente.")
            turnos.remove(t)
            guardar_turnos(turnos)
            input("\nPresione Enter para continuar...")
            limpiar_pantalla()
            return
    
    print(f"✖ Turno con ID {id_turno} no encontrado.")
    input("\nPresione Enter para continuar...")
    limpiar_pantalla()
    
            
