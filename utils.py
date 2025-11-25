import os
import re
from datetime import datetime
from storage import cargar_clientes, log


# Funcion para Limpiar la Consola
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


# Funcion de Validacion de Texto
def validarTextoAlfabetico(texto):

    #Patron a Seguir
    RE_TEXTO = re.compile(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$')

    # 1. Validacion de Ingreso
    if len(texto) < 1:
        print("✖ El campo no puede quedar vacio.")
        log("WARN", "validarTextoAlfabetico", "Texto vacio ingresado")
        return False

    # 2. Validacion del formato Nombre
    elif not RE_TEXTO.match(texto):
        print("✖ Solo se permiten letras y espacios simples.")
        log("WARN", "v lidarTextoAlfabetico", f"Formato inválido: '{texto}'")
        return False

    log("INFO", "validarTextoAlfabetico", f"Texto válido: '{texto}'")
    return True


# Funcion de Validacion de Email
def validarEmail(email, verificar_existencia):    

    clientes = cargar_clientes()

    #Patron a Seguir
    RE_EMAIL = re.compile(r'^[a-zA-Z0-9._%+-]+@gmail\.com$')

    # 1. Validacion de Ingreso
    if email == "":
        print("✖ Debe ingresar un Email. No puede quedar vacio.")
        log("WARN", "validarEmail", "Texto vacio ingresado")
        return False
    
    # 2. Validacion de formato de GMAIL
    elif not bool(RE_EMAIL.match(email)):
        print("✖ EMAIL invalido. Debe ser una direccion de Gmail valida.")
        log(f"WARN", "validarEmail", f"Formato Invalido: '{email}'")
        return False

    # 3. Validacion si ya existe el GMAIL
    else:
        if verificar_existencia:
            for c in clientes.values():
                if c.get("email", "") == email:
                    print("✖ Ya existe un cliente con ese Email.")
                    log("WARN", "validarEmail", "Gmail Existente Cargado")
                    return False

    log("INFO", "validarTextoAlfabetico", f"Email Valido: '{email}'")
    return True


# Funcion para Validar el Ingreso del DNI
def validar_dni(dni, verificar_existencia):

    # Patrón DNI argentino (7 u 8 dígitos, sin empezar en 0)
    RE_DNI = re.compile(r"^[1-9]\d{6,7}$")

    # 1. Primero validar formato
    if not RE_DNI.match(dni):
        print("✖ DNI inválido. Debe tener 7 u 8 dígitos y no empezar en 0.")
        log("WARN", "validar_dni", f"Formato Invalido: '{dni}'")
        return False

    # 2. Verificar existencia solo si se quiere
    elif verificar_existencia:
        clientes = cargar_clientes()
        cliente = clientes.get(dni)
        if not cliente:
            print("✖ No existe un cliente con ese DNI.")
            log("WARN", "validar_dni", f"DNI Existente Cargado: '{dni}'")
            return False

    log("Info", "validar_dni", f"DNI Valido: '{dni}'")
    return True


# Valida que la fecha cumpla el formato y sea una fecha valida
def validar_fecha(fecha):

    # Salva Guarda de Datetime
    if fecha is None:
        return

    # 1. Verifica el Formato de la Fecha y si Existe
    try:
        fecha_dt = datetime.strptime(fecha, "%Y-%m-%d").date()
    except ValueError:
        print("✖ Formato inválido. Debe ser YYYY-MM-DD y la fecha debe existir.")
        log("WARN", "validar_fecha", f"Formato inválido: '{fecha}'")
        return False

    hoy = datetime.today().date()

    # 2. Verifica si la Fecha Ingresada no es pasada la fecha actual
    if fecha_dt < hoy:
        print(f"✖ La fecha ingresada ({fecha}) es anterior a la fecha actual ({hoy}).")
        log("WARN", "validar_fecha", f"Fecha ingresada en el pasado: '{fecha_dt}' < '{hoy}'")
        return False

    log("INFO", "validar_fecha", f"Fecha válida: {fecha_dt}")
    return True


# Funcionp para Validar la Hora Ingresada
def validar_hora(hora):

    RE_HORA = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")  # Formato HH:mm

    if not RE_HORA.match(hora):
        print("✖ Hora invalida. Debe ser un formato HH:mm entre 00:00 y 23:59.")
        log("WARN", "validar_hora", f"Hora inválida ingresada: '{hora}'")
        return False
        
    log("INFO", "validar_hora", f"Hora válida: '{hora}'")
    return True


# Funcion para Validar el Telefono Ingresado
def validarTelefono(telefono):

    #Patron a Seguir
    RE_TELEFONO = re.compile(r"^\d{2,4}\s\d{3,5}-\d{3,4}$") #Formato: 11 2345-6543
    
    # 1. Validacion de Ingreso (Es Opcional el Telefono)
    if len(telefono) < 1:
        return True
    
    # 2. Validacion del Formato
    elif not RE_TELEFONO.match(telefono):
        print("✖ Formato Invalido. Ejemplo valido: 11 2345-6789")
        log("WARN", "validarTelefono", f"Telefono Formato Invalido: '{telefono}'")
        return False

    log("INFO", "validarTelefono", f"Telefono Valido: '{telefono}'")
    return True

