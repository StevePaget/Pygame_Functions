from pygame_functions import *

screenSize(1000, 750)
setBackgroundImage("images/stars.png")

rocket = makeSprite("images/rocket1.png")
moveSprite(rocket,500,300)

showSprite(rocket)

scale = 10
scaleChange = 10
angle = 0

while True:
    angle +=5
    scale += scaleChange
    transformSprite(rocket, angle, scale/100)
    if scale > 300:
        scaleChange = -10
    elif scale <20:
        scaleChange = 10
    pause(20)

endWait()
