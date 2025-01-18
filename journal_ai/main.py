import click
from typing import Optional
from journal_ai.storage import JsonStorage


class JournalManager:
    def __init__(self):
        self.storage = JsonStorage()

    def create_entry(self, content: str) -> str:
        entries = self.storage.load()
        entry_id = str(len(entries) + 1)
        entries[entry_id] = content
        self.storage.save(entries)
        return entry_id

    def view_entries(self):
        return self.storage.load()

    def search_entries(self, keyword: str):
        entries = self.storage.load()
        return {id: content for id, content in entries.items() if keyword.lower() in content.lower()}

    def edit_entry(self, entry_id: str, content: str) -> bool:
        entries = self.storage.load()
        if entry_id in entries:
            entries[entry_id] = content
            self.storage.save(entries)
            return True
        return False

    def delete_entry(self, entry_id: str) -> bool:
        entries = self.storage.load()
        if entry_id in entries:
            del entries[entry_id]
            self.storage.save(entries)
            return True
        return False


@click.group()
def cli():
    """JournalAI - An LLM-enhanced journaling application for your CLI."""
    pass


@cli.command()
@click.argument('content')
def create(content):
    """Create a new journal entry."""
    journal = JournalManager()
    entry_id = journal.create_entry(content)
    click.echo(f"Created entry with ID: {entry_id}")


@cli.command()
def view():
    """View all journal entries."""
    journal = JournalManager()
    entries = journal.view_entries()
    for entry_id, content in entries.items():
        click.echo(f"Entry {entry_id}: {content}")


@cli.command()
@click.argument('keyword')
def search(keyword):
    """Search for entries with a keyword."""
    journal = JournalManager()
    results = journal.search_entries(keyword)
    for entry_id, content in results.items():
        click.echo(f"Entry {entry_id}: {content}")


@cli.command()
@click.argument('entry_id')
@click.argument('content')
def edit(entry_id, content):
    """Edit an existing entry."""
    journal = JournalManager()
    if journal.edit_entry(entry_id, content):
        click.echo(f"Updated entry {entry_id}")
    else:
        click.echo(f"Entry {entry_id} not found")


@cli.command()
@click.argument('entry_id')
def delete(entry_id):
    """Delete a journal entry."""
    journal = JournalManager()
    if journal.delete_entry(entry_id):
        click.echo(f"Deleted entry {entry_id}")
    else:
        click.echo(f"Entry {entry_id} not found")


def main():
    cli()


if __name__ == "__main__":
    main()
