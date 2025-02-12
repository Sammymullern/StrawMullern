
#MIT License

#Copyright (c) 2025 [SAMSON AKACH ([GitHub]\([https://github.com/Sammymullern/](https://github.com/Sammymullern/))#)]
#Permission is hereby granted, free of charge, to any person obtaining a copyof this software and associated #documentation files (the "Software"), to deal in the Software without restriction, including without #limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the #Software, and to permit persons to whom the Software isfurnished to do so, subject to the following #conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions #of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, #INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR #PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE #LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT #OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR #OTHER DEALINGS IN THE SOFTWARE.




import sqlite3
import os 

# Define database file
DB_FILE = "music_app.db"

def init_db():
    """Initialize the database and create tables if they don’t exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create playlists table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS playlists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    """)

    # Create playlist_songs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS playlist_songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            playlist_name TEXT,
            song_title TEXT,
            filepath TEXT NOT NULL,
            duration TEXT
        )
    """)

    conn.commit()
    conn.close()

def add_playlist(name):
    """Add a new playlist to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO playlists (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def delete_playlist(name):
    """Delete a playlist and its associated songs."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Remove songs first
    cursor.execute("DELETE FROM playlist_songs WHERE playlist_name = ?", (name,))
    
    # Remove the playlist
    cursor.execute("DELETE FROM playlists WHERE name = ?", (name,))
    
    conn.commit()
    conn.close()

def get_playlists():
    """Retrieve all playlists."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM playlists")
    playlists = [row[0] for row in cursor.fetchall()]
    conn.close()
    return playlists  # Returns ["Pop", "Hip-Hop"]

def add_song_to_playlist(playlist_name, song_path):
    """Add a song to the specified playlist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    song_title = os.path.basename(song_path)
    duration = "Unknown"

    cursor.execute("""
        INSERT INTO playlist_songs (playlist_name, song_title, filepath, duration)
        VALUES (?, ?, ?, ?)
    """, (playlist_name, song_title, song_path, duration))

    conn.commit()
    conn.close()

def get_playlist_songs(playlist_name):
    """Retrieve all songs from a specific playlist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT filepath FROM playlist_songs WHERE playlist_name = ?", (playlist_name,))
    songs = [row[0] for row in cursor.fetchall()]
    conn.close()
    return songs

def get_library_songs():
    """Retrieve all songs from the library."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT filepath FROM playlist_songs")
    songs = [row[0] for row in cursor.fetchall()]
    conn.close()
    return songs

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
