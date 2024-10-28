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
mouse_x, mouse_y = pygame.mouse.get_pos()

# Global Varibles
Pregame = True
begin = True
bringBack = False

timer = 0
ticker = 0

direction = ""


#All Checks
allCheck = 0
allCheck2 = False
allCheck3 = False
Tag_expansion = True
Tag_network = False
Tag_return = False
Tag_Queenreturn = False

#Player Modifiers
playerMod_expand = 0
playerMod_movementX = 0
playerMod_movementY = 0

#Colors and Images
OFFWHITE = (200, 200, 200)
BLUE = (0, 0, 255)
HOTPINK = (255, 105, 180)
DARK_GRAY = (50, 50, 50)
SPRING_GREEN = (0,255,127)
# image initialization 
script_dir = os.path.abspath(os.path.dirname(__file__))

bot_image_path = os.path.join(script_dir, "Assets", "BOT.png")
bot_image = pygame.image.load(bot_image_path)

Queen_image_path = os.path.join(script_dir, "Assets", "QueenV3.png")
Queen_image = pygame.image.load(Queen_image_path)

# Arrays
covered = []

#Generate a random position for the Hexagon
hexagon_x = random.randint(0, WIDTH - HEXAGON_SIZE)
hexagon_y = random.randint(0, HEIGHT - HEXAGON_SIZE)

# Create a window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("S.R.D.S")

#========= Functions and Classes ============

def drawHexagon(x, y, size):
    '''
    draws the hexagon
    '''
    hexagon_points = []
    for i in range(6):
        angle = 2 * math.pi / 6 * i
        point_x = x + size * math.cos(angle)
        point_y = y + size * math.sin(angle)
        hexagon_points.append((point_x, point_y))
    pygame.draw.polygon(screen, BLUE, hexagon_points)

def checkSearchComplete(botx):
    '''
    MAJOR EVENT INSTATIATION
    When Called, Checks if Hexagon object has been found. If yes, searching phase ends. BringBack phase begins 
    '''
    global begin 
    global bringBack
    global covered  
    if botx.distanceToTarget(hexagon_x, hexagon_y) < 20:
                    for bott in bots:
                        bott.target_X = hexagon_x
                        bott.target_Y = hexagon_y
                    print("OBJECTIVE COMPLETE . . . TARGET AQUIRED")
                    print("NEW DIRECTIVE . . . DELIVER OBJECT")
                    print("")
                    botx.tag = True
                    print(botx.num, "MEMEME", botx.tag)
                    begin = False
                    bringBack = True
                    covered = []
                    return(True)
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

# === Global Robot Commands ===

def network():
    '''
    displays the network lines for the bots
    '''
    for index, bot in enumerate(bots):
        bota = bots[index - 1]
        botb = bots[index - 2]
        pygame.draw.line(screen, SPRING_GREEN, (bot.bot_x - 5, bot.bot_y - 5), (bota.bot_x - 5, bota.bot_y - 5)) 
        pygame.draw.line(screen, SPRING_GREEN, (bot.bot_x - 5, bot.bot_y - 5), (botb.bot_x - 5, botb.bot_y - 5))

