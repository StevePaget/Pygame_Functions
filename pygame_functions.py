# pygame_functions

# Documentation at www.github.com/stevepaget/pygame_functions
# Report bugs at https://github.com/StevePaget/Pygame_Functions/issues


import pygame, sys, os

from pathlib import Path
DIR = Path(__file__).parent.absolute()
DIR = f'{DIR}'.replace('\\','/')
os.chdir(DIR)


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init()
spriteGroup = pygame.sprite.OrderedUpdates()
textboxGroup = pygame.sprite.OrderedUpdates()
gameClock = pygame.time.Clock()
musicPaused = False
hiddenSprites = pygame.sprite.OrderedUpdates()
screenRefresh = True
background = None

keydict = {"space": pygame.K_SPACE, "esc": pygame.K_ESCAPE, "up": pygame.K_UP, "down": pygame.K_DOWN,
           "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "return": pygame.K_RETURN,
           "a": pygame.K_a,
           "b": pygame.K_b,
           "c": pygame.K_c,
           "d": pygame.K_d,
           "e": pygame.K_e,
           "f": pygame.K_f,
           "g": pygame.K_g,
           "h": pygame.K_h,
           "i": pygame.K_i,
           "j": pygame.K_j,
           "k": pygame.K_k,
           "l": pygame.K_l,
           "m": pygame.K_m,
           "n": pygame.K_n,
           "o": pygame.K_o,
           "p": pygame.K_p,
           "q": pygame.K_q,
           "r": pygame.K_r,
           "s": pygame.K_s,
           "t": pygame.K_t,
           "u": pygame.K_u,
           "v": pygame.K_v,
           "w": pygame.K_w,
           "x": pygame.K_x,
           "y": pygame.K_y,
           "z": pygame.K_z,
           "1": pygame.K_1,
           "2": pygame.K_2,
           "3": pygame.K_3,
           "4": pygame.K_4,
           "5": pygame.K_5,
           "6": pygame.K_6,
           "7": pygame.K_7,
           "8": pygame.K_8,
           "9": pygame.K_9,
           "0": pygame.K_0,
           "num0": pygame.K_KP0,
           "num1": pygame.K_KP1,
           "num2": pygame.K_KP2,
           "num3": pygame.K_KP3,
           "num4": pygame.K_KP4,
           "num5": pygame.K_KP5,
           "num6": pygame.K_KP6,
           "num7": pygame.K_KP7,
           "num8": pygame.K_KP8,
           "num9": pygame.K_KP9}
screen = ""


class Background():
    def __init__(self):
        self.colour = pygame.Color("black")

    def setTiles(self, tiles):
        if type(tiles) is str:
            self.tiles = [[loadImage(tiles)]]
        elif type(tiles[0]) is str:
            self.tiles = [[loadImage(i) for i in tiles]]
        else:
            self.tiles = [[loadImage(i) for i in row] for row in tiles]
        self.stagePosX = 0
        self.stagePosY = 0
        self.tileWidth = self.tiles[0][0].get_width()
        self.tileHeight = self.tiles[0][0].get_height()
        screen.blit(self.tiles[0][0], [0, 0])
        self.surface = screen.copy()

    def scroll(self, x, y):
        self.stagePosX -= x
        self.stagePosY -= y
        col = (self.stagePosX % (self.tileWidth * len(self.tiles[0]))) // self.tileWidth
        xOff = (0 - self.stagePosX % self.tileWidth)
        row = (self.stagePosY % (self.tileHeight * len(self.tiles))) // self.tileHeight
        yOff = (0 - self.stagePosY % self.tileHeight)

        col2 = ((self.stagePosX + self.tileWidth) % (self.tileWidth * len(self.tiles[0]))) // self.tileWidth
        row2 = ((self.stagePosY + self.tileHeight) % (self.tileHeight * len(self.tiles))) // self.tileHeight
        screen.blit(self.tiles[row][col], [xOff, yOff])
        screen.blit(self.tiles[row][col2], [xOff + self.tileWidth, yOff])
        screen.blit(self.tiles[row2][col], [xOff, yOff + self.tileHeight])
        screen.blit(self.tiles[row2][col2], [xOff + self.tileWidth, yOff + self.tileHeight])

        self.surface = screen.copy()

    def setColour(self, colour):
        self.colour = parseColour(colour)
        screen.fill(self.colour)
        pygame.display.update()
        self.surface = screen.copy()


