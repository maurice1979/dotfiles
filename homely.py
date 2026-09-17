import platform
import shutil
from pathlib import Path

from homely.files import mkdir, symlink
from homely.system import execute

# 1. Configuration: Dotfiles Symlinks
DOTFILES_DICT = {
    "starship": {
        "from": "starship.toml",
        "to": "~/.config/starship.toml",
        "install_cmd": "brew install starship",
        "bin": "starship",
    },
    "zsh": {
        "from": ".zshrc",
        "to": "~/.zshrc",
        "bin": "zsh",
    },
    "vscode_settings": {
        "from": "vscode/settings.json",
        "to": "~/Library/Application Support/Code/User/settings.json",
        "bin": "code",
    },
    "gitignore_global": {
        "from": "git/ignore",
        "to": "~/.config/git/ignore",
    },
    "ipython_startup": {
        "from": "ipython/00-first.py",
        "to": "~/.ipython/profile_default/startup/00-first.py",
    },
}

# 2. Configuration: CLI Tools (Homebrew Formulae)
BREW_FORMULAE = [
    "duckdb",
    "ffmpeg",
    "gh",
    "jq",
    "postgresql",
    "tree",
    "wget",
    "zsh-autosuggestions",
    "zsh-syntax-highlighting",
]

# 3. Configuration: GUI Applications (Homebrew Casks)
BREW_CASKS = [
    "visual-studio-code",
    "font-hack-nerd-font",
    "ghostty",
    "keepassxc",
    "rectangle",
    "slack",
    "spotify",
    "docker",
]

# 4. Configuration: VS Code Extensions
VSCODE_EXTS = [
    "charliermarsh.ruff",
    "ms-python.python",
    "github.copilot",
    "tamasfe.even-better-toml",
    "eamodio.gitlens",
    "ms-toolsai.jupyter",
]

# 5. Configuration: Python Global Tools (via uv)
PYTHON_TOOLS: list[str] = ["black", "ruff", "mypy"]

# Track results for the final summary
summary_data = []

# ---------------------------------------------------------
# EXECUTION
# ---------------------------------------------------------

# A. Ensure Directories Exist
config_dirs = [
    "~/.config",
    "~/.config/git",
    "~/Library/Application Support/Code/User",
    "~/.ipython/profile_default/startup",
]
for d in config_dirs:
    mkdir(d)

# B. Process Dotfiles Symlinks
for item, config in DOTFILES_DICT.items():
    print(f"📦 Processing {item}...")
    status = "✅"
    binary = config.get("bin")
    if binary and not shutil.which(binary):
        install_cmd = config.get("install_cmd")
        if install_cmd:
            print(f"  🚀 Installing {item}...")
            execute(install_cmd.split())
        else:
            status = "⚠️  No Bin"

    src = Path(__file__).parent / config["from"]
    if src.exists():
        symlink(config["from"], config["to"])
    else:
        status = "❌ Src Missing"
    summary_data.append((item, config["to"], status))

# C. Process CLI Tools (Formulae)
if shutil.which("brew"):
    print("🍺 Syncing CLI Tools...")
    for formula in BREW_FORMULAE:
        status = "✅"
        if not shutil.which(formula):
            print(f"  🚀 Installing {formula}...")
            execute(["brew", "install", formula])
        summary_data.append((formula, "brew install", status))

# D. Process GUI Apps (Casks)
if shutil.which("brew") and platform.system() == "Darwin":
    print("🖥️  Syncing GUI Applications...")
    for cask in BREW_CASKS:
        # `brew list --cask` is the source of truth for "already installed", unlike
        # guessing an /Applications/*.app name (which never matches app-less casks
        # like fonts, forcing a redundant install attempt on every run).
        retcode, _, _ = execute(["brew", "list", "--cask", cask], stdout=True, stderr=True, expectexit=(0, 1))
        if retcode != 0:
            print(f"  🚀 Installing {cask}...")
            execute(["brew", "install", "--cask", cask])
        summary_data.append((cask, "/Applications", "✅"))

