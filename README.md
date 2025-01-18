# JournalAI
An LLM-enhanced journaling application for your CLI.

## Overview
JournalAI is a command-line journaling tool that allows you to manage your journal entries directly from the terminal.

## Features
- **Entry Management**: Create, edit, delete, and view journal entries
- **Search Capability**: Search through entries using keywords
- **Local Storage**: All entries are stored locally as JSON files
- **Bulk Operations**: Ability to view all entries or purge entire journal

## Installation
To install journal-ai, follow these steps:

### From source

1. Clone the repository:
    ```sh
    git clone https://github.com/wvdm1217/journal-ai.git
    ```

2. Navigate to the project directory:
    ```sh
    cd journal-ai
    ```

3. Install the required dependencies:
    ```sh
    uv venv
    source .venv/bin/activate
    ```

4. Install dependencies and package:
    ```sh
    uv pip install -e .
    ```

### Development setup

1. Create a development environment:
    ```sh
    uv venv
    source .venv/bin/activate
    ```

2. Install development dependencies:
    ```sh
    uv pip install -e ".[dev]"
    ```

3. Install pre-commit hooks:
    ```sh
    pre-commit install
    ```

4. Run tests:
    ```sh
    pytest
    ```

## Usage

### Basic Commands
```sh
# Create a new journal entry
journal-ai create "Your journal entry text here"

# View all journal entries
journal-ai view

# Search for entries with a keyword
journal-ai search "keyword"

# Edit an existing entry
journal-ai edit <entry_id> "Updated journal entry text here"

# Delete a journal entry
journal-ai delete <entry_id>
```

## Contributing
We welcome contributions! Please read our contributing guidelines for more details.