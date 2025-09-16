def alta_turno(turnos, clientes, cliente_dni, fecha, hora, tipo):
    turnos.append({
        "cliente_dni": cliente_dni, "fecha": fecha, "hora": hora,
        "tipo": tipo.strip(), "estado": "Activo"
    })
    print(("✔ Turno registrado"))

def listar_turnos(turnos):
    return turnos
