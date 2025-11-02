# LNArcade Refactor Plan

## Current Architecture Review

### Core Functionality
**lnarcade** is a pygame-based arcade launcher that:
- Runs at bootup as the main menu/game selector
- Discovers games from `~/LNApps/` directory
- Displays game artwork and metadata
- Launches games as Python modules
- Manages display state and input handling

### Current Structure

#### Entry Point
- `__main__.py` → `app.py::App.get_instance().start()`
- Singleton pattern for app instance

#### Key Components

1. **App (`app.py`)**
   - Singleton application manager
   - Initializes pygame display (fullscreen on Linux, NOFRAME on macOS)
   - Sets up view state manager
   - Manages background threads (control manager, backend server)
   - Main game loop (event handling, update, draw)

2. **View System (`view/`)**
   - `ViewState` base class with lifecycle methods: `setup()`, `handle_event()`, `update()`, `draw()`
   - `ViewStateManager` for state transitions
   - `SplashScreen` - initial loading screen (currently skipped)
   - `GameSelectView` - main game selection interface
   - `ErrorModalView` - error display (referenced but not reviewed)

3. **Game Discovery (`utilities/find_games.py`)**
   - Scans `~/LNApps/` for game directories
   - Loads `manifest.json` from each game
   - Returns manifest data for display

4. **Control Manager (`control/controlmanager.py`)**
   - Hardware control integration (Adafruit Seesaw rotary encoder)
   - Volume control via system commands
   - **Only runs on non-macOS systems**
   - Requires `BLINKA_FT232H` environment variable

5. **Backend Server (`backend/server.py`)**
   - Currently empty/placeholder
   - Intended for Streamlit-based monitoring/admin

6. **Configuration (`config.py`)**
   - FPS = 10
   - `APP_FOLDER = "LNApps"` (in home directory)
   - `.env` file at `~/.config/.lnarcade`
   - Environment variables: `DEBUG`, `FREE_PLAY`, `SNES9X_EMULATOR_PATH`

---

## Issues & Needed Refactors

### 1. **Game Discovery System**
**Current Issues:**
- Hardcoded to look in `~/LNApps/`
- No validation of manifest schema
- Missing error handling for malformed manifests
- No support for game metadata beyond name and type
- No screenshot/image path specification in manifest

**Needed Changes:**
- Make game directory configurable
- Add proper manifest schema validation
- Support for game metadata: name, description, author, version, screenshot path
- Handle missing screenshots gracefully
- Support for multiple game directories (search paths)

### 2. **Game Launching System**
**Current Issues:**
- Launches games as Python modules: `python3 -m {module_name}`
- Assumes games are in `~/LNApps/` directory
- No support for virtual environments
- Blocking subprocess call
- No proper error recovery
- Display mode toggling is hacky

**Needed Changes:**
- Support launching games with their own venv
- Manifest should specify:
  - Launch command/script
  - Virtual environment path
  - Working directory
- Better display state management (minimize/restore)
- Non-blocking launch with proper process management
- Graceful error handling and recovery

### 3. **Manifest Schema**
**Current Schema (from fishyfrens example):**
```json
{
    "name": "Your Frens are Fishy!",
    "debug": true,
    "skip_to_gameplay": true,
    "starting_level": 0,
    "draw_masks": true,
    "god_mode": true,
    "fastswimmer": false,
    "quiet": true
}
```

**Issues:**
- No standard fields for launcher
- Game-specific config mixed with launcher metadata
- No image/screenshot path
- No launch configuration
- No type field (referenced in code but not in manifest)

**Proposed Schema:**
```json
{
  "launcher": {
    "name": "Your Frens are Fishy!",
    "description": "A fun underwater adventure",
    "author": "YourName",
    "version": "1.0.0",
    "type": "pygame",
    "screenshot": "screenshot.png",
    "launch": {
      "command": "python",
      "args": ["-m", "fishyfrens"],
      "venv": ".venv",
      "cwd": "."
    }
  },
  "game_config": {
    "debug": true,
    "skip_to_gameplay": true,
    "starting_level": 0,
    "draw_masks": true,
    "god_mode": true,
    "fastswimmer": false,
    "quiet": true
  }
}
```

### 4. **Deprecated/Unused Code**
**To Remove:**
- SNES emulator references (`SNES9X_EMULATOR_PATH` in config)
- Arcade library references (lines 200-202, 282-283 in `game_select.py`)
- Commented-out fullscreen toggle code
- Backend server placeholder (or implement properly)
- Control manager (if not using hardware controls)

