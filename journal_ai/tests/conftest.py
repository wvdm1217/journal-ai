import tempfile
from unittest.mock import patch

import pytest

from journal_ai.config import Config
from journal_ai.storage import JsonStorage


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname


@pytest.fixture
def mock_config():
    return Config(
        openai_api_key="test-key",
        model="test-model",
        embedding_model="test-embedding-model",
    )


@pytest.fixture
def storage(temp_dir, mock_config):
    return JsonStorage(directory=temp_dir, config=mock_config)


@pytest.fixture
def storage_with_entries(temp_dir, mock_config):
    storage = JsonStorage(directory=temp_dir, config=mock_config)
    with patch("journal_ai.storage.generate_title", return_value="Mock Title"):
        for i in range(3):
            storage.save_entry(str(i), f"Content {i}")
    return storage
