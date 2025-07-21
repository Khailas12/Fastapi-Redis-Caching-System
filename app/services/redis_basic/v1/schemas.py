from pydantic import BaseModel

class ItemResponse(BaseModel):
    item_id: int
    cached: bool
    data: str

class DeleteResponse(BaseModel):
    status: str