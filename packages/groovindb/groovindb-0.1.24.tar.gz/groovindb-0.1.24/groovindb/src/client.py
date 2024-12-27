from typing import TypeVar, Type, List, Dict, Any, Optional
from .query_builder import QueryBuilder
from .model import Model

T = TypeVar('T', bound='Model')

class PrismaLikeClient:
    def __init__(self, db: 'GroovinDB'):
        self._db = db
        self._models = {}
        self._delegates = {}
        
        # Inicializar delegados para cada modelo
        for model_name in db.available_models:
            model = db.get_model(model_name)
            if model:
                delegate = ModelDelegate(db, model)
                self._delegates[model_name] = delegate
                # Establecer el atributo directamente para autocompletado
                setattr(self, model_name, delegate)

    def __getattr__(self, name: str) -> 'ModelDelegate':
        if name in self._delegates:
            return self._delegates[name]
        raise AttributeError(f"Model '{name}' not found. Available models: {list(self._delegates.keys())}")

    async def query(self, sql: str, params: tuple = None) -> List[Dict[str, Any]]:
        """
        Ejecuta una query SQL raw directamente en la base de datos.
        
        Args:
            sql: Query SQL a ejecutar
            params: Parámetros para la query (opcional)
            
        Returns:
            Lista de registros como diccionarios
        """
        # Usar el primer connector disponible
        connector = next(iter(self._db.connectors.values()))
        return await connector._fetch(sql, params or ())

    async def execute(self, sql: str, params: tuple = None) -> None:
        """
        Ejecuta una query SQL raw que no retorna resultados (INSERT, UPDATE, DELETE, etc)
        
        Args:
            sql: Query SQL a ejecutar
            params: Parámetros para la query (opcional)
        """
        connector = next(iter(self._db.connectors.values()))
        await connector._execute(sql, params or ())

class ModelDelegate:
    """Delegado para operaciones de modelo."""
    
    def __init__(self, db: 'GroovinDB', model: Type[T]):
        self._db = db
        self._model = model

    async def findMany(self, 
                      where: Optional[Dict[str, Any]] = None,
                      select: Optional[Dict[str, bool]] = None,
                      include: Optional[Dict[str, bool]] = None,
                      orderBy: Optional[List[Dict[str, str]]] = None,
                      skip: Optional[int] = None,
                      take: Optional[int] = None) -> List[Dict[str, Any]]:
        query_builder = QueryBuilder()
        
        if where:
            for key, value in where.items():
                query_builder.where(**{key: value})
                
        if select:
            query_builder.select(*select.keys())
            
        if orderBy:
            for order in orderBy:
                for field, direction in order.items():
                    query_builder.order_by(f"{field} {direction}")
                    
        if skip:
            query_builder.offset(skip)
            
        if take:
            query_builder.limit(take)

        return await self._db.find(self._model, query_builder)

    async def findFirst(self,
                       where: Optional[Dict[str, Any]] = None,
                       select: Optional[Dict[str, bool]] = None,
                       include: Optional[Dict[str, bool]] = None) -> Optional[Dict[str, Any]]:
        query_builder = QueryBuilder()
        
        if where:
            for key, value in where.items():
                query_builder.where(**{key: value})
        if select:
            query_builder.select(*select.keys())
        query_builder.limit(1)
        
        return await self._db.find_one(self._model, query_builder)

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._db.create(self._model, data)

    async def update(self, where: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._db.update(self._model, where, data)

    async def delete(self, where: Dict[str, Any]) -> Dict[str, Any]:
        return await self._db.delete(self._model, where)

    async def upsert(self, where: Dict[str, Any], create: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
        existing = await self.findFirst(where=where)
        if existing:
            return await self.update(where, update)
        return await self.create(create)