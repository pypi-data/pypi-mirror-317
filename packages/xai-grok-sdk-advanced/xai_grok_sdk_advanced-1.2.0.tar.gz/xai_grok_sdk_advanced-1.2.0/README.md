### Rate-Limit Monitoring

The SDK provides unlimited API calls but will warn users when nearing the provider's rate limit. Example:

```python
sdk = XaiGrokSDK(api_key="your-api-key")

# Make a request
response = sdk._request("GET", "/models")

# Check rate limit analytics
sdk.analytics()

# Example Output
# Warning: 3/100 API requests remaining. Rate limit resets at 1700000000.
# Total API calls made this session: 5


### Usage Examples

#### Retrieve Analytics
```python
sdk.analytics()
# Output:
# Total API requests: 10
# Cache hits: 2
# Retry attempts: 1
