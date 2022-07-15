# 2022.06.22

# Classic "Flappy bird" game

import pygame
import time
import os
import random

from sys import path
path.append('.\\src')

from settings import *
from classes_world import *
from classes_game import *


if __name__ == "__main__":

    game = Game()
    while game.GAME_IS_ON:
        game.run()
        game.death_screen()

    pygame.quit()
    quit()
