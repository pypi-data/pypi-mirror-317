from typing import Dict, Any, Optional, List, Tuple, Union
from .drivers.postgresql import PostgreSQLDriver
from .drivers.mysql import MySQLDriver
from .helpers.logger import logger

class Connector:
    """
    Conector de base de datos que maneja la conexión y operaciones con diferentes motores.
    
    Attributes:
        driver_type (str): Tipo de driver ('postgresql' o 'mysql')
        database (str): Nombre de la base de datos
        schema (str): Esquema de la base de datos
    """
    
    SUPPORTED_DRIVERS = {
        'postgresql': (PostgreSQLDriver, 5432),
        'mysql': (MySQLDriver, 3306)
    }

    def __init__(
        self,
        driver: str,
        user: str,
        password: str,
        database: str,
        host: str = 'localhost',
        port: Optional[int] = None,
        schema: str = 'public'
    ):
        """
        Inicializa un nuevo conector de base de datos.
        
        Args:
            driver: Tipo de driver ('postgresql' o 'mysql')
            user: Usuario de la base de datos
            password: Contraseña del usuario
            database: Nombre de la base de datos
            host: Host de la base de datos (default: 'localhost')
            port: Puerto de la base de datos (default: None, se usa el puerto por defecto del driver)
            schema: Esquema de la base de datos (default: 'public')
            
        Raises:
            ValueError: Si el driver no está soportado
        """
        if driver not in self.SUPPORTED_DRIVERS:
            raise ValueError(f"Driver no soportado: {driver}. Drivers disponibles: {list(self.SUPPORTED_DRIVERS.keys())}")
        
        self.driver_type = driver
        self.database = database
        self.schema = schema
        
        # Inicializar driver
        driver_class, default_port = self.SUPPORTED_DRIVERS[driver]
        self._driver = driver_class()
        
        # Construir DSN
        port = port or default_port
        self._dsn = f'{driver}://{user}:{password}@{host}:{port}/{database}'

    def _escape_identifier(self, identifier: str) -> str:
        """
        Escapa un identificador (esquema, tabla, columna) para uso seguro en queries.
        
        Args:
            identifier: El identificador a escapar
            
        Returns:
            str: El identificador escapado
        """
        cleaned = identifier.strip().strip('`').strip('"')
        return f'"{cleaned}"'

    async def _handle_schema_path(self, query: str, params: Optional[Tuple] = None) -> Tuple[str, Optional[Tuple]]:
        """
        Maneja queries que contienen SET search_path, separándolas y ejecutando el cambio de esquema.
        
        Args:
            query: Query SQL a ejecutar
            params: Parámetros de la query
            
        Returns:
            Tuple[str, Optional[Tuple]]: La query principal y sus parámetros
        """
        if 'SET search_path' not in query:
            return query, params
            
        queries = [q.strip() for q in query.split(';') if q.strip()]
        search_path = next(q for q in queries if 'SET search_path' in q)
        main_query = next(q for q in queries if 'SET search_path' not in q)
        
        # Escapar el esquema y ejecutar SET search_path
        schema_name = search_path.split('TO')[-1].strip().strip('"')
        escaped_search_path = f'SET search_path TO {self._escape_identifier(schema_name)}'
        await self._driver.execute(escaped_search_path)
        
        return main_query, params

    async def connect(self) -> None:
        """
        Conecta a la base de datos y configura el esquema.
        
        Raises:
            Exception: Si hay un error al conectar o configurar el esquema
        """
        try:
            await self._driver.connect(self._dsn)
            
            if self.schema != 'public':
                # Verificar si el esquema existe
                check_schema = f"""
                    SELECT schema_name 
                    FROM information_schema.schemata 
                    WHERE schema_name = $1
                """
                schema_exists = await self._driver.fetch_one(check_schema, self.schema)
                
                if not schema_exists:
                    # Crear esquema si no existe
                    create_schema = f'CREATE SCHEMA IF NOT EXISTS {self._escape_identifier(self.schema)}'
                    await self._driver.execute(create_schema)
                    logger.info(f"Schema '{self.schema}' created")
                
                # Establecer el esquema en la búsqueda
                set_schema = f'SET search_path TO {self._escape_identifier(self.schema)}'
                await self._driver.execute(set_schema)
                logger.info(f"Search path set to schema '{self.schema}'")
                
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            raise

    async def disconnect(self) -> None:
        """Desconecta de la base de datos"""
        try:
            await self._driver.close()
        except Exception as e:
            logger.error(f"Error disconnecting from database: {e}")
            raise

    async def _execute(self, query: str, params: Optional[Tuple] = None) -> bool:
        """
        Ejecuta una consulta que no devuelve resultados.
        
        Args:
            query: Query SQL a ejecutar
            params: Parámetros de la query
            
        Returns:
            bool: True si la ejecución fue exitosa
            
        Raises:
            Exception: Si hay un error al ejecutar la query
        """
        try:
            query, params = await self._handle_schema_path(query, params)
            if params:
                return await self._driver.execute(query, *params)
            return await self._driver.execute(query)
        except Exception as e:
            logger.error(f"Error executing query: {query}\nParams: {params}\nError: {e}")
            raise

    async def _fetch(self, query: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
        """
        Ejecuta una consulta y devuelve múltiples resultados.
        
        Args:
            query: Query SQL a ejecutar
            params: Parámetros de la query
            
        Returns:
            List[Dict[str, Any]]: Lista de registros encontrados
            
        Raises:
            Exception: Si hay un error al ejecutar la query
        """
        try:
            query, params = await self._handle_schema_path(query, params)
            if params:
                return await self._driver.fetch(query, *params)
            return await self._driver.fetch(query)
        except Exception as e:
            logger.error(f"Error fetching data: {query}\nParams: {params}\nError: {e}")
            raise

    async def _fetch_one(self, query: str, params: Optional[Tuple] = None) -> Optional[Dict[str, Any]]:
        """
        Ejecuta una consulta y devuelve un único resultado.
        
        Args:
            query: Query SQL a ejecutar
            params: Parámetros de la query
            
        Returns:
            Optional[Dict[str, Any]]: El registro encontrado o None si no hay resultados
            
        Raises:
            Exception: Si hay un error al ejecutar la query
        """
        try:
            query, params = await self._handle_schema_path(query, params)
            if params:
                return await self._driver.fetch_one(query, *params)
            return await self._driver.fetch_one(query)
        except Exception as e:
            logger.error(f"Error fetching single record: {query}\nParams: {params}\nError: {e}")
            raise
