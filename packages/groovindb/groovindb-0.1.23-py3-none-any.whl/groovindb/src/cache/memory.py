"""
Implementación de caché en memoria para GroovinDB.
"""
from datetime import datetime, timedelta
from typing import Any, Optional, Dict
import asyncio
import psutil
from .base import CacheProvider, CacheStats, CacheConfig

class MemoryCache(CacheProvider):
    def __init__(self, config: Optional[CacheConfig] = None):
        super().__init__(config)
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._cleanup_task = None
        self._process = psutil.Process()

    async def set(self, key: str, value: Any, ttl: timedelta) -> None:
        self._cache[key] = {
            'value': value,
            'expires_at': datetime.now() + ttl
        }

    async def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            data = self._cache[key]
            if datetime.now() < data['expires_at']:
                self.stats.hits += 1
                return data['value']
            await self.delete(key)
        self.stats.misses += 1
        return None

    async def delete(self, key: str) -> None:
        self._cache.pop(key, None)

    async def clear(self) -> None:
        self._cache.clear()

    async def delete_pattern(self, pattern: str) -> None:
        keys = [k for k in self._cache if pattern in k]
        for key in keys:
            await self.delete(key)

    async def start(self) -> None:
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())

    async def stop(self) -> None:
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass

    async def get_stats(self) -> CacheStats:
        """Obtener estadísticas del caché."""
        try:
            self.stats.memory_usage = self._process.memory_info().rss / 1024 / 1024  # Convertir a MB
            return self.stats
        except Exception as e:
            self.stats.errors += 1
            raise

    async def _cleanup_loop(self) -> None:
        while True:
            now = datetime.now()
            expired = [k for k, v in self._cache.items() if v['expires_at'] < now]
            for key in expired:
                await self.delete(key)
            await asyncio.sleep(60) 