class newSprite(pygame.sprite.Sprite):
    def __init__(self, filename, frames=1, altDims = None):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        img = loadImage(filename)
        if altDims:
            img = pygame.transform.scale(img, (altDims[0]*frames, altDims[1]))
        self.originalWidth = img.get_width() // frames
        self.originalHeight = img.get_height()
        frameSurf = pygame.Surface((self.originalWidth, self.originalHeight), pygame.SRCALPHA, 32)
        x = 0
        for frameNo in range(frames):
            frameSurf = pygame.Surface((self.originalWidth, self.originalHeight), pygame.SRCALPHA, 32)
            frameSurf.blit(img, (x, 0))
            self.images.append(frameSurf.copy())
            x -= self.originalWidth
        self.image = pygame.Surface.copy(self.images[0])

        self.currentImage = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = 0
        self.scale = 1

    def addImage(self, filename):
        self.images.append(loadImage(filename))

    def move(self, xpos, ypos, centre=False):
        if centre:
            self.rect.center = [xpos, ypos]
        else:
            self.rect.topleft = [xpos, ypos]

    def changeImage(self, index):
        self.currentImage = index
        if self.angle == 0 and self.scale == 1:
            self.image = self.images[index]
        else:
            self.image = pygame.transform.rotozoom(self.images[self.currentImage], -self.angle, self.scale)
        oldcenter = self.rect.center
        self.rect = self.image.get_rect()
        originalRect = self.images[self.currentImage].get_rect()
        self.originalWidth = originalRect.width
        self.originalHeight = originalRect.height
        self.rect.center = oldcenter
        self.mask = pygame.mask.from_surface(self.image)
        if screenRefresh:
            updateDisplay()


class newTextBox(pygame.sprite.Sprite):
    def __init__(self, text, xpos, ypos, width, case, maxLength, fontSize):
        pygame.sprite.Sprite.__init__(self)
        self.text = ""
        self.width = width
        self.initialText = text
        self.case = case
        self.maxLength = maxLength
        self.boxSize = int(fontSize * 1.7)
        self.image = pygame.Surface((width, self.boxSize))
        self.image.fill((255, 255, 255))
        pygame.draw.rect(self.image, (0, 0, 0), [0, 0, width - 1, self.boxSize - 1], 2)
        self.rect = self.image.get_rect()
        self.fontFace = pygame.font.match_font("Arial")
        self.fontColour = pygame.Color("black")
        self.initialColour = (180, 180, 180)
        self.font = pygame.font.Font(self.fontFace, fontSize)
        self.rect.topleft = [xpos, ypos]
        newSurface = self.font.render(self.initialText, True, self.initialColour)
        self.image.blit(newSurface, [10, 5])

    def update(self, keyevent):
        key = keyevent.key
        unicode = keyevent.unicode
        if (31 < key < 127 or 255 < key < 266) and (
                self.maxLength == 0 or len(self.text) < self.maxLength):  # only printable characters
            if keyevent.mod in (1, 2) and self.case == 1 and key >= 97 and key <= 122:
                # force lowercase letters
                self.text += chr(key)
            elif keyevent.mod == 0 and self.case == 2 and key >= 97 and key <= 122:
                self.text += chr(key - 32)
            else:
                # use the unicode char
                self.text += unicode

        elif key == 8:
            # backspace. repeat until clear
            keys = pygame.key.get_pressed()
            nexttime = pygame.time.get_ticks() + 200
            deleting = True
            while deleting:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_BACKSPACE]:
                    thistime = pygame.time.get_ticks()
                    if thistime > nexttime:
                        self.text = self.text[0:len(self.text) - 1]
                        self.image.fill((255, 255, 255))
                        pygame.draw.rect(self.image, (0, 0, 0), [0, 0, self.width - 1, self.boxSize - 1], 2)
                        newSurface = self.font.render(self.text, True, self.fontColour)
                        self.image.blit(newSurface, [10, 5])
                        updateDisplay()
                        nexttime = thistime + 50
                        pygame.event.clear()
                else:
                    deleting = False

        self.image.fill((255, 255, 255))
        pygame.draw.rect(self.image, (0, 0, 0), [0, 0, self.width - 1, self.boxSize - 1], 2)
        newSurface = self.font.render(self.text, True, self.fontColour)
        self.image.blit(newSurface, [10, 5])
        if screenRefresh:
            updateDisplay()

    def move(self, xpos, ypos, centre=False):
        if centre:
            self.rect.topleft = [xpos, ypos]
        else:
            self.rect.center = [xpos, ypos]

    def clear(self):
        self.image.fill((255, 255, 255))
        pygame.draw.rect(self.image, (0, 0, 0), [0, 0, self.width - 1, self.boxSize - 1], 2)
        newSurface = self.font.render(self.initialText, True, self.initialColour)
        self.image.blit(newSurface, [10, 5])
        if screenRefresh:
            updateDisplay()


