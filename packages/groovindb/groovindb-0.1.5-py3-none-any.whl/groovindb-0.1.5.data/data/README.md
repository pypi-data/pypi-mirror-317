# GroovinDB

GroovinDB es un ORM asíncrono para Python que proporciona una interfaz similar a Prisma para interactuar con bases de datos PostgreSQL y MySQL.

## Características

- Soporte para PostgreSQL y MySQL
- API asíncrona
- Sistema de caché integrado (memoria y Redis)
- CLI para inicialización y gestión
- Introspección automática de bases de datos
- Generación automática de modelos
- Soporte para múltiples esquemas
- Sistema de logging configurable

## Instalación

```bash
pip install groovindb
```

## Uso Rápido

1. Inicializar el proyecto:

```bash
groovindb init
```

2. Usar en código:

```python
import asyncio
from groovindb import GroovinDB

async def main():
    db = GroovinDB()
    await db.connect()

    # Consultar registros
    users = await db.client.users.findMany(
        where={"active": True},
        orderBy=[{"name": "asc"}],
        take=10
    )

    await db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```

## Configuración

La configuración se almacena en `groovindb.json`:

```json
{
  "postgresql": {
    "user": "user",
    "password": "password",
    "database": "mydb",
    "host": "localhost",
    "port": 5432,
    "schema": "public"
  },
  "cache": {
    "type": "memory",
    "ttl": 300
  },
  "debug": {
    "level": "INFO"
  }
}
```

## Documentación

Para más información, consulta la [documentación completa](https://bitbucket.org/groovinads/groovindb/src/master/README.md).

## Licencia

MIT
