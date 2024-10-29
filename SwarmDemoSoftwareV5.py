import pygame
import sys
import math
import random
import time
import ast
import numpy as n
import os

# ======== Initializton =============
pygame.init()
# C:\Users\kadeh\Documents\Coding\"Python Coding"\"Swarm Robotics Software"

#Constants
WIDTH, HEIGHT = 720, 800
GrandHouseX, GrandHouseY = WIDTH // 2, HEIGHT // 2

# Global Varibles
Pregame = False
begin = True
Runtime = True
Global_Instructions = [1, (GrandHouseX, GrandHouseY), 200, 0, 0, 0]
InstructionPassed = False
new_instruct = True

timer = 0 #Currently unused

numOfRoofs = 0
numOfFrames = 0
numOfWindows = 0

#All Checks
allCheck = 0 #Used for Old Code
Tag_expansion = False #Used for Network Expasion
Tag_network = False #Network Tag
Tag_searchsort = True
Tag_PlayerInput = False
clickRegistered = False
clickRegistered2 = False

#Player Modifiers
#playerMod_expand = 0
playerMod_movementX = 0
playerMod_movementY = 0

#Colors
OFFWHITE = (200, 200, 200)
BLUE = (0, 0, 255)
HOTPINK = (255, 105, 180)
DARK_GRAY = (50, 50, 50)
SPRING_GREEN = (0,255,127)
BROWN = (139, 69, 19)


script_dir = os.path.abspath(os.path.dirname(__file__))

bot_image = pygame.image.load((os.path.join(script_dir, "Assets", "BOT2.png")))
Closed_Truck_Image = pygame.image.load(os.path.join(script_dir, "Assets", "Truck_closed.png"))
Frame_image = pygame.image.load(os.path.join(script_dir, "Assets", "FramePart.png"))
Button_image = pygame.image.load(os.path.join(script_dir, "Assets", "Button.png"))

# Arrays
#covered = []
ObjectParts = []
plotPoints = []
trucks = []
#roofs = []
frames = []
#windows = []


# Create a window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("S.R.D.S")

#========= Functions and Classes ============

def createFrame(num):
    global numOfFrames
    numOfFrames += 1
    framePart = Frame(num)
    frames.append(framePart)
    ObjectParts.append(framePart)

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

def Buttons():
    global Global_Instructions
    global clickRegistered
    global new_instruct
    
    button1 = pygame.Rect(WIDTH - 60, HEIGHT - 40, 25, 25)
    screen.blit(Button_image, (WIDTH - 60, HEIGHT - 40))
        
    button2 = pygame.Rect(WIDTH - 120, HEIGHT - 40, 25, 25)
    screen.blit(Button_image, (WIDTH - 120, HEIGHT - 40))
        
    button3 = pygame.Rect(WIDTH - 180, HEIGHT - 40, 25, 25)
    screen.blit(Button_image, (WIDTH - 180, HEIGHT - 40))
        
    button4 = pygame.Rect(WIDTH - 240, HEIGHT - 40, 25, 25)
    screen.blit(Button_image, (WIDTH - 240, HEIGHT - 40))

    button5 = pygame.Rect(WIDTH - 300, HEIGHT - 40, 25, 25)
    screen.blit(Button_image, (WIDTH - 300, HEIGHT - 40))
    
    if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) and not(clickRegistered):
        clickRegistered = True
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if button1.collidepoint(mouse_x, mouse_y):
            Global_Instructions[0] = 1
            new_instruct = True

        elif button2.collidepoint(mouse_x, mouse_y):
            Global_Instructions[0] = 2
            new_instruct = True

        elif button3.collidepoint(mouse_x, mouse_y):
            Global_Instructions[0] = 3
            new_instruct = True
    
        elif button4.collidepoint(mouse_x, mouse_y):
            Global_Instructions[0] = 4
            new_instruct = True
        
        elif button5.collidepoint(mouse_x, mouse_y):
            Global_Instructions[0] = 5
            new_instruct = True
    
    elif (event.type == pygame.MOUSEBUTTONUP and event.button == 1):
        clickRegistered = False
    
