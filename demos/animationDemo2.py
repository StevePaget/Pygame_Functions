from pygame_functions import *


screenSize(600,600)
setBackgroundColour("pink")
testSprite  = makeSprite("images/links.gif", 32)  # links.gif contains 32 separate frames of animation.

moveSprite(testSprite,300,300,True)
showSprite(testSprite)

nextFrame = clock()
frame = 0
while True:
    if clock() > nextFrame:                         # We only animate our character every 80ms.
        frame = (frame+1)%8                         # There are 8 frames of animation in each direction
        nextFrame += 80                             # so the modulus 8 allows it to loop

    if keyPressed("num6"):
        changeSpriteImage(testSprite, 0*8+frame)    # 0*8 because right animations are the 0th set in the sprite sheet

    elif keyPressed("num2"):
        changeSpriteImage(testSprite, 1*8+frame)    # down facing animations are the 1st set

    elif keyPressed("num4"):
        changeSpriteImage(testSprite, 2*8+frame)    # and so on

    elif keyPressed("num8"):
        changeSpriteImage(testSprite, 3*8+frame)

    else:
        changeSpriteImage(testSprite, 1 * 8 + 5)  # the static facing front look

    tick(120)

endWait()
