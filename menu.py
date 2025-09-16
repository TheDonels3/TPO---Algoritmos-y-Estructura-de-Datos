from clientes import alta_cliente, listar_clientes
from turnos import alta_turno, listar_turnos

def mostrar_menu():
    print("\n=== Gestor de Turnos ===")
    print("1) Alta Cliente")
    print("2) Listado de Clientes")
    print("3) Alta Turno")
    print("4) Listado de Turnos")
    print("0) Salir")

def run_loop():
    clientes = []
    turnos = []
    while True:
        mostrar_menu()
        opcion = input("Opción: ")

        if opcion == "1":
            print("\n--- Alta de Cliente ---")
            dni = input("DNI: ")
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            email = input("Email: ")
            tel = input("Teléfono: ")
            alta_cliente(clientes, dni, nombre, apellido, email, tel)
    
        elif opcion == "2":
            print("\n--- Listado de Clientes ---")
            listar_clientes(clientes)

        elif opcion == "3":
            print("\n--- Alta de Turno ---")
            dni = input("DNI del cliente: ")
            fecha = input("Fecha: ")
            hora = input("Hora: ")
            tipo = input("Tipo de turno: ")
            alta_turno(turnos,clientes,dni,fecha,hora,tipo)

        elif opcion == "4":
            print("\n--- Listado de Turnos ---")
            listar_turnos(turnos)

        elif opcion == "0":
            print("¡Chau!")
            break

        else:
            print("Opción inválida")