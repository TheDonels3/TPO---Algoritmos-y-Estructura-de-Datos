from utils import limpiar_pantalla


def alta_cliente(clientes, dni, nombre, apellido, email, telefono):
    clientes.append({
        "dni": dni, "nombre": nombre.strip(), "apellido": apellido.strip(),
        "email": email.strip(), "telefono": telefono.strip()
    })
    print(("✔ Cliente registrado"))
    input("\nPresione Enter para continuar...")
    limpiar_pantalla()


def listar_clientes(clientes):
    if len(clientes) == 0:
        print("No hay clientes registrados.")
        input("\nPresione Enter para continuar...")
        limpiar_pantalla()
        return
    
    for cliente in clientes:
        print(f"DNI: {cliente['dni']} | {cliente['nombre']} {cliente['apellido']} | Email: {cliente['email']} | Tel: {cliente['telefono']}")
    input("\nPresione Enter para continuar...")
    limpiar_pantalla()
