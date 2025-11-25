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
    """

    def __init__(self, servicios: List[dict], interpretes: List[dict]):
        """
        Inicializa los HashMaps e indexa servicios e intérpretes.
        """

        # HashMaps para servicios
        self._servicios_por_id: Dict[str, dict] = {}
        self._servicios_por_categoria: Dict[str, List[dict]] = {}
        self._servicios_por_zona: Dict[str, List[dict]] = {}

        # HashMaps para intérpretes
        self._interpretes_por_id: Dict[str, dict] = {}
        self._interpretes_por_especialidad: Dict[str, List[dict]] = {}

        # Indexación
        self._indexar_servicios(servicios)
        self._indexar_interpretes(interpretes)

    # ========================================================================
    # MÉTODOS PRIVADOS DE INDEXACIÓN
    # ========================================================================

    def _indexar_servicios(self, servicios: List[dict]) -> None:
        for servicio in servicios:
            sid = servicio.get("id")
            if sid is None:
                continue

            self._indexar_servicio_por_id(sid, servicio)
            self._indexar_servicio_por_categoria(servicio)
            self._indexar_servicio_por_zona(servicio)

    
    def _indexar_servicio_por_id(self, sid: str, servicio: dict) -> None:
        self._servicios_por_id[sid] = servicio

    def _indexar_servicio_por_categoria(self, servicio: dict) -> None:
        categoria = servicio.get("categoria", "Sin Categoria")
        self._servicios_por_categoria.setdefault(categoria, []).append(servicio)

    def _indexar_servicio_por_zona(self, servicio: dict) -> None:
        zona = servicio.get("zona", "Sin Zona")
        self._servicios_por_zona.setdefault(zona, []).append(servicio)


    def _indexar_interpretes(self, interpretes: List[dict]) -> None:
        """Indexa intérpretes en HashMaps."""
        for interprete in interpretes:
            iid = interprete.get("id")
            if iid is None:
                continue

            self._interpretes_por_id[iid] = interprete

            # Especialidades
            especialidades = interprete.get("especialidades", [])
            for esp in especialidades:
                self._interpretes_por_especialidad.setdefault(esp, []).append(interprete)

    # ========================================================================
    # PROPERTIES
    # ========================================================================

    @property
    def servicios_por_id(self) -> Dict[str, dict]:
        return self._servicios_por_id

    @property
    def interpretes_por_id(self) -> Dict[str, dict]:
        return self._interpretes_por_id

    @property
    def servicios_por_categoria(self) -> Dict[str, List[dict]]:
        return self._servicios_por_categoria

    @property
    def servicios_por_zona(self) -> Dict[str, List[dict]]:
        return self._servicios_por_zona

    @property
    def interpretes_por_especialidad(self) -> Dict[str, List[dict]]:
        return self._interpretes_por_especialidad

    # ========================================================================
    # MÉTODOS DE BÚSQUEDA DE SERVICIOS
    # ========================================================================

    def buscar_servicio_por_id(self, id: str) -> Optional[dict]:
        return self.servicios_por_id.get(id)

    def buscar_servicios_por_categoria(self, categoria: str) -> List[dict]:
        return list(self.servicios_por_categoria.get(categoria, []))

    def buscar_servicios_por_zona(self, zona: str) -> List[dict]:
        return list(self.servicios_por_zona.get(zona, []))

    def buscar_servicios_por_texto(self, texto: str) -> List[dict]:
        texto_lower = texto.lower()
        resultados = []

        for servicio in self.servicios_por_id.values():
            if texto_lower in servicio.get("nombre", "").lower():
                resultados.append(servicio)
                continue

            if texto_lower in servicio.get("direccion", "").lower():
                resultados.append(servicio)
                continue

            for caract in servicio.get("caracteristicas_accesibilidad", []):
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

        if categoria:
            candidatos = list(self.servicios_por_categoria.get(categoria, []))
        elif zona:
            candidatos = list(self.servicios_por_zona.get(zona, []))
        else:
            candidatos = list(self.servicios_por_id.values())

        resultados = []
        for servicio in candidatos:

            if subcategoria and servicio.get("subcategoria") != subcategoria:
                continue

            if zona and servicio.get("zona") != zona:
                continue

            if tiene_interprete is not None:
                if bool(servicio.get("tiene_interprete_lsc")) != bool(tiene_interprete):
                    continue

            resultados.append(servicio)

        return resultados

    # ========================================================================
    # MÉTODOS DE BÚSQUEDA DE INTÉRPRETES
    # ========================================================================

    def buscar_interprete_por_id(self, id: str) -> Optional[dict]:
        return self.interpretes_por_id.get(id)

    def buscar_interpretes_por_especialidad(self, especialidad: str) -> List[dict]:
        return list(self.interpretes_por_especialidad.get(especialidad, []))

    def buscar_interpretes_por_zona(self, zona: str) -> List[dict]:
        resultados = []
        for interprete in self.interpretes_por_id.values():
            if zona in interprete.get("zonas_cobertura", []):
                resultados.append(interprete)
        return resultados

    def filtrar_interpretes(
        self,
        especialidad: Optional[str] = None,
        zona: Optional[str] = None,
        disponibilidad: Optional[str] = None,
    ) -> List[dict]:

        if especialidad:
            candidatos = self.buscar_interpretes_por_especialidad(especialidad)
        else:
            candidatos = list(self.interpretes_por_id.values())

        resultados = []

        palabras_clave = {
            "inmediata": ["disponible", "inmediata", "ahora"],
            "tiempo_completo": ["tiempo completo", "completo", "full"],
            "por_horas": ["horas", "por hora"],
            "fines_semana": ["fin", "semana", "sábado", "domingo"],
        }

        for interprete in candidatos:
            if zona and zona not in interprete.get("zonas_cobertura", []):
                continue

            if disponibilidad:
                keywords = palabras_clave.get(disponibilidad.lower(), [])
                disp_texto = interprete.get("disponibilidad", "").lower()
                if not any(kw in disp_texto for kw in keywords):
                    continue

            resultados.append(interprete)

        return resultados

    def obtener_todas_categorias(self) -> List[str]:
        return list(self.servicios_por_categoria.keys())


def crear_buscador_desde_mock() -> BuscadorServicios:
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