class newLabel(pygame.sprite.Sprite):
    def __init__(self, text, fontSize, font, fontColour, xpos, ypos, background):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.fontColour = parseColour(fontColour)
        self.fontFace = pygame.font.match_font(font)
        self.fontSize = fontSize
        self.background = background
        self.font = pygame.font.Font(self.fontFace, self.fontSize)
        self.renderText()
        self.rect.topleft = [xpos, ypos]

    def update(self, newText, fontColour, background):
        self.text = newText
        if fontColour:
            self.fontColour = parseColour(fontColour)
        if background:
            self.background = parseColour(background)

        oldTopLeft = self.rect.topleft
        self.renderText()
        self.rect.topleft = oldTopLeft
        if screenRefresh:
            updateDisplay()

    def renderText(self):
        lineSurfaces = []
        textLines = self.text.split("<br>")
        maxWidth = 0
        maxHeight = 0
        for line in textLines:
            lineSurfaces.append(self.font.render(line, True, self.fontColour))
            thisRect = lineSurfaces[-1].get_rect()
            if thisRect.width > maxWidth:
                maxWidth = thisRect.width
            if thisRect.height > maxHeight:
                maxHeight = thisRect.height
        self.image = pygame.Surface((maxWidth, (self.fontSize + 1) * len(textLines) + 5), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        if self.background != "clear":
            self.image.fill(parseColour(self.background))
        linePos = 0
        for lineSurface in lineSurfaces:
            self.image.blit(lineSurface, [0, linePos])
            linePos += self.fontSize + 1
        self.rect = self.image.get_rect()


def loadImage(fileName, useColorKey=False):
    if os.path.isfile(fileName):
        image = pygame.image.load(fileName)
        image = image.convert_alpha()
        # Return the image
        return image
    else:
        raise Exception(f"Error loading image: {fileName} – Check filename and path?")


def screenSize(sizex, sizey, xpos=None, ypos=None, fullscreen=False):
    global screen
    global background
    if xpos != None and ypos != None:
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{xpos}, {ypos + 50}"
    else:
        windowInfo = pygame.display.Info()
        monitorWidth = windowInfo.current_w
        monitorHeight = windowInfo.current_h
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{(monitorWidth - sizex) // 2}, {(monitorHeight - sizey) // 2}"
    if fullscreen:
        screen = pygame.display.set_mode([sizex, sizey], pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode([sizex, sizey])
    background = Background()
    screen.fill(background.colour)
    pygame.display.set_caption("Graphics Window")
    background.surface = screen.copy()
    pygame.display.update()
    return screen



def moveSprite(sprite, x, y, centre=False):
    sprite.move(x, y, centre)
    if screenRefresh:
        updateDisplay()


def rotateSprite(sprite, angle):
    print("rotateSprite has been deprecated. Please use transformSprite")
    transformSprite(sprite, angle, 1)


def transformSprite(sprite, angle, scale, hflip=False, vflip=False):
    oldmiddle = sprite.rect.center
    if hflip or vflip:
        tempImage = pygame.transform.flip(sprite.images[sprite.currentImage], hflip, vflip)
    else:
        tempImage = sprite.images[sprite.currentImage]
    if angle != 0 or scale != 1:
        sprite.angle = angle
        sprite.scale = scale
        tempImage = pygame.transform.rotozoom(tempImage, -angle, scale)
    sprite.image = tempImage
    sprite.rect = sprite.image.get_rect()
    sprite.rect.center = oldmiddle
    sprite.mask = pygame.mask.from_surface(sprite.image)
    if screenRefresh:
        updateDisplay()


def killSprite(sprite):
    sprite.kill()
    if screenRefresh:
        updateDisplay()


def setBackgroundColour(colour):
    background.setColour(colour)
    if screenRefresh:
        updateDisplay()


def setBackgroundImage(img):
    global background
    background.setTiles(img)
    if screenRefresh:
        updateDisplay()


def hideSprite(sprite):
    hiddenSprites.add(sprite)
    spriteGroup.remove(sprite)
    if screenRefresh:
        updateDisplay()


def hideAll():
    hiddenSprites.add(spriteGroup.sprites())
    spriteGroup.empty()
    if screenRefresh:
        updateDisplay()


def unhideAll():
    spriteGroup.add(hiddenSprites.sprites())
    hiddenSprites.empty()
    if screenRefresh:
        updateDisplay()


def showSprite(sprite):
    spriteGroup.add(sprite)
    if screenRefresh:
        updateDisplay()


def makeSprite(filename, frames=1, altDims = None):
    thisSprite = newSprite(filename, frames, altDims)
    return thisSprite


def addSpriteImage(sprite, image):
    sprite.addImage(image)


def changeSpriteImage(sprite, index):
    sprite.changeImage(index)


def nextSpriteImage(sprite):
    sprite.currentImage += 1
    if sprite.currentImage > len(sprite.images) - 1:
        sprite.currentImage = 0
    sprite.changeImage(sprite.currentImage)


def prevSpriteImage(sprite):
    sprite.currentImage -= 1
    if sprite.currentImage < 0:
        sprite.currentImage = len(sprite.images) - 1
    sprite.changeImage(sprite.currentImage)


def makeImage(filename):
    return loadImage(filename)


def touching(sprite1, sprite2):
    collided = pygame.sprite.collide_mask(sprite1, sprite2)
    return collided


def allTouching(spritename):
    if spriteGroup.has(spritename):
        collisions = pygame.sprite.spritecollide(spritename, spriteGroup, False, collided=pygame.sprite.collide_mask)
        collisions.remove(spritename)
        return collisions
    else:
        return []


def pause(milliseconds, allowEsc=True):
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()
    waittime = current_time + milliseconds
    updateDisplay()
    while not (current_time > waittime or (keys[pygame.K_ESCAPE] and allowEsc)):
        pygame.event.clear()
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_ESCAPE] and allowEsc):
            pygame.quit()
            sys.exit()
        current_time = pygame.time.get_ticks()


def drawRect(xpos, ypos, width, height, colour, linewidth=0):
    global bgSurface
    colour = parseColour(colour)
    thisrect = pygame.draw.rect(screen, colour, [xpos, ypos, width, height], linewidth)
    if screenRefresh:
        pygame.display.update(thisrect)


def drawLine(x1, y1, x2, y2, colour, linewidth=1):
    global bgSurface
    colour = parseColour(colour)
    thisrect = pygame.draw.line(screen, colour, (x1, y1), (x2, y2), linewidth)
    if screenRefresh:
        pygame.display.update(thisrect)


def drawPolygon(pointlist, colour, linewidth=0):
    global bgSurface
    colour = parseColour(colour)
    thisrect = pygame.draw.polygon(screen, colour, pointlist, linewidth)
    if screenRefresh:
        pygame.display.update(thisrect)


def drawEllipse(centreX, centreY, width, height, colour, linewidth=0):
    global bgSurface
    colour = parseColour(colour)
    thisrect = pygame.Rect(centreX - width / 2, centreY - height / 2, width, height)
    pygame.draw.ellipse(screen, colour, thisrect, linewidth)
    if screenRefresh:
        pygame.display.update(thisrect)


def drawTriangle(x1, y1, x2, y2, x3, y3, colour, linewidth=0):
    global bgSurface
    colour = parseColour(colour)
    thisrect = pygame.draw.polygon(screen, colour, [(x1, y1), (x2, y2), (x3, y3)], linewidth)
    if screenRefresh:
        pygame.display.update(thisrect)


def clearShapes():
    global background
    screen.blit(background.surface, [0, 0])
    if screenRefresh:
        updateDisplay()


def updateShapes():
    pygame.display.update()


def end():
    pygame.quit()


def makeSound(filename):
    pygame.mixer.init()
    thissound = pygame.mixer.Sound(filename)

    return thissound


def playSound(sound, loops=0):
    sound.play(loops)


def stopSound(sound):
    sound.stop()


def playSoundAndWait(sound):
    sound.play()
    while pygame.mixer.get_busy():
        # pause
        pause(10)


def makeMusic(filename):
    pygame.mixer.music.load(filename)


def playMusic(loops=0):
    global musicPaused
    if musicPaused:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.play(loops)
    musicPaused = False


def stopMusic():
    pygame.mixer.music.stop()


def pauseMusic():
    global musicPaused
    pygame.mixer.music.pause()
    musicPaused = True


def rewindMusic():
    pygame.mixer.music.rewind()


def endWait():
    updateDisplay()
    print("Press ESC to quit")
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == keydict["esc"]):
                waiting = False
    pygame.quit()
    exit()



