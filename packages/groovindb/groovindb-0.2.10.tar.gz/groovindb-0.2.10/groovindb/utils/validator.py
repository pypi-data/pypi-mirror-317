from typing import Any, Dict, List, Optional
from ..types import (
    WhereInput, OrderByInput, SelectInput, CreateInput, UpdateInput,
    AggregateInput
)

class ValidationError(Exception):
    """Error de validación personalizado"""
    pass

# Definición unificada de operadores y sus mapeos SQL
OPERATORS = {
    "equals": "=",
    "not": "!=",
    "gt": ">",
    "gte": ">=",
    "lt": "<",
    "lte": "<=",
    "in": "IN",
    "notIn": "NOT IN",
    "contains": "LIKE",
    "notContains": "NOT LIKE",
    "startsWith": "LIKE",
    "endsWith": "LIKE",
    "between": "BETWEEN",
    "notBetween": "NOT BETWEEN"
}

# Operadores de agregación válidos
AGGREGATE_OPERATORS = ["_sum", "_avg", "_min", "_max", "_count"]

def validate_where(where: Optional[WhereInput]) -> None:
    """Valida condiciones WHERE"""
    if not where:
        return
    
    for field, condition in where.items():
        if isinstance(condition, dict):
            for op, value in condition.items():
                if op not in OPERATORS:
                    raise ValidationError(f"Operador inválido: {op}")
                
                # Validaciones específicas por operador
                if op in ["in", "notIn"] and not isinstance(value, (list, tuple)):
                    raise ValidationError(f"El operador {op} requiere una lista de valores")
                if op in ["between", "notBetween"] and not (
                    isinstance(value, (list, tuple)) and len(value) == 2
                ):
                    raise ValidationError(f"El operador {op} requiere exactamente 2 valores")

def validate_order_by(order_by: Optional[OrderByInput]) -> None:
    """Valida ordenamiento"""
    if not order_by:
        return
    
    for field, direction in order_by.items():
        if not isinstance(direction, SortOrder):
            raise ValidationError(f"Dirección de ordenamiento inválida: {direction}")

def validate_select(select: Optional[SelectInput]) -> None:
    """Valida campos seleccionados"""
    if not select:
        return
    
    if not isinstance(select, dict):
        raise ValidationError("Select debe ser un diccionario")
    
    for field, include in select.items():
        if not isinstance(include, bool):
            raise ValidationError(f"Valor inválido en select para {field}")

def validate_aggregate(aggregate: Optional[AggregateInput]) -> None:
    """Valida operaciones de agregación"""
    if not aggregate:
        return
    
    for op, fields in aggregate.items():
        if op not in AGGREGATE_OPERATORS:
            raise ValidationError(f"Operador de agregación inválido: {op}")
        if not isinstance(fields, list):
            raise ValidationError(f"Los campos para {op} deben ser una lista")

def validate_input(
    where: Optional[WhereInput] = None,
    order_by: Optional[OrderByInput] = None,
    select: Optional[SelectInput] = None,
    take: Optional[int] = None,
    skip: Optional[int] = None,
    aggregate: Optional[AggregateInput] = None
) -> None:
    """Valida todos los inputs de una consulta"""
    validate_where(where)
    validate_order_by(order_by)
    validate_select(select)
    
    if take is not None and not isinstance(take, int):
        raise ValidationError("take debe ser un número entero")
    if skip is not None and not isinstance(skip, int):
        raise ValidationError("skip debe ser un número entero")
    
    if aggregate:
        validate_aggregate(aggregate) 