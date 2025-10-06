"""
app/services/buscador.py
------------------------
Sistema de búsqueda para My Sign usando HashMaps (diccionarios de Python).

Por qué usamos HashMaps (diccionarios):
- Un HashMap ofrece, en promedio, acceso O(1) para operaciones de búsqueda por clave.
- Aquí mapeamos identificadores y categorías a listas/objetos para realizar búsquedas
  muy rápidas sin recorrer linealmente toda la colección.
- Tradeoff: mayor uso de memoria (duplicación de referencias), a cambio de búsquedas mucho más rápidas.

Estructuras utilizadas:
- servicios_por_id: Dict[str, dict]                 # ID -> servicio (búsqueda directa)
- servicios_por_categoria: Dict[str, List[dict]]   # categoría -> lista de servicios
- servicios_por_zona: Dict[str, List[dict]]        # zona -> lista de servicios
- interpretes_por_id: Dict[str, dict]              # ID -> intérprete
- interpretes_por_especialidad: Dict[str, List[dict]]  # especialidad -> lista intérpretes

Nota: Los diccionarios de Python se comportan como HashMaps con tiempo promedio O(1)
para operaciones get/put. Las complejidades indicadas abajo asumen comportamiento promedio.
"""

from typing import Dict, List, Optional

from data.mock_data import SERVICIOS_MOCK, INTERPRETES_MOCK


