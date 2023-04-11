import queue
import sys

import pyperclip
import keyboard
from threading import Thread
import pystray
from PIL import Image
from queue import Queue

# Tray icon
icon = Image.open("icon.png")
message_queue = Queue()

# Function to handle key press
def on_key_press(key):
    if key.name == 'f9':
        text = pyperclip.paste()
        keyboard.write(text)

# Function to run in thread for keyboard listening
def keyboard_listener():

    while True:
        try:
            message = message_queue.get(block=False)
        except queue.Empty:
            message = None

        if message == "quit":
            break
        else:
            keyboard.wait('f9')
            on_key_press(keyboard.read_event())


# Function to run when quitting from system tray
def on_quit():
    message_queue.put("quit")
    tray_icon.stop()



# Create system tray icon
menu = pystray.Menu(pystray.MenuItem('Quit', on_quit))
tray_icon = pystray.Icon('AutoTyper', icon, menu=menu)

# Start keyboard listening in a separate thread
listener_thread = Thread(target=keyboard_listener, daemon=True)
listener_thread.start()


# Run system tray icon in main thread
tray_icon.run()
