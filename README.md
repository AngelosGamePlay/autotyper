# Realistic Autotyper

This is a Python application that simulates human typing on your computer, including realistic delays, errors, and corrections. It uses the `pynput` library for keyboard control and `Tkinter` for the graphical user interface.

## Features

*   **Realistic Typing Simulation:** Varies typing speed, introduces occasional errors (with corrections), and pauses realistically after words and punctuation. Typing speed is dynamically adjusted based on a target Words Per Minute (WPM).
*   **GUI:** A simple graphical user interface allows you to easily enter text, set the target WPM, and start the autotyping process.
*   **Configurable:** Settings like error rates and pause durations are customizable via a settings menu. Settings are saved to a `config.ini` file.
*   **Multi-threading:** The typing action occurs on a separate thread, preventing the GUI from freezing.
*   **Cancel:** You can cancel the typing process.
*   **Installer:** A Windows installer is provided for easy installation.
*    **Organized Project Structure:** Code is split into modules.

## Requirements

* **For Running the Installer:** Windows operating system.
* **For Building from Source:**
    *   Python 3.6 or higher
    *   `pynput` library

## Installation

### Using the Installer (Recommended)

1.  **Download the installer:** Download the latest installer (`AutotyperSetup.exe`) from the [Releases](<YOUR_GITHUB_RELEASES_URL>) page of this repository.  *(You'll replace `<YOUR_GITHUB_RELEASES_URL>` with the actual URL later.)*
2.  **Run the installer:** Double-click `AutotyperSetup.exe` and follow the on-screen instructions.

### Building from Source (For Developers)

1.  **Clone the repository:**

    ```bash
    git clone <your_repository_url>
    cd autotyper-project
    ```

2.  **Create a Virtual Environment (Recommended):**

    ```bash
    python3 -m venv venv
    venv\bin\activate  # On Windows
    source venv/bin/activate  # On macOS and Linux
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  After installation, run "Autotyper" from your Start Menu.
2.  **Enter the text** you want to type into the text area.
3.  **Enter the desired WPM.** The default is 50 WPM.
4.  **Click "Settings"** to adjust error rates, etc. Click "Save" in the settings window.
5.  **Click "Start Typing".** There will be a delay (configurable in Settings).
6.  **Click "Cancel"** to stop.

## Configuration File

The application uses a configuration file named `config.ini` to store your settings. This file is located in the same directory as the `Autotyper.exe` file. Do not delete this file.

## Important Notes

*   **Security:** Use this program responsibly and ethically.
*   **Permissions:** You may need accessibility/input monitoring permissions.

## Contributing

Feel free to submit pull requests with improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.  This means you can use, modify, and distribute the code freely, even for commercial purposes, as long as you include the original copyright notice and disclaimer.
