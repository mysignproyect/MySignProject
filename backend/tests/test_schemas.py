import pytest
from pydantic import ValidationError
from app.models.schemas import *


def test_servicio_valido():
    """
    Verifica la creación exitosa de un modelo 'Servicio' con todos los campos válidos.
    """
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
        distancia_aproximada=2.5,
    )
    assert servicio.categoria == "Salud"
    assert servicio.tiene_interprete_lsc is True


def test_servicio_categoria_invalida():
    """
    Comprueba que la validación falle al intentar crear un Servicio con una categoría no permitida.
    """
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
            tiene_interprete_lsc=False,
        )


def test_servicio_zona_invalida():
    """
    Verifica que la validación falle si el valor del campo 'zona' no pertenece a las opciones definidas.
    """
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
            tiene_interprete_lsc=False,
        )


def test_servicio_opcional_sin_whatsapp():
    """
    Asegura que el modelo 'Servicio' se pueda crear correctamente si se omite el campo opcional 'whatsapp'.
    """
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
        tiene_interprete_lsc=False,
    )
    assert servicio.whatsapp is None


def test_interprete_valido():
    """
    Verifica la creación exitosa de un modelo 'Interprete' con todos los campos válidos.
    """
    interprete = Interprete(
        id="int-001",
        nombre="Laura Gómez",
        especialidades=["Médica", "Educativa"],
        zonas_cobertura=["Centro", "Norte"],
        disponibilidad="Lunes a viernes 9:00-18:00",
        años_experiencia=5,
        certificaciones=["Certificado LSC Nivel 3"],
        telefono="6047654321",
        whatsapp="3107654321",
        email="laura@example.com",
    )
    assert interprete.años_experiencia == 5


def test_interprete_falta_campo_obligatorio():
    """
    Comprueba que falle la creación de 'Interprete' si falta un campo requerido (como 'telefono').
    """
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
            email="carlos@example.com",
        )


def test_estadisticas_response_valido():
    """
    Verifica la creación exitosa del esquema de respuesta 'EstadisticasResponse'.
    """
    data = EstadisticasResponse(
        total_servicios=10,
        servicios_por_categoria={"Salud": 3, "Educación": 2},
        total_interpretes=4,
        interpretes_por_especialidad={"Médica": 2, "Educativa": 2},
        zonas_disponibles=["Centro", "Norte"],
    )
    assert data.total_servicios == 10
    assert "Salud" in data.servicios_por_categoria


def test_estadisticas_response_error_tipo():
    """
    Comprueba que 'EstadisticasResponse' falle si se pasa un tipo de dato incorrecto (string en lugar de int).
    """
    with pytest.raises(ValidationError):
        EstadisticasResponse(
            total_servicios="diez",
            servicios_por_categoria={"Salud": 3},
            total_interpretes=4,
            interpretes_por_especialidad={"Médica": 2},
            zonas_disponibles=["Centro"],
        )

def test_servicio_telefono_invalido():
    """
    Verifica que falle la creación de 'Servicio' si el campo 'telefono' no cumple con el formato o tipo esperado.
    """
    with pytest.raises(ValidationError):
        Servicio(
            id="srv-010",
            nombre="Servicio X",
            categoria="Salud",
            subcategoria="Hospital",
            direccion="Calle 1",
            telefono="604-ABC",
            zona="Centro",
            caracteristicas_accesibilidad=[],
            horarios="8-5",
            tiene_interprete_lsc=False,
        )

def test_servicio_tiene_caracteristica():
    """
    Prueba el método de instancia 'tiene_caracteristica' para buscar una característica de accesibilidad.
    """
    servicio = Servicio(
        id="srv-012",
        nombre="Servicio Z",
        categoria="Gobierno",
        subcategoria="Oficina",
        direccion="Calle 3",
        telefono="6042222222",
        zona="Sur",
        caracteristicas_accesibilidad=["Rampas", "Baños"],
        horarios="8-5",
        tiene_interprete_lsc=True,
    )
    assert servicio.tiene_caracteristica("rampa") is True
    assert servicio.tiene_caracteristica("ascensor") is False

def test_servicio_coincide_con_texto():
    """
    Prueba el método 'coincide_con_texto' para verificar coincidencias en múltiples campos del servicio.
    """
    servicio = Servicio(
        id="srv-013",
        nombre="Biblioteca Central",
        categoria="Educación",
        subcategoria="Biblioteca",
        direccion="Cra 1",
        telefono="6043333333",
        zona="Centro",
        caracteristicas_accesibilidad=["Ascensor"],
        horarios="8-5",
        tiene_interprete_lsc=False,
    )
    assert servicio.coincide_con_texto("biblioteca") is True
    assert servicio.coincide_con_texto("Cra 1") is True
    assert servicio.coincide_con_texto("Sur") is False


