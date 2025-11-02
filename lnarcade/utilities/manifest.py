"""
Manifest schema and validation for arcade games.

The manifest.json file in each game directory contains metadata and launch configuration.
"""

import os
import json
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field

logger = logging.getLogger()


@dataclass
class LaunchConfig:
    """Configuration for launching a game."""
    command: str = "python"
    args: List[str] = field(default_factory=list)
    venv: Optional[str] = None  # Path to virtual environment (relative to game dir)
    cwd: str = "."  # Working directory (relative to game dir)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LaunchConfig':
        """Create LaunchConfig from dictionary."""
        return cls(
            command=data.get("command", "python"),
            args=data.get("args", []),
            venv=data.get("venv"),
            cwd=data.get("cwd", ".")
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "command": self.command,
            "args": self.args,
            "venv": self.venv,
            "cwd": self.cwd
        }


@dataclass
class LauncherMetadata:
    """Metadata for the arcade launcher."""
    name: str
    description: str = ""
    author: str = ""
    version: str = "1.0.0"
    type: str = "pygame"
    screenshot: str = "screenshot.png"
    launch: LaunchConfig = field(default_factory=LaunchConfig)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LauncherMetadata':
        """Create LauncherMetadata from dictionary."""
        launch_data = data.get("launch", {})
        if isinstance(launch_data, dict):
            launch = LaunchConfig.from_dict(launch_data)
        else:
            launch = LaunchConfig()
        
        return cls(
            name=data.get("name", "Unnamed Game"),
            description=data.get("description", ""),
            author=data.get("author", ""),
            version=data.get("version", "1.0.0"),
            type=data.get("type", "pygame"),
            screenshot=data.get("screenshot", "screenshot.png"),
            launch=launch
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "author": self.author,
            "version": self.version,
            "type": self.type,
            "screenshot": self.screenshot,
            "launch": self.launch.to_dict()
        }


@dataclass
class GameManifest:
    """Complete game manifest with launcher metadata and game-specific config."""
    launcher: LauncherMetadata
    game_config: Dict[str, Any] = field(default_factory=dict)
    game_dir: str = ""  # Absolute path to game directory
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], game_dir: str = "") -> 'GameManifest':
        """Create GameManifest from dictionary."""
        # Handle new format with 'launcher' section
        if "launcher" in data:
            launcher = LauncherMetadata.from_dict(data["launcher"])
            game_config = data.get("game_config", {})
        else:
            # Backward compatibility: treat entire manifest as launcher metadata
            # and extract known launcher fields
            launcher = LauncherMetadata.from_dict(data)
            # Everything else goes into game_config
            game_config = {k: v for k, v in data.items() 
                          if k not in ["name", "description", "author", "version", 
                                      "type", "screenshot", "launch"]}
        
        return cls(
            launcher=launcher,
            game_config=game_config,
            game_dir=game_dir
        )
    
    @classmethod
    def from_file(cls, manifest_path: str) -> Optional['GameManifest']:
        """Load manifest from JSON file."""
        try:
            with open(manifest_path, 'r') as f:
                data = json.load(f)
            
            game_dir = os.path.dirname(os.path.abspath(manifest_path))
            return cls.from_dict(data, game_dir)
        
        except FileNotFoundError:
            logger.error(f"Manifest file not found: {manifest_path}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in manifest {manifest_path}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error loading manifest {manifest_path}: {e}")
            return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "launcher": self.launcher.to_dict(),
            "game_config": self.game_config
        }
    
    def save(self, manifest_path: str) -> bool:
        """Save manifest to JSON file."""
        try:
            with open(manifest_path, 'w') as f:
                json.dump(self.to_dict(), f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving manifest {manifest_path}: {e}")
            return False
    
    def get_screenshot_path(self) -> str:
        """Get absolute path to screenshot image."""
        return os.path.join(self.game_dir, self.launcher.screenshot)
    
    def get_launch_cwd(self) -> str:
        """Get absolute path to launch working directory."""
        return os.path.join(self.game_dir, self.launcher.launch.cwd)
    
    def get_venv_python(self) -> Optional[str]:
        """Get path to Python executable in venv, if specified."""
        if not self.launcher.launch.venv:
            return None
        
        venv_path = os.path.join(self.game_dir, self.launcher.launch.venv)
        
        # Check common venv structures
        python_paths = [
            os.path.join(venv_path, "bin", "python"),  # Unix
            os.path.join(venv_path, "Scripts", "python.exe"),  # Windows
        ]
        
        for python_path in python_paths:
            if os.path.exists(python_path):
                return python_path
        
        logger.warning(f"Virtual environment not found at {venv_path}")
        return None
    
    def validate(self) -> tuple[bool, List[str]]:
        """
        Validate the manifest.
        
        Returns:
            (is_valid, error_messages)
        """
        errors = []
        
        # Check required fields
        if not self.launcher.name:
            errors.append("Missing required field: launcher.name")
        
        # Check screenshot exists
        screenshot_path = self.get_screenshot_path()
        if not os.path.exists(screenshot_path):
            errors.append(f"Screenshot not found: {screenshot_path}")
        
        # Check venv if specified
        if self.launcher.launch.venv:
            venv_python = self.get_venv_python()
            if not venv_python:
                errors.append(f"Virtual environment not found: {self.launcher.launch.venv}")
        
        # Check launch command
        if not self.launcher.launch.command:
            errors.append("Missing launch command")
        
        return (len(errors) == 0, errors)


def create_default_manifest(game_name: str, game_dir: str) -> GameManifest:
    """Create a default manifest for a game."""
    launcher = LauncherMetadata(
        name=game_name,
        description=f"A {game_name} game",
        author="Unknown",
        version="1.0.0",
        type="pygame",
        screenshot="screenshot.png",
        launch=LaunchConfig(
            command="python",
            args=["-m", game_name.lower().replace(" ", "_")],
            venv=".venv",
            cwd="."
        )
    )
    
    return GameManifest(
        launcher=launcher,
        game_config={},
        game_dir=game_dir
    )
