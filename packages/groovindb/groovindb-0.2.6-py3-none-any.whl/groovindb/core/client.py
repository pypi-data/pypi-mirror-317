from typing import Dict, Any, Optional, List, TypeVar, Generic, Union, overload
from ..types import WhereInput, OrderByInput, SelectInput

T = TypeVar('T')

class Table(Generic[T]):
    def __init__(self, db, table_name: str):
        self._db = db
        self._schema = db.config['schema']
        self._table = table_name

    async def findUnique(self, where: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Encuentra un registro por su clave única"""
        query = f'SELECT * FROM "{self._table}" WHERE'
        conditions = [f'"{k}" = ${i+1}' for i, k in enumerate(where.keys())]
        query += ' AND '.join(conditions)
        return await self._db.driver.fetch_one(query, *where.values())

    async def findFirst(self, 
        where: Optional[Dict[str, Any]] = None,
        orderBy: Optional[Dict[str, str]] = None,
        select: Optional[Dict[str, bool]] = None
    ) -> Optional[Dict[str, Any]]:
        """Encuentra el primer registro que coincida"""
        results = await self.findMany(where=where, orderBy=orderBy, select=select, take=1)
        return results[0] if results else None

    async def findMany(self,
        where: Optional[Dict[str, Any]] = None,
        orderBy: Optional[Dict[str, str]] = None,
        select: Optional[Dict[str, bool]] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Encuentra múltiples registros"""
        fields = '*' if not select else ', '.join(f'"{k}"' for k, v in select.items() if v)
        query = f'SELECT {fields} FROM "{self._schema}"."{self._table}"'
        params = []

        if where:
            conditions = []
            for field, value in where.items():
                conditions.append(f'"{field}" = ${len(params) + 1}')
                params.append(value)
            if conditions:
                query += " WHERE " + " AND ".join(conditions)

        if orderBy:
            orders = [f'"{field}" {direction.upper()}' for field, direction in orderBy.items()]
            query += " ORDER BY " + ", ".join(orders)

        if take:
            query += f" LIMIT {take}"
        if skip:
            query += f" OFFSET {skip}"

        return await self._db.driver.fetch(query, *params)

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo registro"""
        fields = [f'"{k}"' for k in data.keys()]
        values = [f'${i+1}' for i in range(len(data))]
        query = f'INSERT INTO "{self._table}" ({", ".join(fields)}) VALUES ({", ".join(values)}) RETURNING *'
        return await self._db.driver.fetch_one(query, *data.values())

    async def update(self,
        where: Dict[str, Any],
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Actualiza registros existentes"""
        set_values = [f'"{k}" = ${i+1}' for i, k in enumerate(data.keys())]
        where_values = [f'"{k}" = ${i+1+len(data)}' for i, k in enumerate(where.keys())]
        
        query = f'UPDATE "{self._table}" SET {", ".join(set_values)} WHERE {" AND ".join(where_values)} RETURNING *'
        return await self._db.driver.fetch_one(query, *data.values(), *where.values())

    async def upsert(self,
        where: Dict[str, Any],
        create: Dict[str, Any],
        update: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Crea o actualiza un registro"""
        existing = await self.findUnique(where)
        if existing:
            return await self.update(where, update)
        return await self.create(create)

    async def delete(self, where: Dict[str, Any]) -> Dict[str, Any]:
        """Elimina registros"""
        conditions = [f'"{k}" = ${i+1}' for i, k in enumerate(where.keys())]
        query = f'DELETE FROM "{self._table}" WHERE {" AND ".join(conditions)} RETURNING *'
        return await self._db.driver.fetch_one(query, *where.values())

    async def count(self, where: Optional[Dict[str, Any]] = None) -> int:
        """Cuenta registros"""
        query = f'SELECT COUNT(*) as count FROM "{self._table}"'
        params = []
        
        if where:
            conditions = []
            for field, value in where.items():
                conditions.append(f'"{field}" = ${len(params) + 1}')
                params.append(value)
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
                
        result = await self._db.driver.fetch_one(query, *params)
        return result['count']

    async def aggregate(self,
        where: Optional[Dict[str, Any]] = None,
        _sum: Optional[List[str]] = None,
        _avg: Optional[List[str]] = None,
        _min: Optional[List[str]] = None,
        _max: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Realiza operaciones de agregación"""
        aggregations = []
        if _sum: aggregations.extend([f'SUM("{field}") as sum_{field}' for field in _sum])
        if _avg: aggregations.extend([f'AVG("{field}") as avg_{field}' for field in _avg])
        if _min: aggregations.extend([f'MIN("{field}") as min_{field}' for field in _min])
        if _max: aggregations.extend([f'MAX("{field}") as max_{field}' for field in _max])
        
        query = f'SELECT {", ".join(aggregations)} FROM "{self._table}"'
        params = []

        if where:
            conditions = []
            for field, value in where.items():
                conditions.append(f'"{field}" = ${len(params) + 1}')
                params.append(value)
            if conditions:
                query += " WHERE " + " AND ".join(conditions)

        return await self._db.driver.fetch_one(query, *params)

class Client:
    def __init__(self, db):
        self._db = db
        # Inicializar tablas dinámicamente
        for table_name in db.tables:
            setattr(self, table_name, Table(db, table_name))

    async def query(self, query: str, *args) -> List[Dict[str, Any]]:
        """Ejecuta una consulta SQL raw"""
        return await self._db.driver.fetch(query, *args)
