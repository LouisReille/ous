# Pyxel Raycaster Project

A 3D raycasting game built with Pyxel, inspired by classic games like Wolfenstein 3D.

## Requirements

- Python 3.9 or higher
- VLC Media Player (for audio playback)
  - On macOS: Download from [videolan.org](https://www.videolan.org/vlc/) or install via Homebrew: `brew install vlc`

## Installation

1. Install Python dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```
   
   Or manually:
   ```bash
   pip3 install pyxel python-vlc
   ```

## Running the Project

Simply run:
```bash
python3 main2.py
```

## Controls

- **Arrow Keys (UP/DOWN)**: Move forward/backward
- **Mouse**: Look around (camera rotation)

## Features

- 3D raycasting engine
- Enemy AI ("nextbot") that follows the player
- Background music
- Multiple wall textures/types

## Files

- `main2.py` - Main game file
- `song2.mp3` - Background music
- `nextbot.png` - Enemy sprite (if used)
