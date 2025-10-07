from utils import limpiar_pantalla


def alta_cliente(clientes, dni, nombre, apellido, email, telefono):
    clientes.append({
        "dni": dni, "nombre": nombre.strip(), "apellido": apellido.strip(),
        "email": email.strip(), "telefono": telefono.strip()
    })
    print(("✔ Cliente registrado"))
    input("\nPresione Enter para continuar...")
    limpiar_pantalla()

def mostrar_cliente(cliente):
    print(f"DNI: {cliente['dni']} | {cliente['nombre']} {cliente['apellido']} | Email: {cliente['email']} | Tel: {cliente['telefono']}")

def listar_clientes(clientes):
    if len(clientes) == 0:
        print("No hay clientes registrados.")
        input("\nPresione Enter para continuar...")
        limpiar_pantalla()
        return
    
    for cliente in clientes:
        mostrar_cliente(cliente)
    input("\nPresione Enter para continuar...")
    limpiar_pantalla()


def modificar_cliente(clientes):
    def mostrar_atributos():
        print("Modificar:")
        print("1- DNI")
        print("2- Nombre")
        print("3- Apellido")
        print("4- Email")
        print("5- Teléfono")
        print("6- Volver atras")
        opcion = int(input("Ingrese el dato a modificar: "))
        return opcion

    if len(clientes)==0:
        print("No hay clientes registrados para modificar.")
        input("Presione Enter para continuar...")
        limpiar_pantalla()
        return
    else:
        flag = True
        while flag:
            listar_clientes(clientes)
            opcion = input("Ingrese el DNI del cliente a modificar: ")
            for cliente in clientes:
                if (cliente.get("dni")==opcion):
                    opcion = mostrar_atributos()
                    if opcion == 1:
                        nuevoDato = input("Ingrese el DNI:")
                        cliente["dni"] = nuevoDato
                    elif opcion == 2:
                        nuevoDato = input("Ingrese el nombre: ")
                        cliente["nombre"] = nuevoDato
                    elif opcion == 3:
                        nuevoDato = input("Ingrese el apellido: ")
                        cliente["apellido"] = nuevoDato
                    elif opcion == 4:
                        nuevoDato = input("Ingrese el email: ")
                        cliente["email"] = nuevoDato
                    elif opcion == 5:
                        nuevoDato = input("Ingrese el telefono: ")
                        cliente["telefono"] = nuevoDato
                    elif opcion == 6:
                        print("Modificación cancelada.")
                        input("Presione Enter para continuar...")
                        limpiar_pantalla()
                        flag = False
                    
                    if 1<= opcion <= 5:
                        print(f"CLIENTE ACTUALIZADO ✔ - Datos actuales:")
                        mostrar_cliente(cliente)
                        input("Presione Enter para continuar...")
                        limpiar_pantalla()
                        flag = False


