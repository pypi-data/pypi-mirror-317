from typing import Any, Dict, Type, Optional, Union
from datetime import datetime
from enum import Enum

class FieldType(Enum):
    INTEGER = "INTEGER"
    BIGINT = "BIGINT"
    VARCHAR = "VARCHAR"
    TEXT = "TEXT"
    BOOLEAN = "BOOLEAN"
    TIMESTAMP = "TIMESTAMP"
    FLOAT = "FLOAT"
    DECIMAL = "DECIMAL"
    JSON = "JSON"
    UUID = "UUID"

class Field:
    def __init__(
        self,
        field_type: FieldType,
        primary_key: bool = False,
        nullable: bool = True,
        unique: bool = False,
        default: Any = None,
        length: Optional[int] = None,
        foreign_key: Optional[str] = None
    ):
        self.field_type = field_type
        self.primary_key = primary_key
        self.nullable = nullable
        self.unique = unique
        self.default = default
        self.length = length
        self.foreign_key = foreign_key

class TypeMapper:
    POSTGRES_TYPES = {
        FieldType.INTEGER: "INTEGER",
        FieldType.BIGINT: "BIGINT",
        FieldType.VARCHAR: "VARCHAR",
        FieldType.TEXT: "TEXT",
        FieldType.BOOLEAN: "BOOLEAN",
        FieldType.TIMESTAMP: "TIMESTAMP WITH TIME ZONE",
        FieldType.FLOAT: "DOUBLE PRECISION",
        FieldType.DECIMAL: "NUMERIC",
        FieldType.JSON: "JSONB",
        FieldType.UUID: "UUID"
    }

    MYSQL_TYPES = {
        FieldType.INTEGER: "INT",
        FieldType.BIGINT: "BIGINT",
        FieldType.VARCHAR: "VARCHAR",
        FieldType.TEXT: "TEXT",
        FieldType.BOOLEAN: "TINYINT(1)",
        FieldType.TIMESTAMP: "DATETIME",
        FieldType.FLOAT: "DOUBLE",
        FieldType.DECIMAL: "DECIMAL",
        FieldType.JSON: "JSON",
        FieldType.UUID: "CHAR(36)"
    }

    @classmethod
    def get_type(cls, field: Field, driver: str) -> str:
        type_map = cls.POSTGRES_TYPES if driver == 'postgresql' else cls.MYSQL_TYPES
        base_type = type_map[field.field_type]
        
        if field.field_type == FieldType.VARCHAR and field.length:
            return f"{base_type}({field.length})"
        return base_type 