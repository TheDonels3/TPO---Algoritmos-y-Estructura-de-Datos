from os import remove
from utils import limpiar_pantalla, validar_fecha, validar_hora, validar_dni
from storage import cargar_turnos, guardar_turnos, bloqueos_por_fecha, _obtener_next_turno_id, cargar_clientes, log
from GMAIL import mensaje_confirmacion, mensaje_modificacion, mensaje_eliminacion
import smtplib
from datetime import datetime


# ---------------------------------------------------------
# FUNCIONES AUXILIARES 
# ---------------------------------------------------------

# Verifica si ya existe un turno ocupado en una fecha y hora determinada
def _existe_turno_en_slot(turnos, fecha, hora):
    for t in turnos:
        if t.get("fecha") == fecha and t.get("hora") == hora and t.get("estado") == "Ocupado":
            return True
    return False

# Verifica si un horario específico está bloqueado para una fecha
def _slot_bloqueado(fecha, hora):
    return hora in bloqueos_por_fecha.get(fecha, set())


# Verifica que la fecha y hora del turno sean futuras (no pasadas)
def _es_fecha_hora_futura(fecha, hora):
    """
    Valida que la fecha y hora proporcionadas sean posteriores al momento actual.
    Retorna True si es futura, False si es pasada.
    """
    try:
        # Combinar fecha y hora en un objeto datetime
        fecha_hora_turno = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
        # Obtener el momento actual
        ahora = datetime.now()
        # Comparar
        return fecha_hora_turno > ahora
    except ValueError:
        log("ERRO", "_es_fecha_hora_futura", f"ValueError: Fecha u hora inválida - {fecha} {hora}")
        # Si hay error al parsear, retornar False por seguridad
        return False


# Verifica si un cliente con un DNI dado está activo en el sistema
def _cliente_activo(clientes, dni):
    c = clientes.get(dni)
    return bool(c and c.get("activo", False))


# Obtiene el nombre completo del cliente dado su DNI
def _obtener_nombre_cliente(dni):
    """
    Retorna el nombre y apellido del cliente para mostrar en listados.
    Si el DNI es especial (Bloqueado, Sin Asignar) o no se encuentra, retorna un texto descriptivo.
    """
    # Casos especiales
    if dni == "Bloqueado":
        return "[HORARIO BLOQUEADO]"
    if dni == "Sin Asignar":
        return "[Sin Asignar]"
    
    # Buscar cliente en el sistema
    clientes = cargar_clientes()
    cliente = clientes.get(dni)
    
    if cliente:
        nombre = cliente.get("nombre", "")
        apellido = cliente.get("apellido", "")
        return f"{apellido}, {nombre}"
    else:
        return "[Cliente no encontrado]"


# ---------------------------------------------------------
# FUNCIÓN PRINCIPAL: ALTA DE TURNO
# ---------------------------------------------------------