class BuscadorServicios:
    """
    Clase que implementa un sistema de búsqueda basado en HashMaps para servicios e intérpretes.

    Ventajas:
    - Consultas por id/categoría/zona/especialidad realizan accesos directos
      a estructuras preconstruidas, evitando búsquedas lineales costosas.
    - Ideal para APIs que necesitan respuestas rápidas y frecuentes.

    Uso:
        buscador = BuscadorServicios(SERVICIOS_MOCK, INTERPRETES_MOCK)
        servicio = buscador.buscar_servicio_por_id("s1")
        hospitales = buscador.buscar_servicios_por_categoria("Salud")
        norte = buscador.buscar_servicios_por_zona("Norte")
        filtrados = buscador.filtrar_servicios(categoria="Salud", tiene_interprete=True)
    """

    def __init__(self, servicios: List[dict], interpretes: List[dict]):
        """
        Construye los HashMaps internos a partir de las listas de servicios e intérpretes.

        Pasos (cada uno comentado con complejidad):
        1. servicios_por_id:
           - Iterar sobre cada servicio y asignarlo por su clave 'id'.
           - Complejidad: O(n) donde n = número de servicios.
        2. servicios_por_categoria:
           - Para cada servicio, tomar servicio['categoria'] y
             añadir el servicio a la lista correspondiente.
           - Complejidad: O(n) (cada inserción en lista es O(1) amortizado).
        3. servicios_por_zona:
           - Análogo a categoría, indexando por servicio['zona'].
           - Complejidad: O(n).
        4. interpretes_por_id:
           - Mapear cada intérprete por su 'id'.
           - Complejidad: O(m) donde m = número de intérpretes.
        5. interpretes_por_especialidad:
           - Para cada intérprete y cada especialidad en su lista,
             añadir el intérprete a la lista de esa especialidad.
           - Complejidad: O(m * k) donde k = promedio de especialidades por intérprete.

        Nota sobre memoria: estas estructuras guardan referencias a los dicts originales,
        por lo que el coste en memoria es principalmente de las listas y claves adicionales,
        no duplicación profunda de los objetos.
        """
        # HashMap: id -> servicio
        self.servicios_por_id: Dict[str, dict] = {}

        # HashMap: categoria -> [servicio, servicio, ...]
        self.servicios_por_categoria: Dict[str, List[dict]] = {}

        # HashMap: zona -> [servicio, servicio, ...]
        self.servicios_por_zona: Dict[str, List[dict]] = {}

        # HashMap: id -> interprete
        self.interpretes_por_id: Dict[str, dict] = {}

        # HashMap: especialidad -> [interprete, interprete, ...]
        self.interpretes_por_especialidad: Dict[str, List[dict]] = {}

        # ----------------------------
        # Construcción de servicios
        # ----------------------------
        # Recorremos todos los servicios una sola vez para poblar los tres mapas relacionados.
        for servicio in servicios:
            sid = servicio.get("id")
            if sid is None:
                # Ignoramos servicios sin id; en producción podríamos lanzar error/validar
                continue

            # 1) Mapear por id (acceso O(1) promedio)
            self.servicios_por_id[sid] = servicio

            # 2) Indexar por categoría
            categoria = servicio.get("categoria", "Sin Categoria")
            if categoria not in self.servicios_por_categoria:
                self.servicios_por_categoria[categoria] = []
            # append es O(1) amortizado
            self.servicios_por_categoria[categoria].append(servicio)

            # 3) Indexar por zona
            zona = servicio.get("zona", "Sin Zona")
            if zona not in self.servicios_por_zona:
                self.servicios_por_zona[zona] = []
            self.servicios_por_zona[zona].append(servicio)

        # ----------------------------
        # Construcción de intérpretes
        # ----------------------------
        # Recorremos todos los intérpretes para mapear por id y por cada especialidad.
        for interprete in interpretes:
            iid = interprete.get("id")
            if iid is None:
                continue

            # Mapear por id
            self.interpretes_por_id[iid] = interprete

            # Mapear por especialidades (cada especialidad -> lista de intérpretes)
            especialidades = interprete.get("especialidades", [])
            for esp in especialidades:
                if esp not in self.interpretes_por_especialidad:
                    self.interpretes_por_especialidad[esp] = []
                self.interpretes_por_especialidad[esp].append(interprete)

    # ----------------------------
    # MÉTODOS DE BÚSQUEDA
    # ----------------------------
    def buscar_servicio_por_id(self, id: str) -> Optional[dict]:
        """
        Busca un servicio por su identificador único.

        Parámetros:
            id (str): Identificador del servicio.

        Retorna:
            dict | None: El diccionario del servicio si existe, o None si no se encuentra.

        Ejemplo:
            buscador.buscar_servicio_por_id("s1")

        Complejidad temporal:
            O(1) promedio (lookup directo en HashMap).
        """
        return self.servicios_por_id.get(id)

    def buscar_servicios_por_categoria(self, categoria: str) -> List[dict]:
        """
        Devuelve la lista de servicios pertenecientes a una categoría dada.

        Parámetros:
            categoria (str): Nombre de la categoría (ej. "Salud").

        Retorna:
            List[dict]: Lista de servicios (vacía si no hay coincidencias).

        Ejemplo:
            buscador.buscar_servicios_por_categoria("Educación")

        Complejidad temporal:
            O(1) para obtener la lista (pero iterar sobre la lista completa es O(k),
            donde k es el número de servicios en esa categoría).
        """
        return list(self.servicios_por_categoria.get(categoria, []))

    def buscar_servicios_por_zona(self, zona: str) -> List[dict]:
        """
        Devuelve la lista de servicios pertenecientes a una zona geográfica.

        Parámetros:
            zona (str): Nombre de la zona (ej. "Centro", "Norte").

        Retorna:
            List[dict]: Lista de servicios en la zona (vacía si no hay coincidencias).

        Ejemplo:
            buscador.buscar_servicios_por_zona("Norte")

        Complejidad temporal:
            O(1) para obtener la lista; iterar sobre la lista es O(k).
        """
        return list(self.servicios_por_zona.get(zona, []))

    def filtrar_servicios(
        self,
        categoria: Optional[str] = None,
        zona: Optional[str] = None,
        tiene_interprete: Optional[bool] = None,
    ) -> List[dict]:
        """
        Filtra servicios combinando criterios opcionales: categoría, zona y disponibilidad de intérprete.

        Estrategia implementada (para evitar búsqueda lineal completa cuando sea posible):
        - Si se proporciona 'categoria', se comienza con la lista de esa categoría (k elementos).
        - Si no, pero se proporciona 'zona', se comienza con la lista de esa zona.
        - Si no se proporciona ninguno, se recurre a todos los servicios (n elementos).
        - A partir de la lista inicial se aplican los filtros restantes (si existen).

        Parámetros:
            categoria (str | None): Filtrar por categoría.
            zona (str | None): Filtrar por zona.
            tiene_interprete (bool | None): Filtrar por disponibilidad de intérprete LSC.

        Retorna:
            List[dict]: Lista de servicios que cumplen los criterios.

        Ejemplo:
            buscador.filtrar_servicios(categoria="Salud", tiene_interprete=True)

        Complejidad temporal:
            - Mejor caso: si categoria o zona reduce mucho la búsqueda, O(k) donde k << n.
            - Peor caso: si no hay filtros iniciales, O(n) donde n = total de servicios.
            """
        # Seleccionar lista inicial de candidatos según criterio que más reduzca la búsqueda.
        candidatos: List[dict]

        if categoria:
            candidatos = self.servicios_por_categoria.get(categoria, [])
            # candidatos es una referencia; crear copia para no modificar estructuras internas
            candidatos = list(candidatos)
        elif zona:
            candidatos = self.servicios_por_zona.get(zona, [])
            candidatos = list(candidatos)
        else:
            # Si no hay filtro de categoría ni zona, tomar todos los servicios
            candidatos = list(self.servicios_por_id.values())

        # Aplicar filtros adicionales
        resultados: List[dict] = []
        for servicio in candidatos:
            # Filtrar por zona si se pasó y la lista inicial fue por categoría
            if zona and servicio.get("zona") != zona:
                continue

            # Filtrar por intérprete si se solicitó
            if tiene_interprete is not None:
                # Campo esperado: 'tiene_interprete_lsc' (bool)
                if bool(servicio.get("tiene_interprete_lsc")) != bool(tiene_interprete):
                    continue

            resultados.append(servicio)

        return resultados

    def buscar_interprete_por_id(self, id: str) -> Optional[dict]:
        """
        Busca un intérprete por su identificador único.

        Parámetros:
            id (str): Identificador del intérprete.

        Retorna:
            dict | None: Diccionario del intérprete o None si no existe.

        Ejemplo:
            buscador.buscar_interprete_por_id("i1")

        Complejidad temporal:
            O(1) promedio (lookup directo en HashMap).
        """
        return self.interpretes_por_id.get(id)

    def buscar_interpretes_por_especialidad(self, especialidad: str) -> List[dict]:
        """
        Devuelve la lista de intérpretes que tienen la especialidad indicada.

        Parámetros:
            especialidad (str): Nombre de la especialidad (ej. "Médica").

        Retorna:
            List[dict]: Lista de intérpretes (vacía si no hay coincidencias).

        Ejemplo:
            buscador.buscar_interpretes_por_especialidad("Legal")

        Complejidad temporal:
            O(1) para obtener la lista; iterar sobre la lista es O(k).
        """
        return list(self.interpretes_por_especialidad.get(especialidad, []))

    def obtener_todas_categorias(self) -> List[str]:
        """
        Retorna una lista con todas las categorías indexadas en el buscador.

        Retorna:
            List[str]: Lista de nombres de categorías.

        Ejemplo:
            buscador.obtener_todas_categorias()

        Complejidad temporal:
            O(c) donde c es el número de categorías (gasto en construcción de la lista).
        """
        return list(self.servicios_por_categoria.keys())


# ----------------------------
# Inicializador por conveniencia (usa datos mock)
# ----------------------------
def crear_buscador_desde_mock() -> BuscadorServicios:
    """
    Crea una instancia de BuscadorServicios inicializada con los datos mock del proyecto.

    Uso:
        buscador = crear_buscador_desde_mock()

    Complejidad:
        O(n + m * k) similar a la construcción directa en __init__.
    """
    return BuscadorServicios(SERVICIOS_MOCK, INTERPRETES_MOCK)


# ----------------------------
# Bloque de prueba rápido (solo para desarrollo)
# ----------------------------
if __name__ == "__main__":
    buscador = crear_buscador_desde_mock()
    print("Total servicios indexados:", len(buscador.servicios_por_id))
    print("Categorías:", buscador.obtener_todas_categorias())
    print("Buscar servicio s1:", buscador.buscar_servicio_por_id("s1"))
    print("Servicios en Salud:", len(buscador.buscar_servicios_por_categoria("Salud")))
    print("Interpretes Médica:", len(buscador.buscar_interpretes_por_especialidad("Médica")))
    print("Filtrar (Salud, tiene interprete=True):", len(buscador.filtrar_servicios(categoria="Salud", tiene_interprete=True)))
