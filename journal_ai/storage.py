import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from journal_ai.config import Config
from journal_ai.models import JournalEntry
from journal_ai.utils import generate_title


class JsonStorage:
    def __init__(self, directory: str = "data", config: Optional[Config] = None):
        self.directory = Path(directory)
        self.entry_directory = self.directory / "entries"
        self.config = config
        self._ensure_data_directory()

    def _ensure_data_directory(self):
        self.directory.mkdir(parents=True, exist_ok=True)
        self.entry_directory.mkdir(parents=True, exist_ok=True)

    def _get_entry_path(self, entry_id: str) -> Path:
        return self.entry_directory / f"{entry_id}.json"

    def get_vector_db_path(self) -> Path:
        return self.directory / "vector.index"

    def load_entry(self, entry_id: str) -> Optional[JournalEntry]:
        try:
            with open(self._get_entry_path(entry_id), "r") as f:
                data = json.load(f)
                data["id"] = entry_id
                return JournalEntry.from_dict(data)
        except FileNotFoundError:
            return None

    def load_all(self) -> Dict[str, JournalEntry]:
        entries = {}
        for file_path in self.entry_directory.glob("*.json"):
            entry_id = file_path.stem
            with open(file_path, "r") as f:
                data = json.load(f)
                data["id"] = entry_id
                entries[entry_id] = JournalEntry.from_dict(data)
        return entries

    def save_entry(
        self,
        entry_id: str,
        content: str,
        existing_entry: Optional[JournalEntry] = None,
        title: Optional[str] = None,
    ):
        now = datetime.now()
        if existing_entry:
            entry = JournalEntry(
                content=content,
                created_at=existing_entry.created_at,
                updated_at=now,
                id=entry_id,
                title=title or existing_entry.title,
                tags=existing_entry.tags,
                embedding=existing_entry.embedding,
            )
        else:
            generated_title = title or generate_title(content, self.config)
            entry = JournalEntry(
                content=content,
                created_at=now,
                updated_at=now,
                id=entry_id,
                title=generated_title,
            )

        with open(self._get_entry_path(entry_id), "w") as f:
            json.dump(entry.to_dict(), f, indent=2)

    def delete_entry(self, entry_id: str) -> bool:
        try:
            self._get_entry_path(entry_id).unlink()
            return True
        except FileNotFoundError:
            return False

    def purge(self):
        # Delete all entry files
        for file_path in self.entry_directory.glob("*.json"):
            file_path.unlink()

        # Delete vector index if it exists
        vector_db_path = self.get_vector_db_path()
        if vector_db_path.exists():
            vector_db_path.unlink()
