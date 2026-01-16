import shutil
from pathlib import Path

from homely.files import mkdir, symlink
from homely.system import execute

# 1. Configuration Dictionary
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

# Track results for the final summary
summary_data = []

# 2. Ensure Directories Exist
config_dirs = ["~/.config", "~/Library/Application Support/Code/User", "~/.config/git"]
for d in config_dirs:
    mkdir(d)

# 3. Processing Loop
for item, config in DOTFILES_DICT.items():
    print(f"📦 Processing {item}...")
    status = "✅"

    # A. Dependency Handling
    binary = config.get("bin")
    if binary and not shutil.which(binary):
        install_cmd = config.get("install_cmd")
        if install_cmd:
            print(f"  🚀 Installing {item}...")
            execute(install_cmd.split())
        else:
            print(f"  ⚠️ Warning: {binary} not found.")
            status = "⚠️  No Bin"
    elif binary:
        print(f"  ✅ {binary} is already present.")

    # B. Symlinking
    src = Path(__file__).parent / config["from"]
    if src.exists():
        symlink(config["from"], config["to"])
    else:
        print(f"  ❌ Error: Source {src} not found!")
        status = "❌ Src Missing"

    summary_data.append((item, config["to"], status))

# 4. Global Python Tools via uv
uv_path = shutil.which("uv") or Path.home() / ".local/bin/uv"
if uv_path:
    python_tools = ["black", "ruff", "mypy"]
    print(f"🐍 Syncing Python tools...")
    for tool in python_tools:
        execute([str(uv_path), "tool", "install", tool])
    summary_data.append(("python_tools", "uv tool install", "✅"))

# 5. Git Configurations
print("🔧 Configuring Git...")
execute(["git", "config", "--global", "core.excludesfile", "~/.config/git/ignore"])
execute(["git", "config", "--global", "core.editor", "code --wait"])
summary_data.append(("git_configs", "global settings", "✅"))

# 6. Final Summary Report
print("\n" + "=" * 75)
print(f"{'Item':<20} | {'Destination Path':<40} | {'Status'}")
print("-" * 75)
for item, dest, stat in summary_data:
    # Clean tilde for display and truncate if too long
    display_path = dest.replace("/Users/jvidal", "~")
    if len(display_path) > 37:
        display_path = display_path[:37] + "..."

    print(f"{item:<20} | {display_path:<40} | {stat}")
print("=" * 75)
print("✨ Environment sync complete!\n")
