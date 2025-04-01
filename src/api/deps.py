import redis.asyncio as aioredis
from redis.asyncio import Redis

from fastapi.security import HTTPBearer


from src.core.config import settings


# async def get_redis_client() -> Redis:
#     redis = await aioredis.from_url(
#         f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
#         password=settings.REDIS_PASSWORD,
#         max_connections=10,
#         encoding="utf8",
#         decode_responses=True,
#         db=1
#     )
#     return redis


bearer_security = HTTPBearer()
