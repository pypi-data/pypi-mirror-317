from pathlib import Path
from typing import Dict, Any, Optional, Set, TYPE_CHECKING
import json
from .client import Client
from .constants import DEFAULT_CONFIG
from ..drivers import get_driver
from ..utils.introspector import DatabaseIntrospector
from ..utils.logger import logger

if TYPE_CHECKING:
    from db_types import GeneratedClient

class GroovinDB:
    def __init__(self, config_file: str = "groovindb.json"):
        # Cargar y validar configuración
        try:
            with open(config_file) as f:
                self.config = {**DEFAULT_CONFIG, **json.load(f)}
        except FileNotFoundError:
            logger.error(f"Archivo de configuración no encontrado: {config_file}")
            raise
        
        # Inicializar componentes
        self.driver = get_driver(self.config.get('driver', 'postgresql'))()
        self.tables: Set[str] = set()
        self.schema_info: Dict[str, Any] = {}
        if TYPE_CHECKING:
            self.client: GeneratedClient
        else:
            self.client = Client(self)
        self._connected = False

    async def connect(self):
        if self._connected:
            return

        try:
            # Construir DSN y conectar
            dsn = f"{self.config['driver']}://{self.config['user']}:{self.config['password']}@{self.config['host']}:{self.config['port']}/{self.config['database']}"
            await self.driver.connect(dsn)
            self._connected = True
            
            # Obtener información del esquema
            introspector = DatabaseIntrospector(self.driver)
            self.schema_info = await introspector.get_schema_info(self.config['schema'])
            self.tables = set(self.schema_info.keys())
            
            logger.info(f"Conectado a {self.config['database']} - {len(self.tables)} tablas encontradas")
        
        except Exception as e:
            logger.error(f"Error al conectar: {e}")
            raise

    async def disconnect(self):
        if self._connected:
            await self.driver.close()
            self._connected = False
            logger.info("Desconectado de la base de datos")

    async def introspect(self):
        """Genera tipos basados en la estructura de la base de datos"""
        if not self._connected:
            await self.connect()

        try:
            code = """from typing import Dict, Any, Optional, List, TypeVar
from groovindb.core.client import Table, Client
from groovindb.types import (
    FindFirstOptions, FindManyOptions, CreateOptions,
    UpdateOptions, UpsertOptions, DeleteOptions,
    WhereInput, OrderByInput, SelectInput
)

"""
            # Generar tipos para cada tabla
            for table_name, info in self.schema_info.items():
                # Crear tipo para la tabla
                code += f"class {table_name.title()}Type:\n"
                for field, field_info in info['fields'].items():
                    code += f"    {field}: {self._map_db_type(field_info['type'])}\n"
                code += "\n"

            # Generar cliente con tipos
            code += "class GeneratedClient(Client):\n"
            for table_name, info in self.schema_info.items():
                code += f"    {table_name}: Table[{table_name.title()}Type]  # campos: {list(info['fields'].keys())}\n"

            Path("db_types.py").write_text(code)
            logger.info("Tipos generados en db_types.py")

            # Recargar el módulo generado
            import importlib.util
            spec = importlib.util.spec_from_file_location("db_types", "db_types.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Actualizar la anotación de tipo del cliente
            if TYPE_CHECKING:
                self.client: GeneratedClient = module.GeneratedClient(self)
            else:
                self.client = module.GeneratedClient(self)
            
        except Exception as e:
            logger.error(f"Error al generar tipos: {e}")
            raise

    def _map_db_type(self, db_type: str) -> str:
        """Mapea tipos de base de datos a tipos de Python"""
        type_map = {
            'integer': 'int',
            'bigint': 'int',
            'character varying': 'str',
            'text': 'str',
            'boolean': 'bool',
            'timestamp': 'datetime',
            'numeric': 'float',
            'json': 'Dict[str, Any]',
            'jsonb': 'Dict[str, Any]',
        }
        return type_map.get(db_type.lower(), 'Any')