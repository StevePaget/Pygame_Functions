#Displays key codes on screen to aid key identification. Esc to quit

from pygame_functions import *
    
screenSize(300,100)

infoLabel = makeLabel("Key Code:", 20, 50,10,"white")
showLabel(infoLabel)  

while True:
    key = waitPress()
    changeLabel(infoLabel,"Key Code: " + str(key))
    if key==27:
        break
pause(1000, False)
