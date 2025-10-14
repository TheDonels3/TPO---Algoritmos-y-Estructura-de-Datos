# from utils import limpiar_pantalla


# def alta_cliente(clientes, dni, nombre, apellido, email, telefono):
#     clientes.append({
#         "dni": dni, "nombre": nombre.strip(), "apellido": apellido.strip(),
#         "email": email.strip(), "telefono": telefono.strip()
#     })
#     print(("✔ Cliente registrado"))
#     input("\nPresione Enter para continuar...")
#     limpiar_pantalla()

# def mostrar_cliente(cliente):
#     print(f"DNI: {cliente['dni']} | {cliente['nombre']} {cliente['apellido']} | Email: {cliente['email']} | Tel: {cliente['telefono']}")

# def listar_clientes(clientes):
#     if len(clientes) == 0:
#         print("No hay clientes registrados.")
#         input("\nPresione Enter para continuar...")
#         limpiar_pantalla()
#         return
    
#     for cliente in clientes:
#         mostrar_cliente(cliente)
#     input("\nPresione Enter para continuar...")
#     limpiar_pantalla()


# def modificar_cliente(clientes):
#     def mostrar_atributos():
#         print("Modificar:")
#         print("1- DNI")
#         print("2- Nombre")
#         print("3- Apellido")
#         print("4- Email")
#         print("5- Teléfono")
#         print("6- Volver atras")
#         opcion = int(input("Ingrese el dato a modificar: "))
#         return opcion

#     if len(clientes)==0:
#         print("No hay clientes registrados para modificar.")
#         input("Presione Enter para continuar...")
#         limpiar_pantalla()
#         return
#     else:
#         flag = True
#         while flag:
#             listar_clientes(clientes)
#             opcion = input("Ingrese el DNI del cliente a modificar: ")
#             for cliente in clientes:
#                 if (cliente.get("dni")==opcion):
#                     opcion = mostrar_atributos()
#                     if opcion == 1:
#                         nuevoDato = input("Ingrese el DNI:")
#                         cliente["dni"] = nuevoDato
#                     elif opcion == 2:
#                         nuevoDato = input("Ingrese el nombre: ")
#                         cliente["nombre"] = nuevoDato
#                     elif opcion == 3:
#                         nuevoDato = input("Ingrese el apellido: ")
#                         cliente["apellido"] = nuevoDato
#                     elif opcion == 4:
#                         nuevoDato = input("Ingrese el email: ")
#                         cliente["email"] = nuevoDato
#                     elif opcion == 5:
#                         nuevoDato = input("Ingrese el telefono: ")
#                         cliente["telefono"] = nuevoDato
#                     elif opcion == 6:
#                         print("Modificación cancelada.")
#                         input("Presione Enter para continuar...")
#                         limpiar_pantalla()
#                         flag = False
                    
#                     if 1<= opcion <= 5:
#                         print(f"CLIENTE ACTUALIZADO ✔ - Datos actuales:")
#                         mostrar_cliente(cliente)
#                         input("Presione Enter para continuar...")
#                         limpiar_pantalla()
#                         flag = False



from utils import limpiar_pantalla, validar_dni

def alta_cliente(clientes, dni, nombre, apellido, email, telefono):
    if not validar_dni(dni):
        print("✖ DNI inválido. Deben ser 7 u 8 dígitos.")
        input("\nEnter para continuar..."); limpiar_pantalla(); return
    if dni in clientes:
        print("✖ Ya existe un cliente con ese DNI.")
        input("\nEnter para continuar..."); limpiar_pantalla(); return
    clientes[dni] = {
        "dni": dni,
        "nombre": nombre.strip(),
        "apellido": apellido.strip(),
        "email": (email or "").strip(),
        "telefono": (telefono or "").strip(),
        "activo": True  # baja lógica
    }
    print("✔ Cliente registrado.")
    input("\nEnter para continuar..."); limpiar_pantalla()

def listar_clientes(clientes, solo_activos=False):
    if not clientes:
        print("No hay clientes registrados.")
        input("\nEnter para continuar..."); limpiar_pantalla(); return
    # Listas por comprensión + lambda para ordenar por apellido, nombre
    items = [c for c in clientes.values() if (c["activo"] or not solo_activos)]
    items = sorted(items, key=lambda c: (c["apellido"].lower(), c["nombre"].lower()))
    for c in items:
        estado = "Activo" if c["activo"] else "Inactivo"
        print(f"DNI: {c['dni']} | {c['apellido']}, {c['nombre']} | Email: {c['email']} | Tel: {c['telefono']} | {estado}")
    input("\nEnter para continuar..."); limpiar_pantalla()

def modificar_cliente(clientes, dni):
    c = clientes.get(dni)
    if not c:
        print("✖ No existe un cliente con ese DNI."); input("\nEnter..."); limpiar_pantalla(); return
    print("Dejar vacío para mantener el valor actual.")
    nombre = input(f"Nombre ({c['nombre']}): ").strip() or c['nombre']
    apellido = input(f"Apellido ({c['apellido']}): ").strip() or c['apellido']
    email = input(f"Email ({c['email']}): ").strip() or c['email']
    tel = input(f"Teléfono ({c['telefono']}): ").strip() or c['telefono']
    activo_in = input(f"Activo? (S/N) actual={ 'S' if c['activo'] else 'N' }: ").strip().lower()
    if activo_in in ('s','n'):
        c['activo'] = (activo_in == 's')
    c.update({"nombre":nombre, "apellido":apellido, "email":email, "telefono":tel})
    print("✔ Cliente actualizado.")
    input("\nEnter para continuar..."); limpiar_pantalla()

def baja_logica_cliente(clientes, dni):
    c = clientes.get(dni)
    if not c:
        print("✖ No existe un cliente con ese DNI."); input("\nEnter..."); limpiar_pantalla(); return
    c["activo"] = False
    print("✔ Baja lógica aplicada (cliente inactivo).")
    input("\nEnter para continuar..."); limpiar_pantalla()

def baja_fisica_cliente(clientes, dni):
    if dni in clientes:
        del clientes[dni]
        print("✔ Cliente eliminado físicamente.")
    else:
        print("✖ No existe un cliente con ese DNI.")
    input("\nEnter para continuar..."); limpiar_pantalla()
