import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from settings import Settings
from library import Library
from playlists import Playlist
from music_player import MusicPlayer
import pygame
import os

# Initialize music player
music_player = MusicPlayer()
shuffle_enabled = False
repeat_enabled = False

def toggle_play_pause():
    if music_player.is_playing():
        music_player.pause_song()
        play_pause_button.config(text="▶ Play")
    else:
        if not music_player.is_paused():  # Check if a new song should start
            music_player.play_song(music_player.get_current_song())
        else:
            music_player.resume_song()
        play_pause_button.config(text="⏸ Pause")
    
    update_now_playing()

def toggle_shuffle():
    global shuffle_enabled
    shuffle_enabled = not shuffle_enabled
    shuffle_button.config(text="🔀 Shuffle ON" if shuffle_enabled else "🔀 Shuffle OFF")
    music_player.set_shuffle(shuffle_enabled)

def toggle_repeat():
    global repeat_enabled
    repeat_enabled = not repeat_enabled
    repeat_button.config(text="🔁 Repeat ON" if repeat_enabled else "🔁 Repeat OFF")
    music_player.set_repeat(repeat_enabled)

def update_now_playing():
    current_song = music_player.get_current_song()
    if current_song:
        song_title = os.path.basename(current_song)
    else:
        song_title = "No Song Playing"
    
    print(f"DEBUG: Now Playing - {song_title}")  # Debug print statement
    now_playing_label.config(text=f"🎧 Now Playing: {song_title}")
    update_progress_bar()

def update_progress_bar():
    if music_player.is_playing():
        position = pygame.mixer.music.get_pos() // 1000  # Convert to seconds
        progress_var.set(position)
        root.after(1000, update_progress_bar)

def seek_song(value):
    pygame.mixer.music.set_pos(float(value))

def next_song():
    music_player.next_song()
    update_now_playing()  # Ensure Now Playing updates

def previous_song():
    music_player.previous_song()
    update_now_playing()  # Ensure Now Playing updates

def play_selected_song(song_path):
    """Play a song selected from the library."""
    music_player.play_song(song_path)
    update_now_playing()  # Ensure Now Playing updates

# Initialize the main window
root = tk.Tk()
root.title("Music Player")
root.geometry("1900x1000")
style = Style("darkly")  # Modern dark theme
root.config(bg="#222222")

# Sidebar
sidebar = ttk.Frame(root, width=200, style="primary.TFrame")
sidebar.pack(side=tk.LEFT, fill=tk.Y)

# Logo placeholder
logo_label = tk.Label(sidebar, text="♪ STRAW", font=("Helvetica", 16, "bold"), bg="#222222", fg="lime")
logo_label.pack(pady=(10, 20))

# Sidebar Buttons
menu_buttons = [
    ("📚 Library", lambda: Library(main_content, play_callback=play_selected_song)),
    ("🎧 Playlist", lambda: Playlist(main_content)),
    ("🔧 Settings", lambda: Settings(main_content, lambda x: None, lambda x: None))
]
for text, command in menu_buttons:
    ttk.Button(sidebar, text=text, style="secondary.TButton", command=command, padding=10).pack(fill=tk.X, padx=10, pady=5)

# Main Content Area
main_content = ttk.Frame(root, style="primary.TFrame")
main_content.pack(side=tk.LEFT, fill=tk.BOTH)

# Now Playing Section
now_playing_label = ttk.Label(root, text="(﹙˓ 🎧 ˒﹚)Playing: No Song Playing", font=("Arial", 12, "bold"), style="info.TLabel")
now_playing_label.pack(side=tk.TOP, pady=5)

# Progress Bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Scale(root, from_=0, to=100, orient="horizontal", variable=progress_var, command=seek_song)
progress_bar.pack(fill=tk.X, padx=20, pady=5)

# Playback Controls
controls_frame = ttk.Frame(root, style="secondary.TFrame")
controls_frame.pack(side=tk.BOTTOM, fill=tk.X)

controls_frame.columnconfigure(list(range(6)), weight=1)

prev_button = ttk.Button(controls_frame, text="⏮", style="info.TButton", command=previous_song, width=12)
prev_button.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

play_pause_button = ttk.Button(controls_frame, text="▶ Play", style="success.TButton", command=toggle_play_pause, width=12)
play_pause_button.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

next_button = ttk.Button(controls_frame, text="⏭", style="info.TButton", command=next_song, width=12)
next_button.grid(row=0, column=2, padx=5, pady=10, sticky="ew")

shuffle_button = ttk.Button(controls_frame, text="🔀 Shuffle OFF", style="warning.TButton", command=toggle_shuffle, width=12)
shuffle_button.grid(row=0, column=3, padx=5, pady=10, sticky="ew")

repeat_button = ttk.Button(controls_frame, text="🔁 Repeat OFF", style="danger.TButton", command=toggle_repeat, width=12)
repeat_button.grid(row=0, column=4, padx=5, pady=10, sticky="ew")

# Volume Control
volume_frame = ttk.Frame(controls_frame)
volume_frame.grid(row=0, column=5, padx=10, pady=10, sticky="ew")
volume_label = ttk.Label(volume_frame, text="🔊", style="secondary.TLabel")
volume_label.pack(side=tk.LEFT, padx=5)

volume_slider = ttk.Scale(volume_frame, from_=0, to=100, orient="horizontal", command=lambda v: music_player.set_volume(float(v)/100))
volume_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)

# Start with the Library Section Open
Library(main_content, play_callback=play_selected_song)

# Run the app
root.mainloop()
