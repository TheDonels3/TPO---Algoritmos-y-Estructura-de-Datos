"""
Tests unitarios con pytest para el módulo de clientes (ABM)
Enfocado en funciones estáticas: validar_dni, cargar_clientes, guardar_clientes
"""
import pytest
import json
import os
from pathlib import Path
from utils import validar_dni, validar_fecha, validar_hora
from storage import cargar_clientes, guardar_clientes, CLIENTES_JSON


# ========== TESTS PARA validar_dni (función estática pura) ==========

class TestValidarDNI:
    """Tests para la validación de DNI"""
    
    def test_dni_valido_7_digitos(self):
        """DNI válido con 7 dígitos"""
        assert validar_dni("1234567") == True
        assert validar_dni("9999999") == True
    
    def test_dni_valido_8_digitos(self):
        """DNI válido con 8 dígitos"""
        assert validar_dni("12345678") == True
        assert validar_dni("34137129") == True
        assert validar_dni("99999999") == True
    
    def test_dni_invalido_menos_7_digitos(self):
        """DNI inválido con menos de 7 dígitos"""
        assert validar_dni("123456") == False
        assert validar_dni("12345") == False
        assert validar_dni("1") == False
        assert validar_dni("") == False
    
    def test_dni_invalido_mas_8_digitos(self):
        """DNI inválido con más de 8 dígitos"""
        assert validar_dni("123456789") == False
        assert validar_dni("1234567890") == False
        assert validar_dni("123456789012345") == False
    
    def test_dni_con_letras(self):
        """DNI inválido con letras"""
        assert validar_dni("1234567a") == False
        assert validar_dni("abc12345") == False
        assert validar_dni("abcdefgh") == False
        assert validar_dni("12a45678") == False
    
    def test_dni_vacio(self):
        """DNI vacío"""
        assert validar_dni("") == False
    
    def test_dni_con_espacios(self):
        """DNI con espacios"""
        assert validar_dni("123 456 78") == False
        assert validar_dni(" 12345678") == False
        assert validar_dni("12345678 ") == False
        assert validar_dni("1234 5678") == False
    
    def test_dni_caracteres_especiales(self):
        """DNI con caracteres especiales"""
        assert validar_dni("123-4567") == False
        assert validar_dni("12.345.678") == False
        assert validar_dni("12,345,678") == False
        assert validar_dni("12345678!") == False


# ========== TESTS PARA validar_fecha (función estática pura) ==========

class TestValidarFecha:
    """Tests para la validación de fechas"""
    
    def test_fecha_valida_formato_correcto(self):
        """Fechas válidas en formato YYYY-MM-DD"""
        assert validar_fecha("2025-11-04") == True
        assert validar_fecha("2025-01-01") == True
        assert validar_fecha("2025-12-31") == True
    
    def test_fecha_invalida_formato_incorrecto(self):
        """Fechas con formato incorrecto"""
        assert validar_fecha("04-11-2025") == False
        assert validar_fecha("2025/11/04") == False
        assert validar_fecha("2025.11.04") == False
        assert validar_fecha("04/11/2025") == False
    
    def test_fecha_invalida_valores_incorrectos(self):
        """Fechas con valores imposibles"""
        assert validar_fecha("2025-13-01") == False  # Mes 13
        assert validar_fecha("2025-00-01") == False  # Mes 0
        assert validar_fecha("2025-02-30") == False  # 30 de febrero
        assert validar_fecha("2025-04-31") == False  # 31 de abril
    
    def test_fecha_vacia(self):
        """Fecha vacía"""
        assert validar_fecha("") == False
    
    def test_fecha_incompleta(self):
        """Fechas incompletas"""
        assert validar_fecha("2025-11") == False
        assert validar_fecha("2025") == False
        assert validar_fecha("11-04") == False


# ========== TESTS PARA validar_hora (función estática pura) ==========

