from typing import Dict, List, Optional
from .schema import Field, FieldType
from .connector import Connector

class DatabaseIntrospector:
    def __init__(self, connector: 'Connector'):
        self.connector = connector

    async def get_schema_info(self, database: str, schema: str = None) -> Dict[str, Dict]:
        if self.connector.driver_type == 'postgresql':
            return await self._get_postgres_schema(schema)
        else:
            return await self._get_mysql_schema(database)

    async def _get_postgres_schema(self, schema: str) -> Dict[str, Dict]:
        query = """
        SELECT 
            t.table_name,
            c.column_name,
            c.data_type,
            c.character_maximum_length,
            c.is_nullable,
            c.column_default,
            tc.constraint_type,
            ccu.table_name as referenced_table_name,
            ccu.column_name as referenced_column_name
        FROM information_schema.tables t
        JOIN information_schema.columns c 
            ON t.table_name = c.table_name 
            AND t.table_schema = c.table_schema
        LEFT JOIN information_schema.key_column_usage kcu
            ON t.table_name = kcu.table_name 
            AND c.column_name = kcu.column_name
            AND t.table_schema = kcu.table_schema
        LEFT JOIN information_schema.table_constraints tc
            ON kcu.constraint_name = tc.constraint_name
            AND kcu.table_schema = tc.table_schema
        LEFT JOIN information_schema.constraint_column_usage ccu
            ON tc.constraint_name = ccu.constraint_name
            AND tc.table_schema = ccu.table_schema
        WHERE t.table_schema = $1
            AND t.table_type = 'BASE TABLE'
        ORDER BY t.table_name, c.ordinal_position;
        """
        results = await self.connector._fetch(query, (schema,))
        return self._process_schema_results(results)

    async def _get_mysql_schema(self, database: str) -> Dict[str, Dict]:
        query = """
        SELECT 
            TABLE_NAME as table_name,
            COLUMN_NAME as column_name,
            DATA_TYPE as data_type,
            CHARACTER_MAXIMUM_LENGTH as character_maximum_length,
            IS_NULLABLE as is_nullable,
            COLUMN_DEFAULT as column_default,
            COLUMN_KEY as column_key,
            REFERENCED_TABLE_NAME as referenced_table_name,
            REFERENCED_COLUMN_NAME as referenced_column_name
        FROM information_schema.COLUMNS
        LEFT JOIN information_schema.KEY_COLUMN_USAGE USING(TABLE_NAME, COLUMN_NAME)
        WHERE TABLE_SCHEMA = %s
        ORDER BY TABLE_NAME, ORDINAL_POSITION
        """
        results = await self.connector._fetch(query, (database,))
        return self._process_schema_results(results)

    def _process_schema_results(self, results: List[Dict]) -> Dict[str, Dict]:
        schema_info = {}
        
        for row in results:
            # Obtener nombres originales
            table_name = row['table_name']
            column_name = row['column_name']
            
            # Crear nombres seguros para Prisma (reemplazar guiones por guiones bajos)
            safe_table_name = table_name.replace('-', '_')
            safe_column_name = column_name.replace('-', '_')
            
            if safe_table_name not in schema_info:
                schema_info[safe_table_name] = {
                    'fields': {},
                    'original_name': table_name,  # Guardar nombre original
                    'mapping': {}  # Mapeo de nombres de columnas
                }
            
            # Guardar mapeo de columnas si el nombre cambió
            if safe_column_name != column_name:
                schema_info[safe_table_name]['mapping'][safe_column_name] = column_name
            
            field = self._map_database_field(row)
            schema_info[safe_table_name]['fields'][safe_column_name] = field
            
        return schema_info

    def _map_database_field(self, field_info: Dict) -> Field:
        type_mapping = {
            # PostgreSQL types
            'integer': FieldType.INTEGER,
            'bigint': FieldType.BIGINT,
            'smallint': FieldType.INTEGER,
            'character varying': FieldType.VARCHAR,
            'varchar': FieldType.VARCHAR,
            'text': FieldType.TEXT,
            'boolean': FieldType.BOOLEAN,
            'timestamp': FieldType.TIMESTAMP,
            'timestamp without time zone': FieldType.TIMESTAMP,
            'timestamp with time zone': FieldType.TIMESTAMP,
            'date': FieldType.TIMESTAMP,
            'time': FieldType.TIMESTAMP,
            'double precision': FieldType.FLOAT,
            'real': FieldType.FLOAT,
            'numeric': FieldType.DECIMAL,
            'decimal': FieldType.DECIMAL,
            'jsonb': FieldType.JSON,
            'json': FieldType.JSON,
            'uuid': FieldType.UUID,
            'bytea': FieldType.TEXT,
            'interval': FieldType.TEXT,
            'citext': FieldType.TEXT,
            # MySQL types
            'int': FieldType.INTEGER,
            'tinyint': FieldType.BOOLEAN,
            'smallint': FieldType.INTEGER,
            'mediumint': FieldType.INTEGER,
            'bigint': FieldType.BIGINT,
            'float': FieldType.FLOAT,
            'double': FieldType.FLOAT,
            'decimal': FieldType.DECIMAL,
            'datetime': FieldType.TIMESTAMP,
            'timestamp': FieldType.TIMESTAMP,
            'date': FieldType.TIMESTAMP,
            'time': FieldType.TIMESTAMP,
            'year': FieldType.INTEGER,
            'char': FieldType.VARCHAR,
            'varchar': FieldType.VARCHAR,
            'tinytext': FieldType.TEXT,
            'text': FieldType.TEXT,
            'mediumtext': FieldType.TEXT,
            'longtext': FieldType.TEXT,
            'json': FieldType.JSON,
            'binary': FieldType.TEXT,
            'varbinary': FieldType.TEXT,
            'blob': FieldType.TEXT,
            'enum': FieldType.VARCHAR,
            'set': FieldType.VARCHAR
        }

        field_type = type_mapping.get(field_info['data_type'].lower(), FieldType.TEXT)
        
        is_primary = False
        if self.connector.driver_type == 'postgresql':
            is_primary = field_info.get('constraint_type') == 'PRIMARY KEY'
        else:
            is_primary = field_info.get('column_key') == 'PRI'

        return Field(
            field_type=field_type,
            primary_key=is_primary,
            nullable=field_info['is_nullable'].upper() == 'YES',
            length=field_info.get('character_maximum_length'),
            foreign_key=f"{field_info.get('referenced_table_name')}.{field_info.get('referenced_column_name')}" 
            if field_info.get('referenced_table_name') else None,
            default=field_info.get('column_default')
        ) 