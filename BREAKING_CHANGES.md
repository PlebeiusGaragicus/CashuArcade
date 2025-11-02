# Breaking Changes - LNArcade Refactor

## Overview

This refactor introduces **BREAKING CHANGES** to clean up the codebase and establish a solid foundation for the CashuArcade system.

## Critical Breaking Changes

### 1. Game Directory Location

**OLD:** `~/LNApps/`  
**NEW:** `~/CashuArcade/`

**Action Required:**
```bash
# Move your games to the new location
mv ~/LNApps ~/CashuArcade

# Or if you want to keep both temporarily
cp -r ~/LNApps/* ~/CashuArcade/
```

**Why:** 
- More descriptive name matching the project
- Games will be submodules within this directory
- Consistent with project structure

### 2. Configuration File Location

**OLD:** `~/.config/.lnarcade`  
**NEW:** `config.env` (in CashuArcade root directory)

**Action Required:**
```bash
# Copy the sample config
cd ~/CashuArcade  # or wherever your CashuArcade is
cp config.env.sample config.env

# Edit as needed
nano config.env
```

**Why:**
- Config lives with the project
- Easier to manage and version control (via .sample file)
- Simpler deployment
- No hidden config in home directory

### 3. SNES Emulator Support Removed

**REMOVED:**
- All SNES emulator references
- `SNES9X_EMULATOR_PATH` config option
- SNES controller button mappings
- N64 controller button mappings
- DragonRise controller button mappings

**Action Required:**
- Remove any SNES-related configuration
- Games must be Python modules, not ROM files

**Why:**
- Focus on Python game submodules
- Simplify codebase
- Remove unused functionality

### 4. Controller Input Changes

**OLD:**
```python
from lnarcade.control.input import SNESButton, N64Button, DragonRiseButton
```

**NEW:**
```python
from lnarcade.control.input import GamepadButton
```

**Action Required:**
- Update any code using hardware-specific button mappings
- Use generic `GamepadButton` class

**Why:**
- Generic gamepad support
- Remove hardware-specific code
- Simpler input handling

### 5. GameLib Integration

**REMOVED FILES:**
- `lnarcade/logger.py` (now uses `gamelib.logger`)

**CHANGED IMPORTS:**
```python
# OLD
from lnarcade.logger import setup_logging
from lnarcade.view import ViewState, ViewStateManager

# NEW
from gamelib.logger import setup_logging
from lnarcade.view import ViewState, ViewStateManager  # Actually imports from gamelib
```

**Action Required:**
- None for most users (imports still work via aliases)
- Direct imports from gamelib are now preferred

**Why:**
- Consistency between launcher and games
- Shared code reduces duplication
- Single source of truth

### 6. ViewManager Method Names

**OLD:**
```python
manager.add_state("view_name", view)
manager.change_state("view_name")
```

**NEW:**
```python
manager.add_view("view_name", view)
manager.run_view("view_name")
```

**Action Required:**
- Update any custom view code using old method names
- Aliases provided for backward compatibility in lnarcade

**Why:**
- Consistency with gamelib naming
- More descriptive method names

## Non-Breaking Changes

These changes are improvements but don't break existing functionality:

### 1. New Manifest System
- Old manifest format still supported
- New format recommended for new games
- Validation and better error messages

### 2. Virtual Environment Support
- Optional feature
- Games without venv still work
- Better dependency isolation when used

### 3. Configurable Game Paths
- Default is `~/CashuArcade`
- Can override with `LNARCADE_GAME_PATHS` env var
- Multiple search paths supported

## Migration Checklist

- [ ] **Move games** from `~/LNApps` to `~/CashuArcade`
- [ ] **Update game manifests** to new format (optional but recommended)
- [ ] **Remove SNES config** if present
- [ ] **Test launcher** with moved games
- [ ] **Update any custom code** using old controller mappings
- [ ] **Verify venv paths** in manifests if using virtual environments

## Quick Migration Script

```bash
#!/bin/bash
# Quick migration for CashuArcade refactor

echo "CashuArcade Migration Script"
echo "============================"

# 1. Move games
if [ -d ~/LNApps ]; then
    echo "Moving ~/LNApps to ~/CashuArcade..."
    if [ -d ~/CashuArcade ]; then
        echo "WARNING: ~/CashuArcade already exists!"
        echo "Merging contents..."
        cp -rn ~/LNApps/* ~/CashuArcade/
    else
        mv ~/LNApps ~/CashuArcade
    fi
    echo "✓ Games moved"
else
    echo "✓ No ~/LNApps directory found (already migrated?)"
fi

# 2. Create new config directory
echo "Creating config directory..."
mkdir -p ~/.config/cashuarcade
echo "✓ Config directory created"

# 3. Clean up old config (optional)
if [ -f ~/.config/.lnarcade ]; then
    echo "Found old config at ~/.config/.lnarcade"
    echo "You may want to review and delete it manually"
fi

echo ""
echo "Migration complete!"
echo "Run: python -m lnarcade"
```

## Rollback

If you need to rollback:

```bash
# Restore old directory structure
mv ~/CashuArcade ~/LNApps

# Use git to revert code changes
cd /path/to/CashuArcade
git checkout <previous-commit>
```

**Note:** Rollback is not recommended as the old structure is deprecated.

## Support

If you encounter issues:

1. Check that games are in `~/CashuArcade`
2. Verify manifest.json exists in each game directory
3. Check logs for specific error messages
4. Review `MANIFEST_GUIDE.md` for manifest format
5. See `REFACTOR_SUMMARY.md` for technical details

## Timeline

- **Old structure (`~/LNApps`)**: Deprecated, no longer supported
- **New structure (`~/CashuArcade`)**: Current and required
- **SNES support**: Removed permanently
- **Old manifest format**: Supported but deprecated

## Benefits of Breaking Changes

1. **Cleaner codebase** - Removed unused SNES code
2. **Better organization** - Proper directory structure
3. **Consistency** - Shared gamelib between launcher and games
4. **Modern features** - Virtual environment support
5. **Maintainability** - Less duplicate code
6. **Extensibility** - Better foundation for future features

## Questions?

- Review `LNARCADE_REFACTOR_PLAN.md` for technical details
- Check `MANIFEST_GUIDE.md` for manifest format
- See `GAMELIB_INTEGRATION.md` for gamelib usage
- Read `REFACTOR_SUMMARY.md` for change summary
