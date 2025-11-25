from utils import limpiar_pantalla, validar_dni, validar_fecha, validarEmail, validarTextoAlfabetico, validarTelefono, validar_hora
from clientes import alta_cliente, listar_clientes, modificar_cliente, baja_logica_cliente, baja_fisica_cliente
from turnos import alta_turno, eliminar_turno_por_id, listar_turnos, listar_por_fecha, desbloquear_slot, listar_por_dni, modificar_turno, bloquear_slot
from storage import log, ver_log

# MUESTRA EL MENSAJE DE BIENVENIDA INICIAL
def mostrar_bienvenida():
    print(
        "\n"
        "┌──────────────────────────────────────────────────┐\n"
        "│     === BIENVENIDO AL GESTOR DE TURNOS ===       │\n"
        "└──────────────────────────────────────────────────┘"
    )
    input("Presione Enter para continuar...")
    limpiar_pantalla()


# MENU PRINCIPAL DEL SISTEMA
def menu_ppal():
    print(
        "\n"
        "┌──────────────────────────────────────────────────┐\n"
        "│            === Gestor de Turnos ===              │\n"
        "│ Menu Principal                                   │\n"
        "│ 1) Clientes                                      │\n"
        "│ 2) Turnos                                        │\n"
        "│ 3) Notificaciones (log)                          │\n"
        "│ 0) Salir                                         │\n"
        "└──────────────────────────────────────────────────┘"
    )


# MENU DE OPCIONES PARA CLIENTES
def menu_clientes():
    print(
        "\n--- CLIENTES ---\n"
        "1) Alta\n"
        "2) Listado (todos)\n"
        "3) Listado (solo activos)\n"
        "4) Modificar un Cliente\n"
        "5) Baja logica\n"
        "6) Baja fisica\n"
        "0) Volver\n"
    )


# MENU DE OPCIONES PARA TURNOS
def menu_turnos():
    print(
        "\n--- TURNOS ---\n"
        "1) Nuevo turno\n"
        "2) Listado general de Turnos\n"
        "3) Listar turnos por DNI\n"
        "4) Listar turnos por fecha\n"
        "5) Modificar un turno\n"
        "6) Eliminar un turno\n"
        "7) Bloquear slot de tiempo (fecha/hora)\n"
        "8) Desbloquear slot de tiempo (fecha/hora)\n"
        "0) Volver\n"
    )


