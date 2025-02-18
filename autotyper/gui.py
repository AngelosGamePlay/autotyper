# autotyper/gui.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from .autotyper import Autotyper
from .settings import Settings
from .gui_settings import SettingsGUI
from threading import Thread

class AutotyperGUI:
    def __init__(self, master):
        self.master = master
        master.title("Realistic Autotyper")
        master.geometry("600x450")

        self.settings = Settings()
        self.autotyper = Autotyper(self.settings)
        self.typing_thread = None
        self.create_widgets()
        master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.check_for_updates()  # Check for updates on startup


    def create_widgets(self):
        # Text Input Area
        self.text_label = ttk.Label(self.master, text="Enter text to type:")
        self.text_label.pack(pady=5)

        self.text_area = scrolledtext.ScrolledText(self.master, width=60, height=10, wrap=tk.WORD)
        self.text_area.pack(pady=5)

        # WPM Input
        self.wpm_frame = ttk.Frame(self.master)
        self.wpm_frame.pack(pady=5)
        self.wpm_label = ttk.Label(self.wpm_frame, text="Target WPM:")
        self.wpm_label.pack(side=tk.LEFT, padx=5)
        self.wpm_entry = ttk.Entry(self.wpm_frame, width=5)
        self.wpm_entry.pack(side=tk.LEFT)
        self.wpm_entry.insert(0, "50")  # Default WPM

        # Button Frame
        self.button_frame = ttk.Frame(self.master)
        self.button_frame.pack(pady=10)

        # Start Button
        self.start_button = ttk.Button(self.button_frame, text="Start Typing", command=self.start_typing_thread)
        self.start_button.pack(side=tk.LEFT, padx=5)

        # Cancel Button
        self.cancel_button = ttk.Button(self.button_frame, text="Cancel", command=self.cancel_typing, state=tk.DISABLED)
        self.cancel_button.pack(side=tk.LEFT, padx=5)

        # Settings Button
        self.settings_button = ttk.Button(self.button_frame, text="Settings", command=self.open_settings)
        self.settings_button.pack(side=tk.LEFT, padx=5)

        # Status Label
        self.status_label = ttk.Label(self.master, text="")
        self.status_label.pack(pady=5)

        # Style (optional - for a slightly nicer look)
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#ccc")
        style.configure("TLabel", padding=6)
        style.configure("TEntry", padding=6)


    def start_typing(self):
        """Starts the autotyping process."""
        text = self.text_area.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text to type.")
            return

        try:
            wpm = int(self.wpm_entry.get())
            if wpm <= 0:
                raise ValueError("WPM must be a positive number.")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid WPM: {e}")
            return

        self.status_label.config(text=f"Starting in {self.settings.get_setting('GUI', 'start_delay')} seconds...")
        self.master.update()

        self.start_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)

        self.autotyper.start_typing(text, self.settings.get_setting('GUI', 'start_delay'), wpm)
        self.status_label.config(text="Typing complete!")
        self.reset_buttons()

    def start_typing_thread(self):
        """Starts the autotyping in a separate thread."""
        self.typing_thread = Thread(target=self.start_typing)
        self.typing_thread.start()

    def cancel_typing(self):
        """Cancels the typing process."""
        self.autotyper.cancel_typing()
        self.status_label.config(text="Typing cancelled!")
        self.reset_buttons()
        self.master.update()

    def reset_buttons(self):
        """Resets the buttons."""
        self.start_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)

    def on_closing(self):
        """Handles the window close event."""
        self.autotyper.cancel_typing()
        self.master.destroy()

    def open_settings(self):
        """Opens the settings window."""
        settings_window = tk.Toplevel(self.master)
        SettingsGUI(settings_window, self.settings, self.update_typing_settings)

    def update_typing_settings(self):
        try:
            wpm = int(self.wpm_entry.get())
            if wpm > 0:
                self.autotyper.calculate_typing_speed(wpm)
        except ValueError:
            pass

    def check_for_updates(self):
        """Checks for updates and prompts the user if available."""
        if self.settings.get_setting('GUI', 'check_for_updates') == 'False':  # String comparison
            return

        if self.autotyper.is_update_available():
            result = messagebox.askyesnocancel("Update Available",
                                            "A new version of Autotyper is available. Do you want to update now?\n\nClick 'Yes' to update automatically.\nClick 'No' to update later.\nClick 'Cancel' to disable update checks.",
                                            )
            if result is True:  # User clicked 'Yes'
                installer_path = self.autotyper.download_latest_installer()
                self.autotyper.run_installer(installer_path)


            elif result is False: # User clicked 'No'
                return # Do nothing
            else: # User clicked Cancel
              self.settings.set_setting('GUI', 'check_for_updates', 'False')  # Use string 'False'
              self.settings.save_settings()