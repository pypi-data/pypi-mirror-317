from abc import ABC, abstractmethod
from typing import Any, List, Optional, Dict

class DriverError(Exception):
    """Error base para drivers"""
    pass

class ConnectionError(DriverError):
    """Error de conexión"""
    pass

class QueryError(DriverError):
    """Error en la query"""
    pass

class BaseDriver(ABC):
    """Driver base para conexiones a bases de datos"""
    
    @abstractmethod
    async def connect(self, dsn: str) -> None:
        """Establece la conexión con la base de datos"""
        pass

    @abstractmethod
    async def close(self) -> None:
        """Cierra la conexión"""
        pass

    @abstractmethod
    async def fetch(self, query: str, *args) -> List[Dict[str, Any]]:
        """Ejecuta una query y retorna múltiples resultados"""
        pass

    @abstractmethod
    async def fetch_one(self, query: str, *args) -> Optional[Dict[str, Any]]:
        """Ejecuta una query y retorna un único resultado"""
        pass

    @abstractmethod
    async def execute(self, query: str, *args) -> None:
        pass

    def _format_error(self, error: Exception) -> str:
        """Formatea el error para logging"""
        return f"{type(error).__name__}: {str(error)}" 