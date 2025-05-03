from unittest.mock import patch

from journal_ai.journal.models import JournalEntry
from journal_ai.storage import JsonStorage


@patch("journal_ai.journal.models.generate_title", return_value="Mock Title")
def test_save_and_load_entry(mock_generate_title, storage: JsonStorage):
    entry_id = "1"
    content = "Test content"
    entry = JournalEntry.create(content=content, entry_id=entry_id)
    storage.save_entry(entry)

    loaded_entry = storage.load_entry(entry_id)
    assert loaded_entry is not None
    assert loaded_entry.content == content
    assert loaded_entry.id == entry_id


@patch("journal_ai.journal.models.generate_title", return_value="Mock Title")
def test_load_all_entries(mock_generate_title, storage: JsonStorage):
    entries = {"1": "First entry", "2": "Second entry", "3": "Third entry"}

    for entry_id, content in entries.items():
        entry = JournalEntry.create(content=content, entry_id=entry_id)
        storage.save_entry(entry)

    loaded_entries = storage.load_all()
    assert len(loaded_entries) == len(entries)
    for entry_id, content in entries.items():
        assert entry_id in loaded_entries
        assert loaded_entries[entry_id].content == content


@patch("journal_ai.journal.models.generate_title", return_value="Mock Title")
def test_delete_entry(mock_generate_title, storage: JsonStorage):
    entry_id = "1"
    content = "Test content"
    entry = JournalEntry.create(content=content, entry_id=entry_id)
    storage.save_entry(entry)

    assert storage.delete_entry(entry_id) is True
    assert storage.load_entry(entry_id) is None
    assert storage.delete_entry("non-existent") is False


@patch("journal_ai.journal.models.generate_title", return_value="Mock Title")
def test_purge(mock_generate_title, storage: JsonStorage):
    for i in range(3):
        entry = JournalEntry.create(content=f"Content {i}", entry_id=str(i))
        storage.save_entry(entry)

    assert len(storage.load_all()) == 3

    storage.purge()
    assert len(storage.load_all()) == 0