def alta_turno(dni, fecha, hora):
    """
    Registra un nuevo turno para un cliente, si pasa todas las validaciones:
    - Fecha válida
    - Hora válida
    - Cliente activo
    - Horario no bloqueado
    - Horario no ocupado
    """
    try:
        clientes = cargar_clientes()
        turnos = cargar_turnos()

        # Validación del formato de fecha (debe ser YYYY-MM-DD)
        if not validar_fecha(fecha):
            print("✖ Fecha inválida. Formato esperado YYYY-MM-DD.")
            return
        
        # Validación del formato de hora (debe ser HH:mm)
        if not validar_hora(hora):
            print("✖ Hora inválida. Formato esperado HH:mm.")
            return
        
        # Validación de que la fecha y hora sean futuras
        if not _es_fecha_hora_futura(fecha, hora):
            print("✖ No se puede agendar un turno en una fecha y hora pasadas.")
            return
        
        # Verificación de que el cliente exista y esté activo
        if not _cliente_activo(clientes, dni):
            print("✖ Cliente inexistente o inactivo.")
            return
        
        # Comprobación de que el horario no esté bloqueado en esa fecha
        if _slot_bloqueado(fecha, hora):
            print("✖ El horario está BLOQUEADO para esa fecha.")
            return
        
        # Verificación de que no exista ya un turno ocupado en ese horario
        if _existe_turno_en_slot(turnos, fecha, hora):
            print("✖ El horario ya está OCUPADO.")
            return

        # Si todas las validaciones pasan, se crea el turno y se guarda
        next_id = _obtener_next_turno_id(turnos)
        turno = {
            "id": next_id,           # Se genera un nuevo ID único
            "dni": dni,              # DNI del cliente
            "fecha": fecha,          # Fecha del turno
            "hora": hora,            # Hora del turno
            "estado": "Ocupado"      # Estado inicial del turno
        }
        # Se agrega el turno a la lista global de turnos
        turnos.append(turno)

        # Envío de correo de confirmación
        try:
            cliente = clientes.get(dni)
            if not cliente or not cliente.get("email"):
                print("⚠ El cliente no tiene un email registrado. No se enviará confirmación.")
            else:
                mensaje_confirmacion(cliente,turno)
                log("INFO", "alta_turno", f"Correo de confirmación enviado a {cliente.get('email')} para turno ID {turno['id']}")

        except smtplib.SMTPException as e:
            print(f"✖ Error al enviar el correo de confirmación: {e}")
            log("ERRO", "alta_turno", f"SMTPException: {e}")
        except KeyError as e_mail:
            print(f"✖ Error: El cliente no tiene un email válido registrado: {e_mail}")
            log("ERRO", "alta_turno", f"KeyError: {e_mail}")
        except Exception as e_mailenviado:
            print(f"✖ Error inesperado al enviar el correo de confirmación: {e_mailenviado}")
            log("ERRO", "alta_turno", f"Exception: {e_mailenviado}")

        # Guardamos después de intentar enviar el mail
        guardar_turnos(turnos)
        print("✔ Turno registrado correctamente.")
        
    except KeyError as e:
        # Esto saltaría si _cliente_activo falla al buscar c["activo"]
        print(f"✖ Error: Faltan datos en el registro del cliente: {e}")
        log("ERRO", "alta_turno", f"KeyError: {e}")
    except KeyboardInterrupt:
        print("\n✖ Operación cancelada por el usuario.")
        log("INFO", "alta_turno", "Operación cancelada por el usuario")
    except Exception as e:
        print(f"✖ Error inesperado al registrar el turno: {e}")
        log("ERRO", "alta_turno", f"Exception: {e}")
    finally:
        input("\nEnter para continuar...")
        limpiar_pantalla()


# ---------------------------------------------------------
# FUNCIÓN: LISTAR TURNOS
# ---------------------------------------------------------

def listar_turnos():
    """
    Muestra todos los turnos registrados en pantalla.
    Si no hay turnos, informa al usuario.
    """
    try:
        turnos = cargar_turnos()

        # Si no hay turnos, se muestra un mensaje informativo
        if not turnos:
            print("No hay turnos registrados.")
            return
        
        # Recorre la lista de turnos (ordenada por fecha y hora) y muestra la información de cada uno
        for t in sorted(turnos, key=lambda x: (x["fecha"], x["hora"])):
            nombre_cliente = _obtener_nombre_cliente(t['dni'])
            print(f"#{t['id']} | {t['fecha']} {t['hora']} | DNI: {t['dni']} | {nombre_cliente} | {t['estado']}")

    except KeyError as e:
        print(f"✖ Error: Campo faltante en datos del turno: {e}")
    except KeyboardInterrupt:
        print("\n✖ Operación cancelada por el usuario.")
    except Exception as e:
        print(f"✖ Error al listar turnos: {e}")
    finally:    
        input("\nPresione Enter para continuar...")
        limpiar_pantalla()



# ---------------------------------------------------------
# FUNCIÓN: LISTAR POR DNI
# ---------------------------------------------------------

def listar_por_dni(dni):
    """
    Muestra todos los turnos en pantalla que conicidan con el DNI ingresado por parametro.
    """
    try:   
        if not validar_dni(dni):
            print("✖ DNI inválido. Deben ser 7 u 8 digitos.")
            input("\nEnter...")
            limpiar_pantalla()
            return
        
        turnos = cargar_turnos()

        # Filtra los turnos que coincidan con el DNI
        lista_dni = [t for t in turnos if t["dni"] == dni]
        
        if not lista_dni:
            print(f"No hay turnos registrados para el DNI {dni}.")
        else:
            nombre_cliente = _obtener_nombre_cliente(dni)
            print(f"--- Turnos para el DNI: {dni} - {nombre_cliente} ---")
            # Ordena los turnos por fecha y luego por hora
            for t in sorted(lista_dni, key=lambda x: (x["fecha"], x["hora"])):
                print(f"#{t['id']} | {t['fecha']} {t['hora']} | {t['estado']}")

    except KeyError as e:
        print(f"✖ Error: Campo faltante en datos del turno: {e}")
    except KeyboardInterrupt:
        print("\n✖ Operación cancelada por el usuario.")
    except Exception as e:
        print(f"✖ Error al listar turnos por DNI: {e}")    
    finally:
        input("\nEnter para continuar...")
        limpiar_pantalla()



