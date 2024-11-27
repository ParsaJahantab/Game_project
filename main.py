import pygame as pg
import sys
from os import path
from settings import *
from sprites.wall import *
from sprites.interactive_tile import *
from sprites.player import *
from sprites.teleporter import *
from sprites.fog import *
from ui.button import *
import random
import importlib
import ast


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.walk_sound = pg.mixer.Sound(WALK_SOUND)
        self.teleport_sound = pg.mixer.Sound(TELEPORT_SOUND)
        self.win_sound = pg.mixer.Sound(WIN_SOUND)
        self.solve_puzzle_sound = pg.mixer.Sound(SOULVE_PUZZLE_SOUND)
        self.fail_puzzle_sound = pg.mixer.Sound(FAIL_PUZZLE_SOUND)
        self.error_sound = pg.mixer.Sound(ERROR_SOUND)
        pg.mixer.music.load(MAZE_MUSIC)
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1)
        self.exit_button = ImageButton(
            (TILESIZE * 9) + 15,
            TILESIZE * 8,
            RED_BUTTON,
            "Exit Game",
            VOLKSWAGEN_BOLD_FONT_PATH,
            16,
            text_color=(0, 0, 0),
            hover_text_color=(255, 255, 255),
        )
        self.reset_button = ImageButton(
            (TILESIZE * 9) + 15,
            TILESIZE * 7,
            BLUE_BUTTON,
            "Rest Game",
            VOLKSWAGEN_BOLD_FONT_PATH,
            16,
            text_color=(0, 0, 0),
            hover_text_color=(255, 255, 255),
        )
        self.volume_button = ImageButton(
            (TILESIZE * 9) + 15,
            TILESIZE * 6,
            GREEN_BUTTON,
            "",
            VOLKSWAGEN_BOLD_FONT_PATH,
            16,
            text_color=(0, 0, 0),
            hover_text_color=(255, 255, 255),
            icon_path=VOLUME_ICON,
            secondary_image_path=GRAY_BUTTON,
            secondary_icon_path=MUTE_ICON,
            scale=(80, 48),
        )
        self.music_button = ImageButton(
            (TILESIZE * 9) + 120,
            TILESIZE * 6,
            GREEN_BUTTON,
            "",
            VOLKSWAGEN_BOLD_FONT_PATH,
            16,
            text_color=(0, 0, 0),
            hover_text_color=(255, 255, 255),
            icon_path=MUSIC_ICON,
            secondary_image_path=GRAY_BUTTON,
            secondary_icon_path=SLASH_ICON,
            scale=(80, 48),
        )
        self.end_exit_button = ImageButton(
            (TILESIZE * 4) - 10,
            TILESIZE * 8,
            RED_BUTTON,
            "Exit Game",
            VOLKSWAGEN_BOLD_FONT_PATH,
            16,
            text_color=(0, 0, 0),
            hover_text_color=(255, 255, 255),
            scale=(300, 60),
        )
        self.end_reset_button = ImageButton(
            (TILESIZE * 4) - 10,
            TILESIZE * 7,
            BLUE_BUTTON,
            "Rest Game",
            VOLKSWAGEN_BOLD_FONT_PATH,
            16,
            text_color=(0, 0, 0),
            hover_text_color=(255, 255, 255),
            scale=(300, 60),
        )
        self.logo_image = self.add_logo((300, 200))
        self.end_logo_image = self.add_logo((600, 400))
        self.score = 2000
        self.solved_puzzles = 0
        self.playing = False
        self.is_mute = False
        self.is_music_mute = False
        self.bonus_score = 0
        self.loaded_functions = self.load_functions_from_module(
            "puzzles_functions", self.get_top_level_functions("puzzles_functions.py")
        )
        self.is_pause = False

    def draw_text(self, text, pos, font, color=WHITE):
        surf = font.render(text, True, color)
        rect = surf.get_rect(topright=(pos[0], pos[1]))
        self.screen.blit(surf, rect)

    def load_functions_from_module(self, module_name, function_names):

        module = importlib.import_module(module_name)
        return [getattr(module, func) for func in function_names]

    def get_top_level_functions(self, file_path):

        with open(file_path, "r") as f:
            file_content = f.read()

        tree = ast.parse(file_content)
        all_functions = set()
        called_functions = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                all_functions.add(node.name)
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                called_functions.add(node.func.id)

        top_level_functions = all_functions - called_functions
        return list(top_level_functions)

    def add_logo(self, size):
        image_path = LOGO
        original_image = pg.image.load(image_path).convert_alpha()
        resized_image = pg.transform.scale(original_image, (size[0], size[1]))
        return resized_image

    def end_game(self):
        if self.player.total_number_of_moves < 15:
            bonus = 150
        elif self.player.total_number_of_moves < 25:
            bonus = 100
        elif self.player.total_number_of_moves < 30:
            bonus = 50
        else:
            bonus = 0
        self.handel_score(2000 + bonus)
        self.play_sound("win")
        self.playing = False

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.lines = pg.sprite.Group()
        self.interactive_walls = pg.sprite.Group()
        self.tiles = pg.sprite.Group()
        self.teleporter = pg.sprite.Group()
        self.fog_sprite = pg.sprite.Group()
        self.player_sprite = pg.sprite.Group()
        self.score = 2000
        self.bonus_score = 0
        self.solved_puzzles = 0
        self.playing = True
        self.is_pause = False
        pg.mixer.music.rewind()
        self.loaded_functions = self.load_functions_from_module(
            "puzzles_functions", self.get_top_level_functions("puzzles_functions.py")
        )
        for x in range(9):
            for y in range(9):
                InteractiveTile(self, x, y, TILESIZE, TILESIZE, GREEN)

        Wall(self, (0, 0), (0, 4), WHITE, "vertical", (-1, 0))
        Wall(self, (0, 5), (0, 9), WHITE, "vertical", (-1, 0))
        Wall(self, (1, 1), (1, 4), WHITE, "vertical", (0, 1))
        Wall(self, (1, 5), (1, 8), WHITE, "vertical", (0, 1))
        Wall(self, (2, 2), (2, 7), WHITE, "vertical", (1, 2))
        Wall(self, (3, 3), (3, 6), WHITE, "vertical", (2, 3))
        Wall(self, (3, 0), (3, 1), WHITE, "vertical", (2, 3))
        Wall(self, (4, 0), (4, 1), WHITE, "vertical", (3, 4))
        Wall(self, (4, 2), (4, 3), WHITE, "vertical", (3, 4))
        Wall(self, (4, 4), (4, 5), WHITE, "vertical", (3, 4))
        Wall(self, (5, 1), (5, 2), WHITE, "vertical", (4, 5))
        Wall(self, (5, 4), (5, 5), WHITE, "vertical", (4, 5))
        Wall(self, (5, 6), (5, 7), WHITE, "vertical", (4, 5))
        Wall(self, (6, 0), (6, 3), WHITE, "vertical", (5, 6))
        Wall(self, (7, 0), (7, 1), WHITE, "vertical", (6, 7))
        Wall(self, (7, 2), (7, 3), WHITE, "vertical", (6, 7))
        Wall(self, (7, 5), (7, 8), WHITE, "vertical", (6, 7))
        Wall(self, (8, 5), (8, 6), WHITE, "vertical", (7, 8))
        Wall(self, (9, 0), (9, 4), WHITE, "vertical", (8, 9))
        Wall(self, (9, 5), (9, 9), WHITE, "vertical", (8, 9))

        Wall(self, (0, 0), (6, 0), WHITE, "horizontal", (-1, 0))
        Wall(self, (7, 0), (9, 0), WHITE, "horizontal", (-1, 0))
        Wall(self, (1, 1), (3, 1), WHITE, "horizontal", (0, 1))
        Wall(self, (4, 1), (5, 1), WHITE, "horizontal", (0, 1))
        Wall(self, (7, 1), (8, 1), WHITE, "horizontal", (0, 1))
        Wall(self, (2, 2), (4, 2), WHITE, "horizontal", (1, 2))
        Wall(self, (5, 2), (6, 2), WHITE, "horizontal", (1, 2))
        Wall(self, (7, 2), (9, 2), WHITE, "horizontal", (1, 2))
        Wall(self, (7, 2), (9, 2), WHITE, "horizontal", (1, 2))
        Wall(self, (0, 3), (1, 3), WHITE, "horizontal", (2, 3))
        Wall(self, (3, 3), (4, 3), WHITE, "horizontal", (2, 3))
        Wall(self, (5, 3), (6, 3), WHITE, "horizontal", (2, 3))
        Wall(self, (4, 4), (5, 4), WHITE, "horizontal", (3, 4))
        Wall(self, (6, 4), (9, 4), WHITE, "horizontal", (3, 4))
        Wall(self, (4, 5), (5, 5), WHITE, "horizontal", (4, 5))
        Wall(self, (6, 5), (7, 5), WHITE, "horizontal", (4, 5))
        Wall(self, (8, 5), (9, 5), WHITE, "horizontal", (4, 5))
        Wall(self, (3, 6), (6, 6), WHITE, "horizontal", (5, 6))
        Wall(self, (7, 6), (8, 6), WHITE, "horizontal", (5, 6))
        Wall(self, (1, 7), (4, 7), WHITE, "horizontal", (6, 7))
        Wall(self, (6, 7), (7, 7), WHITE, "horizontal", (6, 7))
        Wall(self, (1, 8), (2, 8), WHITE, "horizontal", (7, 8))
        Wall(self, (3, 8), (7, 8), WHITE, "horizontal", (7, 8))
        Wall(self, (0, 9), (1, 9), WHITE, "horizontal", (8, 8))
        Wall(self, (2, 9), (9, 9), WHITE, "horizontal", (8, 8))

        Wall(self, (3, 1), (4, 1), PINK, "horizontal", (0, 1), type="interactive", id=0) # portal 
        Wall(self, (1, 3), (2, 3), PINK, "horizontal", (2, 3), type="interactive", id=1)
        Wall(self, (6, 3), (7, 3), PINK, "horizontal", (2, 3), type="interactive", id=2)
        Wall(self, (3, 4), (4, 4), PINK, "horizontal", (3, 4), type="interactive", id=3)
        Wall(self, (2, 8), (3, 8), PINK, "horizontal", (7, 8), type="interactive", id=4)

        Wall(self, (5, 3), (5, 4), PINK, "vertical", (4, 5), type="interactive", id=5)
        Wall(self, (4, 5), (4, 6), PINK, "vertical", (3, 4), type="interactive", id=6)
        Wall(self, (2, 8), (2, 9), PINK, "vertical", (1, 2), type="interactive", id=7)
        Fog(self, 5, 4, os.path.join("assets/fog"))
        self.player = Player(self, 0, 4)
        self.player.total_number_of_moves = 0

        self.tiles = pg.sprite.Group()
        for x in range(9):
            for y in range(9):
                InteractiveTile(self, x, y, TILESIZE, TILESIZE, GREEN)

        Portal(self, 3, 0, TILESIZE // 2, TILESIZE // 2, 1)
        Portal(self, 6, 5, TILESIZE // 2, TILESIZE // 2, 2)

    def play_puzzle(self, sprite:Wall):
        self.pause_game()
        sprite.id
        if not self.loaded_functions:
            sprite.kill()
            self.unpause_game()
            self.solved_puzzles += 1
            return
        if sprite.id >=  len(self.loaded_functions):
            sprite.kill()
            self.unpause_game()
            self.solved_puzzles += 1
            return
        else:
            puzzle = self.loaded_functions[sprite.id]
            if puzzle():
                sprite.kill()
                self.unpause_game()
                self.handel_score(60)
                self.play_sound("solve")
                self.solved_puzzles += 1
            else: 
                self.unpause_game()
                self.handel_score(-10)
                self.play_sound("fail")
                
            
        # random_puzzle = random.choice(self.loaded_functions)
        # if random_puzzle():
        #     sprite.kill()
        #     self.loaded_functions.remove(random_puzzle)
        #     self.unpause_game()
        #     self.handel_score(60)
        #     self.play_sound("solve")
        #     self.solved_puzzles += 1
        # else:
        #     self.unpause_game()
        #     self.handel_score(-10)
        #     self.play_sound("fail")

    def pause_game(self):
        self.is_pause = True
        pg.mixer.music.pause()

    def unpause_game(self):
        self.is_pause = False
        if not self.is_music_mute:
            pg.mixer.music.unpause()

    def run(self):
        while self.playing:
            if not self.is_pause:
                self.dt = self.clock.tick(FPS) / 1000
                self.events()
                self.update()
                self.draw()
        while not self.playing:
            self.draw_end()
            self.events()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()

    def reset(self):
        for sprite in self.all_sprites:
            sprite.kill()

        self.new()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, WHITE, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, WHITE, (0, y), (WIDTH, y))

    def draw_player(self):
        player_image_copy = self.player.image.copy()
        player_image_copy = pg.transform.scale(player_image_copy, (150, 150))
        self.screen.blit(player_image_copy, ((TILESIZE * 9) + 35, (TILESIZE * 3)))

    def handel_score(self, score_change):
        self.bonus_score = max(((self.score + score_change) - 2000), 0)
        self.score = min(2000, self.score + score_change)

    def play_sound(self, sound_to_play):
        if not self.is_mute:
            if sound_to_play == "walk" and not self.player.is_player_in_fog:
                self.walk_sound.play()
            elif sound_to_play == "error" and not self.player.is_player_in_fog:
                self.error_sound.play()
            elif sound_to_play == "teleport":
                self.teleport_sound.play()
            elif sound_to_play == "win":
                self.win_sound.play()
            elif sound_to_play == "solve":
                self.solve_puzzle_sound.play()
            elif sound_to_play == "fail":
                self.fail_puzzle_sound.play()

    def draw(self):
        self.screen.fill(BGCOLOR)
        # self.draw_grid()
        self.tiles.draw(self.screen)
        self.walls.draw(self.screen)
        self.interactive_walls.draw(self.screen)
        self.teleporter.draw(self.screen)
        self.player_sprite.draw(self.screen)
        self.fog_sprite.draw(self.screen)
        self.exit_button.draw(self.screen)
        self.reset_button.draw(self.screen)
        self.volume_button.draw(self.screen)
        self.music_button.draw(self.screen)
        self.draw_player()
        self.draw_text(
            f"Score: {self.score} + {self.bonus_score}",
            ((TILESIZE * 11) + 27, (TILESIZE * 1) + 30),
            pg.font.Font(VOLKSWAGEN_BOLD_FONT_PATH, 20),
        )
        self.draw_text(
            f"Solved Puzzles: {self.solved_puzzles}/8",
            ((TILESIZE * 12) - 10, (TILESIZE * 2) - 10),
            pg.font.Font(VOLKSWAGEN_BOLD_FONT_PATH, 20),
        )
        self.screen.blit(self.logo_image, ((TILESIZE * 8) + 35, -50))

        pg.display.flip()

    def grade(self):
        if self.score + self.bonus_score >= 3750:
            return "S"
        elif self.score + self.bonus_score > 3650 and self.score <= 3749:
            return "A"
        elif self.score + self.bonus_score > 3400 and self.score < 3650:
            return "B"
        else:
            return "C"

    def draw_end(self):
        self.screen.fill(BGCOLOR)
        self.end_exit_button.draw(self.screen)
        self.end_reset_button.draw(self.screen)
        self.screen.blit(self.end_logo_image, ((TILESIZE * 2) - 30, -100))
        self.draw_text(
            f"congrats your score is ",
            ((TILESIZE * 8) - 35, TILESIZE * 3),
            pg.font.Font(VOLKSWAGEN_BOLD_FONT_PATH, 20),
        )

        self.draw_text(
            f"{self.score + self.bonus_score}",
            ((TILESIZE * 7) - 10, TILESIZE * 4 - 30),
            pg.font.Font(VOLKSWAGEN_BOLD_FONT_PATH, 50),
        )

        self.draw_text(
            f"{self.grade()}",
            ((TILESIZE * 6) + 40, TILESIZE * 5 - 30),
            pg.font.Font(VOLKSWAGEN_BOLD_FONT_PATH, 120),
            color=YELLOW,
        )
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if self.exit_button.is_clicked(event) or self.end_exit_button.is_clicked(
                event
            ):
                self.quit()
            if self.reset_button.is_clicked(event) or self.end_reset_button.is_clicked(
                event
            ):
                self.reset()
            if event.type == pg.QUIT:
                self.quit()
            if self.playing:
                if self.volume_button.is_clicked(event):
                    self.is_mute = not self.is_mute
                if self.music_button.is_clicked(event):
                    if self.is_music_mute:
                        pg.mixer.music.unpause()
                    else:
                        pg.mixer.music.pause()
                    self.is_music_mute = not self.is_music_mute

                if event.type == pg.KEYDOWN:
                    if (
                        event.key == pg.K_LEFT or event.key == pg.K_a
                    ) and not self.player.is_moving:
                        self.player.move(dx=-1, direction="horizontal", heading="left")
                    if (
                        event.key == pg.K_RIGHT or event.key == pg.K_d
                    ) and not self.player.is_moving:
                        self.player.move(dx=1, direction="horizontal", heading="right")
                    if (
                        event.key == pg.K_UP or event.key == pg.K_w
                    ) and not self.player.is_moving:
                        self.player.move(dy=-1, direction="vertical", heading="up")
                    if (
                        event.key == pg.K_DOWN or event.key == pg.K_s
                    ) and not self.player.is_moving:
                        self.player.move(dy=1, direction="vertical", heading="down")


g = Game()
g.new()
while True:
    g.run()
