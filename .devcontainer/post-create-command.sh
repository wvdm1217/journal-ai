#!/bin/bash

# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install UV Dependencies
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# Install ruff
uv tool install ruff

# Install pre-commit
uv tool install pre-commit

# Install pre-commit hooks
pre-commit install

# GitHub CLI
gh auth login
gh extension install github/gh-copilot