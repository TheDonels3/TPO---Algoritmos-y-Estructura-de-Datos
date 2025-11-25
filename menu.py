from utils import limpiar_pantalla
from storage import ver_log
from clientes import validar_alta_cliente,validar_modificacion_cliente,listar_clientes, baja_logica_cliente, baja_fisica_cliente
from turnos import validar_alta_turno, validar_modificacion_turno, eliminar_turno_por_id, listar_turnos, listar_por_fecha, desbloquear_slot, listar_por_dni, modificar_turno, bloquear_slot

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

        esValido = True  # Control de submenus
        menu_ppal()
        op = input("Opcion: ").strip()

        # ---------------- CLIENTES ----------------
        if op == "1":

            while esValido:
                menu_clientes()
                opc = input("Opcion clientes: ").strip()
                
                # Alta de cliente nuevo
                if opc == "1":
                    limpiar_pantalla()
                    print(
                        "\n"
                        "┌──────────────────────────────────────────────────┐\n"
                        "│         === ALTA DE NUEVO CLIENTE ===        │\n"
                        "└──────────────────────────────────────────────────┘"
                    )
                    validar_alta_cliente()

                # Listado de todos los clientes
                elif opc == "2":
                    limpiar_pantalla()
                    print(
                        "\n"
                        "┌──────────────────────────────────────────────────┐\n"
                        "│       === LISTADO DE TODOS LOS CLIENTES ===  │\n"
                        "└──────────────────────────────────────────────────┘\n"
                    )
                    listar_clientes(solo_activos=False)

                # Listado solo de clientes activos
                elif opc == "3":
                    limpiar_pantalla()
                    print(
                        "\n"
                        "┌──────────────────────────────────────────────────┐\n"
                        "│     === LISTADO DE CLIENTES ACTIVOS ===     │\n"
                        "└──────────────────────────────────────────────────┘\n"
                    )
                    listar_clientes(solo_activos=True)

                # Modificar datos de cliente existente
                elif opc == "4":
                    limpiar_pantalla()
                    print(
                        "\n"
                        "┌──────────────────────────────────────────────────┐\n"
                        "│         === MODIFICAR CLIENTE ===            │\n"
                        "└──────────────────────────────────────────────────┘"
                    )
                    validar_modificacion_cliente()

                # Baja logica (desactiva cliente sin borrarlo)
                elif opc == "5":
                    limpiar_pantalla()
                    print(
                        "\n"
                        "┌──────────────────────────────────────────────────┐\n"
                        "│        === BAJA LÓGICA DE CLIENTE ===       │\n"
                        "└──────────────────────────────────────────────────┘"
                    )
                    dni = input("DNI para baja logica: ").strip()
                    baja_logica_cliente(dni)

                # Baja fisica (elimina cliente completamente)
                elif opc == "6":
                    limpiar_pantalla()
                    print(
                        "\n"
                        "┌──────────────────────────────────────────────────┐\n"
                        "│        === BAJA FÍSICA DE CLIENTE ===       │\n"
                        "└──────────────────────────────────────────────────┘"
                    )
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
            while esValido:
                menu_turnos()
                opc = input("Opcion turnos: ").strip()

                # Crear nuevo turno
                if opc == "1":
                    limpiar_pantalla()
                    print(
                        "\n"
                        "┌──────────────────────────────────────────────────┐\n"
                        "│           === CREAR NUEVO TURNO ===           │\n"
                        "└──────────────────────────────────────────────────┘"
                    )
                    validar_alta_turno()

                # Listar todos los turnos
                elif opc == "2":
                    limpiar_pantalla()
                    print(
                        "\n"
                        "┌──────────────────────────────────────────────────┐\n"
                        "│        === LISTADO GENERAL DE TURNOS ===    │\n"
                        "└──────────────────────────────────────────────────┘\n"
                    )
                    listar_turnos()

                # Listar turnos por DNI
                elif opc == "3":
                    limpiar_pantalla()
                    print(
                        "\n"
                        "┌──────────────────────────────────────────────────┐\n"
                        "│          === TURNOS POR CLIENTE ===          │\n"
                        "└──────────────────────────────────────────────────┘"
                    )
                    dni = input("DNI: ").strip()
                    listar_por_dni(dni)

                # Listar turnos por fecha
                elif opc == "4":
                    limpiar_pantalla()
                    print(
                        "\n"
                        "┌──────────────────────────────────────────────────┐\n"
                        "│           === TURNOS POR FECHA ===           │\n"
                        "└──────────────────────────────────────────────────┘"
                    )
                    fecha = input("Fecha (YYYY-MM-DD): ").strip()
                    listar_por_fecha(fecha)

                # Modificar un turno existente
                elif opc == "5":
                    limpiar_pantalla()
                    print(
                        "\n"
                        "┌──────────────────────────────────────────────────┐\n"
                        "│            === MODIFICAR TURNO ===            │\n"
                        "└──────────────────────────────────────────────────┘"
                    )
                    validar_modificacion_turno()

                # Eliminar un turno existente
                elif opc == "6":
                    limpiar_pantalla()
                    print(
                        "\n"
                        "┌──────────────────────────────────────────────────┐\n"
                        "│            === ELIMINAR TURNO ===             │\n"
                        "└──────────────────────────────────────────────────┘"
                    )
                    try:
                        tid = int(input("ID de turno a eliminar: ").strip())
                    except ValueError:
                        print("ID invalido.")
                        input("\nPresione Enter para continuar...")
                        limpiar_pantalla()
                        continue
                    eliminar_turno_por_id(tid)

                # Bloquear un horario especifico
                elif opc == "7":
                    limpiar_pantalla()
                    print(
                        "\n"
                        "┌──────────────────────────────────────────────────┐\n"
                        "│          === BLOQUEAR HORARIO ===           │\n"
                        "└──────────────────────────────────────────────────┘"
                    )
                    fecha = input("Fecha (YYYY-MM-DD): ").strip()
                    hora = input("Hora (HH:mm): ").strip()
                    bloquear_slot(fecha, hora)

                # Desbloquear un horario especifico
                elif opc == "8":
                    limpiar_pantalla()
                    print(
                        "\n"
                        "┌──────────────────────────────────────────────────┐\n"
                        "│         === DESBLOQUEAR HORARIO ===         │\n"
                        "└──────────────────────────────────────────────────┘"
                    )
                    fecha = input("Fecha (YYYY-MM-DD): ").strip()
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
            print(
                        "\n"
                        "┌──────────────────────────────────────────────────┐\n"
                        "│           === REGISTRO DE LOGS ===           │\n"
                        "└──────────────────────────────────────────────────┘"
                    )
            ver_log()
            input("\nEnter para continuar...")
            limpiar_pantalla()

        # ---------------- SALIR ----------------
        elif op == "0":
            print("\nChau!")
        
        else:
            print("Opcion invalida.")
