from fastapi import APIRouter, HTTPException
from services.redis_basic.v2.cache_response import cache_response
from config.redis import redis_client  

router = APIRouter()

users_db = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com", "age": 25},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com", "age": 30},
    3: {"id": 3, "name": "Charlie", "email": "charlie@example.com", "age": 22},
}

@router.get("/users/{user_id}")
@cache_response(ttl=120, namespace="users")
async def get_user_details(user_id: int):
    # Simulate a database call by retrieving data from users_db
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    # del users_db[user_id]
    cache_key = f"users:user:{user_id}"
    await redis_client.delete(cache_key)
    return {"message": "User cache removed successfully"}
