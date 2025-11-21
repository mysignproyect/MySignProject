"""
Modelos de datos (schemas) usando Pydantic para validación automática.

Define las estructuras de datos para servicios, intérpretes y respuestas
de la API. Pydantic se encarga de:
- Validación automática de tipos
- Serialización/deserialización JSON
- Generación de documentación OpenAPI
"""

from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Dict


class Servicio(BaseModel):
    """
    Modelo de datos para servicios accesibles (salud, educación, gobierno).

    Representa instituciones y lugares que ofrecen servicios a la
    comunidad sorda de Medellín, con información sobre accesibilidad
    y disponibilidad de intérpretes LSC.
    """

    # Identificación
    id: str = Field(..., description="Identificador único del servicio")
    nombre: str = Field(..., description="Nombre del servicio o institución")

    # Clasificación
    categoria: Literal["Salud", "Educación", "Gobierno"] = Field(
        ..., description="Categoría principal del servicio"
    )
    subcategoria: str = Field(
        ..., description="Tipo específico (ej: Hospital, Clínica, Universidad)"
    )

    # Ubicación y contacto
    direccion: str = Field(..., description="Dirección completa del servicio")
    telefono: str = Field(..., description="Número de teléfono de contacto")
    whatsapp: Optional[str] = Field(None, description="Número de WhatsApp (opcional)")
    zona: Literal["Centro", "Norte", "Sur", "Oriente", "Occidente"] = Field(
        ..., description="Zona geográfica de Medellín"
    )

    # Accesibilidad
    caracteristicas_accesibilidad: List[str] = Field(
        ...,
        description="Lista de características de accesibilidad (rampas, ascensores, etc.)",
    )
    horarios: str = Field(..., description="Horarios de atención al público")
    tiene_interprete_lsc: bool = Field(
        ..., description="Indica si hay intérprete LSC disponible"
    )

    # Información adicional
    distancia_aproximada: Optional[float] = Field(
        None, description="Distancia estimada al usuario en kilómetros (opcional)"
    )

    class Config:
        """Configuración de Pydantic para este modelo"""

        json_schema_extra = {
            "example": {
                "id": "srv-001",
                "nombre": "Hospital Central",
                "categoria": "Salud",
                "subcategoria": "Hospital Público",
                "direccion": "Cra 10 #20-30, Medellín",
                "telefono": "6041234567",
                "whatsapp": "3001234567",
                "zona": "Centro",
                "caracteristicas_accesibilidad": [
                    "Rampas",
                    "Ascensor",
                    "Baños adaptados",
                ],
                "horarios": "Lunes a viernes 8:00-17:00",
                "tiene_interprete_lsc": True,
                "distancia_aproximada": 2.5,
            }
        }


class Interprete(BaseModel):
    """
    Modelo de datos para Intérprete de Lengua de Señas Colombiana (LSC).

    Representa profesionales certificados en interpretación LSC,
    con información sobre especialidades, cobertura geográfica y contacto.

    Nota: No incluye tarifas para simplificar el MVP. El enfoque es
    conectar usuarios con intérpretes, no gestionar pagos.
    """

    # Identificación
    id: str = Field(..., description="Identificador único del intérprete")
    nombre: str = Field(..., description="Nombre completo del intérprete")
    foto: Optional[str] = Field(None, description="URL de foto de perfil (opcional)")

    # Especialización y cobertura
    especialidades: List[str] = Field(
        ...,
        description="Áreas de especialidad: Médica, Legal, Educativa, Empresarial, Eventos",
    )
    zonas_cobertura: List[str] = Field(
        ..., description="Zonas geográficas donde ofrece servicios"
    )
    disponibilidad: str = Field(
        ..., description="Horario general de disponibilidad del intérprete"
    )

    # Experiencia y certificación
    años_experiencia: int = Field(
        ...,
        alias="anios_experiencia",
        description="Años de experiencia como intérprete LSC",
    )
    certificaciones: List[str] = Field(
        ..., description="Certificaciones y cursos relevantes en interpretación LSC"
    )

    # Contacto
    telefono: str = Field(..., description="Teléfono de contacto")
    whatsapp: str = Field(..., description="Número de WhatsApp (obligatorio)")
    email: str = Field(..., description="Correo electrónico")

    class Config:
        """Configuración de Pydantic para este modelo"""

        populate_by_name = True  # Permite usar 'años_experiencia' o 'anios_experiencia'
        json_schema_extra = {
            "example": {
                "id": "int-001",
                "nombre": "Laura Gómez",
                "foto": "https://ejemplo.com/fotos/laura.jpg",
                "especialidades": ["Médica", "Educativa"],
                "zonas_cobertura": ["Centro", "Norte"],
                "disponibilidad": "Lunes a viernes 9:00-18:00",
                "anios_experiencia": 5,
                "certificaciones": [
                    "Certificado LSC Nivel 3",
                    "Curso de ética profesional",
                ],
                "telefono": "6047654321",
                "whatsapp": "3107654321",
                "email": "laura.gomez@example.com",
            }
        }


class EstadisticasResponse(BaseModel):
    """
    Modelo de respuesta para el endpoint de estadísticas generales.

    Proporciona un resumen cuantitativo de los recursos disponibles
    en el sistema: servicios, intérpretes, categorías y zonas.

    Utilizado por el frontend para mostrar información general
    del sistema y métricas de disponibilidad.
    """

    # Estadísticas de servicios
    total_servicios: int = Field(
        ..., description="Cantidad total de servicios disponibles"
    )
    servicios_por_categoria: Dict[str, int] = Field(
        ..., description="Diccionario con conteo de servicios por cada categoría"
    )

    # Estadísticas de intérpretes
    total_interpretes: int = Field(
        ..., description="Cantidad total de intérpretes LSC disponibles"
    )
    interpretes_por_especialidad: Dict[str, int] = Field(
        ..., description="Diccionario con conteo de intérpretes por especialidad"
    )

    # Información geográfica
    zonas_disponibles: List[str] = Field(
        ..., description="Lista de zonas geográficas de Medellín cubiertas"
    )

    class Config:
        """Configuración de Pydantic para este modelo"""

        json_schema_extra = {
            "example": {
                "total_servicios": 18,
                "servicios_por_categoria": {
                    "Salud": 6,
                    "Educación": 6,
                    "Gobierno": 4,
                    "Comercio": 1,
                    "Cultura": 1,
                },
                "total_interpretes": 7,
                "interpretes_por_especialidad": {
                    "Médica": 3,
                    "Legal": 3,
                    "Educativa": 4,
                    "Empresarial": 3,
                    "Eventos": 2,
                },
                "zonas_disponibles": ["Centro", "Norte", "Sur", "Oriente", "Occidente"],
            }
        }
