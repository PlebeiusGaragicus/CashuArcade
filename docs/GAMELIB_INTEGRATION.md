# GameLib Integration

## Overview

The lnarcade launcher now uses `gamelib` for core functionality, ensuring consistency between the launcher and games.

## What Changed

### 1. ViewState System

**Before:**
- `lnarcade/view/__init__.py` contained custom `ViewState` and `ViewStateManager` classes

**After:**
- Now imports from `gamelib.viewstate`
- Uses `View` and `ViewManager` classes
- Provides aliases for backward compatibility:
  - `ViewState` → `View`
  - `ViewStateManager` → `ViewManager`

**Method Changes:**
- `add_state()` → `add_view()`
- `change_state()` → `run_view()`

### 2. Singleton Pattern

**Before:**
- `lnarcade/app.py` contained custom `Singleton` class

**After:**
- Now imports from `gamelib.singleton`
- Identical implementation, no behavior changes

### 3. Logger

**Before:**
- `lnarcade/logger.py` contained custom colored logging setup

**After:**
- Now imports from `gamelib.logger`
- File `lnarcade/logger.py` deleted (was identical to gamelib version)
- Same colored output and debug formatting

### 4. Colors

**Before:**
- `lnarcade/colors.py` defined basic colors (WHITE, BLACK, RED, GREEN, DARK)

**After:**
- Now imports all colors from `gamelib.colors`
- Keeps `DARK` as lnarcade-specific color
- Access to full color palette from gamelib

## Benefits

1. **Consistency**: Launcher and games use the same patterns
2. **Maintainability**: Single source of truth for common code
3. **Reduced Duplication**: No duplicate implementations
4. **Shared Improvements**: Updates to gamelib benefit everything

## File Changes

### Modified Files
- `lnarcade/view/__init__.py` - Now imports from gamelib
- `lnarcade/app.py` - Uses gamelib.singleton and gamelib.logger
- `lnarcade/colors.py` - Imports from gamelib.colors
- `lnarcade/view/splash.py` - Updated method calls

### Deleted Files
- `lnarcade/logger.py` - Replaced by gamelib.logger

## Usage Examples

### Creating a View

```python
from lnarcade.view import ViewState  # Actually gamelib.viewstate.View

class MyView(ViewState):
    def setup(self):
        pass
    
    def handle_event(self, event):
        pass
    
    def update(self):
        pass
    
    def draw(self):
        pass
```

### Using Colors

```python
from lnarcade.colors import *  # Imports from gamelib.colors

# All gamelib colors available
screen.fill(BLACK)
text_color = WHITE
highlight = BLUE
# Plus lnarcade-specific
background = DARK
```

### Logging

```python
import logging
from gamelib.logger import setup_logging

logger = logging.getLogger(__name__)
setup_logging()  # Colored output based on DEBUG env var

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

## Backward Compatibility

All existing code continues to work due to aliases:
- `ViewState` still works (alias for `View`)
- `ViewStateManager` still works (alias for `ViewManager`)
- Method names updated but functionality identical

## Future Considerations

### Potential Additional Integrations

1. **gamelib.utils** - Could use for common utility functions
2. **gamelib.text** - Text rendering helpers
3. **gamelib.texteffect** - Text effects for UI
4. **gamelib.menuaction** - Menu action handling

### Not Integrated (Yet)

- `gamelib.cooldown_keys` - Game-specific, not needed in launcher
- `gamelib.globals` - May not be needed
- `gamelib.menuaction` - Could be useful for menu system

## Testing

After integration, verify:
- [ ] Launcher starts correctly
- [ ] Views switch properly (splash → game_select)
- [ ] Logging works with colors
- [ ] Colors display correctly
- [ ] No import errors

## Notes

- gamelib is a shared library between launcher and games
- Both should be in the same parent directory (~/CashuArcade)
- Games can import gamelib directly
- Launcher imports gamelib and provides arcade-specific functionality
