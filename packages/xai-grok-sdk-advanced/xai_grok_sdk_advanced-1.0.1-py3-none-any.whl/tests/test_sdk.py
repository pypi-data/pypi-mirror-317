import pytest
from xai_grok.sdk import XaiGrokSDK

@pytest.fixture
def sdk():
    return XaiGrokSDK(api_key="test_api_key", base_url="https://api.test.x.ai/v1")

def test_list_models(sdk, requests_mock):
    requests_mock.get("https://api.test.x.ai/v1/models", json={"models": [{"id": "grok-2-1212"}]})
    response = sdk.list_models()
    assert response["models"][0]["id"] == "grok-2-1212"

