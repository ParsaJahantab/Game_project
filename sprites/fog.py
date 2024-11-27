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
        # self.image = pg.image.load("assets/images/environment_15.png").convert_alpha()

        # self.image = pg.transform.scale(self.image, (TILESIZE*2, TILESIZE*3))
        self.image = pg.Surface((TILESIZE * 2, TILESIZE * 4))
        self.image.fill(DARKGREY)
        # self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.number_of_times_fog_visited = 0
        self.number_of_moves_in_the_fog = 0

    #     self.frames = []
    #     for file_name in sorted(os.listdir(frame_folder)):
    #         frame = pg.image.load(os.path.join(frame_folder, file_name)).convert_alpha()
    #         frame = pg.transform.scale(frame, (TILESIZE*4, TILESIZE*7))
    #         self.frames.append(frame)

    #     self.current_frame = 0
    #     self.last_updated = pg.time.get_ticks()
    #     self.image = self.frames[self.current_frame]
    #     self.rect = self.image.get_rect()
    #     self.rect.x = x * TILESIZE
    #     self.rect.y = y * TILESIZE

    # def update(self):
    #     now = pg.time.get_ticks()
    #     if now - self.last_updated > self.frame_rate:
    #         self.last_updated = now
    #         self.current_frame = (self.current_frame + 1) % len(self.frames)
    #         self.image = self.frames[self.current_frame]
