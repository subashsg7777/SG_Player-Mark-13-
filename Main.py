import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import os
from PIL import Image, ImageTk

# Initialize pygame mixer
pygame.mixer.init()

root = tk.Tk()
root.title('SG_Player (Mark 13)')
root.geometry('400x300')

# Global variables
folder_path = ""
song_index = 0  # Track the current song's index
decision = False
status = False

# Functions to play and manage music
def askFolder():
    global folder_path, song_index
    folder_path = filedialog.askdirectory()
    if folder_path:
        load_songs(folder_path)
        song_index = 0  # Reset index whenever a new folder is selected
    
def load_songs(path):
    song_listbox.delete(0, tk.END)  # Clear the listbox before loading new songs
    global songList 
    songList = [f for f in os.listdir(path) if f.endswith('.mp3') or f.endswith('.wav')]
    for song in songList:
        song_listbox.insert(tk.END, song)

def play():
    global song_index,status
    if status == False:
        if song_listbox.size() > 0:  # Ensure there are songs in the list
            selected_song = song_listbox.get(tk.ACTIVE)
            if selected_song:
                full_path = os.path.join(folder_path, selected_song)
                pygame.mixer.music.load(full_path)
                pygame.mixer.music.play()

    else:
        resume()

def play_next_song():
    global song_index,status
    song_index += 1
    if song_index >= song_listbox.size():  # Loop back to the first song
        song_index = 0
    song_listbox.selection_clear(0, tk.END)
    song_listbox.selection_set(song_index)
    song_listbox.activate(song_index)
    status = False
    play()  # Play the next song

# Plays the previous song 
def previous_song():
    global song_index,status
    song_index -= 1
    if song_index < 0:  # Prevent index from going negative
        song_index = song_listbox.size() - 1
    song_listbox.selection_clear(0, tk.END)
    song_listbox.selection_set(song_index)
    song_listbox.activate(song_index)
    status = False
    play()

def pause():
    global decision,status
    decision = True
    status = True
    pygame.mixer.music.pause()

def resume():
    global decision,status
    if status == True:
        decision = False
        pygame.mixer.music.unpause()
    else:
        play()

def stop():
    global folder_path
    folder_path = ''
    pygame.mixer.music.stop()
    song_listbox.selection_clear(0, tk.END)
    refresh_listbox()

# Function to resize the button into correct size
def load_image(imagepath, width, height):
    img = Image.open(imagepath)
    img = img.resize((width, height), Image.LANCZOS)
    return ImageTk.PhotoImage(img)

def refresh_listbox():
    song_listbox.delete(0, tk.END)  # Clear the existing list
    song_listbox.update()  # Refresh the listbox display

# GUI Elements
# Loading elements 
openImage = load_image('open.png', 50, 50)
playImage = load_image('play.png', 25, 25)
pauseImage = load_image('pause.png', 25, 25)
skipImage = load_image('skip.png', 25, 25)
stopImage = load_image('stop.png', 25, 25)
prevImage = load_image('prev.png', 25, 25)

icons = {
    "open": openImage,
    "play": playImage,
    "pause": pauseImage,
    "stop": stopImage,
    "prev": prevImage,
    "next": skipImage
}

open_button = tk.Button(root, command=askFolder, image=icons['open'], width=50, height=50)
open_button.pack()

# Initialize song_listbox outside of functions so it can be used globally
song_listbox = tk.Listbox(root)
song_listbox.pack()

# Create a frame to hold the play buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)  # Add some padding around the frame

# Add buttons to the button frame
play_button = tk.Button(button_frame, text="Play", command=play, image=icons['play'], borderwidth=0, highlightthickness=0)
pause_button = tk.Button(button_frame, text="Pause", command=pause, image=icons['pause'], borderwidth=0, highlightthickness=0)
skip_button = tk.Button(button_frame, text='Next', command=play_next_song, image=icons['next'], borderwidth=0, highlightthickness=0)
prev_button = tk.Button(button_frame, text='Prev', command=previous_song, image=icons['prev'], borderwidth=0, highlightthickness=0)
stop_button = tk.Button(button_frame, text='Stop', command=stop, image=icons['stop'], borderwidth=0, highlightthickness=0)
# resume_button = tk.Button(button_frame,text='resume',command=resume,image=icons['resume'],borderwidth=0,highlightthickness=0)

# Pack buttons into the button frame
play_button.pack(side=tk.LEFT, padx=5)
pause_button.pack(side=tk.LEFT, padx=5)
prev_button.pack(side=tk.LEFT, padx=5)
skip_button.pack(side=tk.LEFT, padx=5)
stop_button.pack(side=tk.LEFT, padx=5)

# Check if the current song has ended
def check_for_song_end():
    if not pygame.mixer.music.get_busy() and song_listbox.size() > 0:  # Song has ended
        if not decision:
            play_next_song()
    root.after(1000, check_for_song_end)  # Check every second

# Start the end event check loop
check_for_song_end()

root.mainloop()