# FUNCION PRINCIPAL DEL PROGRAMA (BUCLE RUN LOOP)
def run_loop():

    mostrar_bienvenida()
    op = ""

    while op != "0":

        esValido = True  # -> Control de submenus
        menu_ppal()
        op = input("Opcion: ").strip()

        # ---------------- CLIENTES ----------------
        if op == "1":

            limpiar_pantalla()

            while esValido:
                menu_clientes()
                opc = input("Opcion clientes: ").strip()
                
                # Alta de cliente nuevo
                if opc == "1":
                    
                    cargaCliente = True
                    while cargaCliente:

                            dni = input("Ingrese su DNI: ").lower().strip()  
                            while not validar_dni(dni, False):
                                input("\nPresione Enter para continuar...")
                                limpiar_pantalla()
                                dni = input("Ingrese su DNI: ").lower().strip()

                            nombre = input("Ingrese su Nombre: ").lower().strip()
                            while not validarTextoAlfabetico(nombre):
                                input("\nPresione Enter para continuar...")
                                limpiar_pantalla()
                                nombre = input("Ingrese su Nombre: ").lower().strip()

                            apellido = input("Ingrese su Apellido: ").lower().strip()
                            while not validarTextoAlfabetico(apellido):
                                input("\nPresione Enter para continuar...")
                                limpiar_pantalla()
                                apellido = input("Ingrese su Apellido: ").lower().strip()
                            
                            email = input("Ingrese su Email: ").lower().strip()
                            while not validarEmail(email, True):
                                input("\nPresione Enter para continuar...")
                                limpiar_pantalla()
                                email = input("Ingrese su Email: ").lower().strip()

                            telefono = input("Ingrese su Telefono {Opcional}: ").strip()
                            while not validarTelefono(telefono):
                                print("Telefono Invalido.")
                                input("\nPresione Enter para continuar...")
                                limpiar_pantalla()
                                telefono = input("Ingrese su Telefono {Opcional}: ").strip()

                            cargaCliente = False     
                            alta_cliente(dni, nombre, apellido, email, telefono)

                # Listado de todos los clientes
                elif opc == "2":
                    listar_clientes(False)

                # Listado solo de clientes activos
                elif opc == "3":
                    listar_clientes(True)

                # Modificar datos de cliente existente
                elif opc == "4":
                    dni = input("Ingrese DNI a modificar: ").strip()

                    while not validar_dni(dni, True):
                        input("\nPresione Enter para continuar...")
                        limpiar_pantalla()
                        dni = input("Ingrese DNI a modificar: ").strip()

                    modificar_cliente(dni)
                

                # Baja logica (desactiva cliente sin borrarlo)
                elif opc == "5":
                    dni = input("DNI para baja logica: ").strip()

                    while not validar_dni(dni, True):
                        input("\nPresione Enter para continuar...")
                        limpiar_pantalla()
                        dni = input("DNI para baja logica: ").strip()

                    baja_logica_cliente(dni)

                # Baja fisica (elimina cliente completamente)
                elif opc == "6":
                    dni = input("DNI para baja fisica: ").strip()

                    while not validar_dni(dni, True):
                        input("\nPresione Enter para continuar...")
                        limpiar_pantalla()
                        dni = input("DNI para baja fisica: ").strip()

                    baja_fisica_cliente(dni)

                # Volver al menu principal
                elif opc == "0":
                    esValido = False
                    limpiar_pantalla()
                    
                else:
                    print("Opcion invalida.")

        # ---------------- TURNOS ----------------
        elif op == "2":

            limpiar_pantalla()

            while esValido:
                menu_turnos()
                opc = input("Opcion turnos: ").strip()

                # Crear nuevo turno
                if opc == "1":  
                    dni = input("DNI cliente: ").strip()

                    while not validar_dni(dni, True):
                        input("\nPresione Enter para continuar...")
                        limpiar_pantalla()
                        dni = input("DNI cliente: ").strip()

                    fecha = input("Fecha (YYYY-MM-DD): ").strip()
                    while not validar_fecha(fecha):
                        input("\nPresione Enter para continuar...")
                        limpiar_pantalla()
                        fecha = input("Fecha (YYYY-MM-DD): ").strip()

                    hora = input("Hora (HH:mm): ").strip()
                    while not validar_hora(hora):
                        input("\nPresione Enter para continuar...")
                        limpiar_pantalla()
                        hora = input("Hora (HH:mm): ").strip()

                    alta_turno(dni, fecha, hora)

                # Listar todos los turnos
                elif opc == "2":
                    listar_turnos()

                # Listar turnos por DNI
                elif opc == "3":
                    dni = input("DNI: ").strip()

                    while not validar_dni(dni, True):
                        input("\nPresione Enter para continuar...")
                        limpiar_pantalla()
                        dni = input("DNI: ").strip()

                    listar_por_dni(dni)

                # Listar turnos por fecha
                elif opc == "4":
                    fecha = input("Fecha (YYYY-MM-DD): ").strip()
                    
                    while not validar_fecha(fecha):
                        input("\nPresione Enter para continuar...")
                        limpiar_pantalla()
                        fecha = input("Fecha (YYYY-MM-DD): ").strip()

                    listar_por_fecha(fecha)

                # Modificar un turno existente
                elif opc == "5":
                    try:
                        tid = int(input("ID de turno a modificar: ").strip())
                    except ValueError:
                        print("✖ ID invalido. Debe ser un número.")
                        log("ERRO", "ValueError", "Dato inválido en ID de Turno")
                        input("Enter...")
                        limpiar_pantalla()
                        continue

                    print(f"\nModificando Turno ID: {tid} (Deje VACÍO para no cambiar)")

                    # ----------------- DNI -----------------
                    nuevo_dni = input("Nuevo DNI (vacío=no cambia): ").strip()
                    if nuevo_dni == "":
                        nuevo_dni = None
                    else:
                        while not validar_dni(nuevo_dni, True):
                            input("\nPresione Enter para continuar...")
                            limpiar_pantalla()
                            nuevo_dni = input("Nuevo DNI (vacío=no cambia): ").strip()
                            if nuevo_dni == "":
                                nuevo_dni = None
                
                    # ----------------- FECHA -----------------
                    nueva_fecha = input("Nueva fecha (YYYY-MM-DD, vacío=no): ").strip()
                    if nueva_fecha == "":
                        nueva_fecha = None
                    else:
                        while not validar_fecha(nueva_fecha):
                            input("\nPresione Enter para continuar...")
                            limpiar_pantalla()
                            nueva_fecha = input("Nueva fecha (YYYY-MM-DD, vacío=no): ").strip()
                            if nueva_fecha == "":
                                nueva_fecha = None
                  
                    # ----------------- HORA -----------------
                    nueva_hora = input("Nueva hora (HH:mm, vacío=no): ").strip()
                    if nueva_hora == "":
                        nueva_hora = None
                    else:
                        while not validar_hora(nueva_hora):
                            input("\nPresione Enter para continuar...")
                            limpiar_pantalla()
                            nueva_hora = input("Nueva hora (HH:mm, vacío=no): ").strip()
                            if nueva_hora == "":
                                nueva_hora = None

                    # Llamada final
                    modificar_turno(tid, nuevo_dni, nueva_fecha, nueva_hora)

                # Eliminar un turno existente
                elif opc == "6":
                    try:
                        tid = int(input("ID de turno a eliminar: ").strip())
                    except ValueError:
                        print("ID invalido.")
                        log("ERRO", "ValueError", "Dato Invalido en ID de Turno")
                        input("\nPresione Enter para continuar...")
                        limpiar_pantalla()
                        continue
                    eliminar_turno_por_id(tid)

                # Bloquear un horario especifico
                elif opc == "7":
                    fecha = input("Fecha (YYYY-MM-DD): ").strip()
                    
                    while not validar_fecha(fecha):
                        input("\nPresione Enter para continuar...")
                        limpiar_pantalla()
                        fecha = input("Fecha (YYYY-MM-DD): ").strip()

                    hora = input("Hora (HH:mm): ").strip()

                    while not validar_hora(hora):
                        input("\nPresione Enter para continuar...")
                        limpiar_pantalla()
                        hora = input("Hora (HH:mm): ").strip()

                    bloquear_slot(fecha, hora)

                # Desbloquear un horario especifico
                elif opc == "8":
                    fecha = input("Fecha (YYYY-MM-DD): ").strip()
                    
                    while not validar_fecha(fecha):
                        input("\nPresione Enter para continuar...")
                        limpiar_pantalla()
                        fecha = input("Fecha (YYYY-MM-DD): ").strip()

                    hora = input("Hora (HH:mm): ").strip()

                    while not validar_hora(hora):
                        input("\nPresione Enter para continuar...")
                        limpiar_pantalla()
                        hora = input("Hora (HH:mm): ").strip()

                    desbloquear_slot(fecha, hora)
                
                 # Volver al menu principal
                elif opc == "0":
                    esValido = False
                    limpiar_pantalla()

                else:
                    print("Opcion invalida.")

        # ---------------- LOG ----------------
        # Mostrar registro de logs o notificaciones (a implementar)
        elif op == "3":
            limpiar_pantalla()

            ver_log()
            input("\nEnter para continuar...")
            limpiar_pantalla()

        # ---------------- SALIR ----------------
        elif op == "0":
            limpiar_pantalla()
            print("\nChau!")
        
        else:
            print("Opcion invalida.")
            input("\nEnter para continuar...")
            limpiar_pantalla()
