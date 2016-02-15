# wghs (Wakefield Graphics Helper Scripts)


# Report bugs to spaget@wghsss.org.uk


import pygame, math , sys, os


bgcolor = pygame.Color("black")
pygame.mixer.pre_init(44100,-16,2,512) 
pygame.init()
pygame.mixer.init()
spriteGroup = pygame.sprite.OrderedUpdates()
textboxGroup = pygame.sprite.OrderedUpdates()
gameClock = pygame.time.Clock()

keydict = {"space":pygame.K_SPACE,"esc":pygame.K_ESCAPE,"up":pygame.K_UP,"down":pygame.K_DOWN,"left":pygame.K_LEFT,"right":pygame.K_RIGHT,
"a":pygame.K_a, 
"b":pygame.K_b, 
"c":pygame.K_c, 
"d":pygame.K_d, 
"e":pygame.K_e, 
"f":pygame.K_f, 
"g":pygame.K_g, 
"h":pygame.K_h, 
"i":pygame.K_i, 
"j":pygame.K_j, 
"k":pygame.K_k, 
"l":pygame.K_l, 
"m":pygame.K_m, 
"n":pygame.K_n, 
"o":pygame.K_o, 
"p":pygame.K_p, 
"q":pygame.K_q, 
"r":pygame.K_r, 
"s":pygame.K_s, 
"t":pygame.K_t, 
"u":pygame.K_u, 
"v":pygame.K_v, 
"w":pygame.K_w, 
"x":pygame.K_x, 
"y":pygame.K_y, 
"z":pygame.K_z,
"1":pygame.K_1, 
 "2":pygame.K_2, 
 "3":pygame.K_3, 
 "4":pygame.K_4, 
 "5":pygame.K_5, 
 "6":pygame.K_6, 
 "7":pygame.K_7, 
 "8":pygame.K_8, 
 "9":pygame.K_9,
 "0":pygame.K_0}
screen = ""
bgSurface = ""

    
class newSprite(pygame.sprite.Sprite):
    def __init__(self,filename):
        pygame.sprite.Sprite.__init__(self)
        self.originalImage = loadImage(filename)
        self.image = pygame.Surface.copy(self.originalImage)
        self.rect=self.image.get_rect()
        self.rect.topleft=(0,0)
        self.mask = pygame.mask.from_surface(self.image)
        
    def move(self,xpos,ypos):
        self.rect.topleft = [xpos,ypos]        
        
class newTextBox(pygame.sprite.Sprite):
    def __init__(self,text,xpos,ypos,width,case):
        pygame.sprite.Sprite.__init__(self)
        self.text = ""
        self.width=width
        self.initialText = text
        self.case=case
        self.image = pygame.Surface((width,30))
        self.image.fill((255,255,255))
        pygame.draw.rect(self.image,(0,0,0),[0,0,width-1,29],2)
        self.rect=self.image.get_rect()
        self.fontFace = pygame.font.match_font("Arial")
        self.fontColour = pygame.Color("black")
        self.initialColour = (180,180,180)
        self.font = pygame.font.Font(self.fontFace,14)
        self.rect.topleft = [xpos,ypos]
        newSurface = self.font.render(self.initialText,True,self.initialColour)
        self.image.blit(newSurface,[10,10])
    
        
    def update(self,key):
        if key >31 and key < 127: # only printable characters
            keys = pygame.key.get_pressed()
            if key > 96 and key < 123: #only allow shift on letters
                if self.case == 2 or ((keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and self.case==0):
                    key -=32
            self.text += chr(key)
        elif key == 8:
            #backspace. repeat until clear
            keys = pygame.key.get_pressed()
            nexttime = pygame.time.get_ticks()+200
            deleting = True
            while deleting:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_BACKSPACE]:
                    thistime = pygame.time.get_ticks()
                    if thistime > nexttime:
                        self.text = self.text[0:len(self.text)-1]
                        self.image.fill((255,255,255))
                        pygame.draw.rect(self.image,(0,0,0),[0,0,self.width-1,29],2)
                        newSurface = self.font.render(self.text,True,self.fontColour)
                        self.image.blit(newSurface,[10,10])
                        updateDisplay()
                        nexttime = thistime + 50
                        pygame.event.clear()
                else:
                    deleting=False
                
        self.image.fill((255,255,255))
        pygame.draw.rect(self.image,(0,0,0),[0,0,self.width-1,29],2)
        newSurface = self.font.render(self.text,True,self.fontColour)
        self.image.blit(newSurface,[10,10])
        updateDisplay()

    def move(self,xpos,ypos):
        self.rect.topleft = [xpos,ypos]

    def clear(self):
        self.image.fill((255,255,255))
        pygame.draw.rect(self.image,(0,0,0),[0,0,self.width-1,29],2)
        newSurface = self.font.render(self.initialText,True,self.initialColour)
        self.image.blit(newSurface,[10,10])
        updateDisplay()
        
