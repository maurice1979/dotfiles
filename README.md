# 🐍 Pythonic Dotfiles

A modular, dictionary-driven dotfiles management system built for Python developers. Managed by [Homely](https://homely.readthedocs.io/) and powered by [uv](https://docs.astral.sh/uv/).

## 🚀 Features

* **Logic-Driven:** Configuration managed via `homely.py` (standard Python 3).
* **Auto-Installation:** Automatically installs missing binaries (Starship, etc.) via Homebrew.
* **Python Toolchain:** Uses `uv tool` to manage global isolated environments for tools like `black`, `ruff`, and `mypy`.
* **VSCode Sync:** Manages `settings.json` and ensures the pathing for macOS is handled correctly.
* **Fast Bootstrap:** A single shell script to go from a fresh OS to a fully configured environment.

## 📂 Structure

```text
.
├── bootstrap.sh    # One-click installation script
├── homely.py       # Main configuration logic & symlinking
├── starship.toml   # Starship prompt configuration
├── .zshrc          # Shell configuration
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

- Installs Homebrew (if missing).

- Installs uv for high-performance Python package management.

- Installs Homely as a global tool.

- Runs homely update to create symlinks and install dependencies.


## ⚙️ Configuration Logic

This repo uses a central DOTFILES_DICT in homely.py. To add a new config file, just add an entry:
Python

```
"tool_name": {
    "from": "source_in_repo",
    "to": "~/path/to/destination",
    "bin": "command_to_check",
    "install_cmd": "brew install tool_name"
}
```

## Updating the dotfiles

1 - Add a new entry to the `DOTFILES_DICT` in `homely.py``
2 - Execute `homely update`

## 📋 Requirements

- OS: macOS (Current logic uses brew and Mac-specific VSCode paths).
- Shell: Zsh (with Starship prompt).
- Python: 3.10+ (managed via uv).

Built with ❤️ and Python.
