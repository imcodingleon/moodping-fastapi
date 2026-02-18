import asyncio
import logging
import google.generativeai as genai
from .base import BaseLLMClient
from app.config import get_settings

logger = logging.getLogger(__name__)


class GeminiClient(BaseLLMClient):
    """gemini-2.5-flash 기반 Google Gemini 클라이언트."""

    def __init__(self):
        settings = get_settings()
        genai.configure(api_key=settings.gemini_api_key)
        self._model = genai.GenerativeModel(
            model_name=settings.gemini_model,
            system_instruction=None,  # system_prompt는 complete()에서 주입
            generation_config=genai.GenerationConfig(
                max_output_tokens=settings.llm_max_tokens,
                temperature=settings.llm_temperature,
            ),
        )
        self._timeout = settings.llm_timeout_seconds

    async def complete(self, system_prompt: str, user_prompt: str) -> str | None:
        combined_prompt = f"{system_prompt}\n\n{user_prompt}"
        try:
            response = await asyncio.wait_for(
                asyncio.to_thread(self._model.generate_content, combined_prompt),
                timeout=self._timeout,
            )
            return response.text
        except asyncio.TimeoutError:
            logger.error("Gemini 호출 타임아웃 (%.1fs)", self._timeout)
            return None
        except Exception as e:
            logger.error("Gemini 호출 실패: %s", e)
            return None
