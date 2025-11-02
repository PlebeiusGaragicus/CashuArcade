import os
import logging
from typing import List, Dict, Optional

logger = logging.getLogger()

from lnarcade.config import APP_FOLDER, get_game_search_paths
from lnarcade.utilities.manifest import GameManifest


def find_game_directories(search_paths: Optional[List[str]] = None) -> List[str]:
    """
    Find all game directories in the search paths.
    
    Args:
        search_paths: List of directories to search. If None, uses default from config.
    
    Returns:
        List of absolute paths to game directories
    """
    if search_paths is None:
        search_paths = get_game_search_paths()
    
    game_dirs = []
    
    for search_path in search_paths:
        expanded_path = os.path.expanduser(search_path)
        
        if not os.path.exists(expanded_path):
            logger.warning(f"Game search path does not exist: {expanded_path}")
            continue
        
        if not os.path.isdir(expanded_path):
            logger.warning(f"Game search path is not a directory: {expanded_path}")
            continue
        
        # Find all subdirectories
        try:
            for entry in os.scandir(expanded_path):
                if entry.is_dir():
                    game_dirs.append(entry.path)
        except PermissionError as e:
            logger.error(f"Permission denied accessing {expanded_path}: {e}")
            continue
    
    logger.debug(f"Found {len(game_dirs)} potential game directories")
    return game_dirs


def load_game_manifests(game_dirs: Optional[List[str]] = None) -> Dict[str, GameManifest]:
    """
    Load manifests from game directories.
    
    Args:
        game_dirs: List of game directories. If None, discovers automatically.
    
    Returns:
        Dictionary mapping game directory name to GameManifest
    """
    if game_dirs is None:
        game_dirs = find_game_directories()
    
    manifests = {}
    
    for game_dir in game_dirs:
        manifest_path = os.path.join(game_dir, "manifest.json")
        
        if not os.path.exists(manifest_path):
            logger.debug(f"No manifest.json in {game_dir}, skipping")
            continue
        
        manifest = GameManifest.from_file(manifest_path)
        
        if manifest is None:
            logger.warning(f"Failed to load manifest from {manifest_path}")
            continue
        
        # Validate manifest
        is_valid, errors = manifest.validate()
        if not is_valid:
            logger.warning(f"Invalid manifest in {game_dir}:")
            for error in errors:
                logger.warning(f"  - {error}")
            # Still include it, but log the issues
        
        game_name = os.path.basename(game_dir)
        manifests[game_name] = manifest
        logger.debug(f"Loaded manifest for '{manifest.launcher.name}' from {game_dir}")
    
    logger.info(f"Successfully loaded {len(manifests)} game manifests")
    return manifests


# Backward compatibility functions
def find_apps() -> list:
    """Legacy function for backward compatibility."""
    return find_game_directories()


def get_app_manifests() -> dict:
    """
    Legacy function for backward compatibility.
    Returns dict of game_name -> manifest dict (old format).
    """
    manifests = load_game_manifests()
    
    # Convert to old format (dict with just the data)
    legacy_format = {}
    for game_name, manifest in manifests.items():
        # For backward compatibility, return the launcher metadata as top-level dict
        legacy_format[game_name] = {
            "name": manifest.launcher.name,
            "type": manifest.launcher.type,
            "description": manifest.launcher.description,
            "author": manifest.launcher.author,
            "version": manifest.launcher.version,
            **manifest.game_config  # Include game-specific config
        }
    
    return legacy_format
