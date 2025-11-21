"""
Rutas/Endpoints principales de la API My Sign.

CHECKPOINT #2:
- Se agregaron endpoints de búsqueda avanzada
- Se implementó paginación opcional
- Se agregó ordenamiento de resultados
- Se mejoró manejo de errores con excepciones personalizadas
- Se agregó endpoint de estadísticas
"""

from fastapi import APIRouter, Query
from typing import List, Optional, Dict, Any, Union
from app.models.schemas import Servicio, Interprete, EstadisticasResponse
from app.services.buscador import BuscadorServicios
from app.services.categoria_tree import (
    inicializar_arbol_con_mock as inicializar_arbol_categorias,
)
from app.utils.pagination import paginar_resultados
from app.utils.errors import RecursoNoEncontrado, ParametroInvalido, ErrorValidacion
from data.mock_data import SERVICIOS_MOCK, INTERPRETES_MOCK

# ============================================================================
# INICIALIZACIÓN DE ESTRUCTURAS DE DATOS
# ============================================================================
# Se crea una instancia global del buscador basado en HashMaps (O(1) promedio por búsqueda)
buscador = BuscadorServicios(SERVICIOS_MOCK, INTERPRETES_MOCK)

# Se crea una instancia del árbol de categorías (para jerarquía de servicios)
arbol = inicializar_arbol_categorias()

# Inicializamos el router principal de FastAPI
router = APIRouter(prefix="/api", tags=["My Sign API"])


# ============================================================================
# FUNCIONES HELPER PARA ORDENAMIENTO
# ============================================================================


def ordenar_servicios(
    servicios: List[dict], sort_by: str = "nombre", order: str = "asc"
) -> List[dict]:
    """
    Ordena una lista de servicios según el criterio especificado.

    Args:
        servicios: Lista de servicios a ordenar
        sort_by: Campo por el cual ordenar (nombre, zona, distancia)
        order: Orden ascendente (asc) o descendente (desc)

    Returns:
        Lista de servicios ordenada

    Complejidad: O(n log n) donde n = cantidad de servicios
    """
    # Si sort_by no es válido, usar nombre por defecto
    if sort_by not in ["nombre", "zona", "distancia"]:
        sort_by = "nombre"

    # Determinar si es orden reverso
    reverse = order.lower() == "desc"

    # Ordenar según el campo
    if sort_by == "distancia":
        # Para distancia, manejar valores None (ponerlos al final)
        return sorted(
            servicios,
            key=lambda x: (
                x.get("distancia_aproximada") is None,
                x.get("distancia_aproximada", float("inf")),
            ),
            reverse=reverse,
        )
    else:
        # Para nombre y zona, ordenar alfabéticamente
        return sorted(
            servicios, key=lambda x: str(x.get(sort_by, "")).lower(), reverse=reverse
        )


def ordenar_interpretes(
    interpretes: List[dict], sort_by: str = "nombre", order: str = "asc"
) -> List[dict]:
    """
    Ordena una lista de intérpretes según el criterio especificado.

    Args:
        interpretes: Lista de intérpretes a ordenar
        sort_by: Campo por el cual ordenar (nombre, experiencia)
        order: Orden ascendente (asc) o descendente (desc)

    Returns:
        Lista de intérpretes ordenada

    Complejidad: O(n log n) donde n = cantidad de intérpretes
    """
    # Si sort_by no es válido, usar nombre por defecto
    if sort_by not in ["nombre", "experiencia"]:
        sort_by = "nombre"

    # Determinar si es orden reverso
    reverse = order.lower() == "desc"

    # Ordenar según el campo
    if sort_by == "experiencia":
        # Para experiencia (años_experiencia), ordenar numéricamente
        return sorted(
            interpretes, key=lambda x: x.get("años_experiencia", 0), reverse=reverse
        )
    else:
        # Para nombre, ordenar alfabéticamente
        return sorted(
            interpretes, key=lambda x: str(x.get("nombre", "")).lower(), reverse=reverse
        )


# ============================================================================
# ENDPOINTS DE CATEGORÍAS
# ============================================================================


