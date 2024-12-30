import logging
from openai import AsyncOpenAI
import httpx
from dataclasses import dataclass
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

@dataclass
class OpenAISettings:
    organization: str
    api_key: str
    proxy: str

class OpenAIService:
    _instance = None
    _is_initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def init(self, settings: OpenAISettings):
        if not self._is_initialized:
            if settings.proxy == "":
                self._client = AsyncOpenAI(
                    api_key=settings.api_key,
                    organization=settings.organization
                )
            else:
                self._client = AsyncOpenAI(
                    api_key=settings.api_key,
                    organization=settings.organization,
                    http_client=httpx.AsyncClient(proxy=settings.proxy)
                )
            self._is_initialized = True

    # @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def chat(self, system: str, user: str, model: str, temperature: float = 0.0, max_tokens: int = 8192):
        logger.warning(f"Chatting with OpenAI model: {model}")
        logger.warning(f"System: {system}")
        logger.warning(f"User: {user}")
        response = await self._client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
        
# Global instance
_openai_service = OpenAIService()

def init_openai(settings: OpenAISettings) -> OpenAIService:
    _openai_service.init(settings)
    return _openai_service

def get_openai() -> OpenAIService:
    if not _openai_service._is_initialized:
        raise RuntimeError("OpenAI service not initialized. Call init_openai first.")
    return _openai_service