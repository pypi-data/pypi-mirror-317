#!/bin/bash

# Colors
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

echo -e "${GREEN}Installing SPARC CLI dependencies...${NC}"

# Change to the sparc_cli directory
cd "$SCRIPT_DIR"

# Install aider-chat and sparc-cli in development mode
pip install aider-chat
pip install -e .

# Install ripgrep if not present
if ! command -v rg &> /dev/null; then
    if command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y ripgrep
    elif command -v yum &> /dev/null; then
        sudo yum install -y ripgrep
    elif command -v brew &> /dev/null; then
        brew install ripgrep
    else
        echo "Please install ripgrep manually: https://github.com/BurntSushi/ripgrep#installation"
    fi
fi

echo -e "\n${GREEN}Installation complete!${NC}"
echo -e "You can now use sparc. Try: sparc --help"
