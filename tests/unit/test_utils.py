from unittest.mock import Mock, patch

import pytest

from journal_ai.utils import Tags, generate_tags, generate_title


@pytest.fixture
def mock_openai_response():
    mock_response = Mock()
    mock_response.choices = [Mock(message=Mock(content="Generated Title"))]
    return mock_response


@pytest.fixture
def mock_openai_tags_response():
    mock_response = Mock()
    mock_choice = Mock()
    mock_message = Mock()
    mock_message.parsed = Tags(tags=["journal", "writing", "test"])
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
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


@patch("journal_ai.utils.OpenAI")
def test_generate_tags(mock_openai_class, mock_openai_tags_response, mock_config):
    mock_client = Mock()
    mock_client.beta.chat.completions.parse.return_value = mock_openai_tags_response
    mock_openai_class.return_value = mock_client

    content = "This is a test journal entry"
    tags = generate_tags(content, mock_config)

    assert tags == ["journal", "writing", "test"]
    mock_client.beta.chat.completions.parse.assert_called_once()


@patch("journal_ai.utils.OpenAI")
def test_generate_tags_error(mock_openai_class, mock_config):
    mock_client = Mock()
    mock_client.beta.chat.completions.parse.side_effect = Exception("API Error")
    mock_openai_class.return_value = mock_client

    content = "This is a test journal entry"
    tags = generate_tags(content, mock_config)

    assert tags == []
    mock_client.beta.chat.completions.parse.assert_called_once()


@patch("journal_ai.utils.OpenAI")
def test_generate_tags_no_api_key(mock_openai_class, mock_config):
    mock_config.openai_api_key = None

    content = "This is a test journal entry"
    tags = generate_tags(content, mock_config)

    assert tags == []
    mock_openai_class.assert_not_called()
