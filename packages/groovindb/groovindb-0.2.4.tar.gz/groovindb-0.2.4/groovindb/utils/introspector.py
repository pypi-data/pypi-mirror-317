from typing import Dict, Any
from ..drivers.postgresql import PostgreSQLDriver
from ..drivers.mysql import MySQLDriver
from .logger import logger

class DatabaseIntrospector:
    def __init__(self, driver):
        self.driver = driver

    async def get_schema_info(self, schema: str = 'public') -> Dict[str, Any]:
        """Obtiene información del esquema de la base de datos"""
        if isinstance(self.driver, PostgreSQLDriver):
            return await self._introspect_postgresql(schema)
        elif isinstance(self.driver, MySQLDriver):
            return await self._introspect_mysql(schema)
        else:
            raise NotImplementedError(f"Introspección no implementada para {type(self.driver)}")

    async def _introspect_postgresql(self, schema: str) -> Dict[str, Any]:
        """Introspección específica para PostgreSQL"""
        query = """
            SELECT 
                t.table_name,
                c.column_name,
                c.data_type,
                c.is_nullable,
                c.column_default
            FROM information_schema.tables t
            JOIN information_schema.columns c 
                ON t.table_name = c.table_name 
                AND t.table_schema = c.table_schema
            WHERE t.table_schema = $1 
            AND t.table_type = 'BASE TABLE'
            ORDER BY t.table_name, c.ordinal_position
        """
        
        try:
            results = await self.driver.fetch(query, schema)
            
            schema_info = {}
            for row in results:
                table_name = row['table_name']
                if table_name not in schema_info:
                    schema_info[table_name] = {'fields': {}}
                
                schema_info[table_name]['fields'][row['column_name']] = {
                    'type': row['data_type'],
                    'nullable': row['is_nullable'] == 'YES',
                    'default': row['column_default']
                }
            
            return schema_info
            
        except Exception as e:
            logger.error(f"Error en introspección PostgreSQL: {e}")
            raise

    async def _introspect_mysql(self, schema: str) -> Dict[str, Any]:
        """Introspección específica para MySQL"""
        query = """
            SELECT 
                TABLE_NAME,
                COLUMN_NAME,
                DATA_TYPE,
                IS_NULLABLE,
                COLUMN_DEFAULT
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = %s
            ORDER BY TABLE_NAME, ORDINAL_POSITION
        """
        
        try:
            results = await self.driver.fetch(query, schema)
            
            schema_info = {}
            for row in results:
                table_name = row['TABLE_NAME']
                if table_name not in schema_info:
                    schema_info[table_name] = {'fields': {}}
                
                schema_info[table_name]['fields'][row['COLUMN_NAME']] = {
                    'type': row['DATA_TYPE'],
                    'nullable': row['IS_NULLABLE'] == 'YES',
                    'default': row['COLUMN_DEFAULT']
                }
            
            return schema_info
            
        except Exception as e:
            logger.error(f"Error en introspección MySQL: {e}")
            raise 