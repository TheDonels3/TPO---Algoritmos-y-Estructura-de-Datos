import smtplib
from storage import cargar_clientes

# Configuracion del servidor SMTP de Gmail
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

clientes = cargar_clientes()


# Funcion para enviar el mensaje de confirmacion del turno
def mensaje_confirmacion(turno):

    # Direccion del remitente y clave de aplicacion de Gmail
    from_addr = "gestordeturnos1@gmail.com"
    password = "rzip hnkk bubg dwlg"

    # Obtener el cliente segun el DNI del turno
    dni = turno['dni']
    cliente = clientes.get(dni)

    # Direccion de correo del destinatario
    to_addr = cliente['email']

    # Construir el mensaje de correo
    mensaje = (
        f"From: {from_addr}\r\n"
        f"To: {to_addr}\r\n"
        f"Subject: Turno Confirmado\r\n"
        "\r\n"
        f"✅ Turno confirmado ✅\n\n"
        f"👤 Nombre: {cliente['nombre']} {cliente['apellido']}\n"
        f"🪪 DNI: {cliente['dni']}\n"
        f"📅 Fecha: {turno['fecha']}\n"
        f"⏰ Hora: {turno['hora']}\n"
        "\n"
        "Este es un mensaje automatico. No responder."
    )

    try:    
        # Conectar con el servidor SMTP de Gmail
        server = smtplib.SMTP(host=SMTP_HOST, port=SMTP_PORT, timeout=10)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(user=from_addr, password=password)
        server.sendmail(from_addr, [to_addr], mensaje.encode("utf-8"))
        print("Correo enviado correctamente ✅")
    except smtplib.SMTPException as e:
        print("Error al enviar correo:", e)
    finally:
        try:
            server.quit()
        except Exception:
            pass


