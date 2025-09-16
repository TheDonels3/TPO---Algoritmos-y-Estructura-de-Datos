def alta_cliente(clientes, dni, nombre, apellido, email, telefono):
    clientes.append({
        "dni": dni, "nombre": nombre.strip(), "apellido": apellido.strip(),
        "email": email.strip(), "telefono": telefono.strip()
    })
    print(("✔ Cliente registrado"))


def listar_clientes(clientes):
    if len(clientes) == 0:
        print("No hay clientes registrados.")
        return
    
    for cliente in clientes:
        print(f"DNI: {cliente['dni']} | {cliente['nombre']} {cliente['apellido']} | Email: {cliente['email']} | Tel: {cliente['telefono']}")

