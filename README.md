# Concesionario Backend

API REST desarrollada con FastAPI y PostgreSQL para la gestión de vehículos de un concesionario.

##  Demo

[https://concesionario-backend-fastapi.onrender.com/docs](https://concesionario-backend-fastapi.onrender.com/docs) — Documentación interactiva Swagger

> ⚠️ El servidor está en Render (plan gratuito) y puede tardar ~30 segundos en despertar. Visita el siguiente enlace para activarlo antes de usar la app:
> [https://concesionario-backend-fastapi.onrender.com/](https://concesionario-backend-fastapi.onrender.com/)

##  Tecnologías

- Python 3.14
- FastAPI
- PostgreSQL
- SQLAlchemy
- databases (async)
- JWT (python-jose)
- bcrypt
- Render (despliegue)

##  Endpoints

### Autenticación
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/auth/register` | Registro de usuario |
| POST | `/auth/login` | Login y obtención de JWT |

### Vehículos (protegidos con JWT)
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/vehicles/` | Listar vehículos |
| POST | `/api/vehicles/` | Crear vehículo |
| PUT | `/api/vehicles/{id}` | Actualizar vehículo |
| DELETE | `/api/vehicles/{id}` | Eliminar vehículo |

##  Instalación
```bash
git clone https://github.com/Josedevoc/concesionario-backend
cd concesionario-backend
pip install -r requirements.txt
uvicorn main:app --reload
```

##  Variables de entorno

Crea un archivo `.env` en la raíz basándote en `.env.example`:
```
DATABASE_URL=postgresql://usuario:password@host/db
SECRET_KEY=tu_secret_key
```

## 📁 Estructura
```
app/
├── routers/
│   ├── __init__.py
│   ├── auth.py          # Endpoints registro y login JWT
│   └── vehicles.py      # Endpoints CRUD vehículos
├── __init__.py
├── database.py          # Conexión PostgreSQL y tablas
├── dependencies.py      # Verificación JWT
├── models.py
└── schemas.py           # Modelos Pydantic
main.py                  # Entrada de la aplicación
requirements.txt
.env.example
```

## 🗄️ Modelos

### Vehicle
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer | Primary key |
| marca | String | Marca del vehículo |
| localidad | String | Sucursal |
| aspirante | String | Nombre del aspirante |
| created_at | DateTime | Fecha de creación |

### User
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer | Primary key |
| username | String | Nombre de usuario único |
| hashed_password | String | Contraseña encriptada con bcrypt |
| created_at | DateTime | Fecha de creación |