### 5. **Display Management**
**Current Issues:**
- Global `APP_SCREEN` variable
- Inconsistent display mode handling
- Hacky pygame reinit after game launch

**Needed Changes:**
- Better encapsulation of display state
- Proper minimize/restore workflow
- Consider using pygame's window management features

### 6. **Configuration System**
**Current Issues:**
- `.env` file in `~/.config/.lnarcade` (unusual location)
- `FREE_PLAY` environment variable
- `AFK_SCROLL_TIME` for auto-scrolling

**Needed Changes:**
- Move to standard config location: `~/.config/lnarcade/config.json`
- Separate launcher config from game configs
- Support for:
  - Game search paths
  - Display preferences
  - Input mappings
  - Theme/appearance settings

### 7. **Input Handling**
**Current:**
- Keyboard only on macOS
- Hardware control manager for Linux (rotary encoder)
- Controller button mappings defined but not used

**Needed:**
- Unified input abstraction
- Support for keyboard, gamepad, and custom hardware
- Configurable key bindings

### 8. **Error Handling**
**Current Issues:**
- Minimal error handling
- `ErrorModalView` referenced but not fully implemented
- No graceful degradation

**Needed:**
- Proper error modal implementation
- Logging improvements
- User-friendly error messages
- Recovery mechanisms

---

## Implementation Plan

### Phase 1: Core Refactors (High Priority)

#### 1.1 Update Manifest Schema
- [ ] Define new manifest schema with `launcher` and `game_config` sections
- [ ] Create manifest validator
- [ ] Update `find_games.py` to parse new schema
- [ ] Add backward compatibility for old manifests

#### 1.2 Refactor Game Discovery
- [ ] Make game directory configurable
- [ ] Support multiple search paths
- [ ] Add proper error handling for missing/invalid manifests
- [ ] Validate screenshot paths
- [ ] Create default screenshot for missing images

#### 1.3 Refactor Game Launching
- [ ] Support venv activation in launch command
- [ ] Update `GameSelectView.launch()` to use manifest launch config
- [ ] Implement proper subprocess management
- [ ] Add error recovery and display restoration
- [ ] Test on macOS

### Phase 2: Configuration System (Medium Priority)

#### 2.1 New Config System
- [ ] Create `~/.config/lnarcade/config.json`
- [ ] Define config schema
- [ ] Migrate from `.env` to JSON config
- [ ] Add config validation

#### 2.2 Update Config Usage
- [ ] Update `config.py` to load from new location
- [ ] Remove deprecated config options
- [ ] Add game search paths to config

### Phase 3: Cleanup (Medium Priority)

#### 3.1 Remove Deprecated Code
- [ ] Remove SNES emulator references
- [ ] Remove arcade library references
- [ ] Clean up commented code
- [ ] Remove or implement backend server

#### 3.2 Code Quality
- [ ] Fix global variables (`APP_SCREEN`, etc.)
- [ ] Improve error handling
- [ ] Add type hints
- [ ] Update logging

### Phase 4: Polish (Low Priority)

#### 4.1 UI Improvements
- [ ] Implement proper splash screen
- [ ] Add game descriptions to UI
- [ ] Improve visual feedback
- [ ] Add loading indicators

#### 4.2 Input System
- [ ] Unified input abstraction
- [ ] Gamepad support
- [ ] Configurable key bindings

---

## Immediate Next Steps

1. **Create new manifest schema** and validator
2. **Update `find_games.py`** to support new schema
3. **Refactor game launching** to support venv
4. **Test with fishyfrens** game
5. **Document new manifest format** for game developers

---

## Testing Strategy

### Test Cases
1. Game discovery with new manifest format
2. Game discovery with old manifest format (backward compat)
3. Game launch with venv
4. Game launch without venv
5. Missing screenshot handling
6. Invalid manifest handling
7. Display restoration after game exit
8. Error modal display

### Test Environment
- macOS (primary development platform)
- Raspberry Pi (future deployment target)

---

## Migration Guide for Games

Games will need to:
1. Update `manifest.json` to new schema
2. Add `screenshot.png` to game directory
3. Ensure game can be launched from venv
4. Test launch from lnarcade

Example migration:
```bash
cd ~/LNApps/fishyfrens
# Add screenshot
cp resources/screenshot.png screenshot.png
# Update manifest.json
# Test launch
```

---

## Notes

- **macOS Focus**: Since you mentioned it will likely run on macOS, we can deprioritize the control manager and focus on keyboard/gamepad input
- **Venv Support**: Critical for isolating game dependencies
- **Backward Compatibility**: Try to support old manifests during transition
- **Documentation**: Need to document manifest format for game developers
