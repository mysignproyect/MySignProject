from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from typing import List, Literal, Optional, Dict  


class Servicio(BaseModel):

    # Identificador único del servicio (puede ser UUID o un string simple)
    id: str = Field(..., description="Identificador único del servicio")

    # Nombre del servicio, por ejemplo: "Hospital San José"
    nombre: str = Field(..., description="Nombre del servicio o institución")

    # Categoría general del servicio (solo acepta valores predefinidos)
    categoria: Literal["Salud", "Educación", "Gobierno"] = Field(
        ..., description="Categoría principal del servicio"
    )

    # Subcategoría más específica, por ejemplo: "Clínica privada" o "Universidad pública"
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
# ============================================================================
# MODELOS DE RESPUESTA PARA ENDPOINTS ESPECIALES
# ============================================================================

class EstadisticasResponse(BaseModel):
    """
    Modelo de respuesta para el endpoint de estadísticas generales.
    
    Proporciona un resumen cuantitativo de los recursos disponibles en el sistema:
    servicios, intérpretes, categorías y zonas.
    """
    
    # Total de servicios registrados en el sistema
    total_servicios: int = Field(..., description="Cantidad total de servicios disponibles")
    
    # Distribución de servicios por categoría
    servicios_por_categoria: Dict[str, int] = Field(
        ...,
        description="Diccionario con el conteo de servicios por cada categoría"
    )
    
    # Total de intérpretes LSC registrados
    total_interpretes: int = Field(..., description="Cantidad total de intérpretes LSC disponibles")
    
    # Distribución de intérpretes por especialidad
    interpretes_por_especialidad: Dict[str, int] = Field(
        ...,
        description="Diccionario con el conteo de intérpretes por cada especialidad"
    )
    
    # Lista de zonas geográficas disponibles
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