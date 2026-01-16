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

## 📊 JupyterLab & Data Science Setup

This environment is optimized for data engineering and analysis using **uv** and **DuckDB**.

### 🛠️ Installation
JupyterLab is managed as a standalone tool via `uv`. The `homely.py` script automatically bundles essential data plugins:
- **DuckDB & JupySQL:** For high-performance SQL analysis.
- **Pandas & NumPy:** For data manipulation.

### 🚀 Automatic Imports (IPython Startup)
To save time, a startup script is symlinked to `~/.ipython/profile_default/startup/00-first.py`. 

Every time you open a Jupyter Notebook or IPython shell, the following are pre-loaded:
- `import pandas as pd` (with optimized display settings)
- `import numpy as np`
- `import duckdb`
- `%load_ext sql` (configured for DuckDB + Pandas)

### 💡 Usage
To start your data environment, simply run:
```bash
jupyter-lab
```

> Note: Avoid using uv run for general exploration, as it creates isolated environments that may ignore your global startup configs. Use the global jupyter-lab tool for the best experience.

### Pro-Tip: Adding new libraries to Jupyter
If you find yourself needing a new library (like `matplotlib` or `scipy`) across all your notebooks, you don't need to change your project files. Just update the `uv tool install` line in `homely.py`:

```python
    execute([
        str(uv_path), "tool", "install", "jupyterlab", 
        "--with", "duckdb", 
        "--with", "pandas", 
        "--with", "jupysql",
        "--with", "matplotlib"  # Add it here!
    ])

### 🔍 Customization

To modify your auto-imports or Pandas display settings, edit: ipython/00-first.py

## 📋 Requirements

- **OS**: macOS (Current logic uses brew and Mac-specific VSCode paths).
- **Shell**: Zsh (with Starship prompt).
- **Python**: 3.10+ (managed via `uv`).

Built with ❤️ and Python.
