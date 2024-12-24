from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple, NamedTuple
from dataclasses import dataclass
from urllib.parse import urlparse

@dataclass
class PoolConfig:
    """Configuración para el pool de conexiones"""
    min_size: int = 1
    max_size: int = 10
    max_queries: Optional[int] = None
    timeout: Optional[float] = None

class DatabaseError(Exception):
    """Error base para operaciones de base de datos."""
    pass

class ConnectionError(DatabaseError):
    """Error de conexión a la base de datos."""
    pass

class QueryError(DatabaseError):
    """Error en la ejecución de queries."""
    pass

class BaseDriver(ABC):
    """Clase base para drivers de base de datos."""

    def __init__(self, pool_config: Optional[PoolConfig] = None):
        """Inicializar driver con configuración opcional."""
        self.pool_config = pool_config or PoolConfig()
        self._pool = None

    @abstractmethod
    async def create_pool(self, dsn: str) -> Any:
        """Crear pool de conexiones."""
        pass

    async def connect(self, dsn: str) -> None:
        """Conectar a la base de datos."""
        try:
            self._pool = await self.create_pool(dsn)
        except Exception as e:
            raise ConnectionError(f"Error al conectar a la base de datos: {str(e)}")

    async def close(self) -> None:
        """Cerrar la conexión a la base de datos."""
        if self._pool:
            await self._pool.close()
            self._pool = None

    @abstractmethod
    async def execute(self, query: str, *args) -> Any:
        """Ejecutar una query."""
        pass

    @abstractmethod
    async def fetch(self, query: str, *args) -> List[Dict[str, Any]]:
        """Ejecutar una query y obtener múltiples resultados."""
        pass

    @abstractmethod
    async def fetch_one(self, query: str, *args) -> Optional[Dict[str, Any]]:
        """Ejecutar una query y obtener un único resultado."""
        pass

    @abstractmethod
    def param_placeholder(self, position: int) -> str:
        """Obtener el placeholder para un parámetro en la posición dada."""
        pass

    def format_query(self, query: str) -> str:
        """Formatear una query según el dialecto SQL del driver."""
        return query

    def parse_dsn(self, dsn: str) -> Dict[str, Any]:
        """Parsear un DSN en sus componentes."""
        try:
            parsed = urlparse(dsn)
            return {
                "host": parsed.hostname or "localhost",
                "port": parsed.port,
                "user": parsed.username,
                "password": parsed.password,
                "database": parsed.path.lstrip("/"),
                "schema": "public"
            }
        except Exception as e:
            raise ConnectionError(f"DSN inválido: {str(e)}") 