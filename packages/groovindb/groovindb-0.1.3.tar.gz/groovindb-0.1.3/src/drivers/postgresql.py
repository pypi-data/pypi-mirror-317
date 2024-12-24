"""
Driver PostgreSQL para GroovinDB.
"""
from typing import Any, Dict, List, Optional
import asyncpg
from .base import BaseDriver, PoolConfig, ConnectionError, QueryError

class PostgreSQLDriver(BaseDriver):
    """Driver para PostgreSQL."""

    async def create_pool(self, dsn: str) -> Any:
        """Crear pool de conexiones."""
        try:
            config = self.parse_dsn(dsn)
            pool_kwargs = {
                "host": config["host"],
                "port": config["port"],
                "user": config["user"],
                "password": config["password"],
                "database": config["database"],
                "min_size": self.pool_config.min_size,
                "max_size": self.pool_config.max_size,
            }
            
            # Solo agregar parámetros opcionales si tienen valor
            if self.pool_config.max_queries is not None:
                pool_kwargs["max_queries"] = self.pool_config.max_queries
            if self.pool_config.timeout is not None:
                pool_kwargs["timeout"] = self.pool_config.timeout
                
            return await asyncpg.create_pool(**pool_kwargs)
        except Exception as e:
            raise ConnectionError(f"Error al crear pool PostgreSQL: {str(e)}")

    async def execute(self, query: str, *args) -> Any:
        """Ejecutar una query."""
        try:
            async with self._pool.acquire() as conn:
                return await conn.execute(query, *args)
        except Exception as e:
            raise QueryError(f"Error al ejecutar query: {str(e)}")

    async def fetch(self, query: str, *args) -> List[Dict[str, Any]]:
        """Ejecutar una query y obtener múltiples resultados."""
        try:
            async with self._pool.acquire() as conn:
                return await conn.fetch(query, *args)
        except Exception as e:
            raise QueryError(f"Error al ejecutar fetch: {str(e)}")

    async def fetch_one(self, query: str, *args) -> Optional[Dict[str, Any]]:
        """Ejecutar una query y obtener un único resultado."""
        try:
            async with self._pool.acquire() as conn:
                return await conn.fetchrow(query, *args)
        except Exception as e:
            raise QueryError(f"Error al ejecutar fetch_one: {str(e)}")

    def param_placeholder(self, position: int) -> str:
        """Obtener el placeholder para un parámetro en la posición dada."""
        return f"${position}"

    def format_query(self, query: str) -> str:
        """Formatear una query según el dialecto SQL del driver."""
        return query 