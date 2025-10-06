"""
Paquete de modelos Pydantic del proyecto My Sign.

Este módulo agrupa las definiciones de los esquemas de datos (schemas)
usados para validar la información que viaja entre la API y los clientes.
"""

from .schemas import Servicio, Interprete

__all__ = ["Servicio", "Interprete"]
