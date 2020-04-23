try:
    import pygame
    import sys
    from gui.label import Label
except ImportError as err:
    print("Couldn't load module. %s" % err)
    sys.exit(2)


class CircleLabel:

    def __init__(self, text='', x=0, y=0, rad=5, fc=(255, 255, 255), bc=(0, 0, 0), ai=False):
        self.x = x
        self.y = y
        self.label = Label(text, x, y, size=(rad-1))
        self.fill_color = fc
        self.border_color = bc
        self.radius = rad if rad > 5 else 5  # minimum radius is 5
        self.ai = ai

    def render(self, surface):
        pygame.draw.circle(surface, self.border_color, (self.x, self.y), self.radius)
        pygame.draw.circle(surface, self.fill_color, (self.x, self.y), self.radius - 3)
        if not self.ai:
            self.label.render(surface)

    def set_text(self, text):
        self.label.set_text(text)

    def set_pos(self, pos):
        self.x, self.y = pos

    def set_radius(self, radius):
        self.radius = radius

    def set_fill_color(self, fc):
        self.fill_color = fc

    def set_border_color(self, bc):
        self.border_color = bc
