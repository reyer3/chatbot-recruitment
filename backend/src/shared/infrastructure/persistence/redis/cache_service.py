from typing import Optional, Any, TypeVar, Generic, Callable, Awaitable
from datetime import timedelta
import json
import hashlib

from .redis_client import RedisClient

T = TypeVar('T')


class CacheService(Generic[T]):
    """Service for handling caching operations"""
    
    def __init__(self, redis_client: RedisClient, prefix: str = "cache"):
        self._redis = redis_client
        self._prefix = prefix
    
    def _build_key(self, key: str) -> str:
        """Build a prefixed cache key"""
        return f"{self._prefix}:{key}"
    
    def _generate_key(self, *args, **kwargs) -> str:
        """Generate a cache key from arguments"""
        # Convert args and kwargs to a string representation
        key_parts = [str(arg) for arg in args]
        key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
        key_str = ":".join(key_parts)
        
        # Create a hash of the key string
        return hashlib.sha256(key_str.encode()).hexdigest()
    
    async def get(self, key: str) -> Optional[T]:
        """Get a value from cache"""
        return await self._redis.get(self._build_key(key))
    
    async def set(
        self,
        key: str,
        value: T,
        expire: Optional[timedelta] = None
    ) -> None:
        """Set a value in cache with optional expiration"""
        await self._redis.set(
            self._build_key(key),
            value,
            expire_seconds=int(expire.total_seconds()) if expire else None
        )
    
    async def delete(self, key: str) -> None:
        """Delete a value from cache"""
        await self._redis.delete(self._build_key(key))
    
    async def exists(self, key: str) -> bool:
        """Check if a key exists in cache"""
        return await self._redis.exists(self._build_key(key))
    
    async def cached(
        self,
        func: Callable[..., Awaitable[T]],
        expire: Optional[timedelta] = None,
        *args,
        **kwargs
    ) -> T:
        """Decorator for caching function results"""
        cache_key = self._generate_key(*args, **kwargs)
        
        # Try to get from cache first
        cached_value = await self.get(cache_key)
        if cached_value is not None:
            return cached_value
        
        # If not in cache, execute function
        result = await func(*args, **kwargs)
        
        # Store in cache if we have a result
        if result is not None:
            await self.set(cache_key, result, expire)
        
        return result
