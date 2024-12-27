"""
Factory para crear instancias de caché según la configuración.
"""
from typing import Dict, Any
from datetime import timedelta
from .base import CacheProvider, CacheConfig, CompressionLevel
from .memory import MemoryCache
from .redis import RedisCache

class CacheFactory:
    @staticmethod
    def create(config: Dict[str, Any]) -> CacheProvider:
        # Crear configuración base
        cache_config = CacheConfig(
            ttl=timedelta(seconds=config.get('ttl', 300)),
            compression_level=CompressionLevel(config.get('compression_level', 0)),
            retry_attempts=config.get('retry_attempts', 3),
            retry_delay=config.get('retry_delay', 1.0),
            timeout=config.get('timeout', 5.0)
        )
        
        cache_type = config.get('type', 'memory')
        
        if cache_type == 'memory':
            return MemoryCache(config=cache_config)
        elif cache_type == 'redis':
            redis_url = config.get('url', 'redis://localhost')
            return RedisCache(url=redis_url, config=cache_config)
        else:
            raise ValueError(f"Tipo de caché no soportado: {cache_type}") 