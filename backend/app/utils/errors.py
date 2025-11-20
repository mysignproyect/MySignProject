"""
Manejo personalizado de errores para la API My Sign.

Define excepciones personalizadas y funciones helper para formatear
respuestas de error consistentes en español para mejor accesibilidad.

Todas las excepciones están diseñadas para ser capturadas por los
exception handlers en main.py y convertidas en respuestas HTTP apropiadas.
"""

from typing import Dict, Any, Optional


# ============================================================================
# EXCEPCIONES PERSONALIZADAS
# ============================================================================

class RecursoNoEncontrado(Exception):
    """
    Excepción cuando un recurso solicitado no existe.
    
    Uso típico:
        - Buscar servicio/intérprete por ID que no existe
        - Solicitar categoría que no está en el sistema
    
    Código HTTP sugerido: 404 Not Found
    """
    pass


class ParametroInvalido(Exception):
    """
    Excepción cuando un parámetro no cumple con valores válidos.
    
    Uso típico:
        - Zona no válida (ej: "Noreste" cuando solo existe "Norte")
        - Especialidad no reconocida
        - Tipo de disponibilidad incorrecto
    
    Código HTTP sugerido: 400 Bad Request
    """
    pass


class ErrorValidacion(Exception):
    """
    Excepción cuando los datos de entrada no pasan validación.
    
    Uso típico:
        - Query params con formato incorrecto
        - Valores fuera de rango (page < 1, limit > 50)
        - Campos requeridos faltantes
    
    Código HTTP sugerido: 422 Unprocessable Entity
    """
    pass


# ============================================================================
# FUNCIONES HELPER PARA FORMATEO DE ERRORES
# ============================================================================

def formato_error_response(
    tipo: str,
    mensaje: str,
    detalles: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Formatea una respuesta de error de manera consistente.
    
    Crea un diccionario estandarizado para respuestas de error,
    facilitando el manejo en el frontend y debugging.
    
    Args:
        tipo: Tipo de error (ej: "RecursoNoEncontrado", "ParametroInvalido")
        mensaje: Mensaje descriptivo del error en español
        detalles: Información adicional sobre el error (opcional)
    
    Returns:
        Diccionario con estructura consistente:
        {
            "error": str,      # Tipo de error
            "mensaje": str,    # Descripción legible
            "detalles": dict   # Info adicional (opcional)
        }
    
    Complejidad: O(1) - Solo construye un diccionario simple
    
    Diseño:
        - Respuestas en español para accesibilidad (comunidad sorda)
        - Estructura consistente facilita parsing en frontend
        - Campo "detalles" opcional permite contexto adicional
    """
    response = {
        "error": tipo,
        "mensaje": mensaje
    }
    
    # Agregar detalles solo si existen (mantener respuesta limpia)
    if detalles:
        response["detalles"] = detalles
    
    return response