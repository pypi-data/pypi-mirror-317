import os
import pytest
from at_common_functions.utils.openai import OpenAISettings, init_openai, get_openai, OpenAIService

@pytest.fixture
def openai_settings(required_env_vars):
    return OpenAISettings(
        organization=required_env_vars["OPENAI_ORG_ID"],
        api_key=required_env_vars["OPENAI_API_KEY"],
        proxy=os.getenv("OPENAI_PROXY_URL", "")
    )

@pytest.fixture
def reset_openai_service():
    OpenAIService._instance = None
    OpenAIService._is_initialized = False
    yield

@pytest.mark.asyncio
async def test_openai_service_initialization(openai_settings, reset_openai_service):
    # Test initialization
    service = init_openai(openai_settings)
    assert service._is_initialized
    assert service == get_openai()

@pytest.mark.asyncio
async def test_openai_chat(openai_settings, reset_openai_service):
    service = init_openai(openai_settings)
    
    response = await service.chat(
        system="You are a helpful AI assistant",
        user="Say 'Hello, World!'",
        model="gpt-3.5-turbo",
        temperature=0.0,
        max_tokens=100
    )
    print(response)
    assert isinstance(response, str)
    assert len(response) > 0