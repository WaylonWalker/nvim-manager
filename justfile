delete-tag:
    #!/usr/bin/env bash
    set -euo pipefail
    
    # Get the version
    VERSION=$(cat version)
    
    # Delete the tag
    git tag -d "v$VERSION"
    git push origin ":refs/tags/v$VERSION"

delete-release:
    #!/usr/bin/env bash
    set -euo pipefail
    
    # Get the version
    VERSION=$(cat version)
    
    # Delete the release
    gh release delete "v$VERSION"

create-tag:
    #!/usr/bin/env bash
    VERSION=$(cat version)
    git tag -a "v$VERSION" -m "Release v$VERSION"
    git push origin "v$VERSION"

create-archives:
    #!/usr/bin/env bash
    VERSION=$(cat version)
    rm -rf dist build
    mkdir -p dist
    
    # Create the binary for each platform
    for platform in "x86_64-unknown-linux-gnu" "aarch64-unknown-linux-gnu"; do
        outdir="nvim-manager-${VERSION}-${platform}"
        mkdir -p "dist/${outdir}"
        
        # Copy the Python script and update version
        cp nvim-manager.py "dist/${outdir}/nvim-manager.py"
        sed -i "s/NIGHTLY/${VERSION}/" "dist/${outdir}/nvim-manager.py"
        
        cd dist
        tar czf "${outdir}.tar.gz" "${outdir}"
        sha256sum "${outdir}.tar.gz" > "${outdir}.tar.gz.sha256"
        cd ..
    done
    
    # Generate install.sh
    ./scripts/generate_install_script.py "$VERSION"
    chmod +x dist/install.sh

create-release: create-tag create-archives
    #!/usr/bin/env bash
    VERSION=$(cat version)
    ./scripts/get_release_notes.py "$VERSION" > release_notes.tmp
    gh release create "v$VERSION" \
        --title "v$VERSION" \
        --notes-file release_notes.tmp \
        dist/nvim-manager-${VERSION}-x86_64-unknown-linux-gnu.tar.gz \
        dist/nvim-manager-${VERSION}-x86_64-unknown-linux-gnu.tar.gz.sha256 \
        dist/nvim-manager-${VERSION}-aarch64-unknown-linux-gnu.tar.gz \
        dist/nvim-manager-${VERSION}-aarch64-unknown-linux-gnu.tar.gz.sha256 \
        dist/install.sh
    rm release_notes.tmp

preview-release-notes:
    #!/usr/bin/env bash
    VERSION=$(cat version)
    ./scripts/get_release_notes.py "$VERSION" | less -R

release: create-release
