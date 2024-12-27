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
from pathlib import Path

class GroovinDB:
    def __init__(self, connections: Dict[str, Dict[str, Any]] = None, config_path: str = None):
        self.connectors = {}
        self.models = {}

        if connections is None:
            connections = self._load_config(config_path)

        if not connections:
            raise ValueError(
                "No se encontró configuración de base de datos. "
                "Debes proporcionar la configuración directamente, mediante un archivo groovindb.json "
                "en la raíz del proyecto, o especificar la ruta con config_path"
            )

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

        # Cargar configuración de stubs
        self.stubs_location = connections.get('stubs', {}).get('location', 'stubs')
        
        # Asegurarse de que el directorio de stubs exista
        stubs_dir = Path(self.stubs_location)
        if not stubs_dir.exists():
            stubs_dir.mkdir(parents=True, exist_ok=True)
            (stubs_dir / '__init__.py').touch()

    def _load_config(self, config_path: str = None) -> Dict[str, Dict[str, Any]]:
        """
        Cargar configuración desde archivo
        
        Args:
            config_path: Ruta explícita al archivo de configuración
        """
        # Obtener el directorio de trabajo actual y el directorio raíz del proyecto
        current_dir = os.getcwd()
        project_root = self._find_project_root(current_dir)
        
        paths_to_try = []
        
        # 1. Intentar ruta explícita si se proporciona
        if config_path:
            if not os.path.isabs(config_path):
                config_path = os.path.join(project_root, config_path)
            paths_to_try.append(Path(config_path))
        
        # 2. Intentar en el directorio raíz del proyecto
        paths_to_try.append(Path(project_root) / "groovindb.json")
        
        # Debug: Imprimir las rutas que estamos probando
        for path in paths_to_try:
            print(f"Buscando configuración en: {path}")
            if path.is_file():
                try:
                    with open(path) as f:
                        config = json.load(f)
                        print(f"✅ Configuración cargada desde: {path}")
                        return config
                except json.JSONDecodeError as e:
                    print(f"❌ Error al cargar {path}: {e}")
                    continue
            else:
                print(f"❌ No se encontró el archivo: {path}")
                    
        return {}

    def _find_project_root(self, start_path: str) -> str:
        """
        Encuentra el directorio raíz del proyecto buscando hacia arriba hasta encontrar
        ciertos archivos indicadores o llegar a la raíz del sistema.
        
        Args:
            start_path: Directorio desde donde comenzar la búsqueda
            
        Returns:
            str: Ruta al directorio raíz del proyecto
        """
        current = Path(start_path)
        
        # Archivos que indican la raíz de un proyecto
        project_indicators = [
            "setup.py",
            "pyproject.toml",
            "requirements.txt",
            ".git",
            ".env",
            "manage.py"  # Para proyectos Django
        ]
        
        # Buscar hacia arriba hasta encontrar un indicador o llegar a la raíz
        while current != current.parent:
            # Verificar si algún indicador está presente
            for indicator in project_indicators:
                if (current / indicator).exists():
                    return str(current)
                
            # Si encontramos un archivo groovindb.json, asumimos que es la raíz
            if (current / "groovindb.json").exists():
                return str(current)
            
            # Subir un nivel
            current = current.parent
        
        # Si no encontramos ningún indicador, usar el directorio actual
        return start_path

    async def connect(self):
        """Conecta a la base de datos y configura el cliente"""
        try:
            # Conectar a las bases de datos
            for driver, connector in self.connectors.items():
                await connector.connect()
                await self._introspect_database(driver, connector)

            # Iniciar caché
            await self.cache.start()
            
            # Generar stubs
            self._generate_client_stubs()
            
            # Crear cliente
            self.client = PrismaLikeClient(self)
            
            # Verificar que se haya inicializado correctamente
            if not self.client:
                raise RuntimeError("Failed to initialize client")
                
        except Exception as e:
            print(f"Error during connection: {e}")
            raise

    def _generate_client_stubs(self):
        """Genera los stubs del cliente con los modelos disponibles"""
        stubs_dir = Path(self.stubs_location).resolve()
        stubs_dir.mkdir(parents=True, exist_ok=True)
        
        # Generar client.pyi
        client_stub_path = stubs_dir / 'client.pyi'
        stub_content = [
            "from typing import Any, Dict, List, Optional, Union",
            "from groovindb.src.client import ModelDelegate",
            "",
            "class PrismaLikeClient:",
        ]
        
        # Agregar propiedades para cada modelo
        for model_name in sorted(self.models.keys()):
            stub_content.append(f"    {model_name}: ModelDelegate")
        
        # Escribir el archivo stub
        with open(client_stub_path, 'w') as f:
            f.write('\n'.join(stub_content))

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
        try:
            connector = self._get_connector_for_model(model_class)
            query = query_builder.build_select_query(
                model_class.__config__.schema,
                model_class.__table__
            )
            return await connector._fetch(query, tuple(query_builder.params))
        except Exception as e:
            print(f"Error en find: {e}")
            print(f"Query: {query}")
            print(f"Params: {query_builder.params}")
            raise

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

    def verify_config_location(self) -> None:
        """
        Verifica y muestra información sobre la ubicación de la configuración.
        Útil para diagnóstico.
        """
        current_dir = os.getcwd()
        project_root = self._find_project_root(current_dir)
        config_path = Path(project_root) / "groovindb.json"
        
        print("\nDiagnóstico de configuración:")
        print(f"📁 Directorio de ejecución: {current_dir}")
        print(f"📄 Directorio raíz del proyecto: {project_root}")
        print(f"📄 Archivo de configuración esperado: {config_path}")
        print(f"✓ ¿Existe el archivo?: {'Sí' if config_path.is_file() else 'No'}")
        
        if config_path.is_file():
            try:
                with open(config_path) as f:
                    config = json.load(f)
                print("✓ Archivo de configuración válido")
                print(f"🔑 Drivers configurados: {list(config.keys())}")
            except json.JSONDecodeError:
                print("❌ Error: El archivo existe pero no es un JSON válido")
        else:
            print("\n📄 Archivos en el directorio raíz:")
            for file in os.listdir(project_root):
                print(f"   - {file}")

    # ... (resto del código)
