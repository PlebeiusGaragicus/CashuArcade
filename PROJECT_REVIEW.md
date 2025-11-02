# CashuArcade Project Review

**Review Date:** November 1, 2025  
**Total Lines of Code:** 4,196 lines (excluding venv)

---

## Executive Summary

CashuArcade is a Python-based arcade game launcher system with an integrated example game. The project consists of three main components:
1. **lnarcade** - The game selector/launcher (780 lines)
2. **fishyfrens** - An example boid-based game (1,301 lines)
3. **gamelib** - Shared utilities library (1,248 lines)

The system is designed to run on both macOS (development) and Linux/Raspberry Pi (production arcade cabinet).

---

## Project Architecture

### 1. lnarcade (Game Launcher)
**Purpose:** Main arcade menu system that discovers and launches games

**Key Components:**
- `app.py` (144 lines) - Main application with Singleton pattern, pygame initialization
- `view/game_select.py` (204 lines) - Game selection UI with visual artwork display
- `utilities/find_games.py` (28 lines) - Discovers games via manifest.json files
- `backend/server.py` (110 lines) - PyWebIO-based web interface on port 8080
- `control/controlmanager.py` (63 lines) - Hardware control via I2C rotary encoder

**Features:**
- Fullscreen game selector with gradient overlays
- Automatic game discovery from `~/LNApps/` directory
- Games must have a `manifest.json` file
- Web-based configuration backend (password: "a")
- Hardware volume control support (Linux only)
- Free play mode toggle
- Auto-scroll after AFK timeout (300s default)

**Configuration:**
- `.env` file stored at `~/.config/.lnarcade`
- Variables: `DEBUG`, `FREE_PLAY`, `SNES9X_EMULATOR_PATH`, `AFK_SCROLL_TIME`
- FPS: 10 (intentionally low for menu)

**Launch Mechanism:**
```python
subprocess.run(["python3", "-m", selected_app], cwd="~/LNApps")
```
- Blocking call - waits for game to exit
- Restores pygame display after game closes

---

### 2. fishyfrens (Example Game)
**Purpose:** Boid simulation game demonstrating the arcade framework

**Key Components:**
- `app.py` (131 lines) - Game application with view management
- `level.py` (195 lines) - Level progression and agent spawning
- `actor/player.py` (174 lines) - Player fish character
- `actor/agent.py` (190 lines) - AI fish with steering behaviors
- `actor/boid.py` (139 lines) - Boid flocking algorithm implementation
- `view/gameplay.py` (391 lines) - Main gameplay view
- `view/camera.py` (114 lines) - Camera system with following behavior
- `audio.py` (69 lines) - Sound effects management

**Game Features:**
- Boid-based AI fish with flocking behavior
- Multiple agent types (friendly, hostile, neutral)
- Camera follows player with smooth interpolation
- Level progression system
- Collision detection using pygame masks
- Debug mode with visual overlays

**Configuration (manifest.json):**
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

**Technical Details:**
- FPS: 80
- Uses pygame for rendering
- Singleton pattern for player and level management
- View state machine (splash → menu → gameplay → results)
- Platform-specific display handling (macOS vs Linux)

---

### 3. gamelib (Shared Library)
**Purpose:** Common utilities shared between games

**Components:**
- `singleton.py` (9 lines) - Singleton pattern implementation
- `viewstate.py` (28 lines) - View/ViewManager base classes
- `globals.py` (4 lines) - Global screen variables
- `colors.py` (1,018 lines) - Comprehensive color definitions
- `logger.py` (31 lines) - Logging setup
- `cooldown_keys.py` (47 lines) - Input cooldown management
- `text.py` (20 lines) - Text rendering utilities
- `texteffect.py` (49 lines) - Text animation effects
- `menuaction.py` (16 lines) - Menu action enum
- `utils.py` (25 lines) - General utilities

**Design Pattern:**
- Base `View` class with lifecycle methods: `setup()`, `handle_event()`, `update()`, `draw()`
- `ViewManager` handles state transitions
- Shared globals for screen dimensions

---

## Dependencies

**requirements.txt:**
```
arcade
pygame
numpy
icecream
```

**Additional (not listed):**
- `pywebio` - Web backend interface
- `python-dotenv` - Environment configuration
- `adafruit-circuitpython-seesaw` - Hardware control (Linux only)
- `board` - CircuitPython board support (Linux only)

