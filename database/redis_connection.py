import redis

redis_client = redis.Redis(
    host="redis",
    port=6379,
    socket_timeout=1,
    socket_connect_timeout=1,
    decode_responses=True
)


# retry limit
async def get_cached(key):

    for attempt in range(2):

        try:
            return redis_client.get(key)
        except Exception as e:
            if attempt == 1:
                return None
