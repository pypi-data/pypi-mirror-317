from typing import TypeVar, Dict, List, Union, Literal, Any, Optional, overload

T = TypeVar('T')

# Operadores de comparación básicos
ComparisonOperator = Literal[
    "equals", "not",
    "in", "notIn",
    "lt", "lte", "gt", "gte",
    "contains", "notContains",
    "startsWith", "endsWith",
    "between", "notBetween",
    "isNull", "isNotNull",
    "like", "notLike",
    "ilike", "notIlike"
]

# Operadores lógicos
LogicalOperator = Literal["AND", "OR", "NOT"]

# Operadores de ordenamiento
SortOrder = Literal["asc", "desc"]
OrderByInput = Dict[str, SortOrder]

# Operadores de agregación
AggregateOperator = Literal["_count", "_sum", "_avg", "_min", "_max"]

# Tipos para filtros complejos
WhereCondition = Dict[ComparisonOperator, Any]
WhereInput = Dict[str, Union[Any, WhereCondition, List[Dict[LogicalOperator, WhereCondition]]]]

# Tipos para select y include
SelectInput = Dict[str, bool]
IncludeInput = Dict[str, bool]

# Tipos para create/update
CreateInput = Dict[str, Any]
UpdateInput = Dict[str, Any]

# Tipos para agregación
AggregateInput = Dict[AggregateOperator, List[str]]

class QueryOptions:
    """Clase base para opciones de consulta"""
    where: Optional[WhereInput] = None
    orderBy: Optional[OrderByInput] = None
    select: Optional[SelectInput] = None
    take: Optional[int] = None
    skip: Optional[int] = None
    include: Optional[Dict[str, bool]] = None

class FindFirstOptions(QueryOptions):
    """Opciones para findFirst"""
    pass

class FindManyOptions(QueryOptions):
    """Opciones para findMany"""
    pass

class CreateOptions:
    """Opciones para create"""
    data: CreateInput
    select: Optional[SelectInput] = None

class UpdateOptions:
    """Opciones para update"""
    where: WhereInput
    data: UpdateInput
    select: Optional[SelectInput] = None

class UpsertOptions:
    """Opciones para upsert"""
    where: WhereInput
    create: CreateInput
    update: UpdateInput
    select: Optional[SelectInput] = None

class DeleteOptions:
    """Opciones para delete"""
    where: WhereInput
    select: Optional[SelectInput] = None 