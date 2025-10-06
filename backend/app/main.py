"""
Módulo principal de la API My Sign.

Este archivo inicializa la aplicación FastAPI, configura el middleware CORS
y define la ruta raíz del proyecto. Todas las rutas adicionales se añadirán
en app/routes/.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Inicialización de la aplicación FastAPI
app = FastAPI(
    title="My Sign API",
    description="API principal para la aplicación My Sign. Maneja servicios e intérpretes en LSC.",
    version="1.0.0"
)

# Configuración de CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción se debe restringir a dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """
    Ruta raíz de prueba para verificar que la API funciona correctamente.
    """
    return {"message": "My Sign API"}
