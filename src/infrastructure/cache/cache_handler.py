import pickle

from redis import asyncio as aioredis

from infrastructure.settings.config import base_config


class CacheService:
    def __init__(self):
        self.redis_pool = aioredis.ConnectionPool.from_url(base_config.redis_url)
        self.cacher = aioredis.Redis(connection_pool=self.redis_pool)

    async def create_cache(self, key, value):
        await self.cacher.set(key, pickle.dumps(value), ex=base_config.EXPIRATION)

    async def read_cache(self, key):
        return await self.cacher.get(key)

    async def update_cache(self, key, value):
        await self.cacher.set(key, pickle.dumps(value), ex=base_config.EXPIRATION)

    async def delete_cache(self, key):
        await self.cacher.delete(key)
