# CashuArcade

A pygame-based arcade launcher for macOS that runs Python games with a shared virtual environment.

## Features

- 🎮 Game launcher with visual menu
- 📦 Games organized in GAMES/ directory
- ⚙️ Manifest-based game configuration
- 🖼️ Screenshot display for each game
- 🎨 Shared gamelib for common functionality
- 🐍 Single shared virtual environment for simplicity

## Quick Start

### 1. Setup Configuration

```bash
# Copy sample config
cp config.env.sample config.env

# Edit if needed (optional)
nano config.env
```

### 2. Setup Virtual Environment

```bash
# Create shared venv
python3 -m venv venv

# Activate and install dependencies
source venv/bin/activate
pip install -r requirements.txt

# Install gamelib and games
pip install -e ./gamelib
pip install -e ./GAMES/fishyfrens
```

### 3. Run the Launcher

```bash
# Use the launcher script
./arcade

# Or manually
source venv/bin/activate
python -m lnarcade
```

## Project Structure

```
CashuArcade/
├── arcade                  # Launcher script
├── fishy                   # Direct game launcher script
├── config.env              # Configuration (copy from config.env.sample)
├── config.env.sample       # Sample configuration
├── venv/                   # Shared virtual environment
├── lnarcade/               # Launcher code
├── gamelib/                # Shared game library
├── GAMES/                  # Games directory
│   ├── fishyfrens/        # Example game
│   │   ├── manifest.json  # Game metadata
│   │   ├── setup.py       # Package setup
│   │   └── ...
│   └── testgame/          # Another game
└── docs/                   # Documentation
```

## Creating a New Game

See [docs/MANIFEST_GUIDE.md](docs/MANIFEST_GUIDE.md) for detailed instructions.

Quick version:

```bash
# 1. Create game directory
cd GAMES
mkdir mygame && cd mygame

# 2. Create game package structure
mkdir mygame
touch mygame/__init__.py mygame/__main__.py

# 3. Create setup.py
cat > setup.py << 'EOF'
from setuptools import setup
setup(
    name="mygame",
    version="1.0.0",
    packages=["mygame"],
    package_dir={"mygame": "."},
    install_requires=["pygame"],
)
EOF

# 4. Create manifest.json
# Set "venv": null to use shared venv

# 5. Add screenshot.png

# 6. Install and test
cd ../..
source venv/bin/activate
pip install -e ./GAMES/mygame
python -m mygame
```

## Documentation

See the `docs/` directory for detailed documentation:

- **[MANIFEST_GUIDE.md](docs/MANIFEST_GUIDE.md)** - How to create game manifests
- **[GAMELIB_INTEGRATION.md](docs/GAMELIB_INTEGRATION.md)** - Using gamelib in your games
- **[GAMES/README.md](GAMES/README.md)** - Games directory overview

## Configuration

Edit `config.env`:

```bash
# Enable debug logging
DEBUG=False

# Free play mode (no coins)
FREE_PLAY=True

# Auto-scroll timeout (seconds)
AFK_SCROLL_TIME=300

# Custom game search paths
# LNARCADE_GAME_PATHS=~/Games:~/MoreGames
```

## Controls

- **↑/↓** - Navigate games
- **Enter** - Launch game
- **Escape** - Quit launcher

## Requirements

- Python 3.9+
- pygame
- python-dotenv

See `requirements.txt` for full list.

## Resources

- [Pygame Documentation](https://www.pygame.org/docs/)
- [Pygame Tutorial](https://www.pygame.org/docs/tut/newbieguide.html)
- [Pygame Games](https://www.pygame.org/tags/all)















> trying to run the python application

myca@jupiter LNApps % ./fishy
./fishy: fork: Resource temporarily unavailable
myca@jupiter LNApps % ./fishy
__vsc_command_output_start:2: fork failed: resource temporarily unavailable
zsh: fork failed: resource temporarily unavailable
__vsc_update_cwd:1: fork failed: resource temporarily unavailable    


> running any command in VS Code terminal (it works but shows:)

__vsc_command_output_start:2: fork failed: resource temporarily unavailable

> Opening a new terminal:

[forkpty: Resource temporarily unavailable]
[Could not create a new process and open a pseudo-tty.]

---

# check running processes
ps aux | wc -l

# check for zombie processes
ps aux | grep 'Z'

1. A zombie process will have a 'Z' in the 'STAT' column.

`htop` or `top`

---

appears the cause of the issue is the rsync-sync extension for VS Code

Solution: comment out .vscode/settings.json

Here are the contents for backup:

```json
{
    "sync-rsync.remote": "satoshi@lnarcade.local:/home/satoshi/LNApps/",
    "sync-rsync.onSave": true,
    "sync-rsync.onSaveIndividual": true,
    "sync-rsync.options": [],
    "sync-rsync.sites": [],
    "sync-rsync.notification": false
}
```


### INSTALLING

>> DEPRECATED!!

```sh
sudo apt-get install -y git pip
git clone https://github.com/PlebeiusGaragicus/arcade-game-menu.git
git clone https://github.com/PlebeiusGaragicus/arcade-apps.git
cd arcade-game-menu
pip install .
```


## Manifests

Each game (or app) needs a manifest.  Here is an example:

```json
{
    "launcher": {
        "name": "My Awesome Game",
        "description": "A brief description of your game",
        "author": "Your Name",
        "version": "1.0.0",
        "type": "pygame",
        "screenshot": "screenshot.png",
        "launch": {
            "command": "python",
            "args": ["-m", "mygame"],
            "venv": ".venv",
            "cwd": "."
        }
    },
    "game_config": {
        "debug": false
    }
}
```