from typing import Dict, Type, Optional, List, Any
from .connector import Connector
from .client import PrismaLikeClient
from .model import Model
from .introspector import DatabaseIntrospector
from .model_generator import ModelGenerator
from .query_builder import QueryBuilder
from .cache.factory import CacheFactory
from .logger import configure_logging
import os
import json
from datetime import timedelta

class GroovinDB:
    def __init__(self, connections: Dict[str, Dict[str, Any]] = None):
        self.connectors = {}
        self.models = {}
        
        if connections is None:
            connections = self._load_config()
            
        if not connections:
            raise ValueError("No se encontró configuración de base de datos")
        
        # Configurar logging
        debug_config = connections.get('debug', {'level': 'INFO'})
        configure_logging(debug_config)
        
        # Configurar caché
        cache_config = connections.get('cache', {'type': 'memory', 'ttl': 300})
        self.cache = CacheFactory.create(cache_config)
        self.cache_ttl = timedelta(seconds=cache_config.get('ttl', 300))
        
        # Configurar conexiones
        supported_drivers = {'postgresql', 'mysql'}  # Lista de drivers soportados
        connection_params = ['user', 'password', 'database', 'host', 'port', 'schema']  # Parámetros válidos
        
        for driver, config in connections.items():
            if driver in supported_drivers:
                # Filtrar solo los parámetros válidos para el Connector
                filtered_config = {k: v for k, v in config.items() if k in connection_params}
                self.connectors[driver] = Connector(driver=driver, **filtered_config)
        
        self.client = None

    def _load_config(self) -> Dict[str, Dict[str, Any]]:
        if os.path.exists("groovindb.json"):
            with open("groovindb.json", "r") as f:
                return json.load(f)
        return {}

    async def connect(self):
        for driver, connector in self.connectors.items():
            await connector.connect()
            await self._introspect_database(driver, connector)
            
        await self.cache.start()
        self.client = PrismaLikeClient(self)

    async def disconnect(self):
        for connector in self.connectors.values():
            await connector.disconnect()
        await self.cache.stop()

    async def _introspect_database(self, driver: str, connector: 'Connector'):
        introspector = DatabaseIntrospector(connector)
        generator = ModelGenerator(driver, schema=connector.schema)
        
        schema_info = await introspector.get_schema_info(
            database=connector.database,
            schema=connector.schema
        )
        
        for table_name, table_info in schema_info.items():
            model_class = generator.generate_model_class(table_name, table_info)
            self.models[table_name] = model_class

    @property
    def available_models(self) -> List[str]:
        return list(self.models.keys())

    def get_model(self, name: str) -> Optional[Type[Model]]:
        return self.models.get(name)

    def _get_connector_for_model(self, model_class: Type[Model]) -> Connector:
        """Obtiene el connector correcto para el modelo basado en su configuración"""
        return self.connectors[model_class.__config__.driver]

    async def find(self, model_class: Type[Model], query_builder: QueryBuilder) -> List[Dict[str, Any]]:
        """Encuentra múltiples registros que coincidan con los criterios"""
        connector = self._get_connector_for_model(model_class)
        query = query_builder.build_select_query(
            model_class.__config__.schema,
            model_class.__table__
        )
        return await connector._fetch(query, tuple(query_builder.params))

    async def find_one(self, model_class: Type[Model], query_builder: QueryBuilder) -> Optional[Dict[str, Any]]:
        """Encuentra un único registro que coincida con los criterios"""
        connector = self._get_connector_for_model(model_class)
        query = query_builder.build_select_query(
            model_class.__config__.schema,
            model_class.__table__,
            limit=1
        )
        result = await connector._fetch_one(query, tuple(query_builder.params))
        return result

    async def create(self, model_class: Type[Model], data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo registro"""
        connector = self._get_connector_for_model(model_class)
        query = QueryBuilder().build_insert_query(
            model_class.__config__.schema,
            model_class.__table__,
            data
        )
        await connector._execute(query, tuple(data.values()))
        return data

    async def update(self, model_class: Type[Model], where: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """Actualiza registros existentes"""
        connector = self._get_connector_for_model(model_class)
        query = QueryBuilder().build_update_query(
            model_class.__config__.schema,
            model_class.__table__,
            where,
            data
        )
        params = tuple(list(data.values()) + list(where.values()))
        await connector._execute(query, params)
        return data

    async def delete(self, model_class: Type[Model], where: Dict[str, Any]) -> Dict[str, Any]:
        """Elimina registros"""
        connector = self._get_connector_for_model(model_class)
        query = QueryBuilder().build_delete_query(
            model_class.__config__.schema,
            model_class.__table__,
            where
        )
        await connector._execute(query, tuple(where.values()))
        return where

    async def load_relations(self, records: List[Dict[str, Any]], relations: List[str]) -> None:
        """Carga las relaciones para los registros dados"""
        # TODO: Implementar carga de relaciones
        pass

    # ... (resto del código)
