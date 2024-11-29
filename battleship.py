import pygame
import random
import sys
from settings import *
from ui.side_ui import *


class BattleshipGame:
    def __init__(self, game):

        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = WIDTH, HEIGHT
        self.GRID_SIZE = 9
        self.CELL_SIZE = TILESIZE
        self.GRID_ORIGIN = (0, 0)
        self.SHIP_TYPES = [4, 3, 2, 1]
        self.WIN_FONT = pygame.font.SysFont("Arial", 32)

        self.grid = [[0] * self.GRID_SIZE for _ in range(self.GRID_SIZE)]
        self.shots_left = 30
        self.start_time = pygame.time.get_ticks()
        self.clicked_cells = set()
        self.mine_hits = {}
        self.running = True
        self.win = False
        self.lose = False
        # self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.exit_button = get_exit_button()
        self.volume_button = get_volume_button(type="puzzle")
        if game.is_mute :
            self.volume_button.icon = self.volume_button.secondary_icon
            self.volume_button.image = self.volume_button.secondary_image
            self.volume_button.is_active = False
        self.music_button = get_music_button(type="puzzle")
        if game.is_music_mute :
            self.music_button.icon = self.music_button.secondary_icon
            self.music_button.image = self.music_button.secondary_image
            self.music_button.is_active = False
        self.end_exit_button = get_exit_button(type="end", maze=False)

        self.screen = game.screen
        self.game = game
        self.time_left = 0

        self.load_images()
        self.place_ships()
        self.place_mines()
        self.game.load_music(BATTLESHIP_MUSIC)

    def load_images(self):
        self.ship_image = pygame.transform.scale(
            pygame.image.load(SHIP_TILE), (self.CELL_SIZE, self.CELL_SIZE)
        )
        self.mine_image = pygame.transform.scale(
            pygame.image.load(MINE_TILE), (self.CELL_SIZE, self.CELL_SIZE)
        )
        self.hit_image = pygame.transform.scale(
            pygame.image.load(HIT_TILE), (self.CELL_SIZE, self.CELL_SIZE)
        )
        self.miss_image = pygame.transform.scale(
            pygame.image.load(MISS_TILE), (self.CELL_SIZE, self.CELL_SIZE)
        )
        self.default_tile_image = pygame.transform.scale(
            pygame.image.load(SEA_TILE), (self.CELL_SIZE, self.CELL_SIZE)
        )

    def place_ships(self):
        for ship_len in self.SHIP_TYPES:
            placed = False
            while not placed:
                x, y = random.randint(0, self.GRID_SIZE - 1), random.randint(
                    0, self.GRID_SIZE - 1
                )
                direction = random.choice(["H", "V"])
                valid = True
                cells = []
                if direction == "H" and x + ship_len <= self.GRID_SIZE:
                    cells = [(x + i, y) for i in range(ship_len)]
                elif direction == "V" and y + ship_len <= self.GRID_SIZE:
                    cells = [(x, y + i) for i in range(ship_len)]

                if cells:
                    for cx, cy in cells:
                        if self.grid[cy][cx] != 0 or any(
                            self.grid[ny][nx] != 0
                            for nx, ny in self.get_neighbors(cx, cy)
                        ):
                            valid = False
                            break
                    if valid:
                        for cx, cy in cells:
                            self.grid[cy][cx] = 2
                        placed = True

    def place_mines(self):
        for _ in range(2):
            placed = False
            while not placed:
                x, y = random.randint(0, self.GRID_SIZE - 2), random.randint(
                    0, self.GRID_SIZE - 1
                )
                if (
                    self.grid[y][x] == 0
                    and self.grid[y][x + 1] == 0
                    and all(
                        self.grid[ny][nx] == 0 for nx, ny in self.get_neighbors(x, y)
                    )
                    and all(
                        self.grid[ny][nx] == 0
                        for nx, ny in self.get_neighbors(x + 1, y)
                    )
                ):
                    self.grid[y][x], self.grid[y][x + 1] = 3, 3
                    placed = True

    def get_neighbors(self, x, y):
        neighbors = []
        for dx, dy in [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.GRID_SIZE and 0 <= ny < self.GRID_SIZE:
                neighbors.append((nx, ny))
        return neighbors

    def draw_grid(self):
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                rect = pygame.Rect(
                    self.GRID_ORIGIN[0] + col * self.CELL_SIZE,
                    self.GRID_ORIGIN[1] + row * self.CELL_SIZE,
                    self.CELL_SIZE,
                    self.CELL_SIZE,
                )
                if (row, col) not in self.clicked_cells:
                    self.screen.blit(self.default_tile_image, rect.topleft)
                else:
                    pygame.draw.rect(self.screen, (50, 50, 50), rect, 1)

    def draw_cells(self):
        for row, col in self.clicked_cells:
            rect = pygame.Rect(
                self.GRID_ORIGIN[0] + col * self.CELL_SIZE,
                self.GRID_ORIGIN[1] + row * self.CELL_SIZE,
                self.CELL_SIZE,
                self.CELL_SIZE,
            )
            if self.grid[row][col] == 1:
                self.screen.blit(self.hit_image, rect.topleft)
            elif self.grid[row][col] == -1:
                self.screen.blit(self.miss_image, rect.topleft)
            elif self.grid[row][col] == 3:
                self.screen.blit(self.mine_image, rect.topleft)

    def display_stats(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        time_left = max(0, 180 - elapsed_time)
        return time_left

    def check_win(self):
        return all(cell != 2 for row in self.grid for cell in row)

    def handle_click(self, x, y):
        col = (x - self.GRID_ORIGIN[0]) // self.CELL_SIZE
        row = (y - self.GRID_ORIGIN[1]) // self.CELL_SIZE
        if (
            0 <= col < self.GRID_SIZE
            and 0 <= row < self.GRID_SIZE
            and (row, col) not in self.clicked_cells
        ):
            self.clicked_cells.add((row, col))
            if self.grid[row][col] == 2:
                self.shots_left += 1
                self.grid[row][col] = 1
                self.game.play_sound("hit")
            elif self.grid[row][col] == 3:
                self.mine_hits[(row, col)] = True
                if len(self.mine_hits) == 4:
                    self.shots_left -= 3
                self.game.play_sound("mine")
            else:
                self.grid[row][col] = -1
                self.game.play_sound("miss")
            self.shots_left -= 1

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if self.exit_button.is_clicked(event) or self.exit_button.is_clicked(
                    event
                ):
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_click(*pygame.mouse.get_pos())
                if self.volume_button.is_clicked(event):
                    self.game.is_mute = not self.game.is_mute
                if self.music_button.is_clicked(event):
                    if self.game.is_music_mute:
                        pg.mixer.music.unpause()
                    else:
                        pg.mixer.music.pause()
                    self.game.is_music_mute = not self.game.is_music_mute

            time_left = self.display_stats()
            self.time_left = time_left
            if time_left == 0 or self.shots_left <= 0:
                self.lose = True
                self.running = False
            if self.check_win():
                self.win = True
                self.running = False

            self.screen.fill(EDGE_BLUE)
            self.draw_grid()
            self.draw_cells()

            draw_side_ui(self.game, type="battleship", puzzle=self)
            pygame.display.flip()

        self.end_screen()
        return self.win

    def end_screen(self):
        self.screen.fill(EDGE_BLUE)
        if self.win:
            draw_text(
                self,
                f"YOU WIN",
                (WIDTH // 2 + TILESIZE * 1 + 30, HEIGHT // 2),
                pg.font.Font(VOLKSWAGEN_BOLD_FONT_PATH, 50),
                color=GREEN,
            )
        else:
            draw_text(
                self,
                f"YOU LOSE",
                (WIDTH // 2+ TILESIZE * 1 + 30, HEIGHT // 2),
                pg.font.Font(VOLKSWAGEN_BOLD_FONT_PATH, 50),
                color=RED,
            )
        self.end_exit_button.draw(self.screen)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if self.end_exit_button.is_clicked(event) or self.end_exit_button.is_clicked(event):
                    return
