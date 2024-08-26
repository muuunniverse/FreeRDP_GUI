#! python3

import pystray
from PIL import Image
import os
import FreeRDP_Main

absolute_path = os.path.dirname(__file__)
image = Image.open(f"{absolute_path}/FreeRDP-icon.ico")

def tray_select(icon, query):
    if str(query) == "New Connection":
        FreeRDP_Main.main() #revert to backup for working file
    elif str(query) == "Exit":
        exit()

icon = pystray.Icon("FreeRDPGUI", image, "FreeRDPGUI", 
                    menu=pystray.Menu(
    pystray.MenuItem("New Connection", 
                     tray_select),
    pystray.MenuItem("Exit", tray_select)))

icon.run() # run tray icon