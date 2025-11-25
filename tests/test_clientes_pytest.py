"""
Tests unitarios con pytest para el módulo de clientes (ABM)
Enfocado en funciones estáticas: validar_dni, cargar_clientes, guardar_clientes.
"""
import pytest
from utils import validar_dni, validar_fecha, validar_hora, validarEmail, validarTelefono, validarTextoAlfabetico


# ---------------------------------------------------------
# TEST validarTextoAlfabetico
# ---------------------------------------------------------
def test_texto_valido():
    assert validarTextoAlfabetico("Juan Perez") == True
    assert validarTextoAlfabetico("María López") == True

def test_texto_vacio():
    assert validarTextoAlfabetico("") == False

def test_texto_invalido():
    assert validarTextoAlfabetico("Juan123") == False
    assert validarTextoAlfabetico("###") == False


# ---------------------------------------------------------
# TEST validarEmail
# ---------------------------------------------------------
def test_email_gmail_valido():
    assert validarEmail("usuario@gmail.com")
    assert validarEmail("nombre.apellido123@gmail.com")
    assert validarEmail("alias+test@gmail.com")
    assert validarEmail("test_email-01@gmail.com")

def test_email_gmail_invalido():
    # dominios incorrectos
    assert not validarEmail("usuario@hotmail.com")
    assert not validarEmail("usuario@yahoo.com")
    assert not validarEmail("usuario@gmail.es")

    # formato incorrecto
    assert not validarEmail("usuariogmail.com")
    assert not validarEmail("usuario@.com")
    assert not validarEmail("usuario@ gmail.com")
    assert not validarEmail("usuario@gmailcom")
    assert not validarEmail("usuario@gmail.")


# ---------------------------------------------------------
# TEST validar_dni
# ---------------------------------------------------------
def test_dni_valido_7_digitos():
    assert validar_dni("1234567", False) == True
    assert validar_dni("9999999", False) == True

def test_dni_valido_8_digitos():
    assert validar_dni("12345678", False) == True
    assert validar_dni("34137129", False) == True
    assert validar_dni("99999999", False) == True

def test_dni_invalido_menos_7_digitos():
    assert validar_dni("123456", False) == False
    assert validar_dni("12345", False) == False
    assert validar_dni("1", False) == False
    assert validar_dni("", False) == False

def test_dni_invalido_mas_8_digitos():
    assert validar_dni("123456789", False) == False
    assert validar_dni("1234567890", False) == False

def test_dni_con_letras():
    assert validar_dni("1234567a", False) == False
    assert validar_dni("abc12345", False) == False
    assert validar_dni("abcdefgh", False) == False

def test_dni_con_espacios():
    assert validar_dni("123 456 78", False) == False
    assert validar_dni(" 12345678", False) == False
    assert validar_dni("12345678 ", False) == False

def test_dni_caracteres_especiales():
    assert validar_dni("123-4567", False) == False
    assert validar_dni("12.345.678", False) == False
    assert validar_dni("12345678!", False) == False


# ---------------------------------------------------------
# TEST validar_fecha
# ---------------------------------------------------------
def test_fecha_valida_formato_correcto():
    assert validar_fecha("2025-12-31") == True
    assert validar_fecha("2025-11-29") == True

def test_fecha_invalida_formato_incorrecto():
    assert validar_fecha("04-11-2025") == False
    assert validar_fecha("2025/11/04") == False
    assert validar_fecha("2025.11.04") == False

def test_fecha_invalida_valores_incorrectos():
    assert validar_fecha("2025-13-01") == False
    assert validar_fecha("2025-00-01") == False
    assert validar_fecha("2025-02-30") == False

def test_fecha_vacia():
    assert validar_fecha("") == False

def test_fecha_incompleta():
    assert validar_fecha("2025-11") == False
    assert validar_fecha("2025") == False


# ---------------------------------------------------------
# TEST validar_hora
# ---------------------------------------------------------
def test_hora_valida_formato_correcto():
    assert validar_hora("00:00") == True
    assert validar_hora("12:30") == True
    assert validar_hora("23:59") == True

def test_hora_invalida_formato_incorrecto():
    assert validar_hora("8:15") == False
    assert validar_hora("08:5") == False
    assert validar_hora("12-30") == False

def test_hora_invalida_valores_incorrectos():
    assert validar_hora("24:00") == False
    assert validar_hora("25:00") == False
    assert validar_hora("12:99") == False

def test_hora_vacia():
    assert validar_hora("") == False

def test_hora_incompleta():
    assert validar_hora("12:") == False
    assert validar_hora(":30") == False


# ---------------------------------------------------------
# TEST validarTelefono
# ---------------------------------------------------------
def test_telefono_vacio():
    assert validarTelefono("") == True  # es opcional

def test_telefono_valido():
    assert validarTelefono("11 2345-6789") == True

def test_telefono_invalido():
    assert validarTelefono("12345") == False
    assert validarTelefono("11-2345-6789") == False
    assert validarTelefono("11 23456-78901") == False