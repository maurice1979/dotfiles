#!/bin/bash
# Fresh-macOS bootstrap. Safe to re-run: every step is idempotent.
#
#   1. Homebrew          (also installs the Xcode Command Line Tools)
#   2. brew bundle       every app, CLI, VS Code extension and uv tool (Brewfile)
#   3. homely            symlinks + config, which need step 2's binaries
#
# Installs run here, in your terminal, not inside homely: homely runs commands
# without a TTY, so casks that ask for your sudo password (docker-desktop) fail there.

set -euo pipefail

DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DOTFILES_DIR"

echo "🚀 Starting macOS bootstrap from $DOTFILES_DIR"

# Ask for the password once up front and keep sudo alive for the whole run,
# so cask installs don't stall halfway through on a prompt.
sudo -v
while true; do sudo -n true; sleep 60; kill -0 "$$" || exit; done 2>/dev/null &

# 1. Homebrew
if [[ -x /opt/homebrew/bin/brew ]]; then
    BREW=/opt/homebrew/bin/brew
elif [[ -x /usr/local/bin/brew ]]; then
    BREW=/usr/local/bin/brew
else
    echo "🍺 Installing Homebrew..."
    NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    BREW=/opt/homebrew/bin/brew
    [[ -x $BREW ]] || BREW=/usr/local/bin/brew
fi
# Always, not only right after installing: a fresh shell has no ~/.zshrc yet,
# so brew isn't on PATH even when it is already installed.
eval "$("$BREW" shellenv)"

# uv tools (homely, ruff, ...) land here; it isn't on PATH until .zshrc is linked.
export PATH="$HOME/.local/bin:$PATH"

# 2. Everything in the Brewfile
echo "📦 Installing Brewfile packages (this takes a while the first time)..."
if ! brew bundle --file="$DOTFILES_DIR/Brewfile"; then
    echo ""
    echo "⚠️  Some Brewfile entries failed (see above). Continuing with the dotfiles;"
    echo "    re-run ./bootstrap.sh or 'brew bundle' afterwards to retry them."
fi

# 3. Dotfiles. `homely add` registers the repo and runs the update itself;
# on later runs the repo is already registered, so just update.
command -v homely >/dev/null || { echo "❌ homely not installed (Brewfile uv entry failed?)"; exit 1; }
if homely repolist 2>/dev/null | grep -q "$DOTFILES_DIR\$"; then
    echo "🏠 Updating dotfiles with homely..."
    homely update
else
    echo "🏠 Registering dotfiles with homely..."
    homely add "$DOTFILES_DIR"
fi

echo ""
echo "===================================================="
echo "🎉 Bootstrap complete!"
echo "👉 Open a new terminal (or: exec zsh)."
echo "👉 Manual steps left: see 'After bootstrap' in README.md"
echo "===================================================="
