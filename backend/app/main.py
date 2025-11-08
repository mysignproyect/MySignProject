from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routes.api import router as api_router
from app.utils.errors import (
    RecursoNoEncontrado,
    ParametroInvalido,
    ErrorValidacion,
    formato_error_response
)

app = FastAPI(
    title="My Sign API",
    description="API del MVP de My Sign - Servicios e Intérpretes LSC en Medellín",
    version="0.2.0"  # Actualizado a v0.2.0 para Checkpoint #2
)

# ============================================================================
# CONFIGURACIÓN DE CORS (Cross-Origin Resource Sharing)
# ============================================================================
# Permite que el frontend (React/Vite) pueda hacer peticiones a esta API
# durante el desarrollo local.
#
# Origins permitidos:
# - localhost:3000 -> Create React App (CRA) default
# - localhost:5173 -> Vite default
# - 127.0.0.1:3000 y 127.0.0.1:5173 -> Variantes con IP local
#
# IMPORTANTE: En producción, cambiar allow_origins a la URL específica del frontend desplegado
# ============================================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # React (Create React App)
        "http://localhost:5173",      # Vite
        "http://127.0.0.1:3000",      # Variante con IP local
        "http://127.0.0.1:5173"       # Variante con IP local
    ],
    allow_credentials=True,           # Permitir cookies y credenciales
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Métodos HTTP permitidos
    allow_headers=["*"],              # Permitir todos los headers
)


# ============================================================================
# MANEJADORES DE EXCEPCIONES PERSONALIZADAS
# ============================================================================

@app.exception_handler(RecursoNoEncontrado)
async def recurso_no_encontrado_handler(request: Request, exc: RecursoNoEncontrado):
    """
    Maneja excepciones cuando un recurso no es encontrado.
    
    Retorna código HTTP 404 con mensaje en español.
    """
    return JSONResponse(
        status_code=404,
        content=formato_error_response(
            tipo="RecursoNoEncontrado",
            mensaje=str(exc)
        )
    )


@app.exception_handler(ParametroInvalido)
async def parametro_invalido_handler(request: Request, exc: ParametroInvalido):
    """
    Maneja excepciones cuando un parámetro tiene un valor inválido.
    
    Retorna código HTTP 400 con mensaje en español.
    """
    return JSONResponse(
        status_code=400,
        content=formato_error_response(
            tipo="ParametroInvalido",
            mensaje=str(exc)
        )
    )


@app.exception_handler(ErrorValidacion)
async def error_validacion_handler(request: Request, exc: ErrorValidacion):
    """
    Maneja excepciones de validación de datos.
    
    Retorna código HTTP 422 con mensaje en español.
    """
    return JSONResponse(
        status_code=422,
        content=formato_error_response(
            tipo="ErrorValidacion",
            mensaje=str(exc)
        )
    )


# ============================================================================
# RUTAS
# ============================================================================

# Ruta raíz
@app.get("/", summary="Inicio", description="Ruta de prueba para verificar que la API está activa.")
def read_root():
    """
    Endpoint de prueba que confirma que la API está corriendo correctamente.
    """
    return {
        "message": "My Sign API",
        "version": "0.2.0",
        "status": "active"
    }


app.include_router(api_router)