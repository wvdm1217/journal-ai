# JournalAI
An LLM-enhanced journaling application for your CLI.

## Overview
JournalAI is a command-line journaling tool that leverages Retrieval-Augmented Generation (RAG) and AI to provide an enhanced journaling experience. It uses UV for Python tooling to ensure a smooth development and usage process.

## Features
- **AI-Powered Entries**: Generate and enhance journal entries with AI assistance
- **Smart Search**: Search through past entries using natural language queries
- **Entry Management**: Create, edit, delete, and view journal entries
- **Custom Prompts**: Use personalized prompts for consistent journaling
- **Data Privacy**: Local storage of entries with optional encryption

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