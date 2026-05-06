import redis

storage = redis.Redis(
    host="redis",
    port=6379,
    db=0,
    decode_responses=True,
    retry_on_timeout=True,
    health_check_interval=30
)

