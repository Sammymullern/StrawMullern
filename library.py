#MIT License

#Copyright (c) 2025 [SAMSON AKACH ([GitHub]\([https://github.com/Sammymullern/](https://github.com/Sammymullern/))#)]
#Permission is hereby granted, free of charge, to any person obtaining a copyof this software and associated #documentation files (the "Software"), to deal in the Software without restriction, including without #limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the #Software, and to permit persons to whom the Software isfurnished to do so, subject to the following #conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions #of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, #INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR #PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE #LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT #OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR #OTHER DEALINGS IN THE SOFTWARE.
import tkinter as tk
from tkinter import ttk, messagebox
import os
from music_player import MusicPlayer
from database import get_library_songs

class Library:
    def __init__(self, parent, play_callback):
        """Initialize the Library section with Tracks, Artists, and Albums tabs."""
        self.parent = parent
        self.play_callback = play_callback  # Callback function for playing songs
        self.music_player = MusicPlayer()
        self.song_list = list(set(get_library_songs()))  # Remove duplicate songs
        self.currently_playing_song = None  # Track the currently playing song
        self.song_labels = {}  # Store all song labels for easy updating
        self.animation_running = False

        # Clear the main content area before adding the library UI
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Create Notebook (Tabbed UI)
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create Frames for Tracks, Artists, and Albums
        self.tracks_frame = ttk.Frame(self.notebook, width=800, height=500)
        self.artists_frame = ttk.Frame(self.notebook, width=800, height=500)
        self.albums_frame = ttk.Frame(self.notebook, width=800, height=500)

        self.tracks_frame.pack_propagate(False)
        self.artists_frame.pack_propagate(False)
        self.albums_frame.pack_propagate(False)

        self.notebook.add(self.tracks_frame, text="Tracks")
        self.notebook.add(self.artists_frame, text="Artists")
        self.notebook.add(self.albums_frame, text="Albums")

        # Populate the tabs
        self.create_scrollable_tracks()
        self.create_scrollable_artists()
        self.create_scrollable_albums()

    def create_scrollable_frame(self, parent):
        """Create a scrollable frame with a canvas and scrollbar."""
        container = ttk.Frame(parent)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Enable mouse scrolling
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        return scrollable_frame, canvas, scrollbar

    def create_scrollable_tracks(self):
        """Create a scrollable frame for tracks and populate it."""
        self.tracks_container, _, _ = self.create_scrollable_frame(self.tracks_frame)
        self.populate_tracks()

    def create_scrollable_artists(self):
        """Create a scrollable frame for artists and populate it."""
        self.artists_container, _, _ = self.create_scrollable_frame(self.artists_frame)
        self.populate_artists()

    def create_scrollable_albums(self):
        """Create a scrollable frame for albums and populate it."""
        self.albums_container, _, _ = self.create_scrollable_frame(self.albums_frame)
        self.populate_albums()

    def populate_tracks(self):
        """Display a list of all added songs in the Tracks tab."""
        for widget in self.tracks_container.winfo_children():
            widget.destroy()

        if not self.song_list:
            ttk.Label(self.tracks_container, text="No songs found in the library.", font=("Arial", 12)).pack(pady=20)
            return

        ttk.Label(self.tracks_container, text="All Tracks", font=("Arial", 12, "bold")).pack(pady=5)
        self.song_labels.clear()

        for song in self.song_list:
            song_name = os.path.basename(song)

            # Customize Track Frame
            song_frame = ttk.Frame(self.tracks_container, padding=8, relief="ridge", borderwidth=3)
            song_frame.pack(fill=tk.X, padx=10, pady=4)

            emoji_label = ttk.Label(song_frame, text="🎵", font=("Arial", 12))
            emoji_label.pack(side=tk.LEFT, padx=5)

            song_label = ttk.Label(song_frame, text=song_name, font=("Arial", 11), anchor="w")
            song_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

            play_button = ttk.Button(song_frame, text="▶ Play", command=lambda s=song: self.play_selected_song(s))
            play_button.pack(side=tk.RIGHT, padx=5)

            self.song_labels[song] = song_label
            song_label.bind("<Button-1>", lambda e, s=song: self.play_selected_song(s))

    def populate_artists(self):
        """Display a list of artists in the Artists tab."""
        for widget in self.artists_container.winfo_children():
            widget.destroy()

        if not self.song_list:
            ttk.Label(self.artists_container, text="No artists found.", font=("Arial", 12)).pack(pady=20)
            return

        ttk.Label(self.artists_container, text="Artists", font=("Arial", 12, "bold")).pack(pady=5)

        # Group songs by artist
        artists = {}
        for song in self.song_list:
            artist = self.get_artist_from_song(song)  # Implement this function
            if artist not in artists:
                artists[artist] = []
            artists[artist].append(song)

        for artist, songs in artists.items():
            artist_frame = ttk.Frame(self.artists_container, padding=8, relief="ridge", borderwidth=3)
            artist_frame.pack(fill=tk.X, padx=10, pady=4)

            ttk.Label(artist_frame, text=artist, font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
            ttk.Label(artist_frame, text=f"{len(songs)} songs", font=("Arial", 10)).pack(side=tk.RIGHT, padx=5)

    def populate_albums(self):
        """Display a list of albums in the Albums tab."""
        for widget in self.albums_container.winfo_children():
            widget.destroy()

        if not self.song_list:
            ttk.Label(self.albums_container, text="No albums found.", font=("Arial", 12)).pack(pady=20)
            return

        ttk.Label(self.albums_container, text="Albums", font=("Arial", 12, "bold")).pack(pady=5)

        # Group songs by album
        albums = {}
        for song in self.song_list:
            album = self.get_album_from_song(song)  # Implement this function
            if album not in albums:
                albums[album] = []
            albums[album].append(song)

        for album, songs in albums.items():
            album_frame = ttk.Frame(self.albums_container, padding=8, relief="ridge", borderwidth=3)
            album_frame.pack(fill=tk.X, padx=10, pady=4)

            ttk.Label(album_frame, text=album, font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
            ttk.Label(album_frame, text=f"{len(songs)} songs", font=("Arial", 10)).pack(side=tk.RIGHT, padx=5)

    def get_artist_from_song(self, song):
        """Extract artist name from song metadata or file path."""
        # Example: Extract artist from file name (you can replace this with metadata extraction)
        return os.path.basename(song).split(" - ")[0]

    def get_album_from_song(self, song):
        """Extract album name from song metadata or file path."""
        # Example: Extract album from file name (you can replace this with metadata extraction)
        return os.path.basename(os.path.dirname(song))

    def play_selected_song(self, song):
        """Play the selected song and update the Now Playing section."""
        if not os.path.exists(song):
            messagebox.showerror("Error", f"Song file not found: {song}")
            return

        try:
            self.play_callback(song)  # Call the function from gui.py to update Now Playing
        except Exception as e:
            messagebox.showerror("Playback Error", f"Could not play the song: {e}")