**Note:** Requirements file is incomplete - needs dependencies from all games

---

## Current Issues & TODOs

### Critical Issues:
1. **Incomplete requirements.txt** - Missing pywebio, dotenv, hardware libraries
2. **Game discovery path hardcoded** - Expects `~/LNApps/` directory
3. **Security concerns** - Weak password ("a"), no HTTPS for web backend
4. **Error handling** - `show_error()` function referenced but not imported in `find_games.py`

### Known Bugs:
1. **Resource fork issue** (from README) - rsync-sync VS Code extension caused process fork failures
2. **Display restoration** - Pygame display needs manual reset after game exits
3. **MacOS fullscreen** - Commented out with warning "DON'T DO FULLSCREEN FOR THE LOVE OF GOD"

### TODOs Found in Code:
1. **lnarcade:**
   - Implement error modal views
   - Add IP address display functionality
   - Improve coin/credit system (currently just FREE_PLAY toggle)
   - Better AFK scroll implementation
   - Robust error handling for missing apps folder

2. **fishyfrens:**
   - Clean up level progression system
   - Improve agent spawning algorithm (currently uses inefficient while loop)
   - Add custom exception view (like seedsigner)
   - Test display settings on Raspberry Pi

3. **gamelib:**
   - Document view lifecycle
   - Add more utility functions

4. **Backend:**
   - Implement HTTPS
   - Add session management (JWT)
   - Rate limiting for password attempts
   - Input validation
   - Logging of access attempts

---

## File Structure

```
CashuArcade/
├── lnarcade/              # Game launcher (780 lines)
│   ├── app.py             # Main application
│   ├── config.py          # Configuration
│   ├── view/              # UI views
│   │   ├── game_select.py # Main menu
│   │   ├── splash.py      # Splash screen
│   │   └── error.py       # Error modal
│   ├── backend/           # Web interface
│   │   └── server.py      # PyWebIO server
│   ├── control/           # Hardware control
│   │   ├── controlmanager.py
│   │   ├── input.py
│   │   └── volume.py
│   └── utilities/         # Helper functions
│       └── find_games.py  # Game discovery
│
├── fishyfrens/            # Example game (1,301 lines)
│   ├── app.py             # Game application
│   ├── config.py          # Game settings
│   ├── level.py           # Level management
│   ├── audio.py           # Sound system
│   ├── manifest.json      # Game metadata
│   ├── actor/             # Game entities
│   │   ├── player.py      # Player character
│   │   ├── agent.py       # AI fish
│   │   ├── boid.py        # Flocking behavior
│   │   └── singletons.py  # Global instances
│   ├── view/              # Game views
│   │   ├── gameplay.py    # Main gameplay
│   │   ├── menu.py        # Main menu
│   │   ├── results.py     # Results screen
│   │   ├── splash.py      # Splash screen
│   │   └── camera.py      # Camera system
│   └── resources/         # Assets
│
├── gamelib/               # Shared library (1,248 lines)
│   ├── singleton.py       # Singleton pattern
│   ├── viewstate.py       # View base classes
│   ├── globals.py         # Global variables
│   ├── colors.py          # Color definitions
│   ├── logger.py          # Logging setup
│   ├── cooldown_keys.py   # Input management
│   ├── text.py            # Text utilities
│   ├── texteffect.py      # Text effects
│   └── utils.py           # General utilities
│
├── resources/             # Shared resources
│   ├── fonts/
│   ├── img/
│   └── sounds/
│
├── TESTING/               # Test scripts (337 lines)
│   ├── bloom.py
│   ├── explosion.py
│   ├── lightning1.py
│   ├── lightning2.py
│   ├── main.py
│   └── sfml.py
│
├── requirements.txt       # Dependencies (incomplete)
├── README.md              # Documentation (mostly notes)
├── countlines.py          # Code metrics utility
└── .gitignore
```

---

## Platform Support

### macOS (Development)
- **Display:** Windowed with NOFRAME flag
- **Height adjustment:** -34px for menu bar/camera cutout
- **Control manager:** Disabled (no hardware support)
- **Fullscreen:** Avoided due to issues

### Linux/Raspberry Pi (Production)
- **Display:** True fullscreen with NOFRAME
- **Hardware control:** I2C rotary encoder for volume
- **Backend:** Web interface for configuration
- **Target:** Arcade cabinet deployment

---

## Game Integration Requirements

For a game to work with lnarcade, it must:

