from typing import ClassVar, Dict, Type, Any, Optional
from dataclasses import dataclass
from .schema import Field, FieldType

@dataclass
class ModelConfig:
    driver: str = 'postgresql'
    schema: str = 'public'
    timestamps: bool = True

class Model:
    __table__: ClassVar[str]
    __fields__: ClassVar[Dict[str, Field]]
    __column_map__: ClassVar[Dict[str, str]]
    __config__: ClassVar[ModelConfig] = ModelConfig()
    __cache_ttl__: ClassVar[int] = 300

    def __init__(self, **kwargs):
        self._relations = None
        self._data: Dict[str, Any] = {}
        
        # Establecer valores por defecto
        for field_name, field in self.__fields__.items():
            if field.default is not None:
                self._data[field_name] = field.default
        
        # Mapear nombres de columnas si es necesario
        for key, value in kwargs.items():
            safe_key = key.replace('-', '_')
            self._data[safe_key] = value

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any):
        if name.startswith('_'):
            super().__setattr__(name, value)
        elif name in getattr(self, '__fields__', {}):
            self._data[name] = value
        else:
            super().__setattr__(name, value)

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el modelo a diccionario usando los nombres originales"""
        result = {}
        for key, value in self._data.items():
            original_key = self.__column_map__.get(key, key)
            result[original_key] = value
        return result

    @classmethod
    def get_field_definitions(cls) -> Dict[str, str]:
        type_mapper = TypeMapper()
        definitions = {}
        
        for field_name, field in cls.__fields__.items():
            # Usar el nombre original de la columna si existe
            original_name = cls.__column_map__.get(field_name, field_name)
            sql_type = type_mapper.get_type(field, cls.__config__.driver)
            
            definition = [sql_type]
            
            if field.primary_key:
                if cls.__config__.driver == 'postgresql':
                    definition.append("PRIMARY KEY")
                else:
                    definition.append("PRIMARY KEY AUTO_INCREMENT")
            
            if not field.nullable:
                definition.append("NOT NULL")
            
            if field.unique:
                definition.append("UNIQUE")
            
            if field.default is not None:
                if isinstance(field.default, str):
                    definition.append(f"DEFAULT '{field.default}'")
                else:
                    definition.append(f"DEFAULT {field.default}")
            
            definitions[original_name] = " ".join(definition)
        
        return definitions

    @classmethod
    def table_name(cls):
        return cls.__table__

    @classmethod
    def from_row(cls, row):
        return cls(**row)

    def __str__(self) -> str:
        """Representación legible del modelo"""
        attributes = [f"{key}={repr(value)}" for key, value in self._data.items()]
        return f"{self.__class__.__name__}({', '.join(attributes)})"

    def __repr__(self) -> str:
        """Representación detallada del modelo"""
        return self.__str__()

class ModelDelegate:
    def __init__(self, db, model):
        self._db = db
        self._model = model

    def perform_action(self):
        # Ejemplo de método que podrías implementar
        print(f"Realizando acción en el modelo: {self._model}")