def networkExpansion(): 
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

 
#Bot Class
class Bot(object):
    '''
    __Init__: Moves Randomly 
    distanceToTarget: returns the distance from the object
    getAway: Moves away from given coordinates
    moveToTarget: Moves towards current target, if close to Hexagon, doesn't move
    '''
    
    def __init__(self, num):
        self.num = num
        self.bot_x = (WIDTH // 2) + random.randint(-50, 50)
        self.bot_y = (HEIGHT // 2)  + random.randint(-50, 50)
        self.runmove = True
        self.target_X = WIDTH // 2
        self.target_Y = HEIGHT // 2
        self.tag = False
              
    def distanceToTarget(self, X, Y):
        distance = math.sqrt((self.bot_x - X)**2 + (self.bot_y - Y)**2)
        return(distance)
                 
    def moveToTarget(self):
        deltaX = (self.target_X - self.bot_x)
        deltaY = (self.target_Y - self.bot_y)
    
        if (deltaX) > 0:
            self.bot_x += 1
            self.bringHome("d")
            #print("RIGHT")
            screen.blit(bot_image, (self.bot_x - 5, self.bot_y - 5))
            #covered.append((self.bot_x, self.bot_y))
            
        elif (deltaX) < 0:
            self.bot_x += -1
            self.bringHome("a")
           # print("LEFT")
            screen.blit(bot_image, (self.bot_x - 5, self.bot_y - 5))
            #covered.append((self.bot_x, self.bot_y))
            
        elif deltaY == 0:
            screen.blit(bot_image, (self.bot_x - 5, self.bot_y - 5))
            return(None)

        if (deltaY) > 0:
            self.bot_y += 1
            self.bringHome("s")
           # print("DOWN")
            screen.blit(bot_image, (self.bot_x - 5, self.bot_y - 5))
            #covered.append((self.bot_x, self.bot_y))
            
            
        elif (deltaY) < 0:
            self.bot_y += -1
            self.bringHome("w")
           # print("UP")
            screen.blit(bot_image, (self.bot_x - 5, self.bot_y - 5))
            #covered.append((self.bot_x, self.bot_y))
            
        elif deltaX == 0:
            screen.blit(bot_image, (self.bot_x - 5, self.bot_y - 5))
            return(None)

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

    def bringHome(self, direction):
        global hexagon_x
        global hexagon_y
        if self.tag == True:
            if direction == "w":
                    hexagon_y -= 1
            if direction == "s":
                    hexagon_y += 1
            if direction == "a":
                    hexagon_x -= 1
            if direction == "d":
                    hexagon_x += 1
            checkDeliveryComplete(self)

#Queen Class
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
    
#Establishing Robots and Commands
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
bots = [bot1, bot2, bot3, bot4, bot5, bot6, bot7, bot8, bot9, bot10, bot11, bot12]

Queen = Queen()

#======== MAIN GAME ============
print("NEW DIRECTIVE . . . AQUIRE TARGET")
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
        
        #Calls the Draw Hexgon Function to draw it
        drawHexagon(hexagon_x, hexagon_y, HEXAGON_SIZE)
        
        #Covered Ground and Network Lines
        for point in covered:
            pygame.draw.circle(screen, DARK_GRAY, point, 1)
        
        # === PLAYER INPUT ===
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_q]:
            Tag_network = False
        if keys[pygame.K_e]:
            Tag_network = True
        if keys[pygame.K_UP]:
            playerMod_expand += 1
            Tag_expansion = False
        if keys[pygame.K_DOWN]:
            playerMod_expand -= 1
            Tag_expansion = True
            if playerMod_expand < 0:
                playerMod_expand = 0
        if keys[pygame.K_w]:
            direction = "w"
            playerMod_movementY -= 1
        if keys[pygame.K_s]:
            direction = "s"
            playerMod_movementY += 1
        if keys[pygame.K_d]:
            direction = "d"
            playerMod_movementX += 1
        if keys[pygame.K_a]:
            direction = "a"
            playerMod_movementX -= 1   
        Queen.PlayerMove() 
        # === Pre-Game ===

        # === SEARCHING PHASE ===
        if begin:
            if Tag_network == False:
                network()
            networkExpansion()
            covered = []
            for bot in bots:
                if checkSearchComplete(bot):
                    break
        
        # === BRING BACK TO CENTER PHASE ===
        if bringBack:
            if Tag_network == False:
                network()
            if not(allCheck == len(bots)):
                for bot in bots:
                    movementCheck(bot)
                    #print(bot.num, allCheck, bot.bot_x, bot.bot_y)
            if allCheck == len(bots):
                for bot in bots:
                    bot.target_X, bot.target_Y = WIDTH // 2, HEIGHT // 2
                    movementCheck(bot)
                allCheck = len(bots)
            else: 
                allCheck = 0

                
            covered = []

        # Update the screen
        pygame.display.update()

# Quit Pygame
pygame.quit()
sys.exit()
