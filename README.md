# cs2032-user-service

> Proyecto del curso **CS2032 – Cloud Computing** · UTEC · 2024-1

Microservicio REST de usuarios (CRUD, registro y login), construido con **FastAPI** y **MongoDB**. Forma parte de un backend de tres microservicios:

| Servicio | Puerto | Responsabilidad |
|---|---|---|
| **cs2032-user-service** | 8001 | Usuarios, registro y login |
| [cs2032-car-service](https://github.com/maykol-morales/cs2032-car-service) | 8002 | Catálogo de autos |
| [cs2032-purchase-service](https://github.com/maykol-morales/cs2032-purchase-service) | 8003 | Compras (marca el auto como no disponible) |

## Stack

- Python 3.12 · FastAPI · Pydantic
- MongoDB (`pymongo`), base `user`, colección `production`
- Docker

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/user` | Crea un usuario (permite definir `admin`) |
| `GET` | `/user/{user_id}` | Obtiene un usuario |
| `PUT` | `/user/{user_id}` | Actualiza un usuario |
| `DELETE` | `/user/{user_id}` | Elimina un usuario |
| `GET` | `/users/` | Lista todos los usuarios |
| `POST` | `/register` | Registro público (siempre `admin: false`) |
| `POST` | `/login?name=...&password=...` | Valida credenciales y devuelve el ID del usuario (`401` si son inválidas) |

Los recursos inexistentes responden `404`. La documentación interactiva queda disponible en `/docs` (Swagger UI).

### Modelo `User`

```json
{
  "name": "maykol",
  "password": "secret",
  "admin": false
}
```

> ⚠️ Proyecto académico: las contraseñas se guardan en texto plano. No usar en producción.

## Configuración

| Variable | Por defecto | Descripción |
|---|---|---|
| `MONGO_URL` | `mongodb://localhost:27017/` | Conexión a MongoDB |

## Ejecución

```bash
# MongoDB local
docker run -d --name mongo -p 27017:27017 mongo

# Local
pip install -r requirements.txt
fastapi dev main.py --port 8001

# Docker
docker build -t user-service .
docker run --network host user-service
```

## Licencia

[Apache 2.0](LICENSE)
