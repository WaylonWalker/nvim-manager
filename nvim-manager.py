#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "rich>=13.9.4",
#     "typer>=0.15.1",
#     "gitpython>=3.1.44",
#     "pyfzf>=0.3.1",
# ]
# ///

from git import Repo
from git.exc import GitCommandError
import os
from pathlib import Path
from pyfzf.pyfzf import FzfPrompt
from rich.console import Console
from rich.table import Table
import shutil
import typer

app = typer.Typer()
console = Console()

NVIM_MANAGER_VERSION = "NIGHTLY"

NVIM_MANAGER_REPO = os.getenv(
    "NVIM_MANAGER_REPO",
    os.getenv("NVIM_MANAGER_GITHUB_REPO", "https://github.com/waylonwalker/devtainer"),
)
NVIM_MANAGER_PREFIX = os.getenv("NVIM_MANAGER_PREFIX", "nvim-waylonwalker")
NVIM_MANAGER_CONFIG_PATH = os.getenv("NVIM_MANGER_CONFIG_PATH", "nvim/.config/nvim")
INSTALL_DIR = Path(os.getenv("NVIM_MANAGER_INSTALL_DIR", Path.home() / ".config"))

DISTROS = {
    "LazyVim": {
        "name": "LazyVim",
        "url": "https://github.com/LazyVim/starter",
        "config_path": ".",
        "prefix": "lazyvim",
        "version": "main",
    },
    "kickstart": {
        "name": "kickstart",
        "url": "https://github.com/nvim-lua/kickstart.nvim",
        "config_path": ".",
        "prefix": "kickstart",
        "version": "master",
    },
    "NvChad": {
        "name": "NvChad",
        "url": "https://github.com/NvChad/NvChad",
        "config_path": ".",
        "prefix": "nvchad",
        "version": "v2.5",
    },
    "AstroNvim": {
        "name": "AstroNvim",
        "url": "https://github.com/AstroNvim/template",
        "config_path": ".",
        "prefix": "astro",
        "version": "main",
    },
    "LunarVim": {
        "name": "LunarVim",
        "url": "https://github.com/LunarVim/LunarVim",
        "config_path": ".",
        "prefix": "lunar",
        "version": "master",
    },
}


def get_versions(repo_url: str = None):
    """Get available versions from git tags."""
    try:
        # Create a temporary directory for cloning
        temp_dir = INSTALL_DIR / "temp-nvim-config"

        if temp_dir.exists():
            shutil.rmtree(temp_dir)

        # Clone the repo with --bare to get all tags
        repo = Repo.clone_from(repo_url or NVIM_MANAGER_REPO, temp_dir, bare=True)

        # Get all tags
        versions = []
        for tag in repo.tags:
            # if tag.name.startswith("v"):
            #     versions.append(tag.name[1:])  # Remove 'v' prefix
            # else:
            #     versions.append(tag.name)
            versions.append(tag.name)

        # Clean up
        shutil.rmtree(temp_dir)
        return sorted(versions, reverse=True)
    except Exception as e:
        console.print(f"[red]Error: Failed to fetch versions: {e}[/red]")
        return []


def print_versions(repo_url: str = None, prefix: str = None):
    """List available tags/branches and highlight installed ones."""
    console.print("Fetching available versions...")
    versions = get_versions(repo_url)
    if not versions:
        return

    prefix = prefix or NVIM_MANAGER_PREFIX
    console.print(f"REPO: {repo_url or NVIM_MANAGER_REPO}")
    console.print("Available Versions:")
    # table = Table(title="Available Versions")
    # table.add_column("Version")
    # table.add_column("Status")

    for version in versions:
        config_dir = INSTALL_DIR / f"{prefix}-{version}"
        status = "[green]Installed[/green]" if config_dir.exists() else ""
        console.print(f"  - {version} {status}")
        # table.add_row(f"{prefix}-{version}", status)

    for distro_name, info in DISTROS.items():
        if distro_name not in versions:
            config_dir = INSTALL_DIR / f"{info['prefix']}-{info['version']}"
            if config_dir.exists():
                console.print(
                    f"  - {info['prefix']}-{info['version']} [green]Installed[/green]"
                )
                # table.add_row(
                #     f'{info["prefix"]}-{info["version"]}', "[green]Installed[/green]"
                # )
            else:
                console.print(f"  - {info['prefix']}-{info['version']}")
                # table.add_row(f'{info["prefix"]}-{info["version"]}', "")

    # console.print(table)

    installed_nvims = [d.name for d in (Path.home() / ".local/share").glob("nvim-*")]
    console.print("")
    console.print("previously used NVIM_APPNAMES in ~/.local/share:")
    for installed_nvim in installed_nvims:
        if installed_nvim not in versions:
            console.print(f"  - {installed_nvim}")


