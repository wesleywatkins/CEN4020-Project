try:
    import os
    import pygame
    import sys
except ImportError as err:
    print("Couldn't load module. %s" % err)
    sys.exit(2)


class Board:

    def __init__(self):
        self.bg = pygame.image.load(os.path.join('assets', 'board.png'))
        self.bg = pygame.transform.scale(self.bg, (pygame.display.get_surface().get_width() - 100,
                                                   pygame.display.get_surface().get_height() - 100))
        self.bg_rect = self.bg.get_rect()
        self.bg_rect.center = (pygame.display.get_surface().get_width() / 2,
                               pygame.display.get_surface().get_height() / 2)

    def render(self, surface):
        surface.blit(self.bg, self.bg_rect)
