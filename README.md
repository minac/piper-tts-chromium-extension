# Speakeasy

macOS menu bar application for reading text and URLs aloud using Piper TTS.

## Features

- 🎙️ Offline text-to-speech using Piper TTS
  - Voice discovery from local `.onnx` files
  - Speed adjustment (0.5x - 2.0x)
  - WAV audio synthesis
- ⚡ Audio playback controls
  - Play, pause, resume, stop
  - Real-time speed adjustment
  - Position and duration tracking
  - Playback state management
  - Completion callbacks
- 🌐 Text extraction from URLs
  - URL detection with protocol validation
  - HTTP fetching with proper headers
  - HTML parsing and content cleaning
  - Whitespace normalization
  - Plain text passthrough
- ⚙️ Settings management
  - JSON persistence with defaults
  - Nested settings with dot notation
  - Voice, speed, output directory, shortcuts
- ⌨️ Global keyboard shortcuts
  - System-wide hotkey registration
  - Configurable key bindings
  - Parse "ctrl+shift+p" format
  - Runtime hotkey updates
- 🎨 Menu bar UI with system tray icon
  - pystray-based tray application
  - Simple menu with Read Text, Settings, and Quit
  - SVG icon with macOS template support (auto-inverts on dark menu bar)
- 🪟 UI Windows
  - Input window for text/URL entry
  - Settings window for configuration
  - tkinter/ttk-based dialogs
- 🔗 Full application integration
  - All components wired together
  - Event-driven architecture
  - Settings persistence
  - Hotkey bindings

## Requirements

- **macOS** (primary target platform)
- **Python 3.10 - 3.12** (recommended)
- **PortAudio** for audio output
- **uv** for package management
- **Piper voice models** (.onnx files)

## Installation

### 1. Install System Dependencies

```bash
# Install PortAudio
brew install portaudio

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone and Install Project

```bash
# Clone repository
git clone https://github.com/minac/speakeasy.git
cd speakeasy

# Install Python dependencies
uv sync --extra dev
```

### 3. Download Piper Voice Models

Download voice models from [Piper Huggingface](https://huggingface.co/rhasspy/piper-voices/tree/main)) and place them in the `voices/` directory:

```bash
# Create voices directory
mkdir -p voices

# Example: Download a voice model
cd voices
curl -L -o en_US-lessac-high.onnx https://huggingface.co/rhasspy/piper-voices/blob/main/en/en_US/lessac/high/en_US-lessac-high.onnx
curl -L -o en_US-lessac-high.onnx.json https://huggingface.co/rhasspy/piper-voices/blob/main/en/en_US/lessac/high/en_US-lessac-high.onnx.json
cd ..
```

## Running the Application

### Step-by-Step Guide

1. **Ensure voice models are installed** in the `voices/` directory
2. **Run the application**:
   ```bash
   uv run python -m src.main
   ```
3. **Look for the speaker icon** in your macOS menu bar (top-right)
4. **Click the icon** to access the menu

## Building for macOS

Create a standalone macOS app bundle that runs in the background and can start on login:

### Build the App

```bash
# Run the build script
./build_app.sh
```

This creates `dist/Speakeasy.app` - a complete macOS application bundle.

### Install the App

1. **Copy to Applications**:
   ```bash
   cp -r dist/Speakeasy.app /Applications/
   ```

2. **Add voice files**:
   - Copy your Piper voice files (`.onnx` + `.json`) to:
   - `/Applications/Speakeasy.app/Contents/Resources/voices/`

3. **Configure auto-start** (optional):
   - Open **System Settings** → **General** → **Login Items**
   - Click the **+** button
   - Select **Speakeasy.app** from Applications
   - The app will now start automatically on login

### Features of the Packaged App

- Runs in the background (no Dock icon)
- Lives in the menu bar only
- Self-contained with all dependencies
- Auto-start on login (when configured)
- Works like any native macOS app

### Manual Build (Alternative)

```bash
# Clean previous builds
rm -rf build dist

# Install dependencies
uv sync --extra dev

# Build with PyInstaller
uv run pyinstaller speakeasy.spec --clean --noconfirm
```

### Technical Details

The build process uses **PyInstaller** to create a native macOS app bundle:
- `speakeasy.spec` - PyInstaller configuration file
- All Python dependencies bundled automatically
- `LSUIElement=True` in Info.plist hides app from Dock
- Assets and voice directory structure included

## Development

```bash
# Run tests
uv run pytest -v

# Run tests with coverage
uv run pytest --cov=src --cov-report=term-missing

# Lint code
uv run ruff check src/ tests/

# Auto-fix linting issues
uv run ruff check --fix src/ tests/
```

## Project Structure

```
speakeasy/
├── src/
│   ├── main.py              # Application entry point & coordinator
│   ├── logger.py            # Structured logging
│   ├── tts_engine.py        # Piper TTS wrapper
│   ├── audio_player.py      # Audio playback controller
│   ├── text_extractor.py    # URL and text processing
│   ├── settings.py          # Settings management
│   ├── hotkeys.py           # Global keyboard shortcuts
│   ├── tray.py              # System tray application
│   └── ui/
│       ├── input_window.py  # Text/URL input dialog
│       └── settings_window.py # Configuration dialog
├── tests/
│   ├── test_tts_engine.py
│   ├── test_audio_player.py
│   ├── test_text_extractor.py
│   ├── test_settings.py
│   ├── test_hotkeys.py
│   ├── test_tray.py
│   ├── test_input_window.py
│   ├── test_settings_window.py
│   └── conftest.py
├── assets/
│   └── icon.svg             # Menu bar icon (SVG)
├── voices/                  # Piper voice models (.onnx)
├── config.json             # User settings (auto-generated)
├── pyproject.toml          # Project metadata and dependencies
├── CLAUDE.md               # Project instructions for Claude
└── IMPLEMENTATION_PLAN.md  # Detailed implementation roadmap
```

## CI/CD

GitHub Actions workflow runs on every PR:
- Linting with ruff
- Full test suite
- macOS environment
- Python 3.12

## License

See LICENSE file for details.
