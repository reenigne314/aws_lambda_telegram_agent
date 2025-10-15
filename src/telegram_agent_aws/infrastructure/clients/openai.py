from functools import lru_cache

from openai import OpenAI

from telegram_agent_aws.config import settings


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    """
    Get or create the OpenAI client singleton.
    The client is created once and cached for subsequent calls.
    """
    return OpenAI(api_key=settings.OPENAI_API_KEY)
