"""
GroovinDB - ORM asíncrono con interfaz similar a Prisma
"""

from .src.main import GroovinDB
from .src.schema import Field, FieldType
from .src.model import Model, ModelConfig

__version__ = "0.1.8"
__all__ = ['GroovinDB', 'Field', 'FieldType', 'Model', 'ModelConfig'] 