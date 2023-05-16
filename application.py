import pygame
import sys
import copy

from graph import *
from settings import *
from player import *
from ghost import *
from graph import *

# Initialize game
pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        # Set up window
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # Set up Game dimensions and settings
        self.state = 'start'                # Controls game state: start, playing, game over
        self.cell_width = MAZE_WIDTH // COLS
        self.cell_height = MAZE_HEIGHT // ROWS

        # Wall locations
        self.walls = []

        # Coin Locations
        self.coins = []

        # Ghosts objects
        self.ghosts = []

        # Ghost positions
        self.g_pos = []

        # Player position
        self.p_pos = None

        # Load Game, Player, and Ghosts
        self.load()
        self.player = Player(self, vec(self.p_pos))
        self.high_score = 0
        self.make_ghosts()

    # Application is running--------------------------------------------------------------------------------------------
    def run(self):
        while self.running:
            if self.state == 'start':  # Start Page
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':  # Game Page
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == 'game over':  # Game over page
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    # Misc Functions----------------------------------------------------------------------------------------------------
    # Include text no screen--------------------------------------------------------------------------------------------
    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)

    # Load background, and find ghosts and player starting positions----------------------------------------------------
    def load(self):
        self.background = pygame.image.load('maze.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

        # Opening walls file
        # Creating walls list with co-ords of walls
        # stored as  a vector
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":  # Wall location
                        self.walls.append(vec(xidx, yidx))
                    elif char == "C":  # Coin location
                        self.coins.append(vec(xidx, yidx))
                    elif char == "P":  # Player location
                        self.p_pos = [xidx, yidx]
                    elif char in ["2", "3", "4", "5"]:  # Ghosts location
                        self.g_pos.append([xidx, yidx])
                    elif char == "B":  # Ghost Gate
                        pygame.draw.rect(self.background, WHITE, (xidx * self.cell_width, yidx * self.cell_height,
                                                                  self.cell_width, self.cell_height))

    # Create ghosts objects---------------------------------------------------------------------------------------------
    def make_ghosts(self):
        for idx, pos in enumerate(self.g_pos):
            self.ghosts.append(Ghost(self, vec(pos), idx))

    # Make outline of grid----------------------------------------------------------------------------------------------
    def draw_grid(self):
        for x in range(WIDTH // self.cell_width):
            pygame.draw.line(self.background, GREY, (x * self.cell_width, 0),
                             (x * self.cell_width, HEIGHT))
        for x in range(HEIGHT // self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x * self.cell_height),
                             (WIDTH, x * self.cell_height))

    # reset after game is over------------------------------------------------------------------------------------------
    def reset(self):
        self.player.lives = 3
        self.high_score = self.player.current_score
        self.player.current_score = 0
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0
        for ghost in self.ghosts:
            ghost.grid_pos = vec(ghost.starting_pos)
            ghost.pix_pos = ghost.get_pix_pos()
            ghost.direction *= 0

        self.coins = []
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(vec(xidx, yidx))
        self.state = "playing"

    # INTRODUCTIONS-----------------------------------------------------------------------------------------------------
    # Functions meant to represent aspects of the starting page

    # Begin game
    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    # Update game after begin
    def start_update(self):
        pass

    # Display intro page
    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('PUSH SPACE BAR', self.screen, [
            WIDTH // 2, HEIGHT // 2 - 50], START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)
        self.draw_text('1 PLAYER ONLY', self.screen, [
            WIDTH // 2, HEIGHT // 2 + 50], START_TEXT_SIZE, (44, 167, 198), START_FONT, centered=True)
        self.draw_text('HIGH SCORE', self.screen, [4, 0],
                       START_TEXT_SIZE, (255, 255, 255), START_FONT)
        pygame.display.update()

    # Active Game ------------------------------------------------------------------------------------------------------
    # Functions meant to represent aspects of the game page where all action is taken place

    # Player controls
    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))  # Left direction
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))  # Right direction
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))  # Up direction
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))  # Down direction

    # Update entity objects
    def playing_update(self):
        self.player.update()
        for ghost in self.ghosts:
            ghost.update()

        for ghost in self.ghosts:
            if ghost.grid_pos == self.player.grid_pos:
                self.remove_life()

        if self.player.current_score >= 287:
            self.state = "game over"

    # Display active plaing screen
    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER // 2, TOP_BOTTOM_BUFFER // 2))
        self.draw_coins()
        # self.draw_grid()                            # FIXME: Comment out when finished
        self.draw_text('CURRENT SCORE: {}'.format(self.player.current_score),
                       self.screen, [60, 0], 18, WHITE, START_FONT)
        self.draw_text('HIGH SCORE: {}'.format(self.high_score), self.screen, [WIDTH // 2 + 60, 0], 18, WHITE, START_FONT)
        self.player.draw()
        for ghost in self.ghosts:
            ghost.draw()
        pygame.display.update()

    # Remove life once ghost(s) hits player
    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = "game over"
        else:
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for ghost in self.ghosts:
                ghost.grid_pos = vec(ghost.starting_pos)
                ghost.pix_pos = ghost.get_pix_pos()
                ghost.direction *= 0

    # Draw coins on screen
    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (124, 123, 7),
                               (int(coin.x * self.cell_width) + self.cell_width // 2 + TOP_BOTTOM_BUFFER // 2,
                                int(coin.y * self.cell_height) + self.cell_height // 2 + TOP_BOTTOM_BUFFER // 2), 5)

    # Game over function------------------------------------------------------------------------------------------------
    # Functions meant to represent aspects of the game over page where the player has either died or won

    # Player wants to quit or play again
    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    # Update screen
    def game_over_update(self):
        pass

    # Display game screen
    def game_over_draw(self):
        self.screen.fill(BLACK)
        quit_text = "Press the escape button to QUIT"
        again_text = "Press SPACE bar to PLAY AGAIN"
        pygame.draw.rect(self.screen, WHITE, pygame.Rect((100, 160), (400, 100)))
        if self.player.current_score >= 287:
            self.draw_text("GAME OVER", self.screen, [WIDTH // 2, 100], 52, GREEN, "arial", centered=True)
            self.draw_text("YOU WON", self.screen, [WIDTH // 2, 210], 52, GREEN, "arial", centered=True)
        elif self.player.current_score < 287:
            self.draw_text("GAME OVER", self.screen, [WIDTH // 2, 100], 52, RED, "arial", centered=True)
            self.draw_text("YOU LOST", self.screen, [WIDTH // 2, 210], 52, RED, "arial", centered=True)
        self.draw_text(again_text, self.screen, [
            WIDTH // 2, HEIGHT // 2], 36, (190, 190, 190), "arial", centered=True)
        self.draw_text(quit_text, self.screen, [
            WIDTH // 2, HEIGHT // 1.5], 36, (190, 190, 190), "arial", centered=True)
        pygame.display.update()
