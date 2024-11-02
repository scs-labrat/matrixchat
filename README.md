# Matrix Chat CLI

Matrix Chat CLI is a peer-to-peer, Matrix-inspired command-line chat and video application. The interface allows users to manage peer connections, start Matrix-style ASCII video feeds, and send real-time messages in a simple, colorful CLI environment.

## Features
- **Peer Management**: Easily add, view, and select peers for communication.
- **Matrix-style Video**: Stream a Matrix-style ASCII video feed from your webcam.
- **Real-time Chat**: Send and receive text messages between selected peers.
- **Test Mode**: Preview the Matrix-style video feed locally.
- **Separate Terminal Sessions**: Launch the video and chat sessions in separate terminals for a clean, organized experience.

## Requirements
- Python 3.6 or higher
- `colorama` and `pyfiglet` for colorful CLI and ASCII banners
- OpenCV (`cv2`), `sounddevice` for handling video and audio streaming

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>

2. **Set Up the Virtual Environment**:

   ```bash
   Copy code
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

Add Any Required Libraries to requirements.txt: Ensure the following libraries are included in your requirements.txt```


4. **Running the CLI Menu**
To start the main CLI menu, run:
    ```bash
    python3 matrix_menu.py  


## Menu Options
- View Peers: Display all saved peers.
- Add Peer: Add a new peer by specifying a name and IP address.
- Select Peer to Connect: Choose a peer to connect for chat or video.
- Launch Video Feed: Start streaming a Matrix-style ASCII video feed to the selected peer in a new terminal.
- Launch Chat: Start a text chat with the selected peer in a new terminal.
- Run Matrix: Launch matrix.py in a new terminal.
- Exit: Close the CLI menu.
- Testing the Video Feed

The menu also includes an option to test the video feed locally in Matrix style. Select 6. Test Video Feed in the menu to open your webcam feed in Matrix ASCII format, allowing you to preview the video feed without connecting to a peer.

Folder Structure
**matrix_menu.py:** The main CLI menu for managing peers, launching chat, and video.
**matrix.py:** A core script that runs the Matrix-style video feed and chat functionalities.
**matrix_video.py**: Script to handle video feed streaming.
**matrix_chat.py**: Script to handle text chat.

### Example Commands
To start a chat or video feed with a peer:

Run the menu:

    python3 matrix_menu.py

Use the options to:
Add and select a peer.
Launch either the chat or video feed in a new terminal.

## Troubleshooting
### Common Issues
Permissions for Terminal Windows: Ensure your terminal supports gnome-terminal or update the matrix_menu.py code to use another terminal emulator.
Audio and Video Dependencies: Install missing packages (opencv-python, sounddevice, etc.) using pip.


## License
This project is licensed under the MIT License.

Acknowledgments
Colorama and pyfiglet for enhancing the CLI interface.
OpenCV for video processing.
Sounddevice for audio streaming.
Enjoy exploring the Matrix-style command-line chat and video application!

markdown
Copy code

### Explanation of the Sections

- **Features**: Highlights what the application can do.
- **Requirements**: Lists necessary libraries and dependencies.
- **Installation**: Provides step-by-step instructions for setup.
- **Usage**: Explains how to navigate the CLI menu and test features.
- **Folder Structure**: Describes key files and directories.
- **Troubleshooting**: Addresses common issues.
- **Example Commands**: Provides a quick start guide.
- **Acknowledgments**: Credits libraries and resources used.