from utils import limpiar_pantalla, validar_dni, validarEmail
from storage import guardar_clientes, cargar_clientes

def validar_email_unico(email, clientes, dni_excluir=None):
    """
    Valida que el email tenga formato correcto y que no esté duplicado.
    
    Args:
        email: Email a validar
        clientes: Diccionario de clientes
        dni_excluir: DNI a excluir de la validación (para modificaciones)
    
    Returns:
        tuple: (es_valido: bool, mensaje_error: str)
    """
    # Validar formato
    if not validarEmail(email):
        return False, "✖ EMAIL invalido. Debe ser una dirección de Gmail válida."
    
    # Verificar si el email ya existe en otro cliente
    for dni_cliente, cliente in clientes.items():
        # Excluir el DNI del cliente actual en caso de modificación
        if dni_excluir and dni_cliente == dni_excluir:
            continue
        
        if cliente.get("email", "") == email:
            return False, "✖ Ya existe un cliente con ese email Gmail."
    
    return True, ""

def validar_alta_cliente():
    try:
        """
        Bucle para validar datos ingresados y crear el cliente
        """
        # Carga los clientes desde el archivo
        clientes = cargar_clientes()

        # Bucle para solicitar DNI hasta que sea válido
        while True:
            dni = input("DNI: ").strip()
            
            # Verifica que el DNI sea valido
            if not validar_dni(dni):
                print("✖ DNI invalido. Deben ser 7 u 8 digitos.")
                input("\nEnter para continuar...")
                limpiar_pantalla()
                continue
            # Verifica si el DNI ya existe
            if dni in clientes:
                print("✖ Ya existe un cliente con ese DNI.")
                input("\nEnter para continuar...")
                limpiar_pantalla()
                continue
            # DNI válido y único, salir del bucle
            break
        
        # Bucle para solicitar Nombre hasta que no esté vacío
        while True:
            nombre = input("Nombre: ").strip()
            if nombre:
                break
            print("✖ El nombre es obligatorio.")
            input("\nEnter para continuar...")
            limpiar_pantalla()
        
        # Bucle para solicitar Apellido hasta que no esté vacío
        while True:
            apellido = input("Apellido: ").strip()
            if apellido:
                break
            print("✖ El apellido es obligatorio.")
            input("\nEnter para continuar...")
            limpiar_pantalla()
        
        # Bucle para solicitar Email (opcional) hasta que sea válido
        while True:
            email = input("Email (opcional): ").strip().lower()
            if email == "":
                break
            
            # Validar email usando la función reutilizable
            es_valido, mensaje_error = validar_email_unico(email, clientes)
            if es_valido:
                break
            
            print(mensaje_error)
            input("\nEnter para continuar...")
            limpiar_pantalla()
        
        tel = input("Telefono (opcional): ").strip()
        
        alta_cliente(dni,nombre,apellido, email, tel)

    except (AttributeError, ValueError):
        print("✖ Error: Valores invalidos proporcionados.")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        input("\nEnter para continuar...")
        limpiar_pantalla()

def validar_modificacion_cliente():
    try:
         # Carga los clientes desde el archivo
        clientes = cargar_clientes()
         # Bucle para solicitar DNI hasta que sea válido y exista
        while True:
            dni = input("DNI del cliente a modificar: ").strip()
            
            # Verifica que el DNI sea valido
            if not validar_dni(dni):
                print("✖ DNI invalido. Deben ser 7 u 8 digitos.")
                input("\nEnter para continuar...")
                limpiar_pantalla()
                continue
            # Verifica si el DNI existe
            if dni not in clientes:
                print("✖ No existe un cliente con ese DNI.")
                input("\nEnter para continuar...")
                limpiar_pantalla()
                continue
            # DNI válido y existe, salir del bucle
            break
        modificar_cliente(dni)
    except (AttributeError, ValueError):
        print("✖ Error: Valores invalidos proporcionados.")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        input("\nEnter para continuar...")
        limpiar_pantalla()


def alta_cliente(dni, nombre, apellido, email, telefono):
    try:
        # Carga los clientes desde el archivo
        clientes = cargar_clientes()
        """
        
        
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
            if c.get("email", "") == email:
                print("✖ Ya existe un cliente con ese email Gmail.")
                input("\nEnter para continuar...")
                limpiar_pantalla()
                return
        """
        # Crea un nuevo registro de cliente
        clientes[dni] = {
            "dni": dni,
            "nombre": nombre.strip(),
            "apellido": apellido.strip(),
            "email": (email.strip() or ""),
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
        
        print("\n=== Datos actuales del cliente ===")
        print(f"DNI: {c['dni']}")
        print(f"Nombre: {c['nombre']}")
        print(f"Apellido: {c['apellido']}")
        print(f"Email: {c['email']}")
        print(f"Teléfono: {c['telefono']}")
        print(f"Estado: {'Activo' if c['activo'] else 'Inactivo'}")
        print("\n=== Ingrese los nuevos datos ===")
        print("(Dejar vacío para mantener el valor actual)\n")
        
        # Solicita y valida nombre
        while True:
            nombre = input(f"Nombre [{c['nombre']}]: ").strip()
            if nombre == "":
                nombre = c['nombre']
                break
            if nombre:
                break
            print("✖ El nombre no puede estar vacío si desea modificarlo.")
            input("\nEnter para continuar...")
            limpiar_pantalla()
        
        # Solicita y valida apellido
        while True:
            apellido = input(f"Apellido [{c['apellido']}]: ").strip()
            if apellido == "":
                apellido = c['apellido']
                break
            if apellido:
                break
            print("✖ El apellido no puede estar vacío si desea modificarlo.")
            input("\nEnter para continuar...")
            limpiar_pantalla()
        
        # Solicita y valida email
        while True:
            email_input = input(f"Email [{c['email']}]: ").strip().lower()
            if email_input == "":
                email = c['email']
                break
            
            # Validar email usando la función reutilizable (excluyendo el DNI actual)
            es_valido, mensaje_error = validar_email_unico(email_input, clientes, dni_excluir=dni)
            if es_valido:
                email = email_input
                break
            
            print(mensaje_error)
            input("\nEnter para continuar...")
            limpiar_pantalla()
        
        # Solicita teléfono
        tel = input(f"Teléfono [{c['telefono']}]: ").strip()
        if tel == "":
            tel = c['telefono']
        
        # Solicita estado activo
        while True:
            activo_in = input(f"Activo? (S/N) [{ 'S' if c['activo'] else 'N' }]: ").strip().lower()
            if activo_in == "":
                activo = c['activo']
                break
            if activo_in in ('s', 'n'):
                activo = (activo_in == 's')
                break
            print("✖ Ingrese 'S' para Sí o 'N' para No.")
            input("\nEnter para continuar...")
            limpiar_pantalla()
        
        # Actualiza los campos
        c.update({
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "telefono": tel,
            "activo": activo
        })
        
        # Guarda los cambios
        guardar_clientes(clientes)
        print("\n✔ Cliente actualizado correctamente.")

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
