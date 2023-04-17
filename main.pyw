import queue
import sys
import time

import pyperclip
import keyboard
from threading import Thread
import pystray
from PIL import Image
from tkinter import Tk, Label, Button, StringVar, Entry, Checkbutton
from queue import Queue
import json
import os

# Tray icon
icon = Image.open("icon.png")
message_queue = Queue()

# Set default key to listen for
if os.path.isfile('hotkey_settings.json'):
    with open('hotkey_settings.json', 'r') as f:
        hotkey_data = json.load(f)
        chosen_key = hotkey_data['hotkey']
else:
    chosen_key = 'F9'

# Flag to indicate whether keyboard listener is active
listener_active = False

# Function to handle key press
def on_key_press(key):
    if key.name == chosen_key.lower():
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
    popup_window.geometry("200x250")

    # Add label and entry field for key selection
    Label(popup_window, text="Enter a key:").pack()
    entry = Entry(popup_window)
    entry.insert(0, chosen_key.upper())
    entry.pack()

    # Add checkbox to save hotkey to JSON file
    save_key_var = StringVar()
    save_key_var.set("false")
    save_key_checkbox = Checkbutton(popup_window, text="Save hotkey as default", variable=save_key_var)
    save_key_checkbox.pack()

    def select_key():
        global chosen_key
        chosen_key = entry.get()
        message_queue.put("restart_listener")

        # Check if the "save to JSON" checkbox is selected
        save_to_json = save_key_var.get()
        if save_to_json:
            # Define the filename of the JSON file
            json_filename = "hotkey_settings.json"

            # Check if the JSON file exists
            if os.path.isfile(json_filename):
                # Open the existing file for writing (overwrite)
                with open(json_filename, "w") as f:
                    # Write the hotkey setting to the file
                    json.dump({"hotkey": chosen_key}, f)
            else:
                # Create a new file for writing
                with open(json_filename, "w") as f:
                    # Write the hotkey setting to the file
                    json.dump({"hotkey": chosen_key}, f)

        popup_window.destroy()

    Button(popup_window, text="Select Key", command=select_key).pack()

    popup_window.mainloop()

# Function to run when quitting from system tray
def on_quit():
    message_queue.put("quit")
    tray_icon.stop()

# Function to run when changing the key to listen for
def on_key_change():
    popup()

# Create system tray icon
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
