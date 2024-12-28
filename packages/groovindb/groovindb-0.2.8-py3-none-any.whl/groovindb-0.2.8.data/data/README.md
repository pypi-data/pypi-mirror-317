# GroovinDB

GroovinDB es un ORM (Object-Relational Mapping) minimalista y eficiente para Python que soporta PostgreSQL y MySQL. Proporciona una interfaz limpia y tipada para interactuar con bases de datos relacionales.

## Características

- Soporte para PostgreSQL y MySQL
- Tipado estático con generación automática de tipos
- API intuitiva y fácil de usar
- CLI integrado para inicialización y generación de tipos
- Operaciones CRUD completas
- Validación de inputs
- Logging integrado
- Soporte para operaciones de agregación
- Queries raw cuando se necesitan

## Instalación

```bash
pip install groovindb
```

## Configuración Rápida

1. Inicializa un nuevo proyecto:

```bash
groovindb init
```

Este comando creará un archivo `groovindb.json` con la configuración de tu base de datos:

```json
{
  "driver": "postgresql",
  "host": "localhost",
  "port": 5432,
  "database": "mi_database",
  "user": "usuario",
  "password": "contraseña",
  "schema": "public"
}
```

2. Genera los tipos de tu base de datos:

```bash
groovindb introspect
```

## Uso Básico

```python
from groovindb import GroovinDB

# Inicializar la conexión
db = GroovinDB()

# Usar async/await
async def main():
    # Conectar a la base de datos
    await db.connect()
    
    # Realizar operaciones
    users = await db.client.users.findMany(
        where={"active": True},
        orderBy={"created_at": "desc"},
        take=10
    )
    
    # Cerrar la conexión
    await db.disconnect()
```

## Operaciones Disponibles

### Búsqueda

```python
# Encontrar un registro único
user = await db.client.users.findUnique(
    where={"id": 1}
)

# Encontrar el primer registro que coincida
user = await db.client.users.findFirst(
    where={"email": "ejemplo@email.com"},
    orderBy={"created_at": "desc"}
)

# Encontrar múltiples registros
users = await db.client.users.findMany(
    where={"active": True},
    orderBy={"created_at": "desc"},
    take=10,
    skip=0
)
```

### Creación y Actualización

```python
# Crear un nuevo registro
new_user = await db.client.users.create({
    "name": "John Doe",
    "email": "john@example.com"
})

# Actualizar un registro
updated_user = await db.client.users.update(
    where={"id": 1},
    data={"active": False}
)

# Crear o actualizar (upsert)
user = await db.client.users.upsert(
    where={"email": "john@example.com"},
    create={"name": "John", "email": "john@example.com"},
    update={"last_login": "2023-01-01"}
)
```

### Eliminación

```python
# Eliminar un registro
deleted_user = await db.client.users.delete(
    where={"id": 1}
)
```

### Agregaciones

```python
# Contar registros
count = await db.client.users.count(
    where={"active": True}
)

# Operaciones de agregación
stats = await db.client.orders.aggregate(
    where={"status": "completed"},
    _sum=["total_amount"],
    _avg=["items_count"],
    _max=["order_value"]
)
```

### Queries Raw

```python
# Ejecutar queries SQL personalizadas
results = await db.client.query(
    "SELECT * FROM users WHERE created_at > $1",
    "2023-01-01"
)
```

## CLI Command Reference

### `init`

Inicializa un nuevo proyecto GroovinDB:

```bash
groovindb init
```

Este comando:
- Crea un archivo de configuración `groovindb.json`
- Solicita interactivamente los detalles de conexión
- Ofrece la opción de generar tipos automáticamente

### `introspect`

Genera tipos TypeScript basados en tu esquema de base de datos:

```bash
groovindb introspect
```

Este comando:
- Lee el esquema de tu base de datos
- Genera tipos TypeScript para todas las tablas
- Crea un cliente tipado para usar en tu código

## Logging

GroovinDB incluye un sistema de logging integrado que puede configurarse según tus necesidades:

```python
from groovindb.utils.logger import logger

# Cambiar nivel de log
logger.setLevel("DEBUG")
```

## Soporte de Drivers

- PostgreSQL (usando `asyncpg`)
- MySQL (usando `aiomysql`)

## Consideraciones de Rendimiento

- Las conexiones son manejadas automáticamente
- Las consultas son validadas antes de ser ejecutadas
- El cliente es generado una sola vez durante la introspección
- Las operaciones de agregación son optimizadas a nivel de base de datos

## Licencia