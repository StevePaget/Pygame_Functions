from pygame_functions import *

screenSize(750,750)
setBackgroundImage("images/stars.png")


surface = makeSprite("images/moonSurface.jpg")  # create the sprite object
moveSprite(surface, 0, 650)                     # move it into position. It is not visible yet
showSprite(surface)                             # display it

lander = makeSprite("images/lander.png")        # create the sprite object
addSpriteImage(lander,"images/landerCrash.png") # add the crashed image
moveSprite(lander, 280, 0)                      # move it into position. It is not visible yet
showSprite(lander)                              # display it

fuelColour = "yellow"
fuelLabel = makeLabel("Fuel: 50", 28, 10, 10, fuelColour)
showLabel(fuelLabel)

ypos = 0
yspeed = 0
upthrust = 0
fuel = 50

while True:
    if keyPressed("up") and fuel > 0:       # only allow thrust if some fuel exists
        upthrust = 2
        fuel = fuel - 1                     # remove some fuel
        if fuel < 10:
            fuelColour = "red"              # Warning for low fuel

        changeLabel(fuelLabel,"Fuel: " + str(int(fuel)), fuelColour)  # Update the label
    else:
        upthrust = 0

    ypos += yspeed
    moveSprite(lander, 280, ypos)
    yspeed += 1 - upthrust      # add a bit of acceleration due to gravity
    

    if touching(lander, surface):
        ypos = 650 - 150        # place the lander on the surface
        if yspeed > 10:
            changeSpriteImage(lander,1)
        yspeed = 0              # stop the movement
        break


    tick(30)


