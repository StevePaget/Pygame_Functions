from pygame_functions import *

screenSize(750,750)
setBackgroundImage("images/stars.png")
setIcon("images/lander.png")
setWindowTitle("Moon Lander")

surface = makeSprite("images/moonSurface.jpg")  # create the sprite object
moveSprite(surface, 0, 650)                     # move it into position. It is not visible yet
showSprite(surface)                             # display it

lander = makeSprite("images/lander.png")        # create the sprite object
addSpriteImage(lander,"images/landerCrash.png") # add the crashed image
moveSprite(lander, 280, 0)                      # move it into position. It is not visible yet
showSprite(lander)                              # display it


ypos = 0
yspeed = 0
upthrust = 0

while True:
    if keyPressed("up"):        # check the Wiki for a list of keys that are recognised
        upthrust = 2
    else:
        upthrust = 0

    ypos += yspeed
    moveSprite(lander, 280, ypos)
    yspeed += 1 - upthrust      # add a bit of acceleration due to gravity
    

    if touching(lander, surface):
        ypos = 650 - 150        # place the lander on the surface
        if yspeed > 10:
            changeSpriteImage(lander, 1)
        yspeed = 0              # stop the movement
        pause(1000)
        break
    tick(30)
    
endWait()
print("done")
