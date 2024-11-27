import pygame as pg
from settings import *


class Wall(pg.sprite.Sprite):
    def __init__(
        self,
        game,
        start_pos,
        end_pos,
        color,
        orientation,
        tiles,
        type="passive",
        id=None,
    ):
        if type == "passive":
            self.groups = game.all_sprites, game.walls
        else:
            self.groups = game.all_sprites, game.interactive_walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.color = color
        self.orientation = orientation
        self.tiles = tiles
        self.id = id

        self.min_x = min(start_pos[0], end_pos[0])
        self.min_y = min(start_pos[1], end_pos[1])
        self.max_x = max(start_pos[0], end_pos[0])
        self.max_y = max(start_pos[1], end_pos[1])

        if orientation == "vertical":
            self.image = pg.Surface(
                (5, (self.max_y * TILESIZE) - (self.min_y * TILESIZE)), pg.SRCALPHA
            )
            self.rect = self.image.get_rect()
            self.rect.topleft = ((self.min_x * TILESIZE), (self.min_y * TILESIZE))
            pg.draw.line(
                self.image,
                self.color,
                (
                    (start_pos[0] * TILESIZE) - (self.min_x * TILESIZE),
                    (start_pos[1] * TILESIZE) - (self.min_y * TILESIZE),
                ),
                (
                    (end_pos[0] * TILESIZE) - (self.min_x * TILESIZE),
                    (end_pos[1] * TILESIZE) - (self.min_y * TILESIZE),
                ),
                5,
            )

        if orientation == "horizontal":
            self.image = pg.Surface(
                ((self.max_x * TILESIZE) - (self.min_x * TILESIZE), 5), pg.SRCALPHA
            )
            self.rect = self.image.get_rect()
            self.rect.topleft = ((self.min_x * TILESIZE), (self.min_y * TILESIZE))
            pg.draw.line(
                self.image,
                self.color,
                (
                    (start_pos[0] * TILESIZE) - (self.min_x * TILESIZE),
                    (start_pos[1] * TILESIZE) - (self.min_y * TILESIZE),
                ),
                (
                    (end_pos[0] * TILESIZE) - (self.min_x * TILESIZE),
                    (end_pos[1] * TILESIZE) - (self.min_y * TILESIZE),
                ),
                5,
            )
