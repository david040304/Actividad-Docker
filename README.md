# 📦 Actividad Docker — Arquitectura Multi-Contenedor

Aplicación web de **Agenda de Contactos** y **Validador de Contraseñas**, separada en 3 servicios independientes listos para dockerizar.

---

## 🏗️ Estructura del proyecto

```
├── backend/                 # API REST (Flask + Gunicorn)
│   ├── app/
│   │   ├── __init__.py      # Application factory
│   │   ├── database.py      # Conexión PostgreSQL
│   │   └── routes/
│   │       ├── contacts.py  # CRUD de contactos
│   │       ├── validator.py # Validador de contraseñas
│   │       └── health.py    # Health check
│   ├── config.py            # Variables de entorno
│   ├── run.py               # Entry point
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
│
├── frontend/                # Interfaz web (Nginx)
│   ├── public/
│   │   ├── index.html       # Página principal
│   │   ├── agenda.html      # Agenda de contactos
│   │   ├── validador.html   # Validador de contraseñas
│   │   ├── css/             # Estilos
│   │   └── js/              # Scripts del frontend
│   ├── nginx.conf           # Proxy inverso → backend
│   └── Dockerfile
│
├── database/                # Base de datos (PostgreSQL)
│   └── init.sql             # Schema + datos iniciales
│
├── docker-compose.yml       # Orquestación de los 3 servicios
├── .dockerignore
└── README.md
```

---

## 🚀 Cómo ejecutar

### Requisitos
- [Docker](https://docs.docker.com/get-docker/) y [Docker Compose](https://docs.docker.com/compose/install/)

### Levantar todo

```bash
docker-compose up --build
```

### Acceder a la aplicación

| Servicio   | URL                          |
|------------|------------------------------|
| Frontend   | http://localhost              |
| Backend    | http://localhost:5000/health  |
| PostgreSQL | localhost:5432               |

### Parar y limpiar

```bash
docker-compose down        # Parar contenedores
docker-compose down -v     # Parar y borrar volúmenes (BD)
```

---

## 🔧 Servicios

### 🟢 Backend (`backend/`)
- **Framework:** Flask 3.1 + Gunicorn
- **BD:** PostgreSQL via `psycopg2`
- **CORS** habilitado para peticiones del frontend
- **Endpoints:**
  - `GET    /api/contacts`       → Listar contactos
  - `POST   /api/contacts`       → Crear contacto
  - `PUT    /api/contacts/:id`   → Actualizar contacto
  - `DELETE /api/contacts/:id`   → Eliminar contacto
  - `POST   /api/validar`        → Validar contraseña
  - `GET    /health`             → Health check

### 🔵 Frontend (`frontend/`)
- **Servidor:** Nginx 1.27 (Alpine)
- HTML/CSS/JS estáticos
- Nginx actúa como **proxy inverso**: las peticiones a `/api/*` se reenvían al backend

### 🟡 Database (`database/`)
- **Motor:** PostgreSQL 16 (Alpine)
- `init.sql` crea la tabla y carga datos de ejemplo
- Volumen persistente `pg_data`

---

## 🌐 Variables de entorno del backend

| Variable       | Valor por defecto | Descripción             |
|----------------|-------------------|-------------------------|
| `DB_HOST`      | `localhost`       | Host de PostgreSQL      |
| `DB_PORT`      | `5432`            | Puerto de PostgreSQL    |
| `DB_NAME`      | `agenda_db`       | Nombre de la BD        |
| `DB_USER`      | `postgres`        | Usuario de la BD       |
| `DB_PASSWORD`  | `postgres`        | Contraseña de la BD    |
| `FLASK_DEBUG`  | `0`               | Modo debug (0/1)       |
