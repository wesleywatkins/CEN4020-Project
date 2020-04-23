try:
    import pygame
    import sys
    from gui.button import Button
except ImportError as err:
    print("Couldn't load module. %s" % err)
    sys.exit(2)


class ActionBar:

    # takes in a list of button names
    def __init__(self, x, y, width, height, buttons, font_size=23):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_size = font_size
        self.buttons = []
        self.update_buttons(buttons)

    def get_event(self, event):
        for b in self.buttons:
            if b.handle_event(event):
                return b.get_text()
        else:
            return None

    def update(self):
        for b in self.buttons:
            b.update()

    def render(self, surface):
        pygame.draw.rect(surface, pygame.Color("white"), (self.x, self.y, self.width, self.height))
        for b in self.buttons:
            b.render(surface)

    def update_buttons(self, buttons):
        self.buttons = []
        for (i, b) in enumerate(buttons):
            self.buttons.append(Button((i + 1) * self.width/(len(buttons) + 1), self.y + self.height/2))
            self.buttons[i].set_text(b, size=self.font_size)

    def disable_button(self, button):
        for b in self.buttons:
            if b.get_text() == button:
                b.enabled = False

    def disable_all(self):
        for b in self.buttons:
            b.enabled = False

    def enable_button(self, button):
        for b in self.buttons:
            if b.get_text() == button:
                b.enabled = True

    def enable_all(self):
        for b in self.buttons:
            b.enabled = True
