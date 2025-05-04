from datetime import datetime

from journal_ai.journal.models import JournalEntry


def test_journal_entry_creation():
    now = datetime.now()
    entry = JournalEntry(
        content="Test content",
        created_at=now,
        updated_at=now,
        id="1",
        title="Test Title",
        tags=["test", "sample"],
        word_count=2,
        embedding=[0.1, 0.2, 0.3],
    )

    assert entry.content == "Test content"
    assert entry.created_at == now
    assert entry.id == "1"
    assert entry.title == "Test Title"
    assert entry.tags == ["test", "sample"]
    assert entry.word_count == 2
    assert entry.embedding == [0.1, 0.2, 0.3]


def test_journal_entry_to_dict():
    now = datetime.now()
    entry = JournalEntry(
        content="Test content",
        created_at=now,
        updated_at=now,
        id="1",
        title="Test Title",
    )

    entry_dict = entry.to_dict()
    assert entry_dict["content"] == "Test content"
    assert entry_dict["created_at"] == now.isoformat()
    assert entry_dict["id"] == "1"
    assert entry_dict["title"] == "Test Title"
    assert isinstance(entry_dict["tags"], list)
    assert isinstance(entry_dict["embedding"], list)


def test_journal_entry_from_dict():
    data = {
        "content": "Test content",
        "created_at": "2024-01-01T12:00:00",
        "updated_at": "2024-01-01T12:00:00",
        "id": "1",
        "title": "Test Title",
        "tags": ["test"],
        "word_count": 2,
        "embedding": [0.1, 0.2],
    }

    entry = JournalEntry.from_dict(data)
    assert entry.content == data["content"]
    assert entry.id == data["id"]
    assert entry.title == data["title"]
    assert entry.tags == data["tags"]
    assert entry.word_count == data["word_count"]
    assert entry.embedding == data["embedding"]
