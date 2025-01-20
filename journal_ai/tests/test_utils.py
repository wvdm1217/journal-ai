from unittest.mock import Mock, patch

import pytest

from journal_ai.utils import generate_title


@pytest.fixture
def mock_openai_response():
    mock_response = Mock()
    mock_response.choices = [Mock(message=Mock(content="Generated Title"))]
    return mock_response


@patch("journal_ai.utils.OpenAI")
def test_generate_title(mock_openai_class, mock_openai_response, mock_config):
    mock_client = Mock()
    mock_client.chat.completions.create.return_value = mock_openai_response
    mock_openai_class.return_value = mock_client

    content = "This is a test journal entry"
    title = generate_title(content, mock_config)

    assert title == "Generated Title"
    mock_client.chat.completions.create.assert_called_once()


@patch("journal_ai.utils.OpenAI")
def test_generate_title_error(mock_openai_class, mock_config):
    mock_client = Mock()
    mock_client.chat.completions.create.side_effect = Exception("API Error")
    mock_openai_class.return_value = mock_client

    content = "This is a test journal entry"
    title = generate_title(content, mock_config)

    assert title == "Untitled Entry"
    mock_client.chat.completions.create.assert_called_once()
