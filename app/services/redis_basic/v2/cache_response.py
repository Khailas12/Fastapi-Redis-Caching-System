import json
from functools import wraps
from fastapi import HTTPException
from config.redis import redis_client
import redis.asyncio as redis

def cache_response(ttl: int = 60, namespace: str = "main"):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user_id = kwargs.get("user_id") or (args[0] if args else None)
            cache_key = f"{namespace}:user:{user_id}"
            print("cache_key12", cache_key)

            try:
                # Check cache
                cached_value = await redis_client.get(cache_key)
                if cached_value:
                    print("cached_value==", cached_value)
                    cached_data = json.loads(cached_value)
                    cached_data["cache"] = True
                    return cached_data
                
                response = await func(*args, **kwargs)
                
                response["cache"] = False
                await redis_client.set(cache_key, json.dumps(response), ex=ttl)
                
                return response
                
            except redis.RedisError as e:
                print(f"Redis error: {e}")
                return await func(*args, **kwargs)
            except Exception as e:
                import traceback; traceback.print_exc()
                raise HTTPException(status_code=500, detail=f"Caching error: {e}")
                
        return wrapper
    return decorator
