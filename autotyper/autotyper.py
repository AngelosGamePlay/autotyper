# autotyper/autotyper.py
import time
import random
import requests  # Import the requests library
import json
import os
import subprocess
import sys
from pynput.keyboard import Key, Controller
from .settings import Settings
from .constants import VERSION # Import Version

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
        self.repo_owner = "AngelosGamePlay"  # Your GitHub username
        self.repo_name = "autotyper"  # Your repository name

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
        except Exception: # Catching *any* exception is generally bad practice, but acceptable here
            return 'x' #If any error, just return x

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

    def get_latest_release_version(self):
        """Fetches the latest release version from GitHub using the API."""
        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/latest"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
            return data['tag_name']
        except (requests.RequestException, KeyError, json.JSONDecodeError):
            return None  # Return None if any error occurs

    def is_update_available(self):
        """Checks if a newer version is available on GitHub."""
        latest_version = self.get_latest_release_version()
        if latest_version:
            #Compares version
            return latest_version > "v" + VERSION #Adds v to match tag format
        return False

    def download_latest_installer(self):
      """Downloads the latest installer .exe from GitHub releases."""
      latest_version = self.get_latest_release_version()
      if not latest_version:
          print("Error: Couldn't retrieve latest release version.")
          return None

      url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/latest"
      try:
          response = requests.get(url)
          response.raise_for_status()
          data = response.json()

          for asset in data['assets']:
              if asset['name'].endswith('.exe'):  # Assuming your installer is a .exe
                download_url = asset['browser_download_url']
                break # Find first exe
          else:
            print("No installer found in latest release.")
            return None

          # Download the installer
          print(f"Downloading installer from: {download_url}")
          installer_filename = f"AutotyperSetup-{latest_version}.exe" #Naming
          response = requests.get(download_url, stream=True) #Download
          response.raise_for_status()

          with open(installer_filename, 'wb') as f: # Write to file
              for chunk in response.iter_content(chunk_size=8192):
                  f.write(chunk)
          print("Installer downloaded successfully.")
          return installer_filename

      except requests.RequestException as e:
        print("Request error")
        return None
      except KeyError as e:
        print("Key error")
        return None
      except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

    def run_installer(self, installer_path):
      """Runs the downloaded installer."""
      if installer_path:
        try:
          subprocess.run([installer_path], check=True) # Run and check if it fails
          sys.exit(0)  # Exit the current process after launching the installer
        except subprocess.CalledProcessError as e:
            print("Called Process Error")
        except FileNotFoundError as e:
            print("File not found error")
        except Exception as e:
            print("Exception")
      else:
        print("Installer path is not valid.")