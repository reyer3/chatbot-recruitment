from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import DeclarativeMeta
from ....domain.aggregate import AggregateRoot
from ..repository import Repository

Model = TypeVar('Model', bound=DeclarativeMeta)
Entity = TypeVar('Entity', bound=AggregateRoot)

class SQLAlchemyRepository(Repository[Entity], Generic[Entity, Model]):
    def __init__(self, session: AsyncSession, model_class: Type[Model], entity_class: Type[Entity]):
        self._session = session
        self._model_class = model_class
        self._entity_class = entity_class

    async def save(self, aggregate: Entity) -> None:
        model = self._to_model(aggregate)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)

    async def search_by_id(self, id: str) -> Optional[Entity]:
        result = await self._session.execute(
            select(self._model_class).where(self._model_class.id == id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def search_all(self) -> List[Entity]:
        result = await self._session.execute(select(self._model_class))
        return [self._to_entity(model) for model in result.scalars().all()]

    async def delete(self, id: str) -> None:
        await self._session.execute(
            delete(self._model_class).where(self._model_class.id == id)
        )
        await self._session.commit()

    def _to_model(self, entity: Entity) -> Model:
        """Convert domain entity to SQLAlchemy model"""
        raise NotImplementedError

    def _to_entity(self, model: Model) -> Entity:
        """Convert SQLAlchemy model to domain entity"""
        raise NotImplementedError
