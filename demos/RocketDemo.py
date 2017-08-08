from pygame_functions import *

screenSize(1000, 750)
setBackgroundImage("images/stars.png")

rocket = makeSprite("images/rocket1.png")
addSpriteImage(rocket,"images/rocket2a.png")


xPos = 500
yPos = 320
xSpeed = 0
ySpeed = 0
moveSprite(rocket, xPos, yPos)
showSprite(rocket)

while True:
    if keyPressed("up"):
        changeSpriteImage(rocket,1)
        transformSprite(rocket, 0,1)
        ySpeed -= 2

    elif keyPressed("down"):
        changeSpriteImage(rocket,1)
        transformSprite(rocket, 180,1)
        ySpeed += 2

    elif keyPressed("right"):
        changeSpriteImage(rocket,1)
        transformSprite(rocket, 90,1)
        xSpeed += 2

    elif keyPressed("left"):
        changeSpriteImage(rocket,1)
        transformSprite(rocket, -90,1)
        xSpeed -= 2
      
    else:
        changeSpriteImage(rocket,0)

    xPos += xSpeed
    if xPos > 960:
        xPos = -100
    elif xPos < -100:
        xPos = 960

    yPos += ySpeed
    if yPos > 700:
        yPos = -100
    elif yPos < -100:
        yPos = 700

    moveSprite(rocket, xPos, yPos)

    tick(30)

endWait()
