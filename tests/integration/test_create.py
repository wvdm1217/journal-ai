import json
import tempfile

import pytest
from click.testing import CliRunner

from journal_ai.journal.journal import JournalManager
from journal_ai.main import cli
from journal_ai.storage import JsonStorage


@pytest.fixture
def cli_runner() -> CliRunner:
    """Fixture providing a CliRunner to test the command line app."""
    return CliRunner()


def test_create_journal_entry(cli_runner: CliRunner):
    """Test the full end-to-end flow of creating a journal entry."""

    content = "Test journal entry content"

    with tempfile.TemporaryDirectory() as temp_dir:
        storage = JsonStorage(directory=temp_dir)
        journal = JournalManager(storage=storage)
        result = cli_runner.invoke(
            cli,
            ["create"],
            input=content,
            obj={"journal": journal},
        )

        with open(temp_dir + "/entries/1.json", "r") as f:
            file_contents = f.read()
            data = json.loads(file_contents)
            assert data["content"] == content
            assert data["id"] == "1"

        assert result.exit_code == 0
