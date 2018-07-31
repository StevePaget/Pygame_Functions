from pygame_functions import *
import math, random

screenSize(1000, 750)
setBackgroundImage("images/stars.png")

rocket = makeSprite("images/rocket1.png")
addSpriteImage(rocket,"images/rocket2a.png")
addSpriteImage(rocket,"images/rocket2b.png")
thrustSound = makeSound("sounds/Rocket-SoundBible.wav")


# we will store our asteroid sprites in a list
asteroids = []
for x in range(5):
    thisAsteroid = makeSprite("images/asteroid.png")
    # we will also add an alternative image to each sprite
    addSpriteImage(thisAsteroid, "images/redasteroid.png")
    # we will give each asteroid a random x position and a random y position
    # we will use dot notation to store this position *inside* the Sprite object
    thisAsteroid.x = random.randint(0,1000)
    thisAsteroid.y = random.randint(0,750)
    moveSprite(thisAsteroid, thisAsteroid.x, thisAsteroid.y)
    #also, store a random x speed and random y speed inside each asteroid Sprite
    thisAsteroid.xspeed = random.randint(-5,5)
    thisAsteroid.yspeed = random.randint(-5,5)
    showSprite(thisAsteroid)
    #now add this asteroid to the list
    asteroids.append(thisAsteroid)

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

        transformSprite(rocket,angle,1)

    elif keyPressed("right"):
        angle = angle +5
        transformSprite(rocket, angle, 1)

    if keyPressed("h"):
        hideAll()

    if keyPressed("u"):
        unhideAll()


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

    # now we will move all the asteroids by their speeds
    for thisAsteroid in asteroids:
        thisAsteroid.x += thisAsteroid.xspeed
        if thisAsteroid.x > 1000:
            thisAsteroid.x = 0
        elif thisAsteroid.x < 0:
            thisAsteroid.x = 1000

        thisAsteroid.y += thisAsteroid.yspeed
        if thisAsteroid.y > 750:
            thisAsteroid.y = 0
        elif thisAsteroid.y < 0:
            thisAsteroid.y = 750

        moveSprite(thisAsteroid, thisAsteroid.x, thisAsteroid.y)

    # now we will grab a list of all the sprites that are currently touching the rocket
    hitAsteroids = allTouching(rocket)
    # and change the image of each one
    for thisHitAsteroid in hitAsteroids:
        changeSpriteImage(thisHitAsteroid,1)

    tick(30)

endWait()
