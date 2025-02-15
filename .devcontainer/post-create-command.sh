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

# Download zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# Copy .zshrc
cp .devcontainer/.zshrc ~/.zshrc