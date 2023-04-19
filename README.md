
# AutoTyper

AutoTyper is a small application that allows you to easily and quickly insert text into any application by simply copying it to the clipboard and pressing a keyboard shortcut. The program runs in the background and waits for you to press the F9 Key, at which point it will automatically insert the text from your clipboard.



## Installation

No installation is required for this program. 
Simply download the AutoTyper.zip file and run main.exe.
    
## Usage/Examples

To use AutoTyper, first copy the text you want to insert to your clipboard. Then press the F9 key (if not configuered otherwise in system tray menu), and the text will be automatically typed into your active application.
The default key can be configured in system tray menue by changing the HotKey an selecting the "save as default key" checkbox. (It will create a .json with configuration)
![image](https://user-images.githubusercontent.com/59826149/232993107-c78d54cb-e6eb-4e9b-8192-faa31a0f40ec.png)

The program can be exited by right-clicking the tray icon and selecting the "Quit" option from the menu.
![image](https://user-images.githubusercontent.com/59826149/232993265-c8f53c7b-a849-4205-aa7d-922fc471a49d.png)


## Note

This program runs in the background and may interfere with other applications that use the same keyboard shortcut. Please use caution when using this program, and make sure you are not accidentally inserting text into the wrong application.

## Optimizations
All files for making changes are in build.zip.

Recreating .exe file with changes: 

Step 1: run build.bat in build folder 

-> new .exe in dist folder

