from utils import limpiar_pantalla, validar_dni, validarEmail
from storage import guardar_clientes, cargar_clientes


def alta_cliente(dni, nombre, apellido, email, telefono):
    try:
        # Carga los clientes desde el archivo
        clientes = cargar_clientes()

        # Verifica que el DNI sea valido
        if not validar_dni(dni):
            print("✖ DNI invalido. Deben ser 7 u 8 digitos.")
            input("\nEnter para continuar...")
            limpiar_pantalla()
            return
        
        # Verifica si el DNI ya existe
        if dni in clientes:
            print("✖ Ya existe un cliente con ese DNI.")
            input("\nEnter para continuar...")
            limpiar_pantalla()
            return
        
        #Verificar que el Gmail cumpla el formato
        if not validarEmail(email):
            print("✖ EMAIL invalido. Debe ser una dirección de Gmail válida.")
            input("\nEnter para continuar...")
            limpiar_pantalla()
            return

        #Verificar si el GMAIL ya existe
        for c in clientes.values():
            if c.get("email", "").strip().lower() == email:
                print("✖ Ya existe un cliente con ese email Gmail.")
                input("\nEnter para continuar...")
                limpiar_pantalla()
                return

        # Crea un nuevo registro de cliente
        clientes[dni] = {
            "dni": dni,
            "nombre": nombre.strip(),
            "apellido": apellido.strip(),
            "email": email.strip(),
            "telefono": (telefono or "").strip(),
            "activo": True
        }

        # Guarda el nuevo cliente
        guardar_clientes(clientes)
        print("✔ Cliente registrado.")

    except AttributeError:
        print("✖ Error: Valores invalidos proporcionados.")
    except Exception as e:
        print(f"✖ Error inesperado al registrar cliente: {e}")
    finally:
        input("\nEnter para continuar...")
        limpiar_pantalla()


def listar_clientes(solo_activos=False):
    try:
        # Carga los clientes actualizados desde el archivo
        clientes = cargar_clientes()

        if not clientes:
            print("No hay clientes registrados.")
            input("\nEnter para continuar...")
            limpiar_pantalla()
            return
        
        # Filtra solo los activos si corresponde
        items = [c for c in clientes.values() if (c["activo"] or not solo_activos)]
        # Ordena alfabeticamente por apellido y nombre
        items = sorted(items, key=lambda c: (c["apellido"].lower(), c["nombre"].lower()))
        
        # Muestra cada cliente
        for c in items:
            estado = "Activo" if c["activo"] else "Inactivo"
            print(f"DNI: {c['dni']} | {c['apellido']}, {c['nombre']} | Email: {c['email']} | Tel: {c['telefono']} | {estado}")
            
    except KeyError as e:
        print(f"✖ Error: Campo faltante en datos del cliente: {e}")
    except Exception as e:
        print(f"✖ Error al listar clientes: {e}")
    finally:
        input("\nEnter para continuar...")
        limpiar_pantalla()


def modificar_cliente(dni):
    try:
        # Carga los clientes desde el archivo
        clientes = cargar_clientes()
        c = clientes.get(dni)
        
        # Verifica que el cliente exista
        if not c:
            print("✖ No existe un cliente con ese DNI.")
            input("\nEnter...")
            limpiar_pantalla()
            return
            
        # Solicita nuevos datos, dejando vacio para mantener el actual
        print("Dejar vacio para mantener el valor actual.")
        nombre = input(f"Nombre ({c['nombre']}): ").strip() or c['nombre']
        apellido = input(f"Apellido ({c['apellido']}): ").strip() or c['apellido']
        email = input(f"Email ({c['email']}): ").strip() or c['email']
        tel = input(f"Telefono ({c['telefono']}): ").strip() or c['telefono']
        activo_in = input(f"Activo? (S/N) actual={ 'S' if c['activo'] else 'N' }: ").strip().lower()
        
        # Actualiza el estado activo si el usuario lo cambia
        if activo_in in ('s', 'n'):
            c['activo'] = (activo_in == 's')
        
        # Actualiza los demas campos
        c.update({"nombre": nombre, "apellido": apellido, "email": email, "telefono": tel})
        
        # Guarda los cambios
        guardar_clientes(clientes)
        print("✔ Cliente actualizado.")

    except KeyError as e:
        print(f"✖ Error: Campo faltante en cliente: {e}")
    except KeyboardInterrupt:
        print("\n✖ Operacion cancelada por el usuario.")
    except Exception as e:
        print(f"✖ Error al modificar cliente: {e}")
    finally:
        input("\nEnter para continuar...")
        limpiar_pantalla()


def baja_logica_cliente(dni):
    try:
        # Carga los clientes desde el archivo
        clientes = cargar_clientes()
        c = clientes.get(dni)

        # Verifica que el cliente exista
        if not c:
            print("✖ No existe un cliente con ese DNI.")
            input("\nEnter...")
            limpiar_pantalla()
            return
            
        # Marca el cliente como inactivo
        c["activo"] = False
        guardar_clientes(clientes)
        print("✔ Baja logica aplicada (cliente inactivo).")

    except KeyError:
        print("✖ Error: Estructura de cliente invalida.")
    except Exception as e:
        print(f"✖ Error al aplicar baja logica: {e}")
    finally:
        input("\nEnter para continuar...")
        limpiar_pantalla()


def baja_fisica_cliente(dni):
    try:
        # Carga los clientes desde el archivo
        clientes = cargar_clientes()

        # Verifica si el cliente existe
        if dni in clientes:
            # En lugar de usar 'del'.
            del clientes[dni]
            guardar_clientes(clientes)
            print("✔ Cliente eliminado fisicamente.")
        else:
            print("✖ No existe un cliente con ese DNI.")

    except Exception as e:
        print(f"✖ Error al eliminar cliente: {e}")
    finally:
        input("\nEnter para continuar...")
        limpiar_pantalla()
