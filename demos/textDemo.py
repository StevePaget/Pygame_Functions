from pygame_functions import *
import random
screenSize(800,800)

# This demo shows you the textBox (for easy typed input) and the label (for text output)


instructionLabel = makeLabel("Please enter a word", 40, 10, 10, "blue", "Agency FB", "yellow")
showLabel(instructionLabel)

wordBox = makeTextBox(10, 80, 300, 0, "Enter text here", 15, 24)
showTextBox(wordBox)
entry = textBoxInput(wordBox)


wordlabel = makeLabel(entry, 30, random.randint(1,700), random.randint(50,700), "red")
showLabel(wordlabel)

pause(1000)
moveLabel(wordlabel, 300,300)


wordlabel = makeLabel(entry, 30, random.randint(1,700), random.randint(50,700), "red")
showLabel(wordlabel)

pause(1000)
hideLabel(wordlabel)


endWait()
