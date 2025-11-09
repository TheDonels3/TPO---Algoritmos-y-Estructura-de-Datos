from utils import limpiar_pantalla
from clientes import alta_cliente, listar_clientes, modificar_cliente, baja_logica_cliente, baja_fisica_cliente
from turnos import alta_turno, listar_turnos
from storage import turnos


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
        "│                                                  │\n"
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
        "4) Modificacion\n"
        "5) Baja logica\n"
        "6) Baja fisica\n"
        "0) Volver\n"
    )


# MENU DE OPCIONES PARA TURNOS
def menu_turnos():
    print(
        "\n--- TURNOS ---\n"
        "1) Nuevo turno\n"
        "2) Listado general\n"
        "3) Listado por DNI\n"
        "4) Listado por fecha\n"
        "5) Modificar (cliente/fecha/hora)\n"
        "6) Eliminar (desde dia actual)\n"
        "7) Bloquear slot (fecha/hora)\n"
        "8) Desbloquear slot\n"
        "0) Volver\n"
    )


# FUNCION PRINCIPAL DEL PROGRAMA (BUCLE RUN LOOP)
def run_loop():

    mostrar_bienvenida()

    while True:

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
                    dni = input("DNI: ").strip()
                    nombre = input("Nombre: ").strip()
                    apellido = input("Apellido: ").strip()
                    email = input("Email (opcional): ").strip()
                    tel = input("Telefono (opcional): ").strip()
                    alta_cliente(dni, nombre, apellido, email, tel)

                # Listado de todos los clientes
                elif opc == "2":
                    listar_clientes(solo_activos=False)

                # Listado solo de clientes activos
                elif opc == "3":
                    listar_clientes(solo_activos=True)

                # Modificar datos de cliente existente
                elif opc == "4":
                    dni = input("DNI a modificar: ").strip()
                    modificar_cliente(dni)

                # Baja logica (desactiva cliente sin borrarlo)
                elif opc == "5":
                    dni = input("DNI para baja logica: ").strip()
                    baja_logica_cliente(dni)

                # Baja fisica (elimina cliente completamente)
                elif opc == "6":
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
                    dni = input("DNI cliente: ").strip()
                    fecha = input("Fecha (YYYY-MM-DD): ").strip()
                    hora = input("Hora (HH:mm): ").strip()
                    alta_turno(dni, fecha, hora)

                # Listar todos los turnos
                elif opc == "2":
                    listar_turnos(turnos)

                # Listar turnos por DNI (a implementar)
                elif opc == "3":

                    dni = input("DNI: ").strip()

                # Listar turnos por fecha (a implementar)
                elif opc == "4":
                    fecha = input("Fecha (YYYY-MM-DD): ").strip()

                # Modificar un turno existente
                elif opc == "5":
                    try:
                        tid = int(input("ID de turno: ").strip())
                    except ValueError:
                        print("ID invalido.")
                        input("Enter...")
                        limpiar_pantalla()
                        continue

                    nuevo_dni = input("Nuevo DNI (vacio=no cambia): ").strip() or None
                    nueva_fecha = input("Nueva fecha (YYYY-MM-DD, vacio=no): ").strip() or None
                    nueva_hora = input("Nueva hora (HH:mm, vacio=no): ").strip() or None

                 # Eliminar un turno existente
                elif opc == "6":
                    try:
                        tid = int(input("ID de turno a eliminar: ").strip())

                    except ValueError:
                        print("ID invalido.")
                        input("Enter...")
                        limpiar_pantalla()
                        continue
                
                # Bloquear un horario especifico
                elif opc == "7":
                    fecha = input("Fecha (YYYY-MM-DD): ").strip()
                    hora = input("Hora (HH:mm): ").strip()

                # Desbloquear un horario especifico
                elif opc == "8":
                    fecha = input("Fecha (YYYY-MM-DD): ").strip()
                    hora = input("Hora (HH:mm): ").strip()
                
                 # Volver al menu principal
                elif opc == "0":
                    esValido = False
                    limpiar_pantalla()

                else:
                    print("Opcion invalida.")

        # ---------------- LOG ----------------
        # Mostrar registro de logs o notificaciones (a implementar)
        elif op == "3":
            ver_log()
            input("\nEnter para continuar...")
            limpiar_pantalla()

        # ---------------- SALIR ----------------
        elif op == "0":
            print("\nChau!")
            break
        
        else:
            print("Opcion invalida.")
