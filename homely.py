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

# 2. Ensure Directories Exist
config_dirs = ["~/.config", "~/Library/Application Support/Code/User"]
for d in config_dirs:
    mkdir(d)

# 3. Processing Loop
for item, config in DOTFILES_DICT.items():
    print(f"📦 Processing {item}...")

    # A. Dependency Handling
    binary = config.get("bin")
    if binary and not shutil.which(binary):
        install_cmd = config.get("install_cmd")
        if install_cmd:
            print(f"  🚀 Installing {item}...")
            # Use brew check or direct execution
            execute(install_cmd.split())
        else:
            print(f"  ⚠️ Warning: {binary} not found.")
    elif binary:
        print(f"  ✅ {binary} is already present.")

    # B. Symlinking
    src = Path(__file__).parent / config["from"]
    if src.exists():
        # Note: homely's symlink handles ~ in the 'to' path automatically
        symlink(config["from"], config["to"])
    else:
        print(f"  ❌ Error: Source {src} not found! Check filenames.")

# 4. Global Python Tools via uv
# We use shutil.which to find uv; if not, we check common install locations
uv_path = shutil.which("uv") or Path.home() / ".local/bin/uv"
if uv_path:
    python_tools = ["black", "ruff", "mypy"]
    for tool in python_tools:
        print(f"🐍 Ensuring {tool} via uv...")
        execute([str(uv_path), "tool", "install", tool])

print("\n✨ Environment sync complete!")


# 1. Register the Global Git Ignore
# We point Git to the symlink we created earlier in the script
execute(["git", "config", "--global", "core.excludesfile", "~/.config/git/ignore"])

# 2. Set VS Code as the default Git editor
execute(["git", "config", "--global", "core.editor", "code --wait"])
