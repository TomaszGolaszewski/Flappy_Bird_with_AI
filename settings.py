import pygame
import os

# window
WIN_WIDTH = 500
WIN_HEIGHT = 900
FRAMERATE = 30#30

# world
PIPES_OFFSET = 600 # X # offset between top and bottom pipe
PIPES_GAP = 200 # Y # offset between top and bottom pipe
BASE_LEVEL = 800
FALLING_INDICATOR = 10
BIRD_START_POINT = (230,300)

DRAW_LINES = True # whether to draw lines between birds and pipes or not (only in AI mode)

# physics
VEL_X = 5
VEL_Y_JUMP = 10.5
G = 3 # XD # falling acceleration
VEL_ROTATION = 15

# sprites
BIRD_IMGS = [
pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),
pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),
pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]

PIPE_IMGS = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
BASE_IMGS = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
BG_IMGS = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))

# initialize fonts
pygame.font.init()
# fonts
STAT_FONT = pygame.font.SysFont("comicsans", 50)
STAT_FONT_2 = pygame.font.SysFont("comicsans", 20)
DEATH_FONT = pygame.font.SysFont("timesnewroman", 50)
