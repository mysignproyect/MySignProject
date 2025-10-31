"""
Rutas/Endpoints principales de la API My Sign.

CHECKPOINT #2: Se agregaron nuevos endpoints para búsqueda avanzada de servicios.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.schemas import Servicio, Interprete
from app.services.buscador import BuscadorServicios
from app.services.categoria_tree import inicializar_arbol_con_mock as inicializar_arbol_categorias
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
# ENDPOINTS DE CATEGORÍAS
# ============================================================================

@router.get(
    "/categorias",
    response_model=List[str],
    summary="Obtener categorías principales",
    description="Devuelve una lista con las 3 categorías principales del sistema: Salud, Educación, Gobierno.",
    tags=["Categorías"]
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
    tags=["Categorías"]
)
def get_subcategorias(categoria: str):
    """
    Obtiene las subcategorías de una categoría principal específica.
    
    Args:
        categoria: Nombre de la categoría (Salud, Educación, Gobierno)
    
    Returns:
        Lista de subcategorías
    
    Raises:
        HTTPException 404: Si la categoría no existe
    
    Estructura de datos usada: Árbol (acceso directo a nodo)
    Complejidad: O(1)
    
    Ejemplo:
        GET /api/categorias/Salud/subcategorias
        Retorna: ["Hospitales", "Clínicas", "Centros de Salud"]
    """
    # Validar que la categoría sea una de las 3 principales
    categorias_validas = ["Salud", "Educación", "Gobierno"]
    if categoria not in categorias_validas:
        raise HTTPException(
            status_code=404,
            detail=f"Categoría '{categoria}' no encontrada. Categorías válidas: {', '.join(categorias_validas)}"
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
    response_model=List[Servicio],
    summary="Buscar servicios con filtros",
    description="Busca servicios filtrando por categoría, subcategoría, zona y/o disponibilidad de intérprete LSC. Todos los filtros son opcionales y se combinan con lógica AND.",
    tags=["Servicios"]
)
def get_servicios(
    categoria: Optional[str] = Query(None, description="Filtra por categoría del servicio (Salud, Educación, Gobierno)"),
    subcategoria: Optional[str] = Query(None, description="Filtra por subcategoría específica (ej: Hospitales, Universidades)"),
    zona: Optional[str] = Query(None, description="Filtra por zona de Medellín (Centro, Norte, Sur, Oriente, Occidente)"),
    tiene_interprete: Optional[bool] = Query(None, description="Filtra servicios que cuenten con intérprete LSC")
):
    """
    Busca servicios aplicando filtros combinados (lógica AND).
    
    ACTUALIZADO (Checkpoint #2): Ahora soporta filtro por subcategoría.
    
    Args:
        categoria: Categoría principal (opcional)
        subcategoria: Subcategoría específica (opcional)
        zona: Zona geográfica (opcional)
        tiene_interprete: Si requiere intérprete LSC (opcional)
    
    Returns:
        Lista de servicios que cumplan TODOS los filtros especificados.
        Si no hay resultados, retorna array vacío [] (NO error).
    
    Estructura de datos usada: HashMap (filtrado eficiente)
    Complejidad: O(k) donde k = servicios en categoría/zona seleccionada
    
    Ejemplo:
        GET /api/servicios?categoria=Salud&zona=Centro&tiene_interprete=true
    """
    # Usar el método mejorado de filtrado que ahora acepta subcategoría
    resultados = buscador.filtrar_servicios(
        categoria=categoria,
        subcategoria=subcategoria,
        zona=zona,
        tiene_interprete=tiene_interprete
    )
    
    # Retornar array vacío si no hay resultados (NO lanzar error)
    return resultados


@router.get(
    "/servicios/buscar",
    response_model=List[Servicio],
    summary="Búsqueda de servicios por texto libre",
    description="Busca servicios por texto en nombre, dirección o características de accesibilidad. Búsqueda case-insensitive.",
    tags=["Servicios"]
)
def buscar_servicios_por_texto(
    q: str = Query(..., min_length=1, description="Texto a buscar (mínimo 1 carácter)")
):
    """
    Busca servicios por texto libre en nombre, dirección y características.
    
    Args:
        q: Texto de búsqueda (requerido, mínimo 1 carácter)
    
    Returns:
        Lista de servicios que coincidan con el texto
    
    Raises:
        HTTPException 422: Si falta el parámetro q (FastAPI lo maneja automáticamente)
        HTTPException 400: Si q está vacío después de validación
    
    Estructura de datos usada: HashMap (itera sobre todos los servicios)
    Complejidad: O(n) donde n = total de servicios
    
    Ejemplo:
        GET /api/servicios/buscar?q=hospital
        GET /api/servicios/buscar?q=rampas
    """
    # Validación adicional: asegurar que no sea solo espacios
    if not q.strip():
        raise HTTPException(
            status_code=400,
            detail="El parámetro de búsqueda no puede estar vacío"
        )
    
    # Buscar en el buscador usando el nuevo método
    resultados = buscador.buscar_servicios_por_texto(q)
    
    # Retornar array vacío si no hay coincidencias (NO error)
    return resultados


@router.get(
    "/servicios/zona/{zona}",
    response_model=List[Servicio],
    summary="Servicios por zona geográfica",
    description="Obtiene servicios de una zona específica de Medellín. Permite filtros adicionales por categoría y disponibilidad de intérprete.",
    tags=["Servicios"]
)
def get_servicios_por_zona(
    zona: str,
    categoria: Optional[str] = Query(None, description="Filtro adicional por categoría"),
    tiene_interprete: Optional[bool] = Query(None, description="Filtro adicional por disponibilidad de intérprete LSC")
):
    """
    Obtiene servicios de una zona geográfica específica.
    
    Args:
        zona: Zona geográfica (Centro, Norte, Sur, Oriente, Occidente)
        categoria: Filtro adicional por categoría (opcional)
        tiene_interprete: Filtro adicional por intérprete LSC (opcional)
    
    Returns:
        Lista de servicios en la zona especificada
    
    Raises:
        HTTPException 400: Si la zona no es válida
    
    Estructura de datos usada: HashMap (acceso directo por zona)
    Complejidad: O(k) donde k = servicios en esa zona
    
    Ejemplo:
        GET /api/servicios/zona/Centro
        GET /api/servicios/zona/Norte?categoria=Salud&tiene_interprete=true
    """
    # Validar que la zona sea válida
    zonas_validas = ["Centro", "Norte", "Sur", "Oriente", "Occidente"]
    if zona not in zonas_validas:
        raise HTTPException(
            status_code=400,
            detail=f"Zona '{zona}' no válida. Zonas disponibles: {', '.join(zonas_validas)}"
        )
    
    # Usar el método de filtrado con zona como parámetro principal
    resultados = buscador.filtrar_servicios(
        zona=zona,
        categoria=categoria,
        tiene_interprete=tiene_interprete
    )
    
    # Retornar array vacío si no hay resultados (NO error)
    return resultados


@router.get(
    "/servicios/{servicio_id}",
    response_model=Servicio,
    summary="Obtener detalle de servicio",
    description="Devuelve la información completa de un servicio específico por su ID único.",
    tags=["Servicios"]
)
def get_servicio_por_id(servicio_id: str):
    """
    Obtiene el detalle completo de un servicio por su ID.
    
    Args:
        servicio_id: ID único del servicio
    
    Returns:
        Servicio completo
    
    Raises:
        HTTPException 404: Si el servicio no existe
    
    Estructura de datos usada: HashMap (acceso directo O(1))
    Complejidad: O(1)
    """
    servicio = buscador.buscar_servicio_por_id(servicio_id)
    if not servicio:
        raise HTTPException(
            status_code=404,
            detail=f"Servicio con ID '{servicio_id}' no encontrado"
        )
    return servicio


# ============================================================================
# ENDPOINTS DE INTÉRPRETES
# ============================================================================

@router.get(
    "/interpretes",
    response_model=List[Interprete],
    summary="Listar intérpretes LSC",
    description="Devuelve una lista de intérpretes de Lengua de Señas Colombiana. Permite filtrar por especialidad.",
    tags=["Intérpretes"]
)
def get_interpretes(
    especialidad: Optional[str] = Query(None, description="Filtra intérpretes por especialidad (Médica, Legal, Educativa, Empresarial, Eventos)")
):
    """
    Lista intérpretes LSC, con filtro opcional por especialidad.
    
    Args:
        especialidad: Especialidad del intérprete (opcional)
    
    Returns:
        Lista de intérpretes
    
    Estructura de datos usada: HashMap (acceso por especialidad)
    Complejidad: O(1) para buscar por especialidad, O(m) para listar todos
    
    Ejemplo:
        GET /api/interpretes
        GET /api/interpretes?especialidad=Médica
    """
    if especialidad:
        return buscador.buscar_interpretes_por_especialidad(especialidad)
    
    # Si no hay filtro, retornar todos los intérpretes
    return list(buscador.interpretes_por_id.values())


@router.get(
    "/interpretes/{interprete_id}",
    response_model=Interprete,
    summary="Obtener detalle de intérprete",
    description="Devuelve la información completa de un intérprete LSC por su ID único.",
    tags=["Intérpretes"]
)
def get_interprete_por_id(interprete_id: str):
    """
    Obtiene el detalle completo de un intérprete por su ID.
    
    Args:
        interprete_id: ID único del intérprete
    
    Returns:
        Intérprete completo
    
    Raises:
        HTTPException 404: Si el intérprete no existe
    
    Estructura de datos usada: HashMap (acceso directo O(1))
    Complejidad: O(1)
    """
    interprete = buscador.buscar_interprete_por_id(interprete_id)
    if not interprete:
        raise HTTPException(
            status_code=404,
            detail=f"Intérprete con ID '{interprete_id}' no encontrado"
        )
    return interprete