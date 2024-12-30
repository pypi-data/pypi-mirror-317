"""
Redis cache implementation for AgenticFleet
"""

from typing import Any, Optional, Union
import json
from redis.asyncio import Redis
from datetime import timedelta

from ..config import get_settings


class RedisCache:
    """Redis cache implementation"""

    def __init__(self):
        """Initialize Redis cache"""
        self.settings = get_settings()
        self._redis: Optional[Redis] = None

    async def initialize(self) -> None:
        """Initialize Redis connection"""
        if not self._redis:
            self._redis = Redis.from_url(
                self.settings.redis_url or "redis://localhost:6379/0"
            )

    async def close(self) -> None:
        """Close Redis connection"""
        if self._redis:
            await self._redis.close()
            self._redis = None

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache

        Args:
            key: Cache key

        Returns:
            Cached value if found, None otherwise
        """
        await self.initialize()
        value = await self._redis.get(key)
        if value:
            return json.loads(value)
        return None

    async def set(
        self,
        key: str,
        value: Any,
        expire: Optional[Union[int, timedelta]] = None
    ) -> None:
        """Set value in cache

        Args:
            key: Cache key
            value: Value to cache
            expire: Optional expiration time in seconds or timedelta
        """
        await self.initialize()
        await self._redis.set(
            key,
            json.dumps(value),
            ex=int(expire.total_seconds()) if isinstance(expire, timedelta) else expire
        )

    async def delete(self, key: str) -> None:
        """Delete value from cache

        Args:
            key: Cache key
        """
        await self.initialize()
        await self._redis.delete(key)

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache

        Args:
            key: Cache key

        Returns:
            True if key exists, False otherwise
        """
        await self.initialize()
        return await self._redis.exists(key) > 0

    async def clear(self) -> None:
        """Clear all cache entries"""
        await self.initialize()
        await self._redis.flushdb()


# Global cache instance
_cache: Optional[RedisCache] = None


def get_cache() -> RedisCache:
    """Get global cache instance

    Returns:
        Redis cache instance
    """
    global _cache
    if _cache is None:
        _cache = RedisCache()
    return _cache 