def keyPressed(keyCheck=""):
    global keydict
    keys = pygame.key.get_pressed()
    if sum(keys) > 0:
        if keyCheck == "" or keys[keydict[keyCheck.lower()]]:
            return True
    return False


def makeLabel(text, fontSize, xpos, ypos, fontColour='black', font='Arial', background="clear"):
    # make a text sprite
    thisText = newLabel(text, fontSize, font, fontColour, xpos, ypos, background)
    return thisText


def moveLabel(sprite, x, y):
    sprite.rect.topleft = [x, y]
    if screenRefresh:
        updateDisplay()


def changeLabel(textObject, newText, fontColour=None, background=None):
    textObject.update(newText, fontColour, background)
    # updateDisplay()


def waitPress():
    pygame.event.clear()
    keypressed = False
    thisevent = pygame.event.wait()
    while thisevent.type != pygame.KEYDOWN:
        thisevent = pygame.event.wait()
    return thisevent.key


def makeTextBox(xpos, ypos, width, case=0, startingText="Please type here", maxLength=0, fontSize=22):
    thisTextBox = newTextBox(startingText, xpos, ypos, width, case, maxLength, fontSize)
    textboxGroup.add(thisTextBox)
    return thisTextBox


def textBoxInput(textbox, functionToCall=None, args=[]):
    # starts grabbing key inputs, putting into textbox until enter pressed
    global keydict
    textbox.text = ""
    returnVal = None
    while True:
        updateDisplay()
        if functionToCall:
            returnVal = functionToCall(*args)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    textbox.clear()
                    if returnVal:
                        return textbox.text, returnVal
                    else:
                        return textbox.text
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    textbox.update(event)
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def clock():
    current_time = pygame.time.get_ticks()
    return current_time


