# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Speakeasy macOS app.

This builds a standalone .app bundle that:
- Runs in the background (no Dock icon)
- Can be added to Login Items
- Includes all dependencies and assets
"""

import sys
from pathlib import Path

block_cipher = None

# Project root
root = Path.cwd()

# Collect all source modules
a = Analysis(
    ['src/main.py'],
    pathex=[str(root)],
    binaries=[],
    datas=[
        # Include assets (icons)
        ('assets/icon.svg', 'assets'),
        ('assets/icon.png', 'assets'),
        # Include empty voices directory structure
        ('voices', 'voices'),
    ],
    hiddenimports=[
        # Ensure all src modules are included
        'src.main',
        'src.logger',
        'src.tts_engine',
        'src.audio_player',
        'src.text_extractor',
        'src.settings',
        'src.hotkeys',
        'src.tray',
        'src.ui.input_window',
        'src.ui.settings_window',
        # Critical runtime imports
        'piper',
        'onnxruntime',
        'sounddevice',
        'numpy',
        'PIL',
        'pystray',
        'bs4',
        'requests',
        'structlog',
        'svglib',
        'reportlab',
        'pynput',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'pytest',
        'pytest_mock',
        'pytest_cov',
        'ruff',
        'pyinstaller',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Speakeasy',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Speakeasy',
)

app = BUNDLE(
    coll,
    name='Speakeasy.app',
    icon='assets/icon.icns',
    bundle_identifier='com.speakeasy.tts',
    version='0.1.0',
    info_plist={
        'CFBundleName': 'Speakeasy',
        'CFBundleDisplayName': 'Speakeasy',
        'CFBundleGetInfoString': 'Text-to-speech reader for macOS',
        'CFBundleIdentifier': 'com.speakeasy.tts',
        'CFBundleVersion': '0.1.0',
        'CFBundleShortVersionString': '0.1.0',
        'NSHumanReadableCopyright': 'Copyright 2024',
        # Hide from Dock - runs as menu bar app only
        'LSUIElement': True,
        # Request microphone access (for audio playback)
        'NSMicrophoneUsageDescription': 'Speakeasy needs audio access for text-to-speech playback.',
        'NSHighResolutionCapable': True,
    },
)
