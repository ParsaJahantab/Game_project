import pygame as pg
from settings import *
from sprites.wall import *
from sprites.interactive_tile import *
from sprites.teleporter import *
from sprites.fog import *
from ui.utils.utils_functions import *


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.player_sprite
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_moving_right = self.load_image(
            [
                "assets/images/player/right_still.png",
                "assets/images/player/right_right.png",
                "assets/images/player/right_still.png",
                "assets/images/player/right_left.png",
            ]
        )
        self.image_moving_left = self.load_image(
            [
                "assets/images/player/left_still.png",
                "assets/images/player/left_right.png",
                "assets/images/player/left_still.png",
                "assets/images/player/left_left.png",
            ]
        )
        self.image_moving_up = self.load_image(
            [
                "assets/images/player/up_still.png",
                "assets/images/player/up_right.png",
                "assets/images/player/up_still.png",
                "assets/images/player/up_left.png",
            ]
        )
        self.image_moving_down = self.load_image(
            [
                "assets/images/player/down_still.png",
                "assets/images/player/down_right.png",
                "assets/images/player/down_still.png",
                "assets/images/player/down_left.png",
            ]
        )
        self.image = self.image_moving_right[0]
        self.current_images = self.image_moving_right
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.x = x
        self.y = y
        self.target_x = x * TILESIZE
        self.target_y = y * TILESIZE
        self.rect.x = self.target_x
        self.rect.y = self.target_y
        self.speed = 4
        self.is_player_in_fog = False
        self.gonna_clollide_with_fog = False
        self.fog: Fog = self.game.fog_sprite.sprites()[0]
        self.is_moving = False

        self.frame_index = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 125
        self.total_number_of_moves = 0
        self.moves_in_the_fog_in_one_go = 0
        self.enter_fog_pos = ()
        
        self.overlay_image = None
        self.overlay_start_time = None
        self.overlay_duration = 3000  
        self.display_text = ""

    def load_image(self, paths):
        images = []
        for path in paths:
            image = pg.image.load(path).convert_alpha()
            image = pg.transform.scale(image, (50, 50))
            images.append(image)
        return images

    def change_heading(self, heading):
        if heading == "left":
            self.current_images = self.image_moving_left
        elif heading == "right":
            self.current_images = self.image_moving_right
        elif heading == "up":
            self.current_images = self.image_moving_up
        elif heading == "down":
            self.current_images = self.image_moving_down

        self.image = self.current_images[0]

    def move(self, dx=0, dy=0, direction="vertical", heading="right"):
        if self.x == 8 and self.y == 4 and dx == 1:
            self.game.end_game()
            return

        collide_with_interactive_walls = self.collide_with_walls(
            dx, dy, wall_type="interactive", direction=direction
        )
        collide_with_passive_walls = self.collide_with_walls(
            dx, dy, wall_type="passive", direction=direction
        )
        self.gonna_clollide_with_fog = self.collide_with_fog(dx, dy)
        self.is_player_in_fog = self.is_in_fog()
        if self.gonna_clollide_with_fog and not self.is_player_in_fog:
            self.fog.number_of_times_fog_visited += 1
            self.moves_in_the_fog_in_one_go += 1
            self.enter_fog_pos = (self.x, self.y)
        elif self.gonna_clollide_with_fog and self.is_player_in_fog:
            self.moves_in_the_fog_in_one_go += 1
            if self.moves_in_the_fog_in_one_go > 10:
                self.check_fog()
                return
        if collide_with_interactive_walls[0]:
            self.puzzle(collide_with_interactive_walls[1])
        elif not collide_with_passive_walls[0]:
            collide_with_portal = self.collide_with_portal(dx, dy)
            if collide_with_portal[0]:
                self.x = collide_with_portal[1][0]
                if self.x == 2:
                    self.x = 3
                    self.moves_in_the_fog_in_one_go = 0
                self.y = collide_with_portal[1][1]
                if self.y == 6:
                    self.y = 5
                    self.moves_in_the_fog_in_one_go = 1
                    self.enter_fog_pos = (3, 0)
                self.teleport()
                return
            if self.collide_with_tiles(dx, dy):
                self.x += dx
                self.y += dy
                self.target_x = self.x * TILESIZE
                self.target_y = self.y * TILESIZE
                self.change_heading(heading)
                self.game.play_sound("walk")
                self.total_number_of_moves += 1
                self.collide_with_items()
                self.collide_with_shopkeeper()
            elif self.x == 6 and self.y == 0 and dy == -1:
                if self.check_for_teleport((1, 8)):
                    self.x = 1
                    self.y = 8
                    self.change_heading(heading)
                    self.teleport()
            elif self.x == 1 and self.y == 8 and dy == 1:
                if self.check_for_teleport((6, 0)):
                    self.x = 6
                    self.y = 0
                    self.change_heading(heading)
                    self.teleport()
            else:
                self.game.play_sound("error")

        elif collide_with_passive_walls[0]:
            self.game.play_sound("error")

    def check_for_teleport(self, endpos):
        return self.collide_with_tiles(endpos[0], endpos[1], "teleport")

    def teleport(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        self.target_x = self.rect.x
        self.target_y = self.rect.y
        self.game.play_sound("teleport")
        self.total_number_of_moves += 1

    def puzzle(self, sprite):
        self.game.play_puzzle(sprite)

    def check_fog(self):
        self.moves_in_the_fog_in_one_go = 0
        self.x = self.enter_fog_pos[0]
        self.y = self.enter_fog_pos[1]
        self.teleport()

    def collide_with_portal(self, dx, dy):
        self.hit_rect.x = self.x * TILESIZE + dx * TILESIZE
        self.hit_rect.y = self.y * TILESIZE + dy * TILESIZE
        for teleporter in self.game.teleporter:
            if self.hit_rect.colliderect(teleporter.rect):
                if teleporter.id == 1:
                    return (True, (6, 6))
                else:
                    return (True, (2, 0))
        return (False, None)

    def collide_with_fog(self, dx, dy):
        self.hit_rect.x = self.x * TILESIZE + dx * TILESIZE
        self.hit_rect.y = self.y * TILESIZE + dy * TILESIZE
        for fog in self.game.fog_sprite:
            if self.hit_rect.colliderect(fog.rect):
                return True
        return False

    def is_in_fog(self):
        self.hit_rect.x = self.x * TILESIZE
        self.hit_rect.y = self.y * TILESIZE
        for fog in self.game.fog_sprite:
            if self.hit_rect.colliderect(fog.rect):
                return True
        return False

    def collide_with_items(self):
        for item in self.game.items:
            if self.hit_rect.colliderect(item.rect):
                self.game.add_item(item)

                
    def collide_with_shopkeeper(self):
        shopkeeper = self.game.shopkeeper.sprites()[0]
        if self.hit_rect.colliderect(shopkeeper.rect):
            self.game.check_coin()

    def collide_with_tiles(self, dx=0, dy=0, type="normal"):
        if type == "normal":
            self.hit_rect.x = self.x * TILESIZE + dx * TILESIZE
            self.hit_rect.y = self.y * TILESIZE + dy * TILESIZE
        else:
            self.hit_rect.x = dx * TILESIZE
            self.hit_rect.y = dy * TILESIZE
        for tile in self.game.tiles:
            if self.hit_rect.colliderect(tile.rect):
                if (
                    self.gonna_clollide_with_fog
                    and self.fog.number_of_times_fog_visited <= 2
                    and self.game.has_torch
                ):
                    self.fog.number_of_moves_in_the_fog += 1
                    if not self.is_player_in_fog:
                        self.game.handel_score(-10)
                    return True
                elif self.gonna_clollide_with_fog and (
                    self.fog.number_of_times_fog_visited > 2 or not self.game.has_torch
                ):
                    if not self.game.has_torch:
                        self.display_overlay("I need a torch")
                    return False
                elif not self.gonna_clollide_with_fog and self.is_player_in_fog:
                    self.moves_in_the_fog_in_one_go = 0
                    if self.fog.number_of_moves_in_the_fog <= 2:
                        self.fog.number_of_moves_in_the_fog = 0
                        return True
                    self.fog.number_of_moves_in_the_fog = 0
                if tile.number_of_time_visited == 0:
                    self.game.handel_score(-10)
                    tile.add_number_of_visit()
                elif tile.number_of_time_visited == 1:
                    self.game.handel_score(-20)
                    tile.add_number_of_visit()
                elif tile.number_of_time_visited == 2:
                    self.game.handel_score(-30)
                    tile.add_number_of_visit()
                elif tile.number_of_time_visited == 3:
                    return False
                return True
        return False

    def collide_with_walls(self, dx=0, dy=0, wall_type="passive", direction="vertical"):
        if wall_type == "passive":
            sprite_type = self.game.walls
        else:
            sprite_type = self.game.interactive_walls
        if direction == "vertical":
            for wall in sprite_type:
                if wall.orientation == "horizontal":
                    if (
                        self.y in wall.tiles
                        and self.y + dy in wall.tiles
                        and self.x < wall.max_x
                        and self.x >= wall.min_x
                    ):
                        return (True, wall)
        else:
            for wall in sprite_type:
                if wall.orientation == "vertical":
                    if (
                        self.x in wall.tiles
                        and self.x + dx in wall.tiles
                        and self.y < wall.max_y
                        and self.y >= wall.min_y
                    ):
                        return (True, wall)
        return (False, None)

    def display_overlay(self, text):
            self.overlay_image = pg.Surface((150, 50), pg.SRCALPHA)  
            self.overlay_image.fill((0, 0, 0, 0))  
            self.display_text = text


            font = pg.font.Font(None, 16)  
            text_surface = font.render(text, True, WHITE)  
            text_rect = text_surface.get_rect(center=(50, 25))
            self.overlay_image.blit(text_surface, text_rect)

            self.overlay_start_time = pg.time.get_ticks()

    def change_animation(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.current_images)
            self.image = self.current_images[self.frame_index]

    def update(self):
        target_center_x = self.target_x + (TILESIZE - self.rect.width) // 2
        target_center_y = self.target_y + (TILESIZE - self.rect.height) // 2

        delta_x = target_center_x - self.rect.x
        delta_y = target_center_y - self.rect.y

        if delta_x != 0:
            self.rect.x += int(self.speed * (delta_x / abs(delta_x)))
            self.is_moving = True
            self.change_animation()

        if delta_y != 0:
            self.rect.y += int(self.speed * (delta_y / abs(delta_y)))
            self.is_moving = True
            self.change_animation()
        if delta_y == 0 and delta_x == 0:
            self.is_moving = False
            self.image = self.current_images[0]

        if abs(delta_x) < self.speed:
            self.rect.x = target_center_x
        if abs(delta_y) < self.speed:
            self.rect.y = target_center_y

        self.hit_rect.center = self.rect.center
        
        if self.overlay_image and self.overlay_start_time:
            current_time = pg.time.get_ticks()
            if current_time - self.overlay_start_time > self.overlay_duration:
                self.overlay_image = None  
                self.display_text = ""
            

    def draw(self, screen):
        screen.blit(self.image, self.rect)

            
    def draw_text(self, screen):
        if self.overlay_image:
            # if self.display_text == "I need a torch":
            #     self.display_text = f"I need a torch\nI can get it from shopkeeper"
            overlay_rect = self.overlay_image.get_rect(midbottom=self.rect.midtop)
            screen.blit(self.overlay_image, overlay_rect)
            draw_text(
            self.game,
            f"{self.display_text}",
            ((TILESIZE * 12) - 40, TILESIZE * 5+15),
            pg.font.Font(VOLKSWAGEN_BOLD_FONT_PATH, 10),
        )
            
