from pygame_functions import *


screenSize(600,600)
setAutoUpdate(False)


setBackgroundImage( [  ["images/dungeonFloor1.png", "images/dungeonFloor2.png"] ,
                       ["images/dungeonFloor3.png", "images/dungeonFloor4.png"]  ])


testSprite  = makeSprite("images/links.gif",32)  # links.gif contains 32 separate frames of animation. Sizes are automatically calculated.

moveSprite(testSprite,300,300,True)

showSprite(testSprite)

nextFrame = clock()
frame=0
while True:
    if clock() > nextFrame:                         # We only animate our character every 80ms.
        frame = (frame+1)%8                         # There are 8 frames of animation in each direction
        nextFrame += 80                             # so the modulus 8 allows it to loop

    if keyPressed("right"):
        changeSpriteImage(testSprite, 0*8+frame)    # 0*8 because right animations are the 0th set in the sprite sheet
        scrollBackground(-5,0)                      # The player is moving right, so we scroll the background left

    elif keyPressed("down"):
        changeSpriteImage(testSprite, 1*8+frame)    # down facing animations are the 1st set
        scrollBackground(0, -5)

    elif keyPressed("left"):
        changeSpriteImage(testSprite, 2*8+frame)    # and so on
        scrollBackground(5,0)

    elif keyPressed("up"):
        changeSpriteImage(testSprite,3*8+frame)
        scrollBackground(0,5)

    else:
        changeSpriteImage(testSprite, 1 * 8 + 5)  # the static facing front look

    updateDisplay()
    tick(120)

endWait()
