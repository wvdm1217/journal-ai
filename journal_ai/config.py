import os
from dataclasses import dataclass


@dataclass
class Config:
    openai_api_key: str
    model: str = "gpt-4-turbo-preview"
    embedding_model: str = "text-embedding-3-small"

    @classmethod
    def from_env(cls) -> "Config":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")

        return cls(
            openai_api_key=api_key,
            model=os.getenv("OPENAI_CHAT_MODEL"),
            embedding_model=os.getenv("OPENAI_EMBEDDING_MODEL"),
        )
