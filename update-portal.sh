#!/bin/bash
# Quick portal update script
# Usage: ./update-portal.sh [client-folder]

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ -z "$1" ]; then
    echo "Updating all client portals..."
    python3 "$SCRIPT_DIR/generate-portal.py" --all
else
    echo "Updating portal for: $1"
    python3 "$SCRIPT_DIR/generate-portal.py" "$1"
fi

echo ""
echo "Done! To deploy, run:"
echo "  cd $SCRIPT_DIR && git add . && git commit -m 'Update portal' && git push"
