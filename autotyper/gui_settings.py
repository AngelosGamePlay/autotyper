# autotyper/gui_settings.py
import tkinter as tk
from tkinter import ttk, messagebox
from .settings import Settings

class SettingsGUI:
    def __init__(self, master, settings, on_save_callback):
        self.master = master
        self.settings = settings
        self.on_save_callback = on_save_callback
        master.title("Settings")
        master.geometry("400x650")  # Increased height
        master.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        # --- Notebook (Tabs) ---
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Typing Settings Tab
        self.typing_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.typing_frame, text='Typing')
        self.create_typing_widgets()

        # GUI Settings Tab
        self.gui_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.gui_frame, text='GUI')
        self.create_gui_widgets()

        # --- Buttons (Save and Restore Defaults) ---
        self.button_frame = ttk.Frame(self.master)  # Back to main master frame
        self.button_frame.pack(pady=10) # and pack

        self.save_button = ttk.Button(self.button_frame, text="Save", command=self.save_settings)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.restore_button = ttk.Button(self.button_frame, text="Restore Defaults", command=self.restore_defaults)
        self.restore_button.pack(side=tk.LEFT, padx=5)

    def create_typing_widgets(self):
        # Use grid with sticky options for better alignment
        row = 0  # Keep track of the row number

        ttk.Label(self.typing_frame, text="Vowel Error Rate:",
                  ).grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        self.vowel_error_rate_entry = ttk.Entry(self.typing_frame, width=10)
        self.vowel_error_rate_entry.grid(row=row, column=1, sticky=tk.EW, padx=5, pady=2)
        self.vowel_error_rate_entry.insert(0, self.settings.get_setting('Typing', 'vowel_error_rate'))
        row += 1

        ttk.Label(self.typing_frame, text="Consonant Error Rate:",
                  ).grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        self.consonant_error_rate_entry = ttk.Entry(self.typing_frame, width=10)
        self.consonant_error_rate_entry.grid(row=row, column=1, sticky=tk.EW, padx=5, pady=2)
        self.consonant_error_rate_entry.insert(0, self.settings.get_setting('Typing', 'consonant_error_rate'))
        row += 1

        ttk.Label(self.typing_frame, text="Word Pause Min:",
                  ).grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        self.word_pause_min_entry = ttk.Entry(self.typing_frame, width=10)
        self.word_pause_min_entry.grid(row=row, column=1, sticky=tk.EW, padx=5, pady=2)
        self.word_pause_min_entry.insert(0, self.settings.get_setting('Typing', 'word_pause_min'))
        row += 1

        ttk.Label(self.typing_frame, text="Word Pause Max:",
                  ).grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        self.word_pause_max_entry = ttk.Entry(self.typing_frame, width=10)
        self.word_pause_max_entry.grid(row=row, column=1, sticky=tk.EW, padx=5, pady=2)
        self.word_pause_max_entry.insert(0, self.settings.get_setting('Typing', 'word_pause_max'))
        row += 1

        ttk.Label(self.typing_frame, text="Punctuation Pause Min:",
                  ).grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        self.punctuation_pause_min_entry = ttk.Entry(self.typing_frame, width=10)
        self.punctuation_pause_min_entry.grid(row=row, column=1, sticky=tk.EW, padx=5, pady=2)
        self.punctuation_pause_min_entry.insert(0, self.settings.get_setting('Typing', 'punctuation_pause_min'))
        row += 1

        ttk.Label(self.typing_frame, text="Punctuation Pause Max:",
                  ).grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        self.punctuation_pause_max_entry = ttk.Entry(self.typing_frame, width=10)
        self.punctuation_pause_max_entry.grid(row=row, column=1, sticky=tk.EW, padx=5, pady=2)
        self.punctuation_pause_max_entry.insert(0, self.settings.get_setting('Typing', 'punctuation_pause_max'))
        row += 1

        ttk.Label(self.typing_frame, text="Wrong Char Delay Min:",
                  ).grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        self.wrong_char_delay_min_entry = ttk.Entry(self.typing_frame, width=10)
        self.wrong_char_delay_min_entry.grid(row=row, column=1, sticky=tk.EW, padx=5, pady=2)
        self.wrong_char_delay_min_entry.insert(0, self.settings.get_setting('Typing', 'wrong_char_delay_min'))
        row += 1

        ttk.Label(self.typing_frame, text="Wrong Char Delay Max:",
                  ).grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        self.wrong_char_delay_max_entry = ttk.Entry(self.typing_frame, width=10)
        self.wrong_char_delay_max_entry.grid(row=row, column=1, sticky=tk.EW, padx=5, pady=2)
        self.wrong_char_delay_max_entry.insert(0, self.settings.get_setting('Typing', 'wrong_char_delay_max'))
        row += 1

        ttk.Label(self.typing_frame, text="Backspace Delay Min:",
                  ).grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        self.backspace_delay_min_entry = ttk.Entry(self.typing_frame, width=10)
        self.backspace_delay_min_entry.grid(row=row, column=1, sticky=tk.EW, padx=5, pady=2)
        self.backspace_delay_min_entry.insert(0, self.settings.get_setting('Typing', 'backspace_delay_min'))
        row += 1

        ttk.Label(self.typing_frame, text="Backspace Delay Max:",
                  ).grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        self.backspace_delay_max_entry = ttk.Entry(self.typing_frame, width=10)
        self.backspace_delay_max_entry.grid(row=row, column=1, sticky=tk.EW, padx=5, pady=2)
        self.backspace_delay_max_entry.insert(0, self.settings.get_setting('Typing', 'backspace_delay_max'))
        row += 1

        ttk.Label(self.typing_frame, text="Break Frequency (chars):",
                  ).grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        self.break_frequency_entry = ttk.Entry(self.typing_frame, width=10)
        self.break_frequency_entry.grid(row=row, column=1, sticky=tk.EW, padx=5, pady=2)
        self.break_frequency_entry.insert(0, self.settings.get_setting('Typing', 'break_frequency'))
        row += 1

        ttk.Label(self.typing_frame, text="Break Duration Min (s):",
                  ).grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        self.break_duration_min_entry = ttk.Entry(self.typing_frame, width=10)
        self.break_duration_min_entry.grid(row=row, column=1, sticky=tk.EW, padx=5, pady=2)
        self.break_duration_min_entry.insert(0, self.settings.get_setting('Typing', 'break_duration_min'))
        row += 1

        ttk.Label(self.typing_frame, text="Break Duration Max (s):",
                  ).grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        self.break_duration_max_entry = ttk.Entry(self.typing_frame, width=10)
        self.break_duration_max_entry.grid(row=row, column=1, sticky=tk.EW, padx=5, pady=2)
        self.break_duration_max_entry.insert(0, self.settings.get_setting('Typing', 'break_duration_max'))
        row += 1

        # Allow the last row to expand, pushing everything else up
        self.typing_frame.grid_rowconfigure(row, weight=1)
        # Allow the entry column to expand
        self.typing_frame.grid_columnconfigure(1, weight=1)


    def create_gui_widgets(self):
        row = 0
         # Start Delay
        ttk.Label(self.gui_frame, text="Start Delay (s):",
                  ).grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.start_delay_entry = ttk.Entry(self.gui_frame, width=10)
        self.start_delay_entry.grid(row=row, column=1, sticky=tk.EW, padx=5, pady=5)
        self.start_delay_entry.insert(0, self.settings.get_setting('GUI', 'start_delay'))
        row+=1

        # Check for Updates (Checkbox)
        ttk.Label(self.gui_frame, text="Check for Updates on Startup:",
                  ).grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.check_for_updates_var = tk.BooleanVar()
        self.check_for_updates_var.set(self.settings.get_setting('GUI', 'check_for_updates') == "True")  # Compare with string "True"
        self.check_for_updates_checkbox = ttk.Checkbutton(self.gui_frame,
                                                            variable=self.check_for_updates_var)
        self.check_for_updates_checkbox.grid(row=row, column=1, sticky=tk.EW, padx=5, pady=5)
        row+=1
        self.gui_frame.grid_columnconfigure(1, weight=1) # Allow column to expand




    def save_settings(self):
        """Saves the entered settings and closes the window."""

        # Typing settings
        if self.settings.validate_setting('Typing', 'vowel_error_rate', self.vowel_error_rate_entry.get()):
            self.settings.set_setting('Typing', 'vowel_error_rate', self.vowel_error_rate_entry.get())
        else:
            messagebox.showerror("Error", "Invalid Vowel Error Rate")
            return

        if self.settings.validate_setting('Typing', 'consonant_error_rate', self.consonant_error_rate_entry.get()):
            self.settings.set_setting('Typing', 'consonant_error_rate', self.consonant_error_rate_entry.get())
        else:
            messagebox.showerror("Error", "Invalid Consonant Error Rate")
            return
        # ... (Repeat similar validation for all other settings) ...
        if self.settings.validate_setting('Typing', 'word_pause_min', self.word_pause_min_entry.get()):
            self.settings.set_setting('Typing', 'word_pause_min', self.word_pause_min_entry.get())
        else:
            messagebox.showerror("Error", "Invalid Word Pause Min")
            return
        if self.settings.validate_setting('Typing', 'word_pause_max', self.word_pause_max_entry.get()):
            self.settings.set_setting('Typing', 'word_pause_max', self.word_pause_max_entry.get())
        else:
            messagebox.showerror("Error", "Invalid Word Pause Max")
            return

        if self.settings.validate_setting('Typing', 'punctuation_pause_min', self.punctuation_pause_min_entry.get()):
          self.settings.set_setting('Typing', 'punctuation_pause_min', self.punctuation_pause_min_entry.get())
        else:
            messagebox.showerror("Error", "Invalid Punctuation Pause Min")
            return

        if self.settings.validate_setting('Typing', 'punctuation_pause_max', self.punctuation_pause_max_entry.get()):
          self.settings.set_setting('Typing', 'punctuation_pause_max', self.punctuation_pause_max_entry.get())
        else:
            messagebox.showerror("Error", "Invalid Punctuation Pause Max")
            return

        if self.settings.validate_setting('Typing', 'wrong_char_delay_min', self.wrong_char_delay_min_entry.get()):
            self.settings.set_setting('Typing', 'wrong_char_delay_min', self.wrong_char_delay_min_entry.get())
        else:
            messagebox.showerror("Error", "Invalid Wrong Char Delay Min")
            return
        if self.settings.validate_setting('Typing', 'wrong_char_delay_max', self.wrong_char_delay_max_entry.get()):
            self.settings.set_setting('Typing', 'wrong_char_delay_max', self.wrong_char_delay_max_entry.get())
        else:
            messagebox.showerror("Error", "Invalid Wrong Char Delay Max")
            return

        if self.settings.validate_setting('Typing', 'backspace_delay_min', self.backspace_delay_min_entry.get()):
            self.settings.set_setting('Typing', 'backspace_delay_min', self.backspace_delay_min_entry.get())
        else:
            messagebox.showerror("Error", "Invalid Backspace Delay Min")
            return
        if self.settings.validate_setting('Typing', 'backspace_delay_max', self.backspace_delay_max_entry.get()):
            self.settings.set_setting('Typing', 'backspace_delay_max', self.backspace_delay_max_entry.get())
        else:
            messagebox.showerror("Error", "Invalid Backspace Delay Max")
            return

        if self.settings.validate_setting('Typing', 'break_frequency', self.break_frequency_entry.get()):
            self.settings.set_setting('Typing', 'break_frequency', self.break_frequency_entry.get())
        else:
            messagebox.showerror("Error", "Invalid Break Frequency")
            return

        if self.settings.validate_setting('Typing', 'break_duration_min', self.break_duration_min_entry.get()):
            self.settings.set_setting('Typing', 'break_duration_min', self.break_duration_min_entry.get())
        else:
            messagebox.showerror("Error", "Invalid Break Duration Min")
            return

        if self.settings.validate_setting('Typing', 'break_duration_max', self.break_duration_max_entry.get()):
            self.settings.set_setting('Typing', 'break_duration_max', self.break_duration_max_entry.get())
        else:
            messagebox.showerror("Error", "Invalid Break Duration Max")
            return

        # GUI settings
        if self.settings.validate_setting('GUI', 'start_delay', self.start_delay_entry.get()):
            self.settings.set_setting('GUI', 'start_delay', self.start_delay_entry.get())
        else:
            messagebox.showerror("Error", "Invalid Start Delay")
            return

        #Check for updates setting
        self.settings.set_setting('GUI', 'check_for_updates', str(self.check_for_updates_var.get()))


        self.settings.save_settings()
        self.on_save_callback()
        self.master.destroy()



    def restore_defaults(self):
        """Restores settings to default values and updates the entry fields."""
        self.settings.reset_to_defaults()

        # Simplified and more robust way to update entry fields:
        for child in self.typing_frame.winfo_children():
            if isinstance(child, ttk.Entry):
                setting_name = child.grid_info()['row']  # Get row number
                if setting_name == 0:  # Vowel Error Rate
                    child.delete(0, tk.END)
                    child.insert(0, self.settings.get_setting('Typing', 'vowel_error_rate'))
                elif setting_name == 1: # Consonant Error Rate
                    child.delete(0, tk.END)
                    child.insert(0, self.settings.get_setting('Typing', 'consonant_error_rate'))
                elif setting_name == 2:
                    child.delete(0, tk.END)
                    child.insert(0, self.settings.get_setting('Typing', 'word_pause_min'))
                elif setting_name == 3:
                    child.delete(0, tk.END)
                    child.insert(0, self.settings.get_setting('Typing', 'word_pause_max'))
                elif setting_name == 4:
                    child.delete(0, tk.END)
                    child.insert(0, self.settings.get_setting('Typing', 'punctuation_pause_min'))
                elif setting_name == 5:
                    child.delete(0, tk.END)
                    child.insert(0, self.settings.get_setting('Typing', 'punctuation_pause_max'))
                elif setting_name == 6:
                    child.delete(0, tk.END)
                    child.insert(0, self.settings.get_setting('Typing', 'wrong_char_delay_min'))
                elif setting_name == 7:
                    child.delete(0, tk.END)
                    child.insert(0, self.settings.get_setting('Typing', 'wrong_char_delay_max'))
                elif setting_name == 8:
                    child.delete(0, tk.END)
                    child.insert(0, self.settings.get_setting('Typing', 'backspace_delay_min'))
                elif setting_name == 9:
                    child.delete(0, tk.END)
                    child.insert(0, self.settings.get_setting('Typing', 'backspace_delay_max'))
                elif setting_name == 10:
                    child.delete(0, tk.END)
                    child.insert(0, self.settings.get_setting('Typing', 'break_frequency'))
                elif setting_name == 11:
                    child.delete(0, tk.END)
                    child.insert(0, self.settings.get_setting('Typing', 'break_duration_min'))
                elif setting_name == 12:
                    child.delete(0, tk.END)
                    child.insert(0, self.settings.get_setting('Typing', 'break_duration_max'))
        for child in self.gui_frame.winfo_children():
            if isinstance(child, ttk.Entry):
                child.delete(0, tk.END)
                child.insert(0, self.settings.get_setting('GUI', 'start_delay'))
            elif isinstance(child, ttk.Checkbutton): #Handle checkbutton
                self.check_for_updates_var.set(self.settings.get_setting('GUI', 'check_for_updates')== "True")