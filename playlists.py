#MIT License

#Copyright (c) 2025 [SAMSON AKACH ([GitHub]\([https://github.com/Sammymullern/](https://github.com/Sammymullern/))#)]
#Permission is hereby granted, free of charge, to any person obtaining a copyof this software and associated #documentation files (the "Software"), to deal in the Software without restriction, including without #limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the #Software, and to permit persons to whom the Software isfurnished to do so, subject to the following #conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions #of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, #INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR #PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE #LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT #OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR #OTHER DEALINGS IN THE SOFTWARE.


import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import os
from database import add_playlist, get_playlists, add_song_to_playlist, get_playlist_songs, delete_playlist, get_library_songs
from music_player import MusicPlayer

class Playlist:
    def __init__(self, parent):
        """Initialize the Playlist UI."""
        self.parent = parent
        self.music_player = MusicPlayer()

        # Clear UI before loading Playlist section
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Title
        ttk.Label(self.parent, text="🎶 Playlists", font=("Arial", 14, "bold")).pack(pady=10)

        # Playlists container
        self.playlists_frame = ttk.Frame(self.parent)
        self.playlists_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Buttons (Enhanced)
        button_frame = ttk.Frame(self.parent)
        button_frame.pack(pady=5)

        self.create_button(button_frame, "➕ New Playlist", self.create_playlist)
        self.create_button(button_frame, "🗑 Delete Playlist", self.remove_playlist)

        # Songs area
        self.songs_frame = ttk.Frame(self.parent)
        self.songs_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.update_playlist_listbox()

    def create_button(self, parent, text, command):
        """Create a button with a unique 3D effect."""
        btn = tk.Button(parent, text=text, command=command, font=("Arial", 10, "bold"),
                        relief="raised", bd=3, padx=10, pady=5, bg="#f0f0f0", fg="black", cursor="hand2")
        btn.pack(side=tk.LEFT, padx=5)

    def update_playlist_listbox(self):
        """Refresh the playlists UI."""
        for widget in self.playlists_frame.winfo_children():
            widget.destroy()

        playlists = get_playlists()
        if not playlists:
            ttk.Label(self.playlists_frame, text="No Playlists Available", font=("Arial", 10)).pack(pady=5)

        for playlist_name in playlists:
            playlist_container = ttk.Frame(self.playlists_frame, padding=5, relief="raised")
            playlist_container.pack(fill=tk.X, pady=5)

            playlist_label = ttk.Label(playlist_container, text=f"📌 {playlist_name}", font=("Arial", 11, "bold"))
            playlist_label.pack(side=tk.LEFT, padx=10, pady=5)

            playlist_label.bind("<Button-1>", lambda e, name=playlist_name: self.show_playlist_songs(name))

    def create_playlist(self):
        """Prompt user to create a new playlist."""
        new_playlist_name = simpledialog.askstring("New Playlist", "Enter Playlist Name:")
        if new_playlist_name:
            add_playlist(new_playlist_name)
            self.update_playlist_listbox()

    def remove_playlist(self):
        """Delete the selected playlist."""
        playlists = get_playlists()
        if not playlists:
            messagebox.showwarning("No Playlists", "There are no playlists to delete.")
            return

        selected_playlist = simpledialog.askstring("Delete Playlist", "Enter Playlist Name to Delete:")

        if selected_playlist and selected_playlist in playlists:
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{selected_playlist}'?")
            if confirm:
                delete_playlist(selected_playlist)
                self.update_playlist_listbox()
                for widget in self.songs_frame.winfo_children():
                    widget.destroy()
        else:
            messagebox.showwarning("Invalid Selection", "The playlist does not exist.")

    def show_playlist_songs(self, playlist_name):
        """Display songs in a playlist and allow playing them."""
        songs = get_playlist_songs(playlist_name)

        # Clear previous content
        for widget in self.songs_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.songs_frame, text=f"🎵 {playlist_name} Songs", font=("Arial", 12, "bold")).pack(pady=5)

        if not songs:
            ttk.Label(self.songs_frame, text="No songs in this playlist", font=("Arial", 10)).pack(pady=5)

        for song_path in songs:
            song_name = os.path.basename(song_path)

            song_frame = ttk.Frame(self.songs_frame, padding=5, relief="solid")
            song_frame.pack(anchor="w", padx=10, pady=2, fill=tk.X)

            song_label = ttk.Label(song_frame, text=f"♬ {song_name}", font=("Arial", 10))
            song_label.pack(side=tk.LEFT, padx=5)

            play_button = ttk.Button(song_frame, text="▶ Play", command=lambda s=song_path: self.music_player.play_song(s))
            play_button.pack(side=tk.RIGHT, padx=5)

        ttk.Button(self.songs_frame, text="➕ Add Song", command=lambda: self.add_song(playlist_name)).pack(pady=10)

    def add_song(self, playlist_name):
        """Allow users to select a song from the Library and add it to the playlist."""
        library_songs = get_library_songs()

        if not library_songs:
            messagebox.showwarning("No Songs", "No songs available in the Library.")
            return

        song_selection_window = tk.Toplevel(self.parent)
        song_selection_window.title("Select a Song from Library")
        song_selection_window.geometry("800x500")

        ttk.Label(song_selection_window, text="Select a song to add:", font=("Arial", 12, "bold")).pack(pady=5)

        song_listbox = tk.Listbox(song_selection_window, height=10, width=50)
        song_listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        for song in library_songs:
            song_listbox.insert(tk.END, os.path.basename(song))

        def confirm_selection():
            """Add the selected song to the playlist."""
            selected_index = song_listbox.curselection()
            if not selected_index:
                return

            selected_song = library_songs[selected_index[0]]
            add_song_to_playlist(playlist_name, selected_song)

            song_selection_window.destroy()
            self.show_playlist_songs(playlist_name)

        ttk.Button(song_selection_window, text="Add Song", command=confirm_selection).pack(pady=5)
