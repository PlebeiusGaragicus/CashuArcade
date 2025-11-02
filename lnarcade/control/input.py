"""
Input handling for arcade controls.

Supports keyboard and generic gamepad input.
Hardware-specific controller mappings have been removed.
"""

from enum import Enum, auto


MOVEMENT_SPEED = 5
DEAD_ZONE = 0.05


class GamepadButton:
    """Generic gamepad button mapping."""
    A: int = 0
    B: int = 1
    X: int = 2
    Y: int = 3
    L: int = 4
    R: int = 5
    SELECT: int = 6
    START: int = 7
    UP: int = 8
    DOWN: int = 9
    LEFT: int = 10
    RIGHT: int = 11


class InputStyle(Enum):
    """Input device types."""
    KEYBOARD: int = auto()
    GAMEPAD: int = auto()


class InputModality:
    """
    Input modality handler.
    
    TODO: Implement proper input abstraction for keyboard and gamepad.
    """
    def __init__(self, controller, input_style: InputStyle = InputStyle.KEYBOARD, button_map: dict = None):
        self.controller = controller
        self.input_style = input_style
        self.button_map = button_map or {}
        self.repeat_lock = False