class TestValidarHora:
    """Tests para la validación de horas"""
    
    def test_hora_valida_formato_correcto(self):
        """Horas válidas en formato HH:mm"""
        assert validar_hora("00:00") == True
        assert validar_hora("12:30") == True
        assert validar_hora("23:59") == True
        assert validar_hora("08:15") == True
    
    def test_hora_invalida_formato_incorrecto(self):
        """Horas con formato incorrecto"""
        assert validar_hora("8:15") == False    # Sin 0 adelante
        assert validar_hora("08:5") == False    # Sin 0 en minutos
        assert validar_hora("8:5") == False     # Sin 0 en ambos
        assert validar_hora("12-30") == False   # Separador incorrecto
        assert validar_hora("12.30") == False   # Separador incorrecto
    
    def test_hora_invalida_valores_incorrectos(self):
        """Horas con valores imposibles"""
        assert validar_hora("24:00") == False   # Hora 24
        assert validar_hora("25:00") == False   # Hora > 23
        assert validar_hora("12:60") == False   # Minutos 60
        assert validar_hora("12:99") == False   # Minutos > 59
    
    def test_hora_vacia(self):
        """Hora vacía"""
        assert validar_hora("") == False
    
    def test_hora_incompleta(self):
        """Horas incompletas"""
        assert validar_hora("12:") == False
        assert validar_hora(":30") == False
        assert validar_hora("12") == False


# ========== TESTS PARA cargar_clientes (función estática I/O) ==========

