import pygame
from settings import *

vec = pygame.math.Vector2


class Player:
    def __init__(self, app, pos):
        self.app = app  # Application
        self.starting_pos = [pos.x, pos.y]  # Starting position
        self.grid_pos = pos  # Position on maze
        self.pix_pos = self.get_pix_pos()  # Position on screen
        self.direction = vec(1, 0)  # Left, right, up, down
        self.stored_direction = None  # Current direction
        self.able_to_move = True  # If alive and not facing a wall
        self.current_score = 0
        self.speed = 2
        self.lives = 1

        # Update player position--------------------------------------------------------------------------------------------

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction * self.speed
        if self.time_to_move():  # Time to move
            if self.stored_direction != None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()  # Possible to move
        # Setting grid position in reference to pix pos
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER +
                            self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER +
                            self.app.cell_height // 2) // self.app.cell_height + 1
        if self.on_coin():  # Eating coins
            self.eat_coin()  # Add points

    # Move player in direction given------------------------------------------------------------------------------------
    def move(self, direction):
        self.stored_direction = direction

    # Find where player is on screen------------------------------------------------------------------------------------
    def get_pix_pos(self):
        return vec((self.grid_pos[0] * self.app.cell_width) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2,
                   (self.grid_pos[1] * self.app.cell_height) +
                   TOP_BOTTOM_BUFFER // 2 + self.app.cell_height // 2)

        # FIXME: print(self.grid_pos, self.pix_pos)

    # Player is able to control pacman----------------------------------------------------------------------------------
    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True

    # Pacman is running into a wall-------------------------------------------------------------------------------------
    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos + self.direction) == wall:
                return False
        return True

    # Add Pacman to screen----------------------------------------------------------------------------------------------
    def draw(self):
        pygame.draw.circle(self.app.screen, PLAYER_COLOUR, (int(self.pix_pos.x),
                                                            int(self.pix_pos.y)), self.app.cell_width // 2 - 2)

        # Drawing player lives
        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, PLAYER_COLOUR, (30 + 20 * x, HEIGHT - 15), 7)

    # Allocate points---------------------------------------------------------------------------------------------------
    def on_coin(self):
        if self.grid_pos in self.app.coins:
            if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    def eat_coin(self):
        self.app.coins.remove(self.grid_pos)
        self.current_score += 1