@router.get(
    "/categorias",
    response_model=List[str],
    summary="Obtener categorías principales",
    description="Devuelve una lista con las 3 categorías principales del sistema: Salud, Educación, Gobierno.",
    tags=["Categorías"],
)
def get_categorias():
    """
    Obtiene las categorías principales de servicios.

    Estructura de datos usada: Árbol (acceso a nodos de primer nivel)
    Complejidad: O(1)

    Returns:
        Lista con las categorías: ["Salud", "Educación", "Gobierno"]
    """
    return arbol.obtener_todas_categorias()


@router.get(
    "/categorias/{categoria}/subcategorias",
    response_model=List[str],
    summary="Obtener subcategorías de una categoría",
    description="Devuelve las subcategorías disponibles de una categoría principal (ej: Hospitales, Clínicas para Salud).",
    tags=["Categorías"],
)
def get_subcategorias(categoria: str):
    """
    Obtiene las subcategorías de una categoría principal específica.

    Args:
        categoria: Nombre de la categoría (Salud, Educación, Gobierno)

    Returns:
        Lista de subcategorías

    Raises:
        RecursoNoEncontrado: Si la categoría no existe

    Estructura de datos usada: Árbol (acceso directo a nodo)
    Complejidad: O(1)

    Ejemplo:
        GET /api/categorias/Salud/subcategorias
        Retorna: ["Hospitales", "Clínicas", "Centros de Salud"]
    """
    # Validar que la categoría sea una de las 3 principales
    categorias_validas = ["Salud", "Educación", "Gobierno"]
    if categoria not in categorias_validas:
        raise RecursoNoEncontrado(
            f"Categoría '{categoria}' no encontrada. Categorías válidas: {', '.join(categorias_validas)}"
        )

    # Obtener subcategorías del árbol
    subcategorias = arbol.obtener_subcategorias(categoria)

    # Si no hay subcategorías (no debería pasar), retornar array vacío
    return subcategorias


# ============================================================================
# ENDPOINTS DE SERVICIOS
# ============================================================================


@router.get(
    "/servicios",
    response_model=Union[List[Servicio], Dict[str, Any]],
    summary="Buscar servicios con filtros, paginación y ordenamiento",
    description="Busca servicios con filtros opcionales, paginación y ordenamiento. Si se especifica page/limit, retorna objeto con data y metadata.",
    tags=["Servicios"],
)
def get_servicios(
    categoria: Optional[str] = Query(
        None, description="Filtra por categoría del servicio"
    ),
    subcategoria: Optional[str] = Query(
        None, description="Filtra por subcategoría específica"
    ),
    zona: Optional[str] = Query(None, description="Filtra por zona de Medellín"),
    tiene_interprete: Optional[bool] = Query(
        None, description="Filtra servicios con intérprete LSC"
    ),
    sort_by: Optional[str] = Query(
        "nombre", description="Ordenar por: nombre, zona, distancia"
    ),
    order: Optional[str] = Query("asc", description="Orden: asc o desc"),
    page: Optional[int] = Query(
        None, ge=1, description="Número de página (inicia paginación)"
    ),
    limit: Optional[int] = Query(
        10, ge=1, le=50, description="Items por página (máx 50)"
    ),
):
    """
    Busca servicios con filtros, ordenamiento y paginación opcionales.

    ACTUALIZADO (Checkpoint #2):
    - Soporta subcategoría
    - Paginación opcional
    - Ordenamiento configurable

    Args:
        categoria: Categoría principal (opcional)
        subcategoria: Subcategoría específica (opcional)
        zona: Zona geográfica (opcional)
        tiene_interprete: Si requiere intérprete LSC (opcional)
        sort_by: Campo de ordenamiento (default: nombre)
        order: Dirección de orden (default: asc)
        page: Número de página (si se especifica, activa paginación)
        limit: Items por página (default: 10)

    Returns:
        Si page es None: List[Servicio]
        Si page está definido: {"data": List[Servicio], "metadata": {...}}

    Estructura de datos usada: HashMap (filtrado eficiente)
    Complejidad: O(k log k) donde k = servicios filtrados (por ordenamiento)
    """
    # Filtrar servicios
    resultados = buscador.filtrar_servicios(
        categoria=categoria,
        subcategoria=subcategoria,
        zona=zona,
        tiene_interprete=tiene_interprete,
    )

    # Ordenar resultados
    resultados = ordenar_servicios(resultados, sort_by, order)

    # Si se especificó paginación, aplicarla
    if page is not None:
        try:
            return paginar_resultados(resultados, page, limit)
        except ValueError as e:
            raise ErrorValidacion(str(e))

    # Sin paginación, retornar lista completa
    return resultados


