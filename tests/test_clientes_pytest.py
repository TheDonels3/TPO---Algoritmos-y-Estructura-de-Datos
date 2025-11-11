"""
Tests unitarios con pytest para el módulo de clientes (ABM)
Enfocado en funciones estáticas: validar_dni, cargar_clientes, guardar_clientes.

Hay 29 Funcion con el Nombre de Test_.
"""
import pytest
import json
from utils import validar_dni, validar_fecha, validar_hora, validarEmail
from storage import cargar_clientes, guardar_clientes, CLIENTES_JSON


# ---------------------------------------------------------
# TEST DE FUNCION validar_dni
# ---------------------------------------------------------
def test_dni_valido_7_digitos():
    assert validar_dni("1234567") == True
    assert validar_dni("9999999") == True

def test_dni_valido_8_digitos():
    assert validar_dni("12345678") == True
    assert validar_dni("34137129") == True
    assert validar_dni("99999999") == True

def test_dni_invalido_menos_7_digitos():
    assert validar_dni("123456") == False
    assert validar_dni("12345") == False
    assert validar_dni("1") == False
    assert validar_dni("") == False

def test_dni_invalido_mas_8_digitos():
    assert validar_dni("123456789") == False
    assert validar_dni("1234567890") == False
    assert validar_dni("123456789012345") == False

def test_dni_con_letras():
    assert validar_dni("1234567a") == False
    assert validar_dni("abc12345") == False
    assert validar_dni("abcdefgh") == False
    assert validar_dni("12a45678") == False

def test_dni_vacio():
    assert validar_dni("") == False

def test_dni_con_espacios():
    assert validar_dni("123 456 78") == False
    assert validar_dni(" 12345678") == False
    assert validar_dni("12345678 ") == False
    assert validar_dni("1234 5678") == False

def test_dni_caracteres_especiales():
    assert validar_dni("123-4567") == False
    assert validar_dni("12.345.678") == False
    assert validar_dni("12,345,678") == False
    assert validar_dni("12345678!") == False

# ---------------------------------------------------------
# TEST DE FUNCION validarEmail
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
# TEST DE FUNCION validar_fecha
# ---------------------------------------------------------
def test_fecha_valida_formato_correcto():
    assert validar_fecha("2025-11-04") == True
    assert validar_fecha("2025-01-01") == True
    assert validar_fecha("2025-12-31") == True

def test_fecha_invalida_formato_incorrecto():
    assert validar_fecha("04-11-2025") == False
    assert validar_fecha("2025/11/04") == False
    assert validar_fecha("2025.11.04") == False
    assert validar_fecha("04/11/2025") == False

def test_fecha_invalida_valores_incorrectos():
    assert validar_fecha("2025-13-01") == False
    assert validar_fecha("2025-00-01") == False
    assert validar_fecha("2025-02-30") == False
    assert validar_fecha("2025-04-31") == False

def test_fecha_vacia():
    assert validar_fecha("") == False

def test_fecha_incompleta():
    assert validar_fecha("2025-11") == False
    assert validar_fecha("2025") == False
    assert validar_fecha("11-04") == False


# ---------------------------------------------------------
# TEST DE FUNCION validar_hora
# ---------------------------------------------------------
def test_hora_valida_formato_correcto():
    assert validar_hora("00:00") == True
    assert validar_hora("12:30") == True
    assert validar_hora("23:59") == True
    assert validar_hora("08:15") == True

def test_hora_invalida_formato_incorrecto():
    assert validar_hora("8:15") == False
    assert validar_hora("08:5") == False
    assert validar_hora("8:5") == False
    assert validar_hora("12-30") == False
    assert validar_hora("12.30") == False

def test_hora_invalida_valores_incorrectos():
    assert validar_hora("24:00") == False
    assert validar_hora("25:00") == False
    assert validar_hora("12:60") == False
    assert validar_hora("12:99") == False

def test_hora_vacia():
    assert validar_hora("") == False

def test_hora_incompleta():
    assert validar_hora("12:") == False
    assert validar_hora(":30") == False
    assert validar_hora("12") == False


# ---------------------------------------------------------
# FIXTURE PARA ARCHIVO TEMPORAL
# ---------------------------------------------------------
@pytest.fixture
def archivo_temporal(tmp_path):
    archivo = tmp_path / "clientes_test.json"
    import storage
    clientes_json_original = storage.CLIENTES_JSON
    storage.CLIENTES_JSON = str(archivo)
    yield archivo
    storage.CLIENTES_JSON = clientes_json_original


