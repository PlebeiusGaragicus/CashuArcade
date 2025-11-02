# Virtual Environment Setup Guide

## Overview

CashuArcade uses a **single shared virtual environment** (`.venv_launcher`) for the launcher and all games to simplify dependency management.

## Directory Structure

```
CashuArcade/
├── .venv_launcher/          # Shared venv for launcher and all games
├── lnarcade/                # Launcher code
├── gamelib/                 # Shared library (installed in .venv_launcher)
├── fishyfrens/              # Game code (installed in .venv_launcher)
│   ├── manifest.json
│   ├── setup.py
│   └── ...
├── testgame/                # Game code
│   ├── manifest.json
│   └── ...
└── requirements.txt         # All dependencies
```

## Why Single Venv?

1. **Simplicity**: One environment to manage
2. **Easy Setup**: Install once, run everything
3. **Shared Dependencies**: All games use the same pygame, numpy, etc.
4. **Development Friendly**: No switching between environments

## Quick Setup

### Manual Setup

```bash
cd ~/Downloads/CashuArcade

# Create shared venv
python3 -m venv .venv_launcher

# Activate and install all dependencies
source .venv_launcher/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Install gamelib and games as editable packages
pip install -e ./gamelib
pip install -e ./fishyfrens

deactivate
```

## Running the Launcher

```bash
cd ~/Downloads/CashuArcade
source .venv_launcher/bin/activate
python -m lnarcade
```

All games run using the shared `.venv_launcher` environment!

## Creating a New Game

### 1. Create Game Directory and Code

```bash
cd ~/Downloads/CashuArcade
mkdir mygame
cd mygame

# Create game package
mkdir mygame
touch mygame/__init__.py
touch mygame/__main__.py
# Add your game code
```

### 2. Create setup.py

```python
from setuptools import setup, find_packages

setup(
    name="mygame",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pygame",
        # Add other dependencies
    ],
    python_requires=">=3.7",
)
```

### 3. Create Manifest

```bash
cp ../lnarcade/manifest_template.json manifest.json
# Edit manifest.json with your game details
# Make sure to set "venv": null in the launch config
```

### 4. Add Screenshot

```bash
# Add a screenshot.png file
```

### 5. Install and Test

```bash
cd ..
source .venv_launcher/bin/activate
pip install -e ./mygame

# Test game directly
python -m mygame

# Test from launcher
python -m lnarcade
```

## Manifest Configuration

In your `manifest.json`, set `venv` to `null` to use the shared environment:

```json
{
    "launcher": {
        "name": "My Game",
        "launch": {
            "command": "python",
            "args": ["-m", "mygame"],
            "venv": null,           // Use shared .venv_launcher
            "cwd": "."
        }
    }
}
```

## How the Launcher Works

When you launch a game from the menu:

1. Launcher reads `manifest.json`
2. Since `venv` is `null`, uses the launcher's Python (already activated)
3. Runs: `python -m {gamename}`
4. Game imports work because they're installed in the shared venv

Example:
```bash
# All games run with the same Python
python -m fishyfrens
python -m testgame
python -m mygame
```

## Troubleshooting

### Module not found error

```
No module named 'mygame'
```

**Solution:** Install the game package in the shared venv:
```bash
cd ~/Downloads/CashuArcade
source .venv_launcher/bin/activate
pip install -e ./mygame
```

### Game won't launch

1. Check manifest has `"venv": null`
2. Check game is installed: `pip list | grep mygame`
3. Test game directly: `python -m mygame`
4. Check launcher logs for errors

### Import errors

If you get import errors for dependencies:
```bash
cd ~/Downloads/CashuArcade
source .venv_launcher/bin/activate
pip install <missing-package>
```

## Best Practices

### 1. Use setup.py for Games

Each game should have a `setup.py` to declare its dependencies:
```python
from setuptools import setup, find_packages

setup(
    name="mygame",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["pygame", "numpy"],
)
```

### 2. Keep Venvs Out of Git

Add to `.gitignore`:
```
.venv_launcher/
```

### 3. Install Games in Editable Mode

```bash
pip install -e ./mygame
```
This allows you to edit code without reinstalling.

### 4. Test Before Committing

```bash
source .venv_launcher/bin/activate
python -m mygame
python -m lnarcade
```

## Summary

- **Single Venv**: `.venv_launcher` for everything
- **gamelib**: Installed as editable package
- **Games**: Installed as editable packages
- **Setup**: Create venv once, install all packages
- **Running**: All games use the same Python environment
- **Benefits**: Simple, fast, easy to manage
