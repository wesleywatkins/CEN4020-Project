# import modules
try:
    import os
    import pygame
    import sys
    from gui.button import RoundedRect
    from gui.label import Label
    from scenes.gamestate import GameState
except ImportError as err:
    print("Couldn't load module. %s" % err)
    sys.exit(2)


class VictoryScreen(GameState):
    def __init__(self):
        super(VictoryScreen, self).__init__()
        self.next_state = "INITIAL"
        self.bg = pygame.image.load(os.path.join('assets', 'board.png')).convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (pygame.display.get_surface().get_width(),
                                                   pygame.display.get_surface().get_height()))
        self.bg_copy = self.bg
        self.bg_rect = self.bg.get_rect()
        self.bg_rect2 = self.bg.get_rect()
        self.bg1_x, self.bg2_x = 0, -self.bg_rect.width
        self.scroll_speed = 0.05
        self.menu_rect = RoundedRect(pygame.Rect(0, 0, 400, 500))
        self.menu_rect.rect.center = (pygame.display.get_surface().get_width()/2,
                                      pygame.display.get_surface().get_height()/2)
        self.title = Label("Victory!")
        self.title.set_pos((pygame.display.get_surface().get_width() / 2,
                            pygame.display.get_surface().get_height() * 0.5))

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True

    def update(self, dt):
        self.scroll_background(dt)

    def render(self, surface):
        surface.fill(pygame.Color("dodgerblue"))
        surface.blit(self.bg, self.bg_rect)
        surface.blit(self.bg, self.bg_rect2)
        self.menu_rect.render(surface)
        self.title.render(surface)

    def scroll_background(self, dt):
        distance = self.scroll_speed * dt
        self.bg1_x += distance
        self.bg2_x += distance
        if self.bg1_x >= self.bg_rect.width:
            self.bg1_x = -1 * self.bg_rect.width
        elif self.bg2_x >= self.bg_rect.width:
            self.bg2_x = -1 * self.bg_rect.width
        self.bg_rect.x = int(self.bg1_x)
        self.bg_rect2.x = int(self.bg2_x)