def version_callback(value: bool):
    if value:
        console.print(f"[green]Version: {NVIM_MANAGER_VERSION}[/green]")
        raise typer.Exit()


def list_callback(value: bool):
    if value:
        print_versions()
        raise typer.Exit()


def get_installed_versions(prefix: str = None) -> list[str]:
    """Get list of installed versions for a given prefix."""
    prefix = prefix or NVIM_MANAGER_PREFIX
    versions = []
    for path in INSTALL_DIR.iterdir():
        if not path.is_dir():
            continue
        if path.name.startswith(f"{prefix}-"):
            version = path.name[len(f"{prefix}-") :]
            versions.append(version)
    return sorted(versions, reverse=True)


def pick_version(versions: list[str], distro_name: str = None) -> str:
    """Let user pick a version from a list."""
    if not versions:
        msg = "No versions installed"
        if distro_name:
            msg += f" for {distro_name}"
        console.print(f"[yellow]{msg}[/yellow]")
        raise typer.Exit(1)

    table = Table(title="Available Versions")
    table.add_column("#", style="cyan")
    table.add_column("Version")

    for i, version in enumerate(versions, 1):
        table.add_row(str(i), version)

    console.print(table)

    while True:
        try:
            choice = typer.prompt("Select version number")
            idx = int(choice) - 1
            if 0 <= idx < len(versions):
                return versions[idx]
            console.print("[red]Invalid selection. Please try again.[/red]")
        except ValueError:
            console.print("[red]Please enter a number.[/red]")


def pick_with_fzf(items: list[str], prompt: str = "Select: ") -> str:
    """Use fzf to pick from a list of items."""
    try:
        fzf = FzfPrompt()
        selected = fzf.prompt(items, '--prompt="' + prompt + '" --height=10')[0]
        return selected
    except (IndexError, Exception):
        return None


def install_config(
    version: str,
    repo_url: str,
    config_path: str = ".",
    prefix: str = None,
    force: bool = False,
    verbose: bool = False,
):
    """Install a specific configuration version."""
    prefix = prefix or NVIM_MANAGER_PREFIX
    install_dir = INSTALL_DIR / f"{prefix}-{version}"
    temp_dir = Path("/tmp") / "nvim-manager"

    if verbose:
        console.print(f"Repo URL: {repo_url}")
        console.print(f"branch: {version}")
        console.print(f"Config path in repository: {config_path}")
        console.print(f"Install directory on host: {install_dir}")

    if install_dir.exists() and not force:
        console.print(
            f"[yellow]Version '{version}' is already installed at {install_dir}[/yellow]"
        )
        console.print("Use --force to reinstall")
        raise typer.Exit(1)

    # Clone the repository to temp directory
    try:
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        if install_dir.exists():
            shutil.rmtree(install_dir)

        # Create install directory
        install_dir.mkdir(parents=True, exist_ok=True)

        # Clone to temp directory
        Repo.clone_from(
            repo_url,
            temp_dir,
            multi_options=[f"--branch={version}", "--single-branch", "--depth=1"],
        )

        # Use NVIM_MANAGER_CONFIG_DIR as the source directory within the repo
        source_dir = temp_dir / config_path
        if not source_dir.exists():
            console.print(
                f"[red]Error: Config directory '{config_path}' not found in repository[/red]"
            )
            raise typer.Exit(1)

        # Copy all files from source_dir to install_dir
        for item in source_dir.iterdir():
            if item.is_file():
                shutil.copy2(str(item), str(install_dir / item.name))
            else:
                shutil.copytree(str(item), str(install_dir / item.name))

        # Clean up temp directory
        shutil.rmtree(temp_dir)

        console.print(f"[green]Version '{version}' installed successfully![/green]")
        console.print("\nTo use this version, run:")
        console.print(f"[green]export NVIM_APPNAME={prefix}-{version}[/green]")

    except (GitCommandError, OSError) as e:
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        if install_dir.exists():
            shutil.rmtree(install_dir)
        console.print(f"[red]Error: Failed to install configuration: {e}[/red]")
        raise typer.Exit(1)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    list: bool = typer.Option(
        False, "--list", "-l", help="List available versions", callback=list_callback
    ),
    version: bool = typer.Option(
        False, "--version", "-v", help="Show version", callback=version_callback
    ),
):
    """
    nvim-manager manages Neovim configurations by leveraging NVIM_APPNAME.
    """
    if ctx.invoked_subcommand is None:
        ctx.get_help()