# E. Process VS Code Extensions
if shutil.which("code"):
    print("🔌 Syncing VS Code Extensions...")
    _, stdout, _ = execute(["code", "--list-extensions"], stdout=True)
    installed_exts = [line.lower() for line in stdout.decode().splitlines()]

    for ext in VSCODE_EXTS:
        status = "✅"
        if ext.lower() not in installed_exts:
            print(f"  🚀 Installing extension: {ext}...")
            # Some extension dependencies can fail with exit code 1 even though
            # the system is in a valid state (e.g. built-in copilot chat is newer).
            retcode, out, err = execute(
                ["code", "--install-extension", ext],
                stdout=True,
                stderr=True,
                expectexit=(0, 1),
            )
            if retcode != 0:
                output_text = ((out or b"") + b"\n" + (err or b"")).decode("utf-8", errors="replace").lower()
                if "built-in extension" in output_text and "cannot be downgraded" in output_text:
                    print(f"  ⚠️  Skipping {ext}: a newer built-in dependency is already present.")
                    status = "⚠️ Built-in newer"
                else:
                    raise SystemError(f"Failed installing extension {ext}.\n{output_text.strip()}")
        summary_data.append((ext.split(".")[-1], "VS Code Ext", status))

# F.1 Global Python Tools & JupyterLab via uv
uv_path = shutil.which("uv") or Path.home() / ".local/bin/uv"
if uv_path:
    print("🐍 Syncing Python tools...")
    for tool in PYTHON_TOOLS:
        execute([str(uv_path), "tool", "install", tool])

    print("📊 Installing JupyterLab with Data Plugins...")
    execute(
        [str(uv_path), "tool", "install", "jupyterlab", "--with", "duckdb", "--with", "pandas", "--with", "jupysql"]
    )
    summary_data.append(("jupyterlab", "uv tool (ds bundle)", "✅"))
    summary_data.append(("python_tools", "uv tool install", "✅"))

# F.2 Safety Check: KeePassXC Database presence
KEEPASS_DB_RELATIVE_PATH = "Library/CloudStorage/GoogleDrive-is.maurice@gmail.com/My Drive/keypass/maupass.kdbx"

print("🔐 Checking KeePassXC Database...")
db_path: Path = Path.home() / KEEPASS_DB_RELATIVE_PATH

if db_path.exists():
    print(f"  ✅ Database found at {KEEPASS_DB_RELATIVE_PATH}")
    summary_data.append(("keepass_db", "File exists", "✅"))
else:
    print(f"  ⚠️  Warning: Database NOT found at {db_path}")
    print("     Ensure your cloud sync (Dropbox/iCloud) is signed in.")
    summary_data.append(("keepass_db", "File missing", "⚠️"))

# F.3 PostgreSQL Service Logic
if shutil.which("brew") and "postgresql" in BREW_FORMULAE:
    print("🐘 Managing PostgreSQL service...")
    # Get status of services
    _, stdout, _ = execute(["brew", "services", "list"], stdout=True)
    services_list = stdout.decode()

    # Find the postgresql line specifically, so an unrelated "started" service
    # elsewhere in the list can't be mistaken for postgresql already running.
    pg_line = next((line for line in services_list.splitlines() if line.startswith("postgresql")), "")

    # If the service isn't running, start it
    if "started" not in pg_line:
        print("  🚀 Starting postgresql...")
        execute(["brew", "services", "start", "postgresql"])
        summary_data.append(("postgres_service", "Started", "✅"))
    else:
        # Optimization: If we just ran brew upgrade, a restart ensures the new version is active
        print("  ♻️  Restarting postgresql to apply any upgrades...")
        execute(["brew", "services", "restart", "postgresql"])
        summary_data.append(("postgres_service", "Restarted/Running", "✅"))

# G. Final System Configs
print("🔧 Configuring Git...")
execute(["git", "config", "--global", "core.excludesfile", "~/.config/git/ignore"])
execute(["git", "config", "--global", "core.editor", "code --wait"])
summary_data.append(("git_configs", "global settings", "✅"))

# ---------------------------------------------------------
# FINAL SUMMARY REPORT
# ---------------------------------------------------------

print("\n" + "=" * 77)
print(f"{'Item':<25} | {'Destination/Action':<40} | {'Status'}")
print("-" * 77)
for item, dest, stat in summary_data:
    display_path = dest.replace(str(Path.home()), "~")
    if len(display_path) > 37:
        display_path = display_path[:37] + "..."
    print(f"{item:<25} | {display_path:<40} | {stat}")
print("=" * 77)
print("\n✨ Environment sync complete!\n")