class TestCargarClientes:
    """Tests para la carga de clientes desde JSON"""
    
    @pytest.fixture
    def archivo_temporal(self, tmp_path):
        """Crea un archivo temporal para tests"""
        archivo = tmp_path / "clientes_test.json"
        # Guardar la ruta original
        import storage
        self.clientes_json_original = storage.CLIENTES_JSON
        # Usar archivo temporal
        storage.CLIENTES_JSON = str(archivo)
        yield archivo
        # Restaurar ruta original
        storage.CLIENTES_JSON = self.clientes_json_original
    
    def test_cargar_archivo_valido(self, archivo_temporal):
        """Cargar desde archivo JSON válido"""
        datos = {
            "12345678": {
                "dni": "12345678",
                "nombre": "Juan",
                "apellido": "Pérez",
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
    
    def test_cargar_archivo_vacio(self, archivo_temporal):
        """Cargar desde archivo vacío"""
        archivo_temporal.write_text("")
        
        resultado = cargar_clientes()
        assert resultado == {}
        assert len(resultado) == 0
    
    def test_cargar_archivo_inexistente(self, tmp_path):
        """Cargar cuando el archivo no existe"""
        import storage
        storage.CLIENTES_JSON = str(tmp_path / "no_existe.json")
        
        resultado = cargar_clientes()
        assert resultado == {}
    
    def test_cargar_json_malformado(self, archivo_temporal, capsys):
        """Cargar desde JSON malformado"""
        archivo_temporal.write_text("{invalid json content")
        
        resultado = cargar_clientes()
        assert resultado == {}
        
        # Verificar que se imprimió mensaje de error
        captured = capsys.readouterr()
        assert "Error al cargar clientes" in captured.out
    
    def test_cargar_diccionario_vacio(self, archivo_temporal):
        """Cargar diccionario vacío válido"""
        archivo_temporal.write_text("{}")
        
        resultado = cargar_clientes()
        assert resultado == {}
    
    def test_cargar_multiples_clientes(self, archivo_temporal):
        """Cargar múltiples clientes"""
        datos = {
            "11111111": {
                "dni": "11111111", 
                "nombre": "Ana", 
                "apellido": "García", 
                "email": "ana@test.com", 
                "telefono": "111111", 
                "activo": True
            },
            "22222222": {
                "dni": "22222222", 
                "nombre": "Carlos", 
                "apellido": "López", 
                "email": "carlos@test.com", 
                "telefono": "222222", 
                "activo": False
            }
        }
        archivo_temporal.write_text(json.dumps(datos, ensure_ascii=False))
        
        resultado = cargar_clientes()
        assert len(resultado) == 2
        assert "11111111" in resultado
        assert "22222222" in resultado
        assert resultado["11111111"]["nombre"] == "Ana"
        assert resultado["22222222"]["activo"] == False
    
    def test_cargar_cliente_con_caracteres_especiales(self, archivo_temporal):
        """Cargar cliente con caracteres especiales (español)"""
        datos = {
            "34137129": {
                "dni": "34137129",
                "nombre": "José",
                "apellido": "Núñez",
                "email": "jose@mail.com",
                "telefono": "123",
                "activo": True
            }
        }
        archivo_temporal.write_text(json.dumps(datos, ensure_ascii=False))
        
        resultado = cargar_clientes()
        assert resultado["34137129"]["nombre"] == "José"
        assert resultado["34137129"]["apellido"] == "Núñez"


# ========== TESTS PARA guardar_clientes (función estática I/O) ==========

class TestGuardarClientes:
    """Tests para guardar clientes en JSON"""
    
    @pytest.fixture
    def archivo_temporal(self, tmp_path):
        """Crea un archivo temporal para tests"""
        archivo = tmp_path / "clientes_test.json"
        import storage
        self.clientes_json_original = storage.CLIENTES_JSON
        storage.CLIENTES_JSON = str(archivo)
        yield archivo
        storage.CLIENTES_JSON = self.clientes_json_original
    
    def test_guardar_diccionario_vacio(self, archivo_temporal):
        """Guardar diccionario vacío"""
        resultado = guardar_clientes({})
        
        assert resultado == True
        assert archivo_temporal.exists()
        contenido = json.loads(archivo_temporal.read_text())
        assert contenido == {}
    
    def test_guardar_un_cliente(self, archivo_temporal):
        """Guardar un cliente"""
        cliente = {
            "12345678": {
                "dni": "12345678",
                "nombre": "María",
                "apellido": "González",
                "email": "maria@test.com",
                "telefono": "987654",
                "activo": True
            }
        }
        
        resultado = guardar_clientes(cliente)
        
        assert resultado == True
        contenido = json.loads(archivo_temporal.read_text())
        assert contenido == cliente
        assert contenido["12345678"]["nombre"] == "María"
    
    def test_guardar_multiples_clientes(self, archivo_temporal):
        """Guardar múltiples clientes"""
        clientes = {
            "11111111": {
                "dni": "11111111", 
                "nombre": "Pedro", 
                "apellido": "Ruiz",
                "email": "pedro@test.com", 
                "telefono": "111", 
                "activo": True
            },
            "22222222": {
                "dni": "22222222", 
                "nombre": "Laura", 
                "apellido": "Díaz",
                "email": "laura@test.com", 
                "telefono": "222", 
                "activo": True
            }
        }
        
        resultado = guardar_clientes(clientes)
        
        assert resultado == True
        contenido = json.loads(archivo_temporal.read_text())
        assert len(contenido) == 2
        assert "11111111" in contenido
        assert "22222222" in contenido
    
    def test_guardar_formato_json_correcto(self, archivo_temporal):
        """Verificar que el JSON guardado tiene formato correcto"""
        cliente = {
            "34137129": {
                "dni": "34137129",
                "nombre": "Walter",
                "apellido": "Navarrete",
                "email": "walter@gmail.com",
                "telefono": "1137588933",
                "activo": True
            }
        }
        
        guardar_clientes(cliente)
        
        # Verificar que se puede leer correctamente
        with open(archivo_temporal, 'r', encoding='utf-8') as f:
            contenido = json.load(f)
        
        assert contenido == cliente
        # Verificar caracteres especiales (español)
        assert "walter@gmail.com" in archivo_temporal.read_text()
    
    def test_guardar_sobrescribe_archivo(self, archivo_temporal):
        """Guardar sobrescribe el archivo existente"""
        # Guardar primer conjunto
        cliente1 = {
            "11111111": {
                "dni": "11111111", 
                "nombre": "Ana", 
                "apellido": "Test",
                "email": "ana@test.com", 
                "telefono": "111", 
                "activo": True
            }
        }
        guardar_clientes(cliente1)
        
        # Guardar segundo conjunto (sobrescribe)
        cliente2 = {
            "22222222": {
                "dni": "22222222", 
                "nombre": "Carlos", 
                "apellido": "Test2",
                "email": "carlos@test.com", 
                "telefono": "222", 
                "activo": True
            }
        }
        guardar_clientes(cliente2)
        
        # Verificar que solo existe el segundo
        contenido = json.loads(archivo_temporal.read_text())
        assert len(contenido) == 1
        assert "22222222" in contenido
        assert "11111111" not in contenido
    
    def test_guardar_con_caracteres_especiales(self, archivo_temporal):
        """Guardar cliente con caracteres especiales (español)"""
        cliente = {
            "12345678": {
                "dni": "12345678",
                "nombre": "José María",
                "apellido": "Núñez Pérez",
                "email": "jose@ñ.com",
                "telefono": "123",
                "activo": True
            }
        }
        
        resultado = guardar_clientes(cliente)
        
        assert resultado == True
        contenido = json.loads(archivo_temporal.read_text())
        assert contenido["12345678"]["nombre"] == "José María"
        assert contenido["12345678"]["apellido"] == "Núñez Pérez"
    
    def test_guardar_cliente_inactivo(self, archivo_temporal):
        """Guardar cliente con estado inactivo"""
        cliente = {
            "12345678": {
                "dni": "12345678",
                "nombre": "Test",
                "apellido": "Inactivo",
                "email": "",
                "telefono": "",
                "activo": False
            }
        }
        
        guardar_clientes(cliente)
        contenido = json.loads(archivo_temporal.read_text())
        assert contenido["12345678"]["activo"] == False


# ========== TESTS DE INTEGRACIÓN (cargar + guardar) ==========

class TestIntegracionCargaGuardado:
    """Tests de integración entre cargar y guardar"""
    
    @pytest.fixture
    def archivo_temporal(self, tmp_path):
        archivo = tmp_path / "clientes_test.json"
        import storage
        self.clientes_json_original = storage.CLIENTES_JSON
        storage.CLIENTES_JSON = str(archivo)
        yield archivo
        storage.CLIENTES_JSON = self.clientes_json_original
    
    def test_guardar_y_cargar(self, archivo_temporal):
        """Guardar y luego cargar debe retornar los mismos datos"""
        datos_originales = {
            "12345678": {
                "dni": "12345678",
                "nombre": "Test",
                "apellido": "Usuario",
                "email": "test@test.com",
                "telefono": "123456789",
                "activo": True
            }
        }
        
        # Guardar
        guardar_clientes(datos_originales)
        
        # Cargar
        datos_cargados = cargar_clientes()
        
        assert datos_cargados == datos_originales
    
    def test_ciclo_completo_multiple(self, archivo_temporal):
        """Múltiples ciclos de guardar y cargar"""
        for i in range(3):
            datos = {
                f"1234567{i}": {
                    "dni": f"1234567{i}",
                    "nombre": f"Usuario{i}",
                    "apellido": f"Test{i}",
                    "email": f"user{i}@test.com",
                    "telefono": f"12345{i}",
                    "activo": True
                }
            }
            guardar_clientes(datos)
            cargados = cargar_clientes()
            assert cargados == datos
    
    def test_modificar_cliente_guardado(self, archivo_temporal):
        """Guardar, cargar, modificar y volver a guardar"""
        # Guardar cliente inicial
        cliente_inicial = {
            "12345678": {
                "dni": "12345678",
                "nombre": "Original",
                "apellido": "Apellido",
                "email": "original@test.com",
                "telefono": "111",
                "activo": True
            }
        }
        guardar_clientes(cliente_inicial)
        
        # Cargar
        clientes = cargar_clientes()
        
        # Modificar
        clientes["12345678"]["nombre"] = "Modificado"
        clientes["12345678"]["email"] = "modificado@test.com"
        
        # Guardar modificación
        guardar_clientes(clientes)
        
        # Cargar y verificar
        clientes_finales = cargar_clientes()
        assert clientes_finales["12345678"]["nombre"] == "Modificado"
        assert clientes_finales["12345678"]["email"] == "modificado@test.com"
    
    def test_agregar_cliente_a_existentes(self, archivo_temporal):
        """Agregar un cliente a un conjunto existente"""
        # Guardar cliente inicial
        clientes = {
            "11111111": {
                "dni": "11111111",
                "nombre": "Primero",
                "apellido": "Cliente",
                "email": "",
                "telefono": "",
                "activo": True
            }
        }
        guardar_clientes(clientes)
        
        # Cargar y agregar nuevo
        clientes = cargar_clientes()
        clientes["22222222"] = {
            "dni": "22222222",
            "nombre": "Segundo",
            "apellido": "Cliente",
            "email": "",
            "telefono": "",
            "activo": True
        }
        guardar_clientes(clientes)
        
        # Verificar
        clientes_finales = cargar_clientes()
        assert len(clientes_finales) == 2
        assert "11111111" in clientes_finales
        assert "22222222" in clientes_finales


# ========== CONFIGURACIÓN DE PYTEST ==========

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
