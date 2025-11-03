import pytest
from pydantic import ValidationError
from app.models.schemas import *

def test_servicio_valido():
    servicio = Servicio(
        id="srv-001",
        nombre="Hospital Central",
        categoria="Salud",
        subcategoria="Hospital Público",
        direccion="Cra 10 #20-30",
        telefono="6041234567",
        whatsapp="3001234567",
        zona="Centro",
        caracteristicas_accesibilidad=["Rampas", "Ascensor"],
        horarios="Lunes a viernes 8:00-17:00",
        tiene_interprete_lsc=True,
        distancia_aproximada=2.5
    )
    assert servicio.categoria == "Salud"
    assert servicio.tiene_interprete_lsc is True


def test_servicio_categoria_invalida():
    with pytest.raises(ValidationError):
        Servicio(
            id="srv-002",
            nombre="Servicio X",
            categoria="Transporte",
            subcategoria="Taxi",
            direccion="Calle 1 #2-3",
            telefono="1234567",
            zona="Norte",
            caracteristicas_accesibilidad=[],
            horarios="8:00-17:00",
            tiene_interprete_lsc=False
        )


def test_servicio_zona_invalida():
    """Debe fallar si la zona no pertenece a las opciones definidas."""
    with pytest.raises(ValidationError):
        Servicio(
            id="srv-003",
            nombre="Hospital Sur",
            categoria="Salud",
            subcategoria="Hospital Público",
            direccion="Calle 1 #2-3",
            telefono="1234567",
            zona="Desconocida",
            caracteristicas_accesibilidad=[],
            horarios="8:00-17:00",
            tiene_interprete_lsc=False
        )


def test_servicio_opcional_sin_whatsapp():
    """Debe permitir crear un servicio sin WhatsApp."""
    servicio = Servicio(
        id="srv-004",
        nombre="Hospital Norte",
        categoria="Salud",
        subcategoria="Hospital Privado",
        direccion="Cra 12 #4-5",
        telefono="6048888888",
        zona="Norte",
        caracteristicas_accesibilidad=["Rampas"],
        horarios="8:00-17:00",
        tiene_interprete_lsc=False
    )
    assert servicio.whatsapp is None


def test_interprete_valido():
    interprete = Interprete(
        id="int-001",
        nombre="Laura Gómez",
        especialidades=["Médica", "Educativa"],
        zonas_cobertura=["Centro", "Norte"],
        disponibilidad="Lunes a viernes 9:00-18:00",
        anios_experiencia=5,
        certificaciones=["Certificado LSC Nivel 3"],
        telefono="6047654321",
        whatsapp="3107654321",
        email="laura@example.com"
    )
    assert interprete.años_experiencia == 5


def test_interprete_falta_campo_obligatorio():
    with pytest.raises(ValidationError):
        Interprete(
            id="int-002",
            nombre="Carlos Ruiz",
            especialidades=["Médica"],
            zonas_cobertura=["Sur"],
            disponibilidad="Lunes a viernes 9:00-18:00",
            anios_experiencia=3,
            certificaciones=["Certificado LSC Nivel 2"],
            whatsapp="3110000000",
            email="carlos@example.com"
        )

def test_estadisticas_response_valido():
    data = EstadisticasResponse(
        total_servicios=10,
        servicios_por_categoria={"Salud": 3, "Educación": 2},
        total_interpretes=4,
        interpretes_por_especialidad={"Médica": 2, "Educativa": 2},
        zonas_disponibles=["Centro", "Norte"]
    )
    assert data.total_servicios == 10
    assert "Salud" in data.servicios_por_categoria


def test_estadisticas_response_error_tipo():
    with pytest.raises(ValidationError):
        EstadisticasResponse(
            total_servicios="diez",
            servicios_por_categoria={"Salud": 3},
            total_interpretes=4,
            interpretes_por_especialidad={"Médica": 2},
            zonas_disponibles=["Centro"]
        )