# ---------------------------------------------------------
# FUNCIÓN: LISTAR POR FECHA
# ---------------------------------------------------------

def listar_por_fecha(fecha):
    """
    Muestra todos los turnos en pantalla que conicidan con la fecha ingresada por parametro.
    """
    try:
        if not validar_fecha(fecha):
            print("✖ Fecha inválida. Formato esperado YYYY-MM-DD.")
            return
        
        turnos = cargar_turnos()

        lista_fecha = [t for t in turnos if t["fecha"]==fecha]
        print(f"--- Turnos para la fecha: {fecha} ---")
        
        if not lista_fecha:
            print("No hay turnos para esa fecha.")
        for t in sorted(lista_fecha, key=lambda x: x["hora"]):
            nombre_cliente = _obtener_nombre_cliente(t['dni'])
            print(f"#{t['id']} | {t['hora']} | DNI: {t['dni']} | {nombre_cliente} | {t['estado']}")
    
    except KeyError as e:
        print(f"✖ Error: Campo faltante en datos del turno: {e}")
    except KeyboardInterrupt:
        print("\n✖ Operación cancelada por el usuario.")
    except Exception as e:
        print(f"✖ Error al listar turnos por fecha: {e}")
    finally:
        input("\nEnter para continuar...")
        limpiar_pantalla()



# ---------------------------------------------------------
# FUNCIÓN: MODIFICAR TURNO
# ---------------------------------------------------------

