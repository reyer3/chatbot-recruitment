from typing import Optional, Any
import json
from redis.asyncio import Redis, ConnectionPool
from ...config import Config


class RedisClient:
    """Redis client wrapper for caching and session management"""
    
    def __init__(self, config: Config):
        self._pool = ConnectionPool(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=config.REDIS_DB,
            password=config.REDIS_PASSWORD,
            decode_responses=True
        )
        self._redis: Optional[Redis] = None
    
    async def connect(self) -> None:
        """Connect to Redis"""
        if not self._redis:
            self._redis = Redis(connection_pool=self._pool)
    
    async def disconnect(self) -> None:
        """Disconnect from Redis"""
        if self._redis:
            await self._redis.close()
            self._redis = None
    
    async def get(self, key: str) -> Optional[Any]:
        """Get a value from Redis"""
        if not self._redis:
            await self.connect()
        
        value = await self._redis.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None
    
    async def set(
        self,
        key: str,
        value: Any,
        expire_seconds: Optional[int] = None
    ) -> None:
        """Set a value in Redis with optional expiration"""
        if not self._redis:
            await self.connect()
        
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        
        if expire_seconds:
            await self._redis.setex(key, expire_seconds, value)
        else:
            await self._redis.set(key, value)
    
    async def delete(self, key: str) -> None:
        """Delete a key from Redis"""
        if not self._redis:
            await self.connect()
        
        await self._redis.delete(key)
    
    async def exists(self, key: str) -> bool:
        """Check if a key exists in Redis"""
        if not self._redis:
            await self.connect()
        
        return await self._redis.exists(key) > 0
