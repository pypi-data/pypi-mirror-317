from typing import TypeVar, Type, List, Dict, Any, Optional
from .query_builder import QueryBuilder
from .model import Model

T = TypeVar('T', bound='Model')

try:
    from .stubs.client import PrismaLikeClient as PrismaLikeClientStub
    class PrismaLikeClient(PrismaLikeClientStub):
        pass
except ImportError:
    class PrismaLikeClient:
        def __init__(self, db: 'GroovinDB'):
            self._db = db
            self._models = {}
            # Crear atributos dinámicamente para cada modelo
            for model_name in db.available_models:
                setattr(self.__class__, model_name, property(
                    lambda self, name=model_name: self._get_model_delegate(name)
                ))

        def _get_model_delegate(self, name: str) -> 'ModelDelegate':
            """Obtiene o crea un ModelDelegate para el modelo dado"""
            if name not in self._models:
                model = self._db.get_model(name)
                if model is None:
                    raise AttributeError(f"Model '{name}' not found")
                self._models[name] = ModelDelegate(self._db, model)
            return self._models[name]

        def __getattr__(self, name: str) -> 'ModelDelegate':
            """Fallback para modelos que no existen como propiedades"""
            return self._get_model_delegate(name)

        def __dir__(self) -> List[str]:
            """Soporte para autocompletado"""
            return list(self._db.available_models)

class ModelDelegate:
    def __init__(self, db: 'GroovinDB', model: Type[T]):
        self._db = db
        self._model = model
        self._query_builder = QueryBuilder()

    def __dir__(self) -> List[str]:
        """Soporte para autocompletado de métodos"""
        return ['findMany', 'findFirst', 'create', 'update', 'delete', 'upsert']

    async def findMany(self, 
                      where: Dict = None,
                      select: Dict = None,
                      include: Dict = None,
                      orderBy: List[Dict] = None,
                      skip: int = None,
                      take: int = None) -> List[Dict]:
        try:
            if where:
                self._query_builder.where(**where)
            if select:
                self._query_builder.select(*select.keys())
            if orderBy:
                for order in orderBy:
                    for field, direction in order.items():
                        self._query_builder.order_by(f"{field} {direction}")
            if skip:
                self._query_builder.offset(skip)
            if take:
                self._query_builder.limit(take)

            results = await self._db.find(self._model, self._query_builder)
            
            if include:
                for relation, value in include.items():
                    if value:
                        await self._db.load_relations(results, [relation])

            return results
        finally:
            self._query_builder.reset()

    async def findFirst(self,
                       where: Dict = None,
                       select: Dict = None,
                       include: Dict = None) -> Optional[Dict]:
        try:
            if where:
                self._query_builder.where(**where)
            if select:
                self._query_builder.select(*select.keys())
            self._query_builder.limit(1)
            
            result = await self._db.find_one(self._model, self._query_builder)
            
            if result and include:
                for relation, value in include.items():
                    if value:
                        await self._db.load_relations([result], [relation])
                        
            return result
        finally:
            self._query_builder.reset()

    async def create(self, data: Dict) -> Dict:
        return await self._db.create(self._model, data)

    async def update(self, where: Dict, data: Dict) -> Dict:
        return await self._db.update(self._model, where, data)

    async def delete(self, where: Dict) -> Dict:
        return await self._db.delete(self._model, where)

    async def upsert(self, where: Dict, create: Dict, update: Dict) -> Dict:
        existing = await self.findFirst(where=where)
        if existing:
            return await self.update(where, update)
        return await self.create(create)