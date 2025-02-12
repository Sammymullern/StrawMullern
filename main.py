#MIT License

#Copyright (c) 2025 [SAMSON AKACH ([GitHub]\([https://github.com/Sammymullern/](https://github.com/Sammymullern/))#)]
#Permission is hereby granted, free of charge, to any person obtaining a copyof this software and associated #documentation files (the "Software"), to deal in the Software without restriction, including without #limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the #Software, and to permit persons to whom the Software isfurnished to do so, subject to the following #conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions #of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, #INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR #PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE #LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT #OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR #OTHER DEALINGS IN THE SOFTWARE.

from database import init_db
from gui import root  # Importing the Tkinter root from gui.py
import pygame  # Ensure pygame is imported

def main():
    init_db()  # Initialize database tables
    root.mainloop()  # Start the GUI

def check_song_end():  # Remove the extra space before 'def'
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            music_player.handle_song_end()
    root.after(100, check_song_end)  # Continuously check every 100ms

# Start event loop
root.after(100, check_song_end)

if __name__ == "__main__":
    main()
