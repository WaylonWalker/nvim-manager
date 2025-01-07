#!/usr/bin/env -S uv run --
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "typer",
#     "gitpython",
#     "rich"
# ]
# ///

from git import Repo
import os
from pathlib import Path
from rich.console import Console
from rich.table import Table
import shutil
import typer

app = typer.Typer()
console = Console()

GITHUB_REPO = os.getenv("NVIM_GITHUB_REPO", "https://github.com/waylonwalker/devtainer")
NVIM_CONFIG_PATH = os.getenv("NVIM_CONFIG_PATH", "nvim/.config/nvim")
INSTALL_DIR = Path(os.getenv("NVIM_INSTALL_DIR", Path.home() / ".config"))
PREFIX = os.getenv("NVIM_PREFIX", "nvim-waylonwalker-")


@app.command()
def install(version: str):
    """Install a specific version of Neovim configuration by tag or branch.

    You can use the installed version with:

    NVIM_APPNAME=<appname> nvim

    Example:
    NVIM_APPNAME=waylonwalker-nvim-0.0.1 nvim
    """
    target_dir = INSTALL_DIR / f"{PREFIX}{version}"
    if target_dir.exists():
        console.print(f"[yellow]Version '{version}' is already installed.[/yellow]")
        return

    console.print(f"Cloning version '{version}'...")
    with console.status(f"Cloning {version}..."):
        temp_dir = INSTALL_DIR / "temp-nvim-config"
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

        Repo.clone_from(GITHUB_REPO, temp_dir, branch=version)
        source_dir = temp_dir / NVIM_CONFIG_PATH
        if not source_dir.exists():
            console.print(
                f"[red]Configuration path '{NVIM_CONFIG_PATH}' not found in '{version}'.[/red]"
            )
            shutil.rmtree(temp_dir)
            raise typer.Exit(code=1)

        shutil.move(str(source_dir), str(target_dir))
        shutil.rmtree(temp_dir)

    console.print(
        f"[green]Version '{version}' installed successfully at {target_dir}.[/green]"
    )


@app.command()
def list_versions():
    """List available tags/branches and highlight installed ones."""
    console.print("Fetching available versions...")
    repo = Repo.clone_from(GITHUB_REPO, INSTALL_DIR / "temp-nvim-config", depth=1)
    tags = [tag.name for tag in repo.tags]
    branches = [
        branch.name.split("/")[-1]
        for branch in repo.remote().refs
        if branch.name != "HEAD"
    ]

    table = Table(title="Available Versions")
    table.add_column("Version", style="cyan")
    table.add_column("Installed", style="green")

    installed_versions = {
        p.name.replace(PREFIX, "")
        for p in INSTALL_DIR.iterdir()
        if p.name.startswith(PREFIX)
    }

    for version in sorted(tags + branches):
        installed = "Yes" if version in installed_versions else "No"
        table.add_row(version, installed)

    console.print(table)
    shutil.rmtree(INSTALL_DIR / "temp-nvim-config")


@app.command()
def update():
    """Update mutable branch-based versions."""
    installed_dirs = [p for p in INSTALL_DIR.iterdir() if p.name.startswith(PREFIX)]

    for installed_dir in installed_dirs:
        version = installed_dir.name.replace(PREFIX, "")
        repo = Repo(installed_dir)

        if not repo.head.is_detached:
            console.print(f"Updating version '{version}'...")
            with console.status(f"Updating {version}..."):
                repo.remote().pull()
            console.print(f"[green]Version '{version}' updated successfully.[/green]")
        else:
            console.print(
                f"[yellow]Version '{version}' is based on a tag and cannot be updated.[/yellow]"
            )


if __name__ == "__main__":
    app()
#!/usr/bin/env -S uv run --script
