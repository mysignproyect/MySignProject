# My Sign - Sistema de Servicios Accesibles para la Comunidad Sorda de Medellín

## Descripción General

**My Sign** es una plataforma web que centraliza información sobre servicios accesibles, intérpretes de Lengua de Señas Colombiana (LSC) y un sistema de emergencias adaptado para la comunidad sorda de Medellín. El objetivo principal es facilitar el acceso a servicios esenciales y promover la inclusión digital, permitiendo búsquedas por categoría, ubicación y contacto ágil en situaciones de emergencia.

---

## Problema que Resuelve

La comunidad sorda de Medellín enfrenta dificultades para acceder a servicios básicos debido a la falta de:
- Información centralizada y confiable sobre servicios accesibles.
- Directorios actualizados de intérpretes certificados en LSC.
- Sistemas de emergencia que consideren sus necesidades comunicativas y tecnológicas.

---

## Solución Propuesta

My Sign ofrece:
- Un portal con información verificada de servicios accesibles (salud, educación, gobierno, etc.).
- Directorio de intérpretes LSC con filtros por especialidad, zona y disponibilidad.
- Sistema de emergencias visual, con mensajes automáticos que incluyen ubicación GPS y solicitud de intérprete.

---

## Características Principales

1. **Búsqueda de Servicios Accesibles**
   - Filtrado por categoría, zona geográfica y características de accesibilidad.
   - Resultados ordenados por proximidad y relevancia.
   - Información clara sobre disponibilidad de intérprete LSC y horarios de atención.

2. **Directorio de Intérpretes LSC**
   - Filtros por especialidad, cobertura geográfica y disponibilidad horaria.
   - Visualización de tarifas, experiencia y certificaciones.
   - Contacto directo vía WhatsApp, teléfono o email.

3. **Sistema de Emergencias**
   - Botón de acceso rápido visible en toda la app.
   - Emergencias predefinidas con iconografía universal.
   - Mensajes automáticos con ubicación GPS y solicitud de intérprete, enviados por WhatsApp, SMS y correo.

4. **Interfaz Accesible**
   - Alto contraste, iconografía universal y navegación simplificada (máximo 3 clics).
   - Compatible con tecnologías asistivas (lectores de pantalla).

---

## Arquitectura del Proyecto

```
MySignProject/
│
├── backend/                    # API REST – FastAPI
│   ├── app/
│   │   ├── models/            # Modelos de datos (Pydantic)
│   │   ├── routes/            # Endpoints y rutas de la API
│   │   └── services/          # Lógica de negocio (HashMaps, Árbol de categorías)
│   ├── data/                  # Datos mock y de prueba
│   ├── tests/                 # Pruebas unitarias
│   ├── main.py                # Entrada principal
│   └── requirements.txt       # Dependencias Python
│
└── frontend/                  # Aplicación React
    ├── src/
    │   ├── components/        # Componentes reutilizables
    │   ├── pages/             # Páginas principales del sitio
    │   └── services/          # Conexión con la API
    ├── package.json
    └── vite.config.js
```

---

## Tecnologías Utilizadas

**Backend**
- Python 3.8+
- FastAPI (API REST, documentación automática)
- Pydantic (modelado y validación de datos)
- Uvicorn (servidor ASGI)
- UnitTest / Pytest (testing)

**Frontend**
- React 19.1.1 (UI)
- Vite 7.1.7 (build y dev server)
- React Router DOM 7.9.3 (routing)
- Lucide React (iconografía accesible)
- ESLint (linting)

**Estructuras de Datos**
- HashMaps (búsqueda rápida O(1) para servicios e intérpretes)
- Árbol jerárquico (organización de categorías y subcategorías)

---

## Requisitos Previos

Instala y verifica las siguientes herramientas:

- Python 3.8+
- Node.js 20.19.0+
- npm (incluido con Node.js)
- Docker (opcional, para despliegue)
- Git

Verifica versiones ejecutando:
```bash
python --version
node --version
npm --version
docker --version
```

---

## Instalación y Configuración

1. **Clonar el Repositorio**
    ```bash
    git clone https://github.com/mysignproyect/MySignProject.git
    cd MySignProject
    ```

