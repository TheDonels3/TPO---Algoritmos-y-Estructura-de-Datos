


from utils import limpiar_pantalla
from clientes import alta_cliente, listar_clientes, modificar_cliente, baja_logica_cliente, baja_fisica_cliente
from turnos import alta_turno, listar_turnos
from storage import clientes

# from notificaciones import ver_log
# import demo_data  # carga data demo

def mostrar_bienvenida():
    print(
        "\n"
        "┌──────────────────────────────────────────────────┐\n"
        "│     === BIENVENIDO AL GESTOR DE TURNOS ===       │\n"
        "└──────────────────────────────────────────────────┘"
    )
    input("Presione Enter para continuar...")
    limpiar_pantalla()

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

def menu_clientes():
    print(
        "\n--- CLIENTES ---\n"
        "1) Alta\n"
        "2) Listado (todos)\n"
        "3) Listado (solo activos)\n"
        "4) Modificación\n"
        "5) Baja lógica\n"
        "6) Baja física\n"
        "0) Volver\n"
    )

def menu_turnos():
    print(
        "\n--- TURNOS ---\n"
        "1) Nuevo turno\n"
        "2) Listado general\n"
        "3) Listado por DNI\n"
        "4) Listado por fecha\n"
        "5) Modificar (cliente/fecha/hora)\n"
        "6) Eliminar (desde día actual)\n"
        "7) Bloquear slot (fecha/hora)\n"
        "8) Desbloquear slot\n"
        "0) Volver\n"
    )

def run_loop():
    mostrar_bienvenida()
    while True:
        menu_ppal()
        op = input("Opción: ").strip()
        if op == "1":
            while True:
                menu_clientes()
                opc = input("Opción clientes: ").strip()
                if opc == "1":
                    dni = input("DNI: ").strip()
                    nombre = input("Nombre: ").strip()
                    apellido = input("Apellido: ").strip()
                    email = input("Email (opcional): ").strip()
                    tel = input("Teléfono (opcional): ").strip()
                    alta_cliente(clientes, dni, nombre, apellido, email, tel)
                elif opc == "2":
                    listar_clientes(clientes, solo_activos=False)
                elif opc == "3":
                    listar_clientes(clientes, solo_activos=True)
                elif opc == "4":
                    dni = input("DNI a modificar: ").strip()
                    modificar_cliente(clientes, dni)
                elif opc == "5":
                    dni = input("DNI para baja lógica: ").strip()
                    baja_logica_cliente(clientes, dni)
                elif opc == "6":
                    dni = input("DNI para baja física: ").strip()
                    baja_fisica_cliente(clientes, dni)
                elif opc == "0":
                    limpiar_pantalla(); break
                else:
                    print("Opción inválida.")
        elif op == "2":
            while True:
                menu_turnos()
                opc = input("Opción turnos: ").strip()
                if opc == "1":
                    dni = input("DNI cliente: ").strip()
                    fecha = input("Fecha (YYYY-MM-DD): ").strip()
                    hora = input("Hora (HH:mm): ").strip()
                    alta_turno(clientes, dni, fecha, hora)
                elif opc == "2":
                    listar_turnos()
                elif opc == "3":
                    dni = input("DNI: ").strip()
                    # listar_por_cliente(dni)
                elif opc == "4":
                    fecha = input("Fecha (YYYY-MM-DD): ").strip()
                    # listar_por_fecha(fecha)
                elif opc == "5":
                    try:
                        tid = int(input("ID de turno: ").strip())
                    except ValueError:
                        print("ID inválido."); input("Enter..."); limpiar_pantalla(); continue
                    nuevo_dni = input("Nuevo DNI (vacío=no cambia): ").strip() or None
                    nueva_fecha = input("Nueva fecha (YYYY-MM-DD, vacío=no): ").strip() or None
                    nueva_hora = input("Nueva hora (HH:mm, vacío=no): ").strip() or None
                    # modificar_turno(clientes, tid, nuevo_dni, nueva_fecha, nueva_hora)
                elif opc == "6":
                    try:
                        tid = int(input("ID de turno a eliminar: ").strip())
                    except ValueError:
                        print("ID inválido."); input("Enter..."); limpiar_pantalla(); continue
                    # eliminar_turno(tid)
                elif opc == "7":
                    fecha = input("Fecha (YYYY-MM-DD): ").strip()
                    hora = input("Hora (HH:mm): ").strip()
                    # bloquear_slot(fecha, hora)
                elif opc == "8":
                    fecha = input("Fecha (YYYY-MM-DD): ").strip()
                    hora = input("Hora (HH:mm): ").strip()
                    # desbloquear_slot(fecha, hora)
                elif opc == "0":
                    limpiar_pantalla(); break
                else:
                    print("Opción inválida.")
        elif op == "3":
            ver_log(); input("\nEnter para continuar..."); limpiar_pantalla()
        elif op == "0":
            print("\n¡Chau!"); break
        else:
            print("Opción inválida.")
