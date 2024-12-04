from typing import Generic, TypeVar, Optional, List, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ....domain.repositories import Repository
from ....domain.entities import Entity
from ....domain.value_objects import EntityId

T = TypeVar('T', bound=Entity)
M = TypeVar('M')

class SQLAlchemyRepository(Repository[T], Generic[T, M]):
    """Base SQLAlchemy repository implementation"""

    def __init__(self, session: AsyncSession, model_class: Type[M], entity_class: Type[T]):
        self._session = session
        self._model_class = model_class
        self._entity_class = entity_class

    async def save(self, entity: T) -> None:
        model = self._to_model(entity)
        self._session.add(model)
        await self._session.commit()

    async def get_by_id(self, entity_id: EntityId) -> Optional[T]:
        result = await self._session.execute(
            select(self._model_class).where(self._model_class.id == str(entity_id))
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def update(self, entity: T) -> None:
        result = await self._session.execute(
            select(self._model_class).where(self._model_class.id == str(entity.id))
        )
        model = result.scalar_one_or_none()
        if model:
            for key, value in self._to_model(entity).__dict__.items():
                if not key.startswith('_'):
                    setattr(model, key, value)
        await self._session.commit()

    async def delete(self, entity_id: EntityId) -> None:
        result = await self._session.execute(
            select(self._model_class).where(self._model_class.id == str(entity_id))
        )
        model = result.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.commit()

    async def list_all(self) -> List[T]:
        result = await self._session.execute(select(self._model_class))
        return [self._to_entity(model) for model in result.scalars().all()]

    def _to_model(self, entity: T) -> M:
        """Convert domain entity to SQLAlchemy model"""
        raise NotImplementedError

    def _to_entity(self, model: M) -> T:
        """Convert SQLAlchemy model to domain entity"""
        raise NotImplementedError
