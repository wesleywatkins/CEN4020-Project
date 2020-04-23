try:
    import pygame
    import sys
    from gui.button import RoundedRect
    from gui.button import Button
    from gui.label import Label
except ImportError as err:
    print("Couldn't load module. %s" % err)
    sys.exit(2)


class Menu:

    def __init__(self, x=0, y=0, w=200, h=500, title='', buttons=None):
        # position and size
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        # buttons and title
        self.set_title(title)
        self.set_buttons(buttons)
        # create actual menu
        self.menu = RoundedRect(pygame.Rect(0, 0, w, h))
        self.menu.rect.center = self.x, self.y

        self.play_button = Button(pygame.display.get_surface().get_width() / 2,
                                  pygame.display.get_surface().get_height() * 0.4)
        self.play_button.set_text("Start Game", size=35)
        self.options_button = Button(pygame.display.get_surface().get_width() / 2,
                                     pygame.display.get_surface().get_height() * 0.55)
        self.options_button.set_text("Options", size=35)
        self.quit_button = Button(pygame.display.get_surface().get_width() / 2,
                                  pygame.display.get_surface().get_height() * 0.7)
        self.quit_button.set_text("Quit Game", size=35)

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
        self.menu.render(surface)
        self.title.render(surface)
        for b in self.buttons:
            b.render(surface)

    def set_title(self, title):
        self.title = Label(title)
        self.title.set_pos((self.x, int(self.y - self.h/2 + self.h * 0.15)))

    def set_pos(self, pos):
        self.x, self.y = pos
        self.menu.rect.center = self.x, self.y

    def set_buttons(self, buttons):
        self.buttons = []
        if not isinstance(buttons, list):
            return
        base = self.h * 0.15
        height = self.h - base
        base += self.y - self.h/2

        for (i, b) in enumerate(buttons):
            x = int(self.x)
            y = int(height * ((i + 1) / (len(buttons) + 1)) + base)
            self.buttons.append(Button(x, y))
            self.buttons[i].set_text(b, size=35)