# ---------------------------------------------------------
# TESTS DE FUNCION cargar_clientes
# ---------------------------------------------------------
def test_cargar_archivo_valido(archivo_temporal):
    datos = {
        "12345678": {
            "dni": "12345678",
            "nombre": "Juan",
            "apellido": "Perez",
            "email": "juan@test.com",
            "telefono": "123456",
            "activo": True
        }
    }
    archivo_temporal.write_text(json.dumps(datos, ensure_ascii=False))
    resultado = cargar_clientes()
    assert resultado == datos
    assert "12345678" in resultado
    assert resultado["12345678"]["nombre"] == "Juan"

def test_cargar_archivo_vacio(archivo_temporal):
    archivo_temporal.write_text("")
    resultado = cargar_clientes()
    assert resultado == {}
    assert len(resultado) == 0

def test_cargar_archivo_inexistente(tmp_path):
    import storage
    storage.CLIENTES_JSON = str(tmp_path / "no_existe.json")
    resultado = cargar_clientes()
    assert resultado == {}

def test_cargar_json_malformado(archivo_temporal, capsys):
    archivo_temporal.write_text("{invalid json content")
    resultado = cargar_clientes()
    assert resultado == {}
    captured = capsys.readouterr()
    assert "Error al cargar clientes" in captured.out

def test_cargar_diccionario_vacio(archivo_temporal):
    archivo_temporal.write_text("{}")
    resultado = cargar_clientes()
    assert resultado == {}

def test_cargar_multiples_clientes(archivo_temporal):
    datos = {
        "11111111": {"dni": "11111111", "nombre": "Ana", "apellido": "Garcia", "email": "ana@test.com", "telefono": "111111", "activo": True},
        "22222222": {"dni": "22222222", "nombre": "Carlos", "apellido": "Lopez", "email": "carlos@test.com", "telefono": "222222", "activo": False}
    }
    archivo_temporal.write_text(json.dumps(datos, ensure_ascii=False))
    resultado = cargar_clientes()
    assert len(resultado) == 2
    assert "11111111" in resultado
    assert "22222222" in resultado


# ---------------------------------------------------------
# TESTS DE FUNCION guardar_clientes
# ---------------------------------------------------------
def test_guardar_diccionario_vacio(archivo_temporal):
    resultado = guardar_clientes({})
    assert resultado == True
    contenido = json.loads(archivo_temporal.read_text())
    assert contenido == {}

def test_guardar_un_cliente(archivo_temporal):
    cliente = {
        "12345678": {"dni": "12345678", "nombre": "Maria", "apellido": "Gonzalez", "email": "maria@test.com", "telefono": "987654", "activo": True}
    }
    resultado = guardar_clientes(cliente)
    assert resultado == True
    contenido = json.loads(archivo_temporal.read_text())
    assert contenido == cliente

def test_guardar_multiples_clientes(archivo_temporal):
    clientes = {
        "11111111": {"dni": "11111111", "nombre": "Pedro", "apellido": "Ruiz", "email": "pedro@test.com", "telefono": "111", "activo": True},
        "22222222": {"dni": "22222222", "nombre": "Laura", "apellido": "Diaz", "email": "laura@test.com", "telefono": "222", "activo": True}
    }
    resultado = guardar_clientes(clientes)
    assert resultado == True
    contenido = json.loads(archivo_temporal.read_text())
    assert len(contenido) == 2
    assert "11111111" in contenido
    assert "22222222" in contenido


# ---------------------------------------------------------
# TESTS DE INTEGRACIÓN
# ---------------------------------------------------------
def test_guardar_y_cargar(archivo_temporal):
    datos_originales = {
        "12345678": {"dni": "12345678", "nombre": "Test", "apellido": "Usuario", "email": "test@test.com", "telefono": "123456789", "activo": True}
    }
    guardar_clientes(datos_originales)
    datos_cargados = cargar_clientes()
    assert datos_cargados == datos_originales

def test_modificar_cliente_guardado(archivo_temporal):
    cliente_inicial = {
        "12345678": {"dni": "12345678", "nombre": "Original", "apellido": "Apellido", "email": "original@test.com", "telefono": "111", "activo": True}
    }
    guardar_clientes(cliente_inicial)
    clientes = cargar_clientes()
    clientes["12345678"]["nombre"] = "Modificado"
    clientes["12345678"]["email"] = "modificado@test.com"
    guardar_clientes(clientes)
    clientes_finales = cargar_clientes()
    assert clientes_finales["12345678"]["nombre"] == "Modificado"
    assert clientes_finales["12345678"]["email"] == "modificado@test.com"

