import json
from pathlib import Path
from typing import Dict, Optional

from journal_ai.config import Config
from journal_ai.journal.models import JournalEntry


class JsonStorage:
    def __init__(self, directory: str = "data", config: Optional[Config] = None):
        self.directory = Path(directory)
        self.entry_directory = self.directory / "entries"
        self.config = config
        self._ensure_data_directory()

    def _ensure_data_directory(self):
        self.directory.mkdir(parents=True, exist_ok=True)
        self.entry_directory.mkdir(parents=True, exist_ok=True)

    def _get_entry_path(self, id: str) -> Path:
        return self.entry_directory / f"{id}.json"

    def get_vector_db_path(self) -> Path:
        return self.directory / "vector.index"

    def load_entry(self, id: str) -> Optional[JournalEntry]:
        try:
            with open(self._get_entry_path(id), "r") as f:
                data = json.load(f)
                data["id"] = id
                return JournalEntry.from_dict(data)
        except FileNotFoundError:
            return None

    def load_all(self) -> Dict[str, JournalEntry]:
        entries = {}
        for file_path in self.entry_directory.glob("*.json"):
            id = file_path.stem
            with open(file_path, "r") as f:
                data = json.load(f)
                data["id"] = id
                entries[id] = JournalEntry.from_dict(data)
        return entries

    def save_entry(
        self,
        entry: JournalEntry,
    ):
        if entry.id is None:
            entry.id = str(len(self.load_all()) + 1)

        with open(self._get_entry_path(entry.id), "w") as f:
            json.dump(entry.to_dict(), f, indent=2)

    def delete_entry(self, id: str) -> bool:
        try:
            self._get_entry_path(id).unlink()
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
