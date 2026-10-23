# Everything this machine installs. `bootstrap.sh` runs `brew bundle` in a real
# terminal *before* homely, so casks that prompt for sudo (docker-desktop) work and
# every binary homely.py / .zshrc relies on already exists.
#
#   brew bundle check --global --no-upgrade   # anything missing?
#   brew bundle         # install/upgrade everything below
#   brew bundle dump --file=- --describe   # what's installed (to spot drift)

tap "dbt-labs/dbt"

# --- Shell -------------------------------------------------------------------
brew "git"
brew "starship"
brew "zsh-autosuggestions"
brew "zsh-syntax-highlighting"
brew "direnv"

# --- CLI tools ---------------------------------------------------------------
brew "gh"
brew "jq"
brew "tree"
brew "wget"
brew "ffmpeg"
brew "tectonic"
brew "prek"

# --- Data / dev --------------------------------------------------------------
brew "uv"
brew "node"
brew "duckdb"
# Versioned on purpose: unversioned "postgresql" is just an alias that moves with
# each major release, and a major bump needs a manual pg_upgrade of the data dir.
# Keg-only, so link: true puts psql & co. on PATH; the service starts at login and
# restarts only when brew bundle upgrades it.
brew "postgresql@18", link: true, restart_service: :changed
brew "dbt-labs/dbt/dbt"
brew "openjdk@21"
brew "awscli"
brew "opentofu"

# --- Fonts -------------------------------------------------------------------
cask "font-hack-nerd-font"
cask "font-meslo-lg-nerd-font"

# --- Dev apps ----------------------------------------------------------------
cask "visual-studio-code"
cask "ghostty"
cask "docker-desktop"  # formerly the "docker" cask; open Docker.app once by hand (README)
cask "dbeaver-community"
cask "quarto"
cask "ollama-app"
cask "claude"

# --- Personal apps -----------------------------------------------------------
cask "keepassxc"
cask "google-drive"    # holds the KeePassXC database
cask "proton-drive"
cask "proton-pass"
cask "rectangle"
cask "firefox"
cask "slack"
cask "spotify"
cask "whatsapp"
cask "blender"

# --- VS Code extensions ------------------------------------------------------
# GitHub Copilot is built into VS Code now; installing github.copilot separately fails.
vscode "anthropic.claude-code"
vscode "charliermarsh.ruff"
vscode "chuckjonas.duckdb"
vscode "dbtlabsinc.dbt"
vscode "dvirtz.parquet-viewer"
vscode "eamodio.gitlens"
vscode "hediet.vscode-drawio"
vscode "mermaidchart.vscode-mermaid-chart"
vscode "ms-python.debugpy"
vscode "ms-python.python"
vscode "ms-python.vscode-pylance"
vscode "ms-python.vscode-python-envs"
vscode "ms-toolsai.jupyter"
vscode "ms-toolsai.jupyter-keymap"
vscode "ms-toolsai.jupyter-renderers"
vscode "ms-toolsai.vscode-jupyter-cell-tags"
vscode "ms-toolsai.vscode-jupyter-slideshow"
vscode "ms-vscode.makefile-tools"
vscode "tamasfe.even-better-toml"
vscode "tomoki1207.pdf"

# --- Global Python tools (uv tool install) -----------------------------------
uv "homely"
uv "ruff"
uv "black"
uv "mypy"
uv "graphifyy[sql]"
uv "jupyterlab", with: ["duckdb", "pandas", "jupysql"]