class newLabel(pygame.sprite.Sprite):
    def __init__(self,text,fontSize,font,fontColour,xpos,ypos,background):
        pygame.sprite.Sprite.__init__(self)
        self.fontColour = pygame.Color(fontColour)
        self.fontFace = pygame.font.match_font(font)
        self.fontSize = fontSize
        self.background = background
        self.font = pygame.font.Font(self.fontFace,self.fontSize)
        newSurface = self.font.render(text,True,self.fontColour)
        self.rect = newSurface.get_rect()
        if self.background !="clear":
            self.image = pygame.Surface((self.rect.width,self.rect.height))
            self.image.fill(pygame.Color(background))
            self.image.blit(newSurface,[0,0])
        else:
            self.image = newSurface
        self.rect.topleft = [xpos,ypos]
        
    def update(self, newText, newFontColour, newBackColour):
        if newFontColour:
            self.fontColour = parseColour(newFontColour)
        if newBackColour:
            self.background = parseColour(newFontColour)
        oldTopLeft = self.rect.topleft
        newSurface = self.font.render(newText,True,self.fontColour)
        self.rect = newSurface.get_rect()
        if self.background !="clear":
            self.image = pygame.Surface((self.rect.width,self.rect.height))
            self.image.fill(self.background)
            self.image.blit(newSurface,[0,0])
        else:
            self.image = newSurface
        self.rect.topleft = oldTopLeft


#this first function is just a re-usable way of loading images from disk.
#It is used whenever the program wants to grab a graphic
def loadImage( fileName, useColorKey = False ):
    if os.path.isfile(fileName):
        image = pygame.image.load( fileName )
        image = image.convert_alpha()
        # Return the image
        return image

def screenSize(sizex, sizey,xpos=None,ypos=None):
    global bgcolor
    global screen
    global bgSurface
    if xpos != None and ypos != None:
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (xpos,ypos+50)
    else:
        windowInfo = pygame.display.Info()
        monitorWidth = windowInfo.current_w
        monitorHeight = windowInfo.current_h
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % ((monitorWidth-sizex)/2,(monitorHeight-sizey)/2)
    screen = pygame.display.set_mode([sizex,sizey])
    screen.fill(bgcolor)
    pygame.display.set_caption("Graphics Window")
    bgSurface = screen.copy()
    pygame.display.update()


def moveSprite(sprite,x,y):
    sprite.move(x,y)
    updateDisplay()

def rotateSprite(sprite,angle):
    oldmiddle = sprite.rect.center
    sprite.image = pygame.transform.rotate(sprite.originalImage, angle)
    sprite.rect = sprite.image.get_rect()
    sprite.rect.center = oldmiddle
    updateDisplay()
    
def killSprite(sprite):
    sprite.kill()

def setBackgroundColour(colour):
    global bgcolor
    global bgSurface

    bgcolor = parseColour(colour)
    screen.fill(bgcolor)
    pygame.display.update()
    bgSurface = screen.copy()
    
def hideSprite(sprite):
    spriteGroup.remove(sprite)
    pygame.display.update()

def showSprite(sprite):
    spriteGroup.add(sprite)
    updateDisplay()


def makeSprite(filename):
    thisSprite = newSprite(filename)
    return thisSprite

def changeSpriteImage(sprite, image):
    sprite.image = image
    oldcenter = sprite.rect.center
    sprite.rect=sprite.image.get_rect()
    sprite.rect.center = oldcenter
    sprite.mask = pygame.mask.from_surface(sprite.image)    
    updateDisplay()
    
def makeImage(filename):
    return loadImage(filename)

def touching(sprite1, sprite2):
    collided = pygame.sprite.collide_mask(sprite1,sprite2)
    return collided

def pause(milliseconds, allowEsc = True):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        waittime=current_time + milliseconds
        while not (current_time>waittime or (keys[pygame.K_ESCAPE] and allowEsc)):
                pygame.event.clear()
                keys = pygame.key.get_pressed()
                if (keys[pygame.K_ESCAPE] and allowEsc):
                    pygame.quit()
                    sys.exit()
                current_time = pygame.time.get_ticks()

def drawRect(xpos,ypos,width,height,colour,linewidth=0):
    global bgSurface
    colour = parseColour(colour)
    thisrect = pygame.draw.rect(screen,colour,[xpos,ypos,width,height],linewidth)
    bgrect = pygame.draw.rect(bgSurface,colour,[xpos,ypos,width,height],linewidth)
    pygame.display.update(thisrect)


def drawLine(x1,y1,x2,y2,colour,linewidth=1):
    global bgSurface
    colour = parseColour(colour)
    thisrect = pygame.draw.line(screen, colour, (x1,y1), (x2,y2), linewidth)  
    bgrect = pygame.draw.line(screen, colour, (x1,y1), (x2,y2), linewidth)    
    pygame.display.update(thisrect)
    