def tick(fps):
    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN and event.key == keydict["esc"]) or event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    gameClock.tick(fps)
    return gameClock.get_fps()


def showLabel(labelName):
    textboxGroup.add(labelName)
    if screenRefresh:
        updateDisplay()


def hideLabel(labelName):
    textboxGroup.remove(labelName)
    if screenRefresh:
        updateDisplay()


def showTextBox(textBoxName):
    textboxGroup.add(textBoxName)
    if screenRefresh:
        updateDisplay()


def hideTextBox(textBoxName):
    textboxGroup.remove(textBoxName)
    if screenRefresh:
        updateDisplay()


def updateDisplay():
    global background
    spriteRects = spriteGroup.draw(screen)
    textboxRects = textboxGroup.draw(screen)
    pygame.display.update()
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_ESCAPE]):
        pygame.quit()
        sys.exit()
    spriteGroup.clear(screen, background.surface)
    textboxGroup.clear(screen, background.surface)


def mousePressed():
    #pygame.event.clear()
    mouseState = pygame.mouse.get_pressed()
    if mouseState[0]:
        return True
    else:
        return False


def spriteClicked(sprite):
    mouseState = pygame.mouse.get_pressed()
    if not mouseState[0]:
        return False  # not pressed
    pos = pygame.mouse.get_pos()
    if sprite.rect.collidepoint(pos):
        return True
    else:
        return False


def parseColour(colour):
    if type(colour) == str:
        # check to see if valid colour
        return pygame.Color(colour)
    else:
        colourRGB = pygame.Color("white")
        colourRGB.r = colour[0]
        colourRGB.g = colour[1]
        colourRGB.b = colour[2]
        return colourRGB


def mouseX():
    x = pygame.mouse.get_pos()
    return x[0]


def mouseY():
    y = pygame.mouse.get_pos()
    return y[1]


def scrollBackground(x, y):
    global background
    background.scroll(x, y)


def setAutoUpdate(val):
    global screenRefresh
    screenRefresh = val

def setIcon(iconfile):
    gameicon = pygame.image.load(iconfile)
    pygame.display.set_icon(gameicon)

def setWindowTitle(string):
    pygame.display.set_caption(string)


if __name__ == "__main__":
    print("pygame_functions is not designed to be run directly.\n" \
        "See the wiki at https://github.com/StevePaget/Pygame_Functions/wiki/Getting-Started for more information.")
