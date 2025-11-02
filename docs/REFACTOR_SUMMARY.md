# LNArcade Refactor Summary

## Overview

The lnarcade launcher has been refactored to support modern game management with virtual environments, better manifest schema, and improved error handling.

**BREAKING CHANGES:** This refactor includes breaking changes:
- Default game directory changed from `~/LNApps` to `~/CashuArcade`
- Config file moved from `~/.config/.lnarcade` to `~/.config/cashuarcade/config.env`
- All SNES emulator references removed
- Games are expected to be submodules within the CashuArcade directory

## What Changed

### 1. New Manifest System

**New Files:**
- `lnarcade/utilities/manifest.py` - Complete manifest schema with validation
- `lnarcade/manifest_template.json` - Template for new games
- `MANIFEST_GUIDE.md` - Comprehensive documentation

**Key Features:**
- Structured schema with `launcher` and `game_config` sections
- Virtual environment support
- Configurable launch commands
- Manifest validation with helpful error messages
- Backward compatibility with old format

### 2. Refactored Game Discovery

**Modified:** `lnarcade/utilities/find_games.py`

**Improvements:**
- Uses new manifest system
- Configurable search paths (via `LNARCADE_GAME_PATHS` env var)
- Better error handling and logging
- Validates manifests on load
- Backward compatibility functions maintained

### 3. Enhanced Game Launching

**Modified:** `lnarcade/view/game_select.py`

**New Features:**
- Virtual environment support - automatically uses venv Python if specified
- Configurable launch commands from manifest
- Better error handling with detailed logging
- Proper display restoration after game exit
- Removed deprecated arcade library code

**Changes to GameListItem:**
- Now uses `GameManifest` object instead of dict
- Automatic screenshot loading with fallback to default
- Properties for clean access to game metadata

### 4. Configuration Updates

**Modified:** `lnarcade/config.py`

**Changes:**
- Added `get_game_search_paths()` function
- Added `MISSING_SCREENSHOT` constant
- Removed deprecated `SNES9X_EMULATOR_PATH` from default .env
- Added `AFK_SCROLL_TIME` to default .env

### 5. Backend Server Cleanup

**Modified:** `lnarcade/backend/server.py`

**Changes:**
- Added proper class structure
- Documented TODO items for future implementation
- No longer just a comment

### 6. Migration Tools

**New File:** `lnarcade/utilities/migrate_manifest.py`

**Features:**
- Migrate single game or all games
- Dry-run mode to preview changes
- Automatic backup of old manifests
- Infers sensible defaults for launch config

## Updated Manifest Format

### Old Format (Still Supported)
```json
{
    "name": "My Game",
    "type": "pygame",
    "debug": true
}
```

### New Format (Recommended)
```json
{
    "launcher": {
        "name": "My Game",
        "description": "Game description",
        "author": "Author Name",
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
        "debug": true
    }
}
```

## Migration Guide

### For Existing Games

1. **Update manifest format:**
   ```bash
   python -m lnarcade.utilities.migrate_manifest ~/CashuArcade/mygame
   ```

2. **Or migrate all games:**
   ```bash
   python -m lnarcade.utilities.migrate_manifest --all
   ```

3. **Add screenshot if missing:**
   ```bash
   cd ~/CashuArcade/mygame
   # Create or copy a screenshot.png file
   ```

