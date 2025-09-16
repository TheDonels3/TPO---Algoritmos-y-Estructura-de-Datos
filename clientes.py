def alta_cliente(clientes, dni, nombre, apellido, email, telefono):
    clientes.append({
        "dni": dni, "nombre": nombre.strip(), "apellido": apellido.strip(),
        "email": email.strip(), "telefono": telefono.strip()
    })
    print(("✔ Cliente registrado"))


def listar_clientes(clientes):
    for cliente in clientes:
        print(f"{cliente['nombre']} {cliente['apellido']} - DNI: {cliente['dni']}")

