#!/bin/bash
# Setup script for CashuArcade virtual environments

set -e  # Exit on error

ARCADE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_CMD="${PYTHON_CMD:-python3}"

echo "=========================================="
echo "CashuArcade Virtual Environment Setup"
echo "=========================================="
echo "Root: $ARCADE_ROOT"
echo "Python: $PYTHON_CMD"
echo ""

# Setup launcher venv
echo "1. Setting up launcher venv..."
if [ -d "$ARCADE_ROOT/.venv_launcher" ]; then
    echo "   ✓ Launcher venv already exists"
else
    echo "   Creating .venv_launcher..."
    $PYTHON_CMD -m venv "$ARCADE_ROOT/.venv_launcher"
    echo "   Installing launcher dependencies..."
    source "$ARCADE_ROOT/.venv_launcher/bin/activate"
    pip install --upgrade pip
    pip install -r "$ARCADE_ROOT/requirements.txt"
    deactivate
    echo "   ✓ Launcher venv created"
fi
echo ""

# Setup game venvs
echo "2. Setting up game venvs..."
for game_dir in "$ARCADE_ROOT"/*/; do
    game_name=$(basename "$game_dir")
    
    # Skip non-game directories
    if [[ "$game_name" == "lnarcade" ]] || \
       [[ "$game_name" == "gamelib" ]] || \
       [[ "$game_name" == "resources" ]] || \
       [[ "$game_name" == "TESTING" ]] || \
       [[ "$game_name" == ".git" ]] || \
       [[ "$game_name" == "venv"* ]] || \
       [[ "$game_name" == ".venv"* ]]; then
        continue
    fi
    
    # Check if it has a manifest
    if [ ! -f "$game_dir/manifest.json" ]; then
        continue
    fi
    
    echo "   Processing: $game_name"
    
    # Check if venv already exists
    if [ -d "$game_dir/.venv" ]; then
        echo "     ✓ venv already exists"
    else
        echo "     Creating .venv..."
        $PYTHON_CMD -m venv "$game_dir/.venv"
        
        # Install requirements if they exist
        if [ -f "$game_dir/requirements.txt" ]; then
            echo "     Installing dependencies..."
            source "$game_dir/.venv/bin/activate"
            pip install --upgrade pip
            pip install -r "$game_dir/requirements.txt"
            deactivate
            echo "     ✓ Dependencies installed"
        else
            echo "     ⚠ No requirements.txt found"
        fi
        
        echo "     ✓ venv created"
    fi
done
echo ""

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To run the launcher:"
echo "  source .venv_launcher/bin/activate"
echo "  python -m lnarcade"
echo ""
echo "To develop a game:"
echo "  cd <gamename>"
echo "  source .venv/bin/activate"
echo "  python -m <gamename>"
echo ""
