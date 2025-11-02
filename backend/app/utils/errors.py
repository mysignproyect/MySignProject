"""
Manejo personalizado de errores para la API My Sign.

Define excepciones personalizadas y funciones helper para formatear
respuestas de error consistentes en español para accesibilidad.
"""

from typing import Dict, Any, Optional


# ============================================================================
# EXCEPCIONES PERSONALIZADAS
# ============================================================================

class RecursoNoEncontrado(Exception):
    """
    Excepción lanzada cuando un recurso solicitado no existe.
    
    Uso: Cuando se busca un servicio, intérprete o categoría por ID y no existe.
    Código HTTP sugerido: 404
    """
    pass


class ParametroInvalido(Exception):
    """
    Excepción lanzada cuando un parámetro no cumple con los valores válidos.
    
    Uso: Cuando una zona, especialidad, tipo de disponibilidad no es válido.
    Código HTTP sugerido: 400
    """
    pass


class ErrorValidacion(Exception):
    """
    Excepción lanzada cuando los datos de entrada no pasan validación.
    
    Uso: Cuando los query params tienen formato incorrecto o valores fuera de rango.
    Código HTTP sugerido: 422
    """
    pass


# ============================================================================
# FUNCIONES HELPER PARA FORMATEAR ERRORES
# ============================================================================

def formato_error_response(
    tipo: str,
    mensaje: str,
    detalles: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Formatea una respuesta de error de manera consistente.
    
    Args:
        tipo: Tipo de error (ej: "RecursoNoEncontrado", "ParametroInvalido")
        mensaje: Mensaje descriptivo del error en español
        detalles: Información adicional sobre el error (opcional)
    
    Returns:
        Diccionario con estructura consistente de error
    
    Ejemplo:
        >>> formato_error_response(
        ...     "ParametroInvalido",
        ...     "La zona 'Noreste' no es válida",
        ...     {"zonas_validas": ["Centro", "Norte", "Sur"]}
        ... )
        {
            "error": "ParametroInvalido",
            "mensaje": "La zona 'Noreste' no es válida",
            "detalles": {"zonas_validas": ["Centro", "Norte", "Sur"]}
        }
    """
    response = {
        "error": tipo,
        "mensaje": mensaje
    }
    
    # Agregar detalles solo si existen
    if detalles:
        response["detalles"] = detalles
    
    return response