@router.get(
    "/servicios/buscar",
    response_model=Union[List[Servicio], Dict[str, Any]],
    summary="Búsqueda de servicios por texto libre",
    description="Busca servicios por texto con paginación y ordenamiento opcionales.",
    tags=["Servicios"],
)
def buscar_servicios_por_texto(
    q: str = Query(..., min_length=1, description="Texto a buscar"),
    sort_by: Optional[str] = Query(
        "nombre", description="Ordenar por: nombre, zona, distancia"
    ),
    order: Optional[str] = Query("asc", description="Orden: asc o desc"),
    page: Optional[int] = Query(None, ge=1, description="Número de página"),
    limit: Optional[int] = Query(10, ge=1, le=50, description="Items por página"),
):
    """
    Busca servicios por texto libre con ordenamiento y paginación opcionales.

    Args:
        q: Texto de búsqueda (requerido)
        sort_by: Campo de ordenamiento
        order: Dirección de orden
        page: Número de página (opcional)
        limit: Items por página

    Returns:
        Lista de servicios o respuesta paginada

    Raises:
        ErrorValidacion: Si q está vacío

    Complejidad: O(n + k log k) donde n = total servicios, k = resultados
    """
    # Validación: asegurar que no sea solo espacios
    if not q.strip():
        raise ErrorValidacion("El parámetro de búsqueda no puede estar vacío")

    # Buscar servicios
    resultados = buscador.buscar_servicios_por_texto(q)

    # Ordenar resultados
    resultados = ordenar_servicios(resultados, sort_by, order)

    # Aplicar paginación si se solicitó
    if page is not None:
        try:
            return paginar_resultados(resultados, page, limit)
        except ValueError as e:
            raise ErrorValidacion(str(e))

    return resultados


@router.get(
    "/servicios/zona/{zona}",
    response_model=Union[List[Servicio], Dict[str, Any]],
    summary="Servicios por zona geográfica",
    description="Obtiene servicios de una zona con filtros, paginación y ordenamiento opcionales.",
    tags=["Servicios"],
)
def get_servicios_por_zona(
    zona: str,
    categoria: Optional[str] = Query(
        None, description="Filtro adicional por categoría"
    ),
    tiene_interprete: Optional[bool] = Query(
        None, description="Filtro adicional por intérprete LSC"
    ),
    sort_by: Optional[str] = Query(
        "nombre", description="Ordenar por: nombre, zona, distancia"
    ),
    order: Optional[str] = Query("asc", description="Orden: asc o desc"),
    page: Optional[int] = Query(None, ge=1, description="Número de página"),
    limit: Optional[int] = Query(10, ge=1, le=50, description="Items por página"),
):
    """
    Obtiene servicios de una zona específica con ordenamiento y paginación.

    Args:
        zona: Zona geográfica (requerido)
        categoria: Filtro adicional (opcional)
        tiene_interprete: Filtro adicional (opcional)
        sort_by: Campo de ordenamiento
        order: Dirección de orden
        page: Número de página (opcional)
        limit: Items por página

    Returns:
        Lista de servicios o respuesta paginada

    Raises:
        ParametroInvalido: Si la zona no es válida
    """
    # Validar zona
    zonas_validas = ["Centro", "Norte", "Sur", "Oriente", "Occidente"]
    if zona not in zonas_validas:
        raise ParametroInvalido(
            f"Zona '{zona}' no válida. Zonas disponibles: {', '.join(zonas_validas)}"
        )

    # Filtrar servicios
    resultados = buscador.filtrar_servicios(
        zona=zona, categoria=categoria, tiene_interprete=tiene_interprete
    )

    # Ordenar
    resultados = ordenar_servicios(resultados, sort_by, order)

    # Paginar si se solicitó
    if page is not None:
        try:
            return paginar_resultados(resultados, page, limit)
        except ValueError as e:
            raise ErrorValidacion(str(e))

    return resultados


