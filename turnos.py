from utils import limpiar_pantalla


def alta_turno(turnos, cliente_dni, fecha, hora, tipo):
    turnos.append({
        "cliente_dni": cliente_dni, "fecha": fecha, "hora": hora,
        "tipo": tipo.strip(), "estado": "Activo"
    })
    print(("✔ Turno registrado"))
    input("\nPresione Enter para continuar...")
    limpiar_pantalla()

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