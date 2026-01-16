# 🐍 Pythonic Dotfiles

A modular, dictionary-driven dotfiles management system built for Python developers. Managed by [Homely](https://homely.readthedocs.io/) and powered by [uv](https://docs.astral.sh/uv/).

## 🚀 Features

* **Logic-Driven**: Configuration managed via `homely.py` (standard Python 3).
* **App & Tool Automation**: Automatically syncs Homebrew Formulae (CLI) and Casks (GUI).
* **VS Code Sync**: Manages `settings.json` and automatically installs your favorite extensions via the code CLI.
* **Python Toolchain**: Uses uv tool to manage global isolated environments for tools like `black`, `ruff`, and `mypy`.
* **Git Global Config**: Automatically sets up global `.gitignore` and configures `VS Code` as your default editor.
* **Fast Bootstrap:**: A single shell script to go from a fresh OS to a fully configured environment.

## 📂 Structure

```text
.
├── bootstrap.sh      # One-click installation script
├── homely.py         # Main configuration logic, symlinking, and app syncing
├── starship.toml     # Starship prompt configuration
├── .zshrc            # Shell configuration
├── git/
│   └── ignore        # Global git ignore patterns
└── vscode/
    └── settings.json # VSCode user preferences
```

## 🛠️ Installation

On a new machine, simply clone this repository and run the bootstrap script:

```bash
git clone [https://github.com/your-username/dotfiles.git](https://github.com/your-username/dotfiles.git) ~/repos_personal/dotfiles
cd ~/repos_personal/dotfiles
chmod +x bootstrap.sh
./bootstrap.sh
```

What the Bootstrap does:

* Installs **Homebrew** (if missing).
* Installs **uv** for high-performance Python package management.
* Installs **Homely** as a global tool.
* Runs `homely update` to create symlinks and install dependencies.


## ⚙️ Configuration Logic


This repo uses a central homely.py file. To add new tools, simply update the relevant list:

* `DOTFILES_DICT`: For files that need to be symlinked (e.g., config files).
* `BREW_FORMULAE`: For command-line tools (e.g., `jq`, `gh`).
* `BREW_CASKS`: For GUI applications (e.g., `slack`, `spotify`).
* `VSCODE_EXTS`: For VS Code extensions (e.g., `ms-python.python`).
* `PYTHON_TOOLS`: For global Python CLI tools managed by `uv`.

## Updating the dotfiles

1 - Add a new entry to the `DOTFILES_DICT` in `homely.py`
2 - Execute `homely update`

Since `homely` is installed globally a uv tool, you can invoke it from any location.

## 📋 Requirements

- **OS**: macOS (Current logic uses brew and Mac-specific VSCode paths).
- **Shell**: Zsh (with Starship prompt).
- **Python**: 3.10+ (managed via `uv`).

Built with ❤️ and Python.
