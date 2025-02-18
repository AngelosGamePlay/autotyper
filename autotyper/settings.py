# autotyper/settings.py
import configparser
import os
import sys

class Settings:
    def __init__(self, config_file='config.ini'):
        # Determine the base directory (works for both script and executable)
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            base_dir = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
        else:
            # Running as a script
            base_dir = os.path.dirname(os.path.abspath(__file__))

        self.config_file = os.path.join(base_dir, config_file)
        self.config = configparser.ConfigParser()


        # Define default settings
        self.defaults = {
            'Typing': {
                'vowel_error_rate': 0.01,
                'consonant_error_rate': 0.03,
                'word_pause_min': 0.15,
                'word_pause_max': 0.3,
                'punctuation_pause_min': 0.3,
                'punctuation_pause_max': 0.6,
                'wrong_char_delay_min': 0.02,
                'wrong_char_delay_max': 0.08,
                'backspace_delay_min': 0.1,
                'backspace_delay_max': 0.3,
                'break_frequency': 500,  # Characters per break
                'break_duration_min': 2.0,
                'break_duration_max': 5.0,
            },
            'GUI': {
                'start_delay': 5,
                'check_for_updates': "True"
            }
        }

        # Load settings from file, or create file with defaults
        self.load_settings()

    def load_settings(self):
        """Loads settings from the config file."""
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
        # Ensure all sections and options are present, add missing ones from defaults
        for section, options in self.defaults.items():
            if not self.config.has_section(section):
                self.config.add_section(section)
            for option, value in options.items():
                # Crucially, *always* get the default here, ensuring correct type
                if not self.config.has_option(section, option):
                    self.config.set(section, option, str(value))
        self.save_settings()

    def save_settings(self):
        """Saves settings to the config file."""
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def get_setting(self, section, option):
        """Retrieves a setting value, converting to the appropriate type.
           Returns the default value if any error occurs.
        """
        try:
            if option.endswith('_rate'):
                return self.config.getfloat(section, option)
            elif option.endswith('_delay') or option.endswith('_min') or option.endswith('_max') or option == 'break_frequency':
                return self.config.getfloat(section, option)
            elif option == 'start_delay':
                return self.config.getint(section, option)
            elif option == 'check_for_updates':
                return self.config.get(section, option)
            else:
                return self.config.get(section, option)  # Fallback
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            # Return default value if any error occurs
            return self.defaults[section][option]

    def set_setting(self, section, option, value):
        """Sets a setting value."""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, str(value))

    def reset_to_defaults(self):
        """Resets all settings to their default values."""
        for section, options in self.defaults.items():
            for option, value in options.items():
                self.set_setting(section, option, value)  # Use set_setting for consistency
        self.save_settings()

    def validate_setting(self, section, option, value):
        """Validates a setting value based on its expected type.
           Returns True if valid, False otherwise.
        """
        try:
            if option.endswith('_rate'):
                float(value)  # Check if it can be converted to float
                return 0.0 <= float(value) <= 1.0  # Rates should be between 0 and 1
            elif option.endswith('_delay') or option.endswith('_min') or option.endswith('_max') or option == 'break_frequency':
                float(value)
                return float(value) >= 0.0  # Delays should be non-negative
            elif option == 'start_delay':
                int(value)
                return int(value) >= 0
            elif option == 'check_for_updates':
                return value in ("True", "False")
            else:
                return True # No validation for other types (shouldn't be any)
        except ValueError:
            return False