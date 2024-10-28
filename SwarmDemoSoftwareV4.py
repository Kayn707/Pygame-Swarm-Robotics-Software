import pygame
import sys
import math
import random
import time
import os

# ======== Initializton =============
pygame.init()

#Constants
WIDTH, HEIGHT = 1280, 720
DOT_SIZE = 10
HEXAGON_SIZE = 20

# Global Varibles
Pregame = True
begin = False
Runtime = False


clickRegistered = False
timer = 0 #Currently unused
ticker = 1 #Unused currently
direction = ""

numOfRoofs = 0
numOfFrames = 0
numOfWindows = 0

#All Checks
allCheck = 0 #Used for Old Code
Tag_expansion = True #Used for Network Expasion
Tag_network = True #Network Tag
Tag_searchsort = True

#Player Modifiers
playerMod_expand = 0
playerMod_movementX = 0
playerMod_movementY = 0

#Colors
OFFWHITE = (200, 200, 200)
BLUE = (0, 0, 255)
HOTPINK = (255, 105, 180)
DARK_GRAY = (50, 50, 50)
SPRING_GREEN = (0,255,127)

# image initialization 
script_dir = os.path.abspath(os.path.dirname(__file__))

print(script_dir)

bot_image_path = os.path.join(script_dir, "Assets", "BOT2.png")
bot_image = pygame.image.load(bot_image_path)

Queen_image_path = os.path.join(script_dir, "Assets", "QueenV3.png")
Queen_image = pygame.image.load(Queen_image_path)

Closed_Truck_image_path = os.path.join(script_dir, "Assets", "Truck_closed.png")
Closed_Truck_Image = pygame.image.load(Closed_Truck_image_path)


Roof_image = pygame.image.load(os.path.join(script_dir, "Assets", "Roof.png"))
Frame_image = pygame.image.load(os.path.join(script_dir, "Assets", "Frame.png"))
Window_image = pygame.image.load(os.path.join(script_dir, "Assets", "Window.png"))

# Arrays
covered = []
plotPoints = []
trucks = []
roofs = []
frames = []
windows = []
ObjectParts = []

# Create a window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("S.R.D.S")

#========= Functions and Classes ============

def createRoof(num):
    global numOfRoofs
    numOfRoofs += 1
    roofPart = Roof(num)
    roofs.append(roofPart)
    ObjectParts.append(roofPart)

def createFrame(num):
    global numOfFrames
    numOfFrames += 1
    framePart = Frame(num)
    frames.append(framePart)
    ObjectParts.append(framePart)

def createWindow(num):
    global numOfWindows
    numOfWindows += 1
    windowPart = Window(num)
    windows.append(windowPart)
    ObjectParts.append(windowPart)


    return(False)

