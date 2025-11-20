"""
Módulo de árbol jerárquico de categorías para servicios.

Implementa un árbol n-ario que organiza servicios en categorías y
subcategorías, permitiendo búsquedas jerárquicas y navegación estructurada.

Estructura del árbol:
    Raíz
    ├── Salud
    │   ├── Hospitales
    │   ├── Clínicas
    │   └── Centros de Salud
    ├── Educación
    │   ├── Colegios
    │   ├── Universidades
    │   └── Institutos
    └── Gobierno
        ├── Alcaldías
        └── Entidades Públicas
"""

from typing import Dict, List, Optional
from data.mock_data import SERVICIOS_MOCK


class NodoCategoria:
    """
    Nodo del árbol de categorías.
    
    Cada nodo puede contener:
    - Subcategorías (nodos hijos)
    - Lista de servicios asociados
    
    Estructura de datos: Árbol n-ario (cada nodo puede tener múltiples hijos)
    """

    def __init__(self, nombre: str):
        """
        Inicializa un nodo de categoría.
        
        Args:
            nombre: Nombre de la categoría o subcategoría
        
        Complejidad: O(1)
        """
        self.nombre: str = nombre
        self.subcategorias: Dict[str, NodoCategoria] = {}
        self.servicios: List[dict] = []

    def add_subcategoria(self, nombre: str) -> "NodoCategoria":
        """
        Agrega o retorna una subcategoría.
        
        Si la subcategoría ya existe, retorna el nodo existente.
        Si no existe, crea un nuevo nodo hijo.
        
        Complejidad: O(1) - Acceso a dict por clave
        """
        if nombre not in self.subcategorias:
            self.subcategorias[nombre] = NodoCategoria(nombre)
        return self.subcategorias[nombre]

    def add_servicio(self, servicio: dict):
        """
        Agrega un servicio a este nodo.
        
        Complejidad: O(1) - Append a lista
        """
        self.servicios.append(servicio)


