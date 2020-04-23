try:
    import os
    import pygame
    import sys
except ImportError as err:
    print("Couldn't load module. %s" % err)
    sys.exit(2)


class Label:

    def __init__(self, text="", x=0, y=0, font_name='OpenSans-Regular.ttf', size=50, color=(0, 0, 0), justification='center'):
        self.x, self.y = x, y
        self.text = text
        self.font_name = font_name
        self.size = size
        self.color = color
        self.justification = justification
        self.font = pygame.font.Font(os.path.join('assets', 'fonts', self.font_name), self.size)
        # self.font = pygame.font.SysFont(font_name, size)
        self.surface = self.font.render(self.text, True, color)

    def render(self, screen):
        w, h = self.font.size(self.text)
        rect = pygame.Rect(0, 0, w, h)
        rect.center = self.x, self.y
        screen.blit(self.surface, rect)

    def update(self):
        self.font = pygame.font.Font(os.path.join('assets', 'fonts', self.font_name), self.size)
        self.surface = self.font.render(self.text, True, self.color)

    def get_pos(self):
        if self.justification == 'left':
            return self.x, self.y
        else:
            return int(self.x + self.surface.get_width()/2), int(self.y + self.surface.get_height()/2)

    def set_pos(self, pos):
        self.x, self.y = pos

    def set_color(self, color):
        self.color = color
        self.update()

    def set_regular(self):
        self.font.set_bold(0)
        self.font.set_italic(0)
        self.font.set_underline(0)

    def set_bold(self, value=5):
        self.font.set_bold(value)
        self.surface = self.font.render(self.text, True, self.color)

    def set_italic(self, value=5):
        self.font.set_italic(value)
        self.surface = self.font.render(self.text, True, self.color)

    def set_underline(self, value=5):
        self.font.set_underline(value)
        self.update()

    def set_text(self, text):
        self.text = text
        self.update()

    def set_size(self, size):
        self.size = size
        self.update()

    def set_font(self, font_name):
        self.font_name = font_name
        self.update()
