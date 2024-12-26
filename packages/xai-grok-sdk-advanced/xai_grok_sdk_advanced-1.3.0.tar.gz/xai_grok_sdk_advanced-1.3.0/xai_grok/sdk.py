import requests
import logging
import time
from xai_grok.utils import RateLimiter, Cache

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("XaiGrokSDK")


class XaiGrokSDK:
    def __init__(self, api_key, base_url="https://api.x.ai/v1", max_retries=3, rate_limit=10):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        self.max_retries = max_retries
        self.rate_limiter = RateLimiter(rate=rate_limit)
        self.cache = Cache()

    def _request(self, method, endpoint, payload=None, stream=False):
        self.rate_limiter.wait()
        cache_key = self.cache.generate_key(method, endpoint, payload)
        cached_response = self.cache.get(cache_key)

        if cached_response:
            return cached_response

        url = f"{self.base_url}{endpoint}"
        last_exception = None  # To track the last exception for final raise
        for attempt in range(self.max_retries):
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    json=payload,
                    stream=stream,
                )
                if response.status_code == 429:  # Rate limit exceeded
                    retry_after = int(response.headers.get("Retry-After", "1"))
                    logger.info("Rate limit reached. Retrying after %s seconds...", retry_after)
                    time.sleep(retry_after)
                    last_exception = Exception("Rate limit reached")
                    continue
                elif response.status_code == 401:
                    logger.error("Invalid API key encountered.")
                    raise Exception("Invalid API key.")
                elif response.status_code >= 500:
                    logger.error("Server error occurred with status code: %s", response.status_code)
                    raise Exception(f"Server error: {response.status_code}")
                elif response.status_code >= 400:
                    logger.error("Client error occurred with status code: %s", response.status_code)
                    raise Exception(f"Client error: {response.status_code}")
                else:
                    if not stream:
                        self.cache.set(cache_key, response.json())
                        self._handle_rate_limit(response.headers)
                        return response.json()
                    return response
            except Exception as e:
                logger.warning("Attempt %d failed: %s", attempt + 1, e)
                last_exception = e
        # If all retries fail, raise the last captured exception
        raise last_exception or Exception(f"Request failed after {self.max_retries} retries.")

    def _handle_rate_limit(self, headers):
        remaining = headers.get("X-RateLimit-Remaining")
        if remaining is not None and int(remaining) <= 5:
            logger.warning("Warning: Rate limit is approaching.")

    def list_models(self):
        return self._request("GET", "/models")

    def chat_completion(self, model, messages, stream=False):
        payload = {"model": model, "messages": messages, "stream": stream}
        return self._request("POST", "/chat/completions", payload, stream)

    def embeddings(self, model, inputs):
        payload = {"model": model, "input": inputs}
        return self._request("POST", "/embeddings", payload)
