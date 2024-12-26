import time

class RateLimiter:
    def __init__(self, rate: float):
        """
        Initialize rate limiter.
        Args:
            rate (float): Maximum number of requests per second.
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

