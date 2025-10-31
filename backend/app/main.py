"""
Archivo principal de la API My Sign.
Define la aplicación FastAPI, configura CORS y monta los routers de endpoints.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.api import router as api_router

app = FastAPI(
    title="My Sign API",
    description="API del MVP de My Sign - Servicios e Intérpretes LSC en Medellín",
    version="0.1.0"
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

# Ruta raíz
@app.get("/", summary="Inicio", description="Ruta de prueba para verificar que la API está activa.")
def read_root():
    """
    Endpoint de prueba que confirma que la API está corriendo correctamente.
    """
    return {"message": "My Sign API"}

# Registro del router principal con todos los endpoints
app.include_router(api_router)