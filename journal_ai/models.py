from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class JournalEntry:
    content: str
    created_at: datetime
    updated_at: datetime
    id: Optional[str] = None
    title: Optional[str] = None
    tags: list[str] = None
    word_count: int = 0

    def to_dict(self):
        return {
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "id": self.id,
            "title": self.title,
            "tags": self.tags or [],
            "word_count": self.word_count or len(self.content.split())
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
            word_count=data.get("word_count", 0)
        )
