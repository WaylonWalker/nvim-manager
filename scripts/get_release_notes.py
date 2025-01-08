#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# ///

import subprocess
import sys


def get_release_notes(version):
    with open("CHANGELOG.md", "r") as f:
        content = f.read()

    sections = content.split("\n## ")
    # First section won't start with ## since it's split on that
    sections = ["## " + s if i > 0 else s for i, s in enumerate(sections)]

    for section in sections:
        if section.startswith(f"## {version}"):
            install_instructions = f"""## Installation

You can install nvim-manager using one of these methods:

> !nvim-manager note requires [uv](https://docs.astral.sh/uv/getting-started/installation/) to be installed

### Using i.jpillora.com (recommended)
```bash
curl https://i.jpillora.com/waylonwalker/nvim-manager | bash
```

### Direct install script
```bash
curl -fsSL https://github.com/waylonwalker/nvim-manager/releases/download/v{version}/install.sh | bash
```

### Manual download
You can also manually download the archive for your platform from the releases page:
- [x86_64-unknown-linux-gnu](https://github.com/waylonwalker/nvim-manager/releases/download/v{version}/nvim-manager-{version}-x86_64-unknown-linux-gnu.tar.gz)
- [aarch64-unknown-linux-gnu](https://github.com/waylonwalker/nvim-manager/releases/download/v{version}/nvim-manager-{version}-aarch64-unknown-linux-gnu.tar.gz)"""

            # Get help output
            try:
                help_output = subprocess.check_output(
                    ["./nvim-manager.py", "--help"],
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                )
                return f"{section.strip()}\n\n{install_instructions.format(version=version)}\n\n## Command Line Usage\n\n```\n{help_output}```"
            except subprocess.CalledProcessError as e:
                return f"{section.strip()}\n\n{install_instructions.format(version=version)}\n\n## Command Line Usage\n\nError getting help: {e.output}"

    return None


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: get_release_notes.py VERSION", file=sys.stderr)
        sys.exit(1)

    version = sys.argv[1]
    notes = get_release_notes(version)
    if notes:
        print(notes)
    else:
        print(f"Error: No release notes found for version {version}", file=sys.stderr)
        sys.exit(1)
