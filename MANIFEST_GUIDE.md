# Game Manifest Guide

This guide explains how to create a `manifest.json` file for your game to work with the LNArcade launcher.

## Manifest Schema

Each game directory must contain a `manifest.json` file with the following structure:

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
        "debug": false,
        "custom_setting": "value"
    }
}
```

## Field Descriptions

### Launcher Section

The `launcher` section contains metadata used by the arcade launcher:

- **`name`** (required): Display name of your game shown in the menu
- **`description`** (optional): Brief description of your game
- **`author`** (optional): Your name or team name
- **`version`** (optional): Game version (default: "1.0.0")
- **`type`** (optional): Game type/engine (default: "pygame")
- **`screenshot`** (optional): Path to screenshot image relative to game directory (default: "screenshot.png")

### Launch Configuration

The `launch` section tells the launcher how to start your game:

- **`command`** (optional): Command to run (default: "python")
- **`args`** (optional): List of command-line arguments (default: [])
- **`venv`** (optional): Path to virtual environment directory relative to game directory (default: null)
- **`cwd`** (optional): Working directory relative to game directory (default: ".")

### Game Config Section

The `game_config` section is for your game-specific configuration. You can put any custom settings here that your game needs. The launcher will not use these values - they are purely for your game's use.

## Examples

### Simple Game (No Virtual Environment)

```json
{
    "launcher": {
        "name": "Simple Snake",
        "description": "Classic snake game",
        "author": "John Doe",
        "screenshot": "screenshot.png",
        "launch": {
            "command": "python",
            "args": ["main.py"]
        }
    },
    "game_config": {
        "difficulty": "medium"
    }
}
```

### Game with Virtual Environment

```json
{
    "launcher": {
        "name": "Advanced Platformer",
        "description": "A complex platformer with many dependencies",
        "author": "Jane Smith",
        "version": "2.1.0",
        "screenshot": "assets/screenshot.png",
        "launch": {
            "command": "python",
            "args": ["-m", "platformer"],
            "venv": ".venv",
            "cwd": "."
        }
    },
    "game_config": {
        "fullscreen": true,
        "music_volume": 0.8
    }
}
```

### Game in Subdirectory

```json
{
    "launcher": {
        "name": "Nested Game",
        "screenshot": "preview.png",
        "launch": {
            "command": "python",
            "args": ["game.py"],
            "venv": "../shared_venv",
            "cwd": "src"
        }
    },
    "game_config": {}
}
```

## Screenshot Requirements

- **Format**: PNG, JPG, or other pygame-supported image formats
- **Recommended Size**: Match your target display resolution (e.g., 1920x1080)
- **Location**: Place in your game directory and reference in `screenshot` field
- **Fallback**: If screenshot is missing, a default "missing image" placeholder will be shown

## Virtual Environment Setup

If your game uses a virtual environment:

1. Create the venv in your game directory:
   ```bash
   cd ~/CashuArcade/mygame
   python -m venv .venv
   ```

2. Install your game's dependencies:
   ```bash
   source .venv/bin/activate  # On macOS/Linux
   # or
   .venv\Scripts\activate  # On Windows
   
   pip install -r requirements.txt
   ```

3. Set `venv` in your manifest:
   ```json
   "launch": {
       "venv": ".venv"
   }
   ```

The launcher will automatically use the Python executable from your venv.

## Directory Structure

Your game directory should look like this:

```
~/CashuArcade/mygame/
├── manifest.json          # Required
├── screenshot.png         # Required (or specified name)
├── .venv/                 # Optional virtual environment
├── mygame/               # Your game code
│   ├── __init__.py
│   └── __main__.py
├── requirements.txt       # Optional
└── README.md             # Optional
```

## Backward Compatibility

The launcher supports old-style manifests without the `launcher` section for backward compatibility:

```json
{
    "name": "Old Style Game",
    "type": "pygame",
    "custom_setting": "value"
}
```

However, this format is deprecated and lacks support for:
- Virtual environments
- Custom launch commands
- Detailed metadata

**Please migrate to the new format.**

## Validation

The launcher will validate your manifest and log warnings for:
- Missing required fields
- Missing screenshot files
- Invalid virtual environment paths
- Missing launch commands

Games with validation errors will still appear in the menu but may not launch correctly.

## Testing Your Manifest

1. Place your game in `~/CashuArcade/yourgame/`
2. Create `manifest.json` and `screenshot.png`
3. Run the launcher: `python -m lnarcade`
4. Check the logs for any validation warnings
5. Try launching your game from the menu

## Common Issues

### Game Won't Launch

- Check that `command` and `args` are correct
- Verify `venv` path if using virtual environment
- Check `cwd` is correct relative to game directory
- Look at launcher logs for error messages

### Screenshot Not Showing

- Verify screenshot file exists at specified path
- Check file permissions
- Ensure path is relative to game directory

### Virtual Environment Not Found

- Check venv path is correct and relative to game directory
- Verify venv was created successfully
- Ensure Python executable exists in venv (bin/python or Scripts/python.exe)

## Support

For issues or questions:
- Check the launcher logs in the console
- Review the `LNARCADE_REFACTOR_PLAN.md` for technical details
- Ensure your manifest follows this guide's schema
