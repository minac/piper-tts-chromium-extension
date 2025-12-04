"""Global keyboard shortcut management using pynput."""

from collections.abc import Callable

from pynput.keyboard import GlobalHotKeys


class HotkeyManager:
    """Manage global keyboard shortcuts."""

    def __init__(self):
        """Initialize HotkeyManager."""
        self._hotkeys: dict[str, Callable] = {}
        self._listener = None

    def parse_hotkey(self, hotkey_string: str) -> str:
        """Parse hotkey string into pynput format.

        Args:
            hotkey_string: Hotkey in format "ctrl+shift+p"

        Returns:
            Hotkey string in pynput format

        Raises:
            ValueError: If hotkey format is invalid
        """
        if not hotkey_string or not hotkey_string.strip():
            raise ValueError("Hotkey string cannot be empty")

        parts = hotkey_string.lower().strip().split("+")

        if len(parts) < 2:
            raise ValueError("Hotkey must have at least one modifier and one key")

        # Validate format: should have modifiers + key
        key_part = parts[-1]
        modifier_parts = parts[:-1]

        # Check if we have only modifiers (no actual key)
        valid_modifiers = {"ctrl", "shift", "alt", "cmd", "super"}
        if not key_part or key_part in valid_modifiers:
            raise ValueError("Hotkey must have a key (not just modifiers)")

        # Validate modifiers
        for modifier in modifier_parts:
            if modifier not in valid_modifiers:
                raise ValueError(f"Invalid modifier: {modifier}")

        # Convert to pynput format
        pynput_parts = []
        for part in parts[:-1]:  # modifiers
            if part == "ctrl":
                pynput_parts.append("<ctrl>")
            elif part == "shift":
                pynput_parts.append("<shift>")
            elif part == "alt":
                pynput_parts.append("<alt>")
            elif part in ["cmd", "super"]:
                pynput_parts.append("<cmd>")

        # Add the key
        pynput_parts.append(key_part)

        return "+".join(pynput_parts)

    def register(self, hotkey: str, callback: Callable):
        """Register a global hotkey.

        Args:
            hotkey: Hotkey string in format "ctrl+shift+p"
            callback: Function to call when hotkey is pressed
        """
        # Parse and validate hotkey (will raise if invalid)
        self.parse_hotkey(hotkey)

        # Store the callback
        self._hotkeys[hotkey] = callback

        # Rebuild listener with all hotkeys
        self._rebuild_listener()

    def unregister(self, hotkey: str):
        """Unregister a global hotkey.

        Args:
            hotkey: Hotkey string to remove
        """
        if hotkey in self._hotkeys:
            del self._hotkeys[hotkey]
            self._rebuild_listener()

    def start(self):
        """Start listening for hotkeys."""
        if self._listener:
            self._listener.start()

    def stop(self):
        """Stop listening for hotkeys."""
        if self._listener:
            self._listener.stop()

    def _rebuild_listener(self):
        """Rebuild the GlobalHotKeys listener with current hotkeys."""
        # Stop existing listener
        if self._listener:
            self._listener.stop()

        # Build hotkey mapping for pynput
        hotkey_mapping = {}
        for hotkey_str, callback in self._hotkeys.items():
            parsed = self.parse_hotkey(hotkey_str)
            hotkey_mapping[parsed] = callback

        # Create new listener
        if hotkey_mapping:
            self._listener = GlobalHotKeys(hotkey_mapping)
