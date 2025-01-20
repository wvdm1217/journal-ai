#!/bin/bash

# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install UV Dependencies
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install