try:
    import pygame
    import sys
    import time
    from pygame import gfxdraw
except ImportError as err:
    print("Couldn't load module. %s" % err)
    sys.exit(2)


class RoundedRect:

    def __init__(self, rect=pygame.Rect(0, 0, 0, 0), bc=(0, 0, 0), fc=(255, 255, 255), rad=10, border=1):
        self.rect = rect
        self.border_color = bc
        self.fill_color = fc
        self.rad = rad
        self.border = border

    def render(self, surface):
        rect = pygame.Rect(self.rect)
        self._aa_render_region(surface, rect, self.border_color, self.rad)
        rect.inflate_ip(-2 * self.border, -2 * self.border)
        self._aa_render_region(surface, rect, self.fill_color, self.rad)

    def _aa_render_region(self, image, rect, color, rad):
        corners = rect.inflate(-2*rad-1, -2*rad-1)
        for attribute in ("topleft", "topright", "bottomleft", "bottomright"):
            x, y = getattr(corners, attribute)
            gfxdraw.aacircle(image, x, y, rad, color)
            gfxdraw.filled_circle(image, x, y, rad, color)
        image.fill(color, rect.inflate(-2*rad, 0))
        image.fill(color, rect.inflate(0, -2*rad))

    def set_border_color(self, color):
        self.border_color = color

    def set_fill_color(self, color):
        self.fill_color = color

    def set_border(self, border):
        if border >= 1:
            self.border = border


class Button:

    def __init__(self, x, y, delay=True):
        # set position
        self.x = x
        self.y = y
        # set font and size
        self.set_color()
        self.set_text("")
        self.padding = 20
        self.width = self.text.get_width() + self.padding
        self.height = self.text.get_height() + self.padding
        # flags
        self.hovering = False
        # timer to make sure button isn't spammed
        self.enabled = not delay
        self.created_time = time.time()
        self.initial_delay = delay
        # store text
        self.text_str = ''

    def handle_event(self, event):
        if self.enabled and event.type == pygame.MOUSEBUTTONUP:
            rect = self.get_rect()
            pos = pygame.mouse.get_pos()
            if rect.collidepoint(pos[0], pos[1]):
                return True
        return False

    def update(self):
        # enable button
        if self.initial_delay and not self.enabled and time.time() >= self.created_time + 1:
            self.enabled = True
            self.initial_delay = False
        # update width and height
        self.width = self.text.get_width() + self.padding
        self.height = self.text.get_height() + self.padding
        # create rect
        rect = pygame.Rect(0, 0, self.width, self.height)
        rect.center = self.x, self.y
        # check for hover
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            self.hovering = True
        else:
            self.hovering = False

    def render(self, screen):
        # draw rectangle
        rect = pygame.Rect(0, 0, self.width, self.height)
        rect.center = self.x, self.y
        color = self.hover_color if self.hovering else self.button_color
        if not self.initial_delay:
            color = color if self.enabled else self.disabled_color
        rr = RoundedRect(rect, bc=color, rad=15)
        if self.fill:
            rr.render(screen)
        else:
            rr.render(screen)
        # draw text
        rect = self.text.get_rect()
        rect.center = (self.x, self.y)
        screen.blit(self.text, rect)

    def set_color(self, text_color=(0, 0, 0), button_color=(200, 200, 200), fill=False):
        self.text_color = text_color
        self.button_color = button_color
        self.hover_color = pygame.Color('dodgerblue2')
        self.disabled_color = (179, 58, 58)
        self.fill = fill

    def set_text(self, string, font='lato', size=50):
        self.text_str = string
        self.font = pygame.font.SysFont(font, size)
        self.text = self.font.render(string, True, self.text_color)

    def get_rect(self):
        return pygame.Rect(int(self.x-self.width/2), int(self.y-self.height/2), self.width, self.height)

    def get_text(self):
        return self.text_str
