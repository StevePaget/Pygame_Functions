from pygame_functions import *

screenSize(750,750)


surface = makeSprite("images/moonSurface.jpg")  # create the sprite object
moveSprite(surface, 0, 650)                     # move it into position. It is not visible yet
showSprite(surface)                             # display it

lander = makeSprite("images/lander.png")       # create the sprite object
moveSprite(lander, 280, 0)                     # move it into position. It is not visible yet
showSprite(lander)                             # display it


ypos = 0
yspeed = 0
while True:
    ypos += yspeed              
    moveSprite(lander, 280, ypos)
    yspeed += 1                 # add a bit of acceleration due to gravity
    
    if touching(lander, surface):
        ypos = 650 - 150        # place the lander on the surface
        yspeed = 0              # stop the movement
    
    if keyPressed("up"):        # check the Wiki for a list of keys that are recognised
        yspeed = -20            # add some upward thrust
    
    pause(30)                   # This pause also includes checking for Esc press (which quits)
    
endWait()
