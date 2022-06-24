import pygame
import neat
import time
import os
import random

from settings import *

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = VEL_ROTATION 
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x              # + right
        self.y = y              # + down
        self.tilt = 0           # + ccw
        self.tick_count = 0     # frames from last jump
        self.vel = 0
        self.height = self.y    # last Y position before jump
        self.img_count = 0      # frames from last animation cycle
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = - VEL_Y_JUMP
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        # d = vt + 0.5at^2
        d = self.vel*self.tick_count + 0.5*G*self.tick_count**2

        if d >= 16:
            d = 16
        if d < 0:
            d -= 2

        self.y = self.y + d

        # tilt when falling
        if d < 0 or self.y < self.height + FALLING_INDICATOR:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        # bird animation
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # stopping animation when falling
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP = PIPES_GAP
    VEL = VEL_X

    def __init__(self, x):
        self.x = x
        self.height = 0
        # self.gap = 100

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMGS, False, True)
        self.PIPE_BOTTOM = PIPE_IMGS

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        t_point = bird_mask.overlap(top_mask, top_offset)
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)

        if t_point or b_point:
            return True
        return False

class Base:
    VEL = VEL_X
    WIDTH = BASE_IMGS.get_width()
    IMG = BASE_IMGS

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
