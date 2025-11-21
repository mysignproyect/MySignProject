"""
Módulo de búsqueda de servicios e intérpretes LSC usando HashMaps.

Implementa la capa de lógica de negocio para My Sign,
utilizando HashMaps para garantizar búsquedas eficientes O(1).
"""

from typing import Dict, List, Optional
from data.mock_data import SERVICIOS_MOCK, INTERPRETES_MOCK


class BuscadorServicios:
    """
    Gestiona la búsqueda y filtrado de servicios e intérpretes LSC.

    Usa múltiples HashMaps para indexar datos y permitir búsquedas
    eficientes sin recorrer colecciones completas.
    """

    def __init__(self, servicios: List[dict], interpretes: List[dict]):
        """
        Inicializa los HashMaps e indexa servicios e intérpretes.

        Args:
            servicios: Lista de servicios a indexar
            interpretes: Lista de intérpretes a indexar

        Complejidad temporal: O(n + m*k)
            n = servicios, m = intérpretes, k = especialidades promedio
        Estructura: HashMap (dict de Python)
        """
        # HashMaps para servicios
        self.servicios_por_id: Dict[str, dict] = {}
        self.servicios_por_categoria: Dict[str, List[dict]] = {}
        self.servicios_por_zona: Dict[str, List[dict]] = {}

        # HashMaps para intérpretes
        self.interpretes_por_id: Dict[str, dict] = {}
        self.interpretes_por_especialidad: Dict[str, List[dict]] = {}

        # Indexar servicios
        for servicio in servicios:
            sid = servicio.get("id")
            if sid is None:
                continue

            # Indexar por ID
            self.servicios_por_id[sid] = servicio

            # Indexar por categoría
            categoria = servicio.get("categoria", "Sin Categoria")
            if categoria not in self.servicios_por_categoria:
                self.servicios_por_categoria[categoria] = []
            self.servicios_por_categoria[categoria].append(servicio)

            # Indexar por zona
            zona = servicio.get("zona", "Sin Zona")
            if zona not in self.servicios_por_zona:
                self.servicios_por_zona[zona] = []
            self.servicios_por_zona[zona].append(servicio)

        # Indexar intérpretes
        for interprete in interpretes:
            iid = interprete.get("id")
            if iid is None:
                continue

            self.interpretes_por_id[iid] = interprete

            # Un intérprete puede tener múltiples especialidades
            especialidades = interprete.get("especialidades", [])
            for esp in especialidades:
                if esp not in self.interpretes_por_especialidad:
                    self.interpretes_por_especialidad[esp] = []
                self.interpretes_por_especialidad[esp].append(interprete)

    # ========================================================================
    # MÉTODOS DE BÚSQUEDA DE SERVICIOS
    # ========================================================================

    def buscar_servicio_por_id(self, id: str) -> Optional[dict]:
        """
        Busca un servicio por su ID único.

        Complejidad: O(1) - Acceso directo a HashMap
        """
        return self.servicios_por_id.get(id)

    def buscar_servicios_por_categoria(self, categoria: str) -> List[dict]:
        """
        Obtiene todos los servicios de una categoría.

        Complejidad: O(1) + O(k) donde k = servicios en la categoría
        """
        return list(self.servicios_por_categoria.get(categoria, []))

    def buscar_servicios_por_zona(self, zona: str) -> List[dict]:
        """
        Obtiene todos los servicios de una zona geográfica.

        Complejidad: O(1) + O(k) donde k = servicios en la zona
        """
        return list(self.servicios_por_zona.get(zona, []))

    def buscar_servicios_por_texto(self, texto: str) -> List[dict]:
        """
        Busca servicios por texto en nombre, dirección y características.
        Búsqueda case-insensitive.

        Args:
            texto: Texto a buscar

        Returns:
            Lista de servicios que contienen el texto

        Complejidad: O(n) - Debe revisar todos los servicios
        Nota: La búsqueda de texto libre no puede optimizarse con HashMap
        """
        texto_lower = texto.lower()
        resultados = []

        for servicio in self.servicios_por_id.values():
            # Buscar en nombre
            if texto_lower in servicio.get("nombre", "").lower():
                resultados.append(servicio)
                continue

            # Buscar en dirección
            if texto_lower in servicio.get("direccion", "").lower():
                resultados.append(servicio)
                continue

            # Buscar en características
            caracteristicas = servicio.get("caracteristicas_accesibilidad", [])
            for caract in caracteristicas:
                if texto_lower in caract.lower():
                    resultados.append(servicio)
                    break

        return resultados

    def filtrar_servicios(
        self,
        categoria: Optional[str] = None,
        subcategoria: Optional[str] = None,
        zona: Optional[str] = None,
        tiene_interprete: Optional[bool] = None,
    ) -> List[dict]:
        """
        Filtra servicios por múltiples criterios (AND lógico).

        Estrategia: Empieza con el criterio más restrictivo (categoria o zona)
        para reducir candidatos antes de aplicar otros filtros.

        Complejidad:
            Mejor caso: O(k) donde k << n (categoria/zona reduce mucho)
            Peor caso: O(n) sin filtros iniciales
        """
        # Elegir conjunto inicial más pequeño
        if categoria:
            candidatos = list(self.servicios_por_categoria.get(categoria, []))
        elif zona:
            candidatos = list(self.servicios_por_zona.get(zona, []))
        else:
            candidatos = list(self.servicios_por_id.values())

        # Aplicar filtros adicionales
        resultados = []
        for servicio in candidatos:
            # Filtrar por subcategoría
            if subcategoria and servicio.get("subcategoria") != subcategoria:
                continue

            # Filtrar por zona
            if zona and servicio.get("zona") != zona:
                continue

            # Filtrar por intérprete
            if tiene_interprete is not None:
                if bool(servicio.get("tiene_interprete_lsc")) != bool(tiene_interprete):
                    continue

            resultados.append(servicio)

        return resultados

    # ========================================================================
    # MÉTODOS DE BÚSQUEDA DE INTÉRPRETES
    # ========================================================================

    def buscar_interprete_por_id(self, id: str) -> Optional[dict]:
        """
        Busca un intérprete por su ID único.

        Complejidad: O(1) - Acceso directo a HashMap
        """
        return self.interpretes_por_id.get(id)

    def buscar_interpretes_por_especialidad(self, especialidad: str) -> List[dict]:
        """
        Obtiene intérpretes con una especialidad específica.

        Complejidad: O(1) + O(k) donde k = intérpretes con esa especialidad
        """
        return list(self.interpretes_por_especialidad.get(especialidad, []))

    def buscar_interpretes_por_zona(self, zona: str) -> List[dict]:
        """
        Busca intérpretes que cubran una zona específica.

        Como las zonas_cobertura es una lista por intérprete,
        debe revisar todos los intérpretes.

        Complejidad: O(m * z) donde m = intérpretes, z = zonas promedio (2-3)
        Nota: Aceptable dado que m suele ser pequeño
        """
        resultados = []

        for interprete in self.interpretes_por_id.values():
            zonas = interprete.get("zonas_cobertura", [])
            if zona in zonas:
                resultados.append(interprete)

        return resultados

    def filtrar_interpretes(
        self,
        especialidad: Optional[str] = None,
        zona: Optional[str] = None,
        disponibilidad: Optional[str] = None,
    ) -> List[dict]:
        """
        Filtra intérpretes por múltiples criterios (AND lógico).

        Args:
            especialidad: Especialidad del intérprete
            zona: Zona de cobertura
            disponibilidad: Tipo (inmediata, tiempo_completo, por_horas, fines_semana)

        Complejidad:
            Mejor caso: O(k) si especialidad reduce mucho
            Peor caso: O(m) sin filtro de especialidad
        """
        # Conjunto inicial
        if especialidad:
            candidatos = self.buscar_interpretes_por_especialidad(especialidad)
        else:
            candidatos = list(self.interpretes_por_id.values())

        resultados = []

        # Palabras clave para disponibilidad
        palabras_clave = {
            "inmediata": ["disponible", "inmediata", "ahora"],
            "tiempo_completo": ["tiempo completo", "completo", "full"],
            "por_horas": ["horas", "por hora"],
            "fines_semana": ["fin", "semana", "sábado", "domingo"],
        }

        for interprete in candidatos:
            # Filtro por zona
            if zona:
                if zona not in interprete.get("zonas_cobertura", []):
                    continue

            # Filtro por disponibilidad
            if disponibilidad:
                keywords = palabras_clave.get(disponibilidad.lower(), [])
                disp_texto = interprete.get("disponibilidad", "").lower()

                if not any(kw in disp_texto for kw in keywords):
                    continue

            resultados.append(interprete)

        return resultados

    def obtener_todas_categorias(self) -> List[str]:
        """
        Obtiene lista de categorías disponibles.

        Complejidad: O(c) donde c = número de categorías (constante pequeña)
        """
        return list(self.servicios_por_categoria.keys())


