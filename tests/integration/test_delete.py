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


def test_delete_journal_entry(cli_runner: CliRunner):
    """Test the full end-to-end flow of deleting a journal entry."""

    # First create an entry that we'll delete
    content = "Test journal entry to be deleted"

    with tempfile.TemporaryDirectory() as temp_dir:
        # Set up storage and journal manager
        storage = JsonStorage(directory=temp_dir)
        journal = JournalManager(storage=storage)

        # Create an entry first
        entry_id = journal.create_entry(content)
        temp_file_path = os.path.join(temp_dir, "entries", f"{entry_id}.json")

        # Verify the entry exists
        assert os.path.exists(temp_file_path)

        # Test delete functionality
        result = cli_runner.invoke(
            cli,
            ["delete", entry_id],
            obj={"journal": journal},
        )

        # Verify the entry was deleted
        assert not os.path.exists(temp_file_path)
        assert result.exit_code == 0
        assert f"Deleted entry {entry_id}" in result.output


def test_delete_nonexistent_entry(cli_runner: CliRunner):
    """Test deleting a journal entry that doesn't exist."""

    with tempfile.TemporaryDirectory() as temp_dir:
        # Set up storage and journal manager
        storage = JsonStorage(directory=temp_dir)
        journal = JournalManager(storage=storage)

        # Try to delete a non-existent entry
        nonexistent_id = "999"
        result = cli_runner.invoke(
            cli,
            ["delete", nonexistent_id],
            obj={"journal": journal},
        )

        # Verify the command executed but reported that the entry wasn't found
        assert result.exit_code == 0
        assert f"Entry {nonexistent_id} not found" in result.output
