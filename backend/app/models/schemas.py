from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from typing import List, Literal, Optional, Dict  


class Servicio(BaseModel):

    id: str = Field(..., description="Identificador único del servicio")

    nombre: str = Field(..., description="Nombre del servicio o institución")

    categoria: Literal["Salud", "Educación", "Gobierno"] = Field(
        ..., description="Categoría principal del servicio"
    )

    subcategoria: str = Field(..., description="Tipo o clasificación más específica del servicio")

    direccion: str = Field(..., description="Dirección completa del servicio")

    telefono: str = Field(..., description="Número de teléfono de contacto")

    whatsapp: Optional[str] = Field(None, description="Número de WhatsApp si aplica")

    zona: Literal["Centro", "Norte", "Sur", "Oriente", "Occidente"] = Field(
        ..., description="Zona geográfica de ubicación del servicio"
    )

    caracteristicas_accesibilidad: List[str] = Field(
        ..., description="Lista de características que mejoran la accesibilidad (rampas, ascensor, etc.)"
    )

    horarios: str = Field(..., description="Horarios de atención del servicio")

    tiene_interprete_lsc: bool = Field(..., description="Indica si el servicio cuenta con intérprete LSC")

    distancia_aproximada: Optional[float] = Field(
        None, description="Distancia estimada al usuario en kilómetros (opcional)"
    )

    class Config:
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
    Modelo de datos para Intérprete de Lengua de Señas Colombiana (LSC).
    
    CAMBIO IMPORTANTE (Checkpoint #2):
    - Se eliminó el campo 'tarifa_hora' para simplificar el MVP.
    - El enfoque es conectar usuarios con intérpretes, sin gestión de tarifas en esta versión.
    """

    id: str = Field(..., description="Identificador único del intérprete")

    nombre: str = Field(..., description="Nombre completo del intérprete")

    foto: Optional[str] = Field(None, description="URL de la foto del intérprete (opcional)")

    especialidades: List[str] = Field(
        ..., description="Áreas de especialidad: Médica, Legal, Educativa, Empresarial, Eventos, etc."
    )

    zonas_cobertura: List[str] = Field(
        ..., description="Zonas de cobertura donde el intérprete puede desplazarse"
    )

    disponibilidad: str = Field(..., description="Horario general de disponibilidad del intérprete")

    años_experiencia: int = Field(..., alias="anios_experiencia", description="Años de experiencia como intérprete")

    certificaciones: List[str] = Field(..., description="Certificaciones y cursos relevantes en interpretación LSC")

    telefono: str = Field(..., description="Teléfono de contacto del intérprete")

    whatsapp: str = Field(..., description="Número de WhatsApp del intérprete")

    email: str = Field(..., description="Correo electrónico del intérprete")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "int-001",
                "nombre": "Laura Gómez",
                "foto": "https://ejemplo.com/fotos/laura.jpg",
                "especialidades": ["Médica", "Educativa"],
                "zonas_cobertura": ["Centro", "Norte"],
                "disponibilidad": "Lunes a viernes 9:00-18:00",
                "anios_experiencia": 5,
                "certificaciones": ["Certificado LSC Nivel 3", "Curso de ética profesional"],
                "telefono": "6047654321",
                "whatsapp": "3107654321",
                "email": "laura.gomez@example.com"
            }
        }

class EstadisticasResponse(BaseModel):
    total_servicios: int = Field(..., description="Cantidad total de servicios disponibles")
    
    servicios_por_categoria: Dict[str, int] = Field(
        ...,
        description="Diccionario con el conteo de servicios por cada categoría"
    )
    
    total_interpretes: int = Field(..., description="Cantidad total de intérpretes LSC disponibles")
    
    interpretes_por_especialidad: Dict[str, int] = Field(
        ...,
        description="Diccionario con el conteo de intérpretes por cada especialidad"
    )
    
    zonas_disponibles: List[str] = Field(
        ...,
        description="Lista de zonas geográficas de Medellín cubiertas"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_servicios": 10,
                "servicios_por_categoria": {
                    "Salud": 3,
                    "Educación": 3,
                    "Gobierno": 2,
                    "Comercio": 1,
                    "Cultura": 1
                },
                "total_interpretes": 4,
                "interpretes_por_especialidad": {
                    "Médica": 2,
                    "Legal": 2,
                    "Educativa": 3,
                    "Empresarial": 2,
                    "Eventos": 1
                },
                "zonas_disponibles": ["Centro", "Norte", "Sur", "Oriente", "Occidente"]
            }
        }