def drawPolygon(pointlist,colour,linewidth=0):
    global bgSurface
    colour = parseColour(colour)
    thisrect = pygame.draw.polygon(screen, colour, pointlist, linewidth)
    bgrect = pygame.draw.polygon(bgSurface, colour, pointlist, linewidth) 
    pygame.display.update(thisrect)

def drawEllipse(centreX,centreY,width, height,colour,linewidth=0):
    global bgSurface
    colour = parseColour(colour)
    thisrect = pygame.Rect(centreX-width/2,centreY-height/2,width,height)
    pygame.draw.ellipse(screen, colour, thisrect, linewidth)
    pygame.draw.ellipse(bgSurface, colour, thisrect, linewidth)
    pygame.display.update(thisrect)


def drawTriangle(x1,y1,x2,y2,x3,y3, colour,linewidth=0):
    global bgSurface
    colour = parseColour(colour)
    thisrect = pygame.draw.polygon(screen, colour, [(x1,y1),(x2,y2),(x3,y3)], linewidth)
    bgrect = pygame.draw.polygon(bgSurface, colour, [(x1,y1),(x2,y2),(x3,y3)], linewidth) 
    pygame.display.update(thisrect)    
    
def clearShapes():
    global bgcolor
    global bgSurface
    screen.fill(bgcolor)
    bgSurface = screen.copy()
    updateShapes()

def updateShapes():
    pygame.display.update()
    
def end():
    pygame.quit()

def makeSound(filename):
    pygame.mixer.init()
    thissound = pygame.mixer.Sound(filename)
    return thissound

def playSound(sound,loops=0):
    sound.play(loops)

def stopSound(sound):
    sound.stop()
    
def playSoundAndWait(sound):
    sound.play()
    while pygame.mixer.get_busy():
        #pause
        pause(10)


def endWait():
        print("Press ESC to quit")
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        waittime=0
        while not keys[pygame.K_ESCAPE]:
            current_time = pygame.time.get_ticks()
            if current_time >waittime:
                pygame.event.clear()
                keys = pygame.key.get_pressed()
                waittime += 20
        pygame.quit()

def keyPressed(keyCheck=""):
    global keydict
    keyCode = keydict[keyCheck.lower()]
    pygame.event.clear()
    keys = pygame.key.get_pressed()
    if keys[keyCode] or keyCheck=="":
        return True
    else:
        return False


def makeLabel(text,fontSize,xpos,ypos,fontColour='black',font='Arial',background="clear"):
    #make a text sprite
    thisText = newLabel(text,fontSize,font,fontColour,xpos,ypos,background)
    return thisText

def moveLabel(sprite,x,y):
    sprite.rect.topleft=[x,y]
    updateDisplay()

def changeLabel(textObject,newText,newFontColour=None,newBackColour=None):
    textObject.update(newText,newFontColour, newBackColour)
    updateDisplay()

def waitPress():
    pygame.event.clear()
    keypressed= False
    thisevent = pygame.event.wait()
    while thisevent.type != pygame.KEYDOWN:
        thisevent = pygame.event.wait()
    return thisevent.key

def makeTextBox(xpos,ypos,width,case=0,startingText="Please type here"):
    thisTextBox = newTextBox(startingText,xpos,ypos,width,case)
    textboxGroup.add(thisTextBox)
    return thisTextBox

def textBoxInput(textbox):
    #starts grabbing key inputs, putting into textbox until enter pressed
    global keydict
    textbox.text=""
    while True:
        updateDisplay()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    textbox.clear()
                    return textbox.text
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    textbox.update(event.key)
            elif event.type== pygame.QUIT:
                pygame.quit()
                sys.exit()
        
    
def clock():
    current_time = pygame.time.get_ticks()
    return current_time
    
def tick(fps):
    gameClock.tick(fps)
    
def showLabel(labelSprite):
    textboxGroup.add(labelSprite)
    updateDisplay()

def hideLabel(labelSprite):
    textboxGroup.remove(labelSprite)
    updateDisplay()
    
def updateDisplay():
    global bgSurface
    spriteRects = spriteGroup.draw(screen)
    textboxRects= textboxGroup.draw(screen)
    pygame.display.update()
    spriteGroup.clear(screen, bgSurface)
    textboxGroup.clear(screen, bgSurface)    


def mousePressed():
    pygame.event.clear()
    mouseState = pygame.mouse.get_pressed()
    if mouseState[0]:
        return True
    else:
        return False

def spriteClicked(sprite):
    mouseState = pygame.mouse.get_pressed()
    if not mouseState[0]:
        return False  #not pressed
    pos = pygame.mouse.get_pos()
    if sprite.rect.collidepoint(pos):
        return True
    else:
        return False
    
    
def parseColour(colour):
    if type(colour) == str:
        #check to see if valid colour
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
