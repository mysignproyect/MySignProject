"""
Módulo: schemas.py
------------------
Contiene los modelos de datos utilizados por la API My Sign,
definidos mediante Pydantic. Estos modelos permiten validar,
estructurar y documentar la información intercambiada entre
el backend y los clientes (frontend, servicios externos, etc.).
"""

from pydantic import BaseModel, Field
from typing import List, Literal, Optional


class Servicio(BaseModel):
    """
    Modelo de datos que representa un servicio accesible en el sistema My Sign.
    Incluye información sobre ubicación, categoría, accesibilidad y disponibilidad
    de intérprete en Lengua de Señas Colombiana (LSC).
    """

    # Identificador único del servicio (puede ser UUID o un string simple)
    id: str = Field(..., description="Identificador único del servicio")

    # Nombre del servicio, por ejemplo: “Hospital San José”
    nombre: str = Field(..., description="Nombre del servicio o institución")

    # Categoría general del servicio (solo acepta valores predefinidos)
    categoria: Literal["Salud", "Educación", "Gobierno"] = Field(
        ..., description="Categoría principal del servicio"
    )

    # Subcategoría más específica, por ejemplo: “Clínica privada” o “Universidad pública”
    subcategoria: str = Field(..., description="Tipo o clasificación más específica del servicio")

    # Dirección física donde se encuentra el servicio
    direccion: str = Field(..., description="Dirección completa del servicio")

    # Número de teléfono principal
    telefono: str = Field(..., description="Número de teléfono de contacto")

    # Número de WhatsApp (opcional, puede no estar disponible)
    whatsapp: Optional[str] = Field(None, description="Número de WhatsApp si aplica")

    # Zona geográfica donde está ubicado el servicio (usada para filtrado)
    zona: Literal["Centro", "Norte", "Sur", "Oriente", "Occidente"] = Field(
        ..., description="Zona geográfica de ubicación del servicio"
    )

    # Lista de características de accesibilidad física o comunicativa
    caracteristicas_accesibilidad: List[str] = Field(
        ..., description="Lista de características que mejoran la accesibilidad (rampas, ascensor, etc.)"
    )

    # Horario de atención al público
    horarios: str = Field(..., description="Horarios de atención del servicio")

    # Indica si hay intérprete de LSC disponible en el sitio
    tiene_interprete_lsc: bool = Field(..., description="Indica si el servicio cuenta con intérprete LSC")

    # Distancia aproximada al usuario (opcional, útil para filtrado por cercanía)
    distancia_aproximada: Optional[float] = Field(
        None, description="Distancia estimada al usuario en kilómetros (opcional)"
    )

    class Config:
        """
        Configuración interna del modelo:
        - json_schema_extra: proporciona un ejemplo para la documentación Swagger.
        """
        json_schema_extra = {
            "example": {
                "id": "srv-001",
                "nombre": "Hospital Central",
                "categoria": "Salud",
                "subcategoria": "Hospital Público",
                "direccion": "Cra 10 #20-30",
                "telefono": "6041234567",
                "whatsapp": "3001234567",
                "zona": "Centro",
                "caracteristicas_accesibilidad": ["Rampas", "Ascensor", "Baños adaptados"],
                "horarios": "Lunes a viernes 8:00-17:00",
                "tiene_interprete_lsc": True,
                "distancia_aproximada": 2.5
            }
        }


class Interprete(BaseModel):
    """
    Modelo de datos que representa un intérprete de Lengua de Señas Colombiana (LSC).
    Almacena información de contacto, especialidades, experiencia y disponibilidad.
    """

    # Identificador único del intérprete (UUID o string)
    id: str = Field(..., description="Identificador único del intérprete")

    # Nombre completo del intérprete
    nombre: str = Field(..., description="Nombre completo del intérprete")

    # URL o ruta de la foto de perfil (opcional)
    foto: Optional[str] = Field(None, description="URL de la foto del intérprete (opcional)")

    # Lista de áreas en las que el intérprete tiene experiencia
    especialidades: List[str] = Field(
        ..., description="Áreas de especialidad: Médica, Legal, Educativa, Empresarial, Eventos, etc."
    )

    # Zonas geográficas en las que el intérprete ofrece sus servicios
    zonas_cobertura: List[str] = Field(
        ..., description="Zonas de cobertura donde el intérprete puede desplazarse"
    )

    # Horario o disponibilidad de atención
    disponibilidad: str = Field(..., description="Horario general de disponibilidad del intérprete")

    # Tarifa por hora en pesos colombianos
    tarifa_hora: float = Field(..., description="Tarifa por hora en COP")

    # Años de experiencia en interpretación LSC
    años_experiencia: int = Field(..., alias="anios_experiencia", description="Años de experiencia como intérprete")

    # Certificaciones académicas o profesionales obtenidas
    certificaciones: List[str] = Field(..., description="Certificaciones y cursos relevantes en interpretación LSC")

    # Número telefónico principal
    telefono: str = Field(..., description="Teléfono de contacto del intérprete")

    # Número de WhatsApp (obligatorio en este caso para contacto rápido)
    whatsapp: str = Field(..., description="Número de WhatsApp del intérprete")

    # Correo electrónico de contacto
    email: str = Field(..., description="Correo electrónico del intérprete")

    class Config:
        """
        Configuración interna del modelo:
        - populate_by_name: permite usar 'anios_experiencia' como alias JSON.
        - json_schema_extra: ejemplo para la documentación Swagger.
        """
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "int-001",
                "nombre": "Laura Gómez",
                "foto": "https://ejemplo.com/fotos/laura.jpg",
                "especialidades": ["Médica", "Educativa"],
                "zonas_cobertura": ["Centro", "Norte"],
                "disponibilidad": "Lunes a viernes 9:00-18:00",
                "tarifa_hora": 85000.0,
                "anios_experiencia": 5,
                "certificaciones": ["Certificado LSC Nivel 3", "Curso de ética profesional"],
                "telefono": "6047654321",
                "whatsapp": "3107654321",
                "email": "laura.gomez@example.com"
            }
        }
