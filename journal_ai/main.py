import click

from journal_ai.config import Config, get_config
from journal_ai.journal.journal import JournalManager
from journal_ai.rag import RAGQuerier
from journal_ai.storage import JsonStorage


@click.group()
@click.pass_context
def cli(ctx: click.Context):
    """JournalAI - An LLM-enhanced journaling application for your CLI."""
    ctx.ensure_object(dict)
    if "journal" not in ctx.obj:
        config: Config = get_config()
        storage = JsonStorage(config=config)
        rag = RAGQuerier(config=config)
        ctx.obj["journal"] = JournalManager(storage=storage, rag=rag)


@cli.command()
@click.pass_context
def create(ctx: click.Context):
    """Create a new journal entry.
    Enter your content and press Ctrl+D (Unix) or Ctrl+Z (Windows) when done."""
    click.echo(
        """Enter your journal entry
        (Press Ctrl+D on Unix or Ctrl+Z on Windows when done):"""
    )
    try:
        content = click.get_text_stream("stdin").read().strip()
        if not content:
            click.echo("Empty entry not allowed.", err=True)
            exit(1)

        journal: JournalManager = ctx.obj["journal"]
        entry_id = journal.create_entry(content)
        click.echo(f"\nCreated entry with ID: {entry_id}")
    except (EOFError, KeyboardInterrupt):
        click.echo("\nEntry creation cancelled.")
        exit(1)
    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True)
        exit(1)


@cli.command()
@click.pass_context
def view(ctx: click.Context):
    """View all journal entries."""
    journal: JournalManager = ctx.obj["journal"]
    entries = journal.view_entries()
    for entry_id, entry in entries.items():
        click.echo(f"\nEntry {entry_id}:")
        if entry.title:
            click.echo(f"Title: {entry.title}")
        click.echo(f"Created: {entry.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        click.echo(f"Updated: {entry.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
        click.echo(f"Words: {entry.word_count}")
        if entry.tags:
            click.echo(f"Tags: {', '.join(entry.tags)}")
        click.echo(f"Content: {entry.content}")
        click.echo("-" * 40)


@cli.command()
@click.argument("keyword")
@click.pass_context
def search(ctx: click.Context, keyword: str):
    """Search for entries with a keyword."""
    journal: JournalManager = ctx.obj["journal"]
    results = journal.search_entries(keyword)
    for entry_id, content in results.items():
        click.echo(f"Entry {entry_id}: {content}")


@cli.command()
@click.argument("entry_id")
@click.argument("content")
@click.pass_context
def edit(ctx: click.Context, entry_id: str, content: str):
    """Edit an existing entry."""
    journal: JournalManager = ctx.obj["journal"]
    if journal.edit_entry(entry_id, content):
        click.echo(f"Updated entry {entry_id}")
    else:
        click.echo(f"Entry {entry_id} not found")


@cli.command()
@click.argument("entry_id")
@click.pass_context
def delete(ctx: click.Context, entry_id: str):
    """Delete a journal entry."""
    journal: JournalManager = ctx.obj["journal"]
    if journal.delete_entry(entry_id):
        click.echo(f"Deleted entry {entry_id}")
    else:
        click.echo(f"Entry {entry_id} not found")


@cli.command()
@click.pass_context
def purge(ctx: click.Context):
    """Delete all journal entries."""
    if click.confirm(
        "Are you sure you want to delete all entries? This cannot be undone."
    ):
        journal: JournalManager = ctx.obj["journal"]
        journal.purge()
        click.echo("All entries have been deleted.")
    else:
        click.echo("Operation cancelled.")


@cli.command()
@click.argument("question")
@click.pass_context
def query(ctx: click.Context, question: str):
    """Ask a question about your journal entries."""
    journal: JournalManager = ctx.obj["journal"]
    response = journal.query(question)
    click.echo("\nAnswer based on your journal entries:")
    click.echo(response)


def main():
    cli(obj={})


if __name__ == "__main__":
    main()
