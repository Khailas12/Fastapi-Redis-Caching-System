from fastapi import FastAPI
from services.redis_basic.v1.router import router as redis_router_v1
from services.redis_basic.v2.router import router as redis_router_v2

app = FastAPI()

app.include_router(redis_router_v1, prefix="/redis-v1", tags=["Redis"])
app.include_router(redis_router_v2, prefix="/redis-v2", tags=["Redis V2"])

@app.get("/health") 
async def health_check():
    return {"status": "healthy"}