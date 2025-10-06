"""
mock_data.py
-------------
Este módulo contiene datos de prueba (mock) para el proyecto My Sign.
Estos datos permiten realizar pruebas locales del backend sin necesidad
de una base de datos real durante el desarrollo del MVP.

Incluye listas de servicios accesibles e intérpretes de Lengua de Señas Colombiana (LSC)
ubicados en Medellín, con información realista y coherente con los modelos Pydantic.
"""

# ============================================
# LISTA DE SERVICIOS DE PRUEBA (SERVICIOS_MOCK)
# ============================================

# Cada servicio representa una entidad de tipo "Salud", "Educación", "Gobierno" u otra categoría,
# incluyendo datos realistas de Medellín (dirección, contacto, zona, etc.)
# Estructura basada en el modelo Servicio definido en app/models/schemas.py

SERVICIOS_MOCK = [
    # --- Servicios de Salud ---
    {
        "id": "s1",
        "nombre": "Hospital San Vicente Fundación",
        "categoria": "Salud",
        "subcategoria": "Hospital General",
        "direccion": "Carrera 51D #62-29, Medellín",
        "telefono": "+57 604 4441333",
        "whatsapp": None,
        "zona": "Norte",
        "caracteristicas_accesibilidad": ["Rampas", "Señalización en Braille", "Ascensores amplios"],
        "horarios": "Lunes a Domingo 24 horas",
        "tiene_interprete_lsc": True,
        "distancia_aproximada": 2.5
    },
    {
        "id": "s2",
        "nombre": "Clínica Las Américas",
        "categoria": "Salud",
        "subcategoria": "Clínica Privada",
        "direccion": "Diagonal 75B #2A-80, Medellín",
        "telefono": "+57 604 3421010",
        "whatsapp": "+57 3101234567",
        "zona": "Occidente",
        "caracteristicas_accesibilidad": ["Rampas", "Personal capacitado en atención a personas sordas"],
        "horarios": "Lunes a Domingo 24 horas",
        "tiene_interprete_lsc": False,
        "distancia_aproximada": 5.1
    },
    {
        "id": "s3",
        "nombre": "Hospital General de Medellín",
        "categoria": "Salud",
        "subcategoria": "Hospital Público",
        "direccion": "Calle 64 #52-59, Medellín",
        "telefono": "+57 604 3846000",
        "whatsapp": None,
        "zona": "Centro",
        "caracteristicas_accesibilidad": ["Rampas", "Baños accesibles", "Ascensores con voz"],
        "horarios": "Lunes a Domingo 24 horas",
        "tiene_interprete_lsc": True,
        "distancia_aproximada": 3.2
    },

    # --- Servicios de Educación ---
    {
        "id": "s4",
        "nombre": "Universidad de Antioquia",
        "categoria": "Educación",
        "subcategoria": "Universidad Pública",
        "direccion": "Calle 67 #53-108, Medellín",
        "telefono": "+57 604 2198332",
        "whatsapp": None,
        "zona": "Norte",
        "caracteristicas_accesibilidad": ["Rampas", "Interpretación LSC en eventos", "Señalización táctil"],
        "horarios": "Lunes a Viernes 7:00 - 18:00",
        "tiene_interprete_lsc": True,
        "distancia_aproximada": 2.0
    },
    {
        "id": "s5",
        "nombre": "Universidad EAFIT",
        "categoria": "Educación",
        "subcategoria": "Universidad Privada",
        "direccion": "Carrera 49 #7 Sur-50, Medellín",
        "telefono": "+57 604 2619500",
        "whatsapp": None,
        "zona": "Sur",
        "caracteristicas_accesibilidad": ["Rampas", "Baños accesibles", "Material digital accesible"],
        "horarios": "Lunes a Viernes 7:00 - 19:00",
        "tiene_interprete_lsc": False,
        "distancia_aproximada": 7.8
    },
    {
        "id": "s6",
        "nombre": "Colegio INEM José Félix de Restrepo",
        "categoria": "Educación",
        "subcategoria": "Colegio Público",
        "direccion": "Carrera 48 #12-50, Medellín",
        "telefono": "+57 604 2665150",
        "whatsapp": None,
        "zona": "Sur",
        "caracteristicas_accesibilidad": ["Rampas", "Intérprete LSC disponible", "Carteles inclusivos"],
        "horarios": "Lunes a Viernes 7:00 - 16:00",
        "tiene_interprete_lsc": True,
        "distancia_aproximada": 6.5
    },

    # --- Servicios de Gobierno ---
    {
        "id": "s7",
        "nombre": "Alcaldía de Medellín",
        "categoria": "Gobierno",
        "subcategoria": "Administración Municipal",
        "direccion": "Carrera 52 #71-120, Medellín",
        "telefono": "+57 604 3855555",
        "whatsapp": "+57 3001239876",
        "zona": "Centro",
        "caracteristicas_accesibilidad": ["Rampas", "Atención prioritaria", "Puntos accesibles de información"],
        "horarios": "Lunes a Viernes 8:00 - 17:00",
        "tiene_interprete_lsc": True,
        "distancia_aproximada": 2.8
    },
    {
        "id": "s8",
        "nombre": "Personería de Medellín",
        "categoria": "Gobierno",
        "subcategoria": "Defensoría del Ciudadano",
        "direccion": "Carrera 52 #71-123, Medellín",
        "telefono": "+57 604 3859970",
        "whatsapp": None,
        "zona": "Centro",
        "caracteristicas_accesibilidad": ["Rampas", "Intérprete LSC disponible bajo solicitud"],
        "horarios": "Lunes a Viernes 8:00 - 17:00",
        "tiene_interprete_lsc": True,
        "distancia_aproximada": 2.9
    },

    # --- Otros Servicios Variados ---
    {
        "id": "s9",
        "nombre": "Centro Comercial Santafé Medellín",
        "categoria": "Comercio",
        "subcategoria": "Centro Comercial",
        "direccion": "Carrera 43A #7 Sur-170, Medellín",
        "telefono": "+57 604 2669999",
        "whatsapp": None,
        "zona": "Sur",
        "caracteristicas_accesibilidad": ["Rampas", "Señalización visual", "Personal capacitado en inclusión"],
        "horarios": "Lunes a Domingo 10:00 - 21:00",
        "tiene_interprete_lsc": False,
        "distancia_aproximada": 8.2
    },
    {
        "id": "s10",
        "nombre": "Museo de Antioquia",
        "categoria": "Cultura",
        "subcategoria": "Museo",
        "direccion": "Carrera 52 #52-43, Medellín",
        "telefono": "+57 604 2513636",
        "whatsapp": "+57 3204567890",
        "zona": "Centro",
        "caracteristicas_accesibilidad": ["Rampas", "Recorridos con intérprete LSC", "Audioguías"],
        "horarios": "Martes a Domingo 10:00 - 17:00",
        "tiene_interprete_lsc": True,
        "distancia_aproximada": 3.0
    }
]