class ArbolCategorias:
    """
    Árbol jerárquico de categorías de servicios.
    
    Organiza servicios en una estructura de árbol con 3 niveles:
    1. Raíz (invisible al usuario)
    2. Categorías principales (Salud, Educación, Gobierno)
    3. Subcategorías (Hospitales, Clínicas, Colegios, etc.)
    
    Justificación del árbol:
        - Representa naturalmente jerarquías (categoría → subcategoría)
        - Permite navegación intuitiva nivel por nivel
        - Facilita búsquedas recursivas por categoría
        - Estructura escalable para agregar más niveles si se requiere
    """

    def __init__(self):
        """
        Inicializa el árbol con la estructura predefinida de categorías.
        
        Complejidad: O(1) - Solo crea nodos de categorías (no carga servicios aún)
        """
        self.raiz = NodoCategoria("Raíz")

        # Construcción de categoría Salud con sus subcategorías
        salud = self.raiz.add_subcategoria("Salud")
        for sub in ["Hospitales", "Clínicas", "Centros de Salud"]:
            salud.add_subcategoria(sub)

        # Construcción de categoría Educación
        educacion = self.raiz.add_subcategoria("Educación")
        for sub in ["Colegios", "Universidades", "Institutos"]:
            educacion.add_subcategoria(sub)

        # Construcción de categoría Gobierno
        gobierno = self.raiz.add_subcategoria("Gobierno")
        for sub in ["Alcaldías", "Entidades Públicas"]:
            gobierno.add_subcategoria(sub)

    def buscar_servicios_categoria(
        self, categoria: str, subcategoria: Optional[str] = None
    ) -> List[dict]:
        """
        Busca servicios en el árbol por categoría y opcionalmente subcategoría.
        
        Usa RECURSIÓN para recorrer el árbol hasta encontrar el nodo deseado.
        
        Args:
            categoria: Categoría principal (ej: "Salud", "Educación")
            subcategoria: Subcategoría específica (opcional, ej: "Hospitales")
        
        Returns:
            Lista de servicios que coinciden con los criterios
        
        Complejidad: O(h + k) donde:
            h = altura del árbol (en este caso, constante pequeña = 2)
            k = servicios encontrados
        
        Estructura: Árbol con recorrido recursivo en profundidad (DFS)
        
        Justificación de recursión:
            La recursión es natural para recorrer árboles ya que:
            - El código es más legible que iteración con pilas
            - Refleja la estructura jerárquica del problema
            - La profundidad es pequeña (máx 2-3 niveles), no hay riesgo de stack overflow
        """
        resultados: List[dict] = []

        def buscar_recursivo(nodo: NodoCategoria):
            """
            Función recursiva interna para recorrer el árbol.
            
            Caso base: Si encontramos la categoría buscada
            Caso recursivo: Seguir buscando en subcategorías
            """
            # Caso base: encontramos la categoría
            if nodo.nombre == categoria:
                if subcategoria:
                    # Buscar subcategoría específica
                    if subcategoria in nodo.subcategorias:
                        resultados.extend(nodo.subcategorias[subcategoria].servicios)
                else:
                    # Sin subcategoría: agregar todos los servicios del nodo y sus hijos
                    resultados.extend(nodo.servicios)
                    for sub in nodo.subcategorias.values():
                        resultados.extend(sub.servicios)
                return

            # Caso recursivo: seguir buscando en subcategorías
            for sub in nodo.subcategorias.values():
                buscar_recursivo(sub)

        # Iniciar búsqueda recursiva desde la raíz
        buscar_recursivo(self.raiz)
        return resultados

    def obtener_todas_categorias(self) -> List[str]:
        """
        Retorna las categorías principales (hijos directos de la raíz).
        
        Returns:
            Lista con nombres: ["Salud", "Educación", "Gobierno"]
        
        Complejidad: O(1) - Solo accede al primer nivel del árbol
        """
        return list(self.raiz.subcategorias.keys())
    
    def obtener_subcategorias(self, categoria: str) -> List[str]:
        """
        Obtiene subcategorías de una categoría principal.
        
        Args:
            categoria: Nombre de categoría principal
        
        Returns:
            Lista de nombres de subcategorías, o lista vacía si no existe
        
        Complejidad: O(1) - Acceso directo al nodo en el árbol
        """
        if categoria in self.raiz.subcategorias:
            nodo_categoria = self.raiz.subcategorias[categoria]
            return list(nodo_categoria.subcategorias.keys())
        return []

    def cargar_servicios(self, servicios: List[dict]):
        """
        Carga servicios en el árbol según su categoría y subcategoría.
        
        Cada servicio se coloca en el nodo correspondiente de la jerarquía.
        Si la categoría no existe, se crea dinámicamente.
        
        Args:
            servicios: Lista de diccionarios con información de servicios
        
        Complejidad: O(n) donde n = número de servicios
            Cada servicio se inserta en O(1) en el nodo correspondiente
        
        Justificación:
            Aunque cargar servicios es O(n), las búsquedas posteriores
            son O(h) gracias a la estructura del árbol, donde h es la altura
            (constante pequeña en este caso).
        """
        for servicio in servicios:
            categoria = servicio.get("categoria")
            subcategoria = servicio.get("subcategoria")

            # Verificar si la categoría existe en el árbol
            if categoria in self.raiz.subcategorias:
                nodo_categoria = self.raiz.subcategorias[categoria]

                # Si tiene subcategoría válida, agregar ahí
                if subcategoria and subcategoria in nodo_categoria.subcategorias:
                    nodo_categoria.subcategorias[subcategoria].add_servicio(servicio)
                else:
                    # Sin subcategoría válida, agregar a categoría principal
                    nodo_categoria.add_servicio(servicio)
            else:
                # Categoría no existe: crearla dinámicamente
                nuevo_nodo = self.raiz.add_subcategoria(categoria)
                nuevo_nodo.add_servicio(servicio)


def inicializar_arbol_con_mock() -> ArbolCategorias:
    """
    Factory function: Crea árbol precargado con datos mock.
    
    Utilizada para testing y desarrollo local.
    
    Returns:
        Instancia de ArbolCategorias con servicios mock cargados
    
    Complejidad: O(n) donde n = servicios en SERVICIOS_MOCK
    """
    arbol = ArbolCategorias()
    arbol.cargar_servicios(SERVICIOS_MOCK)
    return arbol


if __name__ == "__main__":
    """Script de verificación rápida del árbol de categorías"""
    arbol = inicializar_arbol_con_mock()
    
    print("=" * 60)
    print("MY SIGN - ÁRBOL DE CATEGORÍAS")
    print("=" * 60)
    
    # Mostrar estructura del árbol
    print("Categorías disponibles:")
    categorias = arbol.obtener_todas_categorias()
    for cat in categorias:
        print(f"  • {cat}")
        subcats = arbol.obtener_subcategorias(cat)
        for sub in subcats:
            print(f"    ├── {sub}")
    print()
    
    # Pruebas de búsqueda
    print("Prueba 1: Todos los servicios de Salud")
    servicios_salud = arbol.buscar_servicios_categoria("Salud")
    print(f"  → Encontrados: {len(servicios_salud)} servicios")
    print()
    
    print("Prueba 2: Solo Hospitales")
    hospitales = arbol.buscar_servicios_categoria("Salud", "Hospitales")
    print(f"  → Encontrados: {len(hospitales)} hospitales")
    for h in hospitales:
        print(f"    • {h['nombre']}")
    
    print("=" * 60)