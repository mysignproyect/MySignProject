from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.schemas import Servicio, Interprete
from app.services.buscador import BuscadorServicios
from app.services.categoria_tree import inicializar_arbol_con_mock as inicializar_arbol_categorias
from data.mock_data import SERVICIOS_MOCK, INTERPRETES_MOCK

# Se crea una instancia global del buscador basado en HashMaps (O(1) promedio por búsqueda)
buscador = BuscadorServicios(SERVICIOS_MOCK, INTERPRETES_MOCK)

# Se crea una instancia del árbol de categorías (para jerarquía de servicios)
arbol = inicializar_arbol_categorias()

# Inicializamos el router principal de FastAPI
router = APIRouter(prefix="/api", tags=["My Sign API"])


@router.get("/categorias", response_model=List[str], summary="Obtener categorías principales", description="Devuelve una lista con las categorías principales del sistema (Salud, Educación, Gobierno, Intérpretes).")
def get_categorias():
    return arbol.obtener_todas_categorias()


@router.get("/servicios", response_model=List[Servicio], summary="Buscar servicios", description="Busca servicios filtrando opcionalmente por categoría, zona o si tienen intérprete LSC disponible.")
def get_servicios(
    categoria: Optional[str] = Query(None, description="Filtra por categoría del servicio"),
    zona: Optional[str] = Query(None, description="Filtra por zona de Medellín"),
    tiene_interprete: Optional[bool] = Query(None, description="Filtra servicios que cuenten con intérprete LSC")
):
    return buscador.filtrar_servicios(categoria, zona, tiene_interprete)


@router.get("/servicios/{servicio_id}", response_model=Servicio, summary="Obtener detalle de servicio", description="Devuelve la información detallada de un servicio por su ID único.")
def get_servicio_por_id(servicio_id: str):
    """
    Complejidad: O(1) gracias al uso de HashMap (diccionario Python).
    """
    servicio = buscador.buscar_servicio_por_id(servicio_id)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio


@router.get("/servicios/categoria/{categoria}", response_model=List[Servicio], summary="Listar servicios por categoría", description="Devuelve todos los servicios que pertenecen a una categoría específica (por ejemplo, Salud o Educación).")
def get_servicios_por_categoria(categoria: str):
    servicios = buscador.buscar_servicios_por_categoria(categoria)
    if not servicios:
        raise HTTPException(status_code=404, detail="No se encontraron servicios para esta categoría")
    return servicios


@router.get("/interpretes", response_model=List[Interprete], summary="Listar intérpretes", description="Devuelve una lista de intérpretes LSC. Permite filtrar por especialidad (Médica, Legal, etc.).")
def get_interpretes(especialidad: Optional[str] = Query(None, description="Filtra intérpretes por especialidad (Médica, Legal, etc.)")):
    """
    Complejidad: O(1) promedio por búsqueda en HashMap.
    """
    if especialidad:
        return buscador.buscar_interpretes_por_especialidad(especialidad)
    return list(buscador.interpretes_por_id.values())


@router.get("/interpretes/{interprete_id}", response_model=Interprete, summary="Obtener detalle de intérprete", description="Devuelve la información completa de un intérprete LSC por su ID único.")
def get_interprete_por_id(interprete_id: str):
    interprete = buscador.buscar_interprete_por_id(interprete_id)
    if not interprete:
        raise HTTPException(status_code=404, detail="Intérprete no encontrado")
    return interprete
