import pytest
from app.utils.errors import *


def test_recurso_no_encontrado_raise():
    with pytest.raises(RecursoNoEncontrado) as exc:
        raise RecursoNoEncontrado("Servicio no encontrado")
    assert "Servicio no encontrado" in str(exc.value)


def test_parametro_invalido_raise():
    with pytest.raises(ParametroInvalido) as exc:
        raise ParametroInvalido("Zona no válida")
    assert "Zona no válida" in str(exc.value)


def test_error_validacion_raise():
    with pytest.raises(ErrorValidacion) as exc:
        raise ErrorValidacion("Formato incorrecto")
    assert "Formato incorrecto" in str(exc.value)


def test_formato_error_response_basico():
    resultado = formato_error_response("ParametroInvalido", "Zona no válida")
    assert resultado == {"error": "ParametroInvalido", "mensaje": "Zona no válida"}


def test_formato_error_response_con_detalles():
    detalles = {"zonas_validas": ["Centro", "Norte", "Sur"]}
    resultado = formato_error_response(
        "ParametroInvalido", "Zona 'Noreste' no es válida", detalles
    )
    assert "detalles" in resultado
    assert resultado["detalles"]["zonas_validas"] == ["Centro", "Norte", "Sur"]


def test_formato_error_response_tipo_y_mensaje():
    resultado = formato_error_response("ErrorValidacion", "Datos inválidos")
    assert resultado["error"] == "ErrorValidacion"
    assert resultado["mensaje"] == "Datos inválidos"


def test_formato_error_response_detalles_none():
    resultado = formato_error_response(
        "RecursoNoEncontrado", "No existe el ID solicitado", None
    )
    assert "detalles" not in resultado
