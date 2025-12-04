"""Tests for HotkeyManager class."""

import pytest

from src.hotkeys import HotkeyManager


class TestHotkeyManager:
    """Test suite for HotkeyManager."""

    def test_parse_hotkey_string(self):
        """Should parse 'ctrl+shift+p' to key combination."""
        manager = HotkeyManager()

        # Test single modifier + key
        result = manager.parse_hotkey("ctrl+p")
        assert "ctrl" in str(result).lower()
        assert "p" in str(result).lower()

        # Test multiple modifiers + key
        result = manager.parse_hotkey("ctrl+shift+p")
        assert "ctrl" in str(result).lower()
        assert "shift" in str(result).lower()
        assert "p" in str(result).lower()

    def test_register_hotkey_callback(self, mocker):
        """Should register callback for hotkey."""
        manager = HotkeyManager()
        callback = mocker.Mock()

        # Mock pynput GlobalHotKeys
        mock_listener = mocker.Mock()
        mocker.patch("src.hotkeys.GlobalHotKeys", return_value=mock_listener)

        manager.register("ctrl+p", callback)

        # Should have registered the hotkey
        assert "ctrl+p" in manager._hotkeys
        assert manager._hotkeys["ctrl+p"] == callback

    def test_unregister_hotkey(self, mocker):
        """Should remove hotkey binding."""
        manager = HotkeyManager()
        callback = mocker.Mock()

        # Mock pynput GlobalHotKeys
        mock_listener = mocker.Mock()
        mocker.patch("src.hotkeys.GlobalHotKeys", return_value=mock_listener)

        # Register then unregister
        manager.register("ctrl+p", callback)
        manager.unregister("ctrl+p")

        # Should be removed
        assert "ctrl+p" not in manager._hotkeys

    def test_update_hotkey_rebinds(self, mocker):
        """Should update existing hotkey binding."""
        manager = HotkeyManager()
        callback1 = mocker.Mock()
        callback2 = mocker.Mock()

        # Mock pynput GlobalHotKeys
        mock_listener = mocker.Mock()
        mocker.patch("src.hotkeys.GlobalHotKeys", return_value=mock_listener)

        # Register with first callback
        manager.register("ctrl+p", callback1)
        # Update with second callback
        manager.register("ctrl+p", callback2)

        # Should have updated callback
        assert manager._hotkeys["ctrl+p"] == callback2

    def test_invalid_hotkey_raises(self):
        """Should raise for invalid hotkey string."""
        manager = HotkeyManager()

        # Empty string
        with pytest.raises(ValueError):
            manager.parse_hotkey("")

        # Invalid format
        with pytest.raises(ValueError):
            manager.parse_hotkey("invalid")

        # No key, only modifiers
        with pytest.raises(ValueError):
            manager.parse_hotkey("ctrl+shift")

    def test_start_stop_listener(self, mocker):
        """Should start and stop the hotkey listener."""
        manager = HotkeyManager()

        # Mock pynput GlobalHotKeys
        mock_listener = mocker.Mock()
        mocker.patch("src.hotkeys.GlobalHotKeys", return_value=mock_listener)

        callback = mocker.Mock()
        manager.register("ctrl+p", callback)

        manager.start()
        mock_listener.start.assert_called_once()

        manager.stop()
        mock_listener.stop.assert_called_once()
