from typing import Type
from .base import BaseDriver
from .postgresql import PostgreSQLDriver
from .mysql import MySQLDriver

DRIVERS = {
    'postgresql': PostgreSQLDriver,
    'mysql': MySQLDriver
}

def get_driver(name: str) -> Type[BaseDriver]:
    return DRIVERS[name] 