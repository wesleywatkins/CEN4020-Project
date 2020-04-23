# import modules
try:
    import os
    import pygame
    import sys
    from components.menu import Menu
    from scenes.gamestate import GameState
except ImportError as err:
    print("Couldn't load module. %s" % err)
    sys.exit(2)


class SplashScreen(GameState):
    def __init__(self):
        super(SplashScreen, self).__init__()
        self.next_state = "INITIAL"
        self.bg = pygame.image.load(os.path.join('assets', 'board.png')).convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (pygame.display.get_surface().get_width(),
                                                   pygame.display.get_surface().get_height()))
        self.bg_copy = self.bg
        self.bg_rect = self.bg.get_rect()
        self.bg_rect2 = self.bg.get_rect()
        self.bg1_x, self.bg2_x = 0, -self.bg_rect.width
        self.scroll_speed = 0.05
        # set up menu
        self.menu = Menu(w=400, h=500)
        self.menu.set_pos((pygame.display.get_surface().get_width()/2, pygame.display.get_surface().get_height()/2))
        self.menu.set_title('Riskier')
        self.menu.set_buttons(['Start Game', 'Options', 'Quit Game'])

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif self.menu.get_event(event) == 'Start Game':
            self.persist_state()
            self.done = True
        elif self.menu.get_event(event) == 'Options':
            self.menu.set_title('Difficulty')
            self.menu.set_buttons(['Easy', 'Novice', 'Hard'])
        elif self.menu.get_event(event) == 'Quit Game':
            self.persist_state()
            self.quit = True
        elif self.menu.get_event(event) == 'Easy':
            self.persist['difficulty'] = 0
            self.menu.set_title('Riskier')
            self.menu.set_buttons(['Start Game', 'Options', 'Quit Game'])
        elif self.menu.get_event(event) == 'Novice':
            self.persist['difficulty'] = 1
            self.menu.set_title('Riskier')
            self.menu.set_buttons(['Start Game', 'Options', 'Quit Game'])
        elif self.menu.get_event(event) == 'Hard':
            self.persist['difficulty'] = 2
            self.menu.set_title('Riskier')
            self.menu.set_buttons(['Start Game', 'Options', 'Quit Game'])

    def update(self, dt):
        self.menu.update()
        self.scroll_background(dt)

    def render(self, surface):
        surface.fill(pygame.Color("dodgerblue"))
        surface.blit(self.bg, self.bg_rect)
        surface.blit(self.bg, self.bg_rect2)
        self.menu.render(surface)

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

    def persist_state(self):
        if 'difficulty' not in self.persist.keys():
            self.persist['difficulty'] = 0
