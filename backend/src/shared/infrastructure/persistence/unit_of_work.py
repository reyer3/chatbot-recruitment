from abc import ABC, abstractmethod
from typing import AsyncContextManager
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWork(ABC):
    """Abstract base class for unit of work pattern"""
    
    @abstractmethod
    async def begin(self) -> None:
        """Begin a new transaction"""
        pass
    
    @abstractmethod
    async def commit(self) -> None:
        """Commit the current transaction"""
        pass
    
    @abstractmethod
    async def rollback(self) -> None:
        """Rollback the current transaction"""
        pass
    
    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup any resources"""
        pass
    
    @abstractmethod
    def __aenter__(self) -> 'UnitOfWork':
        """Enter the async context"""
        pass
    
    @abstractmethod
    def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the async context"""
        pass


class SqlAlchemyUnitOfWork(UnitOfWork):
    """SQLAlchemy implementation of unit of work pattern"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.transaction = None
    
    async def begin(self) -> None:
        """Begin a new transaction"""
        self.transaction = await self.session.begin()
    
    async def commit(self) -> None:
        """Commit the current transaction"""
        try:
            await self.session.commit()
        except:
            await self.rollback()
            raise
    
    async def rollback(self) -> None:
        """Rollback the current transaction"""
        await self.session.rollback()
    
    async def cleanup(self) -> None:
        """Cleanup the session"""
        await self.session.close()
    
    async def __aenter__(self) -> 'SqlAlchemyUnitOfWork':
        """Enter the async context"""
        await self.begin()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the async context"""
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        await self.cleanup()


@asynccontextmanager
async def transaction_context(uow: UnitOfWork) -> AsyncContextManager[UnitOfWork]:
    """Context manager for handling transactions"""
    try:
        await uow.begin()
        yield uow
        await uow.commit()
    except Exception:
        await uow.rollback()
        raise
    finally:
        await uow.cleanup()
