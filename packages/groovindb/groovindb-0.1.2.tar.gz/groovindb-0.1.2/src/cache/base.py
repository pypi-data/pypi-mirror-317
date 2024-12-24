"""
Módulo base para el sistema de caché de GroovinDB.
Define la interfaz que deben implementar todos los tipos de caché.
"""
from abc import ABC, abstractmethod
from typing import Any, Optional, Dict, TypeVar, Generic, Union, List
from datetime import timedelta
from dataclasses import dataclass
import logging
import zlib
import pickle
from enum import Enum

logger = logging.getLogger('groovindb.cache')

T = TypeVar('T')

class CacheError(Exception):
    """Excepción base para errores de caché"""
    pass

class ConnectionError(CacheError):
    """Error de conexión con el caché"""
    pass

class SerializationError(CacheError):
    """Error al serializar/deserializar datos"""
    pass

class CompressionLevel(Enum):
    """Niveles de compresión disponibles"""
    NONE = 0
    FAST = 1
    BALANCED = 6
    BEST = 9

@dataclass
class CacheConfig:
    """Configuración para el caché"""
    ttl: timedelta = timedelta(minutes=5)
    retry_attempts: int = 3
    retry_delay: float = 1.0
    compression_level: CompressionLevel = CompressionLevel.NONE
    timeout: float = 5.0

@dataclass
class CacheStats:
    """Estadísticas del caché"""
    hits: int = 0
    misses: int = 0
    errors: int = 0
    memory_usage: float = 0.0  # en MB

class CacheProvider(ABC, Generic[T]):
    """
    Interfaz base para proveedores de caché.
    
    Proporciona funcionalidad común y define la interfaz
    que deben implementar todos los tipos de caché.
    """

    def __init__(self, config: Optional[CacheConfig] = None):
        """
        Inicializa el proveedor de caché.
        
        Args:
            config: Configuración del caché
        """
        self.config = config or CacheConfig()
        self.stats = CacheStats()

    def _serialize(self, value: T) -> bytes:
        """
        Serializa y opcionalmente comprime un valor.
        
        Args:
            value: Valor a serializar
            
        Returns:
            bytes: Datos serializados
            
        Raises:
            SerializationError: Si hay un error al serializar
        """
        try:
            data = pickle.dumps(value)
            if self.config.compression_level != CompressionLevel.NONE:
                data = zlib.compress(data, self.config.compression_level.value)
            return data
        except Exception as e:
            raise SerializationError(f"Error al serializar: {str(e)}") from e

    def _deserialize(self, data: bytes) -> T:
        """
        Deserializa y opcionalmente descomprime datos.
        
        Args:
            data: Datos a deserializar
            
        Returns:
            T: Valor deserializado
            
        Raises:
            SerializationError: Si hay un error al deserializar
        """
        try:
            if self.config.compression_level != CompressionLevel.NONE:
                data = zlib.decompress(data)
            return pickle.loads(data)
        except Exception as e:
            raise SerializationError(f"Error al deserializar: {str(e)}") from e

    @abstractmethod
    async def set(self, key: str, value: T, ttl: Optional[timedelta] = None) -> None:
        """
        Almacena un valor en el caché.
        
        Args:
            key: Clave bajo la cual almacenar el valor
            value: Valor a almacenar
            ttl: Tiempo de vida opcional (usa el de la config si no se especifica)
            
        Raises:
            CacheError: Si hay un error al almacenar
        """
        pass

    @abstractmethod
    async def get(self, key: str) -> Optional[T]:
        """
        Recupera un valor del caché.
        
        Args:
            key: Clave a recuperar
            
        Returns:
            Optional[T]: Valor almacenado o None si no existe
            
        Raises:
            CacheError: Si hay un error al recuperar
        """
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """
        Elimina una clave del caché.
        
        Args:
            key: Clave a eliminar
            
        Returns:
            bool: True si se eliminó, False si no existía
            
        Raises:
            CacheError: Si hay un error al eliminar
        """
        pass

    @abstractmethod
    async def clear(self) -> None:
        """
        Limpia todo el caché.
        
        Raises:
            CacheError: Si hay un error al limpiar
        """
        pass

    @abstractmethod
    async def delete_pattern(self, pattern: str) -> int:
        """
        Elimina todas las claves que coincidan con el patrón.
        
        Args:
            pattern: Patrón para buscar claves
            
        Returns:
            int: Número de claves eliminadas
            
        Raises:
            CacheError: Si hay un error al eliminar
        """
        pass

    @abstractmethod
    async def start(self) -> None:
        """
        Inicia el servicio de caché.
        
        Raises:
            ConnectionError: Si hay un error al conectar
        """
        pass

    @abstractmethod
    async def stop(self) -> None:
        """
        Detiene el servicio de caché.
        
        Raises:
            CacheError: Si hay un error al detener
        """
        pass

    @abstractmethod
    async def get_stats(self) -> CacheStats:
        """
        Obtiene estadísticas del caché.
        
        Returns:
            CacheStats: Estadísticas actuales
            
        Raises:
            CacheError: Si hay un error al obtener estadísticas
        """
        pass

    async def get_many(self, keys: List[str]) -> Dict[str, T]:
        """
        Recupera múltiples valores del caché.
        
        Args:
            keys: Lista de claves a recuperar
            
        Returns:
            Dict[str, T]: Diccionario con los valores encontrados
            
        Raises:
            CacheError: Si hay un error al recuperar
        """
        result = {}
        for key in keys:
            value = await self.get(key)
            if value is not None:
                result[key] = value
        return result

    async def set_many(self, values: Dict[str, T], ttl: Optional[timedelta] = None) -> None:
        """
        Almacena múltiples valores en el caché.
        
        Args:
            values: Diccionario de valores a almacenar
            ttl: Tiempo de vida opcional
            
        Raises:
            CacheError: Si hay un error al almacenar
        """
        for key, value in values.items():
            await self.set(key, value, ttl) 