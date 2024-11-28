import pygame as pg
import os
from settings import *

class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coin_sprite
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        
        self.image = pg.image.load(COIN).convert_alpha()
        self.image = pg.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.centerx = x * TILESIZE + TILESIZE // 2
        self.rect.centery = y * TILESIZE + TILESIZE // 2
