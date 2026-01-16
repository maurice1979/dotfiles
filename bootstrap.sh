#!/bin/bash

set -e  # Exit on error

echo "🚀 Starting dotfiles bootstrap..."

# 1. Install uv if not present
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
else
    echo "✅ uv is already installed."
fi

# 2. Install homely using uv tool
if ! command -v homely &> /dev/null; then
    echo "🏠 Installing Homely..."
    uv tool install homely
else
    echo "✅ Homely is already installed."
fi

# 3. Get the directory of this script
DOTFILES_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 4. Register and Update with Homely
echo "🔄 Syncing dotfiles with Homely..."
homely add "$DOTFILES_DIR"
homely update

echo "✨ Bootstrap complete! Restart your shell to see changes."