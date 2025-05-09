import os
from dataclasses import dataclass


@dataclass
class Config:
    openai_api_key: str
    model: str = "gpt-4o"
    embedding_model: str = "text-embedding-3-large"

    @classmethod
    def from_env(cls) -> "Config":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")

        model = os.getenv("OPENAI_CHAT_MODEL") or "gpt-4o"
        embedding_model = (
            os.getenv("OPENAI_EMBEDDING_MODEL") or "text-embedding-3-large"
        )

        return cls(
            openai_api_key=api_key,
            model=model,
            embedding_model=embedding_model,
        )


def get_config() -> Config:
    """Get the configuration for the application.

    Returns:
        Config: The configuration object.
    """
    return Config.from_env()