@router.get(
    "/servicios/{servicio_id}",
    response_model=Servicio,
    summary="Obtener detalle de servicio",
    description="Devuelve la información completa de un servicio específico por su ID único.",
    tags=["Servicios"],
)
def get_servicio_por_id(servicio_id: str):
    """
    Obtiene el detalle completo de un servicio por su ID.

    Args:
        servicio_id: ID único del servicio

    Returns:
        Servicio completo

    Raises:
        RecursoNoEncontrado: Si el servicio no existe

    Complejidad: O(1)
    """
    servicio = buscador.buscar_servicio_por_id(servicio_id)
    if not servicio:
        raise RecursoNoEncontrado(f"Servicio con ID '{servicio_id}' no encontrado")
    return servicio


# ============================================================================
# ENDPOINTS DE INTÉRPRETES
# ============================================================================


@router.get(
    "/interpretes",
    response_model=Union[List[Interprete], Dict[str, Any]],
    summary="Listar intérpretes LSC con filtros, paginación y ordenamiento",
    description="Devuelve lista de intérpretes con filtros opcionales, paginación y ordenamiento.",
    tags=["Intérpretes"],
)
def get_interpretes(
    especialidad: Optional[str] = Query(None, description="Filtra por especialidad"),
    zona: Optional[str] = Query(None, description="Filtra por zona de cobertura"),
    disponibilidad: Optional[str] = Query(
        None, description="Filtra por tipo de disponibilidad"
    ),
    sort_by: Optional[str] = Query(
        "nombre", description="Ordenar por: nombre, experiencia"
    ),
    order: Optional[str] = Query("asc", description="Orden: asc o desc"),
    page: Optional[int] = Query(None, ge=1, description="Número de página"),
    limit: Optional[int] = Query(10, ge=1, le=50, description="Items por página"),
):
    """
    Lista intérpretes con filtros, ordenamiento y paginación opcionales.

    ACTUALIZADO (Checkpoint #2):
    - Soporta múltiples filtros combinables
    - Paginación opcional
    - Ordenamiento configurable

    Args:
        especialidad: Especialidad (opcional)
        zona: Zona de cobertura (opcional)
        disponibilidad: Tipo de disponibilidad (opcional)
        sort_by: Campo de ordenamiento (default: nombre)
        order: Dirección de orden (default: asc)
        page: Número de página (opcional)
        limit: Items por página

    Returns:
        Lista de intérpretes o respuesta paginada

    Complejidad: O(k log k) donde k = intérpretes filtrados
    """
    # Si no hay filtros, retornar todos
    if not any([especialidad, zona, disponibilidad]):
        resultados = list(buscador.interpretes_por_id.values())
    else:
        # Usar filtrado combinado
        resultados = buscador.filtrar_interpretes(
            especialidad=especialidad, zona=zona, disponibilidad=disponibilidad
        )

    # Ordenar
    resultados = ordenar_interpretes(resultados, sort_by, order)

    # Paginar si se solicitó
    if page is not None:
        try:
            return paginar_resultados(resultados, page, limit)
        except ValueError as e:
            raise ErrorValidacion(str(e))

    return resultados


