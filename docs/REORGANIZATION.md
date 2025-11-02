# Repository Reorganization

## Summary

The CashuArcade repository has been reorganized for better structure and simplicity.

## Key Changes

### 1. Games Directory
- **Old**: Games were in the root directory (`fishyfrens/`, `testgame/`)
- **New**: All games are now in `GAMES/` directory
  - `GAMES/fishyfrens/`
  - `GAMES/testgame/`

### 2. Single Virtual Environment
- **Old**: Separate venvs (`.venv_launcher/`, `fishyfrens/.venv/`, etc.)
- **New**: Single shared `venv/` for everything
  - Launcher uses `venv/`
  - All games use `venv/`
  - gamelib installed in `venv/`

### 3. Package Installation
All components are installed as editable packages:
```bash
pip install -e ./gamelib
pip install -e ./lnarcade
pip install -e ./GAMES/fishyfrens
```

### 4. Manifest Configuration
Games now set `"venv": null` in their manifest to use the shared venv:
```json
{
  "launcher": {
    "launch": {
      "venv": null,
      "command": "python",
      "args": ["-m", "fishyfrens"]
    }
  }
}
```

## Directory Structure

```
CashuArcade/
├── venv/                   # Shared virtual environment
├── arcade                  # Launcher script
├── fishy                   # Direct game launcher
├── lnarcade/               # Launcher code
├── gamelib/                # Shared library
├── GAMES/                  # All games here
│   ├── fishyfrens/
│   └── testgame/
├── docs/                   # Documentation
└── resources/              # Shared resources
```

## Benefits

1. **Simpler Setup**: One venv to manage instead of many
2. **Cleaner Root**: Games organized in GAMES/ folder
3. **Easier Development**: No switching between venvs
4. **Faster Installation**: Shared dependencies
5. **Better Organization**: Clear separation of concerns

## Migration Notes

If you have an existing setup:

1. Move games to GAMES/ directory
2. Delete individual game venvs
3. Create/use shared `venv/`
4. Reinstall packages:
   ```bash
   source venv/bin/activate
   pip install -e ./gamelib
   pip install -e ./GAMES/fishyfrens
   ```
5. Update manifests to set `"venv": null`

## Keeping gamelib Separate

gamelib remains a separate package (not merged into lnarcade) because:
- Games can use it independently
- Clear separation of launcher vs game utilities
- Easier to version and maintain
- Can be used by games outside this repo
