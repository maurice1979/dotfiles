#!/bin/bash

# Exit on error
set -e

echo "🚀 Starting macOS Bootstrap..."

# 1. Install Homebrew if not present
if ! command -v brew &> /dev/null; then
    echo "🍺 Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add brew to path for the rest of the script (Apple Silicon)
    eval "$(/opt/homebrew/bin/brew shellenv)"
else
    echo "✅ Homebrew already installed."
fi

# 2. Install uv (via Homebrew as per your preference)
if ! command -v uv &> /dev/null; then
    echo "🐍 Installing uv..."
    brew install uv
else
    echo "✅ uv already installed."
fi

# 3. Install Homely (via pipx/uv tool)
if ! command -v homely &> /dev/null; then
    echo "🏠 Installing Homely..."
    uv tool install homely
else
    echo "✅ Homely already installed."
fi

# 4. Run Homely for the first time
echo "📦 Syncing dotfiles with Homely..."
# This assumes the script is inside your dotfiles repo
DOTFILES_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DOTFILES_DIR"
homely add .
homely update

echo ""
print "===================================================="
echo "🎉 Bootstrap complete!"
echo "👉 Restart your terminal or run: source ~/.zshrc"
echo "👉 Then run 'upsync' to verify everything."
print "===================================================="