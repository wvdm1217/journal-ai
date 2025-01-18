import click
from typing import Optional
from journal_ai.storage import JsonStorage


class JournalManager:
    def __init__(self):
        self.storage = JsonStorage()

    def create_entry(self, content: str) -> str:
        entries = self.storage.load_all()
        entry_id = str(len(entries) + 1)
        self.storage.save_entry(entry_id, content)
        return entry_id

    def view_entries(self):
        return self.storage.load_all()

    def search_entries(self, keyword: str):
        entries = self.storage.load_all()
        return {id: content for id, content in entries.items() if keyword.lower() in content.lower()}

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
    for entry_id, entry in entries.items():
        click.echo(f"\nEntry {entry_id}:")
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


@cli.command()
def purge():
    """Delete all journal entries."""
    if click.confirm('Are you sure you want to delete all entries? This cannot be undone.'):
        journal = JournalManager()
        journal.purge()
        click.echo("All entries have been deleted.")
    else:
        click.echo("Operation cancelled.")


def main():
    cli()


if __name__ == "__main__":
    main()
