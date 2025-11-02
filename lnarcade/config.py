import os
from pathlib import Path
from typing import List

import logging
logger = logging.getLogger()

FPS = 10

MY_DIR = os.path.dirname(os.path.realpath(__file__))

# Use the CashuArcade root directory for config (parent of lnarcade)
DATA_DIR = os.path.dirname(MY_DIR)
DOT_ENV_PATH = os.path.join(DATA_DIR, "config.env")

# Default game folder (games will be submodules in ~/CashuArcade)
APP_FOLDER = "CashuArcade"

SHOW_MOUSE = False
SCREEN_TITLE = "Lightning Arcade"

# Default missing screenshot image
MISSING_SCREENSHOT = os.path.join(MY_DIR, "..", "resources", "img", "missing.jpg")


def get_game_search_paths() -> List[str]:
    """
    Get list of directories to search for games.
    
    Returns:
        List of directory paths (absolute paths)
    """
    # Check for environment variable override first
    env_paths = os.getenv("LNARCADE_GAME_PATHS")
    if env_paths:
        return [p.strip() for p in env_paths.split(":")]
    
    # Default: Search in the parent directory of lnarcade (where games are submodules)
    # This is the CashuArcade root directory
    parent_dir = os.path.dirname(MY_DIR)
    
    # Also check ~/CashuArcade as fallback
    home_arcade = os.path.expanduser(os.path.join("~", APP_FOLDER))
    
    search_paths = [parent_dir]
    
    # Add home directory if it exists and is different from parent_dir
    if os.path.exists(home_arcade) and os.path.abspath(home_arcade) != os.path.abspath(parent_dir):
        search_paths.append(home_arcade)
    
    return search_paths


def create_default_dot_env():
    """Create default config.env file with basic configuration."""
    print(f"Creating default config file in {DOT_ENV_PATH}")

    with open(DOT_ENV_PATH, "w") as f:
        env = "# CashuArcade Configuration\n\n"
        env += "# Enable debug logging\n"
        env += "DEBUG=False\n\n"
        env += "# Free play mode (no coins required)\n"
        env += "FREE_PLAY=True\n\n"
        env += "# Time in seconds before auto-scrolling games (AFK mode)\n"
        env += "AFK_SCROLL_TIME=300\n\n"
        env += "# Override game search paths (colon-separated)\n"
        env += "# LNARCADE_GAME_PATHS=~/CashuArcade:~/OtherGames\n"

        f.write(env)

