import pygame
from queue import PriorityQueue
from a_star import *
import random
import numpy as np

from settings import *
from player import *
from graph import *

vec = pygame.math.Vector2


class Ghost:
    def __init__(self, app, pos, number):
        self.app = app  # Application
        self.grid_pos = pos  # Grid position
        self.starting_pos = [pos.x, pos.y]  # Starting position
        self.pix_pos = self.get_pix_pos()  # Position on screen
        self.radius = int(self.app.cell_width // 2.3)  # Size of Ghosts
        self.number = number  # ghost index
        self.colour = self.set_colour()  # color of ghost
        self.direction = vec(0, 0)  # Direction
        self.personality = self.set_personality()  # Speed mode
        self.target = None  # Target tile
        self.speed = self.set_speed()  # Ghost speed

    # Update ghost object-----------------------------------------------------------------------------------------------
    def update(self):
        self.target = self.set_target()
        if self.target != self.grid_pos:
            self.pix_pos += self.direction * self.speed
            if self.time_to_move():
                self.move()

        # Setting grid position in reference to pix position
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER +
                            self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER +
                            self.app.cell_height // 2) // self.app.cell_height + 1

    # Place ghost on screen---------------------------------------------------------------------------------------------
    def draw(self):
        if self.number == 0:
            image = pygame.transform.scale(pygame.image.load(f'ghosts/chang.png'), (25, 25))
        if self.number == 1:
            image = pygame.transform.scale(pygame.image.load(f'ghosts/ginger.png'), (25, 25))
        if self.number == 2:
            image = pygame.transform.scale(pygame.image.load(f'ghosts/wong.png'), (25, 25))
        if self.number == 3:
            image = pygame.transform.scale(pygame.image.load(f'ghosts/yang.png'), (25, 25))

        self.app.screen.blit(image, (int(self.pix_pos.x - 10), int(self.pix_pos.y - 15)))
        # pygame.draw.circle(self.app.screen, self.colour,
        #                   (int(self.pix_pos.x), int(self.pix_pos.y)), self.radius)

    # Set color depending on ghost personality--------------------------------------------------------------------------
    def set_colour(self):
        if self.number == 0:
            return (43, 78, 203)
        if self.number == 1:
            return (197, 200, 27)
        if self.number == 2:
            return (189, 29, 29)
        if self.number == 3:
            return (215, 159, 33)

    # Set default speed personality-------------------------------------------------------------------------------------
    def set_personality(self):
        if self.number == 0:
            return "speedy"
        elif self.number == 1:
            return "slow"
        elif self.number == 2:
            return "random"
        else:
            return "scared"

    # Ghost speed mode--------------------------------------------------------------------------------------------------
    def set_speed(self):
        if self.personality in ["speedy", "scared"]:
            speed = 1
        else:
            speed = 1
        return speed

    # Ghost target tile-------------------------------------------------------------------------------------------------
    def set_target(self):
        if self.personality == "speedy" or self.personality == "slow":
            return self.app.player.grid_pos
        else:
            if self.app.player.grid_pos[0] > COLS // 2 and self.app.player.grid_pos[1] > ROWS // 2:
                return vec(1, 1)
            if self.app.player.grid_pos[0] > COLS // 2 and self.app.player.grid_pos[1] < ROWS // 2:
                return vec(1, ROWS - 2)
            if self.app.player.grid_pos[0] < COLS // 2 and self.app.player.grid_pos[1] > ROWS // 2:
                return vec(COLS - 2, 1)
            else:
                return vec(COLS - 2, ROWS - 2)

    # Move ghost according to speed mode-------------------------------------------------------------------------------
    def move(self):
        if self.personality == "random":
            self.direction = self.get_random_direction()
        if self.personality == "slow":
            self.direction = self.get_path_direction(self.target)
        if self.personality == "speedy":
            self.direction = self.get_path_direction(self.target)
        if self.personality == "scared":
            self.direction = self.get_path_direction(self.target)

    # Position on screen------------------------------------------------------------------------------------------------
    def get_pix_pos(self):
        return vec((self.grid_pos.x * self.app.cell_width) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2,
                   (self.grid_pos.y * self.app.cell_height) + TOP_BOTTOM_BUFFER // 2 +
                   self.app.cell_height // 2)

    # Ghost are able to move--------------------------------------------------------------------------------------------
    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    # A* Algorthm - helper functions------------------------------------------------------------------------------------

    # Get random position for random ghost movement
    def get_random_direction(self):
        while True:
            number = random.randint(-2, 1)
            if number == -2:
                x_dir, y_dir = 1, 0
            elif number == -1:
                x_dir, y_dir = 0, 1
            elif number == 0:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1
            next_pos = vec(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)
            if next_pos not in self.app.walls:
                break
        return vec(x_dir, y_dir)

    # Find path the ghost should take
    def get_path_direction(self, target):
        next_cell = self.find_next_cell_in_path(target)
        xdir = next_cell[0] - self.grid_pos[0]
        ydir = next_cell[1] - self.grid_pos[1]
        return vec(xdir, ydir)

    # Find the next tile the ghost should traverse
    def find_next_cell_in_path_med(self, target):
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1

        path = a_star_medium(grid, 1, [int(self.grid_pos.x), int(self.grid_pos.y)], [int(target[0]), int(target[1])])

    def find_next_cell_in_path(self, target):
        path = a_star(self, [int(self.grid_pos.x), int(self.grid_pos.y)], [
            int(target[0]), int(target[1])])
        return path[1]

