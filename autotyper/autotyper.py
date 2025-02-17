# autotyper/autotyper.py
import time
import random
from pynput.keyboard import Key, Controller
from .settings import Settings  # Import Settings Class


class Autotyper:
    def __init__(self, settings=None):
        self.keyboard = Controller()
        self.vowels = "aeiouAEIOU"
        self.punctuation = ".?!,"
        self.cancelled = False
        self.typing_speed = None
        self.settings = settings or Settings()  # Use provided settings or create new

    def calculate_typing_speed(self, wpm):
        chars_per_minute = wpm * 6
        self.typing_speed = 60 / chars_per_minute

    def type_like_human(self, text):
        if self.typing_speed is None:
            raise ValueError("Typing speed not set.  Call calculate_typing_speed first.")

        for i, char in enumerate(text):
            if self.cancelled:
                return

            current_speed = random.uniform(self.typing_speed * 0.8, self.typing_speed * 1.2)

            error_rate = (self.settings.get_setting('Typing', 'vowel_error_rate')
                          if char in self.vowels else
                          self.settings.get_setting('Typing', 'consonant_error_rate'))

            if random.random() < error_rate:
                wrong_char = random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
                self.keyboard.press(wrong_char)
                self.keyboard.release(wrong_char)
                time.sleep(random.uniform(self.settings.get_setting('Typing', 'wrong_char_delay_min'),
                                        self.settings.get_setting('Typing', 'wrong_char_delay_max')))

                self.keyboard.press(Key.backspace)
                self.keyboard.release(Key.backspace)
                time.sleep(random.uniform(self.settings.get_setting('Typing', 'backspace_delay_min') * (self.typing_speed / 0.1),
                                        self.settings.get_setting('Typing', 'backspace_delay_max') * (self.typing_speed / 0.1)))

                self.keyboard.press(char)
                self.keyboard.release(char)
            else:
                self.keyboard.press(char)
                self.keyboard.release(char)

            if char != ' ' and char not in self.punctuation:
                time.sleep(current_speed)

            if char == ' ':
                time.sleep(random.uniform(self.settings.get_setting('Typing', 'word_pause_min') * (self.typing_speed / 0.1),
                                        self.settings.get_setting('Typing', 'word_pause_max') * (self.typing_speed / 0.1)))
            elif char in self.punctuation:
                time.sleep(random.uniform(self.settings.get_setting('Typing', 'punctuation_pause_min') * (self.typing_speed / 0.1),
                                        self.settings.get_setting('Typing', 'punctuation_pause_max') * (self.typing_speed / 0.1)))

    def start_typing(self, text, delay, wpm):
        self.cancelled = False
        self.calculate_typing_speed(wpm)
        time.sleep(delay)
        self.type_like_human(text)

    def cancel_typing(self):
        self.cancelled = True

    def update_settings(self):
        """Updates the internal settings used by the Autotyper."""
        # This method is crucial for applying changes made in the GUI.
        # We don't need to reload from the file, as the Settings object
        # itself has already been updated.
        pass  # All settings are already accessed dynamically, no update needed!