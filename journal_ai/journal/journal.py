from typing import Dict, Optional

from journal_ai.config import Config
from journal_ai.journal.models import JournalEntry
from journal_ai.rag import RAGQuerier
from journal_ai.storage import JsonStorage


class JournalManager:
    """Manages journal entries, including creation, viewing, searching, editing,
    and deletion."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config.from_env()
        self.storage = JsonStorage(config=self.config)
        self.rag = RAGQuerier(self.config)

    def create_entry(self, content: str) -> str:
        entries = self.storage.load_all()
        entry_id = str(len(entries) + 1)
        entry = JournalEntry.create(content=content, entry_id=entry_id)
        self.storage.save_entry(entry)
        return entry_id

    def view_entries(self) -> Dict[str, JournalEntry]:
        return self.storage.load_all()

    def search_entries(self, keyword: str) -> Dict[str, JournalEntry]:
        entries = self.storage.load_all()
        return {
            entry_id: entry
            for entry_id, entry in entries.items()
            if keyword.lower() in entry.content.lower()
        }

    def edit_entry(self, entry_id: str, content: str) -> bool:
        existing_entry = self.storage.load_entry(entry_id)
        if existing_entry is not None:
            existing_entry.content = content
            self.storage.save_entry(existing_entry)
            return True
        return False

    def delete_entry(self, entry_id: str) -> bool:
        return self.storage.delete_entry(entry_id)

    def purge(self):
        self.storage.purge()

    def query(self, question: str) -> str:
        entries = self.storage.load_all()
        if not entries:
            return "No journal entries found to query."

        self.rag.index_entries(entries)
        return self.rag.query(question)
