# import modules
try:
    import pygame
    import sys
except ImportError as err:
    print("Couldn't load module. %s" % err)
    sys.exit(2)


class GameState(object):

    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.persist = {}
        self.font = pygame.font.Font(None, 24)

    def startup(self, persistent):
        self.persist = persistent

    def get_event(self, event):
        pass

    def update(self, dt):
        pass

    def render(self, surface):
        pass
