from typing import Dict, Any, Optional, List, TypeVar, Generic
from ..utils.validator import OPERATORS, validate_input, ValidationError
from ..utils.logger import logger

T = TypeVar('T')

class Table(Generic[T]):
    def __init__(self, db, table_name: str):
        self._db = db
        self._schema = db.config['schema']
        self._table = table_name

    async def findUnique(self, where: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Encuentra un registro por su clave única"""
        try:
            validate_input(where=where)
        except ValidationError as e:
            logger.error(f"Error de validación en findUnique: {e}")
            raise

        query = f'SELECT * FROM "{self._schema}"."{self._table}" WHERE'
        conditions = [f'"{k}" = ${i+1}' for i, k in enumerate(where.keys())]
        query += ' AND '.join(conditions)
        return await self._db.driver.fetch_one(query, *where.values())

    async def findFirst(self, 
        where: Optional[Dict[str, Any]] = None,
        orderBy: Optional[Dict[str, str]] = None,
        select: Optional[Dict[str, bool]] = None
    ) -> Optional[Dict[str, Any]]:
        """Encuentra el primer registro que coincida"""
        try:
            validate_input(where=where, order_by=orderBy, select=select, take=1)
        except ValidationError as e:
            logger.error(f"Error de validación en findFirst: {e}")
            raise

        results = await self.findMany(where=where, orderBy=orderBy, select=select, take=1)
        return results[0] if results else None

    def _build_where_condition(self, field: str, value: Any, param_offset: int) -> tuple[str, list]:
        """Construye una condición WHERE con soporte para operadores"""
        params = []
        
        if isinstance(value, dict):
            conditions = []
            for op, val in value.items():
                if op not in OPERATORS:
                    raise ValueError(f"Operador no soportado: {op}")
                    
                sql_op = OPERATORS[op]
                placeholder = f"${param_offset + len(params) + 1}"
                
                if op in ["contains", "notContains"]:
                    conditions.append(f'"{field}" {sql_op} {placeholder}')
                    params.append(f"%{val}%")
                elif op == "startsWith":
                    conditions.append(f'"{field}" {sql_op} {placeholder}')
                    params.append(f"{val}%")
                elif op == "endsWith":
                    conditions.append(f'"{field}" {sql_op} {placeholder}')
                    params.append(f"%{val}")
                elif op in ["between", "notBetween"]:
                    conditions.append(f'"{field}" {sql_op} ${param_offset + len(params) + 1} AND ${param_offset + len(params) + 2}')
                    params.extend(val)
                elif op in ["in", "notIn"]:
                    placeholders = [f"${param_offset + len(params) + i + 1}" for i in range(len(val))]
                    conditions.append(f'"{field}" {sql_op} ({",".join(placeholders)})')
                    params.extend(val)
                else:
                    conditions.append(f'"{field}" {sql_op} {placeholder}')
                    params.append(val)
                    
            return " AND ".join(conditions), params
        else:
            # Caso simple: igualdad
            return f'"{field}" = ${param_offset + 1}', [value]

    async def findMany(self,
        where: Optional[Dict[str, Any]] = None,
        orderBy: Optional[Dict[str, str]] = None,
        select: Optional[Dict[str, bool]] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Encuentra múltiples registros"""
        try:
            validate_input(where=where, order_by=orderBy, select=select, take=take, skip=skip)
        except ValidationError as e:
            logger.error(f"Error de validación en findMany: {e}")
            raise

        fields = '*' if not select else ', '.join(f'"{k}"' for k, v in select.items() if v)
        query = f'SELECT {fields} FROM "{self._schema}"."{self._table}"'
        params = []

        if where:
            conditions = []
            for field, value in where.items():
                condition, new_params = self._build_where_condition(field, value, len(params))
                conditions.append(condition)
                params.extend(new_params)
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
        try:
            validate_input(data=data)
        except ValidationError as e:
            logger.error(f"Error de validación en create: {e}")
            raise

        fields = [f'"{k}"' for k in data.keys()]
        values = [f'${i+1}' for i in range(len(data))]
        query = f'INSERT INTO "{self._schema}"."{self._table}" ({", ".join(fields)}) VALUES ({", ".join(values)}) RETURNING *'
        return await self._db.driver.fetch_one(query, *data.values())

    async def update(self,
        where: Dict[str, Any],
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Actualiza registros existentes"""
        try:
            validate_input(where=where, data=data)
        except ValidationError as e:
            logger.error(f"Error de validación en update: {e}")
            raise

        set_values = [f'"{k}" = ${i+1}' for i, k in enumerate(data.keys())]
        where_values = [f'"{k}" = ${i+1+len(data)}' for i, k in enumerate(where.keys())]
        
        query = f'UPDATE "{self._schema}"."{self._table}" SET {", ".join(set_values)} WHERE {" AND ".join(where_values)} RETURNING *'
        return await self._db.driver.fetch_one(query, *data.values(), *where.values())

    async def upsert(self,
        where: Dict[str, Any],
        create: Dict[str, Any],
        update: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Crea o actualiza un registro"""
        try:
            validate_input(where=where, create=create, update=update)
        except ValidationError as e:
            logger.error(f"Error de validación en upsert: {e}")
            raise

        existing = await self.findUnique(where)
        if existing:
            return await self.update(where, update)
        return await self.create(create)

    async def delete(self, where: Dict[str, Any]) -> Dict[str, Any]:
        """Elimina registros"""
        try:
            validate_input(where=where)
        except ValidationError as e:
            logger.error(f"Error de validación en delete: {e}")
            raise

        conditions = [f'"{k}" = ${i+1}' for i, k in enumerate(where.keys())]
        query = f'DELETE FROM "{self._schema}"."{self._table}" WHERE {" AND ".join(conditions)} RETURNING *'
        return await self._db.driver.fetch_one(query, *where.values())

    async def count(self, where: Optional[Dict[str, Any]] = None) -> int:
        """Cuenta registros"""
        try:
            validate_input(where=where)
        except ValidationError as e:
            logger.error(f"Error de validación en count: {e}")
            raise

        query = f'SELECT COUNT(*) as count FROM "{self._schema}"."{self._table}"'
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
        try:
            validate_input(where=where, aggregate={
                "_sum": _sum or [],
                "_avg": _avg or [],
                "_min": _min or [],
                "_max": _max or []
            })
        except ValidationError as e:
            logger.error(f"Error de validación en aggregate: {e}")
            raise

        aggregations = []
        if _sum: aggregations.extend([f'SUM("{field}") as sum_{field}' for field in _sum])
        if _avg: aggregations.extend([f'AVG("{field}") as avg_{field}' for field in _avg])
        if _min: aggregations.extend([f'MIN("{field}") as min_{field}' for field in _min])
        if _max: aggregations.extend([f'MAX("{field}") as max_{field}' for field in _max])
        
        query = f'SELECT {", ".join(aggregations)} FROM "{self._schema}"."{self._table}"'
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
