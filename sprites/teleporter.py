import pygame as pg
from settings import *


class Portal(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height, id):
        self.groups = game.all_sprites, game.teleporter
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.id = id
        self.image = pg.image.load(PORTAL).convert_alpha()
        self.image = pg.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE + (TILESIZE - width) // 2
        self.rect.y = y * TILESIZE + (TILESIZE - height) // 2


