from pygame_functions import *


screenSize(500,500)
textlabel = makeLabel("Welcome", 22,200,50,"white", font="impact")
showLabel(textlabel)

b1 = makeSprite("images/button1.png")
moveSprite(b1, 200,150)
b2 = makeSprite("images/button2.png")
moveSprite(b2, 200,200)
showSprite(b1)
showSprite(b2)

def clicked1():
    changeLabel(textlabel,"Clicked Button 1")

def clicked2():
    changeLabel(textlabel,"Clicked Button 2")

while True:
    if spriteClicked(b1):
        clicked1()
    elif spriteClicked(b2):
        clicked2()
    tick(30)


endWait()