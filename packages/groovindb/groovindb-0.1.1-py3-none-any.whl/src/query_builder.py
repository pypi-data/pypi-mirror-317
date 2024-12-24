from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field

@dataclass
class QueryBuilder:
    """Constructor de queries SQL."""
    _where: Dict[str, Any] = field(default_factory=dict)
    _select: List[str] = field(default_factory=list)
    _order_by: List[Tuple[str, str]] = field(default_factory=list)
    _limit: Optional[int] = None
    _offset: Optional[int] = None
    _params: List[Any] = field(default_factory=list)

    def select(self, *fields: str) -> 'QueryBuilder':
        """Agregar campos a seleccionar"""
        self._select.extend(fields)
        return self

    def where(self, **conditions: Any) -> 'QueryBuilder':
        """Agregar condiciones WHERE"""
        self._where.update(conditions)
        return self

    def order_by(self, *fields: str) -> 'QueryBuilder':
        """Agregar ordenamiento"""
        for field in fields:
            if ' ' in field:
                col, direction = field.rsplit(' ', 1)
                self._order_by.append((col, direction.upper()))
            else:
                self._order_by.append((field, 'ASC'))
        return self

    def limit(self, value: int) -> 'QueryBuilder':
        """Establecer límite de resultados"""
        self._limit = value
        return self

    def offset(self, value: int) -> 'QueryBuilder':
        """Establecer offset de resultados"""
        self._offset = value
        return self

    @property
    def params(self) -> List[Any]:
        """Obtener los parámetros acumulados"""
        return self._params

    def build_select_query(
        self,
        schema: str,
        table: str,
        columns: Optional[List[str]] = None,
        where: Optional[Dict[str, Any]] = None,
        order_by: Optional[List[Tuple[str, str]]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> str:
        """Construir una query SELECT."""
        # Usar valores acumulados si no se proporcionan explícitamente
        columns = columns or self._select
        where = where or self._where
        order_by = order_by or self._order_by
        limit = limit if limit is not None else self._limit
        offset = offset if offset is not None else self._offset

        # Construir el nombre de la tabla con el esquema correctamente
        table_name = f'"{schema}"."{table}"' if schema else f'"{table}"'
        fields = "*" if not columns else ", ".join(f'"{col}"' for col in columns)
        query = f"SELECT {fields} FROM {table_name}"

        if where:
            where_clause = self._build_where_clause(where)
            query += f" WHERE {where_clause}"

        if order_by:
            order_clause = ", ".join(f'"{col}" {direction}' for col, direction in order_by)
            query += f" ORDER BY {order_clause}"

        if limit is not None:
            query += f" LIMIT {limit}"

        if offset is not None:
            query += f" OFFSET {offset}"

        return query

    def reset(self) -> None:
        """Reiniciar el estado del builder"""
        self._where.clear()
        self._select.clear()
        self._order_by.clear()
        self._limit = None
        self._offset = None
        self._params.clear()

    def build_insert_query(
        self,
        schema: str,
        table: str,
        data: Dict[str, Any]
    ) -> str:
        """Construir una query INSERT."""
        # Construir el nombre de la tabla con el esquema correctamente
        table_name = f'"{schema}"."{table}"' if schema else f'"{table}"'
        columns = [f'"{k}"' for k in data.keys()]
        placeholders = [f"${i+1}" for i in range(len(data))]
        
        return (
            f"INSERT INTO {table_name} ({', '.join(columns)}) "
            f"VALUES ({', '.join(placeholders)})"
        )

    def build_update_query(
        self,
        schema: str,
        table: str,
        where: Dict[str, Any],
        data: Dict[str, Any]
    ) -> str:
        """Construir una query UPDATE."""
        # Construir el nombre de la tabla con el esquema correctamente
        table_name = f'"{schema}"."{table}"' if schema else f'"{table}"'
        set_clause = ", ".join(f'"{k}" = ${i+1}' for i, k in enumerate(data.keys()))
        where_clause = self._build_where_clause(where, start_position=len(data)+1)
        
        return (
            f"UPDATE {table_name} "
            f"SET {set_clause} "
            f"WHERE {where_clause}"
        )

    def build_delete_query(
        self,
        schema: str,
        table: str,
        where: Dict[str, Any]
    ) -> str:
        """Construir una query DELETE."""
        # Construir el nombre de la tabla con el esquema correctamente
        table_name = f'"{schema}"."{table}"' if schema else f'"{table}"'
        where_clause = self._build_where_clause(where)
        
        return f"DELETE FROM {table_name} WHERE {where_clause}"

    def _build_where_clause(
        self,
        conditions: Dict[str, Any],
        start_position: int = 1
    ) -> str:
        """Construir la cláusula WHERE de una query."""
        if not conditions:
            return "1=1"

        parts = []
        position = start_position

        for key, value in conditions.items():
            if key.upper() in ("AND", "OR"):
                sub_conditions = []
                for sub_condition in value:
                    sub_clause, sub_position = self._build_where_clause(
                        sub_condition,
                        position
                    )
                    sub_conditions.append(sub_clause)
                    position = sub_position
                parts.append(f" {key} ".join(sub_conditions))
            else:
                if isinstance(value, dict):
                    operator = next(iter(value))
                    operator_value = value[operator]
                    if operator.lower() == "like":
                        parts.append(f'"{key}" LIKE ${position}')
                    elif operator.lower() in ("gt", ">"):
                        parts.append(f'"{key}" > ${position}')
                    elif operator.lower() in ("lt", "<"):
                        parts.append(f'"{key}" < ${position}')
                    elif operator.lower() in ("gte", ">="):
                        parts.append(f'"{key}" >= ${position}')
                    elif operator.lower() in ("lte", "<="):
                        parts.append(f'"{key}" <= ${position}')
                    elif operator.lower() in ("ne", "!="):
                        parts.append(f'"{key}" != ${position}')
                    position += 1
                else:
                    parts.append(f'"{key}" = ${position}')
                    position += 1

        return " AND ".join(parts)