@router.get(
    "/interpretes/especialidad/{especialidad}",
    response_model=Union[List[Interprete], Dict[str, Any]],
    summary="Intérpretes por especialidad",
    description="Obtiene intérpretes de una especialidad con paginación y ordenamiento opcionales.",
    tags=["Intérpretes"],
)
def get_interpretes_por_especialidad(
    especialidad: str,
    sort_by: Optional[str] = Query(
        "nombre", description="Ordenar por: nombre, experiencia"
    ),
    order: Optional[str] = Query("asc", description="Orden: asc o desc"),
    page: Optional[int] = Query(None, ge=1, description="Número de página"),
    limit: Optional[int] = Query(10, ge=1, le=50, description="Items por página"),
):
    """
    Obtiene intérpretes por especialidad con ordenamiento y paginación.

    Args:
        especialidad: Especialidad del intérprete
        sort_by: Campo de ordenamiento
        order: Dirección de orden
        page: Número de página (opcional)
        limit: Items por página

    Returns:
        Lista de intérpretes o respuesta paginada

    Raises:
        ParametroInvalido: Si la especialidad no es válida
    """
    # Validar especialidad
    especialidades_validas = ["Médica", "Legal", "Educativa", "Empresarial", "Eventos"]
    if especialidad not in especialidades_validas:
        raise ParametroInvalido(
            f"Especialidad '{especialidad}' no válida. Especialidades disponibles: {', '.join(especialidades_validas)}"
        )

    # Buscar intérpretes
    resultados = buscador.buscar_interpretes_por_especialidad(especialidad)

    # Ordenar
    resultados = ordenar_interpretes(resultados, sort_by, order)

    # Paginar si se solicitó
    if page is not None:
        try:
            return paginar_resultados(resultados, page, limit)
        except ValueError as e:
            raise ErrorValidacion(str(e))

    return resultados


@router.get(
    "/interpretes/zona/{zona}",
    response_model=Union[List[Interprete], Dict[str, Any]],
    summary="Intérpretes por zona de cobertura",
    description="Obtiene intérpretes que cubran una zona con filtros, paginación y ordenamiento opcionales.",
    tags=["Intérpretes"],
)
def get_interpretes_por_zona(
    zona: str,
    especialidad: Optional[str] = Query(
        None, description="Filtro adicional por especialidad"
    ),
    sort_by: Optional[str] = Query(
        "nombre", description="Ordenar por: nombre, experiencia"
    ),
    order: Optional[str] = Query("asc", description="Orden: asc o desc"),
    page: Optional[int] = Query(None, ge=1, description="Número de página"),
    limit: Optional[int] = Query(10, ge=1, le=50, description="Items por página"),
):
    """
    Obtiene intérpretes por zona con ordenamiento y paginación.

    Args:
        zona: Zona de cobertura
        especialidad: Filtro adicional (opcional)
        sort_by: Campo de ordenamiento
        order: Dirección de orden
        page: Número de página (opcional)
        limit: Items por página

    Returns:
        Lista de intérpretes o respuesta paginada

    Raises:
        ParametroInvalido: Si la zona no es válida
    """
    # Validar zona
    zonas_validas = ["Centro", "Norte", "Sur", "Oriente", "Occidente"]
    if zona not in zonas_validas:
        raise ParametroInvalido(
            f"Zona '{zona}' no válida. Zonas disponibles: {', '.join(zonas_validas)}"
        )

    # Buscar intérpretes
    if especialidad:
        resultados = buscador.filtrar_interpretes(especialidad=especialidad, zona=zona)
    else:
        resultados = buscador.buscar_interpretes_por_zona(zona)

    # Ordenar
    resultados = ordenar_interpretes(resultados, sort_by, order)

    # Paginar si se solicitó
    if page is not None:
        try:
            return paginar_resultados(resultados, page, limit)
        except ValueError as e:
            raise ErrorValidacion(str(e))

    return resultados


