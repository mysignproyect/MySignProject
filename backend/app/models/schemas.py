"""
Modelos de datos (schemas) usando Pydantic para validación automática.

Define las estructuras de datos para servicios, intérpretes y respuestas
de la API. Pydantic se encarga de:
- Validación automática de tipos
- Serialización/deserialización JSON
- Generación de documentación OpenAPI
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Literal, Optional, Dict


class Servicio(BaseModel):
    """
    Modelo de datos para servicios accesibles (salud, educación, gobierno).

    Representa instituciones y lugares que ofrecen servicios a la
    comunidad sorda de Medellín, con información sobre accesibilidad
    y disponibilidad de intérpretes LSC.
    """

    id: str = Field(..., description="Identificador único del servicio")
    nombre: str = Field(..., description="Nombre del servicio o institución")
    categoria: Literal["Salud", "Educación", "Gobierno"]
    subcategoria: str
    direccion: str
    telefono: str
    whatsapp: Optional[str] = None
    zona: Literal["Centro", "Norte", "Sur", "Oriente", "Occidente"]
    caracteristicas_accesibilidad: List[str]
    horarios: str
    tiene_interprete_lsc: bool
    distancia_aproximada: Optional[float] = None
    
    @field_validator('telefono', 'whatsapp')
    @classmethod
    def validar_telefono(cls, v: Optional[str]) -> Optional[str]:
        """Valida formato de teléfono"""
        if v and not v.isdigit():
            raise ValueError('El teléfono debe contener solo números')
        return v
    
    def tiene_caracteristica(self, caracteristica: str) -> bool:
        """
        Verifica si el servicio tiene una característica específica.
        
        Complejidad: O(n) donde n = características
        """
        return any(
            caracteristica.lower() in c.lower() 
            for c in self.caracteristicas_accesibilidad
        )
    
    def coincide_con_texto(self, texto: str) -> bool:
        """
        Verifica si el servicio coincide con un texto de búsqueda.
        
        Complejidad: O(n + m) donde n = campos, m = características
        """
        texto_lower = texto.lower()
        return (
            texto_lower in self.nombre.lower() or
            texto_lower in self.direccion.lower() or
            any(texto_lower in c.lower() for c in self.caracteristicas_accesibilidad)
        )
    
    def obtener_contacto(self) -> Dict[str, str]:
        """Retorna información de contacto del servicio"""
        contacto = {
            "telefono": self.telefono,
            "direccion": self.direccion
        }
        if self.whatsapp:
            contacto["whatsapp"] = self.whatsapp
        return contacto
    
    def es_cercano(self, distancia_maxima: float = 5.0) -> bool:
        """Verifica si el servicio está cerca según distancia"""
        if self.distancia_aproximada is None:
            return False
        return self.distancia_aproximada <= distancia_maxima
    

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
    id: str
    nombre: str
    foto: Optional[str] = None
    especialidades: List[str]
    zonas_cobertura: List[str]
    disponibilidad: str
    años_experiencia: int = Field(..., alias="anios_experiencia")
    certificaciones: List[str]
    telefono: str
    whatsapp: str
    email: str
    
    @field_validator('email')
    @classmethod
    def validar_email(cls, v: str) -> str:
        """Validación básica de email"""
        if '@' not in v:
            raise ValueError('Email inválido')
        return v
    
    @field_validator('años_experiencia')
    @classmethod
    def validar_experiencia(cls, v: int) -> int:
        """Valida años de experiencia"""
        if v < 0:
            raise ValueError('Los años de experiencia no pueden ser negativos')
        return v
    
    def tiene_especialidad(self, especialidad: str) -> bool:
        """Verifica si tiene una especialidad específica"""
        return especialidad in self.especialidades
    
    def cubre_zona(self, zona: str) -> bool:
        """Verifica si cubre una zona específica"""
        return zona in self.zonas_cobertura
    
    def es_experimentado(self, años_minimos: int = 5) -> bool:
        """Verifica si es un intérprete experimentado"""
        return self.años_experiencia >= años_minimos
    
    def obtener_contacto(self) -> Dict[str, str]:
        """Retorna información de contacto"""
        return {
            "telefono": self.telefono,
            "whatsapp": self.whatsapp,
            "email": self.email
        }

    class Config:
        """Configuración de Pydantic para este modelo"""

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
