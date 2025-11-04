from pydantic import BaseModel, Field
from typing import List, Literal, Optional


class Servicio(BaseModel):

    # Identificador único del servicio (puede ser UUID o un string simple)
    id: str = Field(..., description="Identificador único del servicio")

    # Nombre del servicio, por ejemplo: "Hospital San José"
    nombre: str = Field(..., description="Nombre del servicio o institución")

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