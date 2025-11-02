"""
Utilidades para paginación de resultados.

Proporciona funciones helper para paginar listas de datos de manera eficiente.
"""

from typing import List, Dict, Any, TypeVar
from math import ceil

T = TypeVar('T')


def paginar_resultados(
    items: List[T],
    page: int = 1,
    limit: int = 10
) -> Dict[str, Any]:
    """
    Pagina una lista de items y retorna los datos con metadata de paginación.
    
    Args:
        items: Lista completa de elementos a paginar
        page: Número de página (debe ser >= 1)
        limit: Cantidad de items por página (debe ser > 0 y <= 50)
    
    Returns:
        Diccionario con:
        - data: Lista paginada de items
        - metadata: Información de paginación
    
    Raises:
        ValueError: Si page < 1 o limit no está en rango válido
    
    Complejidad temporal:
        O(1) para calcular índices + O(k) para slice donde k = limit
    
    Ejemplo:
        >>> items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        >>> resultado = paginar_resultados(items, page=2, limit=3)
        >>> resultado['data']
        [4, 5, 6]
        >>> resultado['metadata']['current_page']
        2
    """
    # Validaciones
    if page < 1:
        raise ValueError("El número de página debe ser mayor o igual a 1")
    
    if limit < 1 or limit > 50:
        raise ValueError("El límite debe estar entre 1 y 50")
    
    # Calcular totales
    total_items = len(items)
    total_pages = ceil(total_items / limit) if total_items > 0 else 1
    
    # Ajustar página si excede el total
    if page > total_pages and total_pages > 0:
        page = total_pages
    
    # Calcular índices para el slice
    start_index = (page - 1) * limit
    end_index = start_index + limit
    
    # Obtener datos paginados (slice es O(k) donde k = limit)
    data_paginada = items[start_index:end_index]
    
    # Construir metadata de paginación
    metadata = {
        "total_items": total_items,
        "total_pages": total_pages,
        "current_page": page,
        "page_size": len(data_paginada),  # Puede ser menor que limit en última página
        "has_next": page < total_pages,
        "has_previous": page > 1
    }
    
    return {
        "data": data_paginada,
        "metadata": metadata
    }