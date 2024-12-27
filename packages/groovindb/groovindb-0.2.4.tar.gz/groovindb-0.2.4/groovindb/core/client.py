from typing import Dict, Any, Optional, List, Union, TypeVar, Generic, overload
from ..types import (
    FindFirstOptions, FindManyOptions, CreateOptions,
    UpdateOptions, UpsertOptions, DeleteOptions,
    WhereInput, OrderByInput, SelectInput
)

T = TypeVar('T')

class Table(Generic[T]):
    def __init__(self, db, table_name: str):
        self._db = db
        self._schema = db.config['schema']
        self._table = f"{self._schema}.{table_name}"

    @overload
    async def findFirst(self, options: FindFirstOptions) -> Optional[T]: 
        ...

    @overload
    async def findFirst(self,
        where: Optional[WhereInput] = None,
        orderBy: Optional[OrderByInput] = None,
        select: Optional[SelectInput] = None,
        include: Optional[Dict[str, bool]] = None
    ) -> Optional[T]: 
        ...

    async def findFirst(self, 
        options: Union[FindFirstOptions, Dict] = None,
        **kwargs
    ) -> Optional[T]:
        if isinstance(options, FindFirstOptions):
            where = options.where
            orderBy = options.orderBy
            select = options.select
            include = options.include
        else:
            where = options or kwargs.get('where')
            orderBy = kwargs.get('orderBy')
            select = kwargs.get('select')
            include = kwargs.get('include')

        fields = "*" if not select else ", ".join(select)
        query = f"SELECT {fields} FROM {self._table}"
        params = []
        
        if where:
            conditions = []
            for i, (k, v) in enumerate(where.items()):
                if isinstance(v, dict):
                    for op, val in v.items():
                        op_map = {
                            "gt": ">", "lt": "<", "gte": ">=", "lte": "<=",
                            "contains": "LIKE", "startsWith": "LIKE", "endsWith": "LIKE",
                            "not": "IS NOT"
                        }
                        if op in ["contains", "startsWith", "endsWith"]:
                            if op == "contains":
                                val = f"%{val}%"
                            elif op == "startsWith":
                                val = f"{val}%"
                            else:
                                val = f"%{val}"
                            conditions.append(f"{k} LIKE ${len(params) + 1}")
                            params.append(val)
                        elif op == "not" and val is None:
                            conditions.append(f"{k} IS NOT NULL")
                        else:
                            conditions.append(f"{k} {op_map.get(op, '=')} ${len(params) + 1}")
                            params.append(val)
                else:
                    if v is None:
                        conditions.append(f"{k} IS NULL")
                    else:
                        conditions.append(f"{k} = ${len(params) + 1}")
                        params.append(v)
            query += f" WHERE {' AND '.join(conditions)}"

        if orderBy:
            order_clauses = [f"{list(item.keys())[0]} {list(item.values())[0].upper()}" 
                           for item in orderBy]
            query += f" ORDER BY {', '.join(order_clauses)}"

        query += " LIMIT 1"
        return await self._db.driver.fetch_one(query, *params)

    @overload
    async def findMany(self, options: FindManyOptions) -> List[T]: 
        ...

    @overload
    async def findMany(self,
        where: Optional[WhereInput] = None,
        orderBy: Optional[OrderByInput] = None,
        select: Optional[SelectInput] = None,
        include: Optional[Dict[str, bool]] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
    ) -> List[T]: 
        ...

    async def findMany(self,
        options: Union[FindManyOptions, Dict] = None,
        **kwargs
    ) -> List[T]:
        if isinstance(options, FindManyOptions):
            where = options.where
            orderBy = options.orderBy
            select = options.select
            include = options.include
            take = options.take
            skip = options.skip
        else:
            where = options or kwargs.get('where')
            orderBy = kwargs.get('orderBy')
            select = kwargs.get('select')
            include = kwargs.get('include')
            take = kwargs.get('take')
            skip = kwargs.get('skip')

        fields = "*" if not select else ", ".join(select)
        query = f"SELECT {fields} FROM {self._table}"
        params = []

        if where:
            conditions = []
            for i, (k, v) in enumerate(where.items()):
                if isinstance(v, dict):
                    for op, val in v.items():
                        op_map = {
                            "gt": ">", "lt": "<", "gte": ">=", "lte": "<=",
                            "contains": "LIKE", "in": "IN", "notIn": "NOT IN",
                            "not": "IS NOT"
                        }
                        if op in ["contains"]:
                            val = f"%{val}%"
                            conditions.append(f"{k} LIKE ${len(params) + 1}")
                            params.append(val)
                        elif op in ["in", "notIn"]:
                            placeholders = [f"${len(params) + i + 1}" for i in range(len(val))]
                            conditions.append(f"{k} {op_map[op]} ({','.join(placeholders)})")
                            params.extend(val)
                        elif op == "not" and val is None:
                            conditions.append(f"{k} IS NOT NULL")
                        else:
                            conditions.append(f"{k} {op_map.get(op, '=')} ${len(params) + 1}")
                            params.append(val)
                else:
                    if v is None:
                        conditions.append(f"{k} IS NULL")
                    else:
                        conditions.append(f"{k} = ${len(params) + 1}")
                        params.append(v)
            query += f" WHERE {' AND '.join(conditions)}"

        if orderBy:
            order_clauses = [f"{list(item.keys())[0]} {list(item.values())[0].upper()}" 
                           for item in orderBy]
            query += f" ORDER BY {', '.join(order_clauses)}"

        if take is not None:
            query += f" LIMIT {take}"
        if skip is not None:
            query += f" OFFSET {skip}"

        return await self._db.driver.fetch(query, *params)

    async def count(self, where: Optional[Dict[str, Any]] = None) -> int:
        query = f"SELECT COUNT(*) as count FROM {self._table}"
        if where:
            conditions = []
            params = []
            for k, v in where.items():
                if isinstance(v, dict):
                    for op, val in v.items():
                        op_map = {
                            "gt": ">", "lt": "<", "gte": ">=", "lte": "<=",
                            "contains": "LIKE", "in": "IN", "notIn": "NOT IN",
                            "not": "IS NOT"
                        }
                        if op == "not" and val is None:
                            conditions.append(f"{k} IS NOT NULL")
                        else:
                            conditions.append(f"{k} {op_map.get(op, '=')} ${len(params) + 1}")
                            params.append(val)
                else:
                    if v is None:
                        conditions.append(f"{k} IS NULL")
                    else:
                        conditions.append(f"{k} = ${len(params) + 1}")
                        params.append(v)
            query += f" WHERE {' AND '.join(conditions)}"
            result = await self._db.driver.fetch_one(query, *params)
        else:
            result = await self._db.driver.fetch_one(query)
        return result["count"]

    @overload
    async def create(self, options: CreateOptions) -> T:
        ...

    @overload
    async def create(self,
        data: Dict[str, Any],
        select: Optional[SelectInput] = None
    ) -> T:
        ...

    async def create(self,
        options: Union[CreateOptions, Dict[str, Any]],
        **kwargs
    ) -> T:
        if isinstance(options, CreateOptions):
            data = options.data
            select = options.select
        else:
            data = options
            select = kwargs.get('select')

        columns = ", ".join(data.keys())
        placeholders = ", ".join(f"${i+1}" for i in range(len(data)))
        returning = "*" if not select else ", ".join(select)
        query = f"INSERT INTO {self._table} ({columns}) VALUES ({placeholders}) RETURNING {returning}"
        return await self._db.driver.fetch_one(query, *data.values())

    @overload
    async def update(self, options: UpdateOptions) -> T:
        ...

    @overload
    async def update(self,
        where: WhereInput,
        data: Dict[str, Any],
        select: Optional[SelectInput] = None
    ) -> T:
        ...

    async def update(self,
        options: Union[UpdateOptions, Dict[str, Any]],
        data: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> T:
        if isinstance(options, UpdateOptions):
            where = options.where
            data = options.data
            select = options.select
        else:
            where = options
            select = kwargs.get('select')

        set_values = [f"{k} = ${i+1}" for i, k in enumerate(data.keys())]
        where_values = [f"{k} = ${i+1}" for i, k in enumerate(where.keys(), start=len(data))]
        returning = "*" if not select else ", ".join(select)
        query = f"UPDATE {self._table} SET {', '.join(set_values)} WHERE {' AND '.join(where_values)} RETURNING {returning}"
        return await self._db.driver.fetch_one(query, *data.values(), *where.values())

    @overload
    async def upsert(self, options: UpsertOptions) -> T:
        ...

    @overload
    async def upsert(self,
        where: WhereInput,
        create: Dict[str, Any],
        update: Dict[str, Any],
        select: Optional[SelectInput] = None
    ) -> T:
        ...

    async def upsert(self,
        options: Union[UpsertOptions, Dict[str, Any]],
        create: Optional[Dict[str, Any]] = None,
        update: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> T:
        if isinstance(options, UpsertOptions):
            where = options.where
            create = options.create
            update = options.update
            select = options.select
        else:
            where = options
            select = kwargs.get('select')

        columns = ", ".join(create.keys())
        placeholders = ", ".join(f"${i+1}" for i in range(len(create)))
        
        set_values = [f"{k} = EXCLUDED.{k}" for k in update.keys()]
        conflict_target = list(where.keys())[0]
        
        returning = "*" if not select else ", ".join(select)
        
        query = f"""
            INSERT INTO {self._table} ({columns})
            VALUES ({placeholders})
            ON CONFLICT ({conflict_target})
            DO UPDATE SET {', '.join(set_values)}
            RETURNING {returning}
        """
        return await self._db.driver.fetch_one(query, *create.values())

    @overload
    async def delete(self, options: DeleteOptions) -> T:
        ...

    @overload
    async def delete(self,
        where: WhereInput,
        select: Optional[SelectInput] = None
    ) -> T:
        ...

    async def delete(self,
        options: Union[DeleteOptions, Dict[str, Any]],
        **kwargs
    ) -> T:
        if isinstance(options, DeleteOptions):
            where = options.where
            select = options.select
        else:
            where = options
            select = kwargs.get('select')

        conditions = [f"{k} = ${i+1}" for i, k in enumerate(where.keys())]
        returning = "*" if not select else ", ".join(select)
        query = f"DELETE FROM {self._table} WHERE {' AND '.join(conditions)} RETURNING {returning}"
        return await self._db.driver.fetch_one(query, *where.values())

    async def query(self, sql: str, *params: Any) -> List[Dict[str, Any]]:
        """Ejecutar consulta SQL raw que retorna resultados"""
        return await self._db.driver.fetch(sql, *params)

    async def execute(self, sql: str, *params: Any) -> None:
        """Ejecutar consulta SQL raw sin retorno"""
        await self._db.driver.execute(sql, *params)

class BaseClient:
    """Clase base para el cliente generado"""
    def __init__(self, db):
        self._db = db
        self._tables: Dict[str, Table] = {}

    def __getattr__(self, name: str) -> Table:
        if name not in self._tables:
            if name not in self._db.tables:
                raise AttributeError(f"Tabla '{name}' no encontrada en la base de datos")
            self._tables[name] = Table(self._db, name)
        return self._tables[name]

# La clase Client real será generada y heredará de BaseClient
Client = BaseClient
