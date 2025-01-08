#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# ///

import sys


def generate_install_script(version):
    with open("scripts/install.sh.template", "r") as f:
        template = f.read()

    script = template.replace("{{VERSION}}", version)

    with open("dist/install.sh", "w") as f:
        f.write(script)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: generate_install_script.py VERSION", file=sys.stderr)
        sys.exit(1)

    version = sys.argv[1]
    generate_install_script(version)
