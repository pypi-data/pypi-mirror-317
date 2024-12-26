import requests
from xai_grok.utils import RateLimiter, Cache

class XaiGrokSDK:
    """
    Advanced SDK for xAI Grok API.
    """

    def __init__(self, api_key, base_url="https://api.x.ai/v1", max_retries=3, rate_limit=10):
        """
        Initialize the SDK with API key, base URL, and advanced features.

        Args:
            api_key (str): Your xAI API key.
            base_url (str): Base URL for the xAI API.
            max_retries (int): Number of retries for failed requests.
            rate_limit (int): Maximum requests per second.
        """
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
        """
        Internal request handler with caching, retry logic, and rate-limiting.
        """
        self.rate_limiter.wait()
        cache_key = self.cache.generate_key(method, endpoint, payload)
        cached_response = self.cache.get(cache_key)

        if cached_response:
            return cached_response

        url = f"{self.base_url}{endpoint}"
        for attempt in range(self.max_retries):
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    json=payload,
                    stream=stream,
                )
                if response.status_code == 200:
                    if not stream:
                        self.cache.set(cache_key, response.json())
                        return response.json()
                    return response
                elif response.status_code >= 400:
                    raise Exception(f"API Error {response.status_code}: {response.text}")
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
        raise Exception(f"Request failed after {self.max_retries} retries.")

    def chat_completion(self, model, messages, stream=False):
        """
        Generate a chat completion.

        Args:
            model (str): Model name (e.g., "grok-2-1212").
            messages (list): Conversation messages.
            stream (bool): Enable streaming responses.

        Returns:
            dict or generator: Chat completion or stream.
        """
        payload = {"model": model, "messages": messages, "stream": stream}
        response = self._request("POST", "/chat/completions", payload, stream)
        return response if not stream else self._stream_response(response)

    def embeddings(self, model, inputs):
        """
        Generate embeddings for the provided inputs.

        Args:
            model (str): Model name for embeddings (e.g., "v1").
            inputs (list): Input texts.

        Returns:
            dict: Embedding response.
        """
        payload = {"model": model, "input": inputs}
        return self._request("POST", "/embeddings", payload)

    def list_models(self):
        """
        Retrieve a list of available models.

        Returns:
            dict: List of available models.
        """
        return self._request("GET", "/models")

    def _stream_response(self, response):
        """
        Handle streaming responses.

        Args:
            response (requests.Response): Streaming response object.

        Yields:
            str: Streamed chunks of data.
        """
        for line in response.iter_lines():
            if line:
                yield line.decode("utf-8")