def modificar_turno(id_turno, nuevo_dni=None, nueva_fecha=None, nueva_hora=None):
    """
    Modifica el DNI, la fecha y/o la hora de un turno existente,
    realizando todas las validaciones necesarias.
    """
    try:
        turnos = cargar_turnos()
        clientes = cargar_clientes()

        # 1. Buscar el turno por ID
        turno_a_modificar = None

        for turno in turnos:
            if turno["id"] == id_turno:
                turno_a_modificar = turno
        if not turno_a_modificar:
            print(f"✖ No se encontró un turno con ID {id_turno}.")
            return

        # 2. Verificar si se pidio algun cambio
        if not nuevo_dni and not nueva_fecha and not nueva_hora:
            print("✖ No se especificaron cambios.")
            return

        # 3. Determinar el estado "final" del turno para validaciones
        # Usamos el valor nuevo si se proveyó, o el valor actual si no.
        fecha_final = nueva_fecha or turno_a_modificar['fecha']
        hora_final = nueva_hora or turno_a_modificar['hora']

        cambios_realizados = []

        # 4. Validar DNI (si se cambió)
        if nuevo_dni:
            if not validar_dni(nuevo_dni):
                print(f"✖ DNI {nuevo_dni} no tiene un formato válido.")
                return
            if not _cliente_activo(clientes, nuevo_dni):
                print(f"✖ Cliente con DNI {nuevo_dni} no existe o está inactivo.")
                return

        # 5. Validar Slot (Fecha/Hora) (si se cambió alguno de los dos)
        # Solo validamos el slot si la fecha o la hora son distintas al original
        if nueva_fecha or nueva_hora:
            
            # Validar formatos
            if nueva_fecha and not validar_fecha(nueva_fecha):
                print(f"✖ Fecha {nueva_fecha} inválida. Formato YYYY-MM-DD.")
                return
            if nueva_hora and not validar_hora(nueva_hora):
                print(f"✖ Hora {nueva_hora} inválida. Formato HH:mm.")
                return

            # Validar disponibilidad del slot (usando los valores finales)
            if _slot_bloqueado(fecha_final, hora_final):
                print(f"✖ El horario {fecha_final} {hora_final} está BLOQUEADO.")
                return
            
            # Validamos que no exista OTRO turno (excluyendo el actual)
            for t in turnos:
                if t["id"] != id_turno and \
                   t["fecha"] == fecha_final and \
                   t["hora"] == hora_final and \
                   t["estado"] == "Ocupado":
                    print(f"✖ El horario {fecha_final} {hora_final} ya está OCUPADO por otro turno.")
                    return

        # 6. Aplicar los cambios (si todas las validaciones pasaron)
        if nuevo_dni:
            turno_a_modificar['dni'] = nuevo_dni
            cambios_realizados.append(f"DNI a {nuevo_dni}")
        
        if nueva_fecha:
            turno_a_modificar['fecha'] = nueva_fecha
            cambios_realizados.append(f"Fecha a {nueva_fecha}")

        if nueva_hora:
            turno_a_modificar['hora'] = nueva_hora
            cambios_realizados.append(f"Hora a {nueva_hora}")
        

        # Si el turno ahora tiene un DNI "real" (no "Sin Asignar")
        # y su estado anterior era "Libre", lo actualizamos a "Ocupado".
        if turno_a_modificar['dni'] != "Sin Asignar" and turno_a_modificar['estado'] == "Libre":
            turno_a_modificar['estado'] = "Ocupado"
            if "Estado del Turno: Ocupado" not in cambios_realizados:
                 cambios_realizados.append("Estado del Turno: Ocupado")



        # 7. Guardar y notificar
        guardar_turnos(turnos)
        print(f"✔ Turno ID {id_turno} actualizado: {', '.join(cambios_realizados)}.")
        
        # 8. Enviar email de re-confirmación
        try:
                # print("Enviando email de re-confirmación...")
                # mensaje_confirmacion(turno_a_modificar)
                cliente = clientes.get(nuevo_dni)
                if not cliente or not cliente.get("email"):
                    print("⚠ El cliente no tiene un email registrado. No se enviará confirmación.")
                else:
                    mensaje_modificacion(cliente,turno_a_modificar)
                    log("INFO", "modificar_turno", f"Correo de re-confirmación enviado a {cliente.get('email')} para turno ID {turno_a_modificar['id']}")

        except smtplib.SMTPException as e:
            print(f"⚠ Error al enviar la re-confirmación (SMTP): {e}")
            log("ERRO", "modificar_turno", f"SMTPException: {e}")
        except KeyError as e_mail:
            print(f"⚠ Error: El nuevo cliente no tiene un email válido registrado: {e_mail}")
            log("ERRO", "modificar_turno", f"KeyError: {e_mail}")
        except Exception as e_mailenviado:
            print(f"⚠ Error inesperado al enviar la re-confirmación: {e_mailenviado}")
            log("ERRO", "modificar_turno", f"Exception: {e_mailenviado}")
        

    except KeyError as e:
        print(f"✖ Error: Faltan datos en el registro del turno/cliente: {e}")
        log("ERRO", "modificar_turno", f"KeyError: {e}")
    except KeyboardInterrupt:
        print("\n✖ Operación cancelada por el usuario.")
        log("INFO", "modificar_turno", "Operación cancelada por el usuario")
    except Exception as e:
        print(f"✖ Error inesperado al modificar el turno: {e}")
        log("ERRO", "modificar_turno", f"Exception: {e}")
    finally:
        input("\nEnter para continuar...")
        limpiar_pantalla()





# ---------------------------------------------------------
# FUNCIÓN: BLOQUEAR SLOT
# ---------------------------------------------------------

def bloquear_slot(fecha, hora):
    """
    Crea un turno "Ocupado" con DNI "Bloqueado" para evitar
    que se saquen turnos en ese horario.
    """
    try:
        turnos = cargar_turnos()

        # 1. Validaciones de formato
        if not validar_fecha(fecha):
            print("✖ Fecha inválida. Formato esperado YYYY-MM-DD.")
            input("\nEnter...")
            limpiar_pantalla()
            return

        if not validar_hora(hora):
            print("✖ Hora inválida. Formato esperado HH:mm.")
            input("\nEnter...")
            limpiar_pantalla()
            return

        # 2. Buscar si ya existe un slot en esa fecha/hora        
        slot_existente = None
        for i in turnos:
            if i["fecha"] == fecha and i["hora"] == hora:
                slot_existente = i

        if slot_existente:
            # Caso: El slot ya existe
            if slot_existente["estado"] == "Ocupado":
                if slot_existente["dni"] == "Bloqueado":
                    print(f"ℹ El slot {fecha} {hora} ya se encontraba bloqueado.")
                else:
                    print(f"✖ El slot {fecha} {hora} está OCUPADO por un cliente (DNI: {slot_existente['dni']}). No se puede bloquear.")
            
            elif slot_existente["estado"] == "Libre":
                # Si estaba libre (ej. DNI "Sin Asignar"), lo "ocupamos" para bloquearlo
                slot_existente["dni"] = "Bloqueado"
                slot_existente["estado"] = "Ocupado"
                guardar_turnos(turnos)
                print(f"✔ Slot {fecha} {hora} (que estaba libre) ha sido bloqueado.")
        
        else:
            # Caso: El slot no existe en el JSON, se crea como nuevo bloqueo
            next_id = _obtener_next_turno_id(turnos)
            t = {
                "id": next_id,
                "dni": "Bloqueado", # DNI especial para identificarlo
                "fecha": fecha,
                "hora": hora,
                "estado": "Ocupado" # Ocupado para que _existe_turno_en_slot lo detecte
            }
            turnos.append(t)
            guardar_turnos(turnos)
            log("INFO", "bloquear_slot", f"Slot {fecha} {hora} ha sido creado y bloqueado exitosamente.")
            print(f"✔ Slot {fecha} {hora} ha sido creado y bloqueado exitosamente.")

    except KeyboardInterrupt:
        print("\n✖ Operación cancelada por el usuario.")
        log("INFO", "bloquear_slot", "Operación cancelada por el usuario")
    except Exception as e:
        print(f"✖ Error inesperado al bloquear el slot: {e}")
        log("ERRO", "bloquear_slot", f"Exception: {e}")
    finally:
        input("\nEnter para continuar...")
        limpiar_pantalla()


