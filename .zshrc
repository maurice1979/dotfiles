# 1. INITIALIZE HOMEBREW (Must be first)
if [[ -f "/opt/homebrew/bin/brew" ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
fi

# 2. PATH CONFIGURATION
export PATH="$HOME/.local/bin:$PATH"

# 3. PYTHON / UV CONFIGURATION
export PATH="$HOME/.local/bin:$PATH"
if [[ -f "$HOME/.cargo/env" ]]; then
    source "$HOME/.cargo/env"
fi

# 4. HOMEBREW PLUGINS
# These were installed via BREW_FORMULAE in homely.py
if [[ -d "$HOMEBREW_PREFIX/share/zsh-autosuggestions" ]]; then
    source "$HOMEBREW_PREFIX/share/zsh-autosuggestions/zsh-autosuggestions.zsh"
fi

if [[ -d "$HOMEBREW_PREFIX/share/zsh-syntax-highlighting" ]]; then
    source "$HOMEBREW_PREFIX/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"
fi

# 5. STARSHIP PROMPT
if command -v starship &> /dev/null; then
    eval "$(starship init zsh)"
fi

# 6. ALIASES & USER CONFIG
export EDITOR='code --wait'

alias upsync="brew update && brew upgrade && homely update && source ~/.zshrc"
# alias py="python3"
# ssh-add --apple-use-keychain ~/.ssh/id_ed25519 2>/dev/null