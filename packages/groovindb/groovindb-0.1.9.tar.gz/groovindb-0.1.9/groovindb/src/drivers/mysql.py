"""
Driver MySQL para GroovinDB.
"""
from typing import Any, Dict, List, Optional
import aiomysql
from .base import BaseDriver, PoolConfig, ConnectionError, QueryError

class MySQLDriver(BaseDriver):
    """Driver para MySQL."""

    async def create_pool(self, dsn: str) -> Any:
        """Crear pool de conexiones."""
        try:
            config = self.parse_dsn(dsn)
            return await aiomysql.create_pool(
                host=config["host"],
                port=config["port"],
                user=config["user"],
                password=config["password"],
                db=config["database"],
                minsize=self.pool_config.min_size,
                maxsize=self.pool_config.max_size,
                autocommit=True
            )
        except Exception as e:
            raise ConnectionError(f"Error al crear pool MySQL: {str(e)}")

    async def execute(self, query: str, *args) -> Any:
        """Ejecutar una query."""
        try:
            async with self._pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, args if args else None)
                    return True
        except Exception as e:
            raise QueryError(f"Error al ejecutar query: {str(e)}")

    async def fetch(self, query: str, *args) -> List[Dict[str, Any]]:
        """Ejecutar una query y obtener múltiples resultados."""
        try:
            async with self._pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cur:
                    await cur.execute(query, args if args else None)
                    return await cur.fetchall()
        except Exception as e:
            raise QueryError(f"Error al ejecutar fetch: {str(e)}")

    async def fetch_one(self, query: str, *args) -> Optional[Dict[str, Any]]:
        """Ejecutar una query y obtener un único resultado."""
        try:
            async with self._pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cur:
                    await cur.execute(query, args if args else None)
                    return await cur.fetchone()
        except Exception as e:
            raise QueryError(f"Error al ejecutar fetch_one: {str(e)}")

    def param_placeholder(self, position: int) -> str:
        """Obtener el placeholder para un parámetro en la posición dada."""
        return "%s"

    def format_query(self, query: str) -> str:
        """Formatear una query según el dialecto SQL del driver."""
        return query.replace('"', '`') 