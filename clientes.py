from utils import limpiar_pantalla, validar_dni
from storage import guardar_clientes, cargar_clientes

def alta_cliente(clientes, dni, nombre, apellido, email, telefono):
    try:

        clientes = cargar_clientes()
    
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
            "activo": True
        }
        guardar_clientes(clientes) 
        print("✔ Cliente registrado.")
    except AttributeError:
        print("✖ Error: Valores inválidos proporcionados.")
    except Exception as e:
        print(f"✖ Error inesperado al registrar cliente: {e}")
    finally:
        input("\nEnter para continuar..."); limpiar_pantalla()

def listar_clientes(clientes, solo_activos=False):
    try:
        # Recargar clientes desde el archivo JSON para tener datos actualizados
        # clientes_actualizados = cargar_clientes()

        if not clientes:
            print("No hay clientes registrados.")
            input("\nEnter para continuar..."); limpiar_pantalla(); return
        
        items = [c for c in clientes.values() if (c["activo"] or not solo_activos)]
        items = sorted(items, key=lambda c: (c["apellido"].lower(), c["nombre"].lower()))
        
        for c in items:
            estado = "Activo" if c["activo"] else "Inactivo"
            print(f"DNI: {c['dni']} | {c['apellido']}, {c['nombre']} | Email: {c['email']} | Tel: {c['telefono']} | {estado}")
    except KeyError as e:
        print(f"✖ Error: Campo faltante en datos del cliente: {e}")
    except Exception as e:
        print(f"✖ Error al listar clientes: {e}")
    finally:
        input("\nEnter para continuar..."); limpiar_pantalla()

def modificar_cliente(clientes, dni):
    try:

        # clientes = cargar_clientes()

        c = clientes.get(dni)
        if not c:
            print("✖ No existe un cliente con ese DNI.")
            input("\nEnter..."); limpiar_pantalla(); return
            
        print("Dejar vacío para mantener el valor actual.")
        nombre = input(f"Nombre ({c['nombre']}): ").strip() or c['nombre']
        apellido = input(f"Apellido ({c['apellido']}): ").strip() or c['apellido']
        email = input(f"Email ({c['email']}): ").strip() or c['email']
        tel = input(f"Teléfono ({c['telefono']}): ").strip() or c['telefono']
        activo_in = input(f"Activo? (S/N) actual={ 'S' if c['activo'] else 'N' }: ").strip().lower()
        
        if activo_in in ('s','n'):
            c['activo'] = (activo_in == 's')
        
        c.update({"nombre":nombre, "apellido":apellido, "email":email, "telefono":tel})
        guardar_clientes(clientes)
        print("✔ Cliente actualizado.")
    except KeyError as e:
        print(f"✖ Error: Campo faltante en cliente: {e}")
    except KeyboardInterrupt:
        print("\n✖ Operación cancelada por el usuario.")
    except Exception as e:
        print(f"✖ Error al modificar cliente: {e}")
    finally:
        input("\nEnter para continuar..."); limpiar_pantalla()

def baja_logica_cliente(clientes, dni):

    try:
        clientes = cargar_clientes()
        c = clientes.get(dni)
        if not c:
            print("✖ No existe un cliente con ese DNI.")
            input("\nEnter..."); limpiar_pantalla(); return
            
        c["activo"] = False
        guardar_clientes(clientes)
        print("✔ Baja lógica aplicada (cliente inactivo).")
    except KeyError:
        print("✖ Error: Estructura de cliente inválida.")
    except Exception as e:
        print(f"✖ Error al aplicar baja lógica: {e}")
    finally:
        input("\nEnter para continuar..."); limpiar_pantalla()

def baja_fisica_cliente(clientes, dni):
    try:
        clientes = cargar_clientes()
        if dni in clientes:
            del clientes[dni]
            guardar_clientes(clientes)
            print("✔ Cliente eliminado físicamente.")
        else:
            print("✖ No existe un cliente con ese DNI.")
    except Exception as e:
        print(f"✖ Error al eliminar cliente: {e}")
    finally:
        input("\nEnter para continuar..."); limpiar_pantalla()
