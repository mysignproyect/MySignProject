from typing import Dict, List, Optional
from data.mock_data import SERVICIOS_MOCK


class NodoCategoria:
    """
    Representa un nodo dentro del árbol de categorías.

    Cada nodo puede tener:
    - Un nombre (la categoría o subcategoría)
    - Subcategorías hijas (almacenadas en un diccionario)
    - Una lista de servicios asociados directamente a esa categoría

    Ejemplo de estructura:
        Salud
        ├── Hospitales
        │   ├── [servicios...]
        └── Clínicas
            ├── [servicios...]
    """

    def __init__(self, nombre: str):
        self.nombre: str = nombre
        self.subcategorias: Dict[str, NodoCategoria] = {}
        self.servicios: List[dict] = []

    def add_subcategoria(self, nombre: str) -> "NodoCategoria":
        if nombre not in self.subcategorias:
            self.subcategorias[nombre] = NodoCategoria(nombre)
        return self.subcategorias[nombre]

    def add_servicio(self, servicio: dict):
        """
        Agrega un servicio a la lista del nodo actual.
        Complejidad temporal: O(1)
        """
        self.servicios.append(servicio)

class ArbolCategorias:
    """
    Representa el árbol general de categorías de servicios.

    Estructura base:
        Raíz
        ├── Salud
        │   ├── Hospitales
        │   ├── Clínicas
        │   └── Centros de Salud
        ├── Educación
        │   ├── Colegios
        │   ├── Universidades
        │   └── Institutos
        ├── Gobierno
        │   ├── Alcaldías
        │   └── Entidades Públicas
        └── Intérpretes
            └── Por Especialidad
    """

    def __init__(self):
        """Inicializa la raíz y construye las categorías y subcategorías predefinidas."""
        self.raiz = NodoCategoria("Raíz")

        # Construcción manual de la jerarquía de categorías
        salud = self.raiz.add_subcategoria("Salud")
        for sub in ["Hospitales", "Clínicas", "Centros de Salud"]:
            salud.add_subcategoria(sub)

        educacion = self.raiz.add_subcategoria("Educación")
        for sub in ["Colegios", "Universidades", "Institutos"]:
            educacion.add_subcategoria(sub)

        gobierno = self.raiz.add_subcategoria("Gobierno")
        for sub in ["Alcaldías", "Entidades Públicas"]:
            gobierno.add_subcategoria(sub)

        interpretes = self.raiz.add_subcategoria("Intérpretes")
        interpretes.add_subcategoria("Por Especialidad")

    # ---------------------------------------------------------------
    def buscar_servicios_categoria(
        self, categoria: str, subcategoria: Optional[str] = None
    ) -> List[dict]:
        """
        COMPLEJIDAD TEMPORAL: O(n), donde n es el número total de nodos en el árbol.
        """

        resultados: List[dict] = []

        # Caso base: si el nodo actual es la categoría buscada
        def buscar_recursivo(nodo: NodoCategoria):
            # Caso base: si encontramos la categoría
            if nodo.nombre == categoria:
                if subcategoria:
                    # Buscar recursivamente dentro de las subcategorías
                    if subcategoria in nodo.subcategorias:
                        resultados.extend(nodo.subcategorias[subcategoria].servicios)
                else:
                    # Si no se especifica subcategoría, agregar todos los servicios de este nodo y sus hijos
                    resultados.extend(nodo.servicios)
                    for sub in nodo.subcategorias.values():
                        resultados.extend(sub.servicios)
                return

            # Caso recursivo: recorrer subcategorías hasta encontrar la categoría deseada
            for sub in nodo.subcategorias.values():
                buscar_recursivo(sub)

        buscar_recursivo(self.raiz)
        return resultados

    # ---------------------------------------------------------------
    def obtener_todas_categorias(self) -> List[str]:
        """
        COMPLEJIDAD TEMPORAL: O(n), donde n es el número total de nodos.
        """
        categorias: List[str] = []

        def recorrer(nodo: NodoCategoria):
            # Caso base: si el nodo no tiene subcategorías, retornamos su nombre
            categorias.append(nodo.nombre)

            # Caso recursivo: recorrer todas las subcategorías
            for sub in nodo.subcategorias.values():
                recorrer(sub)

        recorrer(self.raiz)
        return categorias

    # ---------------------------------------------------------------
    def cargar_servicios(self, servicios: List[dict]):
        """
        COMPLEJIDAD TEMPORAL: O(n), siendo n el número de servicios.
        Cada inserción en un nodo es O(1).
        """
        for servicio in servicios:
            categoria = servicio.get("categoria")
            subcategoria = servicio.get("subcategoria")

            # Validar existencia de categoría en el árbol
            if categoria in self.raiz.subcategorias:
                nodo_categoria = self.raiz.subcategorias[categoria]

                # Si tiene subcategoría y existe, se agrega allí
                if subcategoria and subcategoria in nodo_categoria.subcategorias:
                    nodo_categoria.subcategorias[subcategoria].add_servicio(servicio)
                else:
                    # Si no hay subcategoría válida, se agrega directamente a la categoría principal
                    nodo_categoria.add_servicio(servicio)
            else:
                # Si la categoría no existe, crearla dinámicamente
                nuevo_nodo = self.raiz.add_subcategoria(categoria)
                nuevo_nodo.add_servicio(servicio)


def inicializar_arbol_con_mock() -> ArbolCategorias:
    """
    Crea una instancia de ArbolCategorias y carga los servicios de prueba (mock).
    Se utiliza principalmente para pruebas unitarias o desarrollo local.

    COMPLEJIDAD: O(n), donde n es la cantidad de servicios mock cargados.
    """
    arbol = ArbolCategorias()
    arbol.cargar_servicios(SERVICIOS_MOCK)
    return arbol

if __name__ == "__main__":
    arbol = inicializar_arbol_con_mock()
    print("Categorías disponibles:")
    print(arbol.obtener_todas_categorias())
    print("\nServicios en categoría 'Salud' -> 'Hospitales':")
    print(arbol.buscar_servicios_categoria("Salud", "Hospitales"))