# Every program referenced here is installed by the Brewfile (except SDKMAN, see
# README) and each block is guarded, so a half-installed machine still gets a shell.

# 1. HOMEBREW (must be first: sets PATH, HOMEBREW_PREFIX and FPATH for completions)
if [[ -x /opt/homebrew/bin/brew ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
fi

# 2. PATH: uv tools (homely, ruff, jupyter-lab, ...) and the dbt VS Code extension's dbt
export PATH="$HOME/.local/bin:$PATH"
# Docker Desktop's CLI tools (Docker.app also adds ~/.docker/bin via ~/.zprofile itself)
export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"

# 3. COMPLETIONS (after FPATH is complete, before plugins that wrap widgets)
fpath=($HOME/.docker/completions $fpath)
autoload -Uz compinit
compinit

# 4. TOOLS
export EDITOR='code --wait'

if command -v starship &> /dev/null; then
    eval "$(starship init zsh)"
fi

# 5. ALIASES
# ~/.Brewfile is a symlink to the repo's Brewfile (homely.py), so --global finds it.
alias upsync="brew update && brew upgrade && brew bundle --global && homely update && exec zsh"
alias dbtf="$HOME/.local/bin/dbt"  # dbt v2 binary installed by the dbt VS Code extension

# 6. ZSH PLUGINS (syntax highlighting must be sourced last, per its README)
if [[ -f "$HOMEBREW_PREFIX/share/zsh-autosuggestions/zsh-autosuggestions.zsh" ]]; then
    source "$HOMEBREW_PREFIX/share/zsh-autosuggestions/zsh-autosuggestions.zsh"
fi
if [[ -f "$HOMEBREW_PREFIX/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" ]]; then
    source "$HOMEBREW_PREFIX/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"
fi

# 7. SDKMAN: installed by hand (not on Homebrew); must stay at the end of the file.
export SDKMAN_DIR="$HOME/.sdkman"
[[ -s "$SDKMAN_DIR/bin/sdkman-init.sh" ]] && source "$SDKMAN_DIR/bin/sdkman-init.sh"
