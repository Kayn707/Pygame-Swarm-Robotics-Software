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
HEXAGON_SIZE = 50
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
HOTPINK = (255, 105, 180)
dark_gray = (50, 50, 50)
script_dir = os.path.abspath(os.path.dirname(__file__))
bot_image_path = os.path.join(script_dir, "Assets", "BOT.png")
bot_image = pygame.image.load(bot_image_path)
covered = []
#Generate a random position for the Hexagon
hexagon_x = random.randint(0, WIDTH - HEXAGON_SIZE)
hexagon_y = random.randint(0, HEIGHT - HEXAGON_SIZE)


# Create a window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("S.R.D.S")

#========= Functions and Classes ============

def draw_hexagon(x, y, size):
    hexagon_points = []
    for i in range(6):
        angle = 2 * math.pi / 6 * i
        point_x = x + size * math.cos(angle)
        point_y = y + size * math.sin(angle)
        hexagon_points.append((point_x, point_y))
    pygame.draw.polygon(screen, BLUE, hexagon_points)

class Bot(object):
    num = 0 
    
    def __init__(self, num):
        self.num = num
        self.bot_x = WIDTH // 2
        self.bot_y = HEIGHT // 2
        
    def move(self):
        mv = random.randint(1, 4)
        self.bot_y = ((self.bot_y - (mv == 4) + (mv == 1)) * 1)
        self.bot_x = ((self.bot_x - (mv == 3) + (mv == 2)) * 1)
        if not((self.bot_x, self.bot_y) in covered):
            covered.append((self.bot_x, self.bot_y))
            screen.blit(bot_image, (self.bot_x, self.bot_y))
        else:
            self.move()


# Main game loop
running = True
bot1 = Bot(1)
bot2 = Bot(2)
bot3 = Bot(3)
bot4 = Bot(4)
bot5 = Bot(5)
bot6 = Bot(6)
time.sleep(0.1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    #Calls the Draw Hexgon Function to draw it
    draw_hexagon(hexagon_x, hexagon_y, HEXAGON_SIZE)

    #Paint covered ground

    for point in covered:
        pygame.draw.circle(screen, dark_gray, point, 5)
    
    #Call bot function
    time.sleep(0.0)
    bot1.move()
    bot2.move()
    bot3.move()
    bot4.move()
    bot5.move()
    bot6.move()

    # Update the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()


# pygame.draw.circle(screen, HOTPINK, (dot_x, dot_y), DOT_SIZE)
