# JournalAI


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)


An LLM-enhanced journaling application for your CLI.

## Overview
JournalAI is a command-line journaling tool that leverages AI to enhance your journaling experience with smart features like automatic title generation and semantic search.

## Features
- **Entry Management**: Create, edit, delete, and view journal entries
- **AI-Powered Features**:
  - Automatic title generation for entries
  - Semantic search using RAG (Retrieval-Augmented Generation)
  - Natural language querying of your journal entries
- **Local Storage**: All entries and vector indices are stored locally
- **Search Capabilities**: 
  - Keyword-based search
  - Semantic search through RAG
- **Bulk Operations**: View all entries or purge entire journal

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

## Environment Setup
Before using JournalAI, you need to set up the following environment variables:

```sh
OPENAI_API_KEY=...
OPENAI_CHAT_MODEL=gpt-4o
OPENAI_EMBEDDING_MODEL=text-embedding-3-large
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