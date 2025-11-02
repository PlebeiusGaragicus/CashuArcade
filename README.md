# CashuArcade

A pygame-based arcade launcher for macOS that runs Python games as submodules with isolated virtual environments.

## Features

- 🎮 Game launcher with visual menu
- 🔒 Isolated virtual environments per game
- 📦 Games as submodules in the same repository
- ⚙️ Manifest-based game configuration
- 🖼️ Screenshot display for each game
- 🎨 Shared gamelib for common functionality

## Quick Start

### 1. Setup Configuration

```bash
# Copy sample config
cp config.env.sample config.env

# Edit if needed (optional)
nano config.env
```

### 2. Setup Virtual Environments

```bash
# Automated setup (recommended)
./setup_venvs.sh

# Or manual setup
python3 -m venv .venv_launcher
source .venv_launcher/bin/activate
pip install -r requirements.txt
```

### 3. Run the Launcher

```bash
source .venv_launcher/bin/activate
python -m lnarcade
```

## Project Structure

```
CashuArcade/
├── config.env              # Configuration (copy from config.env.sample)
├── config.env.sample       # Sample configuration
├── .venv_launcher/         # Launcher virtual environment
├── lnarcade/               # Launcher code
├── gamelib/                # Shared game library
├── fishyfrens/             # Example game
│   ├── .venv/             # Game's virtual environment
│   ├── manifest.json      # Game metadata
│   └── ...
└── [other games]/          # Additional games
```

## Creating a New Game

See [MANIFEST_GUIDE.md](MANIFEST_GUIDE.md) for detailed instructions.

Quick version:

```bash
# 1. Create game directory
mkdir mygame && cd mygame

# 2. Setup venv
python3 -m venv .venv
source .venv/bin/activate
pip install pygame

# 3. Create manifest
cp ../lnarcade/manifest_template.json manifest.json
# Edit manifest.json

# 4. Create game code
mkdir mygame
touch mygame/__init__.py
touch mygame/__main__.py
# Add your game code

# 5. Add screenshot
# Add screenshot.png

# 6. Test
python -m mygame
```

## Documentation

- **[BREAKING_CHANGES.md](BREAKING_CHANGES.md)** - Migration guide from old structure
- **[MANIFEST_GUIDE.md](MANIFEST_GUIDE.md)** - How to create game manifests
- **[VENV_SETUP.md](VENV_SETUP.md)** - Virtual environment setup guide
- **[GAMELIB_INTEGRATION.md](GAMELIB_INTEGRATION.md)** - Using gamelib in your games
- **[REFACTOR_SUMMARY.md](REFACTOR_SUMMARY.md)** - Technical details of recent refactor

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