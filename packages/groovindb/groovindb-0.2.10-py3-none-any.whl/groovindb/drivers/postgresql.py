from typing import Dict, Any, List, Optional
import asyncpg
from .base import BaseDriver

class PostgreSQLDriver(BaseDriver):
    def __init__(self):
        self.conn = None

    async def connect(self, dsn: str) -> None:
        self.conn = await asyncpg.connect(dsn)

    async def close(self) -> None:
        if self.conn:
            await self.conn.close()

    async def fetch(self, query: str, *args) -> List[Dict[str, Any]]:
        records = await self.conn.fetch(query, *args)
        return [dict(r) for r in records]

    async def fetch_one(self, query: str, *args) -> Optional[Dict[str, Any]]:
        record = await self.conn.fetchrow(query, *args)
        return dict(record) if record else None

    async def execute(self, query: str, *args) -> None:
        """Ejecuta una query sin retornar resultados"""
        await self.conn.execute(query, *args) 