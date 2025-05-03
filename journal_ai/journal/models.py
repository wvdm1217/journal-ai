from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

import numpy as np


@dataclass
class JournalEntry:
    content: str
    created_at: datetime
    updated_at: datetime
    id: Optional[str] = None
    title: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    word_count: int = 0
    embedding: Optional[np.ndarray] = field(default_factory=lambda: np.array([]))

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
