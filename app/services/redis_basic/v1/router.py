from fastapi import APIRouter

from services.redis_basic.v1.schemas import ItemResponse, DeleteResponse
from services.redis_basic.v1.service import RedisService

router = APIRouter()
redis_service = RedisService()

@router.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int):
    cached_item = await redis_service.get_item(item_id)
    
    if cached_item:
        return {"item_id": item_id, "cached": True, "data": cached_item}
    
    item_data = f"Item data for {item_id}"
    
    await redis_service.set_item(item_id, item_data)
    
    return {"item_id": item_id, "cached": False, "data": item_data}


@router.delete("/delete/{item_id}", response_model=DeleteResponse)
async def delete_item(item_id: int):
    await redis_service.delete_item(item_id)
    return {"status": "cache cleared"}
