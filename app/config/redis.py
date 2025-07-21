import redis.asyncio as redis

# Connection pool improves performance by reusing existing connections rather than creating new ones for each request
redis_pool = redis.ConnectionPool(host='redis', port=6379, db=0, decode_responses=True)
redis_client = redis.Redis(connection_pool=redis_pool)