# ==============================================
# LISTA DE INTÉRPRETES DE PRUEBA (INTERPRETES_MOCK)
# ==============================================

# Cada intérprete representa un profesional LSC disponible en Medellín
# con diferentes especialidades, experiencia y cobertura.

INTERPRETES_MOCK = [
    {
        "id": "i1",
        "nombre": "Laura Pérez Gómez",
        "foto": None,
        "especialidades": ["Médica", "Legal"],
        "zonas_cobertura": ["Centro", "Norte"],
        "disponibilidad": "Lunes a Viernes 8:00 - 18:00",
        "tarifa_hora": 60000.0,
        "años_experiencia": 5,
        "certificaciones": ["Certificación Nacional de Intérprete LSC Nivel II"],
        "telefono": "+57 3104567890",
        "whatsapp": "+57 3104567890",
        "email": "laura.perez@example.com"
    },
    {
        "id": "i2",
        "nombre": "Carlos Restrepo Ramírez",
        "foto": None,
        "especialidades": ["Educativa", "Empresarial"],
        "zonas_cobertura": ["Sur", "Centro"],
        "disponibilidad": "Lunes a Sábado 7:00 - 19:00",
        "tarifa_hora": 45000.0,
        "años_experiencia": 3,
        "certificaciones": ["Certificado de Competencia en Interpretación Educativa"],
        "telefono": "+57 3129876543",
        "whatsapp": "+57 3129876543",
        "email": "carlos.restrepo@example.com"
    },
    {
        "id": "i3",
        "nombre": "María Fernanda Torres",
        "foto": None,
        "especialidades": ["Legal", "Eventos"],
        "zonas_cobertura": ["Occidente", "Centro"],
        "disponibilidad": "Lunes a Domingo 8:00 - 20:00",
        "tarifa_hora": 70000.0,
        "años_experiencia": 8,
        "certificaciones": ["Certificado Avanzado en Interpretación Legal"],
        "telefono": "+57 3145678912",
        "whatsapp": "+57 3145678912",
        "email": "maria.torres@example.com"
    },
    {
        "id": "i4",
        "nombre": "Andrés Felipe Gómez",
        "foto": None,
        "especialidades": ["Educativa", "Médica", "Empresarial"],
        "zonas_cobertura": ["Norte", "Oriente"],
        "disponibilidad": "Lunes a Viernes 8:00 - 17:00",
        "tarifa_hora": 50000.0,
        "años_experiencia": 4,
        "certificaciones": ["Certificación en Interpretación LSC Nivel I"],
        "telefono": "+57 3156789123",
        "whatsapp": "+57 3156789123",
        "email": "andres.gomez@example.com"
    }
]

# ==============================================
# NOTA FINAL
# ==============================================
# Estos datos son exclusivamente para desarrollo, pruebas y demostraciones del MVP de My Sign.
# No representan información real ni confidencial.
