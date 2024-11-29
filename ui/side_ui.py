from settings import *
from ui.button import ImageButton
from ui.utils.utils_functions import *


def draw_side_ui(game, type="maze", puzzle=None):
    game.screen.blit(game.logo_image, ((TILESIZE * 8) + 35, -50))
    if type == "maze":
        draw_text(
            game,
            f"Score: {game.score} + {game.bonus_score}",
            ((TILESIZE * 11) + 27, (TILESIZE * 1) + 30),
            pg.font.Font(VOLKSWAGEN_BOLD_FONT_PATH, 20),
        )
        draw_text(
            game,
            f"Solved Puzzles: {game.solved_puzzles}/8",
            ((TILESIZE * 12) - 10, (TILESIZE * 2) - 10),
            pg.font.Font(VOLKSWAGEN_BOLD_FONT_PATH, 20),
        )
        draw_player(game)
    elif type == "battleship":
        draw_text(
            game,
            f"Shots Left: {puzzle.shots_left}",
            ((TILESIZE * 11) + 27, (TILESIZE * 1) + 30),
            pg.font.Font(VOLKSWAGEN_BOLD_FONT_PATH, 20),
        )
        draw_text(
            game,
            f"Time Left: {puzzle.time_left}",
            ((TILESIZE * 12) - 40, (TILESIZE * 2) - 10),
            pg.font.Font(VOLKSWAGEN_BOLD_FONT_PATH, 20),
        )
        draw_text(
            game,
            f"BLUE : undiscovered tiles",
            ((TILESIZE * 12), (TILESIZE * 3) - 20),
            pg.font.Font(VOLKSWAGEN_BOLD_FONT_PATH, 15),
        )
        draw_text(
            game,
            f"GRAY : ship tiles",
            ((TILESIZE * 12) - 40, (TILESIZE * 4) - 70),
            pg.font.Font(VOLKSWAGEN_BOLD_FONT_PATH, 15),
        )
        draw_text(
            game,
            f"RED : mine tiles",
            ((TILESIZE * 12) - 40, (TILESIZE * 5) - 120),
            pg.font.Font(VOLKSWAGEN_BOLD_FONT_PATH, 15),
        )
    
    if type == "maze":
        game.exit_button.draw(game.screen)
        game.reset_button.draw(game.screen)
        game.volume_button.draw(game.screen)
        game.music_button.draw(game.screen)
        
    if type == "battleship":
        puzzle.exit_button.draw(puzzle.screen)
        puzzle.volume_button.draw(puzzle.screen)
        puzzle.music_button.draw(puzzle.screen)
        

