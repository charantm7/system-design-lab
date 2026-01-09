import redis
from rq import Queue

redis_client = redis.Redis(
    host="redis",
    port=6379,
    db=0,
    socket_timeout=1,
    socket_connect_timeout=1,
    decode_responses=True
)

queue = Queue("default", connection=redis_client)

# retry limit


async def get_cached(key):

    for attempt in range(2):

        try:
            return redis_client.get(key)
        except Exception:
            if attempt == 1:
                return None


async def set_cache(key, value, ttl=6000):

    try:
        redis_client.setex(key, ttl, value=value)
    except Exception:
        pass
