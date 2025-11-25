"""
Test Unitarios de el Archivo Turnos.py
Hay 10 Funciones con el nombre de Test
"""

import pytest
from turnos import _existe_turno_en_slot, _slot_bloqueado, _cliente_activo, bloquear_slot

# ---------------------------------------------------------
# TEST DE FUNCION _existe_turno_en_slot
# ---------------------------------------------------------
def test_turno_ocupado():
    turnos = []
    #Turno ocupado
    turnos.append({"id": 1, "dni": "12345678", "fecha": "2025-11-10", "hora": "10:00", "estado": "Ocupado"})
    
    assert _existe_turno_en_slot(turnos, "2025-11-10", "10:00") is True

def test_turno_libre():
    turnos = []
    #Turno libre
    turnos.append({"id": 2, "dni": "12345678", "fecha": "2025-11-10", "hora": "11:00", "estado": "Libre"})
    
    assert _existe_turno_en_slot(turnos, "2025-11-10", "11:00") is False

def test_turno_no_existente():
    turnos = []
    #Sin Turnos
    assert _existe_turno_en_slot(turnos, "2025-11-10", "12:00") is False



# ---------------------------------------------------------
# TEST DE FUNCION _cliente_activo
# ---------------------------------------------------------
clientes_test = {
    "12345678": {"activo": True},    # cliente activo
    "87654321": {"activo": False},   # cliente inactivo
}

def test_cliente_activo_true():
    #Cliente Activo
    assert _cliente_activo(clientes_test, "12345678") is True

def test_cliente_activo_false_inactivo():
    # Cliente Inactivo
    assert _cliente_activo(clientes_test, "87654321") is False

def test_cliente_activo_false_no_existe():
    # Cliente no existente
    assert _cliente_activo(clientes_test, "00000000") is False

def test_cliente_activo_false_sin_clave_activo():
    # Cliente existe pero no tiene la clave "activo"
    clientes_extra = {"11111111": {}}
    assert _cliente_activo(clientes_extra, "11111111") is False
