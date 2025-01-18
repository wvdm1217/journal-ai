from typing import Optional

import click

from journal_ai.config import Config
from journal_ai.storage import JsonStorage
from journal_ai.rag import RAGQuerier


class JournalManager:
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config.from_env()
        self.storage = JsonStorage(config=self.config)
        self.rag = RAGQuerier(self.config)

    def create_entry(self, content: str) -> str:
        entries = self.storage.load_all()
        entry_id = str(len(entries) + 1)
        self.storage.save_entry(entry_id, content)
        return entry_id

    def view_entries(self):
        return self.storage.load_all()

    def search_entries(self, keyword: str):
        entries = self.storage.load_all()
        return {
            id: content
            for id, content in entries.items()
            if keyword.lower() in content.lower()
        }

    def edit_entry(self, entry_id: str, content: str) -> bool:
        existing_entry = self.storage.load_entry(entry_id)
        if existing_entry is not None:
            self.storage.save_entry(entry_id, content, existing_entry)
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


@click.group()
def cli():
    """JournalAI - An LLM-enhanced journaling application for your CLI."""
    pass


@cli.command()
@click.argument("content")
def create(content):
    """Create a new journal entry."""
    try:
        journal = JournalManager()
        entry_id = journal.create_entry(content)
        click.echo(f"Created entry with ID: {entry_id}")
    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True)
        exit(1)


@cli.command()
def view():
    """View all journal entries."""
    journal = JournalManager()
    entries = journal.view_entries()
    for entry_id, entry in entries.items():
        click.echo(f"\nEntry {entry_id}:")
        if entry.title:
            click.echo(f"Title: {entry.title}")
        click.echo(
            f"Created: {entry.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        click.echo(
            f"Updated: {entry.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
        click.echo(f"Words: {entry.word_count}")
        if entry.tags:
            click.echo(f"Tags: {', '.join(entry.tags)}")
        click.echo(f"Content: {entry.content}")
        click.echo("-" * 40)


@cli.command()
@click.argument("keyword")
def search(keyword):
    """Search for entries with a keyword."""
    journal = JournalManager()
    results = journal.search_entries(keyword)
    for entry_id, content in results.items():
        click.echo(f"Entry {entry_id}: {content}")


@cli.command()
@click.argument("entry_id")
@click.argument("content")
def edit(entry_id, content):
    """Edit an existing entry."""
    journal = JournalManager()
    if journal.edit_entry(entry_id, content):
        click.echo(f"Updated entry {entry_id}")
    else:
        click.echo(f"Entry {entry_id} not found")


@cli.command()
@click.argument("entry_id")
def delete(entry_id):
    """Delete a journal entry."""
    journal = JournalManager()
    if journal.delete_entry(entry_id):
        click.echo(f"Deleted entry {entry_id}")
    else:
        click.echo(f"Entry {entry_id} not found")


@cli.command()
def purge():
    """Delete all journal entries."""
    if click.confirm(
        "Are you sure you want to delete all entries? This cannot be undone."
    ):
        journal = JournalManager()
        journal.purge()
        click.echo("All entries have been deleted.")
    else:
        click.echo("Operation cancelled.")


@cli.command()
@click.argument("question")
def query(question):
    """Ask a question about your journal entries."""
    journal = JournalManager()
    response = journal.query(question)
    click.echo("\nAnswer based on your journal entries:")
    click.echo(response)


def main():
    cli()


if __name__ == "__main__":
    main()
