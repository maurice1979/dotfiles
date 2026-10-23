"""Dotfiles: symlinks and post-install configuration, run by `homely update`.

Installing software is the Brewfile's job (`bootstrap.sh` runs `brew bundle` before
homely). homely runs commands without a TTY, so installs that prompt for sudo fail
here, and an install step failing halfway leaves the symlinks half done. This file
only links files and checks what still needs a manual step.
"""

import shutil
from pathlib import Path

from homely.files import mkdir, symlink

HOME = Path.home()

# 1. Dotfiles symlinks: repo path -> target
DOTFILES = {
    "Brewfile": "~/.Brewfile",  # so `brew bundle --global` / `brew bundle check --global` work anywhere
    "starship.toml": "~/.config/starship.toml",
    ".zshrc": "~/.zshrc",
    "vscode/settings.json": "~/Library/Application Support/Code/User/settings.json",
    "git/config": "~/.config/git/config",
    "git/ignore": "~/.config/git/ignore",
    "ssh/config": "~/.ssh/config",
    "ipython/00-first.py": "~/.ipython/profile_default/startup/00-first.py",
}

SSH_KEY = HOME / ".ssh/id_ed25519"
# Globbed so the (public) repo names neither the Google account nor the database file;
# the middle * is the localised "My Drive" folder (e.g. "Mi unidad").
KEEPASS_DB_GLOB = "Library/CloudStorage/GoogleDrive-*/*/keypass/*.kdbx"

summary: list[tuple[str, str, str]] = []

# ---------------------------------------------------------
# A. Symlinks (parent dirs first: a fresh machine has none of them)
# ---------------------------------------------------------
# ssh refuses keys in a group/world-readable ~/.ssh, so create it 0700 ourselves.
(HOME / ".ssh").mkdir(mode=0o700, exist_ok=True)

repo = Path(__file__).parent
for src, dest in DOTFILES.items():
    parent = Path(dest).expanduser().parent
    for d in reversed([parent, *parent.parents]):
        if d != HOME and HOME in d.parents:
            mkdir(str(d))
    if not (repo / src).exists():
        summary.append((src, dest, "❌ source missing"))
        continue
    # homely refuses to replace an existing file (AssertionError), and installers
    # sometimes create one first (e.g. a default ~/.zshrc): move it aside instead.
    target, status = Path(dest).expanduser(), "✅"
    if target.is_symlink() and target.resolve() == (repo / src).resolve():
        pass
    elif target.exists() or target.is_symlink():
        target.rename(target.with_name(target.name + ".pre-dotfiles"))
        status = "✅ (old file kept as .pre-dotfiles)"
    symlink(src, dest)
    summary.append((src, dest, status))

# ---------------------------------------------------------
# B. Checks: things neither the Brewfile nor homely can do for you
# ---------------------------------------------------------
# git/config signs every commit with this key; without it `git commit` fails.
if SSH_KEY.exists():
    summary.append(("ssh key", "~/.ssh/id_ed25519", "✅"))
else:
    summary.append(("ssh key", "~/.ssh/id_ed25519", "⚠️  restore it (commits fail)"))

for binary in ("brew", "code", "starship", "psql", "uv"):
    summary.append((binary, "on PATH", "✅" if shutil.which(binary) else "⚠️  missing (run brew bundle)"))

if any(HOME.glob(KEEPASS_DB_GLOB)):
    summary.append(("keepass db", "Google Drive", "✅"))
else:
    summary.append(("keepass db", "Google Drive", "⚠️  sign in to Google Drive"))

# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------
print("\n" + "=" * 77)
print(f"{'Item':<25} | {'Destination/Action':<40} | Status")
print("-" * 77)
for item, dest, stat in summary:
    shown = dest.replace(str(HOME), "~")
    if len(shown) > 37:
        shown = shown[:37] + "..."
    print(f"{item:<25} | {shown:<40} | {stat}")
print("=" * 77)
print("\n✨ Dotfiles sync complete!\n")
