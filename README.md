# nvim-manager

nvim-manager manages Neovim configurations by leveraging `NVIM_APPNAME` and
putting your dotfiles configuration in `~/.config/nvim/`.

## Why

Your dotfiles change a lot, sometimes it's hard to manage all of the places you
have installed them and potentially made hand edits to.  `nvim-manager` allows
you to easily make static releases of your dotfiles, and keep your nvim install
from breaking by leveraging `NVIM_APPNAME` and pinned releases of your dotfiles
stored in `~/.config`.  In this directory you might have many nvim
configurations installed, `nvim-manager` automates the process of installing
and updating from your dotfiles, while keeping previous pinned versions untouched.

``` bash
~/.config
    ├── nvim # default nvim directory
    ├── lazyvim # another nvim distribution
    ├── nvim-waylonwalker-0.0.1 # pinned release managed by nvim-manager
    ├── nvim-waylonwalker-0.0.2 # pinned release managed by nvim-manager
    └── nvim-waylonwalker-0.0.3 # pinned release managed by nvim-manager
```

## Installation

You can install nvim-manager using one of these methods:

> !nvim-manager note requires [uv](https://docs.astral.sh/uv/getting-started/installation/) to be installed

### Using i.jpillora.com (recommended)

```bash
curl https://i.jpillora.com/waylonwalker/nvim-manager | bash
```

### Direct install script

```bash
# Download and run the latest install script
curl -fsSL https://github.com/waylonwalker/nvim-manager/releases/latest/download/install.sh | bash
```

### Manual download

You can also manually download the archive for your platform from the releases page:

- [x86_64-unknown-linux-gnu](https://github.com/waylonwalker/nvim-manager/releases/download/v{version}/nvim-manager-{version}-x86_64-unknown-linux-gnu.tar.gz)
- [aarch64-unknown-linux-gnu](https://github.com/waylonwalker/nvim-manager/releases/download/v{version}/nvim-manager-{version}-aarch64-unknown-linux-gnu.tar.gz)"""

## Setup

`nvim-manager` is a command-line tool for managing Neovim configurations ran
with [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
# Add the following lines to your .bashrc or .zshrc

# Your dotfiles repository
export NVIM_MANAGER_REPO=https://github.com/WaylonWalker/devtainer

# path to your nvim configuration inside the dotfiles repository
export NVIM_CONFIG_PATH=nvim/.config/nvim

# Where to install your configuration
# Using `~/.config` by default allows you to use NVIM_APPNAME
export NVIM_MANAGER_INSTALL_DIR=$HOME/.config

# Prefix name for your configuration
export NVIM_MANAGER_PREFIX="nvim-waylonwalker-"

# current version that you want to open nvim with
export NVIM_APPNAME=$NVIM_MANAGER_PREFIX-0.0.1
```

## Command Line Usage

### Main Command

```
                                                                                                                                                                                                                                       
 Usage: nvim-manager.py [OPTIONS] COMMAND [ARGS]...                                                                                                                                                                                    
                                                                                                                                                                                                                                       
 nvim-manager manages Neovim configurations by leveraging NVIM_APPNAME.                                                                                                                                                                
                                                                                                                                                                                                                                       
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --list                -l        List available versions                                                                                                                                                                             │
│ --version             -v        Show version                                                                                                                                                                                        │
│ --install-completion            Install completion for the current shell.                                                                                                                                                           │
│ --show-completion               Show completion for the current shell, to copy it or customize the installation.                                                                                                                    │
│ --help                          Show this message and exit.                                                                                                                                                                         │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ list      List available tags/branches and highlight installed ones.                                                                                                                                                                │
│ install   Install a specific version of Neovim configuration by tag or branch.                                                                                                                                                      │
│ update    Update a specific version by reinstalling it.                                                                                                                                                                             │
│ version   Show the version of nvim-manager.                                                                                                                                                                                         │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

### Subcommand: install

```
                                                                                                                                                                                                                                       
 Usage: nvim-manager.py install [OPTIONS] [VERSION]                                                                                                                                                                                    
                                                                                                                                                                                                                                       
 Install a specific version of Neovim configuration by tag or branch.                                                                                                                                                                  
 Example: NVIM_APPNAME=waylonwalker-nvim-0.0.1 nvim                                                                                                                                                                                    
                                                                                                                                                                                                                                       
╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   version      [VERSION]  Version to install [default: None]                                                                                                                                                                        │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --distro               TEXT  Install a specific Neovim distribution [default: None]                                                                                                                                                 │
│ --pick                       Fuzzy pick a version to install                                                                                                                                                                        │
│ --pick-distro                Fuzzy pick a distro to install                                                                                                                                                                         │
│ --repo-url             TEXT  Git repository URL [default: None]                                                                                                                                                                     │
│ --config-path          TEXT  Path to nvim config in repository [default: None]                                                                                                                                                      │
│ --prefix               TEXT  Prefix for the installation directory [default: None]                                                                                                                                                  │
│ --force        -f            Force install even if already exists                                                                                                                                                                   │
│ --help                       Show this message and exit.                                                                                                                                                                            │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

### Subcommand: list

```
                                                                                                                                                                                                                                       
 Usage: nvim-manager.py list [OPTIONS]                                                                                                                                                                                                 
                                                                                                                                                                                                                                       
 List available tags/branches and highlight installed ones.                                                                                                                                                                            
                                                                                                                                                                                                                                       
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --distro        TEXT  List versions for a specific Neovim distribution [default: None]                                                                                                                                              │
│ --help                Show this message and exit.                                                                                                                                                                                   │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

### Subcommand: update

```
                                                                                                                                                                                                                                       
 Usage: nvim-manager.py update [OPTIONS] VERSION                                                                                                                                                                                       
                                                                                                                                                                                                                                       
 Update a specific version by reinstalling it.                                                                                                                                                                                         
 Args:     version: The version to update                                                                                                                                                                                              
                                                                                                                                                                                                                                       
╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    version      TEXT  [default: None] [required]                                                                                                                                                                                  │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                                                                                                         │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

### Subcommand: version

```
                                                                                                                                                                                                                                       
 Usage: nvim-manager.py version [OPTIONS]                                                                                                                                                                                              
                                                                                                                                                                                                                                       
 Show the version of nvim-manager.                                                                                                                                                                                                     
                                                                                                                                                                                                                                       
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                                                                                                         │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```