4. **Set up virtual environment (if needed):**
   ```bash
   cd ~/CashuArcade/mygame
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

### For New Games

1. **Copy template:**
   ```bash
   cp lnarcade/manifest_template.json ~/CashuArcade/mygame/manifest.json
   ```

2. **Edit manifest** with your game's details

3. **Add screenshot:**
   ```bash
   # Add screenshot.png to game directory
   ```

4. **Test:**
   ```bash
   python -m lnarcade
   ```

## Testing

### Quick Test

1. **Check manifest loading:**
   ```python
   from lnarcade.utilities.find_games import load_game_manifests
   manifests = load_game_manifests()
   print(f"Found {len(manifests)} games")
   for name, manifest in manifests.items():
       print(f"  - {manifest.launcher.name}")
   ```

2. **Validate a manifest:**
   ```python
   from lnarcade.utilities.manifest import GameManifest
   manifest = GameManifest.from_file("~/LNApps/mygame/manifest.json")
   is_valid, errors = manifest.validate()
   if not is_valid:
       for error in errors:
           print(f"  ERROR: {error}")
   ```

3. **Run the launcher:**
   ```bash
   python -m lnarcade
   ```

### What to Test

- [ ] Games appear in menu
- [ ] Screenshots display correctly
- [ ] Game launches successfully
- [ ] Display restores after game exit
- [ ] Virtual environment is used (if specified)
- [ ] Error handling for missing files
- [ ] Backward compatibility with old manifests

## Known Issues

1. **Display restoration** - May need adjustment on different platforms
2. **Backend server** - Not implemented yet (placeholder only)
3. **Error modal** - Referenced but not fully implemented
4. **Control manager** - Only works on non-macOS with hardware

## Future Improvements

### High Priority
- [ ] Implement error modal view
- [ ] Add gamepad support
- [ ] Better display state management
- [ ] Non-blocking game launch option

### Medium Priority
- [ ] Backend server implementation (Streamlit/Flask)
- [ ] Credit/coin system
- [ ] Game statistics tracking
- [ ] Configuration UI

### Low Priority
- [ ] Multiple screenshot support (carousel)
- [ ] Video preview support
- [ ] Theme customization
- [ ] Network multiplayer lobby

## Breaking Changes

**YES - This is a breaking refactor:**

1. **Game Directory**: Changed from `~/LNApps` to `~/CashuArcade`
   - You must move your games: `mv ~/LNApps ~/CashuArcade`

2. **Config Location**: Changed from `~/.config/.lnarcade` to `~/.config/cashuarcade/config.env`
   - Old config will not be read automatically

3. **SNES References**: All SNES emulator code removed
   - No longer supports SNES ROM launching
   - Focus is on Python game submodules

4. **Controller Mappings**: Hardware-specific controller classes removed
   - Generic `GamepadButton` class replaces SNES/N64/DragonRise specific mappings

**Migration Required:** You must move your games to the new directory structure.

## Files Modified

- `lnarcade/utilities/find_games.py` - Refactored game discovery
- `lnarcade/view/game_select.py` - Enhanced game launching
- `lnarcade/config.py` - Added configuration functions
- `lnarcade/backend/server.py` - Added structure
- `fishyfrens/manifest.json` - Updated to new format

## Files Created

- `lnarcade/utilities/manifest.py` - Manifest schema and validation
- `lnarcade/utilities/migrate_manifest.py` - Migration tool
- `lnarcade/manifest_template.json` - Template for new games
- `MANIFEST_GUIDE.md` - User documentation
- `LNARCADE_REFACTOR_PLAN.md` - Technical planning document
- `REFACTOR_SUMMARY.md` - This file

## Rollback Plan

If issues arise, you can rollback by:

1. **Restore old manifests:**
   ```bash
   cd ~/CashuArcade/mygame
   mv manifest.json.backup manifest.json
   ```

2. **Use git to revert:**
   ```bash
   git checkout HEAD~1 lnarcade/
   ```

3. **Old code still works** - Backward compatibility maintained

## Support

For issues:
1. Check logs in console output
2. Review `MANIFEST_GUIDE.md`
3. Validate manifest with migration tool
4. Check `LNARCADE_REFACTOR_PLAN.md` for technical details

## Next Steps

1. **Test with fishyfrens** - Verify the refactored system works
2. **Migrate other games** - Update any other game manifests
3. **Create more games** - Use new manifest format
4. **Implement error modal** - Better user feedback
5. **Add gamepad support** - Enhanced input handling
