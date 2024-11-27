import pygame as pg


class ImageButton:
    def __init__(
        self,
        x,
        y,
        image_path,
        text,
        font,
        font_size,
        text_color=(0, 0, 0),
        hover_text_color=(255, 255, 255),
        icon_path=None,
        secondary_image_path=None,
        secondary_icon_path=None,
        scale=None,
    ):
        self.original_image = pg.image.load(image_path).convert_alpha()
        if secondary_image_path is not None:
            self.secondary_image = pg.image.load(secondary_image_path).convert_alpha()
        if scale is not None:
            self.original_image = pg.transform.scale(
                self.original_image, (scale[0], scale[1])
            )
        if scale is not None and secondary_icon_path is not None:
            self.secondary_image = pg.transform.scale(
                self.secondary_image, (scale[0], scale[1])
            )
        self.image = self.original_image
        self.original_rect = self.image.get_rect(topleft=(x, y))
        self.rect = self.original_rect.copy()
        self.font = pg.font.Font(font, font_size)
        self.text = text
        self.text_color = text_color
        self.hover_text_color = hover_text_color
        self.text_surf = self.font.render(text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        self.is_hovered = False
        self.icon_path = icon_path
        self.secondary_icon_path = secondary_icon_path
        self.is_active = True

        if self.icon_path is not None:
            self.icon = pg.image.load(icon_path).convert_alpha()
            self.icon_rect = self.icon.get_rect(center=self.rect.center)
            self.icon = pg.transform.scale(self.icon, (30, 30))

            self.primarily_icon = self.icon

            self.secondary_icon = pg.image.load(secondary_icon_path).convert_alpha()
            self.secondary_icon = pg.transform.scale(self.secondary_icon, (30, 30))

    def draw(self, screen):

        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.is_hovered = True
            self.elevate()
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
        else:
            self.is_hovered = False
            self.reset_elevation()
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

        screen.blit(self.image, self.rect.topleft)
        if self.icon_path is not None:
            screen.blit(self.icon, self.icon_rect.topleft)

        if self.is_hovered:
            self.text_surf = self.font.render(self.text, True, self.hover_text_color)
        else:
            self.text_surf = self.font.render(self.text, True, self.text_color)

        screen.blit(self.text_surf, self.text_rect)

    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pg.mouse.get_pos()):
                if self.icon_path is not None:
                    if self.is_active:
                        self.icon = self.secondary_icon
                        self.image = self.secondary_image
                        self.is_active = not self.is_active
                    else:
                        self.icon = self.primarily_icon
                        self.image = self.original_image
                        self.is_active = not self.is_active
                return True
        return False

    def elevate(self):
        image_to_elevate = (
            self.original_image if self.is_active else self.secondary_image
        )
        self.image = pg.transform.scale(
            image_to_elevate,
            (self.original_rect.width + 10, self.original_rect.height + 10),
        )
        self.rect = self.image.get_rect(center=self.original_rect.center)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        if self.icon_path is not None:
            self.icon_rect = self.icon.get_rect(center=self.rect.center)

    def reset_elevation(self):
        image_to_elevate = (
            self.original_image if self.is_active else self.secondary_image
        )
        self.image = image_to_elevate
        self.rect = self.original_rect.copy()
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        if self.icon_path is not None:
            self.icon_rect = self.icon.get_rect(center=self.rect.center)
