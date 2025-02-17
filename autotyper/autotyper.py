# autotyper/autotyper.py
import time
import random
from pynput.keyboard import Key, Controller
from .settings import Settings

class Autotyper:
    def __init__(self, settings=None):
        self.keyboard = Controller()
        self.vowels = "aeiouAEIOU"
        self.punctuation = ".?!,"
        self.cancelled = False
        self.typing_speed = None
        self.settings = settings or Settings()
        self.keyboard_layout = self._create_keyboard_layout()
        self.chars_typed_since_break = 0  # Track characters typed

    def _create_keyboard_layout(self):
        """Creates a dictionary representing the QWERTY keyboard layout."""
        layout = {
            'q': 'wa', 'w': 'qase', 'e': 'wsdr', 'r': 'edft', 't': 'rfgy', 'y': 'tghu',
            'u': 'yhji', 'i': 'ujko', 'o': 'iklp', 'p': 'ol',
            'a': 'qwsz', 's': 'awedxz', 'd': 'swerfcx', 'f': 'dertgv', 'g': 'frthvb',
            'h': 'gtyjbn', 'j': 'huyknm', 'k': 'jiolm', 'l': 'kop',
            'z': 'asx', 'x': 'zsdc', 'c': 'xdfv', 'v': 'cfgb', 'b': 'vghn', 'n': 'bhjm',
            'm': 'njk',
            '1': '2q', '2': '13wq', '3': '24ew', '4': '35re', '5': '46tr', '6': '57ty',
            '7': '68uy', '8': '79iu', '9': '80oi', '0': '9p',
            '-': '0p', '=': '-',
            '`': '1', '~': '`1', '!': '`12q', '@':'123wq', '#':'234ew', '$':'345re',
            '%': '456tr', '^':'567ty', '&':'678uy', '*':'789iu', '(':'890oi', ')':'90p',
            '_':'-0p', '+':'-=',
            ',': 'ml', '.': ',m', '/': '.',
            ' ': 'cvbnm'  # Spacebar neighbors
        }
        #Add uppercase
        uppercase_layout = {}
        for char, neighbors in layout.items():
            uppercase_layout[char.upper()] = neighbors.upper()
        layout.update(uppercase_layout) # Merge
        return layout

    def get_nearby_char(self, char):
        """Returns a random neighboring character or the original character."""
        try:
            neighbors = self.keyboard_layout.get(char)
            if neighbors:
                return random.choice(neighbors)
            else:
                return char  # Return original if no neighbors (e.g., special chars)
        except AttributeError: #If keyboard_layout not yet initialized (e.g. settings menu)
            return 'x'

    def calculate_typing_speed(self, wpm):
        chars_per_minute = wpm * 6
        self.typing_speed = 60 / chars_per_minute

    def type_like_human(self, text):
        if self.typing_speed is None:
            raise ValueError("Typing speed not set. Call calculate_typing_speed first.")

        for i, char in enumerate(text):
            if self.cancelled:
                return

            current_speed = random.uniform(self.typing_speed * 0.8, self.typing_speed * 1.2)

            if char == '\n':
                self.keyboard.press(Key.enter)
                self.keyboard.release(Key.enter)
                time.sleep(random.uniform(self.settings.get_setting('Typing', 'word_pause_min') * (self.typing_speed / 0.1),
                                        self.settings.get_setting('Typing', 'word_pause_max') * (self.typing_speed / 0.1)))
                continue

            error_rate = (self.settings.get_setting('Typing', 'vowel_error_rate')
                          if char in self.vowels else
                          self.settings.get_setting('Typing', 'consonant_error_rate'))

            if random.random() < error_rate:
                # Simulate hitting a nearby key
                wrong_char = self.get_nearby_char(char)  # Get nearby char
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

            if char != ' ' and char not in self.punctuation and char != '\n':
                time.sleep(current_speed)

            if char == ' ':
                time.sleep(random.uniform(self.settings.get_setting('Typing', 'word_pause_min') * (self.typing_speed / 0.1),
                                        self.settings.get_setting('Typing', 'word_pause_max') * (self.typing_speed / 0.1)))
            elif char in self.punctuation:
                time.sleep(random.uniform(self.settings.get_setting('Typing', 'punctuation_pause_min') * (self.typing_speed / 0.1),
                                        self.settings.get_setting('Typing', 'punctuation_pause_max') * (self.typing_speed / 0.1)))

            # --- Break Logic ---
            self.chars_typed_since_break += 1
            if self.chars_typed_since_break >= self.settings.get_setting('Typing', 'break_frequency'):
                self.take_break()



    def take_break(self):
        """Takes a break with a random duration based on settings."""
        duration = random.uniform(self.settings.get_setting('Typing', 'break_duration_min'),
                                  self.settings.get_setting('Typing', 'break_duration_max'))
        time.sleep(duration)
        self.chars_typed_since_break = 0  # Reset character count


    def start_typing(self, text, delay, wpm):
        self.cancelled = False
        self.chars_typed_since_break = 0 # Reset
        self.calculate_typing_speed(wpm)
        time.sleep(delay)
        self.type_like_human(text)

    def cancel_typing(self):
        self.cancelled = True

    def update_settings(self):
        pass