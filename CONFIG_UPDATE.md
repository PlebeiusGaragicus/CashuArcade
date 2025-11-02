# Configuration Update

## Changes Made

### 1. Config Location Changed

**OLD:** `~/.config/cashuarcade/config.env`  
**NEW:** `config.env` (in CashuArcade root directory)

**Why:**
- Config lives with the project (easier to manage)
- No hidden files in home directory
- Easier to version control via .sample file
- Simpler deployment

### 2. Files Created

- **`config.env.sample`** - Sample configuration with all options documented
- Replaces old `.env` file

### 3. Updated .gitignore

```gitignore
# Config (keep config.env.sample in git)
config.env
.env
```

- `config.env` is ignored (user-specific)
- `config.env.sample` is tracked (template for all users)

## Setup Instructions

### First Time Setup

```bash
cd ~/Downloads/CashuArcade  # or wherever your project is

# Copy sample config
cp config.env.sample config.env

# Edit if needed (all defaults are sensible)
nano config.env
```

### Configuration Options

```bash
# Enable debug logging (shows file names and line numbers)
DEBUG=False

# Free play mode (no coins required)
FREE_PLAY=True

# Time in seconds before auto-scrolling games (AFK mode)
AFK_SCROLL_TIME=300

# Override game search paths (colon-separated)
# LNARCADE_GAME_PATHS=~/CashuArcade:~/OtherGames
```

## Migration from Old Config

If you had config in `~/.config/cashuarcade/config.env`:

```bash
# Copy old config values to new location
cat ~/.config/cashuarcade/config.env

# Create new config
cd ~/Downloads/CashuArcade
cp config.env.sample config.env
# Edit config.env with your old values

# Optional: Remove old config
rm -rf ~/.config/cashuarcade
```

## How It Works

1. **Launcher starts** → Looks for `config.env` in project root
2. **If not found** → Creates default `config.env` automatically
3. **Loads variables** → Uses `python-dotenv` to load into environment
4. **Code accesses** → Via `os.getenv("VARIABLE_NAME")`

## Code Changes

### lnarcade/config.py

```python
# OLD
DATA_DIR = str(Path.home() / ".config" / "cashuarcade")
DOT_ENV_PATH = os.path.join(DATA_DIR, "config.env")

# NEW
DATA_DIR = os.path.dirname(MY_DIR)  # CashuArcade root
DOT_ENV_PATH = os.path.join(DATA_DIR, "config.env")
```

## Benefits

1. **Portable**: Config travels with project
2. **Visible**: No hidden config files
3. **Documented**: Sample file shows all options
4. **Version Control**: .sample file can be tracked
5. **Simple**: No directory creation needed
6. **Standard**: Common pattern in modern projects

## Testing

```bash
# Remove any existing config
rm config.env

# Run launcher (will create default)
source .venv_launcher/bin/activate
python -m lnarcade

# Check created config
cat config.env

# Customize and test
nano config.env
python -m lnarcade
```

## Related Files

- `config.env.sample` - Template configuration
- `config.env` - Your actual configuration (gitignored)
- `.gitignore` - Ignores config.env
- `lnarcade/config.py` - Config loading code
- `README.md` - Updated with new setup instructions
