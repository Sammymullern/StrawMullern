# Music Player

A  Python-based music player using **pygame, tinker etc** to play audio files. This music player allows you to load, play, pause, resume, stop, and navigate through songs. It also supports **shuffle** and **repeat** modes.

## Features

- **Play, Pause, Resume, and Stop songs**
- **Automatic next song playback** when the current song finishes
- **Shuffle Mode**: Plays songs in a random order
- **Repeat Mode**: Repeats the currently playing song
- **Next and Previous song navigation**
- **Volume control**
- **Supports library and playlists**

## Installation

### Prerequisites

Ensure you have **Python 3.6+** installed. You also need to install `pygame` if you haven’t already.

```sh
pip install pygame
```

## Usage

### Running the Music Player

```sh
python main.py
```

### Controlling the Player

- **Play a song:** Automatically starts playing from the loaded list or call `play_song(song_path)`
- **Pause:** `pause_song()`
- **Resume:** `resume_song()`
- **Stop:** `stop_song()`
- **Next song:** `next_song()`
- **Previous song:** `previous_song()`
- **Enable Shuffle:** `set_shuffle(True)`
- **Enable Repeat:** `set_repeat(True)`

### Example Usage in Code

```python
player = MusicPlayer()
player.load_songs()
player.play_song("/path/to/song.mp3")
```

## How Auto-Next Works

- The app listens for a `pygame.USEREVENT` when a song finishes.
- `handle_song_end()` is automatically triggered to either:
  - Repeat the song if `repeat_enabled` is `True`.
  - Play the next song (or shuffle if enabled).

## Supported Formats

- MP3
- WAV
- OGG (depending on `pygame` support)

## Future Improvements

- GUI interface for better user interaction
- Playlist management system
- Equalizer settings

# Music Player

A simple music player built with Python and Tkinter, using **pygame** for audio playback. The app allows users to play, pause, stop, shuffle, repeat, and navigate through songs.

## Features
- Play, pause, and stop songs
- Next and previous song navigation
- Shuffle and repeat modes
- Tracks, Artists, and Albums library views
- Scrollable UI for easy song browsing

## Installation
1. **Clone the repository**:
   ```sh
   git clone https://github.com/your-repo/music-player.git
   cd music-player
   ```
2. **Install dependencies**:
   ```sh
   pip install pygame tk
   ```
3. **Run the app**:
   ```sh
   python main.py
   ```

## Usage
- Open the app and navigate through the **Library**.
- Click on a track to start playing.
- Use the controls to **pause**, **resume**, **skip**, or **enable shuffle/repeat**.



## License

This project is open-source and free to use under the MIT License.

---

Developed by 
SAMSON AKACH FOR LINUX USERS
## Contact
For support or feature requests, feel free to [send an email](mailto:mullerncybert@gmail.com?subject=Music%20Player%20Support&body=Hello,%20I%20have%20a%20question%20about%20the%20music%20player...).





