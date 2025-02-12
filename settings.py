#MIT License

#Copyright (c) 2025 [SAMSON AKACH ([GitHub]\([https://github.com/Sammymullern/](https://github.com/Sammymullern/))#)]
#Permission is hereby granted, free of charge, to any person obtaining a copyof this software and associated #documentation files (the "Software"), to deal in the Software without restriction, including without #limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the #Software, and to permit persons to whom the Software isfurnished to do so, subject to the following #conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions #of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, #INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR #PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE #LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT #OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR #OTHER DEALINGS IN THE SOFTWARE.


import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox
import os
from database import add_song_to_playlist, get_library_songs  # ✅ Import database functions

class Settings:
    def __init__(self, parent, update_library_callback, change_theme_callback):
        """Initialize settings window."""
        self.parent = parent
        self.update_library_callback = update_library_callback
        self.change_theme_callback = change_theme_callback
        
        # Destroy any existing settings frame
        for widget in parent.winfo_children():
            widget.destroy()
        
        self.settings_frame = tk.Frame(parent, bg="lightgray")
        self.settings_frame.pack(fill=tk.BOTH, expand=True)

        # Add Songs Button
        self.add_songs_button = tk.Button(self.settings_frame, text="Add Songs", command=self.add_songs, bg="blue", fg="white")
        self.add_songs_button.pack(pady=10)

        # Add Folder Button
        self.add_folder_button = tk.Button(self.settings_frame, text="Add Folder", command=self.add_folder, bg="purple", fg="white")
        self.add_folder_button.pack(pady=10)

        # Open Theme Settings Button
        self.theme_button = tk.Button(self.settings_frame, text="Theme Settings", command=self.open_theme_settings, bg="gray", fg="white")
        self.theme_button.pack(pady=10)

    def add_songs(self):
        """Allow user to select individual songs and save them to the library."""
        files = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if files:
            for file in files:
                add_song_to_playlist("Library", file)  # ✅ Save song in 'Library' playlist

            messagebox.showinfo("Success", "Songs added successfully!")
            self.update_library_callback(get_library_songs())  # ✅ Refresh Library UI

    def add_folder(self):
        """Allow user to select an entire folder and add all audio files to the library."""
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            # Get all audio files from the selected folder
            audio_files = [os.path.join(folder_selected, f) for f in os.listdir(folder_selected) if f.endswith((".mp3", ".wav"))]

            if not audio_files:
                messagebox.showwarning("No Audio Files", "No MP3 or WAV files found in the selected folder.")
                return

            # Add all songs to the database
            for file in audio_files:
                add_song_to_playlist("Library", file)  # ✅ Save all songs in 'Library'

            messagebox.showinfo("Success", f"Added {len(audio_files)} songs from folder!")
            self.update_library_callback(get_library_songs())  # ✅ Refresh Library UI

    def open_theme_settings(self):
        """Open a new window for theme selection."""
        theme_window = tk.Toplevel(self.parent)
        theme_window.title("Theme Settings")
        theme_window.geometry("300x150")
        theme_window.configure(bg="lightgray")

        tk.Label(theme_window, text="Select Theme:", bg="lightgray").pack(pady=10)
        theme_combobox = Combobox(theme_window, values=["light", "dark", "system"])
        theme_combobox.pack(pady=5)
        theme_combobox.set("light")

        apply_button = tk.Button(theme_window, text="Apply", command=lambda: self.apply_theme(theme_combobox.get()))
        apply_button.pack(pady=10)

    def apply_theme(self, theme_choice):
        """Change theme based on user selection."""
        self.change_theme_callback(theme_choice)
