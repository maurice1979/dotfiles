# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:$HOME/.local/bin:/usr/local/bin:$PATH

# Starship shell prompt
eval "$(starship init zsh)"

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='nvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch $(uname -m)"

# hide the username
# DEFAULT_USER prompt_context(){}

# Homebrew
eval "$(/opt/homebrew/bin/brew shellenv)"

# Load github key at login
#ssh-add --apple-use-keychain ~/.ssh/maurice1979
#ssh-add --apple-use-keychain ~/.ssh/id_ed25519

# Uncomment when using DBT
# source ~/.dbtenv

# source antidote
source ~/.antidote/antidote.zsh

# initialize plugins statically with ${ZDOTDIR:-~}/.zsh_plugins.txt
antidote load