# === Global Robot Commands (GLOBAL COMPUTER) ===
def GenerateInstructions(): #Processes complex instructions to generate simple instructions
    global Global_Instructions
    global new_instruct

    # CURRENT INSTRUCTION FORMAT
    # 0: Current Operation
    # 1: Target Point
    # 2: Expansion Distance
    # 3: List of Objects
    # 4: List of Plots to Build
    # 5: What to Build

    # Player Click Loop 
    Buttons()

    #Distribute the current intructions
    if new_instruct == True:
        Global_Instructions[3] = ObjectParts
        Global_Instructions[4] = (WIDTH // 2, HEIGHT // 2)
        Global_Instructions[5] = "box"
        for bot in bots:
            
            bot.setInstructions(Global_Instructions)
        new_instruct = False
           
    #Meta Loop: Each Bot Processes current instructions       
    for bot in bots:
        bot.ProcessInstructions()
        #User_input = ast.literal_eval(input()
        #Adds Relevent Arrays before dsitribution 
        
# === Classes ===

class Frame(object):
    def __init__(self, num):
        self.num = num
        self.X = truckFrame.X + 7 * (self.num + 1)
        self.Y = truckFrame.Y + 7
        self.delivered = False
        self.taken = False
        self.bot_control = ''
        self.targetLock = False #Checks to see if this object has been designated for a position
        self.partType = "Frame"
        self.image = Frame_image
        self.rect = pygame.Rect((self.X), (self.Y), 10, 100)

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
    
    object_positions = []

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
        self.rules = ''
              
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

    def getAway(self, botx, boty, playerMod_expand):
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
        self.target_X, self.target_Y = ((WIDTH // len(bots)) * self.num) - 25, 40
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
        object.X, object.Y = self.bot_x, self.bot_y #Moving Object

        if object.targetLock == False:
            self.target_X, self.target_Y =  self.build(self.rules[4]) #Instead of Sorting, this builds the designated object based on what is specified 
            object.targetLock = True
        
        if self.moveToTarget() == True: # Resets Process
            self.target_object.delivered = True
            self.target_object = ''
            self.flag_getobject = True
            self.flag_deliverobject = False
        
    def determineObject(self):
        for object in self.rules[3]: #Currently References Position 3 in instructions (object parts)
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

    def ProcessInstructions(self): #Processes Global Intructions  
        instructiones = self.rules
        # Instructions are based on an array system
        # [1 - 10]
        # Defines what the global goal is
        
        if instructiones[0] == 1: #Go To Home
            self.goHome()
        if instructiones[0] == 2: # Move to given Coordinate 
            self.target_X, self.target_Y = self.rules[1]
            self.moveToTarget()
        if instructiones[0] == 3: # Bots Move Away From Each Other a given distance
            self.networkExpansion(instructiones[2])
        if instructiones[0] == 4: # Bots search for an object in object list and sort it
            self.searchAndSort()
        if instructiones[0] == 5:
            self.searchAndSort()

    def setInstructions(self, instructions):
        self.rules = instructions #Only place self.rules can be changed
        if self.rules[0] == 1:
                #print("break1")
                None
        elif self.rules[0] == 2:
                #print("break2")
                self.target_X, self.target_Y = self.rules[1]
        elif self.rules[0] == 3:
                #print("break3")
                self.bot_x += random.randint(-5, 5)
                self.bot_y += random.randint(-5, 5)
        elif self.rules[0] == 4:
            for object in self.rules[3]:
                object.delivered = False
                object.taken = False
                object.bot_control = ''
                object.targetLock = False
                #print("break4")
            self.target_object = ''
        elif self.rules[0] == 5:
            #print("break5")
            self.reset()
                
    def networkExpansion(self, playerMod_expand):
        bota = self.findNearestBot(False, '')
        botb = self.findNearestBot(True, bota)
        if Tag_expansion:
            self.getAway(bota.bot_x, bota.bot_y, playerMod_expand)
        elif not(Tag_expansion):
            self.getAway(bota.bot_x, bota.bot_y, playerMod_expand)
            self.getAway(botb.bot_x, botb.bot_y, playerMod_expand) 
        screen.blit(bot_image, (self.bot_x - 5, self.bot_y - 5))

    def findNearestBot(self, ignorebot, ignorebotwhich):
        checknum = ''
        checkX, checkY = WIDTH, HEIGHT #bots[self.num - 1].bot_x, bots[self.num - 1].bot_y
        bote = self
        if ignorebot == True:
            for bot in bots:
                if not(bot.num == self.num) and not(bot.num == ignorebotwhich.num):
                    if self.distanceToTarget(bot.bot_x, bot.bot_y) < self.distanceToTarget(checkX, checkY):
                        checkX, checkY = bot.bot_x, bot.bot_y
                        bote = bot
            pygame.draw.line(screen, SPRING_GREEN, (self.bot_x, self.bot_y), (checkX, checkY)) 
            return(bote)
        else:
            for bot in bots:
                if not(bot.num == self.num):
                    if self.distanceToTarget(bot.bot_x, bot.bot_y) < self.distanceToTarget(checkX, checkY):
                        checkX, checkY = bot.bot_x, bot.bot_y
                        bote = bot
            pygame.draw.line(screen, SPRING_GREEN, (self.bot_x, self.bot_y), (checkX, checkY)) 
            return(bote)

    def manipulate_obj(self, degree):
        object = self.target_object
        if object == '':
            return False
        elif object.bot_control == self.num and object.delivered == False and self.flag_deliverobject == True:
            object.image = pygame.transform.rotate(Frame_image, degree)
            
    def build(self, plot):
        if self.rules[5] == "box":
            if plot not in Bot.object_positions: #Left Wall
                Bot.object_positions.append(plot)
                return(plot)
            elif (plot[0] + 10, plot[1] + 100) not in Bot.object_positions: #Floor
                Bot.object_positions.append((plot[0] + 10, plot[1] + 100))
                self.manipulate_obj(90)
                return((plot[0] + 10, plot[1] + 100))
            elif (plot[0] + 10, plot[1] - 10) not in Bot.object_positions: #Ceiling
                Bot.object_positions.append((plot[0] + 10, plot[1] - 10))
                self.manipulate_obj(90)
                return((plot[0] + 10, plot[1] - 10))
            elif (plot[0] + 110, plot[1]) not in Bot.object_positions: #Right Wall
                Bot.object_positions.append((plot[0] + 110, plot[1]))
                return((plot[0] + 110, plot[1]))
            elif (plot[0] + 5, plot[1] - 5) not in Bot.object_positions: #Diagonal 
                Bot.object_positions.append((plot[0] + 5, plot[1] - 5))
                self.manipulate_obj(45)
                return((plot[0] + 5, plot[1] - 5))
            elif (plot[0] + 37, plot[1] + 27) not in Bot.object_positions: #Diagonal 
                Bot.object_positions.append((plot[0] + 37, plot[1] + 27))
                self.manipulate_obj(45)
                return((plot[0] + 37, plot[1] + 27))
            else:
                return(truckFrame.X, truckFrame.Y)
        
        if self.rules[5] == "reset":
            self.manipulate_obj(0)
            Bot.object_positions = []
            return(truckFrame.X + 7 * (self.num + 1), truckFrame.Y + 7)
        
            
    def reset(self):
        for object in self.rules[3]:
            object.delivered = False
            object.taken = False
            object.bot_control = ''
            object.targetLock = False

        self.rules[5] = "reset"



    
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

truckFrame = Truck(2, Closed_Truck_Image, 30, (HEIGHT // 2))
trucks = [truckFrame]
                    
#======== MAIN GAME ============
print("NEW DIRECTIVE . . . WAITING FOR INSTRUCTIONS")
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

        # === PLAYER INPUT ===
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            Tag_network = False
        if keys[pygame.K_e]:
            Tag_network = True

        # === Begin ===
        if begin: #Creates all the needed Parts for the simulation 
            for i in range(10):
                createFrame(i)
            begin = False
    
        # === Runtime ===
        if Runtime: #Distributes simple instructions to robots to begin decoding and following
            for truck in trucks:
                screen.blit(truck.image, (truck.X, truck.Y))    
            for part in ObjectParts:
                part.showSelf()
            GenerateInstructions()

        # Update the screen
        pygame.display.update()

# Quit Pygame
pygame.quit()
sys.exit()
