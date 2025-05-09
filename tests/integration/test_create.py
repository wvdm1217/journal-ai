import json
import os
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

        temp_file_path = os.path.join(temp_dir, "entries", "1.json")

        with open(temp_file_path, "r") as f:
            file_contents = f.read()
            data = json.loads(file_contents)
            assert data["content"] == content
            assert data["id"] == "1"

        assert result.exit_code == 0


def test_create_multiple_journal_entries(cli_runner: CliRunner):
    """Test creating multiple journal entries in sequence."""

    contents = [
        "First journal entry content",
        "Second journal entry content",
        "Third journal entry content",
    ]

    with tempfile.TemporaryDirectory() as temp_dir:
        storage = JsonStorage(directory=temp_dir)
        journal = JournalManager(storage=storage)

        # Create multiple entries
        for i, content in enumerate(contents, start=1):
            result = cli_runner.invoke(
                cli,
                ["create"],
                input=content,
                obj={"journal": journal},
            )

            # Verify the result
            assert result.exit_code == 0
            assert f"Created entry with ID: {i}" in result.output

            # Verify the file was created with correct content
            temp_file_path = os.path.join(temp_dir, "entries", f"{i}.json")
            assert os.path.exists(temp_file_path)

            with open(temp_file_path, "r") as f:
                file_contents = f.read()
                data = json.loads(file_contents)
                assert data["content"] == content
                assert data["id"] == str(i)

        # Verify all entries exist in the storage
        entries = journal.view_entries()
        assert len(entries) == len(contents)
        for i, content in enumerate(contents, start=1):
            assert str(i) in entries
            assert entries[str(i)].content == content
