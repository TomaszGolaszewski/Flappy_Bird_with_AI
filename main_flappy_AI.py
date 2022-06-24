# 2022.06.24

# Classic "Flappy bird" game with neural network control implemented

import pygame
import neat
import time
import os
import random

from settings import *
from classes_world import *
from classes_game import *
from classes_game_with_AI import *


def eval_genomes(genomes,config):
    # runs the simulation
    game = GameAI(genomes,config)
    game.run()

if __name__ == "__main__":

    # initialize the pygame
    pygame.init()

    # preparing config file
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # preparing population
    p = neat.Population(config)

    # preparing statistics reporter
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # start evaluation (max 50 generation)
    winner = p.run(eval_genomes,50)

    # to save the winner:
    # import pickle
    # outfile = open("winner.txt", "wb")
    # pickle.dump(winner, outfile)
    # outfile.close()

    pygame.quit()
    quit()
