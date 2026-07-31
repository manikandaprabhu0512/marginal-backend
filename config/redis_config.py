import os

import redis

redis_config = redis.Redis.from_url(os.environ["REDIS_URL"])
