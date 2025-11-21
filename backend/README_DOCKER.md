# 🐳 Guía de Docker - My Sign Project

Esta guía explica cómo ejecutar My Sign usando Docker y Docker Compose.

---

## 📋 **Requisitos Previos**

- **Docker** 20.10+
- **Docker Compose** 2.0+

### Verificar instalación:
```bash
docker --version
docker-compose --version
```

### Instalar Docker (si no lo tienes):
- **Windows/Mac**: [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Linux**: 
  ```bash
  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  ```

---

## 🚀 **Inicio Rápido**

### **Opción 1: Levantar todo el proyecto (Backend + Frontend)**

```bash
# Desde la raíz del proyecto
docker-compose up --build
```

Esto iniciará:
- **Backend (FastAPI)**: http://localhost:8000
- **Frontend (React)**: http://localhost:5173
- **API Docs (Swagger)**: http://localhost:8000/docs

---

### **Opción 2: Solo Backend**

```bash
# Desde la carpeta backend/
cd backend
docker build -t mysign-backend .
docker run -p 8000:8000 mysign-backend
```

Acceder a:
- API: http://localhost:8000
- Documentación: http://localhost:8000/docs

---

## 🛠️ **Comandos Útiles**

### **Iniciar servicios**
```bash
# En primer plano (ver logs)
docker-compose up

# En segundo plano (detached)
docker-compose up -d

# Reconstruir imágenes
docker-compose up --build
```

### **Detener servicios**
```bash
# Detener servicios
docker-compose stop

# Detener y eliminar contenedores
docker-compose down

# Detener y eliminar todo (incluye volúmenes)
docker-compose down -v
```

### **Ver logs**
```bash
# Todos los servicios
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo frontend
docker-compose logs -f frontend
```

### **Ejecutar comandos dentro de contenedores**
```bash
# Shell en backend
docker-compose exec backend bash

# Shell en frontend
docker-compose exec frontend sh

# Correr tests en backend
docker-compose exec backend pytest tests/ -v
```

---

## 📊 **Estructura de Docker**

```
MySignProject/
├── backend/
│   ├── Dockerfile              # Imagen del backend
│   ├── .dockerignore          # Archivos a excluir
│   └── ...
├── frontend/
│   ├── Dockerfile              # Imagen del frontend
│   └── ...
└── docker-compose.yml          # Orquestación completa
```

---

## 🔧 **Configuración Avanzada**

### **Variables de entorno**

Crear archivo `.env` en la raíz:
```env
# Backend
BACKEND_PORT=8000
ENVIRONMENT=development

# Frontend
FRONTEND_PORT=5173
VITE_API_URL=http://localhost:8000
```

Usar en `docker-compose.yml`:
```yaml
services:
  backend:
    env_file: .env
```

### **Hot Reload (desarrollo)**

Los volúmenes ya están configurados para hot-reload:
- Cambios en `backend/app/` se reflejan automáticamente
- Cambios en `frontend/src/` se reflejan automáticamente

### **Producción**

Para producción, modificar `docker-compose.yml`:
```yaml
environment:
  - ENVIRONMENT=production
command: ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🐛 **Troubleshooting**

### **Error: Puerto ya en uso**
```bash
# Verificar qué está usando el puerto
# Windows:
netstat -ano | findstr :8000

# Linux/Mac:
lsof -i :8000

# Cambiar puerto en docker-compose.yml
ports:
  - "8001:8000"  # Usar 8001 externamente
```

### **Error: Cannot connect to Docker daemon**
```bash
# Iniciar Docker Desktop (Windows/Mac)
# O iniciar servicio Docker (Linux):
sudo systemctl start docker
```

### **Reconstruir imágenes desde cero**
```bash
docker-compose build --no-cache
docker-compose up
```

### **Limpiar todo Docker**
```bash
# Eliminar contenedores detenidos
docker container prune

# Eliminar imágenes sin usar
docker image prune -a

# Limpiar todo (¡cuidado!)
docker system prune -a --volumes
```

---

## 📈 **Monitoreo**

### **Ver recursos usados**
```bash
docker stats
```

### **Inspeccionar contenedores**
```bash
# Ver procesos
docker-compose top

# Ver configuración
docker-compose config

# Health check
docker inspect mysign-backend | grep Health -A 10
```

---

## 🔐 **Buenas Prácticas**

✅ **DO:**
- Usar `.dockerignore` para excluir archivos innecesarios
- Usar multi-stage builds para imágenes más pequeñas
- Ejecutar como usuario no-root
- Definir health checks
- Usar volúmenes para persistencia

❌ **DON'T:**
- Incluir secretos/contraseñas en Dockerfile
- Usar `latest` en producción
- Ejecutar como root en producción
- Exponer puertos innecesarios

---

## 📚 **Recursos Adicionales**

- [Documentación oficial de Docker](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [FastAPI en Docker](https://fastapi.tiangolo.com/deployment/docker/)
- [Vite en Docker](https://vitejs.dev/guide/build.html)

---

## 👥 **Soporte**

Para problemas o preguntas:
1. Revisar esta guía
2. Verificar logs: `docker-compose logs`
3. Contactar al equipo de desarrollo

---

**Proyecto:** My Sign - Sistema de Servicios Accesibles LSC  
**Equipo:** Celene Parra, Juan Esteban Acevedo, Daniela Pérez  
**Universidad:** Salazar y Herrera