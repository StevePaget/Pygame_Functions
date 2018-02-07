from pygame_functions import *
import random
screenSize(800,800)
setBackgroundColour("white")

text = "Hello"
xpos = 10
multiLineLabel = makeLabel(text, 27, xpos, 10, "black", "Times")
showLabel(multiLineLabel)

inputBox = makeTextBox(10, 760, 200, 0)
showTextBox(inputBox)


for x in range (26):
    newText = textBoxInput(inputBox)
    text += "<br>" + newText
    changeLabel(multiLineLabel,text, "black",random.choice(["blue","red","green","yellow",[255,90,90],[255,255,255]]))
    moveLabel(multiLineLabel,xpos+(x*20),10)


endWait()
