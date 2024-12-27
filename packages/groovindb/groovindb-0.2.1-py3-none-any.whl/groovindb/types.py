from typing import TypeVar, Dict, List, Union, Literal, Any, Optional, overload

T = TypeVar('T')

# Operadores de comparación
ComparisonOperators = Dict[Literal[
    "equals", "not",
    "in", "notIn",
    "lt", "lte", "gt", "gte",
    "contains", "startsWith", "endsWith",
    "isEmpty", "isNotEmpty"
], Any]

# Operadores de ordenamiento
SortOrder = Literal["asc", "desc"]
OrderByInput = List[Dict[str, SortOrder]]

# Tipos para select y where
WhereInput = Dict[str, Union[Any, ComparisonOperators]]
SelectInput = List[str]

# Tipos para create/update
CreateInput = Dict[str, Any]
UpdateInput = Dict[str, Any]

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