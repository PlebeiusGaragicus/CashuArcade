# Games Directory

This directory contains all the games for CashuArcade.

## Structure

Each game is in its own subdirectory with:
- `manifest.json` - Game metadata and launch configuration
- `setup.py` - Python package setup (for installation)
- Game code and resources

## Current Games

- **fishyfrens** - Your Frens are Fishy! - An underwater adventure
- **testgame** - Smack the Cat! - Test game

## Adding a New Game

1. Create a new directory in `GAMES/`
2. Add your game code with `__init__.py` and `__main__.py`
3. Create `setup.py` for package installation
4. Create `manifest.json` with game metadata
5. Install the game: `pip install -e ./GAMES/yourgame`

See the existing games for examples.

## Installation

All games are installed as editable packages in the shared `venv`:

```bash
cd ~/Downloads/CashuArcade
source venv/bin/activate
pip install -e ./GAMES/fishyfrens
```

## Running Games

### From the launcher:
```bash
./arcade
```

### Directly:
```bash
source venv/bin/activate
cd GAMES/fishyfrens
python -m fishyfrens
```
