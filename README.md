# My Sign  
*Sistema de Servicios Accesibles para la Comunidad Sorda de Medellín*

---

## Índice

1. [Descripción General](#descripción-general)
2. [¿Qué Problema Resuelve?](#qué-problema-resuelve)
3. [Arquitectura y Estructura de Carpetas](#arquitectura-y-estructura-de-carpetas)
    - [Frontend (React)](#frontend-react)
    - [Backend (FastAPI)](#backend-fastapi)
4. [Características Clave](#características-clave)
5. [Manual de Usuario (Guía Paso a Paso)](#manual-de-usuario-guía-paso-a-paso)
6. [Documentación Técnica y Justificación Estructuras de Datos](#documentación-técnica-y-justificación-estructuras-de-datos)
7. [Pruebas Automatizadas y Reportes](#pruebas-automatizadas-y-reportes)
8. [Integración y Uso de IA](#integración-y-uso-de-ia)
9. [Instalación y Ejecución Rápida](#instalación-y-ejecución-rápida)
10. [Recursos de Apoyo y Enlaces](#recursos-de-apoyo-y-enlaces)
11. [Equipo](#equipo)
12. [Créditos, Licencia y Contribuciones](#créditos-licencia-y-contribuciones)
---

## Descripción General

*My Sign* es una aplicación web construida para la comunidad sorda de Medellín. Centraliza información sobre servicios accesibles y un directorio de intérpretes LSC (Lengua de Señas Colombiana). Desde un enfoque centrado en la inclusión, permite localizar intérpretes por zona o especialidad y acceder a instituciones aliadas (salud, educación, gobierno).  
*[Prototipo Interactivo Figma](https://www.figma.com/design/wksq1JPGmSkbUH64O9Uewp/Untitled?node-id=0-1&t=tTwV1PWaw9cesa4M-0)*

---

## ¿Qué Problema Resuelve?

- Dificultad para encontrar servicios realmente accesibles.
- Dispersión y poca confiabilidad en la información de intérpretes y entidades amigables con la comunidad sorda.
- Falta de filtros por criterios relevantes: ubicación, accesibilidad, especialidad.
- Carencia de plataformas inclusivas, visuales y navegables fácilmente por cualquier usuario.

*¿Cómo My Sign Resuelve Esto?*

- Centralización de datos: todo en un solo sitio, validado y categorizado.
- Filtros accesibles, visuales y de bajo esfuerzo cognitivo.
- Directorio 100% enfocado en LSC, con contacto inmediato.
- Interfaz de máximo 3 clics, con diseño validado por la comunidad y uso de gifs e imágenes claras.
- *Todo usuario puede ejecutar la app con 2 comandos.*

---

## Arquitectura y Estructura de Carpetas

### Frontend (React)
```plaintext
frontend/
├── public/
├── src/
│   ├── assets/
│   │   ├── css/
│   │   ├── gif/
│   │   └── img/
│   ├── components/
│   │   ├── CardInterpretes.jsx
│   │   ├── FooterDeLaPagina.jsx
│   │   ├── ListadoInterpretes.jsx
│   │   ├── Nav.jsx
│   │   └── Servicios.jsx
│   ├── pages/
│   │   ├── EntidadesPage.jsx
│   │   ├── InicioPage.jsx
│   │   └── InterpretesPage.jsx
│   └── services/
│       ├── EntidadesService.js
│       └── InterpretesService.js
│   ├── App.jsx
│   ├── main.jsx
│   └── ...
├── reports/
│   ├── report.html
│   ├── reporte_style.css
│   └── test_report.html
├── package.json
└── vite.config.js
```

### Backend (FastAPI & Python)
```plaintext
backend/
├── app/
│   ├── models/
│   ├── routes/
│   ├── services/
│   │   ├── categoria_tree.py
│   │   └── buscador.py
│   ├── utils/
│   └── main.py
├── data/
│   └── mock_data.py
├── app/tests/
│   ├── test_buscador.py
│   ├── test_categoria.py
│   ├── test_errors.py
│   ├── test_pagination.py
│   ├── test_schemas.py
│   └── __init__.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README_DOCKER.md *(Guía Docker)*
└── pyproject.toml
```

---

## Características Clave

- *Búsqueda multicriterio:* Categoría, zona, disponibilidad, accesibilidad.
- *Directorio de intérpretes LSC certificado:* con contacto directo (WhatsApp, email, teléfono).
- *Tarjetas visuales para entidades aliadas:* información directa y clara para salud, gobierno y educación.
- *Filtros por especialidad, zona y tarifa de intérpretes.*
- *Navegación accesible, visual y amigable.*
- *Pruebas automatizadas con generación de reportes visuales HTML.*
- *Despliegue inmediato con Docker para usuarios sin experiencia técnica.*
- *API REST bien documentada (Swagger).*
- *Manual de usuario detallado adaptado para todo nivel.*

---

## Manual de Usuario (Guía Paso a Paso)

### 1. Ingreso y navegación

Al abrir la aplicación:
  - Accedes por defecto a la pantalla principal, donde puedes elegir entre “Servicios” o “Directorio de intérpretes”.
  - Los menús superiores te permiten siempre volver al inicio o a cualquier sección principal en máximo 3 clics.

### 2. Buscar entidades y servicios

- En la pestaña de “Servicios”, filtra por tipo (Salud, Educación, Gobierno), zona o criterios extra de accesibilidad.
- Cada servicio se presenta como una tarjeta con:  
  - Nombre, dirección, teléfonos
  - Zona de cobertura
  - Iconos e indicadores visuales de accesibilidad e intérprete LSC disponible

### 3. Directorio de intérpretes

- Puedes filtrar por especialidad, zona, disponibilidad y tarifas.
- Haz clic en un perfil para ver detalles (certificaciones, años de experiencia, formas de contacto).
- Contacta con un clic vía WhatsApp, llamada o correo electrónico.

### 4. Pruebas y reportes

- Ejecuta las pruebas desde el backend o frontend y revisa los reportes HTML generados automáticamente.
- Ideal para profesores o nuevos desarrolladores que deseen comprobar calidad y confiabilidad del código.

### 5. Ejecución rápida (ver sección ["Instalación y Ejecución Rápida"](#instalación-y-ejecución-rápida))

- ¡Cualquier persona puede correr la app y visualizar todos los datos filtrando con clicks y visualizando información clara desde cualquier dispositivo!
---

## Documentación Técnica y Justificación Estructuras de Datos

*¿Por qué esta arquitectura y estas estructuras?*

- *Árbol jerárquico (Python):*  
  - Modelo de categorías/subcategorías natural.
  - Permite búsquedas recursivas eficientes.
  - Facilita agregar nuevas categorías sin reescribir código.
  - Justificación completa y ejemplos en /backend/app/services/categoria_tree.py.

- *HashMap/Dicts (Python):*  
  - Búsqueda O(1) por id, zona o especialidad.
  - Implementado en /backend/app/services/buscador.py, cubriendo todos casos de búsqueda rápida.
  - Justifica velocidad y escalabilidad para expansión futura.

- *Recursión:*  
  - Para traversar el árbol de categorías de forma limpia y legible.
  - Ejemplo y explicación tanto en la [propuesta académica](./Propuesta proyecto de aula My Sign.docx) como en los comentarios de código y este README.

- *Testing automático:*  
  - Cubre árbol, filtros, búsquedas por texto/zona/categoría, paginación.
  - Unitarias en /backend/app/tests/ cubren casos exitosos, bordes y fallos esperados.

---

## Pruebas Automatizadas y Reportes

*Cobertura plena, claridad para cualquier usuario:*
- Pruebas backend (Pytest + HTML):  
```
  bash
  cd backend
  pytest app/tests/ --html=reports/backend_report.html --self-contained-html
  ```
- Pruebas frontend:
```
  bash
  cd frontend
  npm run test
  ```
- Consulta reportes en /frontend/reports/ y /backend/reports/ para resultados visuales y detallados.

---

## Integración y Uso de IA

- *Diseño de estructuras de datos:* Prompts generados con IA para establecer el mejor árbol y diccionario posible, explicación clara en terminología docente y para usuarios, lista de ventajas, casos de uso, caso base y casos recursivos.
- *Documentación y recursión:* Explicación integrada de cada algoritmo con analogía educativa.
- *Pruebas e Informes:* Automatización de casos de prueba y generación de reportes HTML sugerido por IA.
- *Experiencia de usuario:* Gifs e imágenes en frontend generados y sugeridos para hacer la app más amigable a cualquier persona (ver /frontend/src/assets/gif e /img).

---

## Instalación y Ejecución Rápida

### 👉 [Guía Docker Completa](backend/README_DOCKER.md) (si quieres todo en un comando, sin instalar dependencias)

### Requisitos mínimos

- [Python 3.8+](https://www.python.org/downloads/)
- [Node.js 20+](https://nodejs.org/)
- [npm](https://www.npmjs.com/) (usualmente con Node.js)
- [Git](https://git-scm.com/downloads)
- (Opcional) [Docker](https://docs.docker.com/get-docker/)

---
### 1. Clona el repositorio

```
bash
git clone https://github.com/mysignproyect/MySignProject.git
cd MySignProject
```

---

### 2. Backend: instalación y ejecución
```
bash
cd backend
python -m venv venv
```
# Activar entorno virtual:

# En Windows
```
venv\Scripts\activate
```
# En Mac/Linux
```
source venv/bin/activate
pip install -r requirements.txt
```

#### Corre el backend:
```
bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- Acceso API: [http://localhost:8000](http://localhost:8000)
- Documentación interactiva (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 3. Frontend: instalación y ejecución
```
bash
cd frontend
npm install
npm run dev
```
- Acceso frontend: [http://localhost:5173](http://localhost:5173)

---

### 4. (Opcional) Docker para ejecutar todo de manera automática

Revisa la guía avanzada de Docker:  
[backend/README_DOCKER.md](backend/README_DOCKER.md)

Con Docker solo necesitas:
```
bash
docker compose up --build
```
y todo quedará corriendo automáticamente.

---

### 5. Pruebas y reportes

#### Backend
```
bash
cd backend
pytest app/tests/ --html=report.html --self-contained-html

Revisa el archivo generado report.html para ver resultados completos de las pruebas.
```
#### Frontend
```
bash
cd frontend
npm run test
```
Reporte disponible en /frontend/reports/.

---
## Recursos de Apoyo y Enlaces

- [Prototipo Interactivo Figma](https://www.figma.com/design/wksq1JPGmSkbUH64O9Uewp/Untitled?node-id=0-1&t=tTwV1PWaw9cesa4M-0)*
- [Guía Docker](backend/README_DOCKER.md)

---

## Equipo

- Celene Parra Vega
- Juan Esteban Acevedo Patiño
- Daniela Pérez Agualimpia

---

## Créditos, Licencia y Contribuciones

Proyecto académico para la Universidad Salazar y Herrera.  
*Uso exclusivo para fines educativos.*  
¿Dudas, sugerencias? Contacta al equipo o deja una issue en el repositorio.

---

> Este README fue cuidadosamente integrado para que toda persona, sin importar su background técnico, pueda entender, correr y justificar este software.