"""
Implementación de caché Redis para GroovinDB.
"""
from datetime import timedelta
from typing import Any, Optional
from redis.asyncio import Redis
from .base import CacheProvider, CacheStats, CacheConfig
import json

class RedisCache(CacheProvider):
    def __init__(self, url: str = "redis://localhost"):
        super().__init__()
        self._url = url
        self._redis: Optional[Redis] = None

    async def start(self) -> None:
        self._redis = Redis.from_url(self._url)

    async def stop(self) -> None:
        if self._redis:
            await self._redis.close()

    async def set(self, key: str, value: Any, ttl: timedelta) -> None:
        try:
            serialized = self._serialize(value)
            await self._redis.set(key, serialized, ex=int(ttl.total_seconds()))
        except Exception as e:
            self.stats.errors += 1
            raise

    async def get(self, key: str) -> Optional[Any]:
        try:
            value = await self._redis.get(key)
            if value:
                self.stats.hits += 1
                return self._deserialize(value)
            self.stats.misses += 1
            return None
        except Exception as e:
            self.stats.errors += 1
            raise

    async def delete(self, key: str) -> bool:
        try:
            return bool(await self._redis.delete(key))
        except Exception as e:
            self.stats.errors += 1
            raise

    async def clear(self) -> None:
        try:
            await self._redis.flushdb()
        except Exception as e:
            self.stats.errors += 1
            raise

    async def delete_pattern(self, pattern: str) -> int:
        try:
            keys = await self._redis.keys(f"*{pattern}*")
            if keys:
                return await self._redis.delete(*keys)
            return 0
        except Exception as e:
            self.stats.errors += 1
            raise

    async def get_stats(self) -> CacheStats:
        """Obtener estadísticas del caché."""
        try:
            info = await self._redis.info()
            self.stats.memory_usage = float(info['used_memory']) / 1024 / 1024  # Convertir a MB
            return self.stats
        except Exception as e:
            self.stats.errors += 1
            raise 