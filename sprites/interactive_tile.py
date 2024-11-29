import pygame as pg
from settings import *


class InteractiveTile(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.groups = game.all_sprites, game.tiles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(GRASS_TILE).convert_alpha()
        self.image = pg.transform.scale(self.image, (width, height))
        self.green_tile_image = self.load_image(GRASS_TILE, width, height)
        self.yellow_tile_image = self.load_image(DIRT_TILE, width, height)
        self.red_tile_image = self.load_image(ROCK_TILE, width, height)
        self.image = self.green_tile_image
        self.rect = self.image.get_rect()
        self.rect.x = x * width
        self.rect.y = y * height
        self.number_of_time_visited = 0

    def load_image(self, path, width, height):
        image = pg.image.load(path).convert_alpha()
        image = pg.transform.scale(image, (width, height))
        return image

    def add_number_of_visit(self):
        self.number_of_time_visited += 1
        if self.number_of_time_visited == 2:
            self.image = self.yellow_tile_image
        elif self.number_of_time_visited == 3:
            self.image = self.red_tile_image


