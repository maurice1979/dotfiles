# 🐍 Pythonic Dotfiles

A small, Python-driven dotfiles setup for macOS. A [Brewfile](https://docs.brew.sh/Brew-Bundle-and-Brewfile) declares every app, CLI tool, VS Code extension and global Python tool; [Homely](https://homely.readthedocs.io/) symlinks the config files; [uv](https://docs.astral.sh/uv/) manages the Python tools.

## 🚀 Features

* **One list of software**: `Brewfile` holds Homebrew formulae, casks (GUI apps and fonts), VS Code extensions and `uv tool` installs, so `brew bundle` covers all of them.
* **Install first, configure second**: `bootstrap.sh` runs `brew bundle` in your terminal, then Homely. Anything a config file needs is installed before the config is linked.
* **Symlinked config**: `homely.py` links zsh, Starship, VS Code, git, ssh and IPython config into place, and lists what still needs a manual step.
* **Re-runnable**: every step is idempotent, and `upsync` re-applies everything.

## 📂 Structure

```text
.
├── bootstrap.sh          # Fresh-Mac entry point: Homebrew → brew bundle → homely
├── Brewfile              # Everything installed (also linked to ~/.Brewfile)
├── homely.py             # Symlinks + post-install checks (no installs)
├── .zshrc                # Shell configuration
├── starship.toml         # Starship prompt
├── .editorconfig         # Editor settings for this repo
├── git/
│   ├── config            # Global git config: identity, SSH commit signing, editor
│   └── ignore            # Global git ignore patterns
├── ssh/
│   └── config            # ~/.ssh/config (no keys, ever)
├── ipython/
│   └── 00-first.py       # IPython/Jupyter auto-imports
└── vscode/
    └── settings.json     # VS Code user settings
```

## 🛠️ Installation (new Mac)

```bash
xcode-select --install          # git; Homebrew would install it too, but you need git to clone
git clone https://github.com/maurice1979/dotfiles.git ~/Documents/dotfiles
cd ~/Documents/dotfiles
./bootstrap.sh
```

Clone wherever you like, but **don't move the clone afterwards**: the symlinks point into it.

`bootstrap.sh`:

1. Asks for your password once and keeps `sudo` alive for the rest of the run.
2. Installs **Homebrew** if it's missing, and puts it on `PATH` for this run (a fresh shell has no `~/.zshrc` yet).
3. Runs **`brew bundle`**: every formula, cask, VS Code extension and uv tool in the `Brewfile`, including `homely` itself. It starts the PostgreSQL service. If an entry fails (e.g. a network blip), the script keeps going so your dotfiles still get linked; re-run it to retry.
4. Runs **`homely add`** (first time) or **`homely update`** (later runs) to create the symlinks. Anything already at a target path is renamed to `<name>.pre-dotfiles` rather than overwritten.

It ends with a status table. ⚠️ rows are the manual steps below.

> **Why installs aren't in `homely.py`:** Homely runs commands without a terminal, so casks that ask for your password (Docker Desktop) fail there, and one failed install aborts the rest of the run halfway. That's what broke the previous bootstrap.

## ✋ After bootstrap (manual steps)

Things that can't or shouldn't be scripted:

1. **SSH key**: restore `~/.ssh/id_ed25519` and `id_ed25519.pub` from your backup (`chmod 600 ~/.ssh/id_ed25519`). `git/config` signs every commit with this key, so **`git commit` fails until it's back**. Then recreate the signature-verification file:
   ```bash
   echo "$(git config user.email) $(cat ~/.ssh/id_ed25519.pub)" > ~/.ssh/allowed_signers
   ssh-add --apple-use-keychain ~/.ssh/id_ed25519
   ```
2. **Google Drive**: open it and sign in. The KeePassXC database lives there (`homely.py` checks for it).
3. **Docker Desktop**: open `Docker.app` once and approve the privileged helper (macOS requires this interactively). It also adds `~/.docker/bin` to `~/.zprofile` itself.
4. **Sign-ins**: `gh auth login`, VS Code (Settings Sync / GitHub Copilot, which ships built in), Slack, Claude, Proton.
5. **SDKMAN** (not on Homebrew), if you need it: https://sdkman.io/install. `.zshrc` sources it only when it exists.
6. Open a new terminal (or `exec zsh`).

## ⚙️ Adding things

| To add…                          | Edit                                   | Then                   |
| -------------------------------- | -------------------------------------- | ---------------------- |
| CLI tool                         | `brew "name"` in `Brewfile`            | `brew bundle --global` |
| GUI app / font                   | `cask "name"` in `Brewfile`            | `brew bundle --global` |
| VS Code extension                | `vscode "publisher.name"` in `Brewfile`| `brew bundle --global` |
| Global Python tool               | `uv "name"` in `Brewfile`              | `brew bundle --global` |
| Config file                      | file in the repo + an entry in `DOTFILES` in `homely.py` | `homely update` |

Find names with `brew search <app>`. To spot drift (things you installed by hand and forgot to add):

```bash
brew bundle check --global --verbose --no-upgrade   # in the Brewfile but not installed (without --no-upgrade it also lists everything outdated)
brew bundle cleanup --global             # installed but not in the Brewfile (dry run; --force removes)
```

> **Note:** anything `.zshrc` references must be in the `Brewfile`, and every block in `.zshrc` is guarded, so a half-installed machine still gets a working shell.

## 🔁 `upsync`

```bash
upsync   # brew update && brew upgrade && brew bundle --global && homely update && exec zsh
```

Upgrades everything, installs whatever was added to the `Brewfile` since the last run, re-applies the symlinks (`homely update` also `git pull`s this repo, and refuses to while it has uncommitted changes), and reloads the shell.

## 🖥️ Adopting a Mac that already has these apps

On a machine where some apps were installed by hand (not via Homebrew), `brew bundle` fails for those casks with *"It seems there is already an App at …"*. Hand them over to Homebrew once:

```bash
brew install --cask --adopt docker-desktop spotify firefox google-drive claude ollama-app \
  proton-drive proton-pass whatsapp blender
```

## 📊 JupyterLab & data science

JupyterLab is a global uv tool with DuckDB, pandas and JupySQL bundled in (`uv "jupyterlab", with: [...]` in the `Brewfile`). To make another library available in every notebook, add it to that `with:` list and run `brew bundle --global`.

`ipython/00-first.py` is linked to `~/.ipython/profile_default/startup/`, so every IPython shell and notebook starts with:

- `import pandas as pd` (with wider display settings), `import numpy as np`, `import duckdb`
- `%load_ext sql` (JupySQL, results as pandas DataFrames)

Start it with `jupyter-lab`. Avoid `uv run` for general exploration: it creates isolated environments that may skip the global startup config.

## 📋 Requirements

- **OS**: macOS (Apple Silicon or Intel).
- **Shell**: zsh with Starship.
- **Python**: managed by uv; nothing needs a system Python.

Built with ❤️ and Python.