1. **Be a Python module** - Runnable with `python3 -m gamename`
2. **Have manifest.json** in root directory with at minimum:
   ```json
   {
       "name": "Game Display Name",
       "type": "optional-game-type"
   }
   ```
3. **Have image.png** - Screenshot/artwork for menu display
4. **Be located in** `~/LNApps/` directory
5. **Exit cleanly** - Return to launcher on quit
6. **Handle display** - Initialize pygame display independently

---

## Strengths

1. **Clean architecture** - Separation of launcher, games, and shared library
2. **View state pattern** - Organized UI management
3. **Singleton pattern** - Proper single-instance management
4. **Game discovery** - Automatic manifest-based detection
5. **Platform abstraction** - Handles macOS/Linux differences
6. **Hardware integration** - Support for physical controls
7. **Web backend** - Remote configuration capability
8. **Example game** - fishyfrens demonstrates framework usage

---

## Weaknesses

1. **Incomplete documentation** - README is mostly notes and troubleshooting
2. **Missing dependencies** - requirements.txt doesn't list all packages
3. **Hardcoded paths** - `~/LNApps/` not configurable
4. **Security issues** - Weak password, no HTTPS, no rate limiting
5. **Error handling** - Many TODOs for error cases
6. **Testing** - No unit tests, only manual test scripts
7. **Code duplication** - Similar patterns in lnarcade and gamelib
8. **Magic numbers** - Many hardcoded values without constants

---

## Recommendations

### Immediate Priorities:
1. **Fix requirements.txt** - Add all dependencies with versions
2. **Document setup** - Clear installation and configuration guide
3. **Error handling** - Implement proper error modals and logging
4. **Security** - Strengthen web backend authentication
5. **Configuration** - Make game directory path configurable

### Future Enhancements:
1. **Game management** - Install/uninstall games via web interface
2. **Coin system** - Implement actual payment integration
3. **Statistics** - Track play time, high scores
4. **Multiple displays** - Support for marquee/second screen
5. **Game categories** - Organize games by type
6. **Search/filter** - Find games quickly in large libraries
7. **Themes** - Customizable UI appearance
8. **Emulator support** - Better integration with SNES9X, etc.

### Code Quality:
1. **Type hints** - Add throughout codebase
2. **Unit tests** - Test core functionality
3. **Linting** - Add pylint/flake8 configuration
4. **Documentation** - Docstrings for all public methods
5. **Constants** - Extract magic numbers to config
6. **Logging** - Consistent logging levels and messages

---

## Development Status

**Overall Status:** 🟡 **Functional but needs polish**

- ✅ Core launcher works
- ✅ Game discovery functional
- ✅ Example game complete
- ✅ Hardware control implemented
- ✅ Web backend operational
- ⚠️ Documentation incomplete
- ⚠️ Security needs improvement
- ⚠️ Error handling needs work
- ⚠️ Dependencies not fully specified
- ❌ No automated tests

---

## Getting Started (Inferred)

### Setup:
```bash
# Clone repository
cd ~/Downloads/CashuArcade

# Install dependencies
pip install -r requirements.txt
pip install pywebio python-dotenv  # Missing from requirements.txt

# Create games directory
mkdir -p ~/LNApps

# Copy example game
cp -r fishyfrens ~/LNApps/

# Run launcher
python3 -m lnarcade
```

### Web Backend:
- Access at `http://localhost:8080`
- Default password: `a`
- Configure `.env` settings
- Kill running processes

### Controls:
- **Arrow Keys:** Navigate menu
- **Enter:** Launch game
- **Escape:** Exit
- **A:** Show IP address (hold)
- **B:** Toggle mouse coordinates

---

## Conclusion

CashuArcade is a well-architected arcade launcher system with a solid foundation. The separation of concerns between launcher, games, and shared library is clean. The example game (fishyfrens) effectively demonstrates the framework's capabilities with boid-based AI and smooth gameplay.

The main areas needing attention are:
- Documentation and setup instructions
- Security hardening for production use
- Complete dependency specification
- Comprehensive error handling
- Testing infrastructure

With these improvements, this could be a robust platform for building and deploying arcade games on Raspberry Pi hardware.

**Recommended Next Steps:**
1. Complete requirements.txt
2. Write proper README with setup instructions
3. Implement error handling throughout
4. Add security improvements to web backend
5. Create at least one more example game to validate framework
