import pygame as pg


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PINK = (159, 43, 104)
EDGE_BLUE = (16, 21, 36)

btn_color = '#7367F0'
success_color = '#28C76F'
error_color = '#FF4C51'
white_color = '#fff'


WIDTH = 850   
HEIGHT = 633  
FPS = 35
TITLE = "The Maze"
BGCOLOR = EDGE_BLUE

TILESIZE = 70
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

PLAYER_IMG = 'player.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)

VOLKSWAGEN_BOLD_FONT_PATH = "assets/fonts/Volkswagen-Bold.otf"

WALK_SOUND = "assets/sounds/maze/walk.mp3"
TELEPORT_SOUND = "assets/sounds/maze/teleport.wav"
WIN_SOUND = "assets/sounds/maze/win.wav"
SOULVE_PUZZLE_SOUND = "assets/sounds/maze/solving_puzzle.wav"
FAIL_PUZZLE_SOUND = "assets/sounds/maze/failing_puzzle.wav"
ERROR_SOUND = "assets/sounds/maze/error.mp3"
COIN_SOUND = "assets/sounds/maze/coin_sound.mp3"
HIT_SOUND = "assets/sounds/battleship/hit.mp3"
MINE_SOUND = "assets/sounds/battleship/mine.mp3"
MISS_SOUND = "assets/sounds/battleship/miss.mp3"

MAZE_MUSIC = "assets/music/background_music.mp3"
BATTLESHIP_MUSIC = "assets/music/battleship.mp3"

RED_BUTTON = "assets/images/buttons/red_button_image.png"
BLUE_BUTTON = "assets/images/buttons/blue_button_image.png"
GREEN_BUTTON = "assets/images/buttons/green_button.png"
GRAY_BUTTON = "assets/images/buttons/gray_button.png"

MUSIC_ICON = "assets/images/icons/music.png"
MUTE_ICON = "assets/images/icons/mute.png"
SLASH_ICON = "assets/images/icons/slash.png"
VOLUME_ICON = "assets/images/icons/volume.png"

CURSOR = "assets/images/cursor/cursor.png"

LOGO = "assets/images/logo/logo.png"

PORTAL = "assets/images/items/portal.png"
COIN = "assets/images/items/coin.png"
KEY = "assets/images/items/key.png"
SHOPKEEPER = "assets/images/shopkeeper/shopkeeper.png"

GRASS_TILE = "assets/images/ground/grass.png"
DIRT_TILE = "assets/images/ground/dirt.png"
ROCK_TILE = "assets/images/ground/rock.png"


SHIP_TILE = "assets/images/battleship/ship.png"
SEA_TILE = "assets/images/battleship/sea.png"
HIT_TILE = "assets/images/battleship/hit.png"
MISS_TILE = "assets/images/battleship/miss.png"
MINE_TILE = "assets/images/battleship/mine.png"
