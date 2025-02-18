# Realistic Autotyper

This is a Python application that simulates human typing on your computer, including realistic delays, errors, and corrections. It uses the `pynput` library for keyboard control and `Tkinter` for the graphical user interface.

## Features

*   **Realistic Typing Simulation:** Varies typing speed, introduces occasional errors (with corrections), and pauses realistically after words, punctuation, and newlines. Typing speed is dynamically adjusted based on a target Words Per Minute (WPM).
*   **GUI:** A simple graphical user interface allows you to easily enter text, set the target WPM, load text from files, and paste text from the clipboard.
*   **Configurable:** Settings like error rates, pause durations, break frequency, break duration, and the start/resume delay are customizable via a settings menu. Settings are saved to a `config.ini` file.
*   **Multi-threading:** The typing action occurs on a separate thread, preventing the GUI from freezing.
*   **Start/Pause/Resume/Cancel:** You can start, pause, resume, and cancel the typing process using a single, context-aware button.
*   **Automatic Updates:** The application checks for updates on startup and prompts you to download and run the new installer if a newer version is available. You can disable update checks in the settings.
*   **Installer:** A Windows installer is provided for easy installation.
*   **Organized Project Structure:** Code is split into modules.
*   **Nearby Key Errors:** Simulates making mistakes by pressing on a nearby key.
*   **Progress Bar:** A progress bar shows the percentage of text typed.
*   **Estimated Time Remaining:** Displays an estimate of the time remaining to complete typing.
*   **Tooltips:**  Hover over GUI elements for helpful hints.
*   **Always on Top:** The application window stays on top of other windows.

## Requirements

*   **For Running the Installer:** Windows operating system.
*   **For Building from Source:**
    *   Python 3.6 or higher
    *   `pynput` library
    *   `requests` library

## Installation

### Using the Installer (Recommended)

1.  **Download the installer:** Download the latest installer (`AutotyperSetup.exe`) from the [Releases](https://github.com/AngelosGamePlay/autotyper/releases) page of this repository.
2.  **Run the installer:** Double-click `AutotyperSetup.exe` and follow the on-screen instructions. The installer will prompt you to uninstall any previous versions of Autotyper.

### Building from Source (For Developers)

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/PilotScript/autotyper.git
    cd autotyper-project
    ```

2.  **Create a Virtual Environment (Recommended):**

    ```bash
    python3 -m venv venv
    venv\Scripts\activate  # On Windows
    source venv/bin/activate  # On macOS and Linux
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  After installation, run "Autotyper" from your Start Menu.
2.  **Enter the text** you want to type into the text area, or:
    *   **Load from File:** Click the "Load from File" button to load text from a `.txt` file.
    *   **Paste from Clipboard:** Click the "Paste from Clipboard" button to paste text.
3.  **Enter the desired WPM.** The default is 50 WPM.  You can change the WPM while typing is paused.
4.  **Click "Settings"** to adjust error rates, pause durations, break settings, and other settings. Click "Save" in the settings window.
5.  **Click "Start Typing".**  There will be a delay (configurable in Settings) before typing begins. The button will change to "Pause".
6.  **Click "Pause"** to pause typing. The button will change to "Resume".  You can adjust the WPM while paused.
7.  **Click "Resume"** to resume typing with a configurable delay.  The WPM and time remaining will be recalculated based on the remaining text.
8.  **Click "Cancel"** to stop typing.

## Configuration File

The application uses a configuration file named `config.ini` to store your settings. This file is located in the same directory as the `Autotyper.exe` file. Do not delete this file.

## Important Notes

*   **Security:** Use this program responsibly and ethically.
*   **Permissions:** You may need accessibility/input monitoring permissions.

## Contributing

Feel free to submit pull requests with improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.  This means you can use, modify, and distribute the code freely, even for commercial purposes, as long as you include the original copyright notice and disclaimer.
