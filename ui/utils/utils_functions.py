from settings import *
from ui.button import ImageButton
def draw_text(game, text, pos, font, color=WHITE):
        surf = font.render(text, True, color)
        rect = surf.get_rect(topright=(pos[0], pos[1]))
        game.screen.blit(surf, rect)
        
def draw_player(game):
        player_image_copy = game.player.image.copy()
        player_image_copy = pg.transform.scale(player_image_copy, (150, 150))
        game.screen.blit(player_image_copy, ((TILESIZE * 9) + 35, (TILESIZE * 3)))
        
def get_exit_button(type = "side",maze = True):
        exit_button = ImageButton(
            x = (TILESIZE * 9) + 15 if type == "side" else (TILESIZE * 4) - 10,
            y= TILESIZE * 8,
            image_path=RED_BUTTON,
            text="Exit Game" if maze else "Exit Puzzle",
            font=VOLKSWAGEN_BOLD_FONT_PATH,
            font_size=16,
            text_color=(0, 0, 0),
            hover_text_color=(255, 255, 255),
            scale=None if type == "side" else (300, 60)
        )
        return exit_button
        
        
def get_reset_button(type = "side"):
        reset_button = ImageButton(
            x = (TILESIZE * 9) + 15 if type == "side" else (TILESIZE * 4) - 10,
            y = TILESIZE * 7,
            image_path=BLUE_BUTTON,
            text="Reset Game",
            font=VOLKSWAGEN_BOLD_FONT_PATH,
            font_size= 16,
            text_color=(0, 0, 0),
            hover_text_color=(255, 255, 255),
            scale=None if type == "side" else (300, 60)
        )
        return reset_button
    
def get_volume_button(type="maze"):
        y = 6 if type=="maze" else 7
        volume_button = ImageButton(
            (TILESIZE * 9) + 15,
            TILESIZE * y,
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
        return volume_button
    
def get_music_button(type = "maze"):
    y = 6 if type=="maze" else 7
    music_button = ImageButton(
        (TILESIZE * 9) + 120,
        TILESIZE * y,
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
    return music_button
        