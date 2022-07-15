import pygame
import neat
import time
import os
import random

from settings import *
from classes_world import *

GEN = 0 # generation number

class GameAI:

    def __init__(self, genomes, config):
        # objects
        self.nets = []
        self.ge = []
        self.birds = []

        for _, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config)
            self.nets.append(net)
            self.birds.append(Bird(*BIRD_START_POINT))
            g.fitness = 0
            self.ge.append(g)

        self.base = Base(BASE_LEVEL)
        self.pipes = [Pipe(PIPES_OFFSET)]

        # set the display
        self.win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
        # title and icon
        pygame.display.set_caption("Flappy bird with AI")
        icon = pygame.image.load(os.path.join("imgs","icon.png"))
        pygame.display.set_icon(icon)

        # set the clock
        self.clock = pygame.time.Clock()

        self.GAME_IS_ON = True

    def run(self):
        # main method - runs the simulation

        global GEN
        GEN += 1
        self.score = 0

        running = True
        while running:
            self.clock.tick(FRAMERATE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.GAME_IS_ON = False
                    pygame.quit()
                    quit()
                # manual close
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        running = False
                        self.GAME_IS_ON = False
                        pygame.quit()
                        quit()

            # checking which pipe the birds are seeing
            self.pipe_ind = 0
            if len(self.birds) > 0:
                if len(self.pipes) > 1 and self.birds[0].x > self.pipes[0].x + self.pipes[0].PIPE_TOP.get_width():
                    self.pipe_ind = 1
            else:
                running = False
                break

            for x, bird in enumerate(self.birds):
                bird.move()
                self.ge[x].fitness += 0.1 # cost function - +0.1 for surviving another frame - more is better

                # output = tanh(W1*bird_pos + W2*dist_bird&top_pipe + W3*dist_bird&bottom_pipe + bias)
                output = self.nets[x].activate((bird.y, abs(bird.y - self.pipes[self.pipe_ind].height), abs(bird.y - self.pipes[self.pipe_ind].bottom)))

                if output[0] > 0.5:
                    bird.jump()

            # checking whether bird pass the pipe
            add_pipe = False
            pipes_to_remove = []
            for pipe in self.pipes:
                for x, bird in enumerate(self.birds):
                    if pipe.collide(bird):
                        # bird dies because hit the pipe
                        self.ge[x].fitness -= 1
                        self.birds.pop(x)
                        self.nets.pop(x)
                        self.ge.pop(x)

                    if not pipe.passed and pipe.x < bird.x:
                        pipe.passed = True
                        add_pipe = True

                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    pipes_to_remove.append(pipe)

                pipe.move()

            # add new pipe
            if add_pipe:
                self.score += 1
                for g in self.ge:
                    g.fitness += 5 # cost function - +5 for surviving another pipe - more is better
                self.pipes.append(Pipe(PIPES_OFFSET))

            # remove old pipe
            for r in pipes_to_remove:
                self.pipes.remove(r)

            for x, bird in enumerate(self.birds):
                if bird.y + bird.img.get_height() >= BASE_LEVEL or bird.y < 0:
                    # bird dies because hit the ground (or the sky)
                    self.birds.pop(x)
                    self.nets.pop(x)
                    self.ge.pop(x)

            # to save the winner
            # if self.score > 20:
            #     break

            self.base.move()
            self.draw_window()

    def draw_window(self):
        # draw window
        # draw background
        self.win.blit(BG_IMGS, (0,0))

        # draw pipes
        for pipe in self.pipes:
            pipe.draw(self.win)

        # draw stats
        # score
        text = STAT_FONT.render("Score: " + str(self.score), 1, (255,255,255))
        self.win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
        # generations
        text = STAT_FONT.render("Gen: " + str(GEN), 1, (255,255,255))
        self.win.blit(text, (10, 10))
        # alive
        text = STAT_FONT.render("Alive: " + str(len(self.birds)), 1, (255,255,255))
        self.win.blit(text, (10, 10 + text.get_height()))

        # draw base
        self.base.draw(self.win)

        for bird in self.birds:
            # draw lines between bird and pipe
            if DRAW_LINES:
                try:
                    pygame.draw.line(self.win, (255,0,0), (bird.x + bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (self.pipes[self.pipe_ind].x + self.pipes[self.pipe_ind].PIPE_TOP.get_width()/2, self.pipes[self.pipe_ind].height), 5)
                    pygame.draw.line(self.win, (255,0,0), (bird.x + bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (self.pipes[self.pipe_ind].x + self.pipes[self.pipe_ind].PIPE_BOTTOM.get_width()/2, self.pipes[self.pipe_ind].bottom), 5)
                except:
                    pass
            # draw birds
            bird.draw(self.win)

        # flip the screen
        pygame.display.update()
