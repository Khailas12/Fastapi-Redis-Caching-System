import redis.asyncio as redis
from config.redis import redis_client  

class RedisService:
    async def get_item(self, item_id: int):
        return await redis_client.get(f"item_{item_id}")

    async def set_item(self, item_id: int, data: str, expiration: int = 3600):
        await redis_client.setex(f"item_{item_id}", expiration, data)

    async def delete_item(self, item_id: int):
        await redis_client.delete(f"item_{item_id}")