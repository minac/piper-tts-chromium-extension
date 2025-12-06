"""System tray application with menu bar icon."""


import numpy as np
import pystray
from PIL import Image, ImageDraw
from pystray import Menu, MenuItem

from src.logger import get_logger

logger = get_logger(__name__)


class TrayApplication:
    """Menu bar application for TTS controls."""

    def __init__(self):
        """Initialize TrayApplication."""
        logger.info("initializing_tray_app")
        self._is_playing = False
        self._is_paused = False
        self._audio_data: np.ndarray | None = None
        self._sample_rate: int | None = None
        self._icon = None

        # Create menu
        menu = self._create_menu()

        # Create icon (template=True for macOS adaptive menu bar icons)
        icon_image = self._create_icon_image()
        self._icon = pystray.Icon(
            "piper-tts",
            icon_image,
            "Piper TTS Reader",
            menu=menu,
        )
        # Mark as template icon for macOS to auto-invert on dark menu bar
        if hasattr(self._icon, '_icon_class'):
            # pystray on macOS should handle template icons automatically
            pass
        logger.info("tray_app_initialized")

    def _create_icon_image(self) -> Image.Image:
        """Create TTS icon with speech bubble and sound waves.

        Returns:
            PIL Image for the tray icon (black on transparent for macOS template icon)
        """
        # Create a 44x44 icon @2x for retina displays (macOS will scale down)
        width = 44
        height = 44
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        dc = ImageDraw.Draw(image)

        # Scale factor for 2x resolution
        scale = 2

        # Speech bubble (rounded rectangle)
        # Main bubble body
        dc.rounded_rectangle(
            [2*scale, 2*scale, 15*scale, 12*scale],
            radius=2*scale,
            fill="black"
        )

        # Text lines inside bubble (3 lines)
        dc.rectangle([4*scale, 4*scale, 11*scale, 5*scale], fill="white")  # Top line
        dc.rectangle([4*scale, 7*scale, 10*scale, 8*scale], fill="white")  # Middle line
        dc.rectangle([4*scale, 10*scale, 9*scale, 11*scale], fill="white")  # Bottom line

        # Bubble tail (small triangle at bottom)
        dc.polygon([7*scale, 12*scale, 5*scale, 15*scale, 9*scale, 14*scale], fill="black")

        # Sound waves (3 curved lines at bottom right)
        dc.arc(
            [12*scale, 13*scale, 16*scale, 17*scale],
            start=270, end=90, fill="black", width=2*scale
        )
        dc.arc(
            [15*scale, 12*scale, 19*scale, 18*scale],
            start=270, end=90, fill="black", width=2*scale
        )
        dc.arc(
            [17*scale, 11*scale, 21*scale, 19*scale],
            start=270, end=90, fill="black", width=2*scale
        )

        return image

    def _create_menu(self) -> Menu:
        """Create the application menu.

        Returns:
            pystray Menu object

        Note:
            We use lambdas to wrap method calls so that when main.py replaces
            the methods (e.g., self._read_text = ...), the menu items will
            call the new implementations. Without lambdas, the menu would
            hold direct references to the original stub methods.
        """
        return Menu(
            MenuItem("Read Text...", lambda icon, item: self._read_text(icon, item)),
            Menu.SEPARATOR,
            MenuItem("Settings", lambda icon, item: self._open_settings(icon, item)),
            MenuItem("Quit", lambda icon, item: self._quit(icon, item)),
        )

    def _has_audio(self) -> bool:
        """Check if audio data is available.

        Returns:
            True if audio is ready for playback/export
        """
        return self._audio_data is not None and self._sample_rate is not None

    def _read_text(self, icon, item):
        """Open input window for text/URL entry.

        Args:
            icon: pystray Icon
            item: pystray MenuItem
        """
        logger.info("read_text_clicked")
        # TODO: Open input window
        pass

    def _play_pause(self, icon, item):
        """Start playback.

        Args:
            icon: pystray Icon
            item: pystray MenuItem
        """
        logger.info("play_clicked")
        self._is_playing = True
        self._is_paused = False
        logger.info("starting_playback")
        # TODO: Start audio player

    def _stop(self, icon, item):
        """Stop playback.

        Args:
            icon: pystray Icon
            item: pystray MenuItem
        """
        self._is_playing = False
        self._is_paused = False
        # TODO: Stop audio player

    def _open_settings(self, icon, item):
        """Open settings window.

        Args:
            icon: pystray Icon
            item: pystray MenuItem
        """
        logger.info("settings_clicked")
        # TODO: Open settings window
        pass

    def _quit(self, icon, item):
        """Quit the application.

        Args:
            icon: pystray Icon
            item: pystray MenuItem
        """
        if self._icon:
            self._icon.stop()

    def run(self):
        """Start the tray application (blocking).

        This blocks the calling thread. On macOS, this must be called
        from the main thread as it uses NSApplication internally.
        """
        logger.info("starting_tray_icon")
        if self._icon:
            self._icon.run()
        logger.info("tray_icon_stopped")

    def run_detached(self):
        """Start the tray application in detached mode.

        This is required on macOS when integrating with another mainloop
        (e.g., tkinter). It allows pystray to run alongside the other
        framework's event loop without blocking.

        See: https://pystray.readthedocs.io/en/latest/reference.html
        """
        logger.info("starting_tray_icon_detached")
        if self._icon:
            self._icon.run_detached()
        logger.debug("tray_icon_running_detached")

    def stop(self):
        """Stop the tray application.

        This can be called from any thread to stop the icon.
        """
        logger.info("stopping_tray_icon")
        if self._icon:
            self._icon.stop()
        logger.debug("tray_icon_stop_requested")
