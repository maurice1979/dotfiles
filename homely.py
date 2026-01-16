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
}

# 2. Configuration: CLI Tools (Homebrew Formulae)
BREW_FORMULAE = [
    "duckdb",
    "ffmpeg",
    "gh",
    "jq",
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
    "rectangle",
    "slack",
    "spotify",
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

# 5. Configuration: Python Global Tools
PYTHON_TOOLS = ["black", "ruff", "mypy"]

# Track results for the final summary
summary_data = []

# ---------------------------------------------------------
# EXECUTION
# ---------------------------------------------------------

# A. Ensure Directories Exist
config_dirs = ["~/.config", "~/Library/Application Support/Code/User", "~/.config/git"]
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
        if not shutil.which(formula):
            print(f"  🚀 Installing {formula}...")
            execute(["brew", "install", formula])
            summary_data.append((formula, "brew install", "✅"))
        else:
            summary_data.append((formula, "brew install", "✅"))

# D. Process GUI Apps (Casks)
if shutil.which("brew") and platform.system() == "Darwin":
    print("🖥️  Syncing GUI Applications...")
    for cask in BREW_CASKS:
        app_search_name = cask.replace("-", " ").title()
        app_exists = any(Path("/Applications").glob(f"{app_search_name}*.app"))
        if not app_exists:
            print(f"  🚀 Installing {cask}...")
            execute(["brew", "install", "--cask", cask])
            summary_data.append((cask, "/Applications", "✅"))
        else:
            summary_data.append((cask, "/Applications", "✅"))

# E. Process VS Code Extensions
if shutil.which("code"):
    print("🔌 Syncing VS Code Extensions...")
    # Get list of installed exts to skip re-installing
    _, stdout, _ = execute(["code", "--list-extensions"], stdout=True)
    installed_exts = [line.lower() for line in stdout.decode().splitlines()]

    for ext in VSCODE_EXTS:
        if ext.lower() not in installed_exts:
            print(f"  🚀 Installing extension: {ext}...")
            execute(["code", "--install-extension", ext])
        summary_data.append((ext.split(".")[-1], "VS Code Ext", "✅"))

# F. Global Python Tools via uv
uv_path = shutil.which("uv") or Path.home() / ".local/bin/uv"
if uv_path:
    print("🐍 Syncing Python tools...")
    for tool in PYTHON_TOOLS:
        execute([str(uv_path), "tool", "install", tool])
    summary_data.append(("python_tools", "uv tool install", "✅"))

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