def checkDeliveryComplete(bot):
    global begin 
    global bringBack
    global allCheck
    if bot.distanceToTarget(WIDTH // 2, HEIGHT // 2) < 20:
            print("OBJECTIVE COMPLETE . . . OBJECT DELIVERED")
            print("NEW DIRECTIVE . . . AQUIRE OBJECT")
            print("")
            bot.tag = False
            begin = True
            bringBack = False
            allCheck = 0
            for bot in bots: 
                bot.bot_y += 30
                bot.target_X, bot.target_Y = Queen.X, Queen.Y

def bordercheck(X, Y):
    ''' 
    fixes position when it moves outside the border 
    '''
    if X > WIDTH:
        X += (X - WIDTH) * -1
    elif X < 0:
        X += (X * -1)
    if Y > HEIGHT:
        Y += (Y - HEIGHT) * -1
    elif Y < 0:
        Y += (Y * -1)
    return(X, Y)

def movementCheck(bot):
    global allCheck
    if (bot.distanceToTarget(bot.target_X, bot.target_Y) < 20):
        if bringBack:
            allCheck += 1
            screen.blit(bot_image, (bot.bot_x - 5, bot.bot_y - 5))
        if begin:
            screen.blit(bot_image, (bot.bot_x - 5, bot.bot_y - 5))
            return(None)     
    else:
        if bringBack:
            bot.moveToTarget()

# === Global Robot Commands (GLOBAL COMPUTER) ===
   
def network(): #Displays network lines
    '''
    displays the network lines for the bots
    '''
    for index, bot in enumerate(bots):
        bota = bots[index - 1]
        botb = bots[index - 2]
        pygame.draw.line(screen, SPRING_GREEN, (bot.bot_x - 5, bot.bot_y - 5), (bota.bot_x - 5, bota.bot_y - 5)) 
        pygame.draw.line(screen, SPRING_GREEN, (bot.bot_x - 5, bot.bot_y - 5), (botb.bot_x - 5, botb.bot_y - 5))

def networkExpansion(): #Unused, moves robots away from each Other
    ''' 
    When Called, Robots move a certain distance towards or away from each other and the queen
    '''

    for index, bot in enumerate(bots):
        if index == 0: 
            bot.getAway(Queen.X, Queen.Y)
        else:
            if Tag_expansion:
                bota = bots[index - 1]
                bot.getAway(bota.bot_x, bota.bot_y)
            elif not(Tag_expansion):
                bota = bots[index - 1]
                botb = bots[index - 2]
                bot.getAway(bota.bot_x, bota.bot_y)
                bot.getAway(botb.bot_x, botb.bot_y) 
        screen.blit(bot_image, (bot.bot_x - 5, bot.bot_y - 5))
        #covered.append((bot.bot_x, bot.bot_y))

# === Classes ===

class Roof(object):
    def __init__(self, num):
        self.image = Roof_image
        self.num = num
        self.X = truckRoof.X + 5 + (self.num * 3)
        self.Y = truckRoof.Y + 40
        self.taken = False
        self.delivered = False
        self.bot_control = ''
        self.partType = "Roof"
    def showSelf(self):
        screen.blit(self.image, (self.X, self.Y))

class Frame(object):
    def __init__(self, num):
        self.image = Frame_image
        self.num = num
        self.X = truckFrame.X + 5 + (self.num * 3)
        self.Y = truckFrame.Y + 20
        self.delivered = False
        self.taken = False
        self.bot_control = ''
        self.partType = "Frame"
    def showSelf(self):
        screen.blit(self.image, (self.X, self.Y))

class Window(object):
    def __init__(self, num):
        self.image = Window_image
        self.num = num
        self.X = truckWindow.X + 5 + (self.num * 3)
        self.Y = truckWindow.Y + 20
        self.delivered = False
        self.taken = False
        self.bot_control = ''
        self.partType = "Window"
    def showSelf(self):
        screen.blit(self.image, (self.X, self.Y))
    
class Truck(object):
    '''
    number assigment:
        1 = Roof
        2 = Frame
        3 = Window
    '''
    def __init__(self, num, image, X, Y):
        self.num = num
        self.image = image
        self.X = X
        self.Y = Y
        
class Bot(object):
    '''
    __Init__:  
    distanceToTarget: returns the distance from the object
    getAway: Moves away from given coordinates
    moveToTarget: Moves towards current target
    '''
    
    def __init__(self, num):
        self.num = num
        self.bot_x = 40 + (self.num * 30)
        self.bot_y = 40 
        self.target_X = self.bot_x
        self.target_Y = self.bot_y
        self.tag = False
        self.flag_getobject = True
        self.flag_deliverobject = False
        self.target_object = ''
              
    def distanceToTarget(self, X, Y):
        distance = math.sqrt((self.bot_x - X)**2 + (self.bot_y - Y)**2)
        return(distance)
                 
    def moveToTarget(self):
        deltaX = (self.target_X - self.bot_x)
        deltaY = (self.target_Y - self.bot_y)
    
        if (deltaX) > 0:
            self.bot_x += 1
            #self.bringHome("d")
            #print("RIGHT")
            screen.blit(bot_image, (self.bot_x - 5, self.bot_y - 5))
            #covered.append((self.bot_x, self.bot_y))
            
        elif (deltaX) < 0:
            self.bot_x += -1
            #self.bringHome("a")
           # print("LEFT")
            screen.blit(bot_image, (self.bot_x - 5, self.bot_y - 5))
            #covered.append((self.bot_x, self.bot_y))
            
        elif deltaY == 0:
            screen.blit(bot_image, (self.bot_x - 5, self.bot_y - 5))
            return(True)

        if (deltaY) > 0:
            self.bot_y += 1
            #self.bringHome("s")
           # print("DOWN")
            screen.blit(bot_image, (self.bot_x - 5, self.bot_y - 5))
            #covered.append((self.bot_x, self.bot_y))
                   
        elif (deltaY) < 0:
            self.bot_y += -1
            #self.bringHome("w")
           # print("UP")
            screen.blit(bot_image, (self.bot_x - 5, self.bot_y - 5))
            #covered.append((self.bot_x, self.bot_y))
            
        elif deltaX == 0:
            screen.blit(bot_image, (self.bot_x - 5, self.bot_y - 5))
            return(True)

    def getAway(self, botx, boty):
        if self.distanceToTarget(botx, boty) < (playerMod_expand - 10):
            if self.bot_x - botx < 0:
                self.bot_x -= 1
            else: 
                self.bot_x += 1
           
            if self.bot_y - boty < 0:
                self.bot_y -= 1
            else: 
                self.bot_y += 1
        elif self.distanceToTarget(botx, boty) > (playerMod_expand + 10):
            if self.bot_x - botx > 0:
                self.bot_x -= 1
            else: 
                self.bot_x += 1
           
            if self.bot_y - boty > 0:
                self.bot_y -= 1
            else: 
                self.bot_y += 1
        self.bot_x, self.bot_y = bordercheck(self.bot_x, self.bot_y)

    def goHome(self):
        self.target_X, self.target_Y = 40 + (self.num * 30), 40
        self.moveToTarget()

    def getObject(self):
        if self.target_object == '':
            self.goHome()
            return(None)
        object = self.target_object
        object.taken = True
        self.target_X, self.target_Y = object.X, object.Y
        if self.moveToTarget() == True:
            self.flag_getobject = False
            self.flag_deliverobject = True

    def deliverObject(self):
        if self.target_object == '':
            self.goHome()
            return(None)
        object = self.target_object
        object.X, object.Y = self.bot_x, self.bot_y
        self.target_X, self.target_Y =  plotPoints[object.num]
        self.target_X, self.target_Y = self.target_X + 50, self.target_Y + 50
        if self.moveToTarget() == True:
            self.target_object.delivered = True
            self.target_object = ''
            self.flag_getobject = True
            self.flag_deliverobject = False
        
    def determineObject(self):
        for object in ObjectParts:
            if not(object.delivered):
                if not(object.taken) or object.bot_control == self.num:
                    object.bot_control = self.num
                    self.target_object = object
                    break

    def searchAndSort(self):  
        if self.target_object == '':
            self.determineObject()
        if self.flag_getobject:
            self.getObject()      
        if self.flag_deliverobject:
            self.deliverObject()
        
class Queen(object):

    def __init__(self):
        self.X = (WIDTH // 2)
        self.Y = (HEIGHT // 2)
    
    def PlayerMove(self):
        global playerMod_movementX
        global playerMod_movementY
        self.X += playerMod_movementX
        playerMod_movementX = 0
        self.Y += playerMod_movementY  
        playerMod_movementY = 0 
        Queen.X, Queen.Y = bordercheck(Queen.X, Queen.Y)
        screen.blit(Queen_image, (self.X, self.Y))

#========= BOT SETUP ============
    
#Establishing Robots and Trucks 
bot1 = Bot(1)
bot2 = Bot(2)
bot3 = Bot(3)
bot4 = Bot(4)
bot5 = Bot(5)
bot6 = Bot(6)
bot7 = Bot(7)
bot8 = Bot(8)
bot9 = Bot(9)
bot10 = Bot(10)
bot11 = Bot(11)
bot12 = Bot(12)
bot13 = Bot(13)
bot14 = Bot(14)
bot15 = Bot(15)
bots = [bot1, bot2, bot3, bot4, bot5, bot6, bot7, bot8, bot9, bot10, bot11, bot12, bot13, bot14, bot15]
#bots = [bot1]


truckRoof = Truck(1, Closed_Truck_Image, 30, HEIGHT // 4)
truckFrame = Truck(2, Closed_Truck_Image, 30, (HEIGHT // 2))
truckWindow = Truck(3, Closed_Truck_Image, 30, (HEIGHT // 4) * 3)
trucks = [truckRoof, truckFrame, truckWindow]
                    
#======== MAIN GAME ============
print("NEW DIRECTIVE . . . ASSEMBLE")
print("")

running = True
while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #Add to global timer
        timer += 1
        
        # Clear the screen 
        screen.fill(DARK_GRAY)
    
        #Plot Points 
        for point in plotPoints:
            #print(point)
            plot = pygame.Rect(point, (100, 100))
            pygame.draw.rect(screen, HOTPINK, plot, 5, border_radius=1)
        
        # === PLAYER INPUT ===
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            Tag_network = False
        if keys[pygame.K_e]:
            Tag_network = True


        # === Pre-Game ===
        if Pregame:
            # Show Everything
            for bot in bots:
                bot.goHome()
            for truck in trucks:
                screen.blit(truck.image, (truck.X, truck.Y))    
            for roof in roofs:
                roof.showRoof()
            for frame in frames:
                frame.showFrame()
            for window in windows:
                window.showWindow()
            # === Initial Setup ===
            mouse_x, mouse_y = pygame.mouse.get_pos()
            rect = pygame.Rect((mouse_x) - 50, (mouse_y) - 50, 100, 100)
            pygame.draw.rect(screen, HOTPINK, rect, 5, border_radius=1)
            
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) and not(clickRegistered):
                plotPoints.append((mouse_x - 50, mouse_y - 50))
                clickRegistered = True
            elif (event.type == pygame.MOUSEBUTTONUP and event.button == 1):
                clickRegistered = False
            
            if keys[pygame.K_RETURN]:
                Pregame = False
                Runtime = True
                begin = True

        # === Begin ===
        if begin: #Creates all the house parts
            for i in range(len(plotPoints)): #Creates a part for each house plot
                createRoof(i) 
                createFrame(i)
                createWindow(i)
            begin = False

        # === Runtime ===
        if Runtime:
            for truck in trucks:
                screen.blit(truck.image, (truck.X, truck.Y))    
            if Tag_network:
                network()
            for part in ObjectParts:
                if part.partType == "Window":
                    screen.blit(part.image, (part.X - 5, part.Y + 5))
                elif part.partType == "Frame":
                    screen.blit(part.image, (part.X - 10, part.Y))
                else:
                    screen.blit(part.image, (part.X - 22, part.Y - 24))
           
           
            for bot in bots:
                    bot.searchAndSort()

        # Update the screen
        pygame.display.update()

# Quit Pygame
pygame.quit()
sys.exit()
