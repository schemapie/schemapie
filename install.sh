#!/bin/sh
set -e

REPO="git+https://github.com/schemAPIe/schemapie.git"

cat <<'EOF' 
Welcome to the schemAPIe Installer! Thank you for your support.
                 (
           (   )    )
            )    (  (
       __________________
  ____/   .     .     .  \____
 /    .      /  |  \     .    \
:___     .            .     ___:
 \  \_______  .  .  _______/  /
  \         \______/         /
   \.                      ./
     \____________________/
EOF

echo "For user safety, the schemAPIe installation script will not automatically install dependencies. This script will instead inform you of any missing dependencies that you will need to manually install."
echo "Installing schemapie from GitHub..."

exit 1

deps=true

# Check for python
if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
else
  echo "Python3 is required. Install Python3 here: https://www.python.org/downloads/"
  deps=false
fi

# Check for git
if ! command -v git >/dev/null 2>&1; then
  echo "Git is required. Install Git here: https://git-scm.com/install/"
  deps=false
fi

# Check for pipx
if ! command -v pipx >/dev/null 2>&1; then
  echo "pipx is required. Install pipx here: https://pipx.pypa.io/stable/how-to/install-pipx/"
  deps=false
fi

if [ "$deps" = false ]; then
  echo "Machine is missing dependencies. Check logs for installation requirements."
  echo "Exiting..."
  exit 1
fi

# Install package
pipx install "$REPO" || pipx upgrade schemapie

echo "Installed! Restart your terminal then test the installtion by using: spi --version"