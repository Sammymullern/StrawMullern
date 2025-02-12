import pygame
import random
import os
import threading
from database import get_library_songs, get_playlist_songs

class MusicPlayer:
    def __init__(self):
        """Initialize the Music Player"""
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Detect song end event
        self.current_song_index = 0
        self.songs = get_library_songs()  # Load songs from the library initially
        self.is_paused_flag = False
        self.shuffle_enabled = False
        self.repeat_enabled = False

        # Start a background thread to monitor song completion
        self.event_listener_thread = threading.Thread(target=self.listen_for_events, daemon=True)
        self.event_listener_thread.start()

    def load_songs(self, source="library", playlist_name=None):
        """Load songs from the library or a specific playlist."""
        if source == "library":
            self.songs = get_library_songs()
        elif source == "playlist" and playlist_name:
            self.songs = get_playlist_songs(playlist_name)

        if not self.songs:
            print("No songs available in the selected source.")

    def play_song(self, song_path):
        """Play a selected song."""
        if not os.path.isfile(song_path):
            print(f"Error: File not found - {song_path}")
            return

        if song_path not in self.songs:
            self.songs.append(song_path)
        self.current_song_index = self.songs.index(song_path)

        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        self.is_paused_flag = False
        print(f"Playing: {song_path}")

    def pause_song(self):
        """Pause the currently playing song."""
        pygame.mixer.music.pause()
        self.is_paused_flag = True
        print("Music Paused")

    def resume_song(self):
        """Resume the paused song."""
        pygame.mixer.music.unpause()
        self.is_paused_flag = False
        print("Music Resumed")

    def stop_song(self):
        """Stop playback."""
        pygame.mixer.music.stop()
        self.is_paused_flag = False
        print("Music Stopped")

    def is_playing(self):
        """Check if a song is playing."""
        return pygame.mixer.music.get_busy()

    def is_paused(self):
        """Check if the song is paused."""
        return self.is_paused_flag

    def get_current_song(self):
        """Return the currently playing song."""
        if self.songs and 0 <= self.current_song_index < len(self.songs):
            return self.songs[self.current_song_index]
        return None

    def set_volume(self, volume):
        """Adjust volume (0.0 - 1.0)."""
        pygame.mixer.music.set_volume(volume)
        print(f"Volume set to: {volume}")

    def set_shuffle(self, shuffle):
        """Enable or disable shuffle mode."""
        self.shuffle_enabled = shuffle
        print(f"Shuffle {'enabled' if shuffle else 'disabled'}")

    def set_repeat(self, repeat):
        """Enable or disable repeat mode."""
        self.repeat_enabled = repeat
        print(f"Repeat {'enabled' if repeat else 'disabled'}")

    def next_song(self):
        """Play the next song in the list."""
        if not self.songs:
            self.load_songs()

        if self.shuffle_enabled:
            self.current_song_index = random.randint(0, len(self.songs) - 1)
        else:
            self.current_song_index = (self.current_song_index + 1) % len(self.songs)

        self.play_song(self.get_current_song())

    def previous_song(self):
        """Play the previous song in the list."""
        if not self.songs:
            self.load_songs()

        self.current_song_index = (self.current_song_index - 1) % len(self.songs)
        self.play_song(self.get_current_song())

    def handle_song_end(self):
        """Handles automatic playback when a song finishes."""
        if self.repeat_enabled:
            self.play_song(self.get_current_song())  # Repeat same song
        else:
            self.next_song()  # Play the next song

    def listen_for_events(self):
        """Listen for Pygame events in a separate thread."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    self.handle_song_end()  # Call next song when current song ends
