from pygame_functions import *
import math

screenSize(1000, 750)
setBackgroundImage("images/stars.png")

rocket = makeSprite("images/rocket1.png")
addSpriteImage(rocket,"images/rocket2a.png")
addSpriteImage(rocket,"images/rocket2b.png")

thrustSound = makeSound("sounds/Rocket-SoundBible.wav")


xPos = 500
yPos = 320
xSpeed = 0
ySpeed = 0
angle=0
thrustAmount = 0.5
moveSprite(rocket, xPos, yPos,True)
showSprite(rocket)
thrustFrame = 1
nextframe = clock()

while True:
    if keyPressed("left"):
        angle = angle - 5

        transformSprite(rocket, angle, 1)

    elif keyPressed("right"):
        angle = angle +5
        transformSprite(rocket, angle, 1)

    if keyPressed("up"):
        if clock() > nextframe:
            nextframe = clock() + 200
            if thrustFrame == 1:
                changeSpriteImage(rocket,1)
                thrustFrame=2
            else:
                changeSpriteImage(rocket,2)
                thrustFrame=1
        # use Trigonometry to convert the thrust into 2 components, x and y
        xSpeed += math.sin(math.radians(angle)) * thrustAmount
        ySpeed -= math.cos(math.radians(angle)) * thrustAmount
        playSound(thrustSound)

    else:
        changeSpriteImage(rocket,0)
        stopSound(thrustSound)

    xPos += xSpeed
    if xPos > 1000:
        xPos = 0
    elif xPos < 0:
        xPos = 1000

    yPos += ySpeed
    if yPos > 750:
        yPos = 0
    elif yPos < 0:
        yPos = 750

    moveSprite(rocket, xPos, yPos,True)
    tick(30)

endWait()