# ---------------------------------------------------------
# FUNCIÓN: DESBLOQUEAR_SLOT
# ---------------------------------------------------------

def desbloquear_slot(fecha, hora):

    try:
        turnos = cargar_turnos()

        # Validaciones
        if not validar_fecha(fecha):
            print("✖ Fecha inválida. Formato esperado YYYY-MM-DD.")
            input("\nEnter...")
            limpiar_pantalla()
            return

        if not validar_hora(hora):
            print("✖ Hora inválida. Formato esperado HH:mm.")
            input("\nEnter...")
            limpiar_pantalla()
            return


        # Busca el turno que coincida con la fecha y la hora indicadas
        for turno in turnos:
            if turno["fecha"] == fecha and turno["hora"] == hora:

                # Si el turno está ocupado, lo "desbloquea"
                if turno["estado"] == "Ocupado":

                    turno["dni"] = "Sin Asignar"
                    turno["estado"] = "Libre"
                    print(f"✔ Turno {fecha} {hora} desbloqueado.")
                    guardar_turnos(turnos)
                    log("INFO", "desbloquear_slot", f"Turno {fecha} {hora} desbloqueado.")
                    return
                
                # Si el turno ya estaba libre, informa que no se puede desbloquear
                else:
                    print(f"✖ El turno {fecha} {hora} no está bloqueado.")
                    return
            
        # En caso de no encontrar el turno lo informa
        print(f"✖ No se encontró el turno {fecha} {hora}.")
    
    except KeyError as e:
        print(f"✖ Error: Campo faltante en datos del turno: {e}")
        log("ERRO", "desbloquear_slot", f"KeyError: {e}")
    except KeyboardInterrupt:
        print("\n✖ Operación cancelada por el usuario.")
        log("INFO", "desbloquear_slot", "Operación cancelada por el usuario")
    except Exception as e:
        print(f"✖ Error al desbloquear turno: {e}")
        log("ERRO", "desbloquear_slot", f"Exception: {e}")
    finally:
        input("\nEnter para continuar...")
        limpiar_pantalla()



# ---------------------------------------------------------
# FUNCIÓN: ELIMINAR_TURNO_POR_ID
# ---------------------------------------------------------
def eliminar_turno_por_id(id_turno):
    """
    Elimina un turno por su ID, recibida por parámetro.
    """
    try:
        turnos = cargar_turnos()

        for t in turnos:
            if t["id"] == id_turno:
                print(f"✔ Turno con ID {id_turno} - FECHA: {t['fecha']} - HORA: {t['hora']} - eliminado correctamente.")
                turnos.remove(t)
                guardar_turnos(turnos)
                return

        if id_turno not in turnos:
            print(f"✖ Turno con ID {id_turno} no encontrado.")
            return
    except KeyError as e:
        print(f"✖ Error: Campo faltante en datos del turno: {e}")
    except KeyboardInterrupt:
        print("\n✖ Operación cancelada por el usuario.")
    except Exception as e:
        print(f"✖ Error al eliminar turno: {e}")
    
    finally:
        input("\nPresione Enter para continuar...")
        limpiar_pantalla()
    
            