def test_servicio_obtener_contacto():
    """
    Verifica que el método 'obtener_contacto' retorne el teléfono y WhatsApp del servicio.
    """
    servicio = Servicio(
        id="srv-014",
        nombre="Servicio",
        categoria="Salud",
        subcategoria="Hospital",
        direccion="Cra 10",
        telefono="6044567890",
        whatsapp="3001234567",
        zona="Centro",
        caracteristicas_accesibilidad=[],
        horarios="8-5",
        tiene_interprete_lsc=True,
    )
    contacto = servicio.obtener_contacto()
    assert contacto["telefono"] == "6044567890"
    assert contacto["whatsapp"] == "3001234567"

def test_servicio_es_cercano():
    """
    Prueba el método 'es_cercano' para verificar si la distancia actual es menor o igual a un límite dado.
    """
    servicio = Servicio(
        id="srv-015",
        nombre="Servicio",
        categoria="Salud",
        subcategoria="Hospital",
        direccion="Cra 10",
        telefono="6041234567",
        zona="Centro",
        caracteristicas_accesibilidad=[],
        horarios="8-5",
        tiene_interprete_lsc=True,
        distancia_aproximada=3,
    )
    assert servicio.es_cercano(5) is True 
    assert servicio.es_cercano(2) is False

def test_interprete_email_invalido():
    """
    Comprueba que el modelo 'Interprete' falle si el campo 'email' no tiene un formato de correo válido.
    """
    with pytest.raises(ValidationError):
        Interprete(
            id="int-010",
            nombre="Marta",
            especialidades=["Médica"],
            zonas_cobertura=["Centro"],
            disponibilidad="9-5",
            anios_experiencia=2,
            certificaciones=["Cert"],
            telefono="6041111111",
            whatsapp="3001111111",
            email="correo-sin-arroba",
        )

def test_interprete_experiencia_negativa():
    """
    Verifica que el modelo 'Interprete' falle si 'anios_experiencia' es un número negativo.
    """
    with pytest.raises(ValidationError):
        Interprete(
            id="int-011",
            nombre="Luis",
            especialidades=["Legal"],
            zonas_cobertura=["Norte"],
            disponibilidad="9-5",
            anios_experiencia=-1,
            certificaciones=["Cert"],
            telefono="6041111111",
            whatsapp="3001111111",
            email="luis@example.com",
        )

def test_interprete_es_experimentado():
    """
    Prueba el método 'es_experimentado' para verificar si el intérprete cumple con un umbral de años de experiencia.
    """
    interprete = Interprete(
        id="int-014",
        nombre="Pedro",
        especialidades=["Médica"],
        zonas_cobertura=["Norte"],
        disponibilidad="9-5",
        anios_experiencia=10,
        certificaciones=["Cert"],
        telefono="6041111111",
        whatsapp="3001111111",
        email="pedro@example.com",
    )
    assert interprete.es_experimentado(5) is True
    assert interprete.es_experimentado(15) is False


def test_interprete_tiene_especialidad():
    """
    Prueba el método 'tiene_especialidad' para buscar una especialidad específica.
    """
    interprete = Interprete(
        id="int-012",
        nombre="Ana",
        especialidades=["Eventos", "Legal"],
        zonas_cobertura=["Centro"],
        disponibilidad="9-5",
        anios_experiencia=5,
        certificaciones=["Cert"],
        telefono="6041111111",
        whatsapp="3001111111",
        email="ana@example.com",
    )
    assert interprete.tiene_especialidad("Legal") is True
    assert interprete.tiene_especialidad("Médica") is False

def test_interprete_cubre_zona():
    """
    Prueba el método 'cubre_zona' para verificar si el intérprete trabaja en un área geográfica específica.
    """
    interprete = Interprete(
        id="int-013",
        nombre="Sara",
        especialidades=["Empresarial"],
        zonas_cobertura=["Sur", "Occidente"],
        disponibilidad="9-5",
        anios_experiencia=4,
        certificaciones=["Cert"],
        telefono="6041111111",
        whatsapp="3001111111",
        email="sara@example.com",
    )
    assert interprete.cubre_zona("Sur") is True
    assert interprete.cubre_zona("Norte") is False

def test_interprete_obtener_contacto():
    """
    Verifica que el método 'obtener_contacto' retorne los datos de contacto (teléfono, email) del intérprete.
    """
    interprete = Interprete(
        id="int-015",
        nombre="Leo",
        especialidades=["Eventos"],
        zonas_cobertura=["Centro"],
        disponibilidad="9-5",
        anios_experiencia=3,
        certificaciones=["Cert"],
        telefono="6045555555",
        whatsapp="3005555555",
        email="leo@example.com",
    )
    contacto = interprete.obtener_contacto()
    assert contacto["telefono"] == "6045555555"
    assert contacto["email"] == "leo@example.com"