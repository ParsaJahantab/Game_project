import pygame as pg
import os
from settings import *

class Item(pg.sprite.Sprite):
    def __init__(self, game, x, y,path,type):
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = type
        self.original_image = pg.image.load(path).convert_alpha()
        self.original_image = pg.transform.scale(self.original_image, (60, 60))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = x * TILESIZE + TILESIZE // 2
        self.rect.centery = y * TILESIZE + TILESIZE // 2

        self.scale_factor = 1.0  
        self.last_pulse_time = 0  
        self.pulse_duration = 1000 
        self.growing = True  

    def update(self):

        current_time = pg.time.get_ticks()


        if current_time - self.last_pulse_time >= self.pulse_duration:
            self.last_pulse_time = current_time
            self.growing = not self.growing 

        step = 0.02  
        if self.growing:
            self.scale_factor += step
            if self.scale_factor >= 1.1:  
                self.scale_factor = 1.1
        else:
            self.scale_factor -= step
            if self.scale_factor <= 0.9: 
                self.scale_factor = 0.9

        new_size = int(60 * self.scale_factor)
        self.image = pg.transform.scale(self.original_image, (new_size, new_size))
        self.rect = self.image.get_rect(center=self.rect.center)

