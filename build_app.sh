#!/bin/bash
# Build script for creating Speakeasy.app macOS bundle using PyInstaller
set -e

echo "Building Speakeasy.app for macOS..."
echo

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist
echo "✓ Cleaned"
echo

# Ensure dev dependencies are installed
echo "Installing dependencies (including PyInstaller)..."
uv sync --extra dev
echo "✓ Dependencies installed"
echo

# Build the app bundle
echo "Building app bundle with PyInstaller..."
uv run pyinstaller speakeasy.spec --clean --noconfirm
echo "✓ Build complete"
echo

# Check if build succeeded
if [ -d "dist/Speakeasy.app" ]; then
    echo "========================================="
    echo "SUCCESS! Speakeasy.app created"
    echo "========================================="
    echo
    echo "Location: dist/Speakeasy.app"
    echo "Size: $(du -sh dist/Speakeasy.app | cut -f1)"
    echo
    echo "To install:"
    echo "  1. Copy to Applications:"
    echo "     cp -r dist/Speakeasy.app /Applications/"
    echo
    echo "  2. Copy your voice files (.onnx + .json) to:"
    echo "     /Applications/Speakeasy.app/Contents/Resources/voices/"
    echo
    echo "  3. Configure auto-start (optional):"
    echo "     System Settings → General → Login Items → Add Speakeasy.app"
    echo
    echo "To test without installing:"
    echo "  open dist/Speakeasy.app"
    echo
    echo "The app runs in the background (menu bar only, no Dock icon)"
    echo
else
    echo "ERROR: Build failed - Speakeasy.app not found in dist/"
    exit 1
fi
