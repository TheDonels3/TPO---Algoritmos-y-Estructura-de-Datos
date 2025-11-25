import smtplib
from storage import log

# Funcion para Informar la Confizacion del Turno
def mensaje_confirmacion(cliente, turno):
    mensaje = (
        "Subject: Turno Confirmado\r\n\r\n"
        f"✅ *TURNO CONFIRMADO*\n\n"
        f"👤 Nombre: {cliente['nombre']} {cliente['apellido']}\n"
        f"🪪 DNI: {cliente['dni']}\n"
        f"📅 Fecha: {turno['fecha']}\n"
        f"⏰ Hora: {turno['hora']}\n\n"
        "Este es un mensaje automático. No responder."
    )

    enviar_mensaje(cliente, mensaje)


# Funcion para Informar el Cambio de Turno
def mensaje_modificacion(cliente, turno):
    mensaje =  (
        "Subject: Turno Modificado\r\n\r\n"
        f"♻️ *TU TURNO FUE MODIFICADO*\n\n"
        f"👤 Nombre: {cliente['nombre']} {cliente['apellido']}\n"
        f"🪪 DNI: {cliente['dni']}\n"
        f"📅 Nueva Fecha: {turno['fecha']}\n"
        f"⏰ Nueva Hora: {turno['hora']}\n\n    "
        "Este es un mensaje automático. No responder."
    )

    enviar_mensaje(cliente, mensaje)


# Funcion para Informar de la Eliminacion del Turno
def mensaje_eliminacion(cliente, turno):
    mensaje =  (
        "Subject: Turno Cancelado\r\n\r\n"
        f"❌ *TU TURNO FUE CANCELADO*\n\n"
        f"👤 Nombre: {cliente['nombre']} {cliente['apellido']}\n"
        f"🪪 DNI: {cliente['dni']}\n"
        f"📅 Fecha cancelada: {turno['fecha']}\n"
        f"⏰ Hora cancelada: {turno['hora']}\n\n"
        "Este es un mensaje automático. No responder."
    )

    enviar_mensaje(cliente, mensaje)


def enviar_mensaje(cliente, mensaje):

    # Configuracion del servidor SMTP de Gmail
    SMTP_HOST = "smtp.gmail.com"
    SMTP_PORT = 587

    PASSWORD = "stsz slbd ikpx nsqa"
    FROM_ADDR = "gestordeturnos1@gmail.com"

    to_addr = cliente["email"]
    if not to_addr:
        print("❌ El cliente no tiene un email registrado.")
        log("WARN", "enviar_mensaje", f"Cliente DNI {cliente['dni']} no tiene email registrado")
        return

    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10)
        server.ehlo()
        server.starttls()
        server.login(FROM_ADDR, PASSWORD)
        server.sendmail(FROM_ADDR, [to_addr], mensaje.encode("utf-8"))
        log("INFO", "enviar_mensaje", f"Correo enviado a {to_addr}")
        print("Correo enviado correctamente ✅")
    except Exception as e:
        print("Error al enviar correo:", e)
        log("ERRO", "enviar_mensaje", f"Exception: {e}")
    finally:
            try:
                server.quit()
            except:
                print()


