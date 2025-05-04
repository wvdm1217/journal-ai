from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

import numpy as np

from journal_ai.config import Config
from journal_ai.utils import generate_tags, generate_title


@dataclass
class JournalEntry:
    """Class representing a journal entry."""

    content: str
    created_at: datetime
    updated_at: datetime
    id: Optional[str] = None
    title: Optional[str] = None
    tags: Optional[List[str]] = None
    word_count: int = 0
    embedding: Optional[np.ndarray] = None

    def __post_init__(self):
        if not self.word_count:
            self.word_count = len(self.content.split())

    @classmethod
    def create(
        cls,
        content: str,
        entry_id: Optional[str] = None,
        title: Optional[str] = None,
        config: Optional[Config] = None,
        created_at=None,
        updated_at=None,
        tags: Optional[List[str]] = None,
        **kwargs,
    ):
        """Factory method to create a new journal entry"""
        now = datetime.now()
        created_time = created_at or now
        updated_time = updated_at or now

        generated_title = title
        if not generated_title and config:
            generated_title = generate_title(content, config)

        if not tags and config:
            tags = generate_tags(content, config)
        else:
            tags = tags or []

        return cls(
            content=content,
            created_at=created_time,
            updated_at=updated_time,
            id=entry_id,
            title=generated_title,
            tags=tags,
            **kwargs,
        )

    def to_dict(self):
        return {
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "id": self.id,
            "title": self.title,
            "tags": self.tags or [],
            "word_count": self.word_count or len(self.content.split()),
            "embedding": self.embedding.tolist() if self.embedding is not None else [],
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            content=data["content"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            id=data.get("id"),
            title=data.get("title"),
            tags=data.get("tags", []),
            word_count=data.get("word_count", 0),
            embedding=data.get("embedding", []),
        )
