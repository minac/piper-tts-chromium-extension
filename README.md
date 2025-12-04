# Piper TTS Menu Bar Reader

macOS menu bar application for reading text and URLs aloud using Piper TTS.

## Features

### Completed ✓
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
- 📥 MP3 export
  - WAV to MP3 conversion
  - Smart filename generation from text
  - Timestamp-based naming
  - Conflict resolution
- ⌨️ Global keyboard shortcuts
  - System-wide hotkey registration
  - Configurable key bindings
  - Parse "ctrl+shift+p" format
  - Runtime hotkey updates
- 🎨 Menu bar UI with system tray icon
  - pystray-based tray application
  - Speed submenu (0.5x - 2.0x)
  - Dynamic Play/Pause/Resume text
  - Conditional Download menu item
  - Generated speaker icon
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
- **Python 3.10 - 3.12** (pydub audioop incompatibility with 3.13+)
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
git clone https://github.com/minac/piper-tts-chromium-extension.git
cd piper-tts-chromium-extension

# Install Python dependencies
uv sync --extra dev
```

### 3. Download Piper Voice Models

Download voice models from [Piper TTS releases](https://github.com/rhasspy/piper/releases) and place them in the `voices/` directory:

```bash
# Create voices directory
mkdir -p voices

# Example: Download a voice model
cd voices
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json
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
4. **Click the icon** to access the menu:
   - **Play**: Opens input window for text/URL entry
   - **Speed**: Adjust playback speed (0.5x - 2.0x)
   - **Download MP3**: Save current audio to file
   - **Settings**: Configure voice, speed, output directory
   - **Quit**: Exit the application

### Using the Application

**Reading Text:**
1. Click the speaker icon → Play (or press configured hotkey)
2. Enter text in the input window
3. Click "Read" - audio will synthesize and play automatically
4. Use menu to Pause/Resume/Stop playback

**Reading URLs:**
1. Click Play and paste a URL (e.g., article, Wikipedia page)
2. Click "Read" - text will be extracted and read aloud

**Changing Speed:**
1. While playing, click Speed submenu
2. Select desired speed (0.5x - 2.0x)
3. Playback restarts automatically with new speed

**Exporting to MP3:**
1. After reading text, click "Download MP3"
2. File saved to configured output directory (default: ~/Downloads)
3. Filename format: `first_5_words_YYYYMMDD_HHMMSS.mp3`

**Configuring Settings:**
1. Click Settings in menu
2. Choose voice from dropdown
3. Adjust default speed
4. Set output directory for MP3 exports
5. Click Save

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
piper-tts-chromium-extension/
├── src/
│   ├── main.py              # Application entry point
│   ├── tts_engine.py        # Piper TTS wrapper
│   ├── audio_player.py      # Audio playback controller
│   ├── text_extractor.py    # URL and text processing
│   ├── settings.py          # Settings management
│   ├── export.py            # MP3 export functionality
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
│   ├── test_export.py
│   ├── test_hotkeys.py
│   ├── test_tray.py
│   ├── test_input_window.py
│   ├── test_settings_window.py
│   └── conftest.py
├── voices/                  # Piper voice models (.onnx)
├── config.json             # User settings (auto-generated)
├── pyproject.toml          # Project metadata and dependencies
└── IMPLEMENTATION_PLAN.md  # Detailed implementation roadmap
```

## Implementation Status

See [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for detailed roadmap.

- ✅ **Stage 1**: Project Foundation & TTS Core
  - Project structure with proper packaging
  - PiperTTSEngine class with voice management
  - Speed adjustment and error handling
  - Test suite (8 tests, 94% coverage)

- ✅ **Stage 2**: Audio Playback Controller
  - AudioPlayer class with full controls
  - State management (STOPPED, PLAYING, PAUSED)
  - Thread-safe operations
  - Test suite (13 tests, 83% coverage)

- ✅ **Stage 3**: Text Extraction
  - TextExtractor class with URL detection
  - HTML parsing and content cleaning
  - Whitespace normalization
  - Test suite (8 tests, 95% coverage)

- ✅ **Stage 4**: Settings Management
  - Settings class with JSON persistence
  - Default configuration schema
  - Nested settings access with dot notation
  - Test suite (7 tests, 86% coverage)

- ✅ **Stage 5**: MP3 Export
  - AudioExporter class for WAV to MP3 conversion
  - Smart filename generation with timestamps
  - Conflict resolution for duplicate names
  - Test suite (5 tests, 97% coverage)

- ✅ **Stage 6**: Global Hotkeys
  - HotkeyManager class with pynput integration
  - Hotkey string parsing ("ctrl+shift+p" → pynput format)
  - Register/unregister hotkeys with callbacks
  - Validation for invalid formats
  - Test suite (6 tests, 91% coverage)

- ✅ **Stage 7**: System Tray Integration
  - TrayApplication class with menu bar icon
  - Speed submenu with 6 options (0.5x - 2.0x)
  - Dynamic Play/Pause/Resume menu text
  - Conditional Download MP3 menu item
  - PIL-generated speaker icon
  - Test suite (9 tests, 83% coverage)

- ✅ **Stage 8**: UI Windows
  - InputWindow class for text/URL entry
  - SettingsWindow class for configuration
  - tkinter/ttk-based dialogs
  - Test suite (17 tests, 95% coverage)

- ✅ **Stage 9**: Application Integration
  - PiperTTSApp main coordinator class
  - All components wired together
  - Event-driven architecture
  - Complete read flow implementation
  - Hotkey and tray menu integration

## Testing

All tests use mocking to avoid requiring actual voice files or audio hardware:
- **74 tests total** across nine stages
- **75% overall code coverage** (90% excluding main.py integration layer)
- Tests run in CI on every PR (macOS, Python 3.12)

## CI/CD

GitHub Actions workflow runs on every PR:
- Linting with ruff
- Full test suite
- macOS environment
- Python 3.12

## License

See LICENSE file for details.
