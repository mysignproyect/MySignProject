from pydantic import BaseModel, Field
from typing import List, Literal, Optional

class Servicio(BaseModel):
    id: str
    nombre: str
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

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1",
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
    id: str
    nombre: str
    foto: Optional[str] = None
    especialidades: List[str]
    zonas_cobertura: List[str]
    disponibilidad: str
    tarifa_hora: float
    años_experiencia: int = Field(..., alias="anios_experiencia")
    certificaciones: List[str]
    telefono: str
    whatsapp: str
    email: str

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "I-001",
                "nombre": "Laura Gómez",
                "foto": "https://ejemplo.com/foto.jpg",
                "especialidades": ["Médica", "Educativa"],
                "zonas_cobertura": ["Centro", "Norte"],
                "disponibilidad": "Lunes a viernes 9:00-18:00",
                "tarifa_hora": 80000.0,
                "anios_experiencia": 5,
                "certificaciones": ["Certificado LSC Nivel 3"],
                "telefono": "6047654321",
                "whatsapp": "3107654321",
                "email": "laura@example.com"
            }
        }