2. **Backend (FastAPI)**
    - Ver detalles en [backend/README.md](backend/README.md)
    ```bash
    cd backend
    python -m venv venv
    # Activar entorno virtual
    # Windows:
    venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. **Frontend (React)**
    - Ver detalles en [frontend/README.md](frontend/README.md)
    ```bash
    cd frontend
    npm install
    ```

---

## Ejecución del Proyecto

**Backend**
```bash
cd backend
source venv/bin/activate  # o venv\Scripts\activate en Windows
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
- Acceso: [http://localhost:8000](http://localhost:8000)

**Frontend**
```bash
cd frontend
npm run dev
```
- Acceso: [http://localhost:5173](http://localhost:5173)

---

## Endpoints de la API

- `GET /api/servicios` – Listado de servicios (filtros opcionales)
- `GET /api/servicios/{servicio_id}` – Detalle de servicio
- `GET /api/servicios/categoria/{categoria}` – Servicios por categoría
- `GET /api/interpretes` – Listado de intérpretes (filtros opcionales)
- `GET /api/interpretes/{interprete_id}` – Detalle de intérprete
- `GET /api/categorias` – Todas las categorías

**Documentación interactiva**: [Swagger UI](http://localhost:8000/docs)

---

## Ejemplos de Modelos de Datos

**Servicio**
```json
{
  "id": "s1",
  "nombre": "Hospital San Vicente Fundación",
  "categoria": "Salud",
  "subcategoria": "Hospital General",
  "direccion": "Carrera 51D #62-29, Medellín",
  "telefono": "+57 604 4441333",
  "zona": "Norte",
  "caracteristicas_accesibilidad": ["Rampas", "Ascensores"],
  "tiene_interprete_lsc": true,
  "distancia_aproximada": 2.5
}
```

**Intérprete**
```json
{
  "id": "i1",
  "nombre": "Laura Pérez Gómez",
  "especialidades": ["Médica", "Legal"],
  "zonas_cobertura": ["Centro", "Norte"],
  "disponibilidad": "Lunes a Viernes 8:00 - 18:00",
  "tarifa_hora": 60000.0,
  "años_experiencia": 5,
  "telefono": "+57 3104567890",
  "whatsapp": "+57 3104567890",
  "email": "laura.perez@example.com"
}
```

---

## Pruebas

**Backend**
```bash
cd backend
pytest tests/ -v
```

**Frontend**
```bash
cd frontend
npm run test
```

---

## Casos de Uso

1. **Búsqueda de servicios accesibles**
   - Ejemplo: Usuario busca hospitales en la zona Centro, con intérprete LSC disponible 24h.

2. **Localización de intérpretes especializados**
   - Ejemplo: Usuario filtra intérpretes médicos disponibles en su zona.

3. **Sistema de emergencias**
   - Ejemplo: Usuario reporta emergencia médica, el sistema envía un mensaje automático con ubicación y solicitud de intérprete.

---

## Equipo de Desarrollo

Proyecto académico para la asignatura Estructura de Datos y Lenguajes de Programación Orientada a Objetos.

**Integrantes**
- Celene Parra Vega
- Juan Esteban Acevedo Patiño
- Daniela Pérez Agualimpia

---

## Alcance del MVP

- 15-20 servicios accesibles verificados de Medellín
- 5-8 intérpretes LSC certificados
- 4 categorías principales y 10 subcategorías
- Búsqueda O(1) con HashMaps
- Árbol jerárquico de categorías
- Interfaz accesible (máx. 3 clics por acción)

---

## Licencia

Proyecto académico para la Universidad Salazar y Herrera.  
**Uso exclusivo para fines educativos.**

## Prototipo

- [Prototipo UI proyecto](https://www.figma.com/design/wksq1JPGmSkbUH64O9Uewp/Untitled?node-id=0-1&t=tTwV1PWaw9cesa4M-0)
---

## Contribuciones

Proyecto cerrado.  
Para consultas, sugerencias o comentarios, contactar al equipo de desarrollo.

---

## Recursos Adicionales

- [Documentación Backend](backend/README.md)
- [Documentación Frontend](frontend/README.md)
- [API Docs (Swagger)](http://localhost:8000/docs)
- [Propuesta Original](docs/Propuesta_proyecto_de_aula_My_Sign.docx)

---

## Comentarios Específicos

- Todos los nombres de carpetas y archivos reflejan la estructura actual del proyecto.
- Los ejemplos de modelos corresponden al formato real usado en la API y base de datos.
- Los comandos están pensados para usuarios nuevos y avanzados.
- Instrucciones de pruebas y despliegue separadas para backend y frontend.
- Se destacan los filtros y funcionalidades clave del sistema, según los requerimientos del usuario y comunidad.