@router.get(
    "/interpretes/disponibilidad",
    response_model=Union[List[Interprete], Dict[str, Any]],
    summary="Intérpretes por disponibilidad",
    description="Filtra intérpretes por disponibilidad con filtros, paginación y ordenamiento opcionales.",
    tags=["Intérpretes"],
)
def get_interpretes_por_disponibilidad(
    tipo: str = Query(
        ..., description="Tipo: inmediata, tiempo_completo, por_horas, fines_semana"
    ),
    especialidad: Optional[str] = Query(
        None, description="Filtro adicional por especialidad"
    ),
    zona: Optional[str] = Query(None, description="Filtro adicional por zona"),
    sort_by: Optional[str] = Query(
        "nombre", description="Ordenar por: nombre, experiencia"
    ),
    order: Optional[str] = Query("asc", description="Orden: asc o desc"),
    page: Optional[int] = Query(None, ge=1, description="Número de página"),
    limit: Optional[int] = Query(10, ge=1, le=50, description="Items por página"),
):
    """
    Filtra intérpretes por disponibilidad con ordenamiento y paginación.

    Args:
        tipo: Tipo de disponibilidad (requerido)
        especialidad: Filtro adicional (opcional)
        zona: Filtro adicional (opcional)
        sort_by: Campo de ordenamiento
        order: Dirección de orden
        page: Número de página (opcional)
        limit: Items por página

    Returns:
        Lista de intérpretes o respuesta paginada

    Raises:
        ParametroInvalido: Si el tipo no es válido
    """
    # Validar tipo
    tipos_validos = ["inmediata", "tiempo_completo", "por_horas", "fines_semana"]
    if tipo.lower() not in tipos_validos:
        raise ParametroInvalido(
            f"Tipo '{tipo}' no válido. Tipos disponibles: {', '.join(tipos_validos)}"
        )

    # Filtrar intérpretes
    resultados = buscador.filtrar_interpretes(
        especialidad=especialidad, zona=zona, disponibilidad=tipo
    )

    # Ordenar
    resultados = ordenar_interpretes(resultados, sort_by, order)

    # Paginar si se solicitó
    if page is not None:
        try:
            return paginar_resultados(resultados, page, limit)
        except ValueError as e:
            raise ErrorValidacion(str(e))

    return resultados


@router.get(
    "/interpretes/{interprete_id}",
    response_model=Interprete,
    summary="Obtener detalle de intérprete",
    description="Devuelve la información completa de un intérprete LSC por su ID único.",
    tags=["Intérpretes"],
)
def get_interprete_por_id(interprete_id: str):
    """
    Obtiene el detalle completo de un intérprete por su ID.

    Args:
        interprete_id: ID único del intérprete

    Returns:
        Intérprete completo

    Raises:
        RecursoNoEncontrado: Si el intérprete no existe

    Complejidad: O(1)
    """
    interprete = buscador.buscar_interprete_por_id(interprete_id)
    if not interprete:
        raise RecursoNoEncontrado(f"Intérprete con ID '{interprete_id}' no encontrado")
    return interprete


# ============================================================================
# ENDPOINT DE ESTADÍSTICAS
# ============================================================================


@router.get(
    "/estadisticas",
    response_model=EstadisticasResponse,
    summary="Obtener estadísticas generales del sistema",
    description="Devuelve un resumen cuantitativo de servicios, intérpretes, categorías y zonas disponibles.",
    tags=["Estadísticas"],
)
def get_estadisticas():
    """
    Obtiene estadísticas generales del sistema.

    Calcula totales y distribuciones usando los HashMaps existentes
    para máxima eficiencia.

    Returns:
        EstadisticasResponse con totales y distribuciones

    Estructura de datos usada: HashMaps (acceso O(1) a conteos)
    Complejidad: O(c + e) donde c = categorías, e = especialidades

    Ejemplo de respuesta:
        {
            "total_servicios": 10,
            "servicios_por_categoria": {"Salud": 3, "Educación": 3, ...},
            "total_interpretes": 4,
            "interpretes_por_especialidad": {"Médica": 2, "Legal": 2, ...},
            "zonas_disponibles": ["Centro", "Norte", "Sur", "Oriente", "Occidente"]
        }
    """
    # Calcular totales usando HashMaps (O(1) para acceder a len)
    total_servicios = len(buscador.servicios_por_id)
    total_interpretes = len(buscador.interpretes_por_id)

    # Servicios por categoría (O(c) donde c = número de categorías)
    servicios_por_categoria = {
        categoria: len(servicios)
        for categoria, servicios in buscador.servicios_por_categoria.items()
    }

    # Intérpretes por especialidad (O(e) donde e = número de especialidades)
    interpretes_por_especialidad = {
        especialidad: len(interpretes)
        for especialidad, interpretes in buscador.interpretes_por_especialidad.items()
    }

    # Zonas disponibles (fijas)
    zonas_disponibles = ["Centro", "Norte", "Sur", "Oriente", "Occidente"]

    return EstadisticasResponse(
        total_servicios=total_servicios,
        servicios_por_categoria=servicios_por_categoria,
        total_interpretes=total_interpretes,
        interpretes_por_especialidad=interpretes_por_especialidad,
        zonas_disponibles=zonas_disponibles,
    )