def get_distro(name: str) -> dict:
    """Get distro config by name (case insensitive)."""
    for distro_name, config in DISTROS.items():
        if distro_name.lower() == name.lower():
            return config
    console.print(f"[red]Error: Unknown distribution '{name}'[/red]")
    console.print(f"Available distributions: {', '.join(DISTROS.keys())}")
    raise typer.Exit(code=1)


@app.command("list")
def list_versions(
    distro: str = typer.Option(
        None, help="List versions for a specific Neovim distribution"
    ),
):
    """List available tags/branches and highlight installed ones."""
    if distro:
        distro_config = get_distro(distro)
        print_versions(repo_url=distro_config["url"], prefix=distro_config["prefix"])
    else:
        print_versions()


@app.command()
def install(
    version: str = typer.Argument(None, help="Version to install"),
    distro: str = typer.Option(
        None, "--distro", help="Install a specific Neovim distribution"
    ),
    pick: bool = typer.Option(False, "--pick", help="Fuzzy pick a version to install"),
    pick_distro: bool = typer.Option(
        False, "--pick-distro", help="Fuzzy pick a distro to install"
    ),
    repo_url: str = typer.Option(None, help="Git repository URL"),
    config_path: str = typer.Option(None, help="Path to nvim config in repository"),
    prefix: str = typer.Option(None, help="Prefix for the installation directory"),
    force: bool = typer.Option(
        False, "--force", "-f", help="Force install even if already exists"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
):
    """Install a specific version of Neovim configuration by tag or branch.

    Example:
    NVIM_APPNAME=waylonwalker-nvim-0.0.1 nvim
    """
    if verbose:
        import sys

        console.print(
            f"[green]Using nvim-manager version {NVIM_MANAGER_VERSION}[/green]"
        )
        console.print(
            f"[green]Using python version {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}[/green]"
        )
    if pick_distro:
        # Pick distro and use its configured version
        distro_name = pick_with_fzf(DISTROS.keys(), "Select distribution: ")
        if not distro_name:
            console.print("[yellow]No distribution selected[/yellow]")
            raise typer.Exit(1)

        distro_config = get_distro(distro_name)
        install_config(
            version=distro_config["version"],
            repo_url=distro_config["url"],
            config_path=distro_config["config_path"],
            prefix=distro_config["prefix"],
            force=force,
            verbose=verbose,
        )
        return

    if pick:
        versions = get_versions(repo_url or NVIM_MANAGER_REPO)
        selected_version = pick_with_fzf(versions, "Select version: ")
        if not selected_version:
            console.print("[yellow]No version selected[/yellow]")
            raise typer.Exit(1)
        version = selected_version

    if not version and not distro:
        console.print("[red]Error: Must specify either a version or --distro[/red]")
        console.print("\nExamples:")
        console.print("  nvim-manager install v1.0.0")
        console.print("  nvim-manager install --distro lazyvim")
        console.print("  nvim-manager install --pick")
        console.print("  nvim-manager install --pick-distro")
        raise typer.Exit(code=1)

    # If distro is specified, use the distro-specific installation
    if distro:
        distro_config = get_distro(distro)
        install_config(
            version=distro_config["version"],
            repo_url=distro_config["url"],
            config_path=distro_config["config_path"],
            prefix=distro_config["prefix"],
            force=force,
            verbose=verbose,
        )
        return

    # Install user config
    install_config(
        version=version,
        repo_url=repo_url or NVIM_MANAGER_REPO,
        config_path=config_path or NVIM_MANAGER_CONFIG_PATH or ".",
        prefix=prefix,
        force=force,
        verbose=verbose,
    )


@app.command()
def update(version: str):
    """Update a specific version by reinstalling it.

    Args:
        version: The version to update
    """
    target_dir = INSTALL_DIR / f"{NVIM_MANAGER_PREFIX}-{version}"
    if not target_dir.exists():
        console.print(f"[red]Version '{version}' is not installed.[/red]")
        raise typer.Exit(code=1)

    # Remove existing installation
    shutil.rmtree(target_dir)

    # Install the version again
    install(version)
    console.print(f"[green]Version '{version}' updated successfully.[/green]")


@app.command()
def version():
    """Show the version of nvim-manager."""
    console.print(f"[green]Version: {NVIM_MANAGER_VERSION}[/green]")


if __name__ == "__main__":
    app()
