from unittest.mock import patch


@patch("journal_ai.storage.generate_title", return_value="Mock Title")
def test_save_and_load_entry(mock_generate_title, storage):
    entry_id = "1"
    content = "Test content"
    storage.save_entry(entry_id, content)

    loaded_entry = storage.load_entry(entry_id)
    assert loaded_entry is not None
    assert loaded_entry.content == content
    assert loaded_entry.id == entry_id


@patch("journal_ai.storage.generate_title", return_value="Mock Title")
def test_load_all_entries(mock_generate_title, storage):
    entries = {"1": "First entry", "2": "Second entry", "3": "Third entry"}

    for entry_id, content in entries.items():
        storage.save_entry(entry_id, content)

    loaded_entries = storage.load_all()
    assert len(loaded_entries) == len(entries)
    for entry_id, content in entries.items():
        assert entry_id in loaded_entries
        assert loaded_entries[entry_id].content == content


@patch("journal_ai.storage.generate_title", return_value="Mock Title")
def test_delete_entry(mock_generate_title, storage):
    entry_id = "1"
    content = "Test content"
    storage.save_entry(entry_id, content)

    assert storage.delete_entry(entry_id) is True
    assert storage.load_entry(entry_id) is None
    assert storage.delete_entry("non-existent") is False


@patch("journal_ai.storage.generate_title", return_value="Mock Title")
def test_purge(mock_generate_title, storage):
    for i in range(3):
        storage.save_entry(str(i), f"Content {i}")

    storage.purge()
    assert len(storage.load_all()) == 0
