from utils import limpiar_pantalla, validarTextoAlfabetico, validarEmail, validarTelefono
from storage import guardar_clientes, cargar_clientes, log


# Funcion para dar de Alta a Cliente
def alta_cliente(dni, nombre, apellido, email, telefono):
    try:
        # Carga los clientes desde el archivo
        clientes = cargar_clientes()
    
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
        log("INFO", "alta_cliente", f"Cliente DNI {dni} registrado correctamente")

    except AttributeError as e:
        print("✖ Error: Valores invalidos proporcionados.")
        log("ERRO", "alta_cliente", f"AttributeError: {e}")

    except Exception as e:
        print(f"✖ Error inesperado al registrar cliente: {e}")
        log("ERRO", "alta_cliente", f"Exception: {e}")

    finally:
        input("\nEnter para continuar...")
        limpiar_pantalla()

 
# Funcion para Visualizar la Lista de Clientes
def listar_clientes(solo_activos):
    try:
        # Carga los clientes actualizados desde el archivo
        clientes = cargar_clientes()
        
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
        log("ERRO", "listar_clientes", f"KeyError: {e}")
        
    except Exception as e:
        print(f"✖ Error al listar clientes: {e}")
        log("ERRO", "listar_clientes", f"Exception: {e}")

    finally:
        input("\nEnter para continuar...")
        limpiar_pantalla()


# Funcion para Modicar el Cliente
def modificar_cliente(dni):
    try:
        # Carga los clientes desde el archivo
        clientes = cargar_clientes()
        c = clientes.get(dni)

        # Solicita nuevos datos, dejando vacio para mantener el actual
        print("\nDejar vacío para mantener el valor actual.")

        nombre = input(f"Nombre ({c['nombre']}): ").strip().lower() or c['nombre']
        while not validarTextoAlfabetico(nombre):
            input("\nPresione Enter para continuar...")
            limpiar_pantalla()
            nombre = input(f"Nombre ({c['nombre']}): ").strip().lower() or c['nombre']
    
        apellido = input(f"Apellido ({c['apellido']}): ").strip().lower() or c['apellido']
        while not validarTextoAlfabetico(apellido):
            input("\nPresione Enter para continuar...")
            limpiar_pantalla()
            apellido = input(f"Apellido ({c['apellido']}): ").strip().lower() or c['apellido']

        email = input(f"Email ({c['email']}): ").strip().lower() or c['email']
        while not validarEmail(email, False):
            input("\nPresione Enter para continuar...")
            limpiar_pantalla()
            email = input(f"Email ({c['email']}): ").strip().lower() or c['email']

        tel = input(f"Teléfono ({c['telefono']}): ").strip() or c['telefono']
        while not validarTelefono(tel):
            input("\nPresione Enter para continuar...")
            limpiar_pantalla()
            tel = input(f"Teléfono ({c['telefono']}): ").strip() or c['telefono']

        activo_in = input(f"Activo? (S/N) actual={ 'S' if c['activo'] else 'N' }: ").strip().lower()

        # Actualiza el estado activo si el usuario lo cambia
        if activo_in in ('s', 'n'):
            c['activo'] = (activo_in == 's')

        # Actualiza los demás campos
        c.update({"nombre": nombre, "apellido": apellido, "email": email, "telefono": tel})

        # Guarda los cambios
        guardar_clientes(clientes)
        print("✔ Cliente actualizado.")
        log("INFO", "modificar_cliente", f"Cliente DNI {dni} modificado correctamente")

    except KeyError as e:
        print(f"✖ Error: Campo faltante en cliente: {e}")
        log("ERRO", "modificar_cliente", f"KeyError: {e}")
        
    except Exception as e:
        print(f"✖ Error al modificar cliente: {e}")
        log("ERRO", "modificar_cliente", f"Exception: {e}")

    finally:
        input("\nEnter para continuar...")
        limpiar_pantalla()


# Funcion para Baja Logica del Cliente
def baja_logica_cliente(dni):
    try:
        # Carga los clientes desde el archivo
        clientes = cargar_clientes()
        c = clientes.get(dni)

        # Marca el cliente como inactivo
        c["activo"] = False
        guardar_clientes(clientes)
        print("✔ Baja lógica aplicada (cliente inactivo).")
        log("INFO", "baja_logica_cliente", f"Cliente DNI {dni} marcado como inactivo")

    except KeyError:
        print("✖ Error: Estructura de cliente inválida.")
        log("ERRO", "baja_logica_cliente", f"KeyError: {e}")
        
    except Exception as e:
        print(f"✖ Error al aplicar baja lógica: {e}")
        log("ERRO", "baja_logica_cliente", f"Exception: {e}")

    finally:
        input("\nEnter para continuar...")
        limpiar_pantalla()


# Funcion para Baja Fisica del Cliente
def baja_fisica_cliente(dni):
    try:
        # Cargar clientes desde archivo
        clientes = cargar_clientes()

        # pop devuelve el valor eliminado
        clientes.pop(dni, None)

        guardar_clientes(clientes)
        print("✔ Cliente eliminado físicamente.")
        log("INFO", "baja_fisica_cliente", f"Cliente DNI {dni} eliminado físicamente")
     
    except Exception as e:
        print(f"✖ Error al eliminar cliente: {e}")
        log("ERRO", "baja_fisica_cliente", f"Exception: {e}")
        
    finally:
        input("\nEnter para continuar...")
        limpiar_pantalla()