def crear_buscador_desde_mock() -> BuscadorServicios:
    """
    Crea instancia de BuscadorServicios con datos mock para testing.

    Complejidad: O(n + m*k) - Igual que el constructor
    """
    return BuscadorServicios(SERVICIOS_MOCK, INTERPRETES_MOCK)


if __name__ == "__main__":
    """Script de verificación rápida"""
    buscador = crear_buscador_desde_mock()

    print("=" * 60)
    print("MY SIGN - BUSCADOR DE SERVICIOS E INTÉRPRETES LSC")
    print("=" * 60)
    print(f"Servicios indexados: {len(buscador.servicios_por_id)}")
    print(f"Intérpretes registrados: {len(buscador.interpretes_por_id)}")
    print(f"Categorías: {buscador.obtener_todas_categorias()}")
    print()

    # Pruebas rápidas
    print("✓ Buscar servicio 's1':", buscador.buscar_servicio_por_id("s1")["nombre"])
    print(
        "✓ Servicios de Salud:", len(buscador.buscar_servicios_por_categoria("Salud"))
    )
    print(
        "✓ Intérpretes Médica:",
        len(buscador.buscar_interpretes_por_especialidad("Médica")),
    )
    print(
        "✓ Filtro (Salud + intérprete):",
        len(buscador.filtrar_servicios(categoria="Salud", tiene_interprete=True)),
    )
    print("=" * 60)
