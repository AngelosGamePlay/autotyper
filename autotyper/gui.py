# autotyper/gui.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
# import tkinter.tix as tix  # For more advanced tooltips (optional)
from .autotyper import Autotyper
from .settings import Settings
from .gui_settings import SettingsGUI
from threading import Thread
import time  # Add this line!

class AutotyperGUI:
    def __init__(self, master):
        self.master = master
        master.title("Realistic Autotyper")
        master.geometry("600x600")  # Adjusted for time remaining

        self.settings = Settings()
        self.autotyper = Autotyper(self.settings)
        self.autotyper.master = master # Pass master to Autotyper.
        self.typing_thread = None
        # --- Tooltips (using a simple approach) ---
        self.tooltips = {}  # Store tooltips *BEFORE* create_widgets
        self.create_widgets()
        master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.create_tooltips() # Call create_tooltips *AFTER* creating widgets
        self.check_for_updates()
        self.update_timer_id = None #This stores the after id, so we can cancel it


    def create_widgets(self):
        # Text Input Area
        self.text_label = ttk.Label(self.master, text="Enter text to type or load from file:")
        self.text_label.pack(pady=5)

        self.text_area = scrolledtext.ScrolledText(self.master, width=60, height=10, wrap=tk.WORD)
        self.text_area.pack(pady=5)

        # --- File Load Button ---
        self.load_button = ttk.Button(self.master, text="Load from File", command=self.load_text_from_file)
        self.load_button.pack(pady=5)
        self.tooltips[self.load_button] = "Load text from a .txt file." # Tooltip

        # --- Paste from Clipboard Button ---
        self.paste_button = ttk.Button(self.master, text="Paste from Clipboard", command=self.paste_from_clipboard)
        self.paste_button.pack(pady=5)
        self.tooltips[self.paste_button] = "Paste text from the clipboard."

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

        # Start/Pause/Resume Button (Combined)
        self.start_pause_button = ttk.Button(self.button_frame, text="Start Typing", command=self.start_typing_thread)
        self.start_pause_button.pack(side=tk.LEFT, padx=5)


        # Cancel Button
        self.cancel_button = ttk.Button(self.button_frame, text="Cancel", command=self.cancel_typing, state=tk.DISABLED)
        self.cancel_button.pack(side=tk.LEFT, padx=5)

        # Settings Button
        self.settings_button = ttk.Button(self.button_frame, text="Settings", command=self.open_settings)
        self.settings_button.pack(side=tk.LEFT, padx=5)


        # Status Label
        self.status_label = ttk.Label(self.master, text="")
        self.status_label.pack(pady=5)

        # --- Progress Bar ---
        self.progress_var = tk.IntVar()
        self.progress_bar = ttk.Progressbar(self.master, variable=self.progress_var, maximum=100)
        # Initially hide the progress bar
        self.progress_bar.pack_forget()  # Start hidden!

        # --- Time Remaining Label ---
        self.time_remaining_label = ttk.Label(self.master, text="")
        self.time_remaining_label.pack(pady=5)

        # Style (optional - for a slightly nicer look)
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#ccc")
        style.configure("TLabel", padding=6)
        style.configure("TEntry", padding=6)


    def start_typing(self):
        """Starts the autotyping process (called by the thread)."""
        # Get the text and WPM *before* the delay
        text = self.text_area.get("1.0", tk.END).strip()
        try:
            wpm = int(self.wpm_entry.get())
            if wpm <= 0:
                raise ValueError("WPM must be a positive number.")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid WPM: {e}")
            self.reset_buttons()  # Reset buttons on error
            return

        # The actual typing happens *after* the delay, within the thread.
        self.autotyper.start_typing(text, 0, wpm, self.progress_var)  # delay is now 0
        self.status_label.config(text="Typing complete!")
        self.progress_var.set(0)  # Reset progress bar
        self.reset_buttons()
        self.time_remaining_label.config(text="") # Clear time
        if self.update_timer_id: #Disable timer
            self.master.after_cancel(self.update_timer_id)
        self.progress_bar.pack_forget() # Hide again after completion


    def start_typing_thread(self):
        """Starts the autotyping in a separate thread."""

        # --- UI Setup (BEFORE the delay) ---
        text = self.text_area.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text to type.")
            return
        try:
            wpm = int(self.wpm_entry.get())
            if wpm <= 0:
                raise ValueError("WPM must be a positive number.")
        except ValueError:
            messagebox.showerror("Error", f"Invalid WPM")
            return

        self.status_label.config(text=f"Starting in {self.settings.get_setting('GUI', 'start_delay')} seconds...")
        self.master.update() # Force update

        self.start_pause_button.config(text="Pause")  # Change button text
        self.start_pause_button.config(command=self.toggle_pause_resume) #Change command
        self.cancel_button.config(state=tk.NORMAL)
        self.settings_button.config(state=tk.DISABLED)
        self.text_area.config(state=tk.DISABLED)
        self.wpm_entry.config(state=tk.DISABLED)
        self.load_button.config(state=tk.DISABLED) # Disable load button
        self.paste_button.config(state=tk.DISABLED)  # Disable paste button
        self.progress_bar.pack(fill=tk.X, padx=10, pady=5) # Show progress bar

        # --- Delay (using Tkinter's after) ---
        delay_ms = int(self.settings.get_setting('GUI', 'start_delay') * 1000)  # Get delay in milliseconds
        self.master.after(delay_ms, self._start_typing_thread)  # Call _start_typing_thread after delay



    def _start_typing_thread(self):
        """Internal method to actually start the typing thread (called after the delay)."""
        self.typing_thread = Thread(target=self.start_typing)
        self.typing_thread.daemon = True  # Set the thread as a daemon thread
        self.typing_thread.start()
        self.update_time_remaining() # NOW we start the timer

    def toggle_pause_resume(self):
        """Toggles between pausing and resuming the typing."""
        if self.autotyper.paused:
            # Resume logic
            self.start_pause_button.config(text="Pause")
            delay = self.settings.get_setting('GUI', 'start_delay')
            self.status_label.config(text=f"Resuming in {delay} seconds...")
            self.master.update()  # Force GUI update to show the message immediately
            # Schedule _resume_after_delay to start AFTER the delay
            self.master.after(int(delay * 1000), self._resume_after_delay)

        else:
            # Pause logic
            self.autotyper.pause_typing()
            self.start_pause_button.config(text="Resume")
            self.status_label.config(text="Typing paused...")
            # Enable WPM entry while paused:
            self.wpm_entry.config(state=tk.NORMAL)
            if self.update_timer_id:
                self.master.after_cancel(self.update_timer_id)  # Stop timer updates
            self.master.update()

    def _resume_after_delay(self):
        """Resumes typing and restarts the time remaining updates (called AFTER delay)."""
        # Get remaining text and recalculate
        remaining_text = self.text_area.get("1.0", tk.END).strip()[len(self.autotyper.text_typed_so_far):]
        try:
            wpm = int(self.wpm_entry.get())
            if wpm > 0:
                self.autotyper.calculate_typing_speed(wpm)
                self.autotyper.total_delay = self.autotyper.calculate_total_delay(remaining_text)
                self.autotyper.start_time = time.time()  # Reset start time
        except ValueError: # If error in WPM
            messagebox.showerror("Error", "Invalid WPM. Please enter a positive number.")
            self.reset_buttons()
            return
        self.autotyper.resume_typing()  # NOW we resume
        self.update_time_remaining()   # AND restart the timer
        self.wpm_entry.config(state=tk.DISABLED) #Disable after resuming

    def cancel_typing(self):
        """Cancels the typing process."""
        self.autotyper.cancel_typing()
        self.status_label.config(text="Typing cancelled!")
        self.reset_buttons()  # This will reset to "Start Typing"
        self.progress_var.set(0)  # Reset progress bar
        self.master.update()
        self.time_remaining_label.config(text="") # Clear
        if self.update_timer_id: # Cancel timer
            self.master.after_cancel(self.update_timer_id)
        self.progress_bar.pack_forget()  # Hide on cancel

    def reset_buttons(self):
        """Resets the buttons to their initial states."""
        self.start_pause_button.config(text="Start Typing")
        self.start_pause_button.config(command=self.start_typing_thread)  # Reset command
        self.cancel_button.config(state=tk.DISABLED)
        self.settings_button.config(state=tk.NORMAL)
        self.text_area.config(state=tk.NORMAL)
        self.wpm_entry.config(state=tk.NORMAL)
        self.load_button.config(state=tk.NORMAL)  # Enable load button
        self.paste_button.config(state=tk.NORMAL)  # Enable paste button


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
      except ValueError as e:
        pass

    def check_for_updates(self):
        """Checks for updates and prompts the user if available."""
        if self.settings.get_setting('GUI', 'check_for_updates') == 'False':
            return

        if self.autotyper.is_update_available():
            result = messagebox.askyesnocancel("Update Available",
                                            "A new version of Autotyper is available. Do you want to update now?\n\nClick 'Yes' to update automatically.\nClick 'No' to update later.\nClick 'Cancel' to disable update checks.",
                                            )
            if result is True:
                installer_path = self.autotyper.download_latest_installer()
                self.autotyper.run_installer(installer_path)


            elif result is False:
                return
            else:
              self.settings.set_setting('GUI', 'check_for_updates', 'False')
              self.settings.save_settings()

    def create_tooltips(self):
        """Creates tooltips for GUI elements."""
        self.tooltips[self.text_area] = "Enter the text you want the Autotyper to type, or load from a file."
        self.tooltips[self.wpm_entry] = "Set the target typing speed in Words Per Minute (WPM)."
        self.tooltips[self.start_pause_button] = "Start, pause, or resume the autotyping process."
        self.tooltips[self.cancel_button] = "Cancel the autotyping process."
        self.tooltips[self.settings_button] = "Open the settings window to customize Autotyper."
        self.tooltips[self.status_label] = "Status messages will appear here."
        self.tooltips[self.load_button] = "Load text from a .txt file."
        self.tooltips[self.paste_button] = "Paste text from the clipboard."
        self.tooltips[self.progress_bar] = "Progress of the typing."
        self.tooltips[self.time_remaining_label] = "The estimated time remaining to finish typing."
        # Add tooltips for settings in SettingsGUI as well

        for widget, text in self.tooltips.items():
            widget.bind("<Enter>", lambda event, w=widget, t=text: self.show_tooltip(event, w, t))
            widget.bind("<Leave>", self.hide_tooltip)

        self.tooltip_label = tk.Label(self.master, text="", background="#ffffe0", relief="solid", borderwidth=1) #Label
        self.tooltip_label.pack_forget() #Start hidden

    def show_tooltip(self, event, widget, text):
        """Displays a tooltip."""
        x = widget.winfo_rootx() + 20
        y = widget.winfo_rooty() + widget.winfo_height() + 5
        self.tooltip_label.config(text=text)
        self.tooltip_label.place(x=x, y=y)


    def hide_tooltip(self, event):
        """Hides the tooltip."""
        self.tooltip_label.pack_forget() # Hide
        self.tooltip_label.place_forget()

    def load_text_from_file(self):
        """Loads text from a file into the text area, handling various encodings."""
        file_path = filedialog.askopenfilename(
            title="Select a Text File",
            filetypes=[("All Files", "*.*")]  # Remove specific text file filter
        )
        if file_path:
            try:
                # Try UTF-8 first (most common)
                with open(file_path, "r", encoding="utf-8") as file:
                    text = file.read()
                    self.text_area.delete("1.0", tk.END)  # Clear current text
                    self.text_area.insert("1.0", text)   # Insert loaded text
                    self.status_label.config(text=f"Loaded text from: {file_path}")
                    return  # Success! Exit the function.

            except UnicodeDecodeError:
                # If UTF-8 fails, try other encodings
                try:
                    # Try the system's default encoding (often ANSI/Windows-1252 on Windows)
                    with open(file_path, "r", encoding=None) as file:  # encoding=None uses the system default
                        text = file.read()
                        self.text_area.delete("1.0", tk.END)
                        self.text_area.insert("1.0", text)
                        self.status_label.config(text=f"Loaded text from: {file_path}")
                        return

                except UnicodeDecodeError:
                    try:
                        # Try UTF-16 (less common, but still possible)
                        with open(file_path, "r", encoding="utf-16") as file:
                            text = file.read()
                            self.text_area.delete("1.0", tk.END)
                            self.text_area.insert("1.0", text)
                            self.status_label.config(text=f"Loaded text from: {file_path}")
                            return

                    except UnicodeDecodeError:
                        # If all encodings fail, show an error
                        messagebox.showerror("Error", "Could not decode the file.  It may not be a plain text file or may use an unsupported encoding.")
                        self.status_label.config(text="Error loading file.")
                    except Exception as e: # Catch any other error
                        messagebox.showerror("Error", f"Could not load file:\n{e}")
                        self.status_label.config(text="Error loading file.")
                except Exception as e: # Catch any other error
                    messagebox.showerror("Error", f"Could not load file:\n{e}")
                    self.status_label.config(text="Error loading file.")
            except Exception as e:  # Catch other exceptions (e.g., FileNotFoundError)
                messagebox.showerror("Error", f"Could not load file:\n{e}")
                self.status_label.config(text="Error loading file.")

    def paste_from_clipboard(self):
        """Pastes text from the clipboard into the text area."""
        try:
            text = self.master.clipboard_get()
            self.text_area.delete("1.0", tk.END)  # Clear current text
            self.text_area.insert("1.0", text)   # Insert clipboard text
            self.status_label.config(text="Text pasted from clipboard.")
        except tk.TclError:
            messagebox.showerror("Error", "Clipboard is empty or contains non-text data.")
            self.status_label.config(text="Error pasting from clipboard.")

    def update_time_remaining(self):
        """Updates the time remaining label periodically."""
        if not self.autotyper.paused:  # Only update if not paused
            remaining = self.autotyper.get_remaining_time()
            minutes = int(remaining // 60)
            seconds = int(remaining % 60)
            self.time_remaining_label.config(text=f"Estimated Time Remaining: {minutes:02d}:{seconds:02d}")
        self.update_timer_id = self.master.after(1000, self.update_time_remaining)  # Update every 1 second (1000ms)