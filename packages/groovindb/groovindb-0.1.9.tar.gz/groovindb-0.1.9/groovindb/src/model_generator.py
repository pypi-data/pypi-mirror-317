from typing import Dict, Type, Any
from .model import Model, ModelConfig
from .schema import Field

class ModelGenerator:
    def __init__(self, driver: str, schema: str = 'public'):
        self.driver = driver
        self.schema = schema

    def generate_model_class(self, table_name: str, table_info: Dict) -> Type[Model]:
        """
        Genera una clase de modelo con soporte para nombres con guiones
        """
        original_name = table_info.get('original_name', table_name)
        column_mapping = table_info.get('mapping', {})
        
        class Meta:
            table = original_name  # Nombre real en la base de datos
            column_map = column_mapping  # Mapeo de nombres de columnas
            config = ModelConfig(
                driver=self.driver,
                schema=self.schema  # Usar el esquema pasado al constructor
            )
        
        attrs = {
            '__table__': original_name,
            '__column_map__': column_mapping,
            '__fields__': table_info['fields'],
            '__config__': Meta.config,
            'Meta': Meta
        }
        
        # Crear la clase del modelo
        model_class = type(table_name, (Model,), attrs)
        
        return model_class

    def _generate_field_property(self, field_name: str, field: Field):
        """Genera una propiedad para acceder a un campo del modelo"""
        def getter(self):
            return self._data.get(field_name)
            
        def setter(self, value):
            self._data[field_name] = value
            
        return property(getter, setter)