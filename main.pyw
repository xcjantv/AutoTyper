import queue
import sys
import time

import pyperclip
import keyboard
from threading import Thread
import pystray
from PIL import Image
from tkinter import Tk, Label, Button, StringVar
from queue import Queue

# Tray icon
icon = Image.open("icon.png")
message_queue = Queue()
# Set default key to listen for
chosen_key = 'f9'
# Flag to indicate whether keyboard listener is active
listener_active = False

# Function to handle key press
def on_key_press(key):
    if key.name == chosen_key:
        text = pyperclip.paste()
        keyboard.write(text)

# Function to run in thread for keyboard listening
def keyboard_listener():
    global listener_active
    while True:
        try:
            message = message_queue.get(block=False)
        except queue.Empty:
            message = None

        if message == "quit":
            break
        else:
            if not listener_active:
                listener_active = True
                time.sleep(0.2)
                on_key_press(keyboard.read_event())
                listener_active = False

# Function to open key selection popup
def popup():
    # Create popup window
    popup_window = Tk()
    popup_window.title("Change key")
    popup_window.geometry("200x400")

    # Add label and buttons for key selection
    Label(popup_window, text="Select a key:").pack()

    def select_key(key):
        global chosen_key
        chosen_key = key
        message_queue.put("restart_listener")
        popup_window.destroy()

    for key in keys:
        Button(popup_window, text=key, command=lambda key=key: select_key(key)).pack()

    popup_window.mainloop()

# Function to run when quitting from system tray
def on_quit():
    message_queue.put("quit")
    tray_icon.stop()

# Function to run when changing the key to listen for
def on_key_change():
    popup()

# Create system tray icon
keys = ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12']
menu = pystray.Menu(
    pystray.MenuItem('Change key', on_key_change),
    pystray.MenuItem('Quit', on_quit)
)

# Start keyboard listening in a separate thread
listener_thread = Thread(target=keyboard_listener, daemon=True)
listener_thread.start()

# Create system tray icon
tray_icon = pystray.Icon('AutoTyper', icon, menu=menu)

# Run system tray icon in main thread
tray_icon.run()
