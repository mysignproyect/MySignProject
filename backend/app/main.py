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

# Configuración de CORS (para permitir acceso desde frontend o Postman)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta raíz
@app.get("/", summary="Inicio", description="Ruta de prueba para verificar que la API está activa.")
def read_root():
    return {"message": "My Sign API"}

# Registro del router principal
app.include_router(api_router)
