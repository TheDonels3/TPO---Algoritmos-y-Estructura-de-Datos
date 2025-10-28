from typing import Dict, List, Tuple
from utils import limpiar_pantalla, validar_fecha, validar_hora, hoy_str, comparar_fecha_str
from storage import turnos, bloqueos_por_fecha, next_turno_id

def _slot_key(fecha:str, hora:str)->Tuple[str,str]:
    return (fecha, hora)

def _existe_turno_en_slot(fecha:str, hora:str)->bool:
    return any(t for t in turnos if t["fecha"]==fecha and t["hora"]==hora and t["estado"]=="Ocupado")

def _slot_bloqueado(fecha:str, hora:str)->bool:
    return hora in bloqueos_por_fecha.get(fecha, set())

def _cliente_activo(clientes:Dict[str,dict], dni:str)->bool:
    c = clientes.get(dni)
    return bool(c and c.get("activo", False))

def alta_turno(clientes:Dict[str,dict], dni:str, fecha:str, hora:str):
    # Validaciones
    if not validar_fecha(fecha):
        print("✖ Fecha inválida. Formato esperado YYYY-MM-DD."); input("\nEnter..."); limpiar_pantalla(); return
    if not validar_hora(hora):
        print("✖ Hora inválida. Formato esperado HH:mm."); input("\nEnter..."); limpiar_pantalla(); return
    if not _cliente_activo(clientes, dni):
        print("✖ Cliente inexistente o inactivo."); input("\nEnter..."); limpiar_pantalla(); return
    if _slot_bloqueado(fecha, hora):
        print("✖ El horario está BLOQUEADO para esa fecha."); input("\nEnter..."); limpiar_pantalla(); return
    if _existe_turno_en_slot(fecha, hora):
        print("✖ El horario ya está OCUPADO."); input("\nEnter..."); limpiar_pantalla(); return

    t = {"id": next_turno_id(), "dni": dni, "fecha": fecha, "hora": hora, "estado": "Ocupado"}
    turnos.append(t)
    print("✔ Turno registrado.")
    # confirmar_turno(t, clientes[dni])
    input("\nEnter para continuar..."); limpiar_pantalla()

def listar_turnos(turnos):
    if len(turnos) == 0:
        print("No hay turnos registrados.")
        input("\nPresione Enter para continuar...")
        limpiar_pantalla()
        return
     
    for turno in turnos:
        print(f"DNI: {turno['cliente_dni']} - Fecha: {turno['fecha']} - Hora: {turno['hora']} - Tipo: {turno['tipo']} - Estado: {turno['estado']}")
    input("\nPresione Enter para continuar...")
    limpiar_pantalla()