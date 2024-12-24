"""
GroovinDB - ORM asíncrono con interfaz similar a Prisma
"""

from .main import GroovinDB
from .schema import Field, FieldType
from .model import Model, ModelConfig

__version__ = "0.1.1"
__all__ = ['GroovinDB', 'Field', 'FieldType', 'Model', 'ModelConfig']

