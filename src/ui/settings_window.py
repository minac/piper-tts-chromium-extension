"""Settings window for configuration."""

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, ttk

from src.logger import get_logger
from src.settings import Settings

logger = get_logger(__name__)


class SettingsWindow:
    """Dialog for application settings."""

    def __init__(self, settings: Settings, available_voices: list[str]):
        """Initialize SettingsWindow.

        Args:
            settings: Settings instance
            available_voices: List of available voice names
        """
        logger.info("creating_settings_window", voice_count=len(available_voices))
        self._settings = settings
        self._available_voices = available_voices

        # Create window
        self._window = tk.Toplevel()
        self._window.title("Settings")
        self._window.geometry("500x250")
        self._window.resizable(False, False)
        self._window.lift()
        self._window.attributes('-topmost', True)
        self._window.after_idle(self._window.attributes, '-topmost', False)

        # Variables for form fields
        self._voice_var = tk.StringVar()
        self._output_dir_var = tk.StringVar()

        # Load current settings
        self._load_settings()

        # Create UI
        self._create_widgets()
        logger.debug("settings_window_created")

    def _load_settings(self):
        """Load current settings into variables."""
        self._voice_var.set(self._settings.get("voice"))
        self._output_dir_var.set(self._settings.get("output_directory"))

    def _create_widgets(self):
        """Create all window widgets."""
        # Main frame with padding
        main_frame = tk.Frame(self._window, padx=25, pady=25, bg="#f5f5f7")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Voice selection
        voice_label = tk.Label(
            main_frame,
            text="Voice:",
            font=("SF Pro Text", 12),
            fg="#1d1d1f",
            bg="#f5f5f7",
            anchor="w",
        )
        voice_label.grid(row=0, column=0, sticky="w", pady=(0, 8))

        voice_combo = ttk.Combobox(
            main_frame,
            textvariable=self._voice_var,
            values=self._available_voices,
            state="readonly",
            font=("SF Pro Text", 12),
            width=35,
        )
        voice_combo.grid(row=0, column=1, columnspan=2, sticky="ew", pady=(0, 15))

        # Output directory
        output_label = tk.Label(
            main_frame,
            text="Output Directory:",
            font=("SF Pro Text", 12),
            fg="#1d1d1f",
            bg="#f5f5f7",
            anchor="w",
        )
        output_label.grid(row=1, column=0, sticky="w", pady=(0, 8))

        output_entry = tk.Entry(
            main_frame,
            textvariable=self._output_dir_var,
            font=("SF Pro Text", 12),
            relief=tk.SOLID,
            bd=1,
            highlightthickness=0,
        )
        output_entry.grid(row=1, column=1, sticky="ew", pady=(0, 15))

        browse_btn = tk.Button(
            main_frame,
            text="Browse...",
            command=self._browse_directory,
            font=("SF Pro Text", 11),
            relief=tk.FLAT,
            bd=0,
            bg="#e5e5ea",
            fg="#1d1d1f",
            padx=15,
            pady=5,
        )
        browse_btn.grid(row=1, column=2, padx=(8, 0), pady=(0, 15))

        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)

        # Button frame
        button_frame = tk.Frame(main_frame, bg="#f5f5f7")
        button_frame.grid(row=2, column=0, columnspan=3, pady=(15, 0))

        # Save button (Mac-style accent button)
        save_btn = tk.Button(
            button_frame,
            text="Save",
            command=self._on_save,
            bg="#007AFF",
            fg="white",
            font=("SF Pro Text", 13, "bold"),
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            padx=30,
            pady=8,
            activebackground="#0051D5",
            activeforeground="white",
        )
        save_btn.pack(side=tk.LEFT, padx=5)

        # Cancel button
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self._on_cancel,
            font=("SF Pro Text", 13),
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            bg="#e5e5ea",
            fg="#1d1d1f",
            padx=30,
            pady=8,
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)

    def _browse_directory(self):
        """Open directory browser."""
        directory = filedialog.askdirectory(
            initialdir=Path(self._output_dir_var.get()).expanduser(),
            title="Select Output Directory",
        )
        if directory:
            self._output_dir_var.set(directory)

    def _on_save(self):
        """Save settings and close."""
        # Update settings (speed is managed via tray menu now)
        self._settings.set("voice", self._voice_var.get())
        self._settings.set("output_directory", self._output_dir_var.get())

        # Save to file
        self._settings.save()

        # Close window
        self._window.destroy()

    def _on_cancel(self):
        """Cancel and close without saving."""
        self._window.destroy()

    def show(self):
        """Display the window."""
        logger.info("showing_settings_window")
        self._window.deiconify()
        self._window.focus_force()
        logger.debug("settings_window_visible")
