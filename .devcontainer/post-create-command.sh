#!/bin/bash

# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install UV Dependencies
uv venv
source .venv/bin/activate
uv sync --locked --dev --group=test

# Install pre-commit hooks
pre-commit install

# Download zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# Copy .zshrc
cp .devcontainer/.zshrc ~/.zshrc
