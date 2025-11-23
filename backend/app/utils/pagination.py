"""
Utilidades para paginación de resultados.

Proporciona funciones helper para dividir listas grandes en páginas,
mejorando la experiencia de usuario y reduciendo carga de red.
"""

from typing import List, Dict, Any, TypeVar
from math import ceil

T = TypeVar("T")

class MetadataPaginacion:
    """
    Metadata de una respuesta paginada.
    
    REFACTORIZACIÓN POO: Encapsular metadata en clase
    """
    total_items: int
    total_pages: int
    current_page: int
    page_size: int
    has_next: bool
    has_previous: bool
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario"""
        return {
            "total_items": self.total_items,
            "total_pages": self.total_pages,
            "current_page": self.current_page,
            "page_size": self.page_size,
            "has_next": self.has_next,
            "has_previous": self.has_previous
        }

class Paginador:
    """
    Motor de paginación.
    
    REFACTORIZACIÓN POO: Encapsular lógica en clase
    """
    
    @staticmethod
    def paginar(
        items: List[T],
        page: int,
        limit: int
    ) -> Dict[str, Any]:
        """
        Pagina una lista de items.
        
        NOTA: Este método mantiene la misma firma que la función original
        """
        if page < 1:
            raise ValueError("El número de página debe ser mayor o igual a 1")
        if limit < 1 or limit > 50:
            raise ValueError("El límite debe estar entre 1 y 50")
        
        total_items = len(items)
        total_pages = ceil(total_items / limit) if total_items > 0 else 1
        
        if page > total_pages and total_pages > 0:
            page = total_pages
        
        start_index = (page - 1) * limit
        end_index = start_index + limit
        
        data_paginada = items[start_index:end_index]
        
        metadata = MetadataPaginacion(
            total_items=total_items,
            total_pages=total_pages,
            current_page=page,
            page_size=len(data_paginada),
            has_next=page < total_pages,
            has_previous=page > 1
        )
        
        return {
            "data": data_paginada,
            "metadata": metadata.to_dict()
        }
    

def paginar_resultados(
   items: List[T],
    page: int = 1,
    limit: int = 10
) -> Dict[str, Any]:
    """
    Pagina una lista de items y retorna datos con metadata de paginación.

    Divide una lista completa en páginas del tamaño especificado y
    retorna solo los items de la página solicitada junto con información
    útil para navegación (total de páginas, página actual, etc.).

    Args:
        items: Lista completa de elementos a paginar
        page: Número de página solicitado (debe ser >= 1)
        limit: Cantidad de items por página (debe estar entre 1 y 50)

    Returns:
        Diccionario con estructura:
        {
            "data": [...],           # Items de la página actual
            "metadata": {
                "total_items": int,  # Total de items en la lista
                "total_pages": int,  # Total de páginas disponibles
                "current_page": int, # Página actual
                "page_size": int,    # Items en esta página
                "has_next": bool,    # Hay página siguiente
                "has_previous": bool # Hay página anterior
            }
        }

    Raises:
        ValueError: Si page < 1 o limit no está en rango [1, 50]

    Complejidad temporal: O(1) + O(k) donde:
        - O(1): Cálculos matemáticos (ceil, multiplicaciones)
        - O(k): Operación slice [start:end] donde k = limit
        Total: O(k) donde k es constante pequeña (máx 50)

    Estructura de datos: List slicing

    Justificación:
        El slicing de Python [start:end] es eficiente para acceso secuencial,
        retornando solo los elementos necesarios sin recorrer toda la lista.
        Es más eficiente que iterar manualmente y más legible.

    Optimización:
        Se limita el tamaño de página a 50 para evitar cargas excesivas
        y garantizar tiempos de respuesta predecibles.
    """
    return Paginador.paginar(items, page, limit)


if __name__ == "__main__":
    """Script de verificación de paginación"""
    # Datos de prueba
    test_items = list(range(1, 26))  # [1, 2, 3, ..., 25]

    print("=" * 60)
    print("MY SIGN - SISTEMA DE PAGINACIÓN")
    print("=" * 60)
    print(f"Total de items: {len(test_items)}")
    print(f"Items por página: 10")
    print()

    # Prueba: Página 1
    print("Página 1:")
    resultado = paginar_resultados(test_items, page=1, limit=10)
    print(f"  Datos: {resultado['data']}")
    print(f"  Total páginas: {resultado['metadata']['total_pages']}")
    print(f"  Tiene siguiente: {resultado['metadata']['has_next']}")
    print()

    # Prueba: Página 2
    print("Página 2:")
    resultado = paginar_resultados(test_items, page=2, limit=10)
    print(f"  Datos: {resultado['data']}")
    print(f"  Tiene anterior: {resultado['metadata']['has_previous']}")
    print(f"  Tiene siguiente: {resultado['metadata']['has_next']}")
    print()

    # Prueba: Última página (incompleta)
    print("Página 3 (última, incompleta):")
    resultado = paginar_resultados(test_items, page=3, limit=10)
    print(f"  Datos: {resultado['data']}")
    print(f"  Tamaño: {resultado['metadata']['page_size']} items")
    print(f"  Tiene siguiente: {resultado['metadata']['has_next']}")

    print("=" * 60)
