import pygame
import time
import os
import random

from settings import *
from classes_world import *


class Game:
    def __init__(self):
        # initialize the pygame
        pygame.init()

        # objects
        self.bird = Bird(*BIRD_START_POINT)
        self.base = Base(BASE_LEVEL)
        self.pipes = [Pipe(PIPES_OFFSET)]

        # set the display
        self.win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
        # title and icon
        pygame.display.set_caption("Flappy bird")
        icon = pygame.image.load(os.path.join("imgs","icon.png"))
        pygame.display.set_icon(icon)

        # set the clock
        self.clock = pygame.time.Clock()

        self.GAME_IS_ON = True

        self.today_score = 0 # the best score for today
        # the best score ever
        try:
            score_file = open(SCORE_PATH, "rt")
            self.the_best_score = int(score_file.read())
            self.score_from_file = True
            score_file.close()
        except:
            self.the_best_score = 9999
            self.score_from_file = False

    def run(self):
        # main method - runs the game

        self.score = 0 # score
        global TODAY_SCORE

        running = True
        while running:
            self.clock.tick(FRAMERATE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.GAME_IS_ON = False
    # manual control
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bird.jump()
    # close
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        running = False


            self.bird.move()

            # checking whether bird pass the pipe
            add_pipe = False
            pipes_to_remove = []
            for pipe in self.pipes:
                if pipe.collide(self.bird):
                    # bird dies because hit the pipe
                    running = False

                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    pipes_to_remove.append(pipe)

                if not pipe.passed and pipe.x < self.bird.x:
                    pipe.passed = True
                    add_pipe = True

                pipe.move()

            # add new pipe
            if add_pipe:
                self.pipes.append(Pipe(PIPES_OFFSET))

                # calculate score
                self.score += 1
                if self.score > self.today_score:
                    self.today_score = self.score
                if self.today_score > self.the_best_score:
                    self.the_best_score = self.today_score
                    if self.score_from_file:
                        try:
                            score_file = open(SCORE_PATH, "wt")
                            score_file.write(str(self.the_best_score))
                            score_file.close()
                        except:
                            pass

            # remove old pipe
            for r in pipes_to_remove:
                self.pipes.remove(r)

            if self.bird.y + self.bird.img.get_height() >= BASE_LEVEL:
                # bird dies because hit the ground
                running = False

            self.base.move()
            self.draw_window()

    def death_screen(self):
        # shows screen after death
        self.win.fill((0,0,0))
        text = DEATH_FONT.render("YOU DIED", 1, (255,0,0))
        self.win.blit(text, ((WIN_WIDTH - text.get_width())/2, (WIN_HEIGHT - text.get_height())/2))
        pygame.display.update()

        running = True
        while running:
            self.clock.tick(FRAMERATE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.GAME_IS_ON = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        running = False
                        self.GAME_IS_ON = False

        # resetting objects
        if self.GAME_IS_ON:
            (self.bird.x, self.bird.y) = BIRD_START_POINT
            self.pipes = [Pipe(PIPES_OFFSET)]

    def draw_window(self):
        # draw window

        global TODAY_SCORE # the best score for today

        # draw background
        self.win.blit(BG_IMGS, (0,0))

        # draw pipes
        for pipe in self.pipes:
            pipe.draw(self.win)

        # draw stats
        # score this game
        text = STAT_FONT.render("Score: " + str(self.score), 1, (255,255,255))
        self.win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
        # the best score today
        text = STAT_FONT_2.render("Today: " + str(self.today_score), 1, (255,255,255))
        self.win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10 + 60))
        # the best score ever
        text = STAT_FONT_2.render("The best: " + str(self.the_best_score), 1, (255,255,255))
        self.win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10 + 60 + text.get_height()))

        # draw base
        self.base.draw(self.win)
        # draw bird
        self.bird.draw(self.win)
        # flip the screen
        pygame.display.update()
