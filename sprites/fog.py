import pygame as pg
import os
from settings import *


class Fog(pg.sprite.Sprite):
    def __init__(self, game, x, y, frame_folder):
        self.groups = game.all_sprites, game.fog_sprite
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.frame_folder = frame_folder
        self.frame_rate = FPS
        self.image = pg.Surface((TILESIZE * 2, TILESIZE * 4))
        self.image.fill(DARKGREY)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.number_of_times_fog_visited = 0
        self.number_of_moves_in_the_fog = 0