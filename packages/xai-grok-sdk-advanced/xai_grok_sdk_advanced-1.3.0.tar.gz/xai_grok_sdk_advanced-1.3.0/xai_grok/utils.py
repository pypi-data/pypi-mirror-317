import time
import hashlib
import json
from functools import lru_cache

class RateLimiter:
    def __init__(self, rate: float):
        """
        Initialize rate limiter.

        Args:
            rate (float): Requests per second.
        """
        self.rate = rate
        self.last_request = None

    def wait(self):
        """
        Wait for the next available request slot.
        """
        if self.last_request:
            elapsed = time.time() - self.last_request
            wait_time = max(0, (1 / self.rate) - elapsed)
            time.sleep(wait_time)
        self.last_request = time.time()

class Cache:
    def __init__(self):
        """
        Initialize a simple cache.
        """
        self.data = {}

    def generate_key(self, method, endpoint, payload):
        """
        Generate a unique cache key based on request data.
        """
        key = f"{method}:{endpoint}:{json.dumps(payload, sort_keys=True)}"
        return hashlib.md5(key.encode()).hexdigest()

    def get(self, key):
        """
        Get data from the cache.
        """
        return self.data.get(key)

    def set(self, key, value):
        """
        Store data in the cache.
        """
